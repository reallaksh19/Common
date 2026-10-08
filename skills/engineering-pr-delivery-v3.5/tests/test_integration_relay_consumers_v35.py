"""R5 nine common consumers, real DELP cold-source and authority falsifiers."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import integration_relay_consumers_v35 as R5
import integration_cold_entry_v35 as COLD
import integration_scoreboard_publish_v35 as PUBLISH
import test_integration_cold_entry_v35 as FIXTURES

ENTRIES = (FIXTURES.ROOT_URL, FIXTURES.LEAF_URL, FIXTURES.PR_URL)


class UnifiedRelaySourceConsumers(unittest.TestCase):
    def setUp(self):
        self.provider = FIXTURES.Provider()

    def test_three_entry_without_approval_fuses_nine_same_basis_outputs(self):
        generated = [R5.from_provider(self.provider, url) for url in ENTRIES]
        self.assertEqual(generated[0], generated[1])
        self.assertEqual(generated[1], generated[2])
        result = generated[0]
        self.assertEqual("HOLD_NO_APPROVED_GRAPH", result["approval_status"])
        self.assertEqual("NO_APPROVED_GRAPH", result["source_basis"])
        self.assertEqual(set(R5.SURFACES), set(result["surfaces"]))
        for name, body in result["surfaces"].items():
            with self.subTest(name=name):
                self.assertIn(result["relay_report_sha256"], body)
                self.assertIn("DELP_SOURCE_BASIS: NO_APPROVED_GRAPH", body)
                self.assertIn("OWNER_PUBLISH_APPROVED_GRAPH_SELECTION_THEN_REPLAY", body)
                self.assertIn("SOURCE_NOT_PROVEN", body)
                self.assertIn("LIVE_SCOREBOARD: NOT_AUTHORIZED", body)
        self.assertEqual([], self.provider.writes)

    def test_approved_graph_three_entry_same_derived_consumer_views(self):
        self.provider.set_selected_source()
        outputs = [R5.from_provider(self.provider, url) for url in ENTRIES]
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[1], outputs[2])
        o = outputs[0]
        self.assertEqual("SOURCE_READ_ONLY_ACCEPTANCE_NOT_DERIVED", o["approval_status"])
        self.assertEqual("P0/E0", o["state"]["engineering"])
        self.assertEqual("NOT_DERIVED", o["state"]["programme_ic"])
        self.assertIn("EXACT_CANDIDATE: " + self.provider.sha, o["surfaces"]["draft_pr"])
        self.assertIn("NOT_PUBLISHED", o["surfaces"]["task_evidence_end"])
        self.assertEqual([], self.provider.writes)

    def test_all_nine_surfaces_are_integrity_bound_and_never_assert_test_pass(self):
        m = R5.from_provider(self.provider, FIXTURES.ROOT_URL)
        for name in R5.SURFACES:
            surface = m["surfaces"][name]
            self.assertEqual(1, surface.count("RELAY_REPORT_SHA256:"))
            self.assertIn(m["source_basis"], surface)
            self.assertNotIn("CI 5/5 PASS", surface)
        checklist = m["surfaces"]["reviewer_checklist"]
        for label in R5.COMMON_CR + R5.PROJECT_R:
            self.assertIn(label + " — UNREVIEWED", checklist)
        self.assertEqual(20, checklist.count("— UNREVIEWED"))
        self.assertIn("ADVISORY_NOT_MEASURED", m["surfaces"]["agent_metrics"])
        self.assertIn("HOSTED_TEST_RESULT: UNKNOWN", m["surfaces"]["task_evidence_end"])

    def test_refuse_inflated_principal_ic_custody_or_writes(self):
        base = COLD.reconstruct(self.provider, FIXTURES.ROOT_URL)
        for field, bad in (
            ("programme_ic_credit", "8/8"),
            ("native_custody", "AUTHORIZED"),
            ("event_workflow_activation", "LIVE"),
            ("provider_read_only", False),
        ):
            invalid = dict(base)
            invalid[field] = bad
            with self.subTest(field=field), self.assertRaises(R5.RelayConsumerError):
                R5.build(invalid)
        self.assertEqual([], self.provider.writes)

    def test_fake_approved_model_without_delp_currentness_is_rejected(self):
        base = COLD.reconstruct(self.provider, FIXTURES.ROOT_URL)
        bogus = dict(base, status="GOVERNED_GRAPH_PROVIDER_OBSERVED_READ_ONLY",
                     source_basis="f" * 64, graph_digest="e" * 64)
        with self.assertRaises(R5.RelayConsumerError):
            R5.build(bogus)

    def test_approved_inconsistent_p_e_or_candidate_rejected(self):
        self.provider.set_selected_source()
        good = COLD.reconstruct(self.provider, FIXTURES.LEAF_URL)
        for invalid in (
            dict(good, progress={"P": 5, "E": 80}),
            dict(good, exact_head="not-exact-sha"),
            dict(good, basis_sha256="not-basis"),
            dict(good, actual_next={}),
        ):
            with self.assertRaises(R5.RelayConsumerError):
                R5.build(invalid)

    def test_source_transition_is_readiness_and_digest_change_not_fake_progress(self):
        held = R5.from_provider(self.provider, FIXTURES.PR_URL)
        self.provider.set_selected_source()
        approved = R5.from_provider(self.provider, FIXTURES.PR_URL)
        self.assertNotEqual(held["relay_report_sha256"], approved["relay_report_sha256"])
        self.assertEqual("UNQUALIFIED_NO_APPROVED_GRAPH", held["state"]["engineering"])
        self.assertEqual("P0/E0", approved["state"]["engineering"])
        self.assertEqual("NONE", held["delivery_permission"])
        self.assertEqual("NONE", approved["delivery_permission"])

    def test_cli_read_only_hold_exit_three_approved_zero(self):
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.provider):
            self.assertEqual(3, R5.main([
                "--repository", self.provider.repository, "--entry-url", FIXTURES.ROOT_URL,
            ]))
        self.provider.set_selected_source()
        with patch.object(PUBLISH, "ScoreboardTransport", return_value=self.provider):
            self.assertEqual(0, R5.main([
                "--repository", self.provider.repository, "--entry-url", FIXTURES.PR_URL,
            ]))
        self.assertEqual([], self.provider.writes)


if __name__ == "__main__":
    unittest.main()
