import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from execution_kernel import derive_next_action, validate_execution_state


SHA = "a" * 40
CANDIDATE = "c" * 40
DIGEST = "b" * 64


def state():
    value = {
        "schema_version": "EXECUTION_STATE_V1",
        "authority": "CANONICAL_EXECUTION_STATE",
        "identity": {
            "parent": "PARENT-506",
            "responsibility": "PRD-512-PROD-C4",
            "attempt": 1,
        },
        "repository": {
            "target_ref": "main",
            "target_sha": SHA,
            "branch": "prod/512-execution-kernel-v1",
            "pr": None,
            "candidate_sha": None,
        },
        "protocol": {
            "local_ref": f"reallaksh19/Common@{SHA}:skills/Local_PR_Deliverty_v1.1",
            "local_digest": DIGEST,
            "v35_ref": f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.5",
            "v35_digest": DIGEST,
        },
        "capability": {
            "active_role": "CODER",
            "capability_basis": ["issue://519"],
            "allowed_actions": ["WRITE_CANDIDATE", "RUN_VERIFICATION"],
            "forbidden_actions": ["ADVANCE_STAGE"],
        },
        "lifecycle": {
            "stage": "CODING",
            "last_completed_checkpoint": None,
        },
        "dependencies": {
            "satisfied": [],
            "blocked": [],
        },
        "verification": {
            "expectation_manifest_ref": "manifest://L0-L1-L2",
            "evidence_ledger_ref": None,
            "evidence_state": "MISSING",
            "evidence_candidate_sha": None,
            "unresolved_critical": [],
        },
        "contradictions": [],
        "next_action": {
            "type": "IMPLEMENT",
            "reason_code": "IMPLEMENTATION_REQUIRED",
            "basis_refs": [SHA],
        },
    }
    return value


def set_derived(value):
    value["next_action"] = derive_next_action(value)
    return value


class ExecutionKernelTests(unittest.TestCase):
    def test_missing_candidate_derives_implement(self):
        value = state()
        self.assertEqual(derive_next_action(value)["type"], "IMPLEMENT")
        self.assertEqual(validate_execution_state(value), [])

    def test_contradiction_dominates_dependencies_and_candidate_state(self):
        value = state()
        value["contradictions"] = ["provider says PR closed but state says active"]
        value["dependencies"]["blocked"] = [{
            "id": "DEP-1",
            "reason": "upstream unavailable",
            "evidence_refs": ["provider://dep-1"],
        }]
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "RECONCILE")
        self.assertEqual(value["next_action"]["reason_code"], "STATE_CONTRADICTION")
        self.assertEqual(validate_execution_state(value), [])

    def test_blocked_dependency_derives_wait(self):
        value = state()
        value["dependencies"]["blocked"] = [{
            "id": "DEP-1",
            "reason": "P0 authority closure pending",
            "evidence_refs": ["issue://506"],
        }]
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "WAIT_DEPENDENCY")
        self.assertEqual(validate_execution_state(value), [])

    def test_active_role_none_fails_closed(self):
        value = state()
        value["capability"]["active_role"] = "NONE"
        value["capability"]["allowed_actions"] = []
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "RECONCILE")
        self.assertEqual(value["next_action"]["reason_code"], "ACTIVE_ROLE_MISSING")
        self.assertEqual(validate_execution_state(value), [])

    def test_current_evidence_must_bind_exact_candidate(self):
        value = state()
        value["repository"]["candidate_sha"] = CANDIDATE
        value["verification"]["evidence_state"] = "CURRENT"
        value["verification"]["evidence_candidate_sha"] = "d" * 40
        value["verification"]["evidence_ledger_ref"] = "ledger://1"
        set_derived(value)
        errors = validate_execution_state(value)
        self.assertTrue(any("exact candidate_sha" in error for error in errors), errors)

    def test_stale_evidence_derives_verify(self):
        value = state()
        value["repository"]["candidate_sha"] = CANDIDATE
        value["verification"]["evidence_state"] = "STALE"
        value["verification"]["evidence_candidate_sha"] = "d" * 40
        value["verification"]["evidence_ledger_ref"] = "ledger://old"
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "VERIFY_CANDIDATE")
        self.assertEqual(value["next_action"]["reason_code"], "VERIFICATION_REQUIRED")
        self.assertEqual(validate_execution_state(value), [])

    def test_refuted_critical_derives_repair(self):
        value = state()
        value["repository"]["candidate_sha"] = CANDIDATE
        value["capability"]["allowed_actions"] = [
            "RUN_VERIFICATION",
            "REPAIR_CANDIDATE",
        ]
        value["capability"]["forbidden_actions"] = ["ADVANCE_STAGE"]
        value["verification"]["evidence_state"] = "CURRENT"
        value["verification"]["evidence_candidate_sha"] = CANDIDATE
        value["verification"]["evidence_ledger_ref"] = "ledger://current"
        value["verification"]["unresolved_critical"] = [{
            "id": "L0-CRIT-1",
            "state": "REFUTED",
            "evidence_refs": ["evidence://failure"],
        }]
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "REPAIR_CANDIDATE")
        self.assertEqual(value["next_action"]["reason_code"], "REPAIR_REQUIRED")
        self.assertEqual(validate_execution_state(value), [])

    def test_unknown_critical_derives_more_verification(self):
        value = state()
        value["repository"]["candidate_sha"] = CANDIDATE
        value["verification"]["evidence_state"] = "CURRENT"
        value["verification"]["evidence_candidate_sha"] = CANDIDATE
        value["verification"]["evidence_ledger_ref"] = "ledger://current"
        value["verification"]["unresolved_critical"] = [{
            "id": "L2-CRIT-2",
            "state": "UNKNOWN",
            "evidence_refs": [],
        }]
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "VERIFY_CANDIDATE")
        self.assertEqual(value["next_action"]["reason_code"], "CRITICAL_UNKNOWN")
        self.assertEqual(validate_execution_state(value), [])

    def test_verified_candidate_derives_advancement_only_with_capability(self):
        value = state()
        value["repository"]["candidate_sha"] = CANDIDATE
        value["capability"]["allowed_actions"] = ["ADVANCE_STAGE"]
        value["capability"]["forbidden_actions"] = []
        value["verification"]["evidence_state"] = "CURRENT"
        value["verification"]["evidence_candidate_sha"] = CANDIDATE
        value["verification"]["evidence_ledger_ref"] = "ledger://current"
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "ADVANCE_STAGE")
        self.assertEqual(validate_execution_state(value), [])

    def test_stopped_lifecycle_dominates_all_other_state(self):
        value = state()
        value["lifecycle"]["stage"] = "STOPPED"
        value["contradictions"] = ["ignored after terminal stop"]
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "STOPPED")
        self.assertEqual(value["next_action"]["reason_code"], "LIFECYCLE_STOPPED")
        self.assertEqual(validate_execution_state(value), [])

    def test_allowed_and_forbidden_actions_cannot_overlap(self):
        value = state()
        value["capability"]["forbidden_actions"] = ["WRITE_CANDIDATE"]
        set_derived(value)
        errors = validate_execution_state(value)
        self.assertTrue(any("both allowed and forbidden" in error for error in errors), errors)

    def test_stored_next_action_cannot_disagree_with_kernel(self):
        value = state()
        value["next_action"] = {
            "type": "ADVANCE_STAGE",
            "reason_code": "ADVANCEMENT_READY",
            "basis_refs": ["fake://basis"],
        }
        errors = validate_execution_state(value)
        self.assertTrue(any("does not match derived" in error for error in errors), errors)

    def test_missing_candidate_cannot_carry_evidence(self):
        value = state()
        value["verification"]["evidence_state"] = "CURRENT"
        value["verification"]["evidence_candidate_sha"] = CANDIDATE
        value["verification"]["evidence_ledger_ref"] = "ledger://impossible"
        set_derived(value)
        errors = validate_execution_state(value)
        self.assertTrue(any("missing candidate" in error for error in errors), errors)

    def test_schema_rejects_model_confidence_as_execution_authority(self):
        value = state()
        value["model_confidence"] = 0.99
        errors = validate_execution_state(value)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
