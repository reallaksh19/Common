import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evidence_gate import (
    canonical_manifest_digest,
    gate_decision,
    validate_gate_result,
    validate_review_context,
)


BASE = "a" * 40
CANDIDATE = "c" * 40


def manifest():
    return {
        "schema_version": "PROOF_OBLIGATION_MANIFEST_V1",
        "authority": "FROZEN_EXPECTATION_MANIFEST",
        "identity": {
            "task_id": "PRD-512-PROD-C6",
            "parent_ref": "issue://512",
        },
        "basis": {
            "base_ref": "main",
            "base_sha": BASE,
            "candidate_sha": CANDIDATE,
        },
        "l0": {
            "frozen": True,
            "frozen_ref": "issue://523#l0",
            "obligations": [{
                "id": "L0-1",
                "severity": "CRITICAL",
                "claim": {
                    "type": "BEHAVIOR",
                    "statement": "The intended observable behavior holds.",
                    "subject_refs": ["task://observable"],
                },
                "source_refs": ["issue://523"],
                "evidence_required": [{
                    "id": "REQ-L0-1",
                    "method": "PROPERTY_TEST",
                    "independence": "PRECOMMITTED",
                    "oracle_ref": "oracle://L0-1",
                }],
            }],
        },
        "l1": {
            "baseline_ref": "baseline://main",
            "baseline_sha": BASE,
            "obligations": [],
        },
        "l2": {
            "impact_ref": "impact://candidate",
            "candidate_sha": CANDIDATE,
            "obligations": [],
        },
    }


def ledger(m, state="VERIFIED"):
    digest = canonical_manifest_digest(m)
    items = []
    if state in {"VERIFIED", "REFUTED"}:
        items = [{
            "requirement_id": "REQ-L0-1",
            "method": "PROPERTY_TEST",
            "refs": ["evidence://property-test"],
            "verifier_kind": "DETERMINISTIC_TOOL",
            "verifier_identity": "property-runner",
        }]
    return {
        "schema_version": "EVIDENCE_LEDGER_V1",
        "authority": "EXACT_CANDIDATE_EVIDENCE_LEDGER",
        "manifest_ref": "manifest://prod-c6",
        "manifest_digest": digest,
        "candidate_sha": CANDIDATE,
        "records": [{
            "obligation_id": "L0-1",
            "state": state,
            "evidence_candidate_sha": CANDIDATE,
            "evidence_items": items,
            "disposition_ref": None,
        }],
    }


def review_context(m, l, *, kind="SAME_PRINCIPAL_FRESH_CONTEXT", independence="DEGRADED"):
    return {
        "schema_version": "REVIEW_CONTEXT_V1",
        "authority": "FRESH_REVIEW_CONTEXT",
        "candidate_sha": CANDIDATE,
        "manifest_ref": l["manifest_ref"],
        "manifest_digest": canonical_manifest_digest(m),
        "reviewer": {
            "kind": kind,
            "identity": "reviewer://fresh-1",
            "principal_independence": independence,
            "fresh_context": True,
        },
        "context_policy": {
            "original_task_ref": "issue://523",
            "base_sha": BASE,
            "candidate_sha": CANDIDATE,
            "repository_context_refs": ["repo://base", "repo://candidate"],
            "candidate_visible_in_phase_a": False,
            "generated_tests_visible_in_phase_a": False,
            "coder_reasoning_included": False,
            "coder_confidence_included": False,
            "prior_self_review_included": False,
            "implementation_rationale_included": False,
            "candidate_visible_in_phase_b": True,
        },
        "tool_access": ["repository", "tests", "static-analysis"],
    }


class EvidenceGateTests(unittest.TestCase):
    def test_closed_verified_denominator_is_advance_eligible(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        result = gate_decision(m, l, ctx)
        self.assertEqual(result["decision"], "ADVANCE_ELIGIBLE")
        self.assertEqual(result["reason_codes"], ["CLOSED_DENOMINATOR"])
        self.assertEqual(validate_gate_result(result), [])

    def test_refuted_obligation_requires_repair(self):
        m = manifest()
        l = ledger(m, state="REFUTED")
        ctx = review_context(m, l)
        result = gate_decision(m, l, ctx)
        self.assertEqual(result["decision"], "REPAIR")
        self.assertEqual(result["blocking_obligations"], ["L0-1"])

    def test_unknown_obligation_requires_escalation(self):
        m = manifest()
        l = ledger(m, state="UNKNOWN")
        ctx = review_context(m, l)
        result = gate_decision(m, l, ctx)
        self.assertEqual(result["decision"], "ESCALATE")
        self.assertEqual(result["blocking_obligations"], ["L0-1"])

    def test_candidate_mismatch_requires_evidence_replay(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        l["candidate_sha"] = "e" * 40
        l["records"][0]["evidence_candidate_sha"] = "e" * 40
        result = gate_decision(m, l, ctx)
        self.assertEqual(result["decision"], "REPLAY_EVIDENCE")
        self.assertTrue(result["validation_errors"])

    def test_claimed_manifest_digest_must_match_actual_manifest(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        l["manifest_digest"] = "f" * 64
        ctx["manifest_digest"] = "f" * 64
        result = gate_decision(m, l, ctx)
        self.assertEqual(result["decision"], "REPLAY_EVIDENCE")
        self.assertTrue(
            any("canonical manifest" in error for error in result["validation_errors"]),
            result,
        )

    def test_same_principal_context_cannot_claim_distinct_independence(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l, independence="DISTINCT")
        result = gate_decision(m, l, ctx)
        self.assertEqual(result["decision"], "REPLAY_EVIDENCE")
        self.assertTrue(
            any("DEGRADED independence" in error for error in result["validation_errors"]),
            result,
        )

    def test_distinct_principal_must_claim_distinct_independence(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(
            m,
            l,
            kind="DISTINCT_PRINCIPAL",
            independence="UNKNOWN",
        )
        errors = validate_review_context(ctx)
        self.assertTrue(any("DISTINCT principal independence" in error for error in errors), errors)

    def test_phase_a_cannot_see_candidate(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        ctx["context_policy"]["candidate_visible_in_phase_a"] = True
        errors = validate_review_context(ctx)
        self.assertTrue(any("False was expected" in error for error in errors), errors)

    def test_phase_a_cannot_see_generated_tests(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        ctx["context_policy"]["generated_tests_visible_in_phase_a"] = True
        errors = validate_review_context(ctx)
        self.assertTrue(any("False was expected" in error for error in errors), errors)

    def test_coder_reasoning_is_structurally_excluded(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        ctx["context_policy"]["coder_reasoning_included"] = True
        errors = validate_review_context(ctx)
        self.assertTrue(any("False was expected" in error for error in errors), errors)

    def test_gate_schema_has_no_pass_outcome(self):
        m = manifest()
        l = ledger(m)
        ctx = review_context(m, l)
        result = gate_decision(m, l, ctx)
        result["decision"] = "PASS"
        errors = validate_gate_result(result)
        self.assertTrue(any("is not one of" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
