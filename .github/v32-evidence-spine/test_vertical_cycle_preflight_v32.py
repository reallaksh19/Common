"""Retained first-slice preflight: named discovery, real DELP/R-PROOF invocation, falsifiers.

This is deliberately NOT a full vertical-cycle success claim.  Full mode
must fail closed until R-PROJECTION and downstream consumers actually exist.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vertical_cycle_preflight_v32 as preflight  # noqa: E402


class GoldenContractPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.graph = preflight.load()

    def test_01_precommitted_owner_or_claim_fixture_contract(self):
        result = preflight.validate_contract(self.manifest, self.graph)
        self.assertEqual(12, result["fixture_count"])
        self.assertEqual(7, result["OR_count"])
        self.assertEqual(35, result["root_reserve"])
        self.assertTrue(result["release_digest"].startswith("sha256:"))

    def test_02_source_legacy_merge_no_facts_is_not_progress(self):
        result = preflight.evaluate_source(self.manifest, self.graph)
        self.assertEqual("OBSERVATION_ONLY", result["authority"])
        self.assertNotEqual("COMPLETE", result["programme_state"])
        for issue in ("Common#720", "Common#724"):
            self.assertNotEqual("COMPLETE", result["legacy_leaf_states"][issue])
            self.assertEqual(0, result["legacy_P_E"][issue]["P"])
            self.assertEqual(0, result["legacy_P_E"][issue]["E"])

    def test_03_real_qualification_source_does_not_accept_undiscovered_test(self):
        result = preflight.evaluate_source(self.manifest, self.graph)
        self.assertNotEqual("PROVEN", result["unexecuted_test_overall"])

    def test_04_tampering_source_and_binding_is_caught(self):
        variants = preflight.stress_mutations(self.manifest, self.graph)
        self.assertEqual(9, len(variants))
        self.assertTrue(all(x["outcome"] == "EXPECTED_REJECTION" for x in variants.values()))

    def test_05_full_chain_reports_unimplemented_not_success(self):
        report = preflight.run("full")
        self.assertEqual(2, report["exit_code"])
        self.assertEqual("FAIL_CLOSED_UNIMPLEMENTED_CONSUMERS", report["full_integrated_gate"])
        self.assertIn("NOT_IMPLEMENTED", report["consumer_results"]["HANDOVER_PROMPT"])
        self.assertIn("NOT_IMPLEMENTED", report["consumer_results"]["AGENT_MATRIX"])

    def test_06_fixture_expected_views_not_promoted_to_automatic_writer(self):
        report = preflight.run("preflight")
        views = self.manifest["frozen_expected_current_views"]
        self.assertEqual("MANUAL_CURRENT_OBSERVATION_NOT_IMPLEMENTED", views["title_producer"])
        self.assertEqual("MANUAL_OBSERVED_ONLY", report["consumer_results"]["PARENT_TITLE"])
        self.assertEqual("NO_PRODUCT_PR_AND_RENDERER_NOT_IMPLEMENTED", report["consumer_results"]["PR_TITLE"])

    def test_07_negative_owner_original_link_status_not_fabricated(self):
        damaged = copy.deepcopy(self.manifest)
        damaged["owner_intents"][0]["original_source_ref"] = None
        damaged["owner_intents"][0].pop("original_source_status")
        with self.assertRaisesRegex(preflight.ContractError, "UNPROVEN_ORIGIN_NOT_DISCLOSED"):
            preflight.validate_contract(damaged, self.graph)

    def test_08_false_all_consumer_pass_is_rejected(self):
        damaged = copy.deepcopy(self.manifest)
        damaged["frozen_expected_current_views"]["full_integrated_replay"] = "PASS"
        with self.assertRaisesRegex(preflight.ContractError, "PREMATURE_FULL_PASS"):
            preflight.validate_contract(damaged, self.graph)

    def test_09_no_product_candidate_for_child(self):
        entry = next(
            r for r in self.manifest["observed_historical_material"]
            if r["responsibility"] == "R-PROJECTION"
        )
        self.assertIsNone(entry["head_sha"])
        self.assertIsNone(entry["pr"])
        self.assertEqual("UNREPORTED", entry["checkpoint_facts"])
        self.assertIsNone(next(
            r for r in self.graph["nodes"]
            if r.get("responsibility_id") == "R-PROJECTION"
        ).get("primary_pr"))

    def test_10_exact_fixture_and_source_graph_are_immutably_indexed(self):
        rows = {r["id"]: r for r in self.manifest["fixtures"]}
        self.assertEqual(12, len(rows))
        self.assertIn("GF-COLD-AGENT", rows)
        self.assertIn("GF-AGENT-PROVENANCE", rows)
        self.assertIn("GF-PUBLISH-RACE", rows)
        self.assertEqual(
            set(self.manifest["required_stage_outputs"]),
            set(preflight.REQUIRED),
        )


if __name__ == "__main__":
    unittest.main()
