"""Source-level R3/R4 falsifiers, exercising DELP publisher and real fact ingestion."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import delp_projection_v35 as M
import integration_read_model_v35 as R2
import integration_scoreboard_v35 as R3
import integration_scoreboard_publish_v35 as R4


def graph():
    return {
        "schema": M.GRAPH_SCHEMA,
        "programme": {
            "id": "SMART-LIVE-V35-TEST", "root": "Common#600",
            "repository": "reallaksh19/Common", "graph_generation": 1,
            "scoreboard_approvers": ["owner"],
        },
        "nodes": [
            {"ref": "Common#600", "kind": "ROOT"},
            {
                "ref": "Common#604", "kind": "LEAF", "parent": "Common#600",
                "weight": 1, "responsibility_id": "RK-P3", "spec_generation": 1,
                "primary_pr": "Common#712",
                "units": [{"id": "U01", "weight": 100}],
            },
        ],
    }


class FakeGitHub:
    """Provider with separately mutable issue status/title, PR, checks and facts."""
    repository = "reallaksh19/Common"

    def __init__(self):
        self.sha = "a" * 40
        self.issues = {600: {"title": "My parent programme"},
                       604: {"title": "My child responsibility"}}
        self.comments = {600: [], 604: []}
        self.pr = {"number": 712, "title": "Project candidate PR",
                   "body": "Human authored PR prose.\n\n## Important review context\nPreserve.",
                   "head": {"sha": self.sha}, "state": "open", "draft": True,
                   "merged": False,
                   "base": {"repo": {"full_name": self.repository}}}
        self.checks = {"total_count": 2, "check_runs": [
            {"name": "delp", "status": "completed", "conclusion": "success", "head_sha": self.sha},
            {"name": "Local", "status": "completed", "conclusion": "success", "head_sha": self.sha},
        ]}
        self.writes = []
        self.next_comment_id = 30000
        self.approval_comment = None
        self.move_during_issue_write = False
        self.pr_conflict_once = False

    def get_issue(self, number):
        return copy.deepcopy(self.issues[number])

    def list_comments(self, number):
        return copy.deepcopy(self.comments[number])

    def get_commit_sha(self, ref):
        return "9" * 40

    def get_pull(self, number):
        assert number == 712
        if self.pr_conflict_once:
            self.pr_conflict_once = False
            self.pr["body"] += "\nConcurrent human author edit"
        return copy.deepcopy(self.pr)

    def get_check_runs(self, head_sha):
        return copy.deepcopy(self.checks)

    def get_issue_comment(self, comment_id):
        assert comment_id == 123
        if self.approval_comment is None:
            raise AssertionError("approval not seeded")
        return copy.deepcopy(self.approval_comment)

    def patch_pull(self, number, *, title, body):
        assert number == 712
        self.writes.append(("patch_pull", number))
        self.pr["title"] = title
        self.pr["body"] = body
        return copy.deepcopy(self.pr)

    def patch_title(self, number, title):
        self.writes.append(("patch_title", number))
        self.issues[number]["title"] = title
        if self.move_during_issue_write:
            self.move_during_issue_write = False
            self.sha = "b" * 40
            self.pr["head"]["sha"] = self.sha

    def post_comment(self, number, body):
        self.next_comment_id += 1
        self.writes.append(("post_comment", number))
        record = {"id": self.next_comment_id, "body": body,
                  "user": {"login": "owner"}, "author_association": "OWNER"}
        self.comments[number].append(record)
        return copy.deepcopy(record)

    def patch_comment(self, comment_id, body):
        self.writes.append(("patch_comment", comment_id))
        for comments in self.comments.values():
            for row in comments:
                if row["id"] == comment_id:
                    row["body"] = body
                    return copy.deepcopy(row)
        raise AssertionError("unknown comment")


class PureSmartTitles(unittest.TestCase):
    def setUp(self):
        self.provider = FakeGitHub()
        self.model = R2.from_provider(
            graph(), "Common#604", self.provider,
            human_titles={"Common#600": "My parent programme",
                          "Common#604": "My child responsibility"})

    def test_scope_and_provider_checked_pr_title(self):
        view = R3.render(self.model, self.provider.pr, self.provider.checks)
        self.assertIn("P0/E0", view["pr_title"])
        self.assertIn("CI:PASS@aaaaaaa", view["pr_title"])
        self.assertIn("DRAFT", view["pr_title"])
        self.assertIn("My parent programme", view["issue_titles"]["parent_issue"])
        self.assertIn("My child responsibility", view["issue_titles"]["child_issue"])
        self.assertEqual("PASS", view["checks"]["status"])
        self.assertIn("NOT VERIFIED BY THIS WRITER", view["pr_managed_body"])
        self.assertNotIn("IC 8/8", view["pr_title"])

    def test_managed_body_preserves_original_and_is_idempotent(self):
        original = "Human prose\n\n<!-- OTHER_MANAGED_START -->\nLeave me\n<!-- OTHER_MANAGED_END -->\n"
        first = R3.managed_body(original, "status A")
        second = R3.managed_body(first, "status B")
        self.assertEqual(second, R3.managed_body(second, "status B"))
        self.assertIn("Human prose", second)
        self.assertIn("Leave me", second)
        self.assertEqual(1, second.count(R3.START))
        self.assertNotIn("status A", second)
        self.assertIn("status B", second)

    def test_duplicate_and_broken_marker_rejected(self):
        for payload in (R3.START + " dangling",
                        R3.START + R3.END + R3.START + R3.END,
                        R3.END):
            with self.subTest(payload=payload), self.assertRaises(R3.ScoreboardError):
                R3.managed_body(payload, "generated")

    def test_pr_head_mismatch_refused_even_if_ci_green(self):
        changed = copy.deepcopy(self.provider.pr)
        changed["head"]["sha"] = "b" * 40
        with self.assertRaisesRegex(R3.ScoreboardError, "head changed"):
            R3.render(self.model, changed, self.provider.checks)

    def test_provider_check_verdict_distinguishes_failure_pending_missing_stale(self):
        case = copy.deepcopy(self.provider.checks)
        case["check_runs"][1]["conclusion"] = "failure"
        self.assertEqual("FAIL", R3.render(self.model, self.provider.pr, case)["checks"]["status"])
        case["check_runs"][1]["conclusion"] = None
        case["check_runs"][1]["status"] = "in_progress"
        self.assertEqual("PENDING", R3.render(self.model, self.provider.pr, case)["checks"]["status"])
        case["check_runs"][1]["head_sha"] = "b" * 40
        self.assertEqual("STALE", R3.render(self.model, self.provider.pr, case)["checks"]["status"])
        case["total_count"] = 4
        self.assertEqual("UNKNOWN", R3.render(self.model, self.provider.pr, case)["checks"]["status"])
        self.assertEqual("UNKNOWN", R3.render(self.model, self.provider.pr, {})["checks"]["status"])

    def test_duplicate_title_prefix_is_stripped_only_if_owned(self):
        first = R3.render(self.model, self.provider.pr, self.provider.checks)
        later = copy.deepcopy(self.provider.pr)
        later["title"] = first["pr_title"]
        again = R3.render(self.model, later, self.provider.checks)
        self.assertEqual(first["pr_title"], again["pr_title"])
        later["title"] = "[Other manual prefix] Human protected title"
        manual = R3.render(self.model, later, self.provider.checks)
        self.assertIn("[Other manual prefix]", manual["pr_title"])

    def test_no_fixture_or_foreign_pr_admitted(self):
        forged = dict(self.model)
        forged["mode"] = "OFFLINE_HISTORICAL_GOLDEN_NOT_LIVE"
        with self.assertRaises(R3.ScoreboardError):
            R3.render(forged, self.provider.pr, self.provider.checks)
        foreign = copy.deepcopy(self.provider.pr)
        foreign["base"]["repo"]["full_name"] = "other/repo"
        with self.assertRaises(R3.ScoreboardError):
            R3.render(self.model, foreign, self.provider.checks)


class LivePublisherTests(unittest.TestCase):
    def setUp(self):
        self.transport = FakeGitHub()
        self.graph = graph()
        self.digest = M.validate_graph(self.graph)["digest"]
        self.source = "https://github.com/reallaksh19/Common/issues/741#issuecomment-123"
        self.transport.approval_comment = {
            "id": 123, "html_url": self.source, "user": {"login": "owner"},
            "body": (R4._APPROVAL_START + "\n" + json.dumps({
                "schema": "V35_SCOREBOARD_APPROVAL_V1",
                "scope": "ISSUE_PR_SCOREBOARD_TITLE_AND_MANAGED_BODY_ONLY",
                "repository": "reallaksh19/Common",
                "root": "Common#600",
                "responsibility_ref": "Common#604",
                "pr_number": 712,
                "graph_digest": self.digest,
                "revoked": False,
            }) + "\n" + R4._APPROVAL_END),
        }

    def apply(self):
        return R4.publish(
            self.transport, self.graph, "Common#604", 712,
            expected_graph_digest=self.digest, approval_ref=self.source,
        )

    def test_readonly_plan_never_writes_and_is_source_derived(self):
        preview = R4.plan(self.transport, self.graph, "Common#604", 712)
        self.assertEqual("DRY_RUN_NO_MUTATION", preview["status"])
        self.assertIn("CI:PASS", preview["pr_title"])
        self.assertTrue(preview["pr_body_would_change"])
        self.assertEqual([], self.transport.writes)

    def test_no_approval_no_apply(self):
        with self.assertRaisesRegex(R4.PublishError, "graph digest"):
            R4.publish(self.transport, self.graph, "Common#604", 712)
        with self.assertRaisesRegex(R4.PublishError, "approval"):
            R4.publish(self.transport, self.graph, "Common#604", 712,
                       expected_graph_digest=self.digest, approval_ref="not a provider ref")
        self.assertEqual([], self.transport.writes)

    def test_approval_provider_forgery_and_revocation_block_all_writes(self):
        for mutation in ("untrusted_author", "revoked", "wrong_graph", "different_scope", "missing_block"):
            transport = FakeGitHub()
            transport.approval_comment = copy.deepcopy(self.transport.approval_comment)
            if mutation == "untrusted_author":
                transport.approval_comment["user"]["login"] = "other-account"
            elif mutation == "missing_block":
                transport.approval_comment["body"] = "I approve it"
            else:
                raw = transport.approval_comment["body"]
                payload = json.loads(raw.split(R4._APPROVAL_START, 1)[1].split(R4._APPROVAL_END, 1)[0])
                if mutation == "revoked":
                    payload["revoked"] = True
                elif mutation == "wrong_graph":
                    payload["graph_digest"] = "z" * 64
                else:
                    payload["scope"] = "UNRESTRICTED"
                transport.approval_comment["body"] = (
                    R4._APPROVAL_START + "\n" + json.dumps(payload) + "\n" + R4._APPROVAL_END
                )
            with self.subTest(mutation=mutation), self.assertRaises(R4.PublishError):
                R4.publish(
                    transport, self.graph, "Common#604", 712,
                    expected_graph_digest=self.digest, approval_ref=self.source,
                )
            self.assertEqual([], transport.writes)

    def test_issue_status_and_smart_pr_auto_publication_then_repeat_noop(self):
        first = self.apply()
        self.assertEqual("WRITTEN_READBACK_VERIFIED", first["pr"]["status"])
        self.assertEqual("APPLIED_NONATOMIC_READBACK_CHECKED", first["status"])
        self.assertEqual(1, self.transport.pr["body"].count(R3.START))
        self.assertIn("Human authored PR prose.", self.transport.pr["body"])
        self.assertIn("## Important review context", self.transport.pr["body"])
        self.assertIn("CI:PASS@aaaaaaa", self.transport.pr["title"])
        self.assertIn("My parent programme", self.transport.issues[600]["title"])
        self.assertIn("My child responsibility", self.transport.issues[604]["title"])
        self.assertEqual(1, sum(R3.START in str(self.transport.pr["body"]) for _ in range(1)))
        self.assertTrue(any("LIVE_STATUS_V1" in c["body"] for c in self.transport.comments[600]))
        self.assertTrue(any("LIVE_STATUS_V1" in c["body"] for c in self.transport.comments[604]))
        writes = len(self.transport.writes)
        second = self.apply()
        self.assertEqual("UNCHANGED", second["pr"]["status"])
        self.assertEqual(writes, len(self.transport.writes))

    def test_candidate_moves_during_issue_sync_pr_is_withheld(self):
        self.transport.move_during_issue_write = True
        with self.assertRaisesRegex(R4.PublishError, "changed during issue sync"):
            self.apply()
        self.assertFalse(any(w[0] == "patch_pull" for w in self.transport.writes))

    def test_concurrent_human_edit_preserved_by_retry(self):
        # Simulate human PR edit while the publisher is preparing the body.
        self.transport.pr_conflict_once = True
        result = self.apply()
        self.assertEqual("WRITTEN_READBACK_VERIFIED", result["pr"]["status"])
        self.assertIn("Concurrent human author edit", self.transport.pr["body"])

    def test_foreign_pr_and_repo_refused_before_write(self):
        with self.assertRaises(R4.PublishError):
            R4.publish(self.transport, self.graph, "Common#604", 738,
                       expected_graph_digest=self.digest, approval_ref=self.source)
        wrong = graph()
        wrong["programme"]["repository"] = "other/repo"
        with self.assertRaises(M.DelpError):
            R4.publish(self.transport, wrong, "Common#604", 712,
                       expected_graph_digest=self.digest, approval_ref=self.source)
        self.assertEqual([], self.transport.writes)


if __name__ == "__main__":
    unittest.main()
