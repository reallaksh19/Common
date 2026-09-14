#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_engineering_gates_v2 import GateValidationError, load as load_gate, validate as validate_registry  # noqa: E402


class BindingValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def fail(code: str, message: str):
    raise BindingValidationError(code, message)


def physics_prereq_closure(gate_map: dict, gate_id: str) -> set[str]:
    if gate_id not in gate_map:
        fail("E_BIND_PRIMARY_UNKNOWN", f"unknown primary gate {gate_id}")
    seen: set[str] = set()

    def walk(gid: str):
        if gid in seen:
            return
        seen.add(gid)
        for prereq in gate_map[gid]["prerequisites"]:
            if prereq.startswith("PHY-"):
                if prereq not in gate_map:
                    fail("E_BIND_PREREQ_UNKNOWN", f"{gid} references unknown Physics prerequisite {prereq}")
                walk(prereq)

    walk(gate_id)
    return seen


def validate(binding: dict) -> dict:
    try:
        schema = load("contracts/physics-technical-gate-binding.schema.json")
        jsonschema.validate(binding, schema)
    except jsonschema.ValidationError as exc:
        fail("E_BIND_SCHEMA", exc.message)

    registry = load_gate(binding["registry_ref"])
    try:
        validate_registry(registry)
    except GateValidationError as exc:
        fail("E_BIND_REGISTRY_INVALID", f"{exc.code}: {exc.message}")

    gate_map = {g["subtopic_id"]: g for g in registry["gates"]}
    primary = gate_map.get(binding["primary_gate_id"])
    if primary is None:
        fail("E_BIND_PRIMARY_UNKNOWN", binding["primary_gate_id"])

    if binding["bucket_id"] not in primary["linked_buckets"]:
        fail("E_BIND_BUCKET_NOT_LINKED", f"{binding['bucket_id']} is not linked by {binding['primary_gate_id']}")

    computed = physics_prereq_closure(gate_map, binding["primary_gate_id"])
    declared = set(binding["declared_gate_closure"])
    if declared != computed:
        missing = sorted(computed - declared)
        extra = sorted(declared - computed)
        fail("E_BIND_CLOSURE_MISMATCH", f"missing={missing} extra={extra}")

    blocked = [gid for gid in sorted(computed) if gate_map[gid]["status"] != "ENGINEERING_GATE_READY"]
    if blocked:
        fail("E_BIND_GATE_NOT_READY", f"technical closure contains non-ready gates: {blocked}")

    if binding["status"] != "TECHNICAL_GATE_READY":
        fail("E_BIND_STATUS_MISMATCH", "all technical gates are ready but binding status is not READY")

    # Important authority boundary: technical readiness does not resolve frozen-source custody.
    if binding.get("source_item_status") == "SOURCE_HELD" and "PUBLICATION" in binding["downstream_consumers"]:
        source_custody_note = "technical-ready/source-held: publication must still obey CCU/Core2 source gate"
    else:
        source_custody_note = "technical readiness only"

    return {
        "status": "PASS",
        "binding_id": binding["binding_id"],
        "bucket_id": binding["bucket_id"],
        "primary_gate_id": binding["primary_gate_id"],
        "gate_closure": sorted(computed),
        "source_item_status": binding.get("source_item_status"),
        "authority_note": source_custody_note,
    }


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "topics/m2d-sba23-technical-gate-binding.v1.json"
    print(json.dumps(validate(load(rel)), indent=2))


if __name__ == "__main__":
    main()
