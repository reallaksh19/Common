#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_engineering_gates_v2 import GateValidationError, load as load_gate, validate as validate_registry  # noqa: E402
from compile_engineering_closure import canonical_digest, compile_closure  # noqa: E402


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


def validate_v1(binding: dict) -> dict:
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
        fail("E_BIND_CLOSURE_MISMATCH", f"missing={sorted(computed-declared)} extra={sorted(declared-computed)}")
    blocked = [gid for gid in sorted(computed) if gate_map[gid]["status"] != "ENGINEERING_GATE_READY"]
    if blocked:
        fail("E_BIND_GATE_NOT_READY", f"technical closure contains non-ready gates: {blocked}")
    if binding["status"] != "TECHNICAL_GATE_READY":
        fail("E_BIND_STATUS_MISMATCH", "all technical gates are ready but binding status is not READY")

    source_custody_note = (
        "technical-ready/source-held: publication must still obey CCU/Core2 source gate"
        if binding.get("source_item_status") == "SOURCE_HELD" and "PUBLICATION" in binding["downstream_consumers"]
        else "technical readiness only"
    )
    return {
        "status": "PASS", "binding_id": binding["binding_id"], "bucket_id": binding["bucket_id"],
        "primary_gate_id": binding["primary_gate_id"], "gate_closure": sorted(computed),
        "source_item_status": binding.get("source_item_status"), "authority_note": source_custody_note,
        "binding_mode": "LEGACY_DECLARED_CLOSURE"
    }


def compile_bound_receipt(binding: dict, *, registry: dict | None = None) -> dict:
    request = load(binding["engineering_request_ref"])
    manifest = load(binding["engineering_manifest_ref"])
    if manifest.get("scope_kind") != "BUCKET" or manifest.get("scope_ref") != binding["bucket_id"]:
        fail("E_BIND_BUCKET_SCOPE_MISMATCH", f"manifest scope {manifest.get('scope_kind')}:{manifest.get('scope_ref')} does not bind {binding['bucket_id']}")
    if binding["primary_gate_id"] not in manifest.get("required_gate_ids", []):
        fail("E_BIND_PRIMARY_NOT_DIRECT", f"{binding['primary_gate_id']} is not a direct gate in the engineering manifest")

    try:
        receipt = compile_closure(request, manifest, registry=registry)
    except Exception as exc:
        fail("E_BIND_CLOSURE_RECOMPILE_FAILED", str(exc))
    if receipt["closure_status"] != "READY":
        fail("E_BIND_GATE_NOT_READY", f"current Workbench closure is {receipt['closure_status']}")
    if receipt["receipt_id"] != binding["closure_receipt_id"]:
        fail("E_BIND_RECEIPT_ID_MISMATCH", f"expected {binding['closure_receipt_id']} got {receipt['receipt_id']}")
    return receipt


def validate_v2(binding: dict) -> dict:
    try:
        schema = load("contracts/physics-technical-gate-binding-v2.schema.json")
        jsonschema.validate(binding, schema)
    except jsonschema.ValidationError as exc:
        fail("E_BIND_SCHEMA", exc.message)

    receipt = compile_bound_receipt(binding)
    actual_receipt_digest = canonical_digest(receipt)
    if actual_receipt_digest != binding["closure_receipt_digest"]:
        fail("E_BIND_RECEIPT_DIGEST_MISMATCH", f"expected {binding['closure_receipt_digest']} got {actual_receipt_digest}")
    if receipt["closure_digest"] != binding["closure_logic_digest"]:
        fail("E_BIND_CLOSURE_DIGEST_MISMATCH", f"expected {binding['closure_logic_digest']} got {receipt['closure_digest']}")
    if receipt["registry_digest"] != binding["registry_digest"]:
        fail("E_BIND_REGISTRY_DIGEST_MISMATCH", f"expected {binding['registry_digest']} got {receipt['registry_digest']}")

    return {
        "status": "PASS",
        "binding_id": binding["binding_id"],
        "bucket_id": binding["bucket_id"],
        "primary_gate_id": binding["primary_gate_id"],
        "gate_closure": list(receipt["transitive_gate_ids"]),
        "source_item_status": receipt["source_item_status"],
        "authority_note": "legacy v2 custody pins the whole Workbench receipt and aggregate registry; source/legal state remains independent",
        "binding_mode": "EXACT_WORKBENCH_CLOSURE_RECEIPT",
        "closure_receipt_id": receipt["receipt_id"],
        "closure_receipt_digest": actual_receipt_digest,
        "closure_logic_digest": receipt["closure_digest"],
        "registry_digest": receipt["registry_digest"],
    }


def validate_v3(binding: dict, *, registry: dict | None = None) -> dict:
    try:
        schema = load("contracts/physics-technical-gate-binding-v3.schema.json")
        jsonschema.validate(binding, schema)
    except jsonschema.ValidationError as exc:
        fail("E_BIND_SCHEMA", exc.message)

    receipt = compile_bound_receipt(binding, registry=registry)
    actual_scoped_digest = receipt["scoped_closure_digest"]
    if actual_scoped_digest != binding["scoped_closure_digest"]:
        fail(
            "E_BIND_SCOPED_CLOSURE_DIGEST_MISMATCH",
            f"expected {binding['scoped_closure_digest']} got {actual_scoped_digest}",
        )

    return {
        "status": "PASS",
        "binding_id": binding["binding_id"],
        "bucket_id": binding["bucket_id"],
        "primary_gate_id": binding["primary_gate_id"],
        "gate_closure": list(receipt["transitive_gate_ids"]),
        "source_item_status": receipt["source_item_status"],
        "authority_note": "active technical custody pins the exact scoped closure; aggregate registry digest is provenance only and source/legal state remains independent",
        "binding_mode": "SCOPED_WORKBENCH_CLOSURE_RECEIPT",
        "closure_receipt_id": receipt["receipt_id"],
        "scoped_closure_digest": actual_scoped_digest,
        "registry_digest": receipt["registry_digest"],
        "aggregate_registry_custody": "PROVENANCE_ONLY",
    }


def validate(binding: dict) -> dict:
    version = binding.get("schema_version")
    if version == "3.0.0":
        return validate_v3(binding)
    if version == "2.0.0":
        return validate_v2(binding)
    if version == "1.0.0":
        return validate_v1(binding)
    fail("E_BIND_SCHEMA", f"unsupported binding schema_version {version}")


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "topics/m2d-sba23-technical-gate-binding.v3.json"
    print(json.dumps(validate(load(rel)), indent=2))


if __name__ == "__main__":
    main()
