import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("embedded_coder_v35", ROOT / "scripts" / "embedded_coder_v35.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)

SHA = "a" * 40
DIGEST = "b" * 64
LOCAL_REF = f"reallaksh19/Common@{SHA}:skills/Local_PR_Deliverty_v1.1"
RELAY_REF = f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.5"


def context():
    return module.build_context(
        local_parent_task_id="PARENT-492",
        local_responsibility_task_id="PRD-492-A",
        local_protocol_ref=LOCAL_REF,
        local_protocol_digest=DIGEST,
        relay_protocol_ref=RELAY_REF,
        relay_protocol_digest=DIGEST,
        acceptance_epoch_ref="AE-002",
        acceptance_profile_ref="APR-PRD-492-A-AE002",
        acceptance_profile_digest=DIGEST,
    )


class EmbeddedCoderV35Tests(unittest.TestCase):
    def test_nested_identity_is_namespaced_below_local_responsibility(self):
        c = context()
        self.assertEqual(c["engineering_responsibility"], "ENG-PRD-492-A-CODER")
        self.assertEqual(c["local_responsibility_task_id"], "PRD-492-A")

    def test_non_prd_local_identity_is_rejected(self):
        with self.assertRaisesRegex(module.EmbeddedCoderError, "PRD"):
            module.engineering_responsibility("issue-493")

    def test_role_is_coder_only(self):
        c = context()
        c["role"] = "REVIEWER"
        with self.assertRaisesRegex(module.EmbeddedCoderError, "Coder-only"):
            module.validate_context(c)

    def test_v32_protocol_ref_is_not_valid_v35_authority(self):
        c = context()
        c["relay_protocol_ref"] = c["relay_protocol_ref"].replace("v3.5", "v3.2")
        with self.assertRaisesRegex(module.EmbeddedCoderError, "v3.5"):
            module.validate_context(c)

    def test_all_local_control_plane_authorities_are_explicitly_denied(self):
        c = context()
        self.assertEqual(set(c["prohibited_local_authorities"]), module.PROHIBITED_LOCAL_AUTHORITIES)
        c["prohibited_local_authorities"].remove("LOCAL_MERGE")
        with self.assertRaisesRegex(module.EmbeddedCoderError, "deny every"):
            module.validate_context(c)

    def test_each_local_authority_claim_is_rejected(self):
        for claim in module.PROHIBITED_LOCAL_AUTHORITIES:
            with self.subTest(claim=claim):
                with self.assertRaisesRegex(module.EmbeddedCoderError, "cannot exercise Local"):
                    module.reject_local_authority_claim(claim)

    def test_engineering_complete_never_completes_local_responsibility(self):
        result = module.build_task_result(
            context(),
            engineering_responsibility_complete=True,
            coverage="Coder implementation and exact-head evidence",
            evidence_refs=["TASK_EVIDENCE#1"],
        )
        self.assertTrue(result["engineering_responsibility_complete"])
        self.assertFalse(result["local_responsibility_complete"])
        self.assertEqual(result["result_scope"], "CODER_ENGINEERING_EXECUTION")

    def test_forged_local_complete_is_rejected(self):
        c = context()
        result = module.build_task_result(
            c,
            engineering_responsibility_complete=True,
            coverage="Coder scope",
            evidence_refs=["EV-1"],
        )
        result["local_responsibility_complete"] = True
        result["digest"] = module.canonical_digest({k: v for k, v in result.items() if k != "digest"})
        with self.assertRaisesRegex(module.EmbeddedCoderError, "never declare"):
            module.validate_task_result(c, result)

    def test_acceptance_profile_drift_invalidates_result(self):
        c = context()
        result = module.build_task_result(
            c,
            engineering_responsibility_complete=False,
            coverage="Partial Coder scope",
            evidence_refs=[],
        )
        result["acceptance_profile_digest"] = "c" * 64
        result["digest"] = module.canonical_digest({k: v for k, v in result.items() if k != "digest"})
        with self.assertRaisesRegex(module.EmbeddedCoderError, "profile digest drift"):
            module.validate_task_result(c, result)

    def test_result_is_content_addressed(self):
        c = context()
        result = module.build_task_result(
            c,
            engineering_responsibility_complete=True,
            coverage="Coder scope",
            evidence_refs=["EV-1"],
        )
        self.assertEqual(
            result["digest"],
            module.canonical_digest({k: v for k, v in result.items() if k != "digest"}),
        )
        result["coverage"] = "tampered"
        with self.assertRaisesRegex(module.EmbeddedCoderError, "digest mismatch"):
            module.validate_task_result(c, result)


if __name__ == "__main__":
    unittest.main()
