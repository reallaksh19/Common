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
import agent_intervention_v32 as M3

SCHEMA = yaml.safe_load((ROOT / "schemas" / "agent-intervention-v32.schema.yaml").read_text(encoding="utf-8"))
BASIS_REF = "Common#689#agent-quality-benchmark-v1"
BASIS_DIGEST = "sha256:" + "b" * 64


def obs(oid, kind, disposition, *, critical=False, covered=None, repairs=0):
    row = {
        "id": oid,
        "class": kind,
        "critical": critical,
        "disposition": disposition,
        "repairs": repairs,
        "evidence_refs": [BASIS_REF, f"Common#699#{oid}"],
    }
    if covered is not None:
        row["impact_expected"] = 1
        row["impact_covered"] = covered
    return row


def quality(window_id, rows):
    return M1.evaluate({
        "schema": M1.WINDOW_SCHEMA,
        "window_id": window_id,
        "observations": rows,
    })


def trajectory(*items):
    return M2.evaluate({
        "schema": M2.INPUT_SCHEMA,
        "trajectory_id": "TRAJ-M3",
        "comparison_basis": {"ref": BASIS_REF, "digest": BASIS_DIGEST},
        "windows": [{"sequence": seq, "result": value} for seq, value in items],
    })


def intervention(value):
    return M3.evaluate({"schema": M3.INPUT_SCHEMA, "trajectory": value})


def good(window_id, *, repairs=0):
    return quality(window_id, [
        obs("M1", "MUTATION", "DETECTED", critical=True, covered=1, repairs=repairs),
        obs("M2", "MUTATION", "DETECTED", critical=True, covered=1),
        obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        obs("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
    ])


def poor(window_id):
    return quality(window_id, [
        obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
        obs("M2", "MUTATION", "MISSED", critical=True, covered=0),
        obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        obs("C2", "CLEAN_CONTROL", "FALSE_POSITIVE"),
    ])


class AgentInterventionTests(unittest.TestCase):
    def validate_both(self, source):
        jsonschema.validate(source, SCHEMA)
        derived = M3.evaluate(source)
        jsonschema.validate(derived, SCHEMA)
        return derived

    def test_incomplete_requires_replay(self):
        a = quality("W1", [obs("M1", "MUTATION", "DETECTED", critical=True, covered=1)])
        b = quality("W2", [obs("M1", "MUTATION", "DETECTED", critical=True, covered=1)])
        out = intervention(trajectory((1, a), (2, b)))
        self.assertEqual(("REPLAY_REQUIRED", "EVIDENCE_INCOMPLETE"), (out["recommendation"], out["reason"]))

    def test_mixed_signal_requires_fresh_self_review(self):
        out = intervention(trajectory((1, poor("W1")), (2, good("W2")), (3, poor("W3"))))
        self.assertEqual(("FRESH_SELF_REVIEW", "DIRECTION_REVERSAL"), (out["recommendation"], out["reason"]))

    def test_conflicting_signal_requires_checkpoint(self):
        a = quality("W1", [
            obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("M2", "MUTATION", "MISSED", critical=True, covered=0),
            obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            obs("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        ])
        b = quality("W2", [
            obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("M2", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            obs("C2", "CLEAN_CONTROL", "FALSE_POSITIVE"),
        ])
        out = intervention(trajectory((1, a), (2, b)))
        self.assertEqual(("CHECKPOINT", "COMPONENTS_CONFLICT"), (out["recommendation"], out["reason"]))

    def test_degrading_with_critical_unknown_requires_fresh_reconstruction(self):
        degraded = quality("W2", [
            obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("M2", "MUTATION", "MISSED", critical=True, covered=0),
            obs("U1", "MUTATION", "UNKNOWN", critical=True),
            obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            obs("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        ])
        out = intervention(trajectory((1, good("W1")), (2, degraded)))
        self.assertEqual(
            ("FRESH_RECONSTRUCTION", "CRITICAL_UNCERTAINTY_PRESENT"),
            (out["recommendation"], out["reason"]),
        )

    def test_stable_with_persistent_critical_unknown_requires_fresh_reconstruction(self):
        def uncertain(window_id):
            return quality(window_id, [
                obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
                obs("U1", "MUTATION", "UNKNOWN", critical=True),
                obs("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
                obs("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            ])

        value = trajectory((1, uncertain("W1")), (2, uncertain("W2")))
        self.assertEqual("STABLE", value["trajectory"])
        out = intervention(value)
        self.assertEqual(
            ("FRESH_RECONSTRUCTION", "CRITICAL_UNCERTAINTY_PRESENT"),
            (out["recommendation"], out["reason"]),
        )

    def test_degrading_with_rising_repairs_splits_remainder(self):
        out = intervention(trajectory((1, good("W1")), (2, good("W2", repairs=1))))
        self.assertEqual(
            ("SPLIT_REMAINDER", "DEGRADING_WITH_RISING_REPAIR_RATE"),
            (out["recommendation"], out["reason"]),
        )

    def test_other_degradation_checkpoints(self):
        out = intervention(trajectory((1, good("W1")), (2, poor("W2"))))
        self.assertEqual(("CHECKPOINT", "DEGRADING_CHECKPOINT"), (out["recommendation"], out["reason"]))

    def test_stable_and_improving_require_no_intervention(self):
        stable = intervention(trajectory((1, good("W1")), (2, good("W2"))))
        improving = intervention(trajectory((1, poor("W3")), (2, good("W4"))))
        self.assertEqual("NONE", stable["recommendation"])
        self.assertEqual("NONE", improving["recommendation"])

    def test_handover_and_replan_are_not_quality_only_outputs(self):
        outputs = {
            intervention(trajectory((1, good("A1")), (2, good("A2"))))["recommendation"],
            intervention(trajectory((1, good("B1")), (2, poor("B2"))))["recommendation"],
        }
        self.assertTrue({"HANDOVER", "REPLAN"}.isdisjoint(outputs))

    def test_intermediate_unknown_with_observed_boundaries_remains_valid_m2_input(self):
        a = good("W1")
        middle = quality("W2", [
            obs("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            obs("C1", "CLEAN_CONTROL", "UNKNOWN"),
        ])
        c = good("W3")
        value = trajectory((1, a), (2, middle), (3, c))
        self.assertEqual("INSUFFICIENT_DATA", value["trajectory"])
        out = intervention(value)
        self.assertEqual("REPLAY_REQUIRED", out["recommendation"])

    def test_wrong_authority_and_tampered_digest_reject(self):
        value = trajectory((1, poor("W1")), (2, good("W2")))
        wrong = copy.deepcopy(value)
        wrong["authority"] = "ENGINEERING_PASS"
        with self.assertRaises(M3.InterventionError):
            intervention(wrong)
        tampered = copy.deepcopy(value)
        tampered["trajectory"] = "DEGRADING"
        tampered["reason"] = "MONOTONIC_DEGRADATION"
        with self.assertRaises(M3.InterventionError):
            intervention(tampered)

    def test_duplicate_m2_window_identity_rejects_even_with_recomputed_digest(self):
        value = trajectory((1, poor("W1")), (2, good("W2")))
        duplicate = copy.deepcopy(value)
        duplicate["windows"][1]["window_id"] = duplicate["windows"][0]["window_id"]
        duplicate["trajectory_digest"] = M3._digest({
            "trajectory_id": duplicate["trajectory_id"],
            "comparison_basis": duplicate["comparison_basis"],
            "input_digest": duplicate["input_digest"],
            "trajectory": duplicate["trajectory"],
            "reason": duplicate["reason"],
            "windows": duplicate["windows"],
            "components": duplicate["components"],
        })
        with self.assertRaises(M3.InterventionError):
            intervention(duplicate)

    def test_output_is_advisory_only_with_zero_authority_leakage(self):
        source = {"schema": M3.INPUT_SCHEMA, "trajectory": trajectory((1, poor("W1")), (2, good("W2")))}
        out = self.validate_both(source)
        self.assertTrue(out["advisory_only"])
        self.assertEqual([], out["authority_effects"])
        self.assertEqual(M3.AUTHORITY, out["authority"])
        forbidden = {
            "progress", "p", "e", "pass", "fail", "review_verdict", "admission",
            "merge_authority", "release_authority", "title", "handover", "replan",
        }
        self.assertTrue(forbidden.isdisjoint({key.lower() for key in out}))
        self.assertRegex(out["recommendation_digest"], r"^sha256:[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
