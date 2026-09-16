from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_self_teaching_generation_spec",
    ROOT / "engine" / "validate_self_teaching_generation_spec.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

GOLDEN = ROOT / "golden" / "self_teaching" / "01-depth-and-knowledge-calibration.json"


class SelfTeachingGenerationSpecTests(unittest.TestCase):
    def load_golden(self):
        return json.loads(GOLDEN.read_text(encoding="utf-8"))

    def as_waiver(self, doc, *, support="STANDARD_GUIDED", c2a="M3_INVERSE_TARGET", c2b="M4_HIDDEN_STRUCTURE"):
        cal = doc["core2_calibration"]
        cal["learner_knowledge_percent"] = None
        cal["knowledge_percent_source_ref"] = None
        cal["knowledge_calibration_policy_ref"] = None
        cal["capability_knowledge"] = []
        cal["owner_waiver"] = {
            "owner_ref": "OWNER-001",
            "reason": "Knowledge percentage is not available for this cohort.",
            "selected_core2a_support_profile": support,
            "selected_core2a_max_demand_level": c2a,
            "selected_core2b_max_demand_level": c2b,
        }
        cal["resolved_core2a_support_profile"] = support
        cal["resolved_core2a_max_demand_level"] = c2a
        cal["resolved_core2b_max_demand_level"] = c2b
        return cal

    def test_golden_passes(self):
        mod.validate_generation_spec(self.load_golden())

    def test_medium_requires_research_brief_and_web_evidence(self):
        doc = self.load_golden()
        row = next(x for x in doc["core1_buckets"] if x["difficulty_badge"] == "MEDIUM")
        row["pedagogy_research_brief_ref"] = None
        with self.assertRaisesRegex(ValueError, "MATH_CORE1_RESEARCH_EVIDENCE_INSUFFICIENT"):
            mod.validate_generation_spec(doc)

    def test_hard_respects_30_page_ceiling(self):
        doc = self.load_golden()
        row = next(x for x in doc["core1_buckets"] if x["difficulty_badge"] == "HARD")
        row["target_page_budget"] = 31
        with self.assertRaisesRegex(ValueError, "MATH_CORE1_BUCKET_PAGE_BUDGET_EXCEEDED"):
            mod.validate_generation_spec(doc)

    def test_easy_allows_optional_bound_pedagogy_research(self):
        doc = self.load_golden()
        row = next(x for x in doc["core1_buckets"] if x["difficulty_badge"] == "EASY")
        row["pedagogy_research_brief_ref"] = "RESEARCH:optional-easy"
        row["pedagogy_web_research_refs"] = ["PED-WEB:optional-easy"]
        mod.validate_generation_spec(doc)

    def test_easy_optional_research_must_be_fully_bound(self):
        doc = self.load_golden()
        row = next(x for x in doc["core1_buckets"] if x["difficulty_badge"] == "EASY")
        row["pedagogy_research_brief_ref"] = "RESEARCH:half-bound"
        row["pedagogy_web_research_refs"] = []
        with self.assertRaisesRegex(ValueError, "MATH_CORE1_OPTIONAL_RESEARCH_BINDING_INCOMPLETE"):
            mod.validate_generation_spec(doc)

    def test_easy_stays_at_subtopic_level(self):
        doc = self.load_golden()
        row = next(x for x in doc["core1_buckets"] if x["difficulty_badge"] == "EASY")
        row["subsubtopic_plan"] = ["extra split"]
        with self.assertRaisesRegex(ValueError, "MATH_CORE1_SUBSUBTOPIC_DECOMPOSITION_FORBIDDEN"):
            mod.validate_generation_spec(doc)

    def test_derived_difficulty_badge_must_match_dimensions(self):
        doc = self.load_golden()
        row = next(x for x in doc["core1_buckets"] if x["difficulty_badge_basis"] == "CORE1_SEMANTIC_COMPLEXITY" and x["difficulty_badge"] == "MEDIUM")
        row["difficulty_badge"] = "EASY"
        with self.assertRaisesRegex(ValueError, "MATH_CORE1_DERIVED_DIFFICULTY_BADGE_MISMATCH"):
            mod.validate_generation_spec(doc)

    def test_core2_missing_percent_and_waiver_blocks(self):
        doc = self.load_golden()
        cal = doc["core2_calibration"]
        cal["learner_knowledge_percent"] = None
        cal["knowledge_percent_source_ref"] = None
        cal["knowledge_calibration_policy_ref"] = None
        cal["capability_knowledge"] = []
        cal["owner_waiver"] = None
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_CALIBRATION_EXACTLY_ONE_REQUIRED"):
            mod.validate_generation_spec(doc)

    def test_core2_cannot_have_percent_and_waiver(self):
        doc = self.load_golden()
        cal = doc["core2_calibration"]
        cal["owner_waiver"] = {
            "owner_ref": "OWNER-001",
            "reason": "Knowledge percentage unavailable",
            "selected_core2a_support_profile": cal["resolved_core2a_support_profile"],
            "selected_core2a_max_demand_level": cal["resolved_core2a_max_demand_level"],
            "selected_core2b_max_demand_level": cal["resolved_core2b_max_demand_level"],
        }
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_CALIBRATION_EXACTLY_ONE_REQUIRED"):
            mod.validate_generation_spec(doc)

    def test_percent_requires_source_and_policy(self):
        doc = self.load_golden()
        doc["core2_calibration"]["knowledge_calibration_policy_ref"] = None
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_KNOWLEDGE_PERCENT_BINDING_INCOMPLETE"):
            mod.validate_generation_spec(doc)

    def test_percent_requires_capability_specific_knowledge(self):
        doc = self.load_golden()
        doc["core2_calibration"]["capability_knowledge"] = []
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_CAPABILITY_KNOWLEDGE_REQUIRED"):
            mod.validate_generation_spec(doc)

    def test_duplicate_capability_knowledge_rejected(self):
        doc = self.load_golden()
        row = dict(doc["core2_calibration"]["capability_knowledge"][0])
        row["percent"] = row["percent"] - 5
        doc["core2_calibration"]["capability_knowledge"].append(row)
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_CAPABILITY_KNOWLEDGE_DUPLICATE"):
            mod.validate_generation_spec(doc)

    def test_owner_waiver_can_replace_unknown_percent(self):
        doc = self.load_golden()
        self.as_waiver(doc)
        mod.validate_generation_spec(doc)

    def test_owner_waiver_cannot_carry_fake_capability_knowledge(self):
        doc = self.load_golden()
        self.as_waiver(doc)
        doc["core2_calibration"]["capability_knowledge"] = [{"capability_ref":"MATH-X","percent":50}]
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_WAIVER_CANNOT_FAKE_CAPABILITY_KNOWLEDGE"):
            mod.validate_generation_spec(doc)

    def test_owner_waiver_cannot_be_overridden_silently(self):
        doc = self.load_golden()
        cal = self.as_waiver(doc, support="FOUNDATION_GUIDED", c2a="M1_CONTROLLED_VARIATION", c2b="M2_REPRESENTATION_TRANSFER")
        cal["resolved_core2a_support_profile"] = "ADVANCED_APPLIED"
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_OWNER_WAIVER_SUPPORT_DRIFT"):
            mod.validate_generation_spec(doc)

    def test_owner_waiver_core2a_ceiling_is_bound(self):
        doc = self.load_golden()
        cal = self.as_waiver(doc, support="STANDARD_GUIDED", c2a="M1_CONTROLLED_VARIATION", c2b="M4_HIDDEN_STRUCTURE")
        cal["resolved_core2a_max_demand_level"] = "M3_INVERSE_TARGET"
        with self.assertRaisesRegex(ValueError, "MATH_CORE2_OWNER_WAIVER_CORE2A_CEILING_DRIFT"):
            mod.validate_generation_spec(doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
