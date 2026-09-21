import json
import re
import uuid
from .audit import AuditStore
from .models import ToolResult
from .policy import PolicyEngine
from .router import ModelRouter

TOOL_PATTERN = re.compile(r"TOOL\((?P<name>[a-zA-Z0-9_.:-]+)\)\s*(?P<args>\{.*?\})?", re.S)

class Agent:
    """Small deterministic agent loop.

    The model may propose a tool call using:
      TOOL(name) {"key":"value"}
    The policy engine, not the model, decides whether execution is permitted.
    Actual MCP execution can be attached behind ToolExecutor.
    """

    def __init__(self, router: ModelRouter, policy: PolicyEngine, audit: AuditStore):
        self.router = router
        self.policy = policy
        self.audit = audit

    async def run(self, message: str, max_steps: int = 5, provider: str | None = None):
        trace_id = "tr_" + uuid.uuid4().hex
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an X4 agent. You may propose tools only with "
                    "TOOL(name) {json}. Never claim a tool ran unless a tool result "
                    "is supplied. Be explicit about uncertainty."
                ),
            },
            {"role": "user", "content": message},
        ]
        for _ in range(max_steps):
            result = await self.router.chat(messages, provider)
            match = TOOL_PATTERN.search(result.content)
            if not match:
                return {"trace_id": trace_id, "content": result.content, "steps": len(messages)}
            name = match.group("name")
            raw_args = match.group("args") or "{}"
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
            decision = self.policy.decide(name)
            tool_result = ToolResult(
                name=name,
                decision=decision.action,
                error=None if decision.action != "deny" else decision.reason,
            )
            self.audit.write({
                "trace_id": trace_id,
                "event": "tool_decision",
                "tool": name,
                "arguments_hash": self.audit.fingerprint(args),
                "decision": decision.action,
                "reason": decision.reason,
            })
            if decision.action != "allow":
                messages.append({"role": "assistant", "content": result.content})
                messages.append({
                    "role": "tool",
                    "content": json.dumps(tool_result.model_dump()),
                })
                continue
            # Placeholder: real tool execution must be explicitly wired to an
            # approved connector. We never execute arbitrary model-provided commands.
            messages.append({"role": "assistant", "content": result.content})
            messages.append({
                "role": "tool",
                "content": json.dumps({
                    "name": name,
                    "decision": "allow",
                    "output": "Tool executor not attached; no external action performed.",
                }),
            })
        return {
            "trace_id": trace_id,
            "content": "Maximum agent steps reached.",
            "steps": max_steps,
        }
