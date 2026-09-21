from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Decision:
    action: str
    reason: str

class PolicyEngine:
    """Deny-by-default tool policy.

    Explicit read-only registrations can be allowed. Risky/network/destructive
    tools require a separately supplied approval token.
    """

    def __init__(self) -> None:
        self.read_only: set[str] = set()
        self.risky_words = {
            "delete", "remove", "destroy", "drop", "shutdown", "execute",
            "shell", "write_file", "send_email", "publish", "payment",
        }
        self.network_words = {"http", "request", "browser", "web", "fetch"}

    def register_read_only(self, tool_name: str) -> None:
        self.read_only.add(tool_name)

    def decide(self, tool_name: str, approval: str | None = None) -> Decision:
        name = tool_name.lower()
        if tool_name in self.read_only:
            return Decision("allow", "explicit-read-only-registration")
        if any(word in name for word in self.risky_words | self.network_words):
            if approval:
                return Decision("allow", "explicit-approval-token")
            return Decision("approval", "risky-or-network-tool")
        return Decision("deny", "unknown-tool")
