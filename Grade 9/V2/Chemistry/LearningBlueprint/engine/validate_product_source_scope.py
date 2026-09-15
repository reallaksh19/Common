#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load


class ChemistryProductSourceScopeError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryProductSourceScopeError(code, message)


def validate_schema(obj: dict, rel: str, code: str):
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def _surface_text(authority: dict) -> str:
    payloads = [obj.get("learner_payload") for obj in authority.get("content_objects", [])]
    return json.dumps(payloads, ensure_ascii=False, sort_keys=True).lower()


def validate_product_source_scope(scope: dict, audit: dict, authority: dict) -> dict:
    validate_schema(scope, "contracts/chemistry-product-source-scope-v1.schema.json", "CHEM_PRODUCT_SCOPE_SCHEMA")
    validate_schema(audit, "contracts/chemistry-gate-source-audit.schema.json", "CHEM_PRODUCT_SCOPE_AUDIT_SCHEMA")

    if audit.get("audit_status") != "SOURCE_HARDENED":
        fail("CHEM_PRODUCT_SCOPE_AUDIT_NOT_HARDENED", "source audit is not SOURCE_HARDENED")
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

    higher = [t for t in authorized if int(tier_map[t]["grade_band"]) > int(scope["learner_grade"])]
    if higher:
        if not scope.get("extension_authority_ref", "").strip() or not scope.get("extension_reason", "").strip():
            fail("CHEM_PRODUCT_SCOPE_EXTENSION_AUTHORITY_MISSING", f"higher-grade tiers require explicit extension authority: {sorted(higher)}")
    elif scope.get("program_context") == "GRADE_LEVEL" and scope.get("extension_authority_ref"):
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

    held_fingerprints = {
        t["fingerprint"]
        for t in audit["transformation_bindings"]
        if t["scope_tier"] in held
    }
    guards = scope["held_transformation_guards"]
    guard_fingerprints = {g["fingerprint"] for g in guards}
    if guard_fingerprints != held_fingerprints:
        fail(
            "CHEM_PRODUCT_SCOPE_HELD_GUARD_INCOMPLETE",
            f"held transformation guards {sorted(guard_fingerprints)} != audited held transformations {sorted(held_fingerprints)}",
        )

    surface = _surface_text(authority)
    for guard in guards:
        for token in guard["detection_tokens"]:
            if token.lower() in surface:
                fail(
                    "CHEM_PRODUCT_SCOPE_HELD_CONTENT_LEAK",
                    f"held transformation {guard['fingerprint']} detected via token {token}",
                )

    for label in audit["learner_surface_policy"]["forbidden_surface_labels"]:
        if label.lower() in surface:
            fail("CHEM_PRODUCT_SCOPE_LEARNER_JARGON_LEAK", f"forbidden learner-surface label: {label}")

    counts = {tier: list(assignment_map.values()).count(tier) for tier in sorted(authorized)}
    return {
        "status": "PASS",
        "scope_contract_id": scope["scope_contract_id"],
        "subtopic_id": scope["subtopic_id"],
        "learner_grade": scope["learner_grade"],
        "authorized_scope_tiers": sorted(authorized),
        "held_scope_tiers": sorted(held),
        "learning_atom_count": len(atoms),
        "learning_atom_tier_counts": counts,
        "held_guard_count": len(guards),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("scope_contract")
    p.add_argument("source_audit")
    p.add_argument("product_authority")
    a = p.parse_args()
    try:
        result = validate_product_source_scope(load(a.scope_contract), load(a.source_audit), load(a.product_authority))
    except ChemistryProductSourceScopeError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
