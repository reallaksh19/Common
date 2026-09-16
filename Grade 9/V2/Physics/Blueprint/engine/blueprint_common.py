#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTRACTS = ROOT / "contracts"

EVIDENCE_STATES = {"PRESENT", "ABSENT", "PARTIAL", "UNRESOLVED", "CONFLICTED"}
GROUND_TRUTH_AUTHORITIES = {"ORIGINAL_EVIDENCE", "AUTHORITATIVE_SOURCE"}
RUN_STATES = {
    "GT_READY", "ROUTED", "FIRST_CORE_COMPLETE", "SECOND_CORE_COMPLETE",
    "CROSS_VALIDATED", "JOIN_READY", "ASSIMILATION_COMPILED", "CORE1A_REALIZED",
    "EXPOSURE_RECORDED", "CORE2A_ELIGIBLE", "CORE2A_REALIZED", "FINAL_AUDIT_PASS",
    "BLOCKED_EVIDENCE", "BLOCKED_CONFLICT", "BLOCKED_PREREQUISITE",
    "BLOCKED_REPRESENTATION", "BLOCKED_EXPOSURE", "BLOCKED_OWNER_REVIEW",
}
RUN_ID_RE = re.compile(r"^PHY-PLR-[0-9a-f]{16}$")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def file_digest(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: str | Path) -> dict:
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    return json.loads(target.read_text(encoding="utf-8"))


def validate_schema(instance: dict, schema_name: str) -> None:
    schema = load(CONTRACTS / schema_name)
    jsonschema.validate(instance, schema)


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)
