#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load  # noqa: E402
from validate_chemistry_gate_source_audit import validate as validate_source_audit  # noqa: E402

SCOPE_SCHEMA_REL = "contracts/chemistry-core-source-scope.schema.json"
AUTH_SCHEMA_REL = "contracts/chemistry-core-authority.schema.json"


class ChemistryCoreSourceScopeError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryCoreSourceScopeError(code, message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def _digest_without(obj: dict[str, Any], field: str) -> str:
    payload = copy.deepcopy(obj)
    payload.pop(field, None)
    return digest(payload)


def validate_core_source_scope(
    scope: dict[str, Any],
    audit: dict[str, Any],
    authority: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    try:
        jsonschema.validate(scope, load(SCOPE_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_CORE_SCOPE_SCHEMA", exc.message)
    try:
        jsonschema.validate(authority, load(AUTH_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_CORE_SCOPE_AUTHORITY_SCHEMA", exc.message)
    if authority["authority_digest"] != _digest_without(authority, "authority_digest"):
        fail("CHEM_CORE_SCOPE_AUTHORITY_DIGEST_MISMATCH")

    audit_result = validate_source_audit(audit, registry)
    if audit_result["audit_role"] != "PRODUCTION_SOURCE_AUDIT":
        fail("CHEM_CORE_SCOPE_STRESS_AUDIT_NOT_AUTHORITY")
    if audit_result["audit_status"] != "SOURCE_HARDENED":
        fail("CHEM_CORE_SCOPE_AUDIT_NOT_HARDENED")
    if scope["source_audit_digest"] != digest(audit):
        fail("CHEM_CORE_SCOPE_AUDIT_DIGEST_MISMATCH")
    if scope["gate_id"] != audit["gate_id"]:
        fail("CHEM_CORE_SCOPE_GATE_MISMATCH")
    if scope["subtopic_id"] != authority["subtopic_id"]:
        fail("CHEM_CORE_SCOPE_SUBTOPIC_MISMATCH")
    if scope["product_mode"] != authority["product_mode"]:
        fail("CHEM_CORE_SCOPE_MODE_MISMATCH")

    tier_map = {row["tier_id"]: row for row in audit["scope_tiers"]}
    authorized = set(scope["authorized_scope_tiers"])
    held = set(scope["held_scope_tiers"])
    if authorized & held:
        fail("CHEM_CORE_SCOPE_TIER_DUAL_STATE")
    if authorized | held != set(tier_map):
        fail("CHEM_CORE_SCOPE_TIER_PARTITION_INCOMPLETE")

    higher = sorted(tier for tier in authorized if tier_map[tier]["minimum_learner_grade"] > scope["learner_grade"])
    if higher and (not scope["extension_authority_ref"].strip() or not scope["extension_reason"].strip()):
        fail("CHEM_CORE_SCOPE_EXTENSION_AUTHORITY_MISSING", ",".join(higher))
    if not higher and scope["program_context"] == "GRADE_LEVEL" and scope["extension_authority_ref"].strip():
        fail("CHEM_CORE_SCOPE_EXTENSION_UNNEEDED")

    expected_units = {(row["scope_unit_kind"], row["scope_unit_id"]) for row in authority["scope_units"]}
    assignments = scope["scope_unit_assignments"]
    assignment_keys = [(row["scope_unit_kind"], row["scope_unit_id"]) for row in assignments]
    if len(assignment_keys) != len(set(assignment_keys)):
        fail("CHEM_CORE_SCOPE_ASSIGNMENT_DUPLICATE")
    if set(assignment_keys) != expected_units:
        fail("CHEM_CORE_SCOPE_ASSIGNMENT_INCOMPLETE")
    illegal = {
        f"{row['scope_unit_kind']}:{row['scope_unit_id']}": row["scope_tier"]
        for row in assignments
        if row["scope_tier"] not in authorized
    }
    if illegal:
        fail("CHEM_CORE_SCOPE_UNAUTHORIZED_TIER", json.dumps(illegal, sort_keys=True))

    held_transforms = {
        row["asset_ref"]
        for row in audit["asset_bindings"]
        if row["asset_kind"] == "TRANSFORMATION" and row["scope_tier_id"] in held
    }
    guards = scope["held_transformation_guards"]
    guard_refs = {row["fingerprint"] for row in guards}
    if guard_refs != held_transforms:
        fail("CHEM_CORE_SCOPE_HELD_GUARD_INCOMPLETE", f"guards={sorted(guard_refs)} held={sorted(held_transforms)}")

    surface = "\n".join(authority["learner_surface_strings"]).lower()
    for guard in guards:
        for token in guard["detection_tokens"]:
            if token.lower() in surface:
                fail("CHEM_CORE_SCOPE_HELD_CONTENT_LEAK", f"{guard['fingerprint']}:{token}")
    for label in audit["learner_surface_policy"]["forbidden_surface_labels"]:
        if label.lower() in surface:
            fail("CHEM_CORE_SCOPE_LEARNER_JARGON_LEAK", label)

    return {
        "status": "PASS",
        "scope_contract_id": scope["scope_contract_id"],
        "product_mode": scope["product_mode"],
        "gate_id": scope["gate_id"],
        "authorized_scope_tiers": sorted(authorized),
        "held_scope_tiers": sorted(held),
        "scope_unit_count": len(expected_units),
        "held_guard_count": len(guards),
        "source_audit_role": audit_result["audit_role"],
    }
