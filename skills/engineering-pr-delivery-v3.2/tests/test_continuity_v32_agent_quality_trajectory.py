from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import agent_quality_metrics_v32 as M1
import agent_quality_trajectory_v32 as M2

SCHEMA = yaml.safe_load((ROOT / "schemas" / "agent-quality-trajectory-v32.schema.yaml").read_text(encoding="utf-8"))


BASIS_REF = "Common#689#agent-quality-benchmark-v1"
BASIS_DIGEST = "sha256:" + "b" * 64


def obs(oid, kind, disposition, *, critical=False, covered=None, repairs=0):
    row = {
        "id": oid,
        "class": kind,
        "critical": critical,
        "disposition": disposition,
        "repairs": repairs,
        "evidence_refs": [BASIS_REF, f"Common#694#{oid}"],
    }
    if covered is not None:
        row["impact_expected"] = 1
        row["impact_covered"] = covered
    return row


def result(window_id, rows):
    return M1.evaluate({
        "schema": M1.WINDOW_SCHEMA,
        "window_id": window_id,
        "observations": rows,
    })


def poor(window_id="W-POOR"):
    return result(window_id, [
        obs("M1", "MUTATION", "DETECTED", critical=True, covered=1, repairs=1),
        obs("M2", "MUTATION", "MISSED", critical=True, covered=0),
        obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        obs("C2", "CLEAN_CONTROL", "FALSE_POSITIVE"),
    ])


def good(window_id="W-GOOD"):
    return result(window_id, [
        obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
        obs("M2", "MUTATION", "DETECTED", critical=True, covered=1),
        obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        obs("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
    ])


def source(*items):
    return {
        "schema": M2.INPUT_SCHEMA,
        "trajectory_id": "TRAJ-001",
        "comparison_basis": {"ref": BASIS_REF, "digest": BASIS_DIGEST},
        "windows": [{"sequence": seq, "result": value} for seq, value in items],
    }


class AgentQualityTrajectoryTests(unittest.TestCase):
    def validate_both(self, value):
        jsonschema.validate(value, SCHEMA)
        derived = M2.evaluate(value)
        jsonschema.validate(derived, SCHEMA)
        return derived

    def test_identical_quality_is_stable(self):
        out = self.validate_both(source((1, poor("W1")), (2, poor("W2"))))
        self.assertEqual(("STABLE", "ALL_COMPONENTS_STABLE"), (out["trajectory"], out["reason"]))

    def test_monotonic_improvement_is_improving(self):
        out = self.validate_both(source((1, poor("W1")), (2, good("W2"))))
        self.assertEqual(("IMPROVING", "MONOTONIC_IMPROVEMENT"), (out["trajectory"], out["reason"]))
        self.assertEqual("IMPROVING", out["components"]["repair_rate"]["direction"])

    def test_monotonic_degradation_is_degrading(self):
        out = self.validate_both(source((1, good("W1")), (2, poor("W2"))))
        self.assertEqual(("DEGRADING", "MONOTONIC_DEGRADATION"), (out["trajectory"], out["reason"]))

    def test_reversal_is_mixed_signal_not_a_forced_score(self):
        out = self.validate_both(source((1, poor("W1")), (2, good("W2")), (3, poor("W3"))))
        self.assertEqual(("INSUFFICIENT_DATA", "MIXED_SIGNAL"), (out["trajectory"], out["reason"]))
        self.assertIn("MIXED", {row["direction"] for row in out["components"].values()})

    def test_conflicting_components_are_insufficient(self):
        first = result("W1", [
            obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("M2", "MUTATION", "MISSED", critical=True, covered=0),
            obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            obs("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        ])
        second = result("W2", [
            obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("M2", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            obs("C2", "CLEAN_CONTROL", "FALSE_POSITIVE"),
        ])
        out = self.validate_both(source((1, first), (2, second)))
        self.assertEqual(("INSUFFICIENT_DATA", "CONFLICTING_SIGNAL"), (out["trajectory"], out["reason"]))

    def test_unknown_m1_component_is_incomplete_signal(self):
        first = result("W1", [obs("M1", "MUTATION", "DETECTED", critical=True, covered=1)])
        second = result("W2", [obs("M1", "MUTATION", "DETECTED", critical=True, covered=1)])
        out = self.validate_both(source((1, first), (2, second)))
        self.assertEqual(("INSUFFICIENT_DATA", "INCOMPLETE_SIGNAL"), (out["trajectory"], out["reason"]))
        self.assertEqual("INSUFFICIENT_DATA", out["components"]["clean_tnr"]["direction"])

    def test_comparison_basis_must_be_durable_and_shared_by_every_window(self):
        value = source((1, poor("W1")), (2, good("W2")))
        value["comparison_basis"] = {"ref": "Common#689#different-benchmark", "digest": BASIS_DIGEST}
        with self.assertRaises(M2.TrajectoryError):
            M2.evaluate(value)

    def test_sequence_not_input_order_controls_result_and_digest(self):
        a, b = poor("W1"), good("W2")
        forward = M2.evaluate(source((1, a), (2, b)))
        reverse_input = M2.evaluate(source((2, b), (1, a)))
        self.assertEqual(forward, reverse_input)

    def test_duplicate_sequence_or_window_rejects(self):
        a = poor("W1")
        with self.assertRaises(M2.TrajectoryError):
            M2.evaluate(source((1, a), (1, good("W2"))))
        with self.assertRaises(M2.TrajectoryError):
            M2.evaluate(source((1, a), (2, copy.deepcopy(a))))

    def test_wrong_or_tampered_m1_authority_rejects(self):
        bad = poor("W1")
        bad["authority"] = "ENGINEERING_PASS"
        with self.assertRaises(M2.TrajectoryError):
            M2.evaluate(source((1, bad), (2, good("W2"))))

    def test_rates_not_raw_counts_define_lower_is_better_components(self):
        small = result("W1", [
            obs("U1", "MUTATION", "UNKNOWN", critical=True),
            *[obs(f"C{i}", "CLEAN_CONTROL", "CLEAN_ACCEPTED") for i in range(1, 10)],
        ])
        large = result("W2", [
            obs("U1", "MUTATION", "UNKNOWN", critical=True),
            obs("U2", "MUTATION", "UNKNOWN", critical=True),
            *[obs(f"C{i}", "CLEAN_CONTROL", "CLEAN_ACCEPTED") for i in range(1, 19)],
        ])
        out = M2.evaluate(source((1, small), (2, large)))
        self.assertEqual("STABLE", out["components"]["critical_unknown_rate"]["direction"])

    def test_output_has_zero_authority_leakage(self):
        out = self.validate_both(source((1, poor("W1")), (2, good("W2"))))
        forbidden = {
            "progress", "p", "e", "pass", "fail", "review_verdict",
            "merge_authority", "admission", "title", "intervention",
        }
        self.assertTrue(forbidden.isdisjoint({key.lower() for key in out}))
        self.assertEqual([], out["authority_effects"])
        self.assertEqual(M2.AUTHORITY, out["authority"])


if __name__ == "__main__":
    unittest.main()
