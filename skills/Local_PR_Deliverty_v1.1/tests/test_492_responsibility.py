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

    def test_observation_preserves_every_canonical_release_state_without_authorizing(self):
        for release in sorted(responsibility.CANONICAL_RELEASE_STATES):
            with self.subTest(release=release):
                row = responsibility.responsibility_observation(parent_task(release), native_task())
                self.assertEqual(row["release_state"], release)

    def test_observation_sources_native_identity_and_acceptance_fields(self):
        row = responsibility.responsibility_observation(parent_task(), native_task())
        self.assertEqual(row, {
            "task_id": "PRD-017",
            "release_state": "READY",
            "acceptance_epoch_id": "AE-002",
            "acceptance_profile_ref": "APR-PRD-017-AE002",
            "acceptance_profile_digest": "a" * 64,
            "local_responsibility_complete": False,
        })

    def test_observation_rejects_synthetic_duplicate_fields_on_native_task(self):
        for field, value in (
            ("acceptance_epoch_ref", "AE-002"),
            ("release_state", "READY"),
            ("responsibility_complete", True),
        ):
            with self.subTest(field=field):
                task = native_task()
                task[field] = value
                with self.assertRaisesRegex(responsibility.ResponsibilityError, "synthetic observation field"):
                    responsibility.responsibility_observation(parent_task(), task)

    def test_observation_rejects_parent_profile_mismatch(self):
        parent = parent_task()
        parent["control_plane"]["responsibility_registry"][0]["acceptance_profile_digest"] = "b" * 64
        with self.assertRaisesRegex(responsibility.ResponsibilityError, "Profile digest differs"):
            responsibility.responsibility_observation(parent, native_task())

    def test_observation_keeps_local_completion_false_until_validation_binding_exists(self):
        for release in sorted(responsibility.CANONICAL_RELEASE_STATES):
            with self.subTest(release=release):
                row = responsibility.responsibility_observation(parent_task(release), native_task())
                self.assertFalse(row["local_responsibility_complete"])

    def test_observation_has_no_caller_completion_override(self):
        with self.assertRaises(TypeError):
            responsibility.responsibility_observation(
                parent_task(),
                native_task(),
                validated_delivery_result={
                    "record": "DELIVERY_RESULT",
                    "task_id": "PRD-017",
                    "responsibility_complete": True,
                },
            )

    # Mutation-envelope amendment requested by the SU-1 Coordinator/Super-Reviewer.
    def test_observation_rejects_release_state_complete(self):
        with self.assertRaisesRegex(responsibility.ResponsibilityError, "non-canonical"):
            responsibility.responsibility_observation(parent_task("COMPLETE"), native_task())

    def test_observation_rejects_missing_registry_entry(self):
        parent = parent_task()
        parent["control_plane"]["responsibility_registry"] = []
        with self.assertRaisesRegex(responsibility.ResponsibilityError, "absent"):
            responsibility.responsibility_observation(parent, native_task())

    def test_observation_rejects_duplicate_registry_entry(self):
        parent = parent_task()
        entry = copy.deepcopy(parent["control_plane"]["responsibility_registry"][0])
        parent["control_plane"]["responsibility_registry"].append(entry)
        with self.assertRaisesRegex(responsibility.ResponsibilityError, "Duplicate"):
            responsibility.responsibility_observation(parent, native_task())

    def test_observation_rejects_unestablished_bootstrap(self):
        parent = parent_task()
        parent["control_plane"]["bootstrap_state"] = "PENDING"
        with self.assertRaisesRegex(responsibility.ResponsibilityError, "not established"):
            responsibility.responsibility_observation(parent, native_task())

    def test_observation_rejects_non_responsibility_task(self):
        task = native_task()
        task["kind"] = "CHILD"
        with self.assertRaisesRegex(responsibility.ResponsibilityError, "only to RESPONSIBILITY"):
            responsibility.responsibility_observation(parent_task(), task)


if __name__ == "__main__":
    unittest.main()
