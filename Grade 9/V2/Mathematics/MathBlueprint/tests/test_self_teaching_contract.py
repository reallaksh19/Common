from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_self_teaching_contract",
    ROOT / "engine" / "validate_self_teaching_contract.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class SelfTeachingContractTests(unittest.TestCase):
    def load_policy(self):
        return json.loads((ROOT / "policies" / "math-self-teaching-policy.json").read_text(encoding="utf-8"))

    def test_canonical_policy_passes(self):
        mod.validate_contract(self.load_policy())

    def test_core1a_remains_declarative(self):
        doc = self.load_policy()
        doc["stage_profiles"]["CORE1A"]["mode"] = "OPEN_ENDED"
        with self.assertRaisesRegex(ValueError, "MATH_SELF_TEACHING_STAGE_MODE_DRIFT"):
            mod.validate_contract(doc)

    def test_core1b_is_open_ended_and_attempt_first(self):
        doc = self.load_policy()
        doc["stage_profiles"]["CORE1B"]["attempt_before_explanation"] = False
        with self.assertRaisesRegex(ValueError, "MATH_SELF_TEACHING_ATTEMPT_ORDER_DRIFT"):
            mod.validate_contract(doc)

    def test_core1b_requires_closed_self_guided_help_loop(self):
        doc = self.load_policy()
        doc["stage_profiles"]["CORE1B"]["help_path"].remove("REPRESENTATION_HELP")
        with self.assertRaisesRegex(ValueError, "MATH_CORE1B_SELF_GUIDED_HELP_INCOMPLETE"):
            mod.validate_contract(doc)

    def test_core2a_is_solution_apprenticeship(self):
        doc = self.load_policy()
        doc["stage_profiles"]["CORE2A"]["role"] = "QUESTION_BANK"
        with self.assertRaisesRegex(ValueError, "MATH_SELF_TEACHING_STAGE_ROLE_DRIFT"):
            mod.validate_contract(doc)

    def test_core2b_requires_recognition_to_method_help(self):
        doc = self.load_policy()
        doc["stage_profiles"]["CORE2B"]["help_path"].remove("METHOD_HELP")
        with self.assertRaisesRegex(ValueError, "MATH_CORE2B_TRANSFER_HELP_INCOMPLETE"):
            mod.validate_contract(doc)

    def test_core1_depth_cannot_depend_on_learner_knowledge(self):
        doc = self.load_policy()
        doc["generation_governance"]["core1_series"]["learner_knowledge_controls_depth"] = True
        # This invariant is enforced fail-closed at schema level before the
        # semantic validator. Either rejection path is correct; do not weaken
        # the schema merely to force a custom error code.
        with self.assertRaises(Exception):
            mod.validate_contract(doc)

    def test_badge_page_budget_cannot_drift(self):
        doc = self.load_policy()
        doc["generation_governance"]["core1_series"]["difficulty_badges"]["HARD"]["max_pages"] = 40
        with self.assertRaisesRegex(ValueError, "MATH_CORE1_DIFFICULTY_BADGE_POLICY_DRIFT"):
            mod.validate_contract(doc)

    def test_core2_calibration_applies_only_to_2a_2b(self):
        doc = self.load_policy()
        doc["generation_governance"]["core2_series"]["calibration_applies_to"] = ["CORE1A", "CORE2A", "CORE2B"]
        with self.assertRaises(Exception):
            mod.validate_contract(doc)

    def test_static_products_cannot_claim_mastery(self):
        doc = self.load_policy()
        doc["global_invariants"]["static_products_do_not_claim_learner_mastery"] = False
        with self.assertRaisesRegex(ValueError, "MATH_SELF_TEACHING_GLOBAL_INVARIANT_FALSE"):
            mod.validate_contract(doc)

    def test_frozen_core2_question_invariant_is_mandatory(self):
        doc = self.load_policy()
        doc["global_invariants"]["frozen_core2_questions_are_not_rewritten"] = False
        with self.assertRaisesRegex(ValueError, "MATH_SELF_TEACHING_GLOBAL_INVARIANT_FALSE"):
            mod.validate_contract(doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
