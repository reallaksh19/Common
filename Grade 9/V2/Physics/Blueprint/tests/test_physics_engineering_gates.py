#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_engineering_gates import (  # noqa: E402
    load_json,
    validate,
    run_falsification_battery,
    validate_gate_schema,
    validate_subtopic_invariants,
    EngineeringGateValidationError,
)

REGISTRY_PATH = ROOT / "policy" / "physics-technical-engineering-gates.v1.json"


def test_registry_schema_and_subtopic_invariants():
    reg = load_json(REGISTRY_PATH)
    subtopics = validate(reg)
    assert len(subtopics) == 12
    assert "PHY-VEC-BASICS" in subtopics
    assert "PHY-NLM-CONNECTED" in subtopics


def test_maturity_is_strictly_engineering():
    reg = load_json(REGISTRY_PATH)
    for gate in reg["subtopic_gates"]:
        assert gate["maturity"] == "ENGINEERING"
        assert gate["difficulty_profile"]["maturity"] == "ENGINEERING"
        assert "psychometric" not in gate["difficulty_profile"]


def test_16_point_technical_structure_present():
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


def test_vector_and_nlm_falsification_battery():
    run_falsification_battery()


def main():
    ts = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for t in ts:
        t()
    print(f"Physics Technical Engineering Gate tests: PASS ({len(ts)} test suites)")


if __name__ == "__main__":
    main()
