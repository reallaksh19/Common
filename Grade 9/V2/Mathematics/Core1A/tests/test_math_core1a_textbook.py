#!/usr/bin/env python3
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
C1A = HERE.parents[1]
ENGINE_PATH = C1A / "engine" / "build_math_core1a_textbook.py"

spec = importlib.util.spec_from_file_location("build_math_core1a_textbook", ENGINE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class Core1ALearnerInstanceTests(unittest.TestCase):
    """Tests for the capability/family instance materializer used by bucket realization."""

    def sample_asset(self, bridge=None):
        return {
            "asset_id": "MATH-PCK-DISTANCE-DEMO-v1",
            "capability_refs": ["MATH-COORDINATE-DISTANCE"],
            "anchor": "Distance combines horizontal and vertical change through a right-triangle relationship.",
            "ordinary_language_bridge": bridge or "Imagine walking across and then up: the direct path is the hypotenuse.",
            "reconstruction_route": [
                "match x-coordinates with x-coordinates and y-coordinates with y-coordinates",
                "find the horizontal and vertical changes",
                "combine them with the Pythagorean relationship",
                "take the non-negative square root because distance cannot be negative",
            ],
            "misconception_discriminator": {
                "candidate_wrong_model": "subtract an x-coordinate from a y-coordinate",
                "probe": "ask which axis each difference belongs to before calculating",
            },
            "repair_route": ["align x/y roles", "form one x-difference and one y-difference"],
            "verification_method": ["reverse the point order and confirm the same distance"],
        }

    def sample_family(self):
        return {
            "family_id": "MATH-PF-DISTANCE-FORMULA",
            "problem_signature": {
                "recognition_cues": ["two ordered pairs", "a distance relationship"],
                "target_job": "construct or use the distance relationship while keeping coordinate roles matched",
            },
            "reasoning_route_template": [
                {"semantic_job": "read the coordinate roles"},
                {"semantic_job": "form horizontal and vertical differences"},
                {"semantic_job": "combine them with the Pythagorean relationship"},
            ],
            "common_invalid_mechanisms": [],
        }

    def sample_lesson(self, family_ref="MATH-PF-DISTANCE-FORMULA"):
        asset = self.sample_asset()
        return {
            "lesson_id": "MATH-C1L-0123456789abcdef",
            "learner_title": "Coordinate Distance",
            "capability_ref": "MATH-COORDINATE-DISTANCE",
            "treatment": "ACTIVE_STUDY",
            "scope_role": "DIRECT_ASSESSED",
            "assessment_question_refs": ["Q1"],
            "pck_asset_refs": [asset["asset_id"]],
            "required_pck_jobs": ["EXPLAIN"],
            "instructional_sequence": ["ANCHOR","REPRESENT","EXPLAIN","RECONSTRUCT","CONTRAST","WORKED","GUIDED","FADED","INDEPENDENT","VERIFY","TRANSFER"],
            "representation_requirements": ["ORDERED_PAIR"],
            "problem_authoring_plans": [
                {
                    "plan_id": "MATH-PAP-0000000000000001",
                    "capability_ref": "MATH-COORDINATE-DISTANCE",
                    "problem_family_ref": family_ref,
                    "instance_role": role,
                    "must_be_new_instance": True,
                    "source_question_reuse": False,
                    "source_question_refs": [],
                    "variation_requirements": ["new instance"],
                    "verification_obligations": ["VERIFY_DISTANCE_RELATION"],
                }
                for role in mod.REQUIRED_ROLES
            ],
            "verification_requirements": ["VERIFY_DISTANCE_RELATION"],
            "future_evidence_obligations": [{} for _ in range(8)],
            "scope_trace": {"study_scope_ref": "SCOPE", "study_model_capability_ref": "MATH-COORDINATE-DISTANCE"},
        }

    def test_family_bank_complete(self):
        expected = {
            "MATH-PF-EUCLID-CLASSIFICATION", "MATH-PF-DISTANCE-FORMULA",
            "MATH-PF-QUADRANT-SIGN-TRANSFORM", "MATH-PF-LINE-INTERCEPT",
            "MATH-PF-LINE-SLOPE-POINT", "MATH-PF-PAIR-COUNT",
            "MATH-PF-COLLINEARITY-SLOPE", "MATH-PF-EUCLID-PARALLEL-EXPLANATION",
            "MATH-PF-LINEAR-PARAMETER-SUFFICIENCY", "MATH-PF-INTERSECTION-THEN-LINE",
            "MATH-PF-EQUIDISTANT-AXIS-POINT", "MATH-PF-EQUILATERAL-COORDINATE",
            "MATH-PF-LINEAR-TREND-EXTRAPOLATION", "MATH-PF-RIVER-CURRENT-SYSTEM",
        }
        self.assertEqual(set(mod.FAMILY_BANKS), expected)
        for family in expected:
            self.assertGreaterEqual(len(mod.family_bank(family)), 6, family)

    def test_authored_unit_materializes_required_roles(self):
        lesson = self.sample_lesson()
        asset = self.sample_asset()
        unit = mod.authored_lesson(lesson, {asset["asset_id"]: asset}, {"MATH-PF-DISTANCE-FORMULA": self.sample_family()})
        self.assertEqual(len(unit["worked_examples"]), 2)
        self.assertTrue(set(mod.REQUIRED_ROLES).issubset(set(unit["practice"])))
        self.assertNotIn("author a new instance", str(unit).lower())

    def test_unsupported_family_fails_closed(self):
        lesson = self.sample_lesson("MATH-PF-UNSEEN-FAMILY")
        asset = self.sample_asset()
        with self.assertRaisesRegex(ValueError, "CORE1A_FAMILY_GENERATOR_MISSING"):
            mod.authored_lesson(lesson, {asset["asset_id"]: asset}, {"MATH-PF-DISTANCE-FORMULA": self.sample_family()})


if __name__ == "__main__":
    unittest.main(verbosity=2)
