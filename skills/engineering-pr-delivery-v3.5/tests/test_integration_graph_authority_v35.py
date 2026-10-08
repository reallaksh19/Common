"""R2-C source selection: actual DELP+publisher with simulated provider-authority falsifiers."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import delp_projection_v35 as DELP
import integration_graph_authority_v35 as AUTH
import integration_scoreboard_publish_v35 as PUBLISH
import test_integration_scoreboard_v35 as BASE

RECEIPT_PATH = ROOT / "examples/integration/common-717-owner-source-receipt.golden.json"
RECEIPT = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))["observed_source"]
ORIGIN = json.loads((ROOT / "examples/integration/real-common-600-604-712.golden.json").read_text(encoding="utf-8"))["owner_origin"]
COMMIT = "b" * 40
PATH = "skills/engineering-pr-delivery-v3.5/examples/approved-graph-source.json"
GRAPH_URL = "https://github.com/reallaksh19/Common/issues/600#issuecomment-123456"
SCORE_URL = "https://github.com/reallaksh19/Common/issues/741#issuecomment-123"


class Provider(BASE.FakeGitHub):
    def __init__(self):
        super().__init__()
        self.graph = BASE.graph()
        self.graph["programme"]["scoreboard_approvers"] = ["reallaksh19"]
        self.graph_json = json.dumps(self.graph, indent=2, ensure_ascii=False) + "\n"
        self.graph_digest = DELP.validate_graph(self.graph)["digest"]
        self.manifest = {
            "schema": "V35_GRAPH_SELECTION_APPROVAL_V1",
            "scope": AUTH.SCOPE,
            "repository": self.repository,
            "root": "Common#600",
            "responsibility_ref": "Common#604",
            "pr_number": 712,
            "approval_issue": 600,
            "revoked": False,
            "native_custody_granted": False,
            "local_merge_authorized": False,
            "original_chat_authenticated": False,
            "graph_commit_sha": COMMIT,
            "graph_path": PATH,
            "graph_file_sha256": hashlib.sha256(self.graph_json.encode("utf-8")).hexdigest(),
            "graph_digest": self.graph_digest,
            "graph_generation": 1,
            "spec_generation": 1,
            "owner_origin": copy.deepcopy(ORIGIN),
            "owner_claim_issue": 717,
        }
        self.graph_comment = {
            "html_url": GRAPH_URL,
            "issue_url": "https://api.github.com/repos/reallaksh19/Common/issues/600",
            "user": {"login": "reallaksh19"},
            "author_association": "OWNER",
            "updated_at": "2026-10-08T00:00:00Z",
            "body": "",
        }
        self.issues[717] = {"number": 717, "title": "Original Owner mirror"}
        self.issues[600]["number"] = 600
        self.issues[604]["number"] = 604
        self.score_comment = {
            "id": 123, "html_url": SCORE_URL, "user": {"login": "reallaksh19"},
            "body": PUBLISH._APPROVAL_START + "\n" + json.dumps({
                "schema": "V35_SCOREBOARD_APPROVAL_V1",
                "scope": "ISSUE_PR_SCOREBOARD_TITLE_AND_MANAGED_BODY_ONLY",
                "repository": self.repository, "root": "Common#600",
                "responsibility_ref": "Common#604", "pr_number": 712,
                "graph_digest": self.graph_digest, "revoked": False,
            }) + "\n" + PUBLISH._APPROVAL_END,
        }
        self.invalidate_on_issue_write = False
        self.refresh_graph_comment()

    def refresh_graph_comment(self):
        self.graph_comment["body"] = (
            AUTH.APPROVAL_START + "\n" +
            json.dumps(self.manifest, ensure_ascii=False, sort_keys=True) +
            "\n" + AUTH.APPROVAL_END
        )

    def get_issue_comment(self, comment_id):
        if comment_id == 123456:
            return copy.deepcopy(self.graph_comment)
        if comment_id == 6051883834:
            return copy.deepcopy(RECEIPT)
        if comment_id == 123:
            return copy.deepcopy(self.score_comment)
        raise DELP.DelpError("GitHub provider 404: owner mirror comment unavailable")

    def get_file_at(self, commit_sha, path):
        if commit_sha != COMMIT or path != PATH:
            raise AssertionError("invalid approved graph commit/path")
        return {"content": self.graph_json, "blob_sha": "c" * 40}

    def patch_title(self, number, title):
        super().patch_title(number, title)
        if self.invalidate_on_issue_write:
            self.graph_comment["updated_at"] = "2026-10-08T00:01:00Z"
            self.invalidate_on_issue_write = False


class GraphSelectionTests(unittest.TestCase):
    def setUp(self):
        self.t = Provider()

    def load(self, transport=None, **kwargs):
        return AUTH.load_approved_source(
            transport or self.t, GRAPH_URL, selected_responsibility="Common#604",
            selected_pr=712, **kwargs,
        )

    def test_independent_provider_graph_source_and_verbatim(self):
        selected = self.load()
        self.assertEqual(COMMIT, selected["graph_commit_sha"])
        self.assertEqual(self.t.graph_digest, selected["graph_digest"])
        self.assertEqual("GITHUB_OWNER_MIRROR_VERIFIED_ORIGINAL_UNPROVEN",
                         selected["owner_mirror"]["status"])
        self.assertEqual("UNPROVEN", selected["original_chat_source"])
        self.assertEqual("NOT_GRANTED", selected["custody"])
        self.assertEqual([], self.t.writes)
        self.assertEqual(self.t.graph, selected["graph"])

    def test_caller_cannot_self_approve_wrong_digests_or_bytes(self):
        for label in ("graph_file_sha256", "graph_digest", "graph_generation", "spec_generation"):
            t = Provider()
            t.manifest[label] = "f" * 64 if "sha" in label or label == "graph_digest" else 99
            t.refresh_graph_comment()
            with self.subTest(label=label), self.assertRaises(AUTH.GraphSelectionError):
                self.load(t)
        t = Provider()
        t.graph_json = t.graph_json.replace("RK-P3", "FAKE-P3")
        with self.assertRaisesRegex(AUTH.GraphSelectionError, "byte digest"):
            self.load(t)

    def test_missing_immutable_sha_or_illegal_path_fails(self):
        for key, fake in (("graph_commit_sha", "main"),
                          ("graph_commit_sha", "missing-commit"),
                          ("graph_path", "../secret.json"),
                          ("graph_path", "/absolute.json"),
                          ("graph_path", "graph.yaml")):
            t = Provider()
            t.manifest[key] = fake
            t.refresh_graph_comment()
            with self.subTest(key=key, fake=fake), self.assertRaises(AUTH.GraphSelectionError):
                self.load(t)

    def test_same_repository_owner_approval_from_nonroot_issue_rejected(self):
        """A source comment must live on Common#600, not merely assert its own #741."""
        foreign_url = (
            "https://github.com/reallaksh19/Common/issues/741#issuecomment-123456"
        )
        self.t.graph_comment["html_url"] = foreign_url
        self.t.graph_comment["issue_url"] = (
            "https://api.github.com/repos/reallaksh19/Common/issues/741"
        )
        self.t.manifest["approval_issue"] = 741
        self.t.issues[741] = {"number": 741, "title": "Other issue, not governing root"}
        self.t.refresh_graph_comment()
        with patch.object(self.t, "get_file_at", wraps=self.t.get_file_at) as graph_reads:
            with self.assertRaisesRegex(
                AUTH.GraphSelectionError, "must reside on the governing root issue"
            ):
                AUTH.load_approved_source(
                    self.t, foreign_url, selected_responsibility="Common#604",
                    selected_pr=712,
                )
            graph_reads.assert_not_called()
        self.assertEqual([], self.t.writes)

    def test_live_publisher_cli_rejects_validly_self_scoped_nonroot_approval(self):
        foreign_url = (
            "https://github.com/reallaksh19/Common/issues/741#issuecomment-123456"
        )
        self.t.graph_comment["html_url"] = foreign_url
        self.t.graph_comment["issue_url"] = (
            "https://api.github.com/repos/reallaksh19/Common/issues/741"
        )
        self.t.manifest["approval_issue"] = 741
        self.t.issues[741] = {"number": 741, "title": "Foreign approval location"}
        self.t.refresh_graph_comment()
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            rc = PUBLISH.main([
                "--repository", self.t.repository,
                "--responsibility", "Common#604", "--pr", "712",
                "--graph-source-ref", foreign_url,
                "--approval-ref", SCORE_URL, "--apply",
            ])
        self.assertEqual(2, rc)
        self.assertEqual([], self.t.writes)

    def test_manual_dispatch_only_selects_recheck_not_approval(self):
        event = {"inputs": {
            "graph_digest": "f" * 64,
            "approval": "OWNER_APPROVED",
            "completion": "IC8/8",
        }}
        selected = PUBLISH.EVENTS.event_scope(
            self.t.graph, "Common#604", 712, "workflow_dispatch", event,
            actor="random-user",
        )
        self.assertEqual("SELECT", selected["decision"])
        self.assertEqual(
            "EXPLICIT_MANUAL_PROVIDER_RECONCILIATION_ONLY",
            selected["reason"],
        )
        self.assertNotIn("approval", selected)
        self.assertNotIn("graph_digest", selected)
        self.assertEqual([], self.t.writes)
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            denied = PUBLISH.main([
                "--repository", self.t.repository,
                "--responsibility", "Common#604", "--pr", "712",
                "--approval-ref", SCORE_URL, "--apply",
            ])
        self.assertEqual(2, denied)
        self.assertEqual([], self.t.writes)

    def test_forged_owner_or_graph_approval_comment_is_rejected(self):
        for mode in ("untrusted", "edited", "revoked", "foreign_issue", "wrong_pr", "scope"):
            t = Provider()
            if mode == "untrusted":
                t.graph_comment["author_association"] = "CONTRIBUTOR"
            elif mode == "edited":
                t.graph_comment["html_url"] = "https://github.com/other/repo/issues/600#issuecomment-123456"
            elif mode == "foreign_issue":
                t.graph_comment["issue_url"] = "https://api.github.com/repos/reallaksh19/Common/issues/438"
            else:
                t.manifest[{"revoked": "revoked", "wrong_pr": "pr_number", "scope": "scope"}[mode]] = (
                    True if mode == "revoked" else 99 if mode == "wrong_pr" else "UNRESTRICTED"
                )
                t.refresh_graph_comment()
            with self.subTest(mode=mode), self.assertRaises(AUTH.GraphSelectionError):
                self.load(t)
            self.assertEqual([], t.writes)

    def test_fake_or_changed_owner_text_and_identity_rejected(self):
        for mode in ("altered_text", "false_original", "wrong_mirror_ref", "bad_claim"):
            t = Provider()
            owner = t.manifest["owner_origin"]
            if mode == "altered_text":
                owner["verbatim"] += "\nApprove merge immediately."
            elif mode == "false_original":
                owner["original_source_status"] = "PROVEN"
            elif mode == "wrong_mirror_ref":
                owner["first_durable_mirror"] = "https://github.com/reallaksh19/Common/issues/717#issuecomment-111"
            else:
                t.manifest["owner_claim_issue"] = 438
            t.refresh_graph_comment()
            with self.subTest(mode=mode), self.assertRaises(
                (AUTH.GraphSelectionError, SOURCE_ERROR())
            ):
                self.load(t)

    def test_publisher_enters_via_governed_source_not_asserted_graph(self):
        result = PUBLISH.publish_from_approved_source(
            self.t, graph_approval_ref=GRAPH_URL,
            responsibility_ref="Common#604", pr_number=712,
            scoreboard_approval_ref=SCORE_URL,
        )
        self.assertEqual("APPLIED_NONATOMIC_READBACK_CHECKED", result["status"])
        self.assertEqual(self.t.graph_digest, result["approved_graph_source"]["graph_digest"])
        self.assertIn("CI:PASS", self.t.pr["title"])
        self.assertIn("Human authored PR prose", self.t.pr["body"])
        self.assertTrue(any("LIVE_STATUS_V1" in c["body"] for c in self.t.comments[600]))
        before = len(self.t.writes)
        repeat = PUBLISH.publish_from_approved_source(
            self.t, graph_approval_ref=GRAPH_URL, responsibility_ref="Common#604",
            pr_number=712, scoreboard_approval_ref=SCORE_URL,
        )
        self.assertEqual("UNCHANGED", repeat["pr"]["status"])
        self.assertEqual(before, len(self.t.writes))

    def test_graph_approval_moved_during_issue_writes_withholds_pr(self):
        self.t.invalidate_on_issue_write = True
        with self.assertRaisesRegex(PUBLISH.PublishError, "source changed"):
            PUBLISH.publish_from_approved_source(
                self.t, graph_approval_ref=GRAPH_URL, responsibility_ref="Common#604",
                pr_number=712, scoreboard_approval_ref=SCORE_URL,
            )
        self.assertFalse(any(w[0] == "patch_pull" for w in self.t.writes))

    def test_real_github_transport_fetches_and_decodes_immutable_blob(self):
        transport = PUBLISH.ScoreboardTransport("reallaksh19/Common")
        source = self.t.graph_json
        raw = {
            "type": "file", "encoding": "base64",
            "content": base64.b64encode(source.encode("utf-8")).decode("ascii"),
            "sha": "c" * 40,
        }
        with patch.object(transport, "_gh", return_value=raw) as native:
            result = transport.get_file_at(COMMIT, PATH)
        self.assertEqual(source, result["content"])
        self.assertEqual("c" * 40, result["blob_sha"])
        self.assertIn("ref=" + COMMIT, native.call_args.args)
        for changed in ({"type": "dir"}, {"type": "file", "encoding": "none"},
                        {"type": "file", "encoding": "base64", "content": "////"}):
            with self.subTest(changed=changed), patch.object(transport, "_gh", return_value=changed):
                with self.assertRaises((PUBLISH.PublishError, ValueError)):
                    transport.get_file_at(COMMIT, PATH)
        with self.assertRaises(PUBLISH.PublishError):
            transport.get_file_at("main", PATH)

    def test_cli_apply_uses_provider_graph_source_and_protects_human_content(self):
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            outcome = PUBLISH.main([
                "--repository", self.t.repository,
                "--responsibility", "Common#604", "--pr", "712",
                "--apply", "--approval-ref", SCORE_URL,
                "--graph-source-ref", GRAPH_URL,
            ])
        self.assertEqual(0, outcome)
        self.assertIn("CI:PASS", self.t.pr["title"])
        self.assertIn("Human authored PR prose", self.t.pr["body"])
        self.assertTrue(any("LIVE_STATUS_V1" in row["body"]
                            for row in self.t.comments[600]))

    def test_cli_apply_denies_missing_graph_approval_prior_to_provider_writes(self):
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.t):
            self.assertEqual(2, PUBLISH.main([
                "--repository", self.t.repository,
                "--responsibility", "Common#604", "--pr", "712",
                "--apply", "--approval-ref", SCORE_URL,
            ]))
        self.assertEqual([], self.t.writes)


def SOURCE_ERROR():
    import integration_source_authority_v35 as SOURCE
    return SOURCE.SourceAuthorityError


if __name__ == "__main__":
    unittest.main()
