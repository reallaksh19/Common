import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from proof_obligations import (
    critical_findings,
    validate_ledger,
    validate_manifest,
    validate_pair,
)


BASE = "a" * 40
CANDIDATE = "c" * 40
DIGEST = "d" * 64


def requirement(rid, method, independence):
    return {
        "id": rid,
        "method": method,
        "independence": independence,
        "oracle_ref": f"oracle://{rid}",
    }


def obligation(oid, severity, claim_type, reqs):
    return {
        "id": oid,
        "severity": severity,
        "claim": {
            "type": claim_type,
            "statement": f"Claim for {oid}",
            "subject_refs": [f"subject://{oid}"],
        },
        "source_refs": [f"source://{oid}"],
        "evidence_required": reqs,
    }


def manifest():
    return {
        "schema_version": "PROOF_OBLIGATION_MANIFEST_V1",
        "authority": "FROZEN_EXPECTATION_MANIFEST",
        "identity": {
            "task_id": "PRD-512-PROD-C5",
            "parent_ref": "issue://512",
        },
        "basis": {
            "base_ref": "main",
            "base_sha": BASE,
            "candidate_sha": CANDIDATE,
        },
        "l0": {
            "frozen": True,
            "frozen_ref": "issue://521#l0",
            "obligations": [
                obligation(
                    "L0-CRIT-1",
                    "CRITICAL",
                    "BEHAVIOR",
                    [requirement("REQ-L0-1", "PROPERTY_TEST", "PRECOMMITTED")],
                ),
            ],
        },
        "l1": {
            "baseline_ref": "baseline://main",
            "baseline_sha": BASE,
            "obligations": [
                obligation(
                    "L1-HIGH-1",
                    "HIGH",
                    "PRESERVATION",
                    [requirement("REQ-L1-1", "CONTRACT_TEST", "BASELINE_DERIVED")],
                ),
            ],
        },
        "l2": {
            "impact_ref": "impact://candidate",
            "candidate_sha": CANDIDATE,
            "obligations": [
                obligation(
                    "L2-CRIT-1",
                    "CRITICAL",
                    "IMPACT",
                    [requirement("REQ-L2-1", "STATIC_ANALYSIS", "IMPACT_DERIVED")],
                ),
            ],
        },
    }


def evidence_item(requirement_id, method):
    return {
        "requirement_id": requirement_id,
        "method": method,
        "refs": [f"evidence://{requirement_id}"],
        "verifier_kind": "DETERMINISTIC_TOOL",
        "verifier_identity": "coordinator-test",
    }


def record(oid, state, requirement_id, method, disposition_ref=None):
    items = []
    if requirement_id is not None:
        items.append(evidence_item(requirement_id, method))
    return {
        "obligation_id": oid,
        "state": state,
        "evidence_candidate_sha": CANDIDATE,
        "evidence_items": items,
        "disposition_ref": disposition_ref,
    }


def ledger():
    return {
        "schema_version": "EVIDENCE_LEDGER_V1",
        "authority": "EXACT_CANDIDATE_EVIDENCE_LEDGER",
        "manifest_ref": "manifest://proof-v1",
        "manifest_digest": DIGEST,
        "candidate_sha": CANDIDATE,
        "records": [
            record("L0-CRIT-1", "VERIFIED", "REQ-L0-1", "PROPERTY_TEST"),
            record("L1-HIGH-1", "VERIFIED", "REQ-L1-1", "CONTRACT_TEST"),
            record("L2-CRIT-1", "VERIFIED", "REQ-L2-1", "STATIC_ANALYSIS"),
        ],
    }


class ProofObligationTests(unittest.TestCase):
    def test_valid_closed_denominator_pair(self):
        self.assertEqual(validate_pair(manifest(), ledger()), [])

    def test_l1_must_bind_manifest_base_sha(self):
        value = manifest()
        value["l1"]["baseline_sha"] = "b" * 40
        errors = validate_manifest(value)
        self.assertTrue(any("baseline_sha" in error for error in errors), errors)

    def test_l2_cannot_exist_before_candidate(self):
        value = manifest()
        value["basis"]["candidate_sha"] = None
        value["l2"]["candidate_sha"] = None
        errors = validate_manifest(value)
        self.assertTrue(any("l2 obligations cannot exist" in error for error in errors), errors)

    def test_obligation_ids_are_globally_unique(self):
        value = manifest()
        value["l2"]["obligations"][0]["id"] = "L0-CRIT-1"
        errors = validate_manifest(value)
        self.assertTrue(any("globally unique" in error for error in errors), errors)

    def test_critical_obligation_requires_evidence_requirement(self):
        value = manifest()
        value["l0"]["obligations"][0]["evidence_required"] = []
        errors = validate_manifest(value)
        self.assertTrue(any("CRITICAL obligation requires" in error for error in errors), errors)

    def test_ledger_denominator_cannot_drop_obligation(self):
        m = manifest()
        l = ledger()
        l["records"] = l["records"][:-1]
        errors = validate_pair(m, l)
        self.assertTrue(any("missing obligations" in error for error in errors), errors)

    def test_ledger_denominator_cannot_add_unknown_obligation(self):
        m = manifest()
        l = ledger()
        l["records"].append(
            record("UNKNOWN-OBLIGATION", "UNKNOWN", None, "OTHER")
        )
        errors = validate_pair(m, l)
        self.assertTrue(any("unknown obligations" in error for error in errors), errors)

    def test_ledger_candidate_must_equal_manifest_candidate(self):
        l = ledger()
        l["candidate_sha"] = "e" * 40
        for row in l["records"]:
            row["evidence_candidate_sha"] = "e" * 40
        errors = validate_pair(manifest(), l)
        self.assertTrue(any("manifest candidate_sha" in error for error in errors), errors)

    def test_each_record_evidence_binds_ledger_candidate(self):
        l = ledger()
        l["records"][0]["evidence_candidate_sha"] = "e" * 40
        errors = validate_ledger(l)
        self.assertTrue(any("evidence_candidate_sha" in error for error in errors), errors)

    def test_verified_requires_all_declared_evidence_requirements(self):
        m = manifest()
        m["l0"]["obligations"][0]["evidence_required"].append(
            requirement("REQ-L0-2", "FAULT_INJECTION", "PRECOMMITTED")
        )
        errors = validate_pair(m, ledger())
        self.assertTrue(any("VERIFIED without required evidence coverage" in error for error in errors), errors)

    def test_evidence_method_must_match_declared_requirement(self):
        l = ledger()
        l["records"][0]["evidence_items"][0]["method"] = "UNIT_TEST"
        errors = validate_pair(manifest(), l)
        self.assertTrue(any("expects method PROPERTY_TEST" in error for error in errors), errors)

    def test_evidence_cannot_claim_undeclared_requirement(self):
        l = ledger()
        l["records"][0]["evidence_items"][0]["requirement_id"] = "REQ-FAKE"
        errors = validate_pair(manifest(), l)
        self.assertTrue(any("undeclared requirement" in error for error in errors), errors)

    def test_not_applicable_requires_disposition(self):
        l = ledger()
        l["records"][1] = record(
            "L1-HIGH-1",
            "NOT_APPLICABLE",
            None,
            "OTHER",
            disposition_ref=None,
        )
        errors = validate_ledger(l)
        self.assertTrue(any("NOT_APPLICABLE requires disposition_ref" in error for error in errors), errors)

    def test_unknown_critical_remains_visible_to_execution_kernel(self):
        l = ledger()
        l["records"][2] = record(
            "L2-CRIT-1",
            "UNKNOWN",
            None,
            "OTHER",
        )
        self.assertEqual(validate_pair(manifest(), l), [])
        findings = critical_findings(manifest(), l)
        self.assertEqual(findings, [{
            "id": "L2-CRIT-1",
            "state": "UNKNOWN",
            "evidence_refs": [],
        }])

    def test_refuted_critical_projects_evidence(self):
        l = ledger()
        l["records"][0] = record(
            "L0-CRIT-1",
            "REFUTED",
            "REQ-L0-1",
            "PROPERTY_TEST",
        )
        self.assertEqual(validate_pair(manifest(), l), [])
        findings = critical_findings(manifest(), l)
        self.assertEqual(findings[0]["state"], "REFUTED")
        self.assertEqual(findings[0]["evidence_refs"], ["evidence://REQ-L0-1"])

    def test_schema_rejects_aggregate_pass_field(self):
        value = ledger()
        value["pass"] = True
        errors = validate_ledger(value)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors), errors)

    def test_schema_rejects_reviewer_confidence_as_authority(self):
        value = manifest()
        value["reviewer_confidence"] = 0.99
        errors = validate_manifest(value)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
