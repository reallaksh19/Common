import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from shadow_rollout import (
    derive_classification,
    derive_relative_outcome,
    summarize,
    validate_observation,
    validate_summary,
)


CANDIDATE = "c" * 40


def observation(
    *,
    gate="ADVANCE_ELIGIBLE",
    incumbent="ADVANCE",
    adjudication="CORRECT",
    severity=None,
    evidence_refs=None,
):
    value = {
        "schema_version": "SHADOW_OBSERVATION_V1",
        "authority": "NON_BLOCKING_SHADOW_OBSERVATION",
        "candidate_sha": CANDIDATE,
        "gate_result": {
            "ref": "gate://1",
            "decision": gate,
        },
        "incumbent": {
            "decision": incumbent,
            "evidence_refs": ["incumbent://1"],
        },
        "adjudication": {
            "state": adjudication,
            "severity": severity,
            "evidence_refs": list(evidence_refs or []),
        },
        "production_effect": "NONE",
        "classification": "PENDING_ADJUDICATION",
        "relative_outcome": "PENDING",
    }
    value["classification"] = derive_classification(value)
    value["relative_outcome"] = derive_relative_outcome(value)
    return value


class ShadowRolloutTests(unittest.TestCase):
    def test_true_clear(self):
        value = observation()
        self.assertEqual(value["classification"], "TRUE_CLEAR")
        self.assertEqual(value["relative_outcome"], "SAME")
        self.assertEqual(validate_observation(value), [])

    def test_false_clear_when_gate_advances_defect(self):
        value = observation(
            adjudication="DEFECT",
            severity="HIGH",
            evidence_refs=["defect://1"],
        )
        self.assertEqual(value["classification"], "FALSE_CLEAR")
        self.assertEqual(validate_observation(value), [])

    def test_true_block_when_repair_matches_defect(self):
        value = observation(
            gate="REPAIR",
            incumbent="BLOCK",
            adjudication="DEFECT",
            severity="CRITICAL",
            evidence_refs=["defect://2"],
        )
        self.assertEqual(value["classification"], "TRUE_BLOCK")
        self.assertEqual(value["relative_outcome"], "SAME")

    def test_false_block_when_repair_blocks_correct_candidate(self):
        value = observation(
            gate="REPAIR",
            incumbent="ADVANCE",
            adjudication="CORRECT",
        )
        self.assertEqual(value["classification"], "FALSE_BLOCK")
        self.assertEqual(value["relative_outcome"], "DIVERGENT")

    def test_protective_escalation_catches_incumbent_miss(self):
        value = observation(
            gate="ESCALATE",
            incumbent="ADVANCE",
            adjudication="DEFECT",
            severity="HIGH",
            evidence_refs=["defect://3"],
        )
        self.assertEqual(value["classification"], "PROTECTIVE_ESCALATION")
        self.assertEqual(value["relative_outcome"], "CAUGHT_INCUMBENT_MISS")

    def test_gate_can_avoid_incumbent_false_block(self):
        value = observation(
            gate="ADVANCE_ELIGIBLE",
            incumbent="BLOCK",
            adjudication="CORRECT",
        )
        self.assertEqual(value["relative_outcome"], "AVOIDED_INCUMBENT_FALSE_BLOCK")

    def test_pending_adjudication_remains_pending(self):
        value = observation(
            gate="REPLAY_EVIDENCE",
            incumbent="UNKNOWN",
            adjudication="UNKNOWN",
        )
        self.assertEqual(value["classification"], "PENDING_ADJUDICATION")
        self.assertEqual(value["relative_outcome"], "PENDING")
        self.assertEqual(validate_observation(value), [])

    def test_defect_requires_severity_and_evidence(self):
        value = observation(
            adjudication="DEFECT",
            severity=None,
            evidence_refs=[],
        )
        errors = validate_observation(value)
        self.assertTrue(any("requires severity" in error for error in errors), errors)
        self.assertTrue(any("requires evidence_refs" in error for error in errors), errors)

    def test_correct_adjudication_cannot_carry_defect_severity(self):
        value = observation(
            adjudication="CORRECT",
            severity="HIGH",
        )
        errors = validate_observation(value)
        self.assertTrue(any("severity=null" in error for error in errors), errors)

    def test_stored_classification_cannot_be_tampered(self):
        value = observation()
        value["classification"] = "FALSE_CLEAR"
        errors = validate_observation(value)
        self.assertTrue(any("does not match derived" in error for error in errors), errors)

    def test_shadow_record_cannot_acquire_production_effect(self):
        value = observation()
        value["production_effect"] = "BLOCK"
        errors = validate_observation(value)
        self.assertTrue(any("NONE was expected" in error for error in errors), errors)

    def test_summary_counts_without_composite_score(self):
        samples = [
            observation(),
            observation(
                adjudication="DEFECT",
                severity="HIGH",
                evidence_refs=["defect://4"],
            ),
            observation(
                gate="ESCALATE",
                incumbent="ADVANCE",
                adjudication="DEFECT",
                severity="NORMAL",
                evidence_refs=["defect://5"],
            ),
            observation(
                gate="REPLAY_EVIDENCE",
                incumbent="UNKNOWN",
                adjudication="UNKNOWN",
            ),
        ]
        summary = summarize(samples)
        self.assertEqual(summary["sample_count"], 4)
        self.assertEqual(summary["adjudicated_count"], 3)
        self.assertEqual(summary["counts"]["TRUE_CLEAR"], 1)
        self.assertEqual(summary["counts"]["FALSE_CLEAR"], 1)
        self.assertEqual(summary["counts"]["PROTECTIVE_ESCALATION"], 1)
        self.assertEqual(summary["counts"]["PENDING_ADJUDICATION"], 1)
        self.assertEqual(summary["relative_counts"]["CAUGHT_INCUMBENT_MISS"], 1)
        self.assertNotIn("score", summary)
        self.assertNotIn("threshold", summary)
        self.assertEqual(validate_summary(summary), [])

    def test_summary_counts_must_equal_sample_count(self):
        summary = summarize([observation()])
        summary["counts"]["TRUE_CLEAR"] = 0
        errors = validate_summary(summary)
        self.assertTrue(any("counts must equal" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
