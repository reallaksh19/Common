import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("local_v11_integrated", ROOT / "scripts" / "local_v11_integrated.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)

SHA = "a" * 40
DIGEST = "b" * 64
LOCAL_REF = f"reallaksh19/Common@{SHA}:skills/Local_PR_Deliverty_v1.1"
V35_REF = f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.5"


def local_task(complete=False):
    return {
        "kind": "RESPONSIBILITY",
        "task_id": "PRD-492-A",
        "acceptance_epoch_ref": "AE-002",
        "acceptance_profile_ref": "APR-PRD-492-A-AE002",
        "acceptance_profile_digest": DIGEST,
        "release_state": "READY",
        "responsibility_complete": complete,
    }


def v35_result(local_complete=False, coder_complete=True):
    return {
        "result_scope": "CODER_ENGINEERING_EXECUTION",
        "engineering_responsibility": "ENG-PRD-492-A-CODER",
        "engineering_responsibility_complete": coder_complete,
        "local_responsibility_task_id": "PRD-492-A",
        "local_responsibility_complete": local_complete,
        "acceptance_epoch_ref": "AE-002",
        "acceptance_profile_ref": "APR-PRD-492-A-AE002",
        "acceptance_profile_digest": DIGEST,
    }


class LocalV11IntegratedTests(unittest.TestCase):
    def test_coder_complete_does_not_complete_local_responsibility(self):
        row = module.observe_responsibility(local_task(False), v35_result(False, True))
        self.assertTrue(row["coder_engineering_complete"])
        self.assertFalse(row["local_responsibility_complete"])

    def test_local_complete_may_only_come_from_local_task(self):
        row = module.observe_responsibility(local_task(True), v35_result(False, True))
        self.assertTrue(row["local_responsibility_complete"])

    def test_v35_cannot_claim_local_completion(self):
        with self.assertRaisesRegex(module.IntegratedModeError, "illegally claims"):
            module.observe_responsibility(local_task(False), v35_result(True, True))

    def test_stale_acceptance_profile_is_rejected(self):
        result = v35_result()
        result["acceptance_profile_digest"] = "c" * 64
        with self.assertRaisesRegex(module.IntegratedModeError, "profile digest is stale"):
            module.observe_responsibility(local_task(), result)

    def test_v31_provider_cannot_select_integrated_mode(self):
        with self.assertRaisesRegex(module.IntegratedModeError, "V3.5"):
            module.build_integrated_context(
                parent_task_id="PARENT-492",
                local_protocol_ref=LOCAL_REF,
                local_protocol_digest=DIGEST,
                engineering_evidence_provider_ref=V35_REF.replace("v3.5", "v3.1"),
                engineering_evidence_provider_digest=DIGEST,
                responsibility_observations=[],
            )

    def test_integrated_mode_has_complete_non_authority_boundary(self):
        row = module.observe_responsibility(local_task(), v35_result())
        context = module.build_integrated_context(
            parent_task_id="PARENT-492",
            local_protocol_ref=LOCAL_REF,
            local_protocol_digest=DIGEST,
            engineering_evidence_provider_ref=V35_REF,
            engineering_evidence_provider_digest=DIGEST,
            responsibility_observations=[row],
        )
        self.assertEqual(set(context["non_authorities"]), module.NON_AUTHORITIES)
        self.assertEqual(context["authority"], "OBSERVATION_ONLY")
        self.assertEqual(context["legacy_v31_interpretation"], "READABLE_COMPATIBILITY_ONLY")

    def test_every_forbidden_authority_action_is_rejected(self):
        for action in module.NON_AUTHORITIES:
            with self.subTest(action=action):
                with self.assertRaisesRegex(module.IntegratedModeError, "cannot exercise authority"):
                    module.assert_observation_only_action(action)

    def test_status_projection_never_returns_pass_or_merge_authority(self):
        row = module.observe_responsibility(local_task(False), v35_result(False, True))
        context = module.build_integrated_context(
            parent_task_id="PARENT-492",
            local_protocol_ref=LOCAL_REF,
            local_protocol_digest=DIGEST,
            engineering_evidence_provider_ref=V35_REF,
            engineering_evidence_provider_digest=DIGEST,
            responsibility_observations=[row],
        )
        status = module.derive_programme_status(context)
        self.assertEqual(status["engineering_acceptance_verdict"], "NOT_AUTHORIZED")
        self.assertEqual(status["merge_authority"], "NOT_AUTHORIZED")
        self.assertEqual(status["coder_engineering_complete"], 1)
        self.assertEqual(status["local_responsibilities_complete"], 0)


if __name__ == "__main__":
    unittest.main()
