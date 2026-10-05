import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def base_task(kind):
    return {
        "record": "TASK",
        "version": "1.1",
        "task_id": "PARENT-492" if kind == "PARENT" else ("PRD-017" if kind == "RESPONSIBILITY" else "child-91"),
        "kind": kind,
        "repository": "owner/project",
        "issue": 492 if kind == "PARENT" else 91,
        "parent_issue": None if kind == "PARENT" else 492,
        "pr": None if kind == "PARENT" else 105,
        "parent_owner": "coordinator",
        "spec_ref": "https://example.invalid/spec",
        "spec_digest": "1" * 64,
        "protocol_ref": "reallaksh19/Common@" + "2" * 40 + ":skills/Local_PR_Deliverty_v1.1",
        "project_protocol_ref": "owner/project@" + "3" * 40 + ":review/protocol.json",
        "project_protocol_digest": "4" * 64,
        "scope": "bounded responsibility",
        "acceptance": [] if kind == "RESPONSIBILITY" else [{
            "id": "AC-1",
            "requirement": "works",
            "required": True,
            "verification_method_ids": ["VM-1"],
            "super_review_required": True,
        }],
        "children": [],
        "required_checks": [],
        "owner_principals": ["owner"],
        "required_check_policy": {
            "source_ref": "policy",
            "digest": "5" * 64,
            "provider": "GITHUB_ACTIONS",
        },
        "required_check_contracts": [],
        "waivable_criteria": [],
        "protocol_digest": "6" * 64,
        "role_principals": {
            "CODER": ["coder"],
            "REVIEWER": ["reviewer"],
            "COORDINATOR": ["coordinator"],
        },
        "stacked_dependencies": [],
        "waivable_required_checks": [],
        "target_ref": "refs/heads/main",
    }


def errors(record):
    return [e.message for e in sorted(VALIDATOR.iter_errors(record), key=lambda e: str(e.path))]


class TaskSchema492Tests(unittest.TestCase):
    def test_native_responsibility_uses_task_id_as_prd_identity(self):
        task = base_task("RESPONSIBILITY")
        task.update(
            representation={
                "kind": "SINGLE_ISSUE",
                "primary_issue": 91,
                "member_issues": [91],
                "predecessor_attempt_refs": [],
                "delivery_pr_history": [105],
            },
            acceptance_epoch_id="AE-001",
            acceptance_profile_ref="APR-PRD-017-AE001",
            acceptance_profile_digest="7" * 64,
        )
        self.assertEqual([], errors(task))

    def test_native_responsibility_rejects_non_prd_identity(self):
        task = base_task("RESPONSIBILITY")
        task["task_id"] = "issue-91"
        task.update(
            representation={
                "kind": "SINGLE_ISSUE",
                "primary_issue": 91,
                "member_issues": [91],
                "predecessor_attempt_refs": [],
                "delivery_pr_history": [105],
            },
            acceptance_epoch_id="AE-001",
            acceptance_profile_ref="APR-PRD-017-AE001",
            acceptance_profile_digest="7" * 64,
        )
        self.assertTrue(errors(task))

    def test_issue_set_is_provider_representation_not_multiple_active_candidates(self):
        task = base_task("RESPONSIBILITY")
        task.update(
            representation={
                "kind": "ISSUE_SET",
                "primary_issue": 91,
                "member_issues": [91, 92, 93],
                "predecessor_attempt_refs": [],
                "delivery_pr_history": [101, 105],
            },
            pr=105,
            acceptance_epoch_id="AE-001",
            acceptance_profile_ref="APR-PRD-017-AE001",
            acceptance_profile_digest="7" * 64,
        )
        self.assertEqual([], errors(task))
        self.assertEqual(task["pr"], 105)

    def test_parent_control_plane_has_per_responsibility_release(self):
        task = base_task("PARENT")
        task.update(
            workspace="/work/project",
            timers={
                "poll_seconds": 60,
                "stage_minutes": {"CODER": 15, "REVIEWER": 15, "COORDINATOR": 45, "PARENT_CHECK": 45},
                "ci_wait_minutes": 30,
                "recovery_grace_minutes": 5,
                "handover_seconds": 0,
                "override_reason": None,
            },
            owner_commands=[],
            merge_authority={"mode": "OWNER_ONLY", "reference": None, "delegate_principal": None},
            start_permissions=[],
            control_plane={
                "bootstrap_state": "ESTABLISHED",
                "current_acceptance_epoch_id": "AE-001",
                "acceptance_basis_registry": [{
                    "epoch_id": "AE-001",
                    "epoch_ref": "acceptance://AE-001",
                    "epoch_digest": "8" * 64,
                }],
                "responsibility_registry": [
                    {
                        "task_id": "PRD-001",
                        "release_state": "READY",
                        "acceptance_profile_ref": "APR-PRD-001-AE001",
                        "acceptance_profile_digest": "9" * 64,
                    },
                    {
                        "task_id": "PRD-002",
                        "release_state": "BLOCKED_DEPENDENCY",
                        "acceptance_profile_ref": "APR-PRD-002-AE001",
                        "acceptance_profile_digest": "a" * 64,
                    },
                ],
                "authority_grant_refs": ["AUTH-1"],
            },
        )
        self.assertEqual([], errors(task))

    def test_legacy_child_still_valid_without_native_fields(self):
        task = base_task("CHILD")
        self.assertEqual([], errors(task))

    def test_responsibility_cannot_duplicate_acceptance_denominator(self):
        task = base_task("RESPONSIBILITY")
        task["acceptance"] = [{
            "id": "AC-1",
            "requirement": "duplicated",
            "required": True,
            "verification_method_ids": ["VM-1"],
            "super_review_required": True,
        }]
        task.update(
            representation={
                "kind": "SINGLE_ISSUE",
                "primary_issue": 91,
                "member_issues": [91],
                "predecessor_attempt_refs": [],
                "delivery_pr_history": [105],
            },
            acceptance_epoch_id="AE-001",
            acceptance_profile_ref="APR-PRD-017-AE001",
            acceptance_profile_digest="7" * 64,
        )
        self.assertTrue(errors(task))


if __name__ == "__main__":
    unittest.main()
