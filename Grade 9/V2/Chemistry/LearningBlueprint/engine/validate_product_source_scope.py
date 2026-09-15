#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from validate_chemistry_gate_source_audit import validate as validate_source_audit  # noqa: E402


class ChemistryProductSourceScopeError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryProductSourceScopeError(code, message)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def digest(obj: dict) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_schema(obj: dict, rel: str, code: str):
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def _surface_text(authority: dict) -> str:
    payloads = [obj.get("learner_payload") for obj in authority.get("content_objects", [])]
    return json.dumps(payloads, ensure_ascii=False, sort_keys=True).lower()


def validate_product_source_scope(scope: dict, audit: dict, authority: dict, registry: dict) -> dict:
    validate_schema(scope, "contracts/chemistry-product-source-scope-v1.schema.json", "CHEM_PRODUCT_SCOPE_SCHEMA")
    audit_result = validate_source_audit(audit, registry)

    if audit_result["audit_role"] != "PRODUCTION_SOURCE_AUDIT":
        fail("CHEM_PRODUCT_SCOPE_STRESS_AUDIT_NOT_AUTHORITY", "stress-test source audit cannot authorize a learner product")
    if audit_result["audit_status"] != "SOURCE_HARDENED":
        fail("CHEM_PRODUCT_SCOPE_AUDIT_NOT_HARDENED", "production source audit is not SOURCE_HARDENED")
    if scope["source_audit_digest"] != digest(audit):
        fail("CHEM_PRODUCT_SCOPE_AUDIT_DIGEST_MISMATCH", "scope contract does not bind exact source audit bytes")
    if scope["gate_id"] != audit["gate_id"]:
        fail("CHEM_PRODUCT_SCOPE_GATE_MISMATCH", "scope contract and source audit gate_id differ")
    if scope["subtopic_id"] != authority.get("subtopic_id"):
        fail("CHEM_PRODUCT_SCOPE_SUBTOPIC_MISMATCH", "scope contract and product authority subtopic differ")

    tier_map = {item["tier_id"]: item for item in audit["scope_tiers"]}
    audit_tiers = set(tier_map)
    authorized = set(scope["authorized_scope_tiers"])
    held = set(scope["held_scope_tiers"])
    if authorized & held:
        fail("CHEM_PRODUCT_SCOPE_TIER_DUAL_STATE", "a source tier cannot be both authorized and held")
    if authorized | held != audit_tiers:
        fail("CHEM_PRODUCT_SCOPE_TIER_PARTITION_INCOMPLETE", "every audited source tier must be explicitly authorized or held")

    higher = sorted(t for t in authorized if tier_map[t]["minimum_learner_grade"] > scope["learner_grade"])
    if higher:
        if not scope["extension_authority_ref"].strip() or not scope["extension_reason"].strip():
            fail("CHEM_PRODUCT_SCOPE_EXTENSION_AUTHORITY_MISSING", f"higher-grade tiers require explicit extension authority: {higher}")
    elif scope["program_context"] == "GRADE_LEVEL" and scope["extension_authority_ref"].strip():
        fail("CHEM_PRODUCT_SCOPE_EXTENSION_UNNEEDED", "grade-level product should not declare unused extension authority")

    atoms = [a["atom_id"] for a in authority.get("learning_atoms", [])]
    if not atoms or len(atoms) != len(set(atoms)):
        fail("CHEM_PRODUCT_SCOPE_AUTHORITY_ATOMS_INVALID", "product authority learning atoms are missing or duplicated")
    assignments = scope["learning_atom_scope_assignments"]
    assignment_ids = [a["learning_atom_id"] for a in assignments]
    if len(assignment_ids) != len(set(assignment_ids)):
        fail("CHEM_PRODUCT_SCOPE_ASSIGNMENT_DUPLICATE", "learning atom scope assignment duplicated")
    if set(assignment_ids) != set(atoms):
        fail("CHEM_PRODUCT_SCOPE_ASSIGNMENT_INCOMPLETE", "every product learning atom must have exactly one source-scope tier")
    assignment_map = {a["learning_atom_id"]: a["scope_tier"] for a in assignments}
    illegal = {aid: tier for aid, tier in assignment_map.items() if tier not in authorized}
    if illegal:
        fail("CHEM_PRODUCT_SCOPE_UNAUTHORIZED_TIER", f"learning atoms use held/unapproved tiers: {illegal}")

    held_transforms = {
        row["asset_ref"]
        for row in audit["asset_bindings"]
        if row["asset_kind"] == "TRANSFORMATION" and row["scope_tier_id"] in held
    }
    guards = scope["held_transformation_guards"]
    guard_refs = {g["fingerprint"] for g in guards}
    if guard_refs != held_transforms:
        fail("CHEM_PRODUCT_SCOPE_HELD_GUARD_INCOMPLETE", f"guards={sorted(guard_refs)} held={sorted(held_transforms)}")

    surface = _surface_text(authority)
    for guard in guards:
        for token in guard["detection_tokens"]:
            if token.lower() in surface:
                fail("CHEM_PRODUCT_SCOPE_HELD_CONTENT_LEAK", f"held transformation {guard['fingerprint']} detected via token {token}")
    for label in audit["learner_surface_policy"]["forbidden_surface_labels"]:
        if label.lower() in surface:
            fail("CHEM_PRODUCT_SCOPE_LEARNER_JARGON_LEAK", f"forbidden learner-surface label: {label}")

    return {
        "status":"PASS",
        "scope_contract_id":scope["scope_contract_id"],
        "gate_id":scope["gate_id"],
        "authorized_scope_tiers":sorted(authorized),
        "held_scope_tiers":sorted(held),
        "learning_atom_count":len(atoms),
        "held_guard_count":len(guards),
        "source_audit_role":audit_result["audit_role"],
    }
