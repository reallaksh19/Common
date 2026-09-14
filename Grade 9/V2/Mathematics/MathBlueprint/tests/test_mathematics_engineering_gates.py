#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_mathematics_engineering_gates import (  # noqa: E402
    load_json,
    validate,
    run_falsification_battery,
    validate_gate_schema,
    validate_subtopic_invariants,
    MathematicsEngineeringGateValidationError,
)

REGISTRY_PATH = ROOT / "policies" / "mathematics-technical-engineering-gates.v1.json"


class MathematicsEngineeringGateTests(unittest.TestCase):
    def test_math_registry_schema_and_subtopic_invariants(self):
        reg = load_json(REGISTRY_PATH)
        subtopics = validate(reg)
        self.assertEqual(len(subtopics), 10)
        expected_subtopics = [
            "MATH-NUM-RADICALS",
            "MATH-ALG-POLYNOMIALS",
            "MATH-LIN-EQUATIONS",
            "MATH-QUAD-EQUATIONS",
            "MATH-GEO-COORDINATES",
            "MATH-GEO-TRIANGLES",
            "MATH-TRIG-RATIOS",
            "MATH-GEO-CIRCLES",
            "MATH-MENS-SURFACES",
            "MATH-STAT-PROBABILITY"
        ]
        for expected in expected_subtopics:
            self.assertIn(expected, subtopics, f"Missing expected subtopic {expected}")

    def test_math_maturity_is_strictly_engineering(self):
        reg = load_json(REGISTRY_PATH)
        for gate in reg["subtopic_gates"]:
            self.assertEqual(gate["maturity"], "ENGINEERING")
            self.assertEqual(gate["difficulty_profile"]["maturity"], "ENGINEERING")
            self.assertNotIn("psychometric", gate["difficulty_profile"])

    def test_math_16_point_technical_structure_present(self):
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
                self.assertIn(k, gate, f"Missing key {k} in subtopic {gate['subtopic_id']}")

    def test_math_cross_reference_prerequisite_closure(self):
        reg = load_json(REGISTRY_PATH)
        subtopic_ids = {g["subtopic_id"] for g in reg["subtopic_gates"]}
        for gate in reg["subtopic_gates"]:
            for prereq in gate.get("prerequisite_ids", []):
                if prereq.startswith("MATH-"):
                    self.assertIn(prereq, subtopic_ids, f"Unresolved prerequisite {prereq} in {gate['subtopic_id']}")
                    self.assertNotEqual(prereq, gate["subtopic_id"], f"Self dependency in {gate['subtopic_id']}")

    def test_math_mutation_falsification_battery(self):
        run_falsification_battery()


if __name__ == "__main__":
    unittest.main()
