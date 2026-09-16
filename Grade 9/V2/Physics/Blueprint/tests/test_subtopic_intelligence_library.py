#!/usr/bin/env python3
"""
Unit Tests for Physics Subtopic Intelligence Library (SIL) Intake Validator
===========================================================================
Tests packet extraction, 6-point intake gate validation, and mutation falsification.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from validate_subtopic_intelligence_library import (  # noqa: E402
    DEFAULT_SPEC_PATH,
    extract_packets,
    validate_packet,
    validate_subtopic_intelligence_spec,
)


class PhysicsSubtopicIntelligenceLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec_text = DEFAULT_SPEC_PATH.read_text(encoding="utf-8")

    def test_sil_intake_validation_full_spec_passes(self) -> None:
        report = validate_subtopic_intelligence_spec(self.spec_text)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["total_packets_evaluated"], 43)
        self.assertEqual(report["packets_passing"], 43)
        self.assertEqual(report["packets_failing"], 0)

    def test_sil_each_packet_satisfies_all_gates(self) -> None:
        report = validate_subtopic_intelligence_spec(self.spec_text)
        for eval_item in report["packet_evaluations"]:
            with self.subTest(gate_id=eval_item["gate_id"]):
                self.assertEqual(eval_item["status"], "PASS")
                self.assertEqual(eval_item["gates"]["gate1_preconditions"]["status"], "PASS")
                self.assertEqual(eval_item["gates"]["gate2_learning_atoms"]["status"], "PASS")
                self.assertEqual(eval_item["gates"]["gate3_misconceptions"]["status"], "PASS")
                self.assertEqual(eval_item["gates"]["gate4_reconstructable_ttus"]["status"], "PASS")
                self.assertEqual(eval_item["gates"]["gate5_exam_families"]["status"], "PASS")

    def test_sil_validator_detects_missing_preconditions(self) -> None:
        packets = extract_packets(self.spec_text)
        self.assertGreater(len(packets), 0)
        p = dict(packets[0])
        # Mutate to remove preconditions
        p["body"] = p["body"].replace("Non-Negotiable Preconditions", "General Notes")
        result = validate_packet(p)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["gates"]["gate1_preconditions"]["status"], "FAIL")

    def test_sil_validator_detects_insufficient_atoms(self) -> None:
        packets = extract_packets(self.spec_text)
        p = dict(packets[0])
        # Strip out ATOM entries
        p["body"] = re.sub(r"ATOM-[A-Z]+-\d+", "CONCEPT_ITEM", p["body"])
        result = validate_packet(p)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["gates"]["gate2_learning_atoms"]["status"], "FAIL")

    def test_sil_validator_detects_missing_misconceptions(self) -> None:
        packets = extract_packets(self.spec_text)
        p = dict(packets[0])
        p["body"] = p["body"].replace("Misconception:", "Note:")
        result = validate_packet(p)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["gates"]["gate3_misconceptions"]["status"], "FAIL")

    def test_sil_validator_detects_missing_ttu_completion_keys(self) -> None:
        packets = extract_packets(self.spec_text)
        p = dict(packets[0])
        p["body"] = p["body"].replace("COMPLETION KEY", "SOLUTIONS OMITTED")
        result = validate_packet(p)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["gates"]["gate4_reconstructable_ttus"]["status"], "FAIL")

    def test_sil_validator_detects_missing_exam_families(self) -> None:
        packets = extract_packets(self.spec_text)
        p = dict(packets[0])
        p["body"] = re.sub(r"FAMILY-[A-Z]+-\d+", "EXAM_ITEM", p["body"])
        result = validate_packet(p)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["gates"]["gate5_exam_families"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
