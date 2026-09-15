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
    assert len(subtopics) == 43
    assert "PHY-VEC-BASICS" in subtopics
    assert "PHY-NLM-CONNECTED" in subtopics
    assert "PHY-KIN-1D-MOTION" in subtopics
    assert "PHY-OPTICS-REFLECTION-MIRRORS" in subtopics
    assert "PHY-THERMO-FIRST-SECOND-LAW" in subtopics
    assert "PHY-OSC-SHM-WAVES" in subtopics


def test_cbse_and_jee_tier_coverage():
    reg = load_json(REGISTRY_PATH)
    gates = reg["subtopic_gates"]
    assert len(gates) == 43

    valid_tiers = {"NOT_IN_JEE", "JEE_MAINS", "JEE_ADVANCED", "BOTH"}
    grades_present = set()
    tier_counts = {t: 0 for t in valid_tiers}

    for g in gates:
        sid = g["subtopic_id"]
        assert "jee_tier" in g, f"Gate {sid} missing jee_tier"
        assert g["jee_tier"] in valid_tiers, f"Gate {sid} invalid jee_tier: {g['jee_tier']}"
        tier_counts[g["jee_tier"]] += 1

        assert "cbse_ref" in g, f"Gate {sid} missing cbse_ref"
        cbse = g["cbse_ref"]
        assert cbse["grade"] in {9, 10, 11}, f"Gate {sid} invalid grade: {cbse['grade']}"
        assert isinstance(cbse["chapter"], str) and len(cbse["chapter"]) > 0
        grades_present.add(cbse["grade"])

    assert grades_present == {9, 10, 11}, f"Expected grades 9, 10, 11 to all be present, got: {grades_present}"
    assert tier_counts["BOTH"] > 0
    assert tier_counts["JEE_MAINS"] > 0
    assert tier_counts["NOT_IN_JEE"] > 0


def test_mutation_falsification_jee_tier():
    reg = load_json(REGISTRY_PATH)
    bad = copy.deepcopy(reg)
    bad["subtopic_gates"][0]["jee_tier"] = "INVALID_TIER"
    try:
        validate_gate_schema(bad)
        raise AssertionError("Expected failure for invalid jee_tier")
    except EngineeringGateValidationError as err:
        assert err.code == "ENG_GATE_SCHEMA_VIOLATION"


def test_mutation_falsification_cbse_ref():
    reg = load_json(REGISTRY_PATH)
    bad = copy.deepcopy(reg)
    del bad["subtopic_gates"][0]["cbse_ref"]
    try:
        validate_gate_schema(bad)
        raise AssertionError("Expected failure for missing cbse_ref")
    except EngineeringGateValidationError as err:
        assert err.code == "ENG_GATE_SCHEMA_VIOLATION"


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
