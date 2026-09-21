import json
from pathlib import Path
from typing import Any

class MCPManager:
    """Configuration-first MCP registry.

    This layer deliberately does not execute arbitrary MCP processes by itself.
    It provides discovery metadata and a safe place to integrate an official
    MCP client SDK or a separately sandboxed connector.
    """

    def __init__(self, config_path: str = "config/mcp.json"):
        self.path = Path(config_path)

    def servers(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8")).get("servers", {})

    def summary(self) -> list[dict[str, Any]]:
        return [
            {"name": name, "command": cfg.get("command"), "args": cfg.get("args", [])}
            for name, cfg in self.servers().items()
        ]
