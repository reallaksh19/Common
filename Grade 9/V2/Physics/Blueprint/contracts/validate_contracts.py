#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> None:
    schema_dir = ROOT / "contracts"
    schema_names = [
        "architecture-blueprint.schema.json",
        "packet-envelope.schema.json",
        "evidence-state.schema.json",
        "routing-decision.schema.json",
        "independent-validation-session.schema.json",
    ]
    schemas = {name: load(schema_dir / name) for name in schema_names}
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    Draft202012Validator(schemas["architecture-blueprint.schema.json"]).validate(
        load(ROOT / "policy" / "architecture.v1.json")
    )

    evidence_validator = Draft202012Validator(schemas["evidence-state.schema.json"])
    for fixture in sorted((ROOT / "fixtures" / "golden").glob("*.json")):
        evidence_validator.validate(load(fixture)["evidence"])

    architecture = load(ROOT / "policy" / "architecture.v1.json")
    if architecture["role_lifecycle"]["CORE2A"] != "ACTIVE":
        raise AssertionError("CORE2A_MUST_BE_ACTIVE_AFTER_SEMANTIC_CONTRACT")
    if not architecture["invariants"]["core2a_requires_taught_state_receipts"]:
        raise AssertionError("CORE2A_TAUGHT_STATE_GATE_DISABLED")
    if not architecture["invariants"]["core2a_may_not_infer_learner_mastery"]:
        raise AssertionError("CORE2A_MASTERY_INFERENCE_GUARD_DISABLED")
    if architecture["invariants"]["max_subtopics_per_handoff"] != 3:
        raise AssertionError("HANDOFF_BOUND_DRIFT")
    if not architecture["invariants"]["learning_atoms_unbounded"]:
        raise AssertionError("TRANSPORT_BOUND_LEAKED_INTO_PEDAGOGY")

    independent = load(ROOT / "policy" / "independent-validation.v1.json")
    if not independent["self_validation_forbidden"]:
        raise AssertionError("SELF_VALIDATION_POLICY_DISABLED")
    if not independent["fresh_validator_instance_required"]:
        raise AssertionError("FRESH_VALIDATOR_POLICY_DISABLED")
    first = independent["passes"][0]
    if first["mode"] != "GROUND_TRUTH_ONLY" or "UPSTREAM_CLAIMS" not in first["must_not_see"]:
        raise AssertionError("GROUND_TRUTH_BLIND_PASS_POLICY_DRIFT")

    print("Blueprint contracts: PASS")


if __name__ == "__main__":
    validate()
