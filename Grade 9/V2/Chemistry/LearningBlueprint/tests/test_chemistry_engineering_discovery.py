#!/usr/bin/env python3
"""Tests for Chemistry Engineering Discovery Compiler & Selection Protocol."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_discovery import (  # noqa: E402
    ChemistryEngineeringDiscoveryError,
    digest,
    discover_candidates,
    load_engineering,
    promote_explicit_selection,
    validate_discovery_vocabulary_catalog,
)

REGISTRY = load_engineering("policies/chemistry-technical-engineering-gates.v1.json")
VOCABULARY = json.loads((ROOT / "policies/chemistry-engineering-discovery-vocabulary.v1.json").read_text(encoding="utf-8"))


def discovery_request(query: str, suffix: str = "1", hints: list[str] | None = None, kinds: list[str] | None = None) -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "discovery_request_id": f"CHEM-ENG-DISC-REQ-TEST-{suffix}",
        "query": query,
        "hints": hints or [],
        "candidate_kinds": kinds or ["ENGINEERING_GATE", "BUCKET"],
        "max_candidates": 6,
    }


class ChemistryEngineeringDiscoveryTests(unittest.TestCase):
    def test_vocabulary_validation_passes(self):
        res = validate_discovery_vocabulary_catalog(VOCABULARY, REGISTRY)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["entry_count"], 52)
        self.assertGreater(res["term_count"], 300)

    def test_discovery_is_ranked_but_non_authoritative(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "NONAUTH", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY), copy.deepcopy(VOCABULARY))
        self.assertGreater(receipt["candidate_count"], 0)
        self.assertEqual(receipt["candidates"][0]["scope_ref"], target["subtopic_id"])
        self.assertEqual(receipt["authority"], "CANDIDATE_DISCOVERY_ONLY")
        self.assertEqual(receipt["technical_authorization"], "NOT_EVALUATED")
        self.assertFalse(receipt["automatic_selection"])
        self.assertTrue(receipt["requires_explicit_exact_selection"])

    def test_discovery_recalls_grade9_matter_states(self):
        req = discovery_request("kinetic particle theory solid liquid gas", "G9-MATTER")
        receipt = discover_candidates(req, REGISTRY, VOCABULARY)
        top = receipt["candidates"][0]
        self.assertEqual(top["scope_ref"], "CHEM-MATTER-STATES")

    def test_discovery_recalls_grade10_balancing(self):
        req = discovery_request("balancing chemical equations conservation of mass", "G10-BAL")
        receipt = discover_candidates(req, REGISTRY, VOCABULARY)
        top = receipt["candidates"][0]
        self.assertEqual(top["scope_ref"], "CHEM-EQ-BALANCING")

    def test_discovery_recalls_grade11_thermo_gibbs(self):
        req = discovery_request("gibbs free energy delta G spontaneity", "G11-GIBBS")
        receipt = discover_candidates(req, REGISTRY, VOCABULARY)
        top = receipt["candidates"][0]
        self.assertEqual(top["scope_ref"], "CHEM-THERMO-GIBBS-SPONTANEITY")

    def test_discovery_recalls_grade11_vsepr_geometry(self):
        req = discovery_request("vsepr theory molecular shapes steric number", "G11-VSEPR")
        receipt = discover_candidates(req, REGISTRY, VOCABULARY)
        top = receipt["candidates"][0]
        self.assertEqual(top["scope_ref"], "CHEM-BOND-VSEPR-GEOMETRY")

    def test_explicit_selection_promotion(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "SEL-PROMO", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, REGISTRY, VOCABULARY)
        selection = {
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "selection_id": "CHEM-ENG-DISC-SEL-TEST-1",
            "discovery_id": receipt["discovery_id"],
            "discovery_receipt_digest": digest(receipt),
            "selected_scope_kind": "ENGINEERING_GATE",
            "selected_scope_refs": [target["subtopic_id"]],
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "explicit_selection_acknowledgement": "EXACT_IDENTITY_CONFIRMED",
        }
        res = promote_explicit_selection(selection, request, receipt, REGISTRY, VOCABULARY)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["technical_authorization"], "ALLOWED_FOR_DOWNSTREAM_MANIFEST")

    def test_unlisted_selection_id_rejected(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "UNLISTED", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, REGISTRY, VOCABULARY)
        selection = {
            "schema_version": "1.0.0",
            "subject": "CHEMISTRY",
            "selection_id": "CHEM-ENG-DISC-SEL-TEST-2",
            "discovery_id": receipt["discovery_id"],
            "discovery_receipt_digest": digest(receipt),
            "selected_scope_kind": "ENGINEERING_GATE",
            "selected_scope_refs": ["CHEM-UNKNOWN-GATE-999"],
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "explicit_selection_acknowledgement": "EXACT_IDENTITY_CONFIRMED",
        }
        with self.assertRaises(ChemistryEngineeringDiscoveryError):
            promote_explicit_selection(selection, request, receipt, REGISTRY, VOCABULARY)


if __name__ == "__main__":
    unittest.main()
