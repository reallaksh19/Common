"""R1-E independent cycle acceptance: same basis on every offline consumer."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "integration_cycle_stress_v35.py"
FIXTURE = ROOT / "examples/integration/real-common-600-604-712.golden.json"
FROZEN_EXPECTED = ROOT / "examples/integration/real-common-600-604-712.expected-cycle.json"

sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("integration_cycle_stress_v35", SCRIPT)
C = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(C)


class IntegrationCycleStressAcceptance(unittest.TestCase):
    def data(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_all_nine_surfaces_and_three_titles_share_one_basis(self):
        data = self.data()
        report = C.cycle(data)
        self.assertEqual("OFFLINE_HISTORICAL_GOLDEN_NOT_LIVE", report["mode"])
        self.assertEqual(9, len(report["surfaces"]))
        self.assertEqual(3, len(report["titles"]))
        expected = "BASIS_SHA256: " + report["basis_sha256"]
        for key, body in report["surfaces"].items():
            with self.subTest(key=key):
                self.assertIn(expected, body)
                self.assertIn("SOURCE_NOT_PROVEN", body)
                self.assertIn("UNRESOLVED_CHAT_LINK", body)
                self.assertIn("EVIDENCE_REF:", body)
                self.assertIn("NEXT:", body)
        self.assertIn("TASK_EVIDENCE — START [GENERATED EXAMPLE",
                      report["surfaces"]["task_evidence_start"])
        self.assertIn("TASK_EVIDENCE — END [GENERATED EXAMPLE",
                      report["surfaces"]["task_evidence_end"])
        self.assertIn("not authority", report["surfaces"]["owner_report"].lower())
        self.assertIn("NOT_CODED_NOT_TESTED",
                      report["surfaces"]["parent_issue"])
        self.assertIn("BLOCKED_SOURCE_NOT_PROVEN",
                      report["surfaces"]["draft_pr"])
        self.assertIn("CR-10 Integration", report["surfaces"]["reviewer_checklist"])
        self.assertIn("R-10 Agent-6 replay", report["surfaces"]["reviewer_checklist"])
        C.assert_same_cycle(data, report)

    def test_all_twelve_outputs_match_prior_hosted_frozen_bytes(self):
        """Regression oracle read back from previous hosted run, not recomputed by cycle()."""
        expected = json.loads(FROZEN_EXPECTED.read_text(encoding="utf-8"))
        observed = C.cycle(self.data())
        self.assertEqual("HOSTED_GOLDEN_SPECIMEN_NOT_AUTHORITATIVE", expected["provenance"])
        self.assertEqual(expected["source_basis"], observed["basis_sha256"])
        self.assertEqual(expected["titles"], observed["titles"])
        self.assertEqual(expected["surfaces"], observed["surfaces"])

    def test_individual_title_and_body_tamper_is_detected(self):
        data = self.data()
        original = C.cycle(data)
        for kind in ("titles", "surfaces"):
            for key in original[kind]:
                wrong = copy.deepcopy(original)
                wrong[kind][key] += " PROGRESS=100"
                with self.subTest(kind=kind, key=key), self.assertRaises(
                    C.GoldenContractError
                ):
                    C.assert_same_cycle(data, wrong)

    def test_moving_candidate_invalidates_prior_ci_not_owner_semantics(self):
        data = self.data()
        before = C.cycle(data)
        after_data = copy.deepcopy(data)
        after_data["candidate_pr"]["head_sha"] = "d" * 40
        after = C.cycle(after_data)
        self.assertEqual("CI_STALE", after["qualification"])
        self.assertEqual("HOLD", after["semantic"])
        self.assertEqual(before["titles"]["parent_issue"],
                         after["titles"]["parent_issue"])
        self.assertNotEqual(before["titles"]["draft_pr"],
                            after["titles"]["draft_pr"])
        with self.assertRaises(C.GoldenContractError):
            C.assert_same_cycle(after_data, before)

    def test_forged_owner_or_foreign_leaf_rejected(self):
        fixture = self.data()
        for section, key, value in (
            ("owner_origin", "original_source_status", "PROVEN"),
            ("candidate_pr", "responsibility_issue", 438),
            ("responsibility", "custody_source", "SAFE"),
            ("review_observation", "independent", "APPROVED"),
        ):
            bad = copy.deepcopy(fixture)
            bad[section][key] = value
            with self.subTest(section=section, key=key), self.assertRaises(
                C.GoldenContractError
            ):
                C.cycle(bad)

    def test_standalone_cli_rejects_unsupported_complete_scoreboard(self):
        data = self.data()
        data["programme"]["integration_acceptance"]["qualified"] = 8
        with tempfile.TemporaryDirectory() as tmp:
            forged = Path(tmp) / "unsupported-ic.json"
            forged.write_text(json.dumps(data), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--stress-check", "--fixture", str(forged)],
                capture_output=True, text=True, timeout=25, check=False,
            )
        self.assertNotEqual(0, proc.returncode)
        self.assertIn("unsupported IC acceptance", proc.stderr)
        self.assertNotIn('"result": "PASS"', proc.stdout)

    def test_module_self_runs_and_emits_the_exact_same_cycle(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--stress-check",
             "--fixture", str(FIXTURE), "--emit"],
            capture_output=True, text=True, check=False, timeout=25,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        report = C.stress_check(self.data())
        self.assertIn('"result": "PASS"', proc.stdout)
        self.assertIn(report["basis_sha256"], proc.stdout)
        self.assertGreaterEqual(report["checked"], 20)
        generated = C.cycle(self.data())
        for key, title in generated["titles"].items():
            self.assertIn(f"=== TITLE {key} ===\n{title}", proc.stdout)
        for key, body in generated["surfaces"].items():
            self.assertIn(f"=== SURFACE {key} ===\n{body}", proc.stdout)
        # Emit exactly the same CLI-produced specimen to hosted logs for Owner
        # review, not a manually recreated / unverifiable issue comment.
        for name, title in generated["titles"].items():
            print("V35_CYCLE_TITLE_JSON=" + json.dumps(
                {"name": name, "title": title, "basis_sha256": report["basis_sha256"]},
                ensure_ascii=False, sort_keys=True))
        for name, body in generated["surfaces"].items():
            print("V35_CYCLE_SURFACE_JSON=" + json.dumps(
                {"name": name, "body": body, "basis_sha256": report["basis_sha256"]},
                ensure_ascii=False, sort_keys=True))
        print("V3.5_SELF_RUN_STRESS_RESULT=" + json.dumps(report, sort_keys=True))
        print("V3.5_ISSUE_EXCERPT=" +
              generated["surfaces"]["parent_issue"][:260].replace("\n", " | "))
        print("V3.5_TASK_EVIDENCE_EXCERPT=" +
              generated["surfaces"]["task_evidence_end"][:260].replace("\n", " | "))
        print("V3.5_HANDOVER_EXCERPT=" +
              generated["surfaces"]["handover_prompt"][:260].replace("\n", " | "))


if __name__ == "__main__":
    unittest.main()
