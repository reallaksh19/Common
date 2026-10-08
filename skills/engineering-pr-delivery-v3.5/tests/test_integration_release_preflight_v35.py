"""R7-U2 release preflight: no source approval means HOLD, no silent deployment."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import delp_projection_v35 as DELP
import integration_release_preflight_v35 as R7
import integration_scoreboard_publish_v35 as PUBLISH
import test_integration_cold_entry_v35 as COLD_TESTS
import test_integration_graph_authority_v35 as GRAPH_TESTS


class Provider(COLD_TESTS.Provider):
    def __init__(self):
        super().__init__()
        self.workflow_state = "active"
        self.workflow_path = R7.DEFAULT_WORKFLOW
        self.workflow_guards = True
        self.workflow_calls = []
        self.default_head = "9" * 40

    def _gh(self, *args):
        self.workflow_calls.append(args)
        if args == (f"repos/{self.repository}",):
            return {"default_branch": "main"}
        if args == (
            f"repos/{self.repository}/actions/workflows/v35-smart-scoreboard.yml",
        ):
            return {"path": self.workflow_path, "state": self.workflow_state}
        raise DELP.DelpError("GitHub provider request not found")

    def get_file_at(self, commit_sha, path):
        if path != R7.DEFAULT_WORKFLOW:
            return super().get_file_at(commit_sha, path)
        if commit_sha != self.default_head:
            raise DELP.DelpError("workflow commit not the default branch head")
        if not self.workflow_guards:
            return {"content": "name: insecure-event-handler\non: workflow_dispatch\n"}
        return {"content": "\n".join(R7._REQUIRED_WORKFLOW_SOURCE)}


class ReleasePreflightTests(unittest.TestCase):
    def setUp(self):
        self.t = Provider()
        self.root = COLD_TESTS.ROOT_URL

    def preflight(self, permission=None, provider=None):
        return R7.assess(
            provider or self.t, self.root,
            scoreboard_approval_ref=permission,
        )

    def test_actual_missing_graph_returns_explicit_hold_and_zero_writes(self):
        outcome = self.preflight()
        self.assertEqual("HOLD_GRAPH_SOURCE_NOT_APPROVED", outcome["status"])
        self.assertEqual("MISSING_ON_GOVERNING_ROOT", outcome["graph_selection"])
        self.assertEqual("NOT_EVALUATED_NO_APPROVED_GRAPH", outcome["scoreboard_permission"])
        self.assertEqual("NONE", outcome["programme_ic_credit"])
        self.assertEqual("SOURCE_NOT_PROVEN", outcome["native_custody"])
        self.assertFalse(outcome["live_status_writer_invoked"])
        self.assertEqual([], self.t.writes)
        self.assertEqual([], self.t.workflow_calls)

    def test_graph_only_requires_separate_scoreboard_permission(self):
        self.t.set_selected_source()
        outcome = self.preflight()
        self.assertEqual("HOLD_SCOREBOARD_PERMISSION_MISSING", outcome["status"])
        self.assertEqual("PROVIDER_OWNER_ROOT_GRAPH_VERIFIED", outcome["graph_selection"])
        self.assertEqual("MISSING_SCOPED_COMMENT_REF", outcome["scoreboard_permission"])
        self.assertEqual([], self.t.workflow_calls)
        self.assertEqual([], self.t.writes)

    def test_false_scoreboard_comment_denied_before_deployment(self):
        self.t.set_selected_source()
        self.t.score_comment["user"]["login"] = "not-graph-approved"
        outcome = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("HOLD_SCOREBOARD_PERMISSION_UNVERIFIED", outcome["status"])
        self.assertEqual([], self.t.workflow_calls)
        self.assertEqual([], self.t.writes)

    def test_disabled_active_state_is_not_operational_release(self):
        self.t.set_selected_source()
        self.t.workflow_state = "disabled_manually"
        outcome = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("HOLD_DEFAULT_BRANCH_WORKFLOW_NOT_VERIFIED", outcome["status"])
        self.assertEqual("WORKFLOW_NOT_ACTIVE", outcome["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_unverified_workflow_or_missing_guard_does_not_release(self):
        self.t.set_selected_source()
        self.t.workflow_guards = False
        bad = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("WORKFLOW_GUARDS_NOT_PRESENT", bad["workflow"]["status"])
        self.t.workflow_guards = True
        self.t.workflow_path = ".github/workflows/something-else.yml"
        changed = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("WORKFLOW_IDENTITY_MISMATCH", changed["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_unreachable_workflow_api_remains_unverified_not_absent(self):
        self.t.set_selected_source()
        self.t.workflow_path = None

        def fail_api(*args):
            raise DELP.DelpError("provider outage")

        with patch.object(self.t, "_gh", side_effect=fail_api):
            outcome = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("HOLD_DEFAULT_BRANCH_WORKFLOW_NOT_VERIFIED", outcome["status"])
        self.assertEqual("WORKFLOW_PROVIDER_UNVERIFIED", outcome["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_all_machine_observations_cannot_grant_ic_or_activation(self):
        self.t.set_selected_source()
        passed = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("PREFLIGHT_GATES_OBSERVED_NOT_OPERATIONALLY_ACCEPTED", passed["status"])
        self.assertEqual("TRUSTED_DEFAULT_BRANCH_WORKFLOW_OBSERVED",
                         passed["workflow"]["status"])
        self.assertEqual("NOT_OBSERVED", passed["independent_reviewer"])
        self.assertEqual("NOT_INFERRED", passed["separate_owner_activation"])
        self.assertEqual("NONE", passed["programme_ic_credit"])
        self.assertEqual("NONE", passed["issue_pr_body_changes"])
        self.assertFalse(passed["live_status_writer_invoked"])
        self.assertEqual([], self.t.writes)

    def test_root_scoping_rejects_child_entry_before_status_check(self):
        with self.assertRaisesRegex(R7.ReleasePreflightError, "governing parent"):
            R7.assess(self.t, COLD_TESTS.LEAF_URL)
        with self.assertRaises(R7.ReleasePreflightError):
            R7._checked_workflow(self.t, "../untrusted.yml")
        self.assertEqual([], self.t.writes)

    def test_cli_hold_nonzero_and_all_machine_gates_zero_without_writes(self):
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            self.assertEqual(3, R7.main([
                "--repository", self.t.repository, "--root-url", self.root,
            ]))
        self.t.set_selected_source()
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            self.assertEqual(0, R7.main([
                "--repository", self.t.repository, "--root-url", self.root,
                "--scoreboard-approval-ref", GRAPH_TESTS.SCORE_URL,
            ]))
        self.assertEqual([], self.t.writes)


if __name__ == "__main__":
    unittest.main()
