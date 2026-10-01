#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("v7", ROOT / "engine" / "validate_blueprint_v7.py")
v7 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(v7)
POLICY = json.loads((ROOT / "policies" / "v7-product-assurance-policy.json").read_text())


def disposition(state="OPTIONAL", ref=None):
    d = {"disposition": state}
    if ref is not None:
        d["realization_ref"] = ref
    return d


def base_ccbom():
    cores = {c: disposition() for c in v7.CORES}
    cores["CORE1A"] = disposition("MUST_REALIZE", "A1-BLOCK-EQ")
    cores["CORE1B"] = disposition("MUST_RECONSTRUCT", "B1-TTU-EQ")
    return {
        "schema_version": "7.0.0", "ccbom_id": "CCBOM-REDOX", "subtopic_id": "REDOX-STATE",
        "registry_ref": "REG-REDOX", "assets": [{"asset_id": "EQ-ZN-HALF", "asset_class": "EQUATION", "authority_ref": "REG-EQ-ZN", "core_dispositions": cores}],
        "coverage_summary": {"mandatory_total": 2, "mandatory_closed": 2, "unresolved_asset_ids": []}
    }


def base_similarity():
    return {
        "schema_version": "7.0.0",
        "non_frozen_prose": {"exclusions_applied": True, "verbatim_5gram_overlap": 0.04, "max_identical_contiguous_words": 12},
        "generated_example_comparisons": [{"relation_type": "STRUCTURAL_SIBLING", "pedagogical_reason": "new evidence chain", "components": {"problem_family": .8, "givens": .4, "numerical_values": .0, "target": .5, "representation": .3, "model_sequence": .6, "special_condition": .2, "solution_path": .5}}],
        "ab_comparisons": [{"relation_type": "PEDAGOGICAL_TRANSFORMATION", "review_reason": "A explains; B reconstructs", "components": {"example": .5, "representation": .4, "learner_action": .2, "sequence": .25}}]
    }


def core1_difficulty():
    dims = {k: 2 for k in POLICY["difficulty"]["core1_intrinsic_dimensions"]}
    return {"schema_version": "7.0.0", "kind": "INTRINSIC_DIFFICULTY", "product_mode": "CORE1B", "dimensions": dims, "derived_badge": "HARD", "final_badge": "HARD", "disagreement_reason": "", "explicit_owner_confirmation": False}


def core1b_purpose():
    return {"schema_version": "7.0.0", "product_mode": "CORE1B", "observed_actions": ["PREDICT_OR_RETRIEVE", "RECONSTRUCT", "EXPLAIN_OR_JUSTIFY", "VERIFY"], "dominant_mode": "CONSTRUCTIVE_TUTOR", "major_ttu_count": 5, "learner_generated_major_ttu_count": 4}


def core2b_purpose():
    return {"schema_version": "7.0.0", "product_mode": "CORE2B", "observed_actions": ["ATTEMPT", "MODEL_OR_REPRESENTATION_CHOICE", "FIRST_MOVE_COMMITMENT", "JUSTIFY", "VERIFY"], "dominant_mode": "OPEN_PROBLEM_TUTOR", "major_ttu_count": 5, "learner_generated_major_ttu_count": 4}


def learner_fit():
    return {"schema_version": "7.0.0", "product_mode": "CORE2B", "question_id": "CHEM-C2A-SRC-U2Q35", "purpose": "COMPETITIVE_EXAM", "purpose_used": True, "task_demand_score": 3, "compiler_support": "STANDARD", "fit_focus": ["representation", "model_selection"], "conditioning": {"mode": "KNOWLEDGE_EVIDENCE", "knowledge_percent": 90, "subdimensions": {"recognition": 85, "representation": 40, "model_selection": 45, "first_move": 80, "execution": 85, "explanation": 75, "verification": 70}}}


def source_question():
    return {"schema_version": "7.0.0", "question_id": "CHEM-C2A-SRC-U2Q15C", "source_class": "SOURCE_FROZEN", "learner_visible_source": "NCERT Class IX Science Exemplar — Unit 2 — Q15(c)", "source_title": "NCERT Class IX Science Exemplar", "source_unit_or_chapter": "Unit 2", "source_question_number": "Q15(c)", "source_locator": "Unit 2 Q15(c)", "source_stem_hash": "sha256:abc", "stem_identity_status": "EXACT", "answer_status": "CLOSED", "answer_ref": "ANS-U2Q15C", "canonical_solution_ref": "SOL-U2Q15C", "verification_ref": "VER-U2Q15C"}


class V7AssuranceTests(unittest.TestCase):
    def assertFails(self, fn, payload, fragment):
        with self.assertRaises(v7.BlueprintV7Error) as ctx:
            fn(payload, POLICY)
        self.assertIn(fragment, str(ctx.exception))

    def test_ccbom_passes_when_every_mandatory_asset_closes(self):
        self.assertEqual(v7.validate_ccbom(base_ccbom(), POLICY)["coverage_ratio"], 1.0)

    def test_ccbom_rejects_missing_core_disposition(self):
        p = base_ccbom(); del p["assets"][0]["core_dispositions"]["CORE2B"]
        self.assertFails(v7.validate_ccbom, p, "CORE_DISPOSITION_INCOMPLETE")

    def test_ccbom_rejects_missing_realization_ref(self):
        p = base_ccbom(); del p["assets"][0]["core_dispositions"]["CORE1B"]["realization_ref"]
        p["coverage_summary"] = {"mandatory_total": 2, "mandatory_closed": 1, "unresolved_asset_ids": ["EQ-ZN-HALF:CORE1B"]}
        self.assertFails(v7.validate_ccbom, p, "COVERAGE_NOT_CLOSED")

    def test_similarity_passes_structural_transformation(self):
        self.assertEqual(v7.validate_similarity(base_similarity(), POLICY)["status"], "PASS")

    def test_similarity_rejects_prose_copying(self):
        p = base_similarity(); p["non_frozen_prose"]["verbatim_5gram_overlap"] = .25
        self.assertFails(v7.validate_similarity, p, "5GRAM_OVERLAP_EXCESSIVE")

    def test_similarity_rejects_generated_near_duplicate(self):
        p = base_similarity(); p["generated_example_comparisons"][0]["components"] = {k: 1.0 for k in POLICY["similarity"]["generated_example"]["weights"]}
        self.assertFails(v7.validate_similarity, p, "EXAMPLE_NEAR_DUPLICATE")

    def test_similarity_rejects_a_b_pedagogical_clone(self):
        p = base_similarity(); p["ab_comparisons"][0]["components"] = {k: 1.0 for k in POLICY["similarity"]["pedagogical_ab"]["weights"]}
        self.assertFails(v7.validate_similarity, p, "PEDAGOGICAL_DUPLICATION_HARD_FAIL")

    def test_declared_fading_anchor_can_reuse_structure(self):
        p = base_similarity(); p["ab_comparisons"][0]["relation_type"] = "FADING_ANCHOR"; p["ab_comparisons"][0]["components"] = {k: 1.0 for k in POLICY["similarity"]["pedagogical_ab"]["weights"]}
        self.assertEqual(v7.validate_similarity(p, POLICY)["status"], "PASS")

    def test_core1_difficulty_is_independently_derived(self):
        r = v7.validate_difficulty(core1_difficulty(), POLICY)
        self.assertEqual((r["score"], r["derived_badge"]), (20, "HARD"))

    def test_core1_difficulty_rejects_bad_derived_badge(self):
        p = core1_difficulty(); p["derived_badge"] = "MEDIUM"
        self.assertFails(v7.validate_difficulty, p, "DERIVED_BADGE_DRIFT")

    def test_two_band_difficulty_override_requires_owner_confirmation(self):
        p = core1_difficulty(); p["dimensions"] = {k: 0 for k in POLICY["difficulty"]["core1_intrinsic_dimensions"]}; p["derived_badge"] = "EASY"; p["final_badge"] = "HARD"; p["disagreement_reason"] = "owner chooses depth"
        self.assertFails(v7.validate_difficulty, p, "OWNER_CONFIRMATION_REQUIRED")

    def test_core2_uses_task_demand_not_intrinsic_badge(self):
        p = {"schema_version": "7.0.0", "kind": "TASK_DEMAND", "product_mode": "CORE2B", "demand_score": 12, "demand_band": "HIGH"}
        self.assertEqual(v7.validate_difficulty(p, POLICY)["band"], "HIGH")

    def test_core1b_purpose_passes(self):
        self.assertEqual(v7.validate_purpose(core1b_purpose(), POLICY)["status"], "PASS")

    def test_purpose_rejects_missing_required_action(self):
        p = core1b_purpose(); p["observed_actions"].remove("VERIFY")
        self.assertFails(v7.validate_purpose, p, "MANDATORY_ACTION_MISSING")

    def test_b_layer_requires_majority_generated_ttu_actions(self):
        p = core2b_purpose(); p["learner_generated_major_ttu_count"] = 2
        self.assertFails(v7.validate_purpose, p, "LEARNER_GENERATION_RATIO_LOW")

    def test_learner_fit_recomputes_and_tightens_for_weak_focus(self):
        self.assertEqual(v7.validate_learner_fit(learner_fit(), POLICY)["validator_support"], "STANDARD")

    def test_learner_fit_rejects_compiler_mismatch(self):
        p = learner_fit(); p["compiler_support"] = "CHALLENGE_MINIMAL"
        self.assertFails(v7.validate_learner_fit, p, "COMPILER_VALIDATOR_MISMATCH")

    def test_owner_override_route_does_not_invent_percentage(self):
        p = {"schema_version": "7.0.0", "product_mode": "CORE2A", "question_id": "QX", "purpose": "REVISION", "purpose_used": True, "task_demand_score": 8, "compiler_support": "GUIDED", "fit_focus": ["recognition"], "conditioning": {"mode": "OWNER_OVERRIDE", "support_band": "GUIDED", "reason": "knowledge unavailable", "knowledge_percent": None}}
        self.assertEqual(v7.validate_learner_fit(p, POLICY)["conditioning_mode"], "OWNER_OVERRIDE")

    def test_owner_override_rejects_fabricated_percentage(self):
        p = {"schema_version": "7.0.0", "product_mode": "CORE2A", "question_id": "QX", "purpose": "REVISION", "purpose_used": True, "task_demand_score": 8, "compiler_support": "GUIDED", "fit_focus": ["recognition"], "conditioning": {"mode": "OWNER_OVERRIDE", "support_band": "GUIDED", "reason": "knowledge unavailable", "knowledge_percent": 50}}
        self.assertFails(v7.validate_learner_fit, p, "FABRICATED_PERCENT")

    def test_source_question_retains_visible_question_number_and_answer(self):
        self.assertTrue(v7.validate_question_custody(source_question(), POLICY)["answer_closed"])

    def test_source_question_number_must_be_learner_visible(self):
        p = source_question(); p["learner_visible_source"] = "NCERT Class IX Science Exemplar — Unit 2"
        self.assertFails(v7.validate_question_custody, p, "QUESTION_NUMBER_NOT_VISIBLE")

    def test_generated_question_discloses_origin(self):
        p = {"schema_version": "7.0.0", "question_id": "GEN-1", "source_class": "GENERATED_ORIGINAL", "learner_visible_source": "Generated original — grounded in PF-REDOX", "generated_grounding_refs": ["PF-REDOX"], "answer_status": "CLOSED", "answer_ref": "A", "canonical_solution_ref": "S", "verification_ref": "V"}
        self.assertEqual(v7.validate_question_custody(p, POLICY)["status"], "PASS")

    def test_question_without_answer_closure_fails(self):
        p = source_question(); p["answer_status"] = "OPEN"
        self.assertFails(v7.validate_question_custody, p, "ANSWER_CLOSURE_MISSING")

    def test_badges_keep_core1_and_core2_difficulty_names_separate(self):
        p1 = {"schema_version": "7.0.0", "product_mode": "CORE1B", "learner_visible_badges": ["BUCKET", "CONCEPT", "INTRINSIC_DIFFICULTY", "PURPOSE", "LEARNER_ACTION"], "student_knowledge_percent_visible": False}
        p2 = {"schema_version": "7.0.0", "product_mode": "CORE2B", "learner_visible_badges": ["BUCKET", "CONCEPT", "TASK_DEMAND", "PURPOSE", "SOURCE", "SUPPORT"], "student_knowledge_percent_visible": False}
        self.assertEqual(v7.validate_badges(p1, POLICY)["status"], "PASS")
        self.assertEqual(v7.validate_badges(p2, POLICY)["status"], "PASS")

    def test_badges_reject_knowledge_percentage_exposure(self):
        p = {"schema_version": "7.0.0", "product_mode": "CORE2B", "learner_visible_badges": ["TASK_DEMAND"], "student_knowledge_percent_visible": True}
        self.assertFails(v7.validate_badges, p, "KNOWLEDGE_PERCENT_BADGE_FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
