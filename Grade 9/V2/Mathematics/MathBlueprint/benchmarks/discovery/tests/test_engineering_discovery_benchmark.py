#!/usr/bin/env python3
"""Adversarial and Extensibility Tests for Engineering Discovery Benchmark."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCHMARK_DIR = HERE.parent
ROOT = BENCHMARK_DIR.parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from benchmark_runner import load_json, run_benchmark  # noqa: E402
from compile_mathematics_engineering_discovery import (  # noqa: E402
    MathematicsEngineeringDiscoveryError,
    discover_candidates,
    load_engineering,
    promote_explicit_selection,
    REGISTRY_REL,
    VOCABULARY_REL,
)
from compile_mathematics_engineering_workbench import (  # noqa: E402
    MathematicsEngineeringWorkbenchError,
    digest,
    resolve_manifest,
)

REGISTRY = load_engineering(REGISTRY_REL)
VOCABULARY = load_engineering(VOCABULARY_REL)
CORPUS = load_json(BENCHMARK_DIR / "corpus" / "engineering_discovery_benchmark_corpus.v1.json")


class EngineeringDiscoveryBenchmarkTests(unittest.TestCase):
    def test_rank_1_does_not_authorize_engineering_gate(self):
        """Proves Top-1 candidate ranking never grants technical authorization."""
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": "MATH-ENG-DISC-REQ-TEST_RANK1",
            "query": "Quadratic Equations, Discriminant Analysis & Vieta Relations",
            "hints": [],
            "max_candidates": 6,
        }
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertEqual(receipt["candidates"][0]["rank"], 1)
        self.assertEqual(receipt["authority"], "CANDIDATE_DISCOVERY_ONLY")
        self.assertEqual(receipt["technical_authorization"], "NOT_EVALUATED")
        self.assertEqual(receipt["publication_authorization"], "NOT_IMPLIED")
        self.assertFalse(receipt["automatic_selection"])
        self.assertTrue(receipt["requires_explicit_exact_selection"])

    def test_alias_string_sent_directly_to_exact_resolver_fails(self):
        """Proves alias phrases cannot be used as exact Engineering Gate IDs."""
        forged_request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "request_id": "MATH-ENG-REQ-FORGED_ALIAS",
            "scope_kind": "ENGINEERING_GATE",
            "scope_refs": ["Vieta relations and sum of roots"],
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "owner_decision_ref": None,
        }
        with self.assertRaises(MathematicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(forged_request, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "MATH_ENG_SCOPE_UNMAPPED")

    def test_ambiguous_query_is_not_auto_resolved(self):
        """Proves queries matching multiple candidates do not arbitrarily pick a winner."""
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": "MATH-ENG-DISC-REQ-TEST_AMBIGUOUS",
            "query": "Roots",
            "hints": [],
            "max_candidates": 6,
        }
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertGreater(receipt["candidate_count"], 1)
        self.assertFalse(receipt["automatic_selection"])
        self.assertTrue(receipt["requires_explicit_exact_selection"])

    def test_no_valid_target_query_does_not_fabricate_identity(self):
        """Proves out-of-domain query cannot fabricate an Engineering identity."""
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": "MATH-ENG-DISC-REQ-TEST_BIOLOGY",
            "query": "Photosynthesis chloroplast light dependent reaction Calvin cycle",
            "hints": [],
            "max_candidates": 6,
        }
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertEqual(receipt["authority"], "CANDIDATE_DISCOVERY_ONLY")
        self.assertEqual(receipt["technical_authorization"], "NOT_EVALUATED")
        self.assertFalse(receipt["automatic_selection"])

    def test_registry_drift_stales_prior_discovery_receipt(self):
        """Proves mutating the registry invalidates a prior discovery receipt."""
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": "MATH-ENG-DISC-REQ-TEST_DRIFT",
            "query": "Quadratic Equations",
            "hints": [],
            "max_candidates": 6,
        }
        registry = copy.deepcopy(REGISTRY)
        receipt = discover_candidates(request, registry)
        selection = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "selection_id": "MATH-ENG-DISC-SEL-DRIFT",
            "discovery_id": receipt["discovery_id"],
            "discovery_receipt_digest": digest(receipt),
            "selected_scope_kind": "ENGINEERING_GATE",
            "selected_scope_refs": [receipt["candidates"][0]["scope_ref"]],
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "explicit_selection_acknowledgement": "EXACT_IDENTITY_CONFIRMED",
        }

        # Alter registry
        tampered_registry = copy.deepcopy(REGISTRY)
        tampered_registry["subtopic_gates"][0]["learner_title"] += " (Tampered)"

        with self.assertRaises(MathematicsEngineeringDiscoveryError) as ctx:
            promote_explicit_selection(request, receipt, selection, registry=tampered_registry)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED")

    def test_vocabulary_drift_stales_prior_selection(self):
        """Proves mutating the vocabulary invalidates prior explicit selection promotion."""
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": "MATH-ENG-DISC-REQ-TEST_VOCAB_DRIFT",
            "query": "Quadratic Equations",
            "hints": [],
            "max_candidates": 6,
        }
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        selection = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "selection_id": "MATH-ENG-DISC-SEL-VOCAB_DRIFT",
            "discovery_id": receipt["discovery_id"],
            "discovery_receipt_digest": digest(receipt),
            "selected_scope_kind": "ENGINEERING_GATE",
            "selected_scope_refs": [receipt["candidates"][0]["scope_ref"]],
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "explicit_selection_acknowledgement": "EXACT_IDENTITY_CONFIRMED",
        }

        tampered_vocab = copy.deepcopy(VOCABULARY)
        tampered_vocab["entries"][0]["terms"].append({
            "phrase": "totally new vocabulary phrase",
            "term_class": "LEARNER_ALIAS"
        })

        with self.assertRaises(MathematicsEngineeringDiscoveryError) as ctx:
            promote_explicit_selection(request, receipt, selection, vocabulary_catalog=tampered_vocab)
        self.assertEqual(ctx.exception.code, "MATH_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED")

    def test_benchmark_data_cannot_carry_technical_authorization_allowed(self):
        """Proves benchmark corpus and results schema-lock authorization to NOT_EVALUATED."""
        self.assertEqual(CORPUS.get("technical_authorization"), "NOT_EVALUATED")
        self.assertEqual(CORPUS.get("publication_authorization"), "NOT_IMPLIED")
        results = run_benchmark(CORPUS)
        self.assertEqual(results.get("technical_authorization"), "NOT_EVALUATED")
        self.assertEqual(results.get("publication_authorization"), "NOT_IMPLIED")

    def test_synthetic_extensibility_allows_discovery_without_python_branching(self):
        """Proves adding synthetic gate data + vocabulary allows discovery without any Python edits."""
        synthetic_gate_id = "MATH-SYNTH-HYPERBOLIC-ROTATION"
        synthetic_registry = copy.deepcopy(REGISTRY)
        synthetic_registry["subtopic_gates"].append({
            "subtopic_id": synthetic_gate_id,
            "learner_title": "Hyperbolic Rotations and Lorentz Boosts",
            "mathematical_objective": "Understand hyperbolic rotations in Minkowski space",
            "technical_readiness": "SYNTHETIC_TEST",
            "linked_buckets": ["BUCKET-MATH-SYNTHETIC"],
            "provenance": {"source_scope": "SYNTHETIC_TEST_FIXTURE", "claim_status": "PROVISIONAL"},
            "technical_core": [],
            "mandatory_equations": [],
            "representations": [],
            "misconceptions": [],
            "problem_families": [],
        })

        synthetic_vocab = copy.deepcopy(VOCABULARY)
        synthetic_vocab["entries"].append({
            "target_scope_kind": "ENGINEERING_GATE",
            "target_scope_ref": synthetic_gate_id,
            "terms": [
                {"phrase": "lorentz boost transformation", "term_class": "TECHNICAL_TERM"},
                {"phrase": "hyperbolic rotation angle", "term_class": "TECHNICAL_TERM"},
            ]
        })

        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "discovery_request_id": "MATH-ENG-DISC-REQ-SYNTHETIC",
            "query": "lorentz boost transformation",
            "hints": [],
            "max_candidates": 6,
        }

        # Discover with synthetic data
        receipt = discover_candidates(request, registry=synthetic_registry, vocabulary_catalog=synthetic_vocab)
        self.assertGreater(receipt["candidate_count"], 0)
        self.assertEqual(receipt["candidates"][0]["scope_ref"], synthetic_gate_id)
        self.assertIn("VOCABULARY_EXACT", receipt["candidates"][0]["match_basis"])

    def test_benchmark_quantitative_recall_thresholds(self):
        """Validates quantitative benchmark targets across all 80 queries in the curated corpus."""
        output = run_benchmark(CORPUS)
        metrics = output["metrics"]
        self.assertGreaterEqual(metrics["TOTAL_QUERIES"], 80)
        self.assertGreaterEqual(metrics["TOP_1_RECALL"], 0.95, "Top-1 recall must be at least 95%")
        self.assertEqual(metrics["TOP_3_RECALL"], 1.0, "Top-3 recall must be 100%")
        self.assertEqual(metrics["TOP_5_RECALL"], 1.0, "Top-5 recall must be 100%")
        self.assertEqual(metrics["MISS_RATE"], 0.0, "Miss rate must be 0%")
        self.assertEqual(metrics["NO_VALID_TARGET_BEHAVIOR_SAFE"], True, "No-valid-target safety must pass")
        self.assertEqual(len(output["gap_records"]), 0, "No vocabulary gaps should exist in curated corpus")


if __name__ == "__main__":
    unittest.main(verbosity=2)

