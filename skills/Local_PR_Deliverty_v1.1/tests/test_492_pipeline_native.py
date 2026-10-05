import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pipeline


NOW = datetime(2026, 10, 5, 8, 30, tzinfo=timezone.utc)


def native_task():
    return {
        "task_id": "PRD-017",
        "kind": "RESPONSIBILITY",
        "issue": 91,
        "pr": 105,
        "representation": {
            "kind": "SINGLE_ISSUE",
            "primary_issue": 91,
            "member_issues": [91],
            "predecessor_attempt_refs": [],
            "delivery_pr_history": [105],
        },
        "acceptance_epoch_id": "AE-001",
        "acceptance_profile_ref": "APR-PRD-017-AE001",
        "acceptance_profile_digest": "a" * 64,
    }


def parent(release="READY", with_permission=True):
    permissions = []
    if with_permission:
        permissions.append({
            "id": "PERM-1",
            "child_issue": None,
            "responsibility_task_id": "PRD-017",
            "issued_at": "2026-10-05T08:00:00Z",
            "coordinator": "coordinator",
            "parent_comment_ref": "https://github.com/owner/project/issues/492#issuecomment-1",
            "reason": "release",
            "during_record": None,
            "reviewed_head_sha": None,
            "mode": "SERIAL",
            "revoked_at": None,
        })
    return {
        "issue": 492,
        "parent_owner": "coordinator",
        "children": [],
        "start_permissions": permissions,
        "control_plane": {
            "bootstrap_state": "ESTABLISHED",
            "current_acceptance_epoch_id": "AE-001",
            "acceptance_basis_registry": [],
            "responsibility_registry": [{
                "task_id": "PRD-017",
                "release_state": release,
                "acceptance_profile_ref": "APR-PRD-017-AE001",
                "acceptance_profile_digest": "a" * 64,
            }],
            "authority_grant_refs": [],
        },
    }


def stage_record(stage="CODER", status="RUNNING"):
    return {
        "record_id": "R-1",
        "stage": stage,
        "started_at": "2026-10-05T08:05:00Z",
        "work_periods": [{"start": "2026-10-05T08:05:00Z", "end": None}],
        "writer_stopped": False,
        "status": status,
        "publications": {
            "start": {
                "comment_ref": "https://github.com/owner/project/issues/492#issuecomment-start",
                "published_at": "2026-10-05T08:04:30Z",
            },
            "end": None,
        },
        "parent_context": {
            "read_at": "2026-10-05T08:04:00Z",
            "through_comment_ref": "https://github.com/owner/project/issues/492#issuecomment-frontier",
        },
    }


class NativePipeline492Tests(unittest.TestCase):
    def test_permission_at_resolves_native_responsibility_target(self):
        grant = pipeline.permission_at(parent(), native_task(), NOW)
        self.assertIsNotNone(grant)
        self.assertEqual(grant["responsibility_task_id"], "PRD-017")

    def test_ready_native_coder_start_accepts_release_and_permission(self):
        pipeline.validate_evidence(stage_record(), parent(), native_task(), None, NOW)

    def test_blocked_native_release_rejects_stage_start_even_with_permission(self):
        with self.assertRaisesRegex(pipeline.RecordError, "BLOCKED_DEPENDENCY"):
            pipeline.validate_evidence(
                stage_record(), parent(release="BLOCKED_DEPENDENCY"), native_task(), None, NOW
            )

    def test_ready_native_release_still_requires_start_permission(self):
        with self.assertRaisesRegex(pipeline.RecordError, "Coordinator child permission"):
            pipeline.validate_evidence(stage_record(), parent(with_permission=False), native_task(), None, NOW)

    def test_legacy_issue_lookup_remains_supported(self):
        legacy_parent = parent(with_permission=False)
        legacy_parent["start_permissions"] = [{
            "id": "LEGACY-PERM",
            "child_issue": 91,
            "issued_at": "2026-10-05T08:00:00Z",
            "coordinator": "coordinator",
            "parent_comment_ref": "https://github.com/owner/project/issues/492#issuecomment-legacy",
            "reason": "legacy release",
            "during_record": None,
            "reviewed_head_sha": None,
            "mode": "SERIAL",
            "revoked_at": None,
        }]
        grant = pipeline.permission_at(legacy_parent, 91, NOW)
        self.assertEqual(grant["id"], "LEGACY-PERM")

    def test_pipeline_rejects_native_permission_to_unknown_registry_task(self):
        unknown = parent()
        unknown["start_permissions"][0]["responsibility_task_id"] = "PRD-999"
        tasks = {
            "PARENT-492": {"task_id": "PARENT-492", "kind": "PARENT", "pr": None},
            "PRD-017": native_task(),
        }
        with self.assertRaisesRegex(pipeline.RecordError, "declared production responsibility"):
            pipeline.validate_pipeline(unknown, tasks, [], {}, NOW)


if __name__ == "__main__":
    unittest.main()
