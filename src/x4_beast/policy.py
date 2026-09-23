from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Decision:
    action: str          # allow | deny | approval
    reason: str

class PolicyEngine:
    """Deny-by-default tool policy with Beast Mode autonomy levels.

    Levels:
      0 Observe          – read-only, no execution
      1 Assist           – read + plan + patch + open PR (approval for risky)
      2 Governed Autopilot – plan → policy → execute → verify → recover/autofix (hard limits)
      3 Never            – block all high-impact actions
    """

    def __init__(self, autonomy_level: int = 1, autofix_enabled: bool = True) -> None:
        self.autonomy_level = max(0, min(3, autonomy_level))
        self.autofix_enabled = autofix_enabled
        self.read_only: set[str] = set()
        self.risky_words = {
            "delete", "remove", "destroy", "drop", "shutdown", "execute",
            "shell", "write_file", "send_email", "publish", "payment",
            "autofix", "apply_patch",
        }
        self.network_words = {"http", "request", "browser", "web", "fetch"}

    def register_read_only(self, tool_name: str) -> None:
        self.read_only.add(tool_name)

    def decide(self, tool_name: str, approval: str | None = None) -> Decision:
        name = tool_name.lower()

        # Level 0: pure observe – deny everything except explicit read-only
        if self.autonomy_level == 0:
            if tool_name in self.read_only:
                return Decision("allow", "level-0-read-only")
            return Decision("deny", "level-0-observe-only")

        # Level 3: never autonomous for high-impact
        if self.autonomy_level == 3 and any(w in name for w in self.risky_words):
            return Decision("deny", "level-3-never-autonomous")

        if tool_name in self.read_only:
            return Decision("allow", "explicit-read-only-registration")

        is_risky = any(word in name for word in self.risky_words | self.network_words)

        if is_risky:
            # Autofix only allowed when explicitly enabled and level >= 2
            if "autofix" in name or "apply_patch" in name:
                if not self.autofix_enabled:
                    return Decision("deny", "autofix-disabled")
                if self.autonomy_level < 2:
                    return Decision("approval", "autofix-requires-level-2-or-approval")

            if approval:
                return Decision("allow", "explicit-approval-token")
            return Decision("approval", "risky-or-network-tool")

        return Decision("deny", "unknown-tool")
