#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_chemistry_engineering_gates import (  # noqa: E402
    load_json,
    validate,
    run_falsification_battery,
    validate_gate_schema,
    validate_subtopic_invariants,
    ChemistryEngineeringGateValidationError,
)

REGISTRY_PATH = ROOT / "policies" / "chemistry-technical-engineering-gates.v1.json"


def test_chemistry_registry_schema_and_subtopic_invariants():
    reg = load_json(REGISTRY_PATH)
    subtopics = validate(reg)
    assert len(subtopics) == 10
    expected_subtopics = [
        "CHEM-SYM-LITERACY",
        "CHEM-ION-VALENCY",
        "CHEM-FORMULA-CONSTRUCTION",
        "CHEM-EQ-BALANCING",
        "CHEM-STATE-SYMBOLS",
        "CHEM-REACTION-CONDITIONS",
        "CHEM-REP-TRANSLATION",
        "CHEM-CALC-STOICHIOMETRY",
        "CHEM-ACID-BASE-IONS",
        "CHEM-REDOX-OXIDATION"
    ]
    for expected in expected_subtopics:
        assert expected in subtopics, f"Missing expected subtopic {expected}"


def test_chemistry_maturity_is_strictly_engineering():
    reg = load_json(REGISTRY_PATH)
    for gate in reg["subtopic_gates"]:
        assert gate["maturity"] == "ENGINEERING"
        assert gate["difficulty_profile"]["maturity"] == "ENGINEERING"
        assert "psychometric" not in gate["difficulty_profile"]


def test_chemistry_16_point_technical_structure_present():
    reg = load_json(REGISTRY_PATH)
    required_keys = [
        "subtopic_id", "learner_title", "chapter", "authority_tier",
        "maturity", "technical_readiness", "provenance", "canonical_concept_ids",
        "prerequisite_ids", "linked_buckets", "linked_problem_family_ids",
        "technical_core", "mandatory_equations", "representations",
        "model_conditions", "reasoning_sequence", "required_transformations",
        "misconceptions", "mandatory_verifications", "problem_families",
        "difficulty_profile", "release_checklist", "badges", "falsification_cases"
    ]
    for gate in reg["subtopic_gates"]:
        for k in required_keys:
            assert k in gate, f"Missing key {k} in subtopic {gate['subtopic_id']}"


def test_chemistry_cross_reference_prerequisite_closure():
    reg = load_json(REGISTRY_PATH)
    subtopic_ids = {g["subtopic_id"] for g in reg["subtopic_gates"]}
    for gate in reg["subtopic_gates"]:
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("CHEM-"):
                assert prereq in subtopic_ids, f"Unresolved prerequisite {prereq} in {gate['subtopic_id']}"
                assert prereq != gate["subtopic_id"], f"Self dependency in {gate['subtopic_id']}"


def test_chemistry_mutation_falsification_battery():
    run_falsification_battery()


def main():
    ts = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for t in ts:
        t()
    print(f"Chemistry Technical Engineering Gate tests: PASS ({len(ts)} test suites)")


if __name__ == "__main__":
    main()
