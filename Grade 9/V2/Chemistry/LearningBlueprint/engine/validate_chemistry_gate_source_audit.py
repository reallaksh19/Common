#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parents[1]


class ChemistrySourceAuditError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def fail(code: str, message: str):
    raise ChemistrySourceAuditError(code, message)


def transformation_ref(record: dict) -> str:
    return (
        f"{record['from_mode']}->{record['to_mode']}|"
        f"{record['target_core_role']}"
    )


def expected_assets(gate: dict) -> dict[str, set[str]]:
    return {
        "CONCEPT": set(gate["canonical_concept_ids"]),
        "EQUATION": {row["equation_id"] for row in gate["mandatory_equations"]},
        "TRANSFORMATION": {
            transformation_ref(row) for row in gate["required_transformations"]
        },
    }


def validate(audit: dict, registry: dict | None = None) -> dict:
    registry = registry or load(audit["base_registry_ref"])
    schema = load("contracts/chemistry-gate-source-audit.schema.json")
    Draft202012Validator.check_schema(schema)
    try:
        Draft202012Validator(schema).validate(audit)
    except ValidationError as exc:
        fail("CHEM_SOURCE_AUDIT_SCHEMA", f"{exc.message} at {list(exc.path)}")

    gate = next(
        (
            row
            for row in registry["subtopic_gates"]
            if row["subtopic_id"] == audit["gate_id"]
        ),
        None,
    )
    if gate is None:
        fail("CHEM_SOURCE_AUDIT_GATE_MISSING", audit["gate_id"])

    layers = {row["layer_id"]: row for row in audit["source_layers"]}
    if len(layers) != len(audit["source_layers"]):
        fail("CHEM_SOURCE_AUDIT_DUPLICATE_SOURCE_LAYER", "source layer ids must be unique")

    tiers = {row["tier_id"]: row for row in audit["scope_tiers"]}
    if len(tiers) != len(audit["scope_tiers"]):
        fail("CHEM_SOURCE_AUDIT_DUPLICATE_SCOPE_TIER", "scope tier ids must be unique")

    bindings: dict[tuple[str, str], dict] = {}
    for row in audit["asset_bindings"]:
        key = (row["asset_kind"], row["asset_ref"])
        if key in bindings:
            fail("CHEM_SOURCE_AUDIT_DUPLICATE_ASSET_BINDING", f"duplicate={key}")
        bindings[key] = row

        missing_layers = sorted(set(row["authority_layer_ids"]) - set(layers))
        if missing_layers:
            fail(
                "CHEM_SOURCE_AUDIT_UNRESOLVED_SOURCE_REF",
                f"asset={key} missing={missing_layers}",
            )
        if row["scope_tier_id"] not in tiers:
            fail(
                "CHEM_SOURCE_AUDIT_UNRESOLVED_SCOPE_TIER",
                f"asset={key} tier={row['scope_tier_id']}",
            )

    expected = expected_assets(gate)
    for kind in audit["coverage_requirements"]:
        expected_refs = expected[kind]
        bound_refs = {
            asset_ref
            for (asset_kind, asset_ref), _row in bindings.items()
            if asset_kind == kind
        }
        if expected_refs != bound_refs:
            fail(
                "CHEM_SOURCE_AUDIT_ASSET_COVERAGE",
                (
                    f"kind={kind} "
                    f"missing={sorted(expected_refs - bound_refs)} "
                    f"extra={sorted(bound_refs - expected_refs)}"
                ),
            )

    surface = audit["learner_surface_policy"]
    if surface["legacy_internal_ids"] and not surface["internal_concept_ids_hidden"]:
        fail(
            "CHEM_SOURCE_AUDIT_LEARNER_SURFACE",
            "legacy internal ids require internal_concept_ids_hidden=true",
        )

    if audit["audit_status"] == "SOURCE_HARDENED":
        open_repairs = [
            row["defect_id"]
            for row in audit["repair_records"]
            if row["status"] == "OPEN"
        ]
        if open_repairs:
            fail(
                "CHEM_SOURCE_AUDIT_OPEN_REPAIR",
                f"source-hardened audit has open repairs={open_repairs}",
            )

    authority_effect = (
        "NONE_STRESS_TEST_ONLY"
        if audit["audit_role"] == "STRESS_TEST_SOURCE_AUDIT"
        else "SOURCE_SCOPE_EVIDENCE_ONLY"
    )

    return {
        "status": "PASS",
        "audit_status": audit["audit_status"],
        "audit_role": audit["audit_role"],
        "authority_effect": authority_effect,
        "gate_id": audit["gate_id"],
        "source_layer_count": len(layers),
        "scope_tier_count": len(tiers),
        "asset_binding_count": len(bindings),
        "coverage_requirements": list(audit["coverage_requirements"]),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: validate_chemistry_gate_source_audit.py <audit-json-relative-to-LearningBlueprint>"
        )
    audit = load(sys.argv[1])
    print(json.dumps(validate(audit), indent=2))


if __name__ == "__main__":
    main()
