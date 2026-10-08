"""R2-B source-level falsifiers for claimed Owner provenance and provider currentness."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import delp_projection_v35 as DELP
import integration_source_authority_v35 as SOURCE

FIXTURE = ROOT / "examples/integration/real-common-600-604-712.golden.json"
OWNER = json.loads(FIXTURE.read_text(encoding="utf-8"))["owner_origin"]


def graph():
    return {
        "schema": DELP.GRAPH_SCHEMA,
        "programme": {
            "id": "SOURCE-TEST", "root": "Common#600",
            "repository": "reallaksh19/Common", "graph_generation": 2
        },
        "nodes": [
            {"ref": "Common#600", "kind": "ROOT"},
            {"ref": "Common#604", "kind": "LEAF", "parent": "Common#600",
             "weight": 1, "responsibility_id": "RK-P3", "spec_generation": 2,
             "primary_pr": "Common#712",
             "units": [{"id": "U01", "weight": 100}]},
        ],
    }


class SourceProvider:
    repository = "reallaksh19/Common"

    def __init__(self):
        self.head = "a" * 40
        self.move_head_after_read = False
        self.calls = []
        self.comment = {
            "id": 6051883834,
            "html_url": OWNER["first_durable_mirror"],
            "issue_url": "https://api.github.com/repos/reallaksh19/Common/issues/717",
            "author_association": "OWNER",
            "user": {"login": "reallaksh19"},
            "updated_at": "2026-10-08T03:58:15Z",
            "body": ("OWNER_INTENT_SOURCE_RECEIPT_V1\n\n"
                     "**Verbatim Owner utterance (first durable copy):**\n\n"
                     + "\n".join("> " + line if line else ">"
                                 for line in OWNER["verbatim"].split("\n")) +
                     "\n\n**Original source:** UNAVAILABLE"),
        }
        self.issue = {"number": 717, "title": "Owner claim issue"}
        self.pull = {
            "number": 712, "state": "open", "draft": True,
            "base": {"repo": {"full_name": self.repository}},
            "head": {"sha": self.head},
        }
        self.writes = []

    def get_issue_comment(self, comment_id):
        self.calls.append(("comment", comment_id))
        return copy.deepcopy(self.comment)

    def get_issue(self, issue_number):
        self.calls.append(("issue", issue_number))
        return copy.deepcopy(self.issue)

    def get_commit_sha(self, ref):
        return "9" * 40

    def get_pull(self, number):
        self.calls.append(("pull", number))
        self.pull["head"]["sha"] = self.head
        ret = copy.deepcopy(self.pull)
        if self.move_head_after_read and self.calls.count(("pull", number)) >= 2:
            self.head = "b" * 40
        return ret

    def list_comments(self, number):
        return []

    def patch_title(self, *args):
        self.writes.append(args)
        raise AssertionError("source preflight must never modify GitHub")


class VerifiedSourcePreflight(unittest.TestCase):
    def setUp(self):
        self.g = graph()
        self.digest = DELP.validate_graph(self.g)["digest"]
        self.transport = SourceProvider()

    def run_preflight(self, **kwargs):
        args = dict(
            transport=self.transport, graph=self.g,
            responsibility_ref="Common#604", pr_number=712,
            owner_origin=OWNER, claim_issue=717,
            independently_pinned_graph_digest=self.digest,
        )
        args.update(kwargs)
        return SOURCE.assess(**args)

    def test_mirror_verified_but_original_source_and_custody_not_promoted(self):
        record = self.run_preflight()
        self.assertEqual("PARTIAL_PROVIDER_PROVENANCE_NOT_RELEASED", record["result"])
        self.assertEqual(
            "GITHUB_OWNER_MIRROR_VERIFIED_ORIGINAL_UNPROVEN", record["owner_mirror"]["status"]
        )
        self.assertEqual("UNPROVEN", record["original_owner_source"])
        self.assertEqual("NOT_PROVEN", record["native_custody"])
        self.assertEqual("NONE", record["acceptance_credit"])
        self.assertEqual("NONE", record["delivery_permission"])
        self.assertEqual("a" * 40, record["provider_candidate_head"])
        self.assertEqual(self.digest, record["graph_digest"])
        self.assertEqual("RK-P3", record["responsibility_id"])
        self.assertEqual([], self.transport.writes)
        self.assertIn(("comment", 6051883834), self.transport.calls)
        self.assertIn(("issue", 717), self.transport.calls)
        self.assertIn(("pull", 712), self.transport.calls)

    def test_quote_change_preserving_first_phrase_is_rejected(self):
        tampered = dict(OWNER)
        tampered["verbatim"] = OWNER["verbatim"] + "\nOwner grants native custody."
        with self.assertRaisesRegex(SOURCE.SourceAuthorityError, "full Owner quotation"):
            self.run_preflight(owner_origin=tampered)

    def test_source_mirror_edited_after_record_is_rejected(self):
        self.transport.comment["body"] = self.transport.comment["body"].replace(
            "reviewer checklist", "delete reviewer checklist"
        )
        with self.assertRaisesRegex(SOURCE.SourceAuthorityError, "full Owner quotation"):
            self.run_preflight()

    def test_wrong_mirror_issue_url_author_or_association_refused(self):
        cases = (
            ("wrong_html_url", "html_url", "https://github.com/reallaksh19/Common/issues/717#issuecomment-1"),
            ("foreign_issue", "issue_url", "https://api.github.com/repos/reallaksh19/Common/issues/438"),
            ("untrusted", "author_association", "CONTRIBUTOR"),
        )
        for label, field, invalid in cases:
            with self.subTest(label=label):
                transport = SourceProvider()
                transport.comment[field] = invalid
                with self.assertRaises(SOURCE.SourceAuthorityError):
                    self.run_preflight(transport=transport)
        transport = SourceProvider()
        transport.comment["user"]["login"] = ""
        with self.assertRaises(SOURCE.SourceAuthorityError):
            self.run_preflight(transport=transport)

    def test_foreign_repository_and_wrong_child_or_pr_refused(self):
        other = graph()
        other["programme"]["repository"] = "other/Common"
        with self.assertRaises(DELP.DelpError):
            self.run_preflight(graph=other)
        with self.assertRaises(SOURCE.SourceAuthorityError):
            self.run_preflight(responsibility_ref="Common#438")
        with self.assertRaises(SOURCE.SourceAuthorityError):
            self.run_preflight(pr_number=737)
        foreign = SourceProvider()
        foreign.pull["base"]["repo"]["full_name"] = "other/Common"
        with self.assertRaises(SOURCE.SourceAuthorityError):
            self.run_preflight(transport=foreign)

    def test_stale_graph_digest_and_unknown_original_receipt_fail_closed(self):
        with self.assertRaisesRegex(SOURCE.SourceAuthorityError, "graph digest"):
            self.run_preflight(independently_pinned_graph_digest="a" * 64)
        unsupported = dict(OWNER)
        unsupported["original_source_ref"] = "https://fake.invalid/original"
        unsupported["original_source_status"] = "PROVEN"
        with self.assertRaisesRegex(SOURCE.SourceAuthorityError, "unverified original"):
            self.run_preflight(owner_origin=unsupported)
        with self.assertRaisesRegex(SOURCE.SourceAuthorityError, "owner source envelope"):
            self.run_preflight(owner_origin=None)

    def test_unchanged_source_has_stable_basis_digest(self):
        first = self.run_preflight()
        second = self.run_preflight()
        self.assertEqual(first["basis_digest"], second["basis_digest"])
        self.transport.head = "b" * 40
        changed = self.run_preflight()
        self.assertNotEqual(first["basis_digest"], changed["basis_digest"])
        self.assertEqual("NONE", changed["acceptance_credit"])

    def test_provider_head_moves_mid_reconciliation(self):
        # First PR read is SHA A, observation in DELP may see A, last read sees B.
        transport = SourceProvider()
        transport.move_head_after_read = True
        with self.assertRaisesRegex(SOURCE.SourceAuthorityError, "head changed"):
            self.run_preflight(transport=transport)
        self.assertEqual([], transport.writes)


if __name__ == "__main__":
    unittest.main()
