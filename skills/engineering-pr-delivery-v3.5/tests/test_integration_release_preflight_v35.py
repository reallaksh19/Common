"""R7-U2 release preflight: no source approval means HOLD, no silent deployment."""
from __future__ import annotations

import hashlib
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
        self.workflow_marker_spoof = False
        self.workflow_blob_override = None
        self.workflow_move_head = False
        self.workflow_head_reads = 0
        self.workflow_calls = []
        self.default_head = "9" * 40
        self.workflows_source = (
            ROOT / R7._AUDITED_TEMPLATE_PATH
        ).read_text(encoding="utf-8")

    def get_commit_sha(self, ref):
        if ref == "main":
            self.workflow_head_reads += 1
            if self.workflow_move_head and self.workflow_head_reads >= 2:
                return "8" * 40
            return self.default_head
        return super().get_commit_sha(ref)

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
            source = "name: insecure-event-handler\\non: workflow_dispatch\\n"
        elif self.workflow_marker_spoof:
            source = (
                "# --graph-source-ref --approval-ref --apply --event-name "
                "--event-payload github.event.repository.default_branch\\n"
                "name: TROJAN\\non: [workflow_dispatch]\\n"
                "permissions: write-all\\njobs: {unsafe: {runs-on: ubuntu-latest, "
                "steps: [{run: 'echo unsafe'}]}}\\n"
            )
        else:
            source = self.workflows_source
        content = source.encode("utf-8")
        git_sha = hashlib.sha1(
            b"blob " + str(len(content)).encode("ascii") + b"\\x00" + content
        ).hexdigest()
        return {"content": source, "blob_sha": (
            self.workflow_blob_override if self.workflow_blob_override is not None
            else git_sha
        )}


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
        self.assertEqual("WORKFLOW_NOT_AUDITED_TEMPLATE", bad["workflow"]["status"])
        self.t.workflow_guards = True
        self.t.workflow_path = ".github/workflows/something-else.yml"
        changed = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("WORKFLOW_IDENTITY_MISMATCH", changed["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_reviewed_inert_workflow_template_bytes_match_pinned_digest(self):
        data = self.t.workflows_source.encode("utf-8")
        calculated = hashlib.sha1(
            b"blob " + str(len(data)).encode("ascii") + b"\\x00" + data
        ).hexdigest()
        self.assertEqual(R7._AUDITED_WORKFLOW_BLOB_SHA, calculated)
        self.assertIn("--graph-source-ref", self.t.workflows_source)

    def test_comment_marker_spoof_does_not_pass_trusted_workflow_check(self):
        self.t.set_selected_source()
        self.t.workflow_marker_spoof = True
        result = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("HOLD_DEFAULT_BRANCH_WORKFLOW_NOT_VERIFIED", result["status"])
        self.assertEqual("WORKFLOW_NOT_AUDITED_TEMPLATE",
                         result["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_changed_permissions_or_checkout_break_audited_identity(self):
        self.t.set_selected_source()
        for edit in (
            lambda code: code.replace("issues: write", "issues: read"),
            lambda code: code.replace("ref: ${{ github.event.repository.default_branch }}",
                                      "ref: ${{ github.event.pull_request.head.sha }}"),
            lambda code: code.replace("persist-credentials: false",
                                      "persist-credentials: true"),
            lambda code: code + "\\n# --graph-source-ref --approval-ref --apply\\n",
        ):
            self.t.workflows_source = (
                ROOT / R7._AUDITED_TEMPLATE_PATH
            ).read_text(encoding="utf-8")
            self.t.workflows_source = edit(self.t.workflows_source)
            result = self.preflight(GRAPH_TESTS.SCORE_URL)
            self.assertEqual("WORKFLOW_NOT_AUDITED_TEMPLATE",
                             result["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_same_bytes_but_wrong_provider_blob_sha_rejected(self):
        self.t.set_selected_source()
        self.t.workflow_blob_override = "f" * 40
        result = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("WORKFLOW_NOT_AUDITED_TEMPLATE",
                         result["workflow"]["status"])
        self.assertEqual([], self.t.writes)

    def test_default_branch_head_drifts_during_workflow_readback(self):
        self.t.set_selected_source()
        self.t.workflow_move_head = True
        result = self.preflight(GRAPH_TESTS.SCORE_URL)
        self.assertEqual("HOLD_DEFAULT_BRANCH_WORKFLOW_NOT_VERIFIED", result["status"])
        self.assertEqual("WORKFLOW_DEFAULT_HEAD_MOVED", result["workflow"]["status"])
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
        self.assertEqual("AUDITED_TEMPLATE_BYTES_VERIFIED",
                         passed["workflow"]["workflow_source_integrity"])
        self.assertEqual(R7._AUDITED_WORKFLOW_BLOB_SHA,
                         passed["workflow"]["audited_blob_sha"])
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
