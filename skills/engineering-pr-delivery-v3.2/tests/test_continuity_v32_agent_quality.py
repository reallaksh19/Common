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

import agent_quality_metrics_v32 as M


SCHEMA = yaml.safe_load((ROOT / "schemas" / "agent-quality-window-v32.schema.yaml").read_text(encoding="utf-8"))


def row(
    oid,
    kind,
    disposition,
    *,
    critical=False,
    expected=None,
    covered=None,
    repairs=0,
    refs=None,
):
    out = {
        "id": oid,
        "class": kind,
        "critical": critical,
        "disposition": disposition,
        "repairs": repairs,
        "evidence_refs": refs or [f"Common#690#{oid}"],
    }
    if expected is not None:
        out["impact_expected"] = expected
    if covered is not None:
        out["impact_covered"] = covered
    return out


def window(*rows):
    return {
        "schema": M.WINDOW_SCHEMA,
        "window_id": "M1-WINDOW-001",
        "observations": list(rows),
    }


class AgentQualityMetricTests(unittest.TestCase):
    def validate_both(self, source):
        jsonschema.validate(source, SCHEMA)
        result = M.evaluate(source)
        jsonschema.validate(result, SCHEMA)
        return result

    def test_clean_perfect_window_derives_one_without_authority(self):
        result = self.validate_both(window(
            row("M1", "MUTATION", "DETECTED", critical=True, expected=2, covered=2, repairs=1),
            row("M2", "MUTATION", "DETECTED", expected=3, covered=3),
            row("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            row("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        ))
        for key in ("mutation_tpr", "clean_tnr", "balanced_accuracy", "critical_mutation_recall", "impact_coverage"):
            self.assertEqual("OBSERVED", result["metrics"][key]["state"])
            self.assertEqual(1.0, result["metrics"][key]["value"])
        self.assertEqual(1, result["metrics"]["repair_count"])
        self.assertEqual([], result["authority_effects"])
        self.assertEqual(M.AUTHORITY, result["authority"])

    def test_misses_and_false_positives_reduce_only_observed_metrics(self):
        result = self.validate_both(window(
            row("M1", "MUTATION", "DETECTED", expected=2, covered=2),
            row("M2", "MUTATION", "MISSED", critical=True, expected=2, covered=1),
            row("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            row("C2", "CLEAN_CONTROL", "FALSE_POSITIVE"),
        ))
        self.assertEqual(0.5, result["metrics"]["mutation_tpr"]["value"])
        self.assertEqual(0.5, result["metrics"]["clean_tnr"]["value"])
        self.assertEqual(0.5, result["metrics"]["balanced_accuracy"]["value"])
        self.assertEqual(0.0, result["metrics"]["critical_mutation_recall"]["value"])
        self.assertEqual(0.75, result["metrics"]["impact_coverage"]["value"])

    def test_unknown_denominators_remain_unknown_not_zero(self):
        result = self.validate_both(window(
            row("M1", "MUTATION", "UNKNOWN", critical=True),
            row("C1", "CLEAN_CONTROL", "UNKNOWN", critical=True),
        ))
        for key in ("mutation_tpr", "clean_tnr", "balanced_accuracy", "critical_mutation_recall", "impact_coverage"):
            metric = result["metrics"][key]
            self.assertEqual("UNKNOWN", metric["state"])
            self.assertIsNone(metric["value"])
            self.assertEqual(0, metric["denominator"])
        self.assertEqual(2, result["unknown_observation_count"])
        self.assertEqual(2, result["metrics"]["critical_unknown_count"])

    def test_input_fails_closed_on_impossible_or_cross_class_evidence(self):
        cases = [
            window(row("M1", "MUTATION", "DETECTED", expected=1, covered=2)),
            window(row("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED", expected=1, covered=1)),
            window(row("M1", "MUTATION", "CLEAN_ACCEPTED")),
        ]
        for source in cases:
            with self.subTest(source=source):
                with self.assertRaises(M.MetricError):
                    M.evaluate(source)

    def test_digest_is_order_independent_within_one_window(self):
        a = row("M1", "MUTATION", "DETECTED", refs=["ref:b", "ref:a"])
        b = row("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED", refs=["ref:c"])
        first = M.evaluate(window(a, b))
        a2 = copy.deepcopy(a)
        a2["evidence_refs"].reverse()
        second = M.evaluate(window(b, a2))
        self.assertEqual(first["input_digest"], second["input_digest"])
        self.assertEqual(first["evidence_digest"], second["evidence_digest"])

    def test_empty_window_is_rejected(self):
        with self.assertRaises(M.MetricError):
            M.evaluate(window())

    def test_duplicate_observation_identity_is_rejected(self):
        with self.assertRaises(M.MetricError):
            M.evaluate(window(
                row("X", "MUTATION", "DETECTED"),
                row("X", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            ))

    def test_result_has_no_progress_or_verdict_authority_fields(self):
        result = self.validate_both(window(row("M1", "MUTATION", "DETECTED")))
        forbidden = {"progress", "p", "e", "pass", "fail", "review_verdict", "merge_authority", "admission", "title"}
        self.assertTrue(forbidden.isdisjoint({key.lower() for key in result}))
        self.assertEqual([], result["authority_effects"])


if __name__ == "__main__":
    unittest.main()
