"""#718/#733 source-level integrated fixture replay — separately frozen oracle.

The full programme gate intentionally remains red: ESC-4/5 consumers
are separately unreleased. This suite certifies only the bounded ESC-3
pure cross-surface product slice, including real DELP and R-PROOF join.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess

HERE = Path(__file__).resolve()
V32 = HERE.parents[1]
ROOT = HERE.parents[3]
sys.path.insert(0, str(V32 / "scripts"))
import vertical_cycle_v32 as replay  # noqa: E402
import pr_responsibility_view_v32 as view  # noqa: E402


class VerticalResponsibilityCycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json").read_text())
        cls.graph = json.loads((ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json").read_text())

    def test_01_release_claim_and_owner_source_bound_real_chain(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual("PASS_PURE_READ_VIEWS", r["R_PROJECTION_phase_gate"])
        self.assertEqual("UNREPORTED", r["material_vs_facts"]["checkpoint_facts"])
        self.assertEqual(["UNRESOLVED_CHAT_MESSAGE_LINK"], r["owner_origin_status"])
        self.assertEqual([], r["authority_effects"])

    def test_02_parent_title_oracle_independent_of_renderer(self):
        r = replay.replay(self.manifest, self.graph)
        golden = replay._fixture(self.manifest, "GF-SMART-SURFACES")["expected"]
        self.assertEqual(golden["parent_title"], r["parent_actual_title"])

    def test_03_child_title_oracle_independent_of_renderer(self):
        r = replay.replay(self.manifest, self.graph)
        golden = replay._fixture(self.manifest, "GF-SMART-SURFACES")["expected"]
        self.assertEqual(golden["child_title"], r["child_actual_title"])

    def test_04_changed_candidate_draft_smart_title_never_keeps_old_head(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertIn("HEAD:bbbbbbb · Q:UNPROVEN", r["draft_changed_head_title"])
        self.assertNotEqual(r["source_input_digest"], r["changed_head_input_digest"])

    def test_05_PR_managed_block_preserves_exact_OI_OR_and_evidence_basis(self):
        r = replay.replay(self.manifest, self.graph)
        body = r["draft_pr_managed_description"]
        self.assertIn("OR-718-04", body)
        self.assertIn("GF-PR-HEAD", body)
        self.assertIn(r["changed_head_input_digest"], body)
        self.assertIn("UNBOUND_ADVISORY", body)

    def test_06_full_chain_fails_closed_on_unreleased_handover_and_metric(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", r["full_ESC_6_gate"])
        self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED", r["stage_results"]["HANDOVER_PROMPT"])
        self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED", r["stage_results"]["AGENT_MATRIX"])

    def test_07_mutated_parent_title_oracle_is_rejected(self):
        m = copy.deepcopy(self.manifest)
        replay._fixture(m, "GF-SMART-SURFACES")["expected"]["parent_title"] = "🟢 [718] COMPLETE"
        with self.assertRaisesRegex(replay.ReplayError, "GOLDEN_PARENT_TITLE_MISMATCH"):
            replay.replay(m, self.graph)

    def test_08_mutated_child_title_oracle_is_rejected(self):
        m = copy.deepcopy(self.manifest)
        replay._fixture(m, "GF-SMART-SURFACES")["expected"]["child_title"] = "🟢 [733] CODE COMPLETE"
        with self.assertRaisesRegex(replay.ReplayError, "GOLDEN_CHILD_TITLE_MISMATCH"):
            replay.replay(m, self.graph)

    def test_09_changed_graph_release_digest_rejected(self):
        g = copy.deepcopy(self.graph)
        g["programme"]["decomposition_proposal"]["released_proposal_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(replay.ReplayError, "FROZEN_PLAN_DIGEST_DRIFT"):
            replay.replay(self.manifest, g)

    def test_10_wrong_original_chat_source_status_rejected(self):
        m = copy.deepcopy(self.manifest)
        m["owner_intents"][0]["original_source_status"] = "KNOWN"
        with self.assertRaisesRegex(view.ViewError, "ORIGINAL_SOURCE_UNACCOUNTED"):
            replay.replay(m, self.graph)

    def test_11_exact_candidate_move_does_not_claim_semantic_progress(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual("PASS_REAL_V32_DELP_AND_STALE_QUALIFIER", r["stage_results"]["SOURCE_OBSERVATION"])
        self.assertEqual("UNREPORTED", r["material_vs_facts"]["checkpoint_facts"])
        self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", r["full_ESC_6_gate"])

    def test_12_report_is_deterministic_and_no_authority_leaks(self):
        a = replay.replay(self.manifest, self.graph)
        b = replay.replay(self.manifest, self.graph)
        self.assertEqual(a, b)
        self.assertNotIn("OWNER_AUTHORIZED_MERGE", json.dumps(a))
        self.assertNotIn("FULL_PASS", json.dumps(a))

    def test_13_output_stage_contract_has_every_consumer(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual(set(self.manifest["required_stage_outputs"]), set(r["stage_results"]))

    def test_14_real_source_runner_generates_replay_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "report.json"
            report = replay.replay(self.manifest, self.graph)
            path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("PASS_PURE_READ_VIEWS", loaded["R_PROJECTION_phase_gate"])
            self.assertTrue(loaded["fixture_manifest_digest"].startswith("sha256:"))


    def test_15_executable_source_module_phase_gate_and_report(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "phase-report.json"
            command = [sys.executable, str(V32 / "scripts" / "vertical_cycle_v32.py"),
                       "--manifest", str(ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"),
                       "--graph", str(ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json"),
                       "--report", str(report)]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(0, run.returncode, run.stderr)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("PASS_PURE_READ_VIEWS", result["R_PROJECTION_phase_gate"])
            self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", result["full_ESC_6_gate"])
            self.assertEqual(0, result["exit_code"])
            print("V32_733_REAL_CLI_PHASE=PASS")
            print("V32_733_CLI_FIXTURE_DIGEST=" + result["fixture_manifest_digest"])

    def test_16_executable_source_module_full_gate_must_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "full-expected-red.json"
            command = [sys.executable, str(V32 / "scripts" / "vertical_cycle_v32.py"),
                       "--assert-all-consumers", "--report", str(report)]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(2, run.returncode, run.stderr)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", result["full_ESC_6_gate"])
            self.assertEqual(2, result["exit_code"])
            self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED",
                             result["stage_results"]["HANDOVER_PROMPT"])
            self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED",
                             result["stage_results"]["AGENT_MATRIX"])
            print("V32_733_REAL_CLI_FULL=EXPECTED_RED_UNRELEASED")


if __name__ == "__main__":
    unittest.main()
