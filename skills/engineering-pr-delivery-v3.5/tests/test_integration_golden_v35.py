from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "integration_golden_v35.py"
FIXTURE = ROOT / "examples/integration/real-common-600-604-712.golden.json"

spec = importlib.util.spec_from_file_location("integration_golden_v35", SCRIPT)
G = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(G)


class IntegrationGoldenV35ContractTests(unittest.TestCase):
    """IC1–IC8 *oracle prerequisites*; not proof of operational GitHub sync."""

    def source(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_real_historical_parent_child_pr_title_golden(self):
        data = self.source()
        rendered = G.derive(data)
        expect = data["expected"]
        self.assertEqual(expect["programme_title"], rendered["issue_titles"]["programme"])
        self.assertEqual(expect["responsibility_title"], rendered["issue_titles"]["responsibility"])
        self.assertEqual(expect["pr_title"], rendered["pr_title"])
        self.assertEqual(expect["qualification"], rendered["qualification"])
        self.assertEqual(expect["product_status"], rendered["product_status"])
        self.assertEqual("DERIVED_GOLDEN_ONLY_NOT_PRODUCTION", rendered["authority"])

    def test_owner_text_mirror_and_missing_original_link_remain_explicit(self):
        data = self.source()
        rendered = G.derive(data)
        self.assertIn(data["owner_origin"]["verbatim"], rendered["handover_prompt"])
        self.assertIn("UNRESOLVED_CHAT_LINK", rendered["handover_prompt"])
        self.assertIn("6051883834", rendered["handover_prompt"])
        self.assertIn("SOURCE_NOT_PROVEN", rendered["handover_prompt"])
        forged = copy.deepcopy(data)
        forged["owner_origin"]["original_source_status"] = "PROVEN"
        with self.assertRaisesRegex(G.GoldenContractError, "Owner"):
            G.derive(forged)
        missing = copy.deepcopy(data)
        missing["owner_origin"]["first_durable_mirror"] = "https://chatgpt.com/fake"
        with self.assertRaisesRegex(G.GoldenContractError, "Owner"):
            G.derive(missing)

    def test_ownership_mismatch_between_parent_leaf_and_pr_fails(self):
        data = self.source()
        for key, value in (
            ("parent_issue", 438),
            ("issue", 605),
        ):
            damaged = copy.deepcopy(data)
            damaged["responsibility"][key] = value
            with self.subTest(key=key), self.assertRaises(G.GoldenContractError):
                G.derive(damaged)
        damaged = copy.deepcopy(data)
        damaged["candidate_pr"]["responsibility_issue"] = 438
        with self.assertRaises(G.GoldenContractError):
            G.derive(damaged)

    def test_candidate_sha_drift_invalidates_green_checks_but_not_semantics(self):
        data = self.source()
        data["candidate_pr"]["head_sha"] = "d" * 40
        view = G.derive(data)
        self.assertEqual("CI_STALE", view["qualification"])
        self.assertIn("CI STALE", view["pr_title"])
        self.assertEqual("HOLD", view["product_status"])
        self.assertIn("CI STALE", view["handover_prompt"])
        self.assertNotIn("CI 5/5", view["pr_title"])

    def test_ci_and_agent_health_cannot_grant_progress_or_custody(self):
        data = self.source()
        view = G.derive(data)
        self.assertEqual("HOLD", view["product_status"])
        self.assertEqual("NONE", view["agent_matrix"]["semantic_progress_effect"])
        self.assertEqual("NONE", view["agent_matrix"]["custody_authority_effect"])
        self.assertEqual(0, data["programme"]["integration_acceptance"]["qualified"])
        forged = copy.deepcopy(data)
        forged["agent_observation"]["status"] = "GREEN"
        with self.assertRaises(G.GoldenContractError):
            G.derive(forged)
        forged = copy.deepcopy(data)
        forged["responsibility"]["custody_source"] = "SAFE"
        with self.assertRaises(G.GoldenContractError):
            G.derive(forged)

    def test_self_review_is_not_independent_review_or_acceptance(self):
        data = self.source()
        view = G.derive(data)
        self.assertEqual(10, len(view["review_checklist"]))
        self.assertEqual({"NOT_REVIEWED"}, {x["state"] for x in view["review_checklist"]})
        self.assertIn("SELF REVIEW: NOT_REVIEWED", view["handover_prompt"])
        self.assertIn("independent review: NOT_REVIEWED", view["handover_prompt"])
        forged = copy.deepcopy(data)
        forged["review_observation"]["independent"] = "APPROVED"
        with self.assertRaises(G.GoldenContractError):
            G.derive(forged)


if __name__ == "__main__":
    unittest.main()
