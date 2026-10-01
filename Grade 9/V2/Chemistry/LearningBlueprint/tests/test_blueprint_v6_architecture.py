import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "validate_blueprint_v6.py"
POLICY_PATH = ROOT / "policies" / "v6-dual-router-ttu-family-policy.json"
GOLDEN = ROOT / "golden" / "v6"

spec = importlib.util.spec_from_file_location("validate_blueprint_v6", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def load(name):
    return json.loads((GOLDEN / name).read_text(encoding="utf-8"))


class BlueprintV6ArchitectureTests(unittest.TestCase):
    def test_registry_cdau_sdu_and_both_lau_routes_pass(self):
        self.assertEqual(mod.validate_registry(load("registry-redox.json"))["status"], "PASS")
        self.assertEqual(mod.validate_cdau(load("cdau-redox.json"))["status"], "PASS")
        self.assertEqual(mod.validate_sdu(load("sdu-hard-redox.json"), POLICY)["status"], "PASS")
        self.assertEqual(mod.validate_lau(load("lau-knowledge-redox.json"), POLICY)["status"], "PASS")
        self.assertEqual(mod.validate_lau(load("lau-owner-redox.json"), POLICY)["status"], "PASS")

    def test_concept_and_problem_ttu_goldens_pass(self):
        c1a = load("concept-ttu-core1a-redox.json")
        c1b = load("concept-ttu-core1b-redox.json")
        c2a = load("problem-ttu-core2a-redox.json")
        c2b = load("problem-ttu-core2b-redox.json")
        self.assertEqual(mod.validate_concept_ttu(c1a)["status"], "PASS")
        self.assertEqual(mod.validate_concept_ttu(c1b)["status"], "PASS")
        self.assertEqual(mod.validate_problem_ttu(c2a)["status"], "PASS")
        self.assertEqual(mod.validate_problem_ttu(c2b)["status"], "PASS")
        self.assertEqual(mod.validate_ab_differentiation(c1a, c1b)["status"], "PASS")
        self.assertEqual(mod.validate_ab_differentiation(c2a, c2b)["status"], "PASS")

    def test_dialogues_and_self_help_goldens_pass(self):
        for name in ("dialogue-core1b-redox.json", "dialogue-core2b-redox.json"):
            self.assertEqual(mod.validate_tutor_dialogue(load(name))["status"], "PASS")
        for name in (
            "self-help-core1a-redox.json",
            "self-help-core1b-redox.json",
            "self-help-core2a-redox.json",
            "self-help-core2b-redox.json",
        ):
            self.assertEqual(mod.validate_self_help(load(name))["status"], "PASS")

    def test_sdu_rejects_learner_adaptation_fields(self):
        payload = load("sdu-hard-redox.json")
        payload["knowledge_percent"] = 50
        with self.assertRaisesRegex(mod.BlueprintV6Error, "SDU_LEARNER_ADAPTATION_LEAK"):
            mod.validate_sdu(payload, POLICY)

    def test_sdu_page_budget_is_ceiling_not_quality_target(self):
        payload = load("sdu-hard-redox.json")
        payload["core1a_plan"]["max_pages"] = 31
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CORE1A_PAGE_ENVELOPE_INVALID"):
            mod.validate_sdu(payload, POLICY)
        payload = load("sdu-hard-redox.json")
        payload["core1b_plan"]["page_count_is_quality_metric"] = True
        with self.assertRaisesRegex(mod.BlueprintV6Error, "PAGE_COUNT_QUALITY_METRIC_FORBIDDEN"):
            mod.validate_sdu(payload, POLICY)

    def test_lau_requires_evidence_or_owner_override(self):
        payload = load("lau-owner-redox.json")
        payload["conditioning"] = {"mode": "UNKNOWN"}
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CONDITIONING_UNRESOLVED"):
            mod.validate_lau(payload, POLICY)

    def test_lau_rejects_dual_conditioning(self):
        payload = load("lau-knowledge-redox.json")
        payload["conditioning"]["owner_override"] = {
            "support_band": "GUIDED",
            "reason": "invalid dual route",
            "preserve_system_finding": True,
        }
        with self.assertRaisesRegex(mod.BlueprintV6Error, "DUAL_CONDITIONING"):
            mod.validate_lau(payload, POLICY)

    def test_owner_override_cannot_fabricate_percent(self):
        payload = load("lau-owner-redox.json")
        payload["conditioning"]["knowledge_percent"] = 50
        with self.assertRaisesRegex(mod.BlueprintV6Error, "FABRICATED_PERCENT"):
            mod.validate_lau(payload, POLICY)

    def test_task_demand_is_required_and_machine_checked(self):
        payload = load("lau-knowledge-redox.json")
        del payload["task_demand"]["model_discrimination"]
        with self.assertRaisesRegex(mod.BlueprintV6Error, "TASK_DEMAND_MISSING"):
            mod.validate_lau(payload, POLICY)
        payload = load("lau-knowledge-redox.json")
        payload["task_demand"]["synthesis"] = 4
        with self.assertRaisesRegex(mod.BlueprintV6Error, "TASK_DEMAND_INVALID"):
            mod.validate_lau(payload, POLICY)

    def test_support_is_not_hardcoded_from_percentage_alone(self):
        payload = load("lau-knowledge-redox.json")
        payload["conditioning"]["learner_state"]["knowledge_percent"] = 90
        payload["resolved_support"]["support_band"] = "GUIDED"
        payload["core2a_plan"]["support_band"] = "GUIDED"
        payload["core2b_plan"]["support_band"] = "GUIDED"
        payload["task_demand"].update({k: 3 for k in mod.TASK_DIMS})
        result = mod.validate_lau(payload, POLICY)
        self.assertEqual(result["support_band"], "GUIDED")
        self.assertTrue(result["fit_used"])

    def test_core1b_requires_tutor_dialogue_and_core1a_forbids_it(self):
        payload = load("concept-ttu-core1b-redox.json")
        del payload["tutor_dialogue_ref"]
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CORE1B_TUTOR_DIALOGUE_REQUIRED"):
            mod.validate_concept_ttu(payload)
        payload = load("concept-ttu-core1a-redox.json")
        payload["tutor_dialogue_ref"] = "TD-NOT-ALLOWED"
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CORE1A_TUTOR_DIALOGUE_FORBIDDEN"):
            mod.validate_concept_ttu(payload)

    def test_core2b_requires_tutor_dialogue_and_core2a_forbids_it(self):
        payload = load("problem-ttu-core2b-redox.json")
        del payload["tutor_dialogue_ref"]
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CORE2B_TUTOR_DIALOGUE_REQUIRED"):
            mod.validate_problem_ttu(payload)
        payload = load("problem-ttu-core2a-redox.json")
        payload["tutor_dialogue_ref"] = "TD-NOT-ALLOWED"
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CORE2A_TUTOR_DIALOGUE_FORBIDDEN"):
            mod.validate_problem_ttu(payload)

    def test_tutor_dialogue_is_static_attempt_first_and_target_driven(self):
        payload = load("dialogue-core2b-redox.json")
        payload["delivery_mode"] = "LIVE"
        with self.assertRaisesRegex(mod.BlueprintV6Error, "LIVE_RUNTIME_FORBIDDEN"):
            mod.validate_tutor_dialogue(payload)
        payload = load("dialogue-core2b-redox.json")
        payload["initial_attempt"]["answer_hidden"] = False
        with self.assertRaisesRegex(mod.BlueprintV6Error, "ATTEMPT_FIRST_REQUIRED"):
            mod.validate_tutor_dialogue(payload)
        payload = load("dialogue-core2b-redox.json")
        payload["stage_selection_reason"] = ""
        with self.assertRaisesRegex(mod.BlueprintV6Error, "TEMPLATE_DRIVEN"):
            mod.validate_tutor_dialogue(payload)

    def test_ab_pedagogical_duplication_fails(self):
        a = load("concept-ttu-core1a-redox.json")
        b = load("concept-ttu-core1b-redox.json")
        b["differentiation_fingerprint"] = copy.deepcopy(a["differentiation_fingerprint"])
        with self.assertRaisesRegex(mod.BlueprintV6Error, "LEARNER_ACTION_DUPLICATION"):
            mod.validate_ab_differentiation(a, b)

    def test_problem_transfer_lineage_is_semantically_checked(self):
        payload = load("problem-ttu-core2b-redox.json")
        payload["transfer_lineage"]["relationship"] = "FADING_ANCHOR"
        payload["transfer_lineage"]["transfer_evidence_status"] = "NEAR_TRANSFER"
        with self.assertRaisesRegex(mod.BlueprintV6Error, "TRANSFER_LINEAGE_INVALID"):
            mod.validate_problem_ttu(payload)

    def test_cdau_cannot_take_over_sdu_or_lau(self):
        payload = load("cdau-redox.json")
        payload["release_policy"]["cdau_may_not_select_core2_support"] = False
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CDAU_LAU_AUTHORITY_LEAK"):
            mod.validate_cdau(payload)
        payload = load("cdau-redox.json")
        payload["release_policy"]["cdau_may_not_rewrite_intrinsic_difficulty"] = False
        with self.assertRaisesRegex(mod.BlueprintV6Error, "CDAU_SDU_AUTHORITY_LEAK"):
            mod.validate_cdau(payload)

    def test_registry_requires_stable_validated_provenanced_assets(self):
        payload = load("registry-redox.json")
        payload["assets"][1]["asset_id"] = payload["assets"][0]["asset_id"]
        with self.assertRaisesRegex(mod.BlueprintV6Error, "ASSET_ID_INVALID"):
            mod.validate_registry(payload)
        payload = load("registry-redox.json")
        payload["assets"][0]["validation_status"] = "DRAFT"
        with self.assertRaisesRegex(mod.BlueprintV6Error, "UNVALIDATED_ASSET"):
            mod.validate_registry(payload)

    def test_self_help_cannot_be_open(self):
        payload = load("self-help-core2b-redox.json")
        payload["independent_verification"]["required"] = False
        with self.assertRaisesRegex(mod.BlueprintV6Error, "SELF_HELP_CLOSURE_INCOMPLETE"):
            mod.validate_self_help(payload)


if __name__ == "__main__":
    unittest.main()
