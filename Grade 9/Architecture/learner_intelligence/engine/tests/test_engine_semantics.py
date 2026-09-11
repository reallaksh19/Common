#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
LI_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ENGINE))

from derive_state import canonical_bytes, derive  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class LearnerIntelligenceEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load(ENGINE / "fixtures" / "capability_registry.v1.json")
        cls.policy = load(ENGINE / "fixtures" / "state_reduction_policy.v1.json")
        cls.answer_sheet = load(LI_ROOT / "fixtures" / "cross_subject_answer_sheet_acceptance.json")
        cls.recurrence = load(ENGINE / "fixtures" / "cross_subject_recurrence_fixture.json")

    def state(self, result, capability_ref):
        return next(row for row in result["capability_states"] if row["capability_ref"] == capability_ref)

    def case(self, result, case_id):
        return next(row for row in result["case_results"] if row["case_id"] == case_id)

    def test_same_inputs_are_deterministic(self):
        a = derive(self.answer_sheet, self.registry, self.policy)
        b = derive(self.answer_sheet, self.registry, self.policy)
        self.assertEqual(canonical_bytes(a), canonical_bytes(b))
        self.assertEqual(a["output_digest"], b["output_digest"])

    def test_math_success_survives_later_algebra_failure(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        row = self.case(result, "MATH-COORD-ALG-01")
        self.assertIn("MATH-COORD-GEOMETRIC-MODELLING", row["preserved_capabilities"])
        self.assertIn("MATH-ALG-EXPAND-BINOMIAL-SQUARE", row["candidate_failure_capabilities"])
        self.assertIn("MATHEMATICS_COORDINATE_GEOMETRY_GLOBALLY_WEAK", row["forbidden_conclusions"])
        self.assertEqual(self.state(result, "MATH-COORD-GEOMETRIC-MODELLING")["state"], "DEVELOPING")
        self.assertEqual(self.state(result, "MATH-ALG-EXPAND-BINOMIAL-SQUARE")["state"], "UNKNOWN")

    def test_word_modelling_is_not_erased_by_expression_error(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        row = self.case(result, "MATH-WORD-EQUATION-01")
        self.assertIn("MATH-WORD-MODELLING", row["preserved_capabilities"])
        self.assertIn("SHARED-SYMBOLIC-PRESERVE-MEANING", row["candidate_failure_capabilities"])
        self.assertIn("MATHEMATICS_WORD_PROBLEM_MODELLING_WEAK", row["forbidden_conclusions"])

    def test_physics_state_transition_failure_does_not_erase_model_selection(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        row = self.case(result, "PHYSICS-MULTIPHASE-01")
        self.assertIn("PHY-KIN-SELECT-EQUATION", row["preserved_capabilities"])
        self.assertIn("PHY-KIN-PROPAGATE-STATE", row["candidate_failure_capabilities"])
        self.assertEqual(self.state(result, "PHY-KIN-PROPAGATE-STATE")["state"], "UNKNOWN")
        self.assertIn("PHYSICS_KINEMATIC_FORMULA_KNOWLEDGE_ABSENT", row["forbidden_conclusions"])

    def test_ambiguous_projectile_interpretation_requires_probe(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        row = self.case(result, "PHYSICS-PROJECTILE-01")
        self.assertEqual(row["action"], "DIAGNOSTIC_PROBE_REQUIRED")
        state = self.state(result, "PHY-PROJ-DIAGRAM-STATE-TRANSLATION")
        self.assertEqual(state["evidence_summary"]["ambiguous_evidence"], 1)
        self.assertEqual(state["state"], "UNKNOWN")

    def test_chemistry_concept_is_preserved_when_shared_proportional_reasoning_fails(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        row = self.case(result, "CHEM-GAS-PROP-01")
        self.assertIn("CHEM-GAS-RELATIONSHIP", row["preserved_capabilities"])
        self.assertIn("CHEM-GAS-CONDITIONS", row["preserved_capabilities"])
        self.assertIn("SHARED-PROPORTIONAL-REASONING", row["candidate_failure_capabilities"])
        self.assertIn("CHEMISTRY_GAS_LAW_CONCEPT_ABSENT", row["forbidden_conclusions"])

    def test_single_failure_does_not_become_repair_required(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        single_failure_caps = [
            "MATH-ALG-EXPAND-BINOMIAL-SQUARE",
            "SHARED-SYMBOLIC-PRESERVE-MEANING",
            "PHY-KIN-PROPAGATE-STATE",
            "SHARED-PROPORTIONAL-REASONING",
        ]
        for capability_ref in single_failure_caps:
            self.assertNotEqual(self.state(result, capability_ref)["state"], "REPAIR_REQUIRED")

    def test_answer_sheet_does_not_infer_psychological_cause(self):
        result = derive(self.answer_sheet, self.registry, self.policy)
        self.assertEqual(result["psychological_cause_inference"], "PROHIBITED")
        self.assertEqual(result["cross_subject_candidates"], [])

    def test_cross_subject_recurrence_is_candidate_not_cause(self):
        result = derive(self.recurrence, self.registry, self.policy)
        self.assertEqual(len(result["cross_subject_candidates"]), 1)
        row = result["cross_subject_candidates"][0]
        self.assertEqual(row["capability_ref"], "SHARED-SIGNED-EXECUTION")
        self.assertEqual(row["classification"], "CROSS_SUBJECT_RECURRING_FAILURE_CANDIDATE")
        self.assertEqual(row["causal_status"], "CANDIDATE_NOT_CAUSE")
        self.assertEqual(row["subjects_seen"], ["CHEMISTRY", "MATHEMATICS", "PHYSICS"])
        self.assertEqual(self.state(result, "SHARED-SIGNED-EXECUTION")["state"], "REPAIR_REQUIRED")


if __name__ == "__main__":
    unittest.main()
