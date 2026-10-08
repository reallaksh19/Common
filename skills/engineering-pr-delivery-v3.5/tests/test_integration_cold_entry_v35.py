"""R2-D: cold issue/root/PR replay, independence and source authority negatives."""
from __future__ import annotations

import copy
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import integration_cold_entry_v35 as COLD
import integration_graph_authority_v35 as GRAPH
import test_integration_graph_authority_v35 as APPROVED


ROOT_URL = "https://github.com/reallaksh19/Common/issues/600"
LEAF_URL = "https://github.com/reallaksh19/Common/issues/604"
PR_URL = "https://github.com/reallaksh19/Common/pull/712"


class Provider(APPROVED.Provider):
    def __init__(self):
        super().__init__()
        self.issues[600]["body"] = (
            "<!-- V35_PARENT_OWNER_INTENT_BEGIN -->\n"
            "# RESPONSIBILITY KERNEL IMPLEMENTATION PROGRAMME\n"
            "Never trust mutable source as authority."
        )
        self.issues[604]["body"] = (
            "# RK-P3 — P3 custody\n"
            "Parent programme: Common #600  \n"
            "Claim: source-to-evidence validated\n"
        )
        self.pr["body"] = (
            "**Authority:** [programme #600](https://github.com/reallaksh19/Common/issues/600)"
            " → [P3 #604](https://github.com/reallaksh19/Common/issues/604)\n"
            "Human authored PR prose.\n"
        )

    def set_selected_source(self):
        self.comments[600].append({
            "id": 123456, "html_url": APPROVED.GRAPH_URL,
            "body": self.graph_comment["body"],
            "user": {"login": "reallaksh19"},
            "author_association": "OWNER",
        })


class ColdEntryTests(unittest.TestCase):
    def setUp(self):
        self.t = Provider()

    def test_three_cold_entries_agree_on_missing_approval_not_fabricated_status(self):
        records = [COLD.reconstruct(self.t, url) for url in (ROOT_URL, LEAF_URL, PR_URL)]
        self.assertEqual(records[0], records[1])
        self.assertEqual(records[1], records[2])
        for record in records:
            self.assertEqual("HOLD_NO_PROVIDER_APPROVED_GRAPH", record["status"])
            self.assertEqual("NOT_AUTHORIZED", record["event_workflow_activation"])
            self.assertEqual("NOT_DERIVED", record["programme_ic_credit"])
            self.assertEqual("SOURCE_NOT_PROVEN", record["native_custody"])
            self.assertEqual("UNKNOWN_UNTIL_APPROVED_GRAPH", record["selected_leaf"])
            self.assertEqual("OWNER_PUBLISH_APPROVED_GRAPH_SELECTION_THEN_REPLAY",
                             record["actual_next"])
        self.assertEqual([], self.t.writes)

    def test_real_github_approved_source_yields_same_basis_all_three_entries(self):
        self.t.set_selected_source()
        records = [COLD.reconstruct(self.t, url) for url in (ROOT_URL, LEAF_URL, PR_URL)]
        self.assertEqual(records[0], records[1])
        self.assertEqual(records[1], records[2])
        source = records[0]
        self.assertEqual("GOVERNED_GRAPH_PROVIDER_OBSERVED_READ_ONLY", source["status"])
        self.assertEqual(self.t.graph_digest, source["graph_digest"])
        self.assertEqual("Common#604", source["selected_leaf"])
        self.assertEqual(712, source["approved_pr"])
        self.assertEqual(self.t.sha, source["exact_head"])
        self.assertIn("basis_sha256", source)
        self.assertEqual("UNPROVEN", source["owner_original_source"])
        self.assertEqual("NOT_AUTHORIZED", source["event_workflow_activation"])
        self.assertEqual([], self.t.writes)

    def test_duplicate_active_or_malformed_approval_denied(self):
        self.t.set_selected_source()
        self.t.comments[600].append(dict(self.t.comments[600][0]))
        with self.assertRaisesRegex(COLD.ColdEntryError, "multiple graph-selection"):
            COLD.reconstruct(self.t, ROOT_URL)
        self.t.comments[600] = [{"id": 123456, "body": GRAPH.APPROVAL_START}]
        with self.assertRaisesRegex(COLD.ColdEntryError, "invalid or incomplete"):
            COLD.reconstruct(self.t, ROOT_URL)

    def test_owner_and_graph_source_change_rejected_not_readiness(self):
        self.t.set_selected_source()
        self.t.graph_comment["author_association"] = "CONTRIBUTOR"
        with self.assertRaisesRegex(COLD.ColdEntryError, "source verification"):
            COLD.reconstruct(self.t, ROOT_URL)
        self.t = Provider()
        self.t.set_selected_source()
        self.t.graph_json = self.t.graph_json.replace("RK-P3", "IMPERSONATED")
        with self.assertRaisesRegex(COLD.ColdEntryError, "source verification"):
            COLD.reconstruct(self.t, LEAF_URL)

    def test_foreign_or_ambiguous_routes_refused_before_approval(self):
        for url in (
            "https://github.com/foreign/Common/issues/600",
            "https://github.com/reallaksh19/Common/pulls/712",
            "https://github.com/reallaksh19/Common/issues/0",
        ):
            with self.subTest(url=url), self.assertRaises(COLD.ColdEntryError):
                COLD.reconstruct(self.t, url)
        wrong_child = Provider()
        wrong_child.issues[604]["body"] += "\nParent programme: Common #438\n"
        with self.assertRaisesRegex(COLD.ColdEntryError, "unique"):
            COLD.reconstruct(wrong_child, LEAF_URL)
        wrong_pr = Provider()
        wrong_pr.pr["body"] += "\n[P3 #438](https://github.com/reallaksh19/Common/issues/438)"
        with self.assertRaisesRegex(COLD.ColdEntryError, "unique"):
            COLD.reconstruct(wrong_pr, PR_URL)

    def test_selected_graph_must_match_leaf_or_pr_entry_not_just_root(self):
        self.t.set_selected_source()
        self.t.issues[604]["body"] = "Parent programme: Common #600\n"
        good = COLD.reconstruct(self.t, LEAF_URL)
        self.assertEqual("Common#604", good["selected_leaf"])
        self.t.pr["body"] = "**Authority:** programme #600 and [P3 #438](x)"
        with self.assertRaisesRegex(COLD.ColdEntryError, "leaf disagrees"):
            COLD.reconstruct(self.t, PR_URL)

    def test_no_root_marker_or_foreign_pr_base_is_not_authority(self):
        self.t.issues[600]["body"] = "# generic other issue"
        with self.assertRaises(COLD.ColdEntryError):
            COLD.reconstruct(self.t, ROOT_URL)
        self.t = Provider()
        self.t.pr["base"]["repo"]["full_name"] = "foreign/repo"
        with self.assertRaises(COLD.ColdEntryError):
            COLD.reconstruct(self.t, PR_URL)

    def test_cold_entry_cli_fail_closed_on_real_missing_approval(self):
        import integration_scoreboard_publish_v35 as SCOREBOARD
        with patch.object(SCOREBOARD, "ScoreboardTransport", return_value=self.t):
            self.assertEqual(3, COLD.main([
                "--repository", self.t.repository,
                "--entry-url", ROOT_URL,
            ]))
        self.assertEqual([], self.t.writes)
        self.t.set_selected_source()
        with patch.object(SCOREBOARD, "ScoreboardTransport", return_value=self.t):
            self.assertEqual(0, COLD.main([
                "--repository", self.t.repository,
                "--entry-url", PR_URL,
            ]))
        self.assertEqual([], self.t.writes)

    def test_no_native_custody_grant_from_owner_graph_even_when_green(self):
        self.t.set_selected_source()
        value = COLD.reconstruct(self.t, PR_URL)
        self.assertEqual("SOURCE_NOT_PROVEN", value["native_custody"])
        self.assertEqual("NOT_DERIVED", value["local_merge_authority"])
        self.assertEqual("NOT_DERIVED", value["programme_ic_credit"])
        self.assertTrue(value["provider_read_only"])
        self.assertEqual([], self.t.writes)


if __name__ == "__main__":
    unittest.main()
