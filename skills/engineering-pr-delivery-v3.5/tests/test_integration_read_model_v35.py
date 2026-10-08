"""R2 read-model tests: use the actual DELP module, not historical golden derive()."""
from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import delp_projection_v35 as M
import integration_read_model_v35 as R


def graph():
    return {
        "schema": M.GRAPH_SCHEMA,
        "programme": {
            "id": "R2-REAL-ENGINE-ADAPTER",
            "root": "Common#600",
            "repository": "reallaksh19/Common",
            "graph_generation": 1,
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


def fact(g):
    return M.bind_facts_to_graph(g, {
        "schema": M.FACTS_SCHEMA,
        "responsibility": {"issue": "Common#604"},
        "material": {"pr": "Common#712", "candidate_sha": "a" * 40},
        "units": [{"id": "U01", "state": "COMPLETE", "result": "VERIFIED",
                   "evidence_refs": ["Common#604#issuecomment-123"]}],
    })


class FakeReadOnlyProvider:
    repository = "reallaksh19/Common"

    def __init__(self, candidate="a" * 40, comments=()):
        self.candidate = candidate
        self.comments = list(comments)
        self.reads = []
        self.writes = []

    def get_commit_sha(self, ref):
        self.reads.append(("get_commit_sha", ref))
        return "9" * 40

    def get_pull(self, number):
        self.reads.append(("get_pull", number))
        return {"head": {"sha": self.candidate}, "state": "open", "merged": False}

    def list_comments(self, number):
        self.reads.append(("list_comments", number))
        return list(self.comments)

    def patch_title(self, *args):
        self.writes.append(args)
        raise AssertionError("read-only R2 must not publish")


class DELPSourceReadModelTests(unittest.TestCase):
    def test_real_project_and_evidence_change_all_views_on_one_basis(self):
        g = graph()
        accepted = [{"source": "Common#604#issuecomment-123",
                     "order": 1, "facts": fact(g)}]
        observed = {"Common#604": {"candidate_sha": "a" * 40}}
        fresh = R.from_observations(g, "Common#604", accepted, observed)
        # This is DELP-computed P/E, not hand-authored percentages.
        self.assertEqual(100, fresh["progress"]["P"])
        self.assertEqual(100, fresh["progress"]["E"])
        self.assertEqual(["Common#604#issuecomment-123"], fresh["accepted_evidence_sources"])
        self.assertEqual(9, len(fresh["surfaces"]))
        for body in fresh["surfaces"].values():
            self.assertIn(fresh["basis_sha256"], body)
        self.assertIn(fresh["actual_next"]["action"], fresh["surfaces"]["handover_prompt"])
        stale = R.from_observations(
            g, "Common#604", accepted,
            {"Common#604": {"candidate_sha": "b" * 40}},
        )
        self.assertEqual(100, stale["progress"]["P"])
        self.assertEqual(0, stale["progress"]["E"])
        self.assertNotEqual(fresh["basis_sha256"], stale["basis_sha256"])
        self.assertNotEqual(fresh["candidate_sha"], stale["candidate_sha"])
        self.assertEqual("UNKNOWN_UNOBSERVED", stale["ci_qualification"])

    def test_foreign_fact_never_mints_progress(self):
        g = graph()
        forged = fact(g)
        forged["responsibility"]["issue"] = "Common#438"
        model = R.from_observations(
            g, "Common#604",
            [{"source": "forged", "order": 1, "facts": forged}],
            {"Common#604": {"candidate_sha": "a" * 40}},
        )
        self.assertEqual(0, model["progress"]["P"])
        self.assertTrue(model["rejected_facts"])
        self.assertEqual([], model["accepted_evidence_sources"])
        self.assertEqual("UNKNOWN_NOT_DERIVED", model["integration_acceptance"])
        self.assertEqual("NOT_PROVEN_NO_AUTHORITY", model["custody_grant"])

    def test_unknown_or_foreign_leaf_rejected(self):
        with self.assertRaises(R.ReadModelError):
            R.from_observations(graph(), "Common#438", [], {})
        wrong_repo = graph()
        wrong_repo["programme"]["repository"] = "other/repository"
        with self.assertRaises(M.DelpError):
            R.from_provider(wrong_repo, "Common#604", FakeReadOnlyProvider())

    def test_actual_provider_methods_called_without_publication(self):
        transport = FakeReadOnlyProvider()
        model = R.from_provider(graph(), "Common#604", transport)
        self.assertEqual("DELP_SOURCE_PROJECTED_READ_ONLY", model["mode"])
        self.assertEqual("a" * 40, model["candidate_sha"])
        self.assertEqual("UNKNOWN_UNOBSERVED", model["ci_qualification"])
        self.assertEqual([], transport.writes)
        self.assertIn(("get_pull", 712), transport.reads)
        self.assertIn(("list_comments", 604), transport.reads)
        self.assertIn(("get_commit_sha", "main"), transport.reads)
        self.assertIn("BASIS_SHA256:", model["surfaces"]["parent_issue"])

    def test_github_comment_fact_is_parsed_validated_and_head_bound(self):
        """Exercise ledger_from_github -> partition_ledger -> project, not hand-built counts."""
        import yaml

        frozen_graph = graph()
        comment = {
            "id": 123,
            "user": {"login": "owner"},
            "author_association": "OWNER",
            "body": ("```yaml\\n" +
                     yaml.safe_dump({"CHECKPOINT_FACTS_V1": fact(frozen_graph)},
                                    sort_keys=False) +
                     "```\\n"),
        }
        observed = FakeReadOnlyProvider(comments=[comment])
        current = R.from_provider(frozen_graph, "Common#604", observed)
        self.assertEqual((100, 100),
                         (current["progress"]["P"], current["progress"]["E"]))
        self.assertEqual(["Common#604#issuecomment-123"],
                         current["accepted_evidence_sources"])

        # A changed head does not erase the claim, but voids its E evidence.
        moved = R.from_provider(
            frozen_graph, "Common#604",
            FakeReadOnlyProvider(candidate="b" * 40, comments=[comment]))
        self.assertEqual((100, 0), (moved["progress"]["P"], moved["progress"]["E"]))
        self.assertNotEqual(current["basis_sha256"], moved["basis_sha256"])

        # A correctly shaped comment from an untrusted identity is not a fact.
        untrusted = {**comment, "author_association": "NONE"}
        unsafe = R.from_provider(
            frozen_graph, "Common#604", FakeReadOnlyProvider(comments=[untrusted]))
        self.assertEqual(0, unsafe["progress"]["P"])
        self.assertTrue(unsafe["rejected_facts"])
        self.assertEqual([], unsafe["accepted_evidence_sources"])

    def test_owner_verbatim_is_integrity_bound_but_not_authentication(self):
        owner = {
            "verbatim": "Owner direct prompt text from a supplied mirror",
            "first_durable_mirror": "https://github.com/reallaksh19/Common/issues/717#issuecomment-1",
            "original_source_status": "UNRESOLVED_CHAT_LINK",
        }
        a = R.from_observations(graph(), "Common#604", [], {}, owner_origin=owner)
        modified = {**owner, "verbatim": owner["verbatim"] + " forged sentence"}
        b = R.from_observations(graph(), "Common#604", [], {}, owner_origin=modified)
        self.assertNotEqual(a["basis_sha256"], b["basis_sha256"])
        self.assertEqual("MIRROR_UNVERIFIED_ORIGINAL", a["owner"]["authentication"])
        self.assertEqual("UNKNOWN_NOT_DERIVED", b["integration_acceptance"])
        with self.assertRaises(R.ReadModelError):
            R.from_observations(graph(), "Common#604", [], {},
                                owner_origin={**owner, "original_source_status": "PROVEN"})


if __name__ == "__main__":
    unittest.main()
