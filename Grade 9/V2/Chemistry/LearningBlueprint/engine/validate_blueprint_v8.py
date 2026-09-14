#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


class BlueprintV8Error(ValueError):
    pass


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _task_key(packet: dict) -> str:
    task = packet["task_type"]
    mode = packet["product_mode"]
    if task == "CORE_GENERATION":
        if mode not in {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
            raise BlueprintV8Error("CHEM_V8_CORE_GENERATION_PRODUCT_MODE_INVALID")
        return f"CORE_GENERATION_{mode}"
    if task == "TTU_DESIGN":
        if mode in {"CORE1A", "CORE1B"}:
            return "TTU_DESIGN_CONCEPT"
        if mode in {"CORE2A", "CORE2B"}:
            return "TTU_DESIGN_PROBLEM"
        raise BlueprintV8Error("CHEM_V8_TTU_DESIGN_PRODUCT_MODE_INVALID")
    return task


def validate(packet: dict, policy: dict) -> dict:
    required = {
        "schema_version", "execution_id", "subject", "task_type", "product_mode",
        "authority_refs", "authority_sources_used", "output_bindings",
        "missing_authority_action", "execution_status"
    }
    missing_fields = sorted(required - set(packet))
    if missing_fields:
        raise BlueprintV8Error("CHEM_V8_EXECUTION_FIELD_MISSING:" + ",".join(missing_fields))
    if packet["schema_version"] != "8.0.0" or packet["subject"] != "CHEMISTRY":
        raise BlueprintV8Error("CHEM_V8_EXECUTION_IDENTITY_INVALID")
    if packet["task_type"] not in policy["task_types"]:
        raise BlueprintV8Error("CHEM_V8_TASK_TYPE_INVALID")
    if packet["missing_authority_action"] != "BLOCK":
        raise BlueprintV8Error("CHEM_V8_MISSING_AUTHORITY_MUST_BLOCK")

    used = set(packet["authority_sources_used"])
    forbidden = used & set(policy["forbidden_authority_sources"])
    if forbidden:
        raise BlueprintV8Error("CHEM_V8_MEMORY_OR_UNTRACED_AUTHORITY_FORBIDDEN:" + ",".join(sorted(forbidden)))
    illegal = used - set(policy["allowed_authority_sources"])
    if illegal:
        raise BlueprintV8Error("CHEM_V8_UNKNOWN_AUTHORITY_SOURCE:" + ",".join(sorted(illegal)))

    refs = packet["authority_refs"]
    if not isinstance(refs, list) or not refs:
        raise BlueprintV8Error("CHEM_V8_AUTHORITY_REFS_MISSING")
    types = set()
    ref_ids = set()
    for item in refs:
        if not isinstance(item, dict) or not str(item.get("authority_type", "")).strip() or not str(item.get("ref", "")).strip():
            raise BlueprintV8Error("CHEM_V8_AUTHORITY_REF_INVALID")
        types.add(item["authority_type"])
        ref_ids.add(item["ref"])

    key = _task_key(packet)
    required_types = set(policy["task_requirements"].get(key, []))
    missing_types = sorted(required_types - types)

    bindings = packet["output_bindings"]
    if not isinstance(bindings, list):
        raise BlueprintV8Error("CHEM_V8_OUTPUT_BINDINGS_INVALID")
    legal_classes = set(policy["output_binding_rule"]["technical_object_classes"])
    for binding in bindings:
        if not isinstance(binding, dict):
            raise BlueprintV8Error("CHEM_V8_OUTPUT_BINDING_INVALID")
        if binding.get("object_class") not in legal_classes:
            raise BlueprintV8Error("CHEM_V8_OUTPUT_OBJECT_CLASS_INVALID")
        if not str(binding.get("output_id", "")).strip() or not str(binding.get("authority_ref", "")).strip():
            raise BlueprintV8Error("CHEM_V8_OUTPUT_BINDING_INCOMPLETE")
        if binding["authority_ref"] not in ref_ids:
            raise BlueprintV8Error("CHEM_V8_OUTPUT_AUTHORITY_REF_UNRESOLVED:" + binding["output_id"])

    status = packet["execution_status"]
    if status not in {"READY", "BLOCKED"}:
        raise BlueprintV8Error("CHEM_V8_EXECUTION_STATUS_INVALID")
    if missing_types:
        if status != "BLOCKED":
            raise BlueprintV8Error("CHEM_V8_REQUIRED_BLUEPRINT_AUTHORITY_MISSING:" + ",".join(missing_types))
        if not packet.get("blocked_reasons"):
            raise BlueprintV8Error("CHEM_V8_BLOCKED_REASON_MISSING")
        return {"status": "BLOCKED", "missing_authority_types": missing_types}
    if status == "BLOCKED":
        if not packet.get("blocked_reasons"):
            raise BlueprintV8Error("CHEM_V8_BLOCKED_REASON_MISSING")
        return {"status": "BLOCKED", "missing_authority_types": []}

    return {
        "status": "READY",
        "task_key": key,
        "authority_types": sorted(types),
        "bound_output_count": len(bindings),
        "memory_authority_used": False
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", required=True)
    ap.add_argument("--packet", required=True)
    args = ap.parse_args()
    try:
        result = validate(load(args.packet), load(args.policy))
    except BlueprintV8Error as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
