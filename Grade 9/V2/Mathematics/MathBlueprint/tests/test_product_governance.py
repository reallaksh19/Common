#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "validate_product_governance.py"
GOLD = ROOT / "golden" / "product_governance"
REGISTRY = ROOT / "golden" / "domain_registry" / "01-theory-of-equations-registry.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


gov = load_module("validate_product_governance", ENGINE)


class ProductGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.registry = load(REGISTRY)
        self.coverage = load(GOLD / "01-theory-of-equations-coverage.json")
        self.similarity = load(GOLD / "01-theory-of-equations-similarity.json")
        self.governance = load(GOLD / "01-theory-of-equations-governance.json")

    def test_full_release_golden_passes(self):
        result = gov.validate_release(self.registry, self.coverage, self.similarity, self.governance)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["coverage"]["asset_count"], len(self.registry["assets"]))

    def test_registry_asset_cannot_be_silently_skipped(self):
        bad = copy.deepcopy(self.coverage)
        bad["subtopics"][0]["asset_coverage"].pop()
        with self.assertRaisesRegex(ValueError, "COVERAGE_REGISTRY_ASSET_UNDISPOSED"):
            gov.validate_coverage(bad, self.registry)

    def test_semantic_asset_cannot_disappear_from_core1b(self):
        bad = copy.deepcopy(self.coverage)
        row = bad["subtopics"][0]["asset_coverage"][0]
        row["CORE1B"] = {
            "obligation":"NOT_APPLICABLE", "treatment":"NONE", "disposition":"NOT_APPLICABLE",
            "realization_refs":[], "omission_reason":None, "owner_override_ref":None,
        }
        with self.assertRaisesRegex(ValueError, "COVERAGE_SEMANTIC_TRACK_GAP"):
            gov.validate_coverage(bad, self.registry)

    def test_intentional_omission_requires_owner_and_reason(self):
        bad = copy.deepcopy(self.coverage)
        row = bad["subtopics"][0]["asset_coverage"][0]["CORE1A"]
        row.update({"disposition":"INTENTIONALLY_OMITTED", "realization_refs":[], "omission_reason":"Owner chose omission", "owner_override_ref":None})
        with self.assertRaisesRegex(ValueError, "COVERAGE_OMISSION_UNGOVERNED"):
            gov.validate_coverage(bad, self.registry)

    def test_exact_equation_repeat_requires_declared_lineage(self):
        bad = copy.deepcopy(self.similarity)
        bad["comparisons"][0]["declared_relation"] = "NONE"
        bad["comparisons"][0]["classification"] = "DISTINCT"
        with self.assertRaisesRegex(ValueError, "SIMILARITY_CANONICAL_REPEAT_LINEAGE_MISSING"):
            gov.validate_similarity(bad)

    def test_high_content_and_pedagogy_similarity_is_hard_duplicate(self):
        bad = copy.deepcopy(self.similarity)
        row = bad["comparisons"][1]
        row.update({"declared_relation":"NONE", "content_similarity":0.95, "pedagogical_similarity":0.90, "classification":"HARD_DUPLICATE"})
        with self.assertRaisesRegex(ValueError, "SIMILARITY_HARD_DUPLICATE"):
            gov.validate_similarity(bad)

    def test_strong_overlap_is_a_release_block_even_with_declared_semantic_reuse(self):
        bad = copy.deepcopy(self.similarity)
        row = bad["comparisons"][1]
        row.update({
            "declared_relation":"SEMANTIC_REUSE",
            "content_similarity":0.80,
            "pedagogical_similarity":0.70,
            "classification":"STRONG_OVERLAP",
        })
        with self.assertRaisesRegex(ValueError, "SIMILARITY_STRONG_PEDAGOGICAL_OVERLAP"):
            gov.validate_similarity(bad)

    def test_structural_sibling_must_live_inside_declared_band(self):
        bad = copy.deepcopy(self.similarity)
        bad["comparisons"][-1]["structural_similarity"] = 0.95
        with self.assertRaisesRegex(ValueError, "SIMILARITY_STRUCTURAL_SIBLING_RANGE_INVALID"):
            gov.validate_similarity(bad)

    def test_difficulty_badge_must_change_actual_product_controls(self):
        bad = copy.deepcopy(self.governance)
        bad["difficulty_audits"][0]["page_ceiling"] = 20
        with self.assertRaisesRegex(ValueError, "DIFFICULTY_BADGE_CONSEQUENCE_DRIFT"):
            gov.validate_governance(bad, self.registry)

    def test_owner_may_override_difficulty_without_rewriting_derived_finding(self):
        good = copy.deepcopy(self.governance)
        row = good["difficulty_audits"][0]
        row.update({
            "declared_badge":"EASY", "badge_authority":"OWNER", "operational_badge":"EASY",
            "page_ceiling":10, "research_level":"NONE", "owner_override_ref":"OVR-DIFF-001",
            "status":"OWNER_OVERRIDDEN_MISMATCH",
        })
        good["badge_sets"][0]["difficulty"] = "EASY"
        good["badge_sets"][0]["research_badge"] = "NONE"
        result = gov.validate_governance(good, self.registry)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(row["derived_badge"], "HARD")

    def test_core1b_cannot_collapse_to_passive_reading(self):
        bad = copy.deepcopy(self.governance)
        row = next(x for x in bad["purpose_audits"] if x["stage"] == "CORE1B")
        row["learner_actions"] = ["READ", "INSPECT"]
        with self.assertRaisesRegex(ValueError, "PURPOSE_CORE1B_RECONSTRUCTION_WEAK"):
            gov.validate_governance(bad, self.registry)

    def test_core2b_cannot_exceed_learner_demand_ceiling(self):
        bad = copy.deepcopy(self.governance)
        row = next(x for x in bad["learner_fit_audits"] if x["stage"] == "CORE2B")
        row["maximum_allowed_demand"] = "M3_INVERSE_TARGET"
        with self.assertRaisesRegex(ValueError, "LEARNER_FIT_DEMAND_CEILING_EXCEEDED"):
            gov.validate_governance(bad, self.registry)

    def test_capability_specific_knowledge_is_required_when_percentage_path_is_used(self):
        bad = copy.deepcopy(self.governance)
        bad["learner_fit_audits"][0]["calibration_basis"]["capability_knowledge"] = []
        with self.assertRaisesRegex(ValueError, "LEARNER_FIT_CAPABILITY_KNOWLEDGE_MISSING"):
            gov.validate_governance(bad, self.registry)

    def test_owner_waiver_is_legal_when_percentage_is_unavailable(self):
        good = copy.deepcopy(self.governance)
        for row in good["learner_fit_audits"]:
            row["calibration_basis"] = {"type":"OWNER_OVERRIDE", "owner_ref":"OWNER-001", "reason":"Learner knowledge percentage is unavailable."}
        self.assertEqual(gov.validate_governance(good, self.registry)["status"], "PASS")

    def test_every_frozen_source_question_must_keep_custody(self):
        bad = copy.deepcopy(self.governance)
        bad["question_custody"] = [x for x in bad["question_custody"] if x["origin"] != "SOURCE_CORE2"]
        with self.assertRaisesRegex(ValueError, "QUESTION_CUSTODY_SOURCE_QUESTION_MISSING"):
            gov.validate_governance(bad, self.registry)

    def test_generated_question_cannot_masquerade_as_source(self):
        bad = copy.deepcopy(self.governance)
        row = next(x for x in bad["question_custody"] if x["origin"] == "GENERATED_ORIGINAL")
        row["source_question_no"] = "Q2"
        row["source_relation"] = "EXACT_SOURCE"
        with self.assertRaisesRegex(ValueError, "QUESTION_CUSTODY_GENERATED_MASQUERADES_AS_SOURCE"):
            gov.validate_governance(bad, self.registry)

    def test_badge_refs_are_type_checked_against_registry(self):
        bad = copy.deepcopy(self.governance)
        bad["badge_sets"][0]["equation_refs"] = ["REG-MATH-CON-VIETA"]
        with self.assertRaisesRegex(ValueError, "BADGE_REF_TYPE_MISMATCH"):
            gov.validate_governance(bad, self.registry)


if __name__ == "__main__":
    unittest.main(verbosity=2)
