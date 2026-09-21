import hashlib
import json
import time
import uuid
from pathlib import Path
from typing import Any

class AuditStore:
    def __init__(self, jsonl_path: str):
        self.path = Path(jsonl_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def fingerprint(value: Any) -> str:
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
        return "sha256:" + hashlib.sha256(raw).hexdigest()

    def write(self, event: dict[str, Any]) -> dict[str, Any]:
        event = {
            "timestamp": time.time(),
            "event_id": "evt_" + uuid.uuid4().hex,
            **event,
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, separators=(",", ":"), default=str) + "\n")
        return event
