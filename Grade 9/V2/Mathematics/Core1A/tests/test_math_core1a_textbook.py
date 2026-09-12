#!/usr/bin/env python3
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
C1A = HERE.parents[1]
ENGINE_PATH = C1A / "engine" / "build_math_core1a_textbook.py"
SCHEMA_PATH = C1A / "contracts" / "math-core1a-textbook-manuscript.schema.json"

spec = importlib.util.spec_from_file_location("build_math_core1a_textbook", ENGINE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class Core1ATextbookTests(unittest.TestCase):
    def sample_asset(self):
        return {
            "asset_id": "MATH-PCK-DISTANCE-DEMO-v1",
            "anchor": "Distance combines horizontal and vertical change through a right-triangle relationship.",
            "ordinary_language_bridge": "Imagine walking across and then up: the direct path is the hypotenuse of that right triangle.",
            "reconstruction_route": [
                "match x-coordinates with x-coordinates and y-coordinates with y-coordinates",
                "find the horizontal and vertical changes",
                "use the Pythagorean relationship to combine those perpendicular changes",
                "take the non-negative square root because distance cannot be negative",
            ],
            "misconception_discriminator": {
                "candidate_wrong_model": "subtract an x-coordinate from a y-coordinate because the numbers are nearby on the page",
                "probe": "ask which axis each difference belongs to before calculating",
            },
            "repair_route": [
                "write the two ordered pairs in aligned x/y columns",
                "form one x-difference and one y-difference",
                "square the two changes before adding them",
            ],
            "verification_method": [
                "reverse the point order and confirm the same distance is obtained",
                "check that the result is non-negative",
            ],
        }

    def sample_family(self):
        return {
            "family_id": "MATH-PF-DISTANCE-FORMULA",
            "problem_signature": {
                "recognition_cues": ["two ordered pairs", "a distance or equal-distance relationship"],
                "target_job": "construct or use the distance relationship while keeping coordinate roles matched",
            },
            "reasoning_route_template": [
                {"semantic_job": "read the coordinate roles"},
                {"semantic_job": "form the horizontal and vertical differences"},
                {"semantic_job": "combine them with the Pythagorean relationship"},
                {"semantic_job": "check the distance relationship"},
            ],
            "common_invalid_mechanisms": [],
        }

    def sample_core1(self, family_ref="MATH-PF-DISTANCE-FORMULA", bridge=None):
        asset = self.sample_asset()
        if bridge is not None:
            asset["ordinary_language_bridge"] = bridge
        self.assets = {asset["asset_id"]: asset}
        self.families = {"MATH-PF-DISTANCE-FORMULA": self.sample_family()}
        lesson = {
            "lesson_id": "MATH-C1L-0123456789abcdef",
            "learner_title": "Coordinate Distance",
            "capability_ref": "MATH-COORDINATE-DISTANCE",
            "treatment": "ACTIVE_STUDY",
            "scope_role": "DIRECT_ASSESSED",
            "assessment_question_refs": ["Q1"],
            "pck_asset_refs": [asset["asset_id"]],
            "required_pck_jobs": ["EXPLAIN"],
            "instructional_sequence": [
                "ANCHOR", "REPRESENT", "EXPLAIN", "RECONSTRUCT", "CONTRAST",
                "WORKED", "GUIDED", "FADED", "INDEPENDENT", "VERIFY", "TRANSFER",
            ],
            "representation_requirements": ["ORDERED_PAIR", "GEOMETRIC_DISTANCE_RELATION"],
            "problem_authoring_plans": [
                {
                    "plan_id": "MATH-PAP-0000000000000001",
                    "capability_ref": "MATH-COORDINATE-DISTANCE",
                    "problem_family_ref": family_ref,
                    "instance_role": role,
                    "must_be_new_instance": True,
                    "source_question_reuse": False,
                    "source_question_refs": [],
                    "variation_requirements": ["use a new instructional instance"],
                    "verification_obligations": ["VERIFY_DISTANCE_RELATION"],
                }
                for role in mod.REQUIRED_ROLES
            ],
            "verification_requirements": ["VERIFY_DISTANCE_RELATION"],
            "future_evidence_obligations": [{} for _ in range(8)],
            "scope_trace": {"study_scope_ref": "SCOPE", "study_model_capability_ref": "MATH-COORDINATE-DISTANCE"},
        }
        plan = {
            "core1_study_plan_id": "MATH-C1SP-0123456789abcdef",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "release_class": "PROVISIONAL_PENDING_EXPERT_REVIEW",
            "pck_authority": {
                "promotion_registry_ref": "REG",
                "promotion_registry_digest": "0" * 64,
                "bound_asset_refs": [asset["asset_id"]],
                "provisional_asset_refs": [asset["asset_id"]],
                "producer_legal_asset_refs": [],
                "expert_review_state": "PENDING",
                "release_legal": False,
            },
            "study_model_ref": "MODEL",
            "study_model_digest": "1" * 64,
            "pck_candidate_registry_ref": "CANDIDATES",
            "pck_promotion_registry_ref": "PROMOTIONS",
            "lessons": [lesson],
            "scope_completeness": {
                "required_capability_refs": ["MATH-COORDINATE-DISTANCE"],
                "covered_capability_refs": ["MATH-COORDINATE-DISTANCE"],
                "omitted_capability_refs": [],
                "status": "PASS",
            },
            "input_digest": "2" * 64,
            "plan_digest": "",
        }
        plan["plan_digest"] = mod.digest(plan, "plan_digest")
        return plan

    def test_family_bank_complete(self):
        expected = {
            "MATH-PF-EUCLID-CLASSIFICATION",
            "MATH-PF-DISTANCE-FORMULA",
            "MATH-PF-QUADRANT-SIGN-TRANSFORM",
            "MATH-PF-LINE-INTERCEPT",
            "MATH-PF-LINE-SLOPE-POINT",
            "MATH-PF-PAIR-COUNT",
            "MATH-PF-COLLINEARITY-SLOPE",
            "MATH-PF-EUCLID-PARALLEL-EXPLANATION",
            "MATH-PF-LINEAR-PARAMETER-SUFFICIENCY",
            "MATH-PF-INTERSECTION-THEN-LINE",
            "MATH-PF-EQUIDISTANT-AXIS-POINT",
            "MATH-PF-EQUILATERAL-COORDINATE",
            "MATH-PF-LINEAR-TREND-EXTRAPOLATION",
            "MATH-PF-RIVER-CURRENT-SYSTEM",
        }
        self.assertEqual(set(mod.FAMILY_BANKS), expected)
        for family in expected:
            self.assertGreaterEqual(len(mod.family_bank(family)), 6, family)

    def test_full_lesson_materializes_real_instances_and_pdf(self):
        plan = self.sample_core1()
        book = mod.manuscript(plan, self.assets, self.families)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(book, schema)
        lesson = book["lessons"][0]
        self.assertEqual(len(lesson["worked_examples"]), 2)
        self.assertTrue(set(mod.REQUIRED_ROLES).issubset(set(lesson["practice"])))
        self.assertNotIn("author a new instance", json.dumps(book).lower())
        self.assertEqual(book["quality_audit"]["status"], "PASS")
        self.assertGreaterEqual(book["quality_audit"]["actual_problem_instances"], 5)
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "book.pdf"
            meta = mod.render_pdf(book, pdf)
            self.assertTrue(pdf.exists())
            self.assertGreater(pdf.stat().st_size, 1000)
            self.assertEqual(len(meta["pdf_sha256"]), 64)

    def test_unsupported_family_fails_closed(self):
        plan = self.sample_core1(family_ref="MATH-PF-UNSEEN-FAMILY")
        with self.assertRaisesRegex(ValueError, "CORE1A_FAMILY_GENERATOR_MISSING"):
            mod.manuscript(plan, self.assets, self.families)

    def test_internal_jargon_is_a_publication_failure(self):
        plan = self.sample_core1(bridge="Author a new instance of this family before publication.")
        with self.assertRaisesRegex(ValueError, "CORE1A_QUALITY_GATE_FAILED"):
            mod.manuscript(plan, self.assets, self.families)


if __name__ == "__main__":
    unittest.main(verbosity=2)
