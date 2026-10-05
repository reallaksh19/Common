import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import responsibility


def native_task():
    return {
        "task_id": "PRD-017",
        "kind": "RESPONSIBILITY",
        "issue": 91,
        "pr": 112,
        "representation": {
            "kind": "CONTINUATION",
            "primary_issue": 91,
            "member_issues": [91],
            "predecessor_attempt_refs": ["PR-105"],
            "delivery_pr_history": [105, 112],
        },
        "acceptance_epoch_id": "AE-002",
        "acceptance_profile_ref": "APR-PRD-017-AE002",
        "acceptance_profile_digest": "a" * 64,
    }


def parent_task(release="READY"):
    return {
        "task_id": "PARENT-492",
        "kind": "PARENT",
        "control_plane": {
            "bootstrap_state": "ESTABLISHED",
            "current_acceptance_epoch_id": "AE-002",
            "acceptance_basis_registry": [],
            "responsibility_registry": [{
                "task_id": "PRD-017",
                "release_state": release,
                "acceptance_profile_ref": "APR-PRD-017-AE002",
                "acceptance_profile_digest": "a" * 64,
            }],
            "authority_grant_refs": [],
        },
    }


class ResponsibilityTests(unittest.TestCase):
    def test_native_task_id_is_the_responsibility_identity(self):
        view = responsibility.responsibility_view(native_task())
        self.assertEqual(view["identity"], "PRD-017")
        self.assertEqual(view["identity_mode"], "NATIVE_TASK_ID")

    def test_legacy_child_is_projected_without_rewriting_history(self):
        child = {"task_id": "child-91", "kind": "CHILD", "issue": 91, "pr": 105}
        before = copy.deepcopy(child)
        view = responsibility.responsibility_view(child)
        self.assertEqual(view["identity"], "child-91")
        self.assertEqual(view["identity_mode"], "LEGACY_TASK_ID")
        self.assertEqual(view["representation"]["kind"], "SINGLE_ISSUE")
        self.assertEqual(child, before)

    def test_replacement_pr_is_sequential_history_not_new_responsibility(self):
        task = native_task()
        responsibility.validate_material_candidate(task)
        self.assertEqual(task["task_id"], "PRD-017")
        self.assertEqual(task["representation"]["delivery_pr_history"], [105, 112])

    def test_active_pr_must_be_latest_delivery_candidate(self):
        task = native_task()
        task["pr"] = 105
        with self.assertRaises(responsibility.ResponsibilityError):
            responsibility.validate_material_candidate(task)

    def test_native_permission_targets_task_id_not_issue_number(self):
        task = native_task()
        self.assertTrue(responsibility.permission_targets_task(
            {"responsibility_task_id": "PRD-017", "child_issue": None}, task
        ))
        self.assertFalse(responsibility.permission_targets_task(
            {"responsibility_task_id": "PRD-018", "child_issue": 91}, task
        ))

    def test_legacy_permission_still_targets_child_issue(self):
        child = {"task_id": "child-91", "kind": "CHILD", "issue": 91, "pr": 105}
        self.assertTrue(responsibility.permission_targets_task(
            {"child_issue": 91}, child
        ))

    def test_parent_registry_release_is_per_responsibility(self):
        responsibility.validate_native_release(parent_task("READY"), native_task())
        with self.assertRaises(responsibility.ResponsibilityError):
            responsibility.validate_native_release(parent_task("BLOCKED_DEPENDENCY"), native_task())

    def test_parent_profile_must_match_responsibility_profile(self):
        parent = parent_task()
        parent["control_plane"]["responsibility_registry"][0]["acceptance_profile_digest"] = "b" * 64
        with self.assertRaises(responsibility.ResponsibilityError):
            responsibility.validate_native_release(parent, native_task())


if __name__ == "__main__":
    unittest.main()
