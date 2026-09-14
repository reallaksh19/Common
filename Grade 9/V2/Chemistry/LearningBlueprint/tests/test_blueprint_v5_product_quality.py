import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "validate_blueprint_v5.py"
POLICY_PATH = ROOT / "policies" / "v5-study-product-quality-policy.json"
GOLDEN = ROOT / "golden" / "v5"

spec = importlib.util.spec_from_file_location("validate_blueprint_v5", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def load(name):
    return json.loads((GOLDEN / name).read_text(encoding="utf-8"))


class BlueprintV5ProductQualityTests(unittest.TestCase):
    def test_all_four_product_goldens_pass(self):
        a = mod.validate_study_product(load("core1a-hard-study-product.json"), POLICY)
        b = mod.validate_study_product(load("core1b-hard-study-product.json"), POLICY)
        c = mod.validate_question_product(load("core2a-owner-question-product.json"), POLICY)
        d = mod.validate_question_product(load("core2b-owner-question-product.json"), POLICY)
        for result in (a, b, c, d):
            self.assertEqual(result["status"], "PASS")
            self.assertFalse(result["page_count_used_as_quality_metric"])

    def test_executive_summary_cannot_pass_as_core1a(self):
        data = load("core1a-hard-study-product.json")
        data["learning_atoms"][0]["required_jobs"] = ["MEANING", "ANSWER_CLOSURE"]
        with self.assertRaisesRegex(mod.BlueprintV5Error, "STUDY_MANDATORY_JOB_OMITTED"):
            mod.validate_study_product(data, POLICY)

    def test_declared_job_without_technical_object_fails(self):
        data = load("core1a-hard-study-product.json")
        data["technical_objects"] = [x for x in data["technical_objects"] if x["object_id"] != "OS-WORKED"]
        with self.assertRaisesRegex(mod.BlueprintV5Error, "STUDY_OBLIGATION_UNCLOSED"):
            mod.validate_study_product(data, POLICY)

    def test_hard_product_requires_additional_technical_depth(self):
        data = load("core1a-hard-study-product.json")
        data["technical_objects"] = [x for x in data["technical_objects"] if x["job"] != "MISCONCEPTION_CONTRAST"]
        for page in data["page_plan"]:
            page["technical_object_ids"] = [x for x in page["technical_object_ids"] if x != "H-MISCON"]
        with self.assertRaisesRegex(mod.BlueprintV5Error, "HARD_TECHNICAL_DEPTH_MISSING"):
            mod.validate_study_product(data, POLICY)

    def test_page_count_targeting_is_forbidden(self):
        data = load("core1a-hard-study-product.json")
        data["target_pages"] = 30
        with self.assertRaisesRegex(mod.BlueprintV5Error, "PAGE_COUNT_TARGETING_FORBIDDEN"):
            mod.validate_study_product(data, POLICY)

    def test_unjustified_white_space_fails_on_content_page(self):
        data = load("core1a-hard-study-product.json")
        data["page_plan"][1]["expected_active_area_ratio"] = 0.31
        with self.assertRaisesRegex(mod.BlueprintV5Error, "UNJUSTIFIED_EMPTY_PAGE_AREA"):
            mod.validate_study_product(data, POLICY)

    def test_workspace_blank_area_requires_real_learner_action(self):
        data = load("core1b-hard-study-product.json")
        page = next(x for x in data["page_plan"] if x["page_role"] == "WORKSPACE")
        page["learner_action_ids"] = []
        with self.assertRaisesRegex(mod.BlueprintV5Error, "WORKSPACE_NOT_JUSTIFIED"):
            mod.validate_study_product(data, POLICY)

    def test_cross_core_expository_duplication_fails(self):
        data = load("core1b-hard-study-product.json")
        data["cross_core_reuse_audit"]["shared_expository_block_count"] = 2
        with self.assertRaisesRegex(mod.BlueprintV5Error, "CROSS_CORE_EXPOSITORY_DUPLICATION"):
            mod.validate_study_product(data, POLICY)

    def test_generic_template_repetition_fails(self):
        data = load("core1b-hard-study-product.json")
        data["cross_core_reuse_audit"]["repeated_generic_template_fraction"] = 0.60
        with self.assertRaisesRegex(mod.BlueprintV5Error, "GENERIC_TEMPLATE_REPETITION_EXCESSIVE"):
            mod.validate_study_product(data, POLICY)

    def test_research_must_translate_to_real_technical_objects(self):
        data = load("core1a-hard-study-product.json")
        data["research_translation"][0]["technical_object_ids"] = ["NOT-A-REAL-OBJECT"]
        with self.assertRaisesRegex(mod.BlueprintV5Error, "RESEARCH_TRANSLATION_TECHNICAL_BINDING_INVALID"):
            mod.validate_study_product(data, POLICY)

    def test_question_without_full_solution_path_fails(self):
        data = load("core2a-owner-question-product.json")
        data["coverage_closure"]["full_solution_path_count"] = 1
        with self.assertRaisesRegex(mod.BlueprintV5Error, "QUESTION_EPISODE_CLOSURE_MISSING"):
            mod.validate_question_product(data, POLICY)

    def test_core2b_hint_must_bind_to_reasoning_step(self):
        data = load("core2b-owner-question-product.json")
        data["episodes"][0]["hint_bindings"][0]["binds_to_step_id"] = "UNKNOWN"
        with self.assertRaisesRegex(mod.BlueprintV5Error, "HINT_NOT_BOUND_TO_REASONING_STEP"):
            mod.validate_question_product(data, POLICY)

    def test_source_question_custody_drift_fails(self):
        data = load("core2a-owner-question-product.json")
        data["episodes"][0]["stem_custody"] = "GENERATED_UNDER_AUTHORITY"
        with self.assertRaisesRegex(mod.BlueprintV5Error, "SOURCE_QUESTION_CUSTODY_DRIFT"):
            mod.validate_question_product(data, POLICY)

    def test_core2_helper_prose_may_not_be_copied_between_a_and_b(self):
        data = load("core2b-owner-question-product.json")
        data["cross_core_reuse_audit"]["shared_helper_prose_count"] = 3
        with self.assertRaisesRegex(mod.BlueprintV5Error, "CROSS_CORE_HELPER_PROSE_DUPLICATION"):
            mod.validate_question_product(data, POLICY)

    def test_question_episode_cannot_omit_problem_solving_job(self):
        data = load("core2b-owner-question-product.json")
        data["episodes"][0]["required_jobs"].remove("REPRESENTATION_CHOICE")
        with self.assertRaisesRegex(mod.BlueprintV5Error, "QUESTION_MANDATORY_JOB_OMITTED"):
            mod.validate_question_product(data, POLICY)


if __name__ == "__main__":
    unittest.main(verbosity=2)
