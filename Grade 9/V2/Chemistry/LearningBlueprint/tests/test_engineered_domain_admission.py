#!/usr/bin/env python3
"""Tests for Chemistry Engineered Domain Admission Validator."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from validate_engineered_domain_admission import (  # noqa: E402
    ChemistryEngineeredDomainAdmissionError,
    load_json,
    validate,
)

REGISTRY = load_json("policies/chemistry-technical-engineering-gates.v1.json")


class ChemistryEngineeredDomainAdmissionTests(unittest.TestCase):
    def test_valid_admission_passes(self):
        valid_doc = {
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "admission_receipt_id": "CHEM-ENG-ADM-TEST-1",
            "registry_id": "CHEM-G9-11-TECHNICAL-ENGINEERING-GATES-v1",
            "registry_digest": "sha256:1663c3d884f20664c08d29de4d23d3dd10370fd5321093d298a2ed3a037c6d2d",
            "evaluated_gate_ids": ["CHEM-SYM-LITERACY", "CHEM-ION-VALENCY"],
            "admitted_gate_ids": ["CHEM-SYM-LITERACY", "CHEM-ION-VALENCY"],
            "held_gate_ids": [],
            "admission_status": "ADMITTED",
        }
        res = validate(valid_doc, REGISTRY)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["admitted_count"], 2)

    def test_held_gates_with_admitted_status_rejected(self):
        invalid_doc = {
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "admission_receipt_id": "CHEM-ENG-ADM-TEST-2",
            "registry_id": "CHEM-G9-11-TECHNICAL-ENGINEERING-GATES-v1",
            "registry_digest": "sha256:1663c3d884f20664c08d29de4d23d3dd10370fd5321093d298a2ed3a037c6d2d",
            "evaluated_gate_ids": ["CHEM-SYM-LITERACY"],
            "admitted_gate_ids": [],
            "held_gate_ids": ["CHEM-SYM-LITERACY"],
            "admission_status": "ADMITTED",
        }
        with self.assertRaises(ChemistryEngineeredDomainAdmissionError):
            validate(invalid_doc, REGISTRY)


if __name__ == "__main__":
    unittest.main()
