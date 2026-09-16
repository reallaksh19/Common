import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from project_chemistry_problem_family import (  # noqa: E402
    ChemistrySemanticProjectionError,
    project_problem_family,
    validate_problem_family_projection,
)


class ChemistrySemanticProjectionTests(unittest.TestCase):
    def setUp(self):
        self.problem_family = {
            "family_id": "PF-CHEM-TEST",
            "name": "Synthetic Chemistry reasoning family",
            "recognition_cues": "A governed chemical relationship must be identified before solving.",
            "first_technical_move": "Write the governing chemical relationship explicitly.",
            "common_fatal_error": "Reverse the governing relationship before checking the evidence.",
            "typical_unknown": "The chemically consistent conclusion.",
        }

    def test_positive_and_negative_semantics_are_projected_to_distinct_roles(self):
        projected = project_problem_family(self.problem_family)
        self.assertEqual(projected["method_steps"], [self.problem_family["first_technical_move"]])
        self.assertEqual(projected["common_fatal_errors"], [self.problem_family["common_fatal_error"]])
        self.assertNotIn(self.problem_family["common_fatal_error"], projected["method_steps"])
        self.assertEqual(projected["semantic_role_trace"]["common_fatal_error"], "ERROR_TO_AVOID")

    def test_fatal_error_cannot_be_reclassified_as_method_step(self):
        projected = project_problem_family(self.problem_family)
        bad = copy.deepcopy(projected)
        bad["method_steps"].append(self.problem_family["common_fatal_error"])
        with self.assertRaises(ChemistrySemanticProjectionError) as ctx:
            validate_problem_family_projection(self.problem_family, bad)
        self.assertEqual(ctx.exception.code, "CHEM_SEMANTIC_PROJECTION_FATAL_ERROR_AS_METHOD_STEP")

    def test_missing_semantic_field_fails_closed(self):
        bad = copy.deepcopy(self.problem_family)
        bad.pop("common_fatal_error")
        with self.assertRaises(ChemistrySemanticProjectionError) as ctx:
            project_problem_family(bad)
        self.assertEqual(ctx.exception.code, "CHEM_SEMANTIC_PROJECTION_SOURCE_FIELD_MISSING")

    def test_generic_projection_contains_no_topic_branch(self):
        text = (ENGINE / "project_chemistry_problem_family.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
