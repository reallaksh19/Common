#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ENGINE = HERE.parents[1] / "engine"
sys.path.insert(0, str(ENGINE))

import build_math_core1a_textbook as base
import core1a_capability_authoring as cap

cap.install()


class CapabilityAwareAuthoringTests(unittest.TestCase):
    def lesson(self, capability, family, pck):
        return {
            "lesson_id": "MATH-C1L-aaaaaaaaaaaaaaaa",
            "learner_title": capability.replace("MATH-", "").replace("-", " ").title(),
            "capability_ref": capability,
            "treatment": "ACTIVE_STUDY",
            "assessment_question_refs": ["Q1"],
            "pck_asset_refs": [pck],
            "problem_authoring_plans": [
                {"instance_role": role, "problem_family_ref": family}
                for role in base.REQUIRED_ROLES
            ],
            "verification_requirements": ["VERIFY_RESULT"],
        }

    def test_binomial_square_uses_capability_instances_not_generic_axis_problem(self):
        capability = "MATH-BINOMIAL-SQUARE-EXPANSION"
        family = "MATH-PF-EQUIDISTANT-AXIS-POINT"
        pck = "MATH-PCK-BINOMIAL-SQUARE-RECONSTRUCTION-v1"
        lesson = self.lesson(capability, family, pck)
        assets = {
            pck: {
                "asset_id": pck,
                "capability_refs": [capability],
                "anchor": "A binomial square is a repeated product, so both cross-products matter.",
                "ordinary_language_bridge": "Write the square as two equal brackets before expanding.",
                "reconstruction_route": ["rewrite as a repeated product", "multiply every term", "combine the cross-products"],
                "misconception_discriminator": {"candidate_wrong_model": "square each term and omit the middle term", "probe": "ask for the repeated product"},
                "repair_route": ["write both brackets", "show both cross-products"],
                "verification_method": ["multiply the brackets back"],
            }
        }
        families = {
            family: {
                "family_id": family,
                "problem_signature": {"recognition_cues": ["point on an axis", "equal distances"], "target_job": "model an equal-distance condition"},
                "reasoning_route_template": [],
                "common_invalid_mechanisms": [],
            }
        }
        out = cap.authored_lesson(lesson, assets, families)
        self.assertEqual(out["title"], "Squaring a Binomial Without Losing the Middle Term")
        combined = " ".join(x["prompt"] for x in out["worked_examples"]).lower()
        self.assertIn("expand", combined)
        self.assertIn("²", combined)
        self.assertNotEqual(out["title"], base.DISPLAY_TITLES[family])

    def test_asset_selection_prefers_exact_capability_match(self):
        lesson = self.lesson("MATH-LINEAR-SYSTEM-SETUP", "MATH-PF-INTERSECTION-THEN-LINE", "A")
        lesson["pck_asset_refs"] = ["A", "B"]
        assets = {
            "A": {"asset_id": "A", "capability_refs": ["MATH-LINEAR-SYSTEM-SOLVE"]},
            "B": {"asset_id": "B", "capability_refs": ["MATH-LINEAR-SYSTEM-SETUP"]},
        }
        self.assertEqual(cap.choose_asset_for_capability(lesson, assets)["asset_id"], "B")

    def test_all_current_capability_overrides_have_six_instances(self):
        for capability, factory in cap.CUSTOM_BANKS.items():
            rows = factory()
            self.assertGreaterEqual(len(rows), 6, capability)
            for row in rows:
                self.assertTrue(row.prompt.strip(), capability)
                self.assertGreaterEqual(len(row.steps), 2, capability)
                self.assertEqual(len(row.hints), 3, capability)


if __name__ == "__main__":
    unittest.main(verbosity=2)
