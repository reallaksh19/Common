#!/usr/bin/env python3
"""Tests for Chemistry Engineering Workbench Registry Proof & Manifest Resolution."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_workbench import (  # noqa: E402
    REGISTRY_REL,
    compile_registry_proof,
    load,
    resolve_manifest,
)

REGISTRY = load(REGISTRY_REL)


class ChemistryEngineeringWorkbenchTests(unittest.TestCase):
    def test_registry_contains_all_52_gates(self):
        self.assertEqual(len(REGISTRY["subtopic_gates"]), 52)

    def test_manifest_resolves_transitive_prerequisites(self):
        target = next(g for g in REGISTRY["subtopic_gates"] if g["subtopic_id"] == "CHEM-CALC-STOICHIOMETRY")
        req = {
            "schema_version": "2.0.0",
            "request_id": "CHEM-ENG-REQ-TEST-RES",
            "subject": "CHEMISTRY",
            "requested_topic": target["learner_title"],
            "requested_scope": f"Gate {target['subtopic_id']}",
            "engineering_depth": "STANDARD",
            "requested_action": "DECLARE_DIRECT_GATES",
            "requested_for": ["CDAU", "PAL"],
        }
        man = resolve_manifest(req, REGISTRY, gate_id=target["subtopic_id"])
        self.assertEqual(man["required_gate_ids"], ["CHEM-CALC-STOICHIOMETRY"])
        self.assertEqual(man["scope_ref"], "CHEM-CALC-STOICHIOMETRY")

    def test_registry_proof_all_52_gates_ready(self):
        proof = compile_registry_proof(REGISTRY)
        self.assertEqual(proof["gate_count"], 52)
        self.assertEqual(proof["ready_gate_count"], 52)
        self.assertEqual(proof["blocked_gate_ids"], [])
        self.assertTrue(proof["all_registry_gates_blueprint_admissible"])


if __name__ == "__main__":
    unittest.main()
