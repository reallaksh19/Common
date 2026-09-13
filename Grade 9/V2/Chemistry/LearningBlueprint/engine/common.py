from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


class BlueprintError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_routing_policy() -> dict[str, Any]:
    return load_json(ROOT / "policies" / "adaptive-routing-policy.json")


def load_assimilation_policy() -> dict[str, Any]:
    return load_json(ROOT / "policies" / "assimilation-policy.json")


def load_transfer_policy() -> dict[str, Any]:
    return load_json(ROOT / "policies" / "transfer-eligibility-policy.json")
