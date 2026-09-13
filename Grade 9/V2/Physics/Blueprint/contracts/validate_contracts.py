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
    ]
    schemas = {name: load(schema_dir / name) for name in schema_names}
    for name, schema in schemas.items():
        Draft202012Validator.check_schema(schema)

    Draft202012Validator(schemas["architecture-blueprint.schema.json"]).validate(
        load(ROOT / "policy" / "architecture.v1.json")
    )

    evidence_validator = Draft202012Validator(schemas["evidence-state.schema.json"])
    for fixture in sorted((ROOT / "fixtures" / "golden").glob("*.json")):
        evidence_validator.validate(load(fixture)["evidence"])

    architecture = load(ROOT / "policy" / "architecture.v1.json")
    if architecture["role_lifecycle"]["CORE2A"] != "PLACEHOLDER":
        raise AssertionError("CORE2A_MUST_REMAIN_PLACEHOLDER_IN_BLUEPRINT_V1")
    if architecture["invariants"]["max_subtopics_per_handoff"] != 3:
        raise AssertionError("HANDOFF_BOUND_DRIFT")
    if not architecture["invariants"]["learning_atoms_unbounded"]:
        raise AssertionError("TRANSPORT_BOUND_LEAKED_INTO_PEDAGOGY")

    print("Blueprint contracts: PASS")


if __name__ == "__main__":
    validate()
