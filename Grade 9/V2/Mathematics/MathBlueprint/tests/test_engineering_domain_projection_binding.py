from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from compile_mathematics_engineering_workbench import load as load_engineering
from project_engineering_to_domain_registry import project_engineering_to_domain_registry
from validate_engineering_domain_projection_binding import (
    validate_projection_binding,
    validate_release_projection_binding,
)


class EngineeringDomainProjectionBindingTests(unittest.TestCase):
    CAP = "MATH-TEST-CAP"
    DIRECT = "MATH-ALG-POLYNOMIALS"

    @staticmethod
    def capability_asset(asset_id: str, subtopic_id: str, capability_ref: str, join_ref: str):
        return {
            "asset_id": asset_id,
            "asset_type": "CAPABILITY",
            "subtopic_id": subtopic_id,
            "title": "Test capability",
            "authority_class": "CORE1_SEMANTIC",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": ["GT:" + capability_ref],
            "core1_refs": [capability_ref],
            "core2_refs": [],
            "validation_refs": ["VAL:TEST"],
            "join_ref": join_ref,
            "depends_on": [],
            "payload": {
                "statement": "Use the exact test mathematical capability.",
                "prerequisite_refs": [],
                "implications": ["The capability is available to the projection binding test."],
                "boundary_notes": [],
            },
            "provenance_note": "Synthetic same-run capability for projection binding tests."
        }

    def projected(self):
        base = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "registry_id": "MATH-REG-TEST-PROJECTION-BINDING",
            "run_ref": "RUN-TEST-PROJECTION-BINDING",
            "source_manifest_refs": ["GT-TEST-PROJECTION-BINDING"],
            "join_refs": ["JOIN:TEST:PROJECTION:BINDING"],
            "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
            "assets": [self.capability_asset(
                "REG-MATH-CAP-TESTPROJECTIONBINDING",
                "SUB-TEST-PROJECTION-BINDING",
                self.CAP,
                "JOIN:TEST:PROJECTION:BINDING",
            )],
        }
        engineering = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
        coverage = {
            "crosswalk_id": "MATH-ENG-XWALK-TEST-BINDING",
            "capability_gate_map": {self.CAP: [self.DIRECT]},
            "bucket_gate_map": [{
                "bucket_id": "BUCKET-TEST",
                "capability_refs": [self.CAP],
                "engineering_gate_ids": [self.DIRECT],
                "engineering_gap_capability_refs": [],
            }],
        }
        registry, receipt = project_engineering_to_domain_registry(
            base,
            engineering_registry=engineering,
            projection_coverage=coverage,
            bucket_plan={"buckets": [{"bucket_id": "BUCKET-TEST", "member_capability_refs": [self.CAP]}]},
            bucket_sid={"BUCKET-TEST": "SUB-TEST-PROJECTION-BINDING"},
            core2_pages=[{"question_ref": "QTEST", "capability_refs": [self.CAP]}],
        )
        return registry, receipt, engineering, coverage

    def release_context(self, registry, receipt, coverage):
        summary = {
            "engineering_domain_projection_ref": receipt["projection_id"],
            "engineering_domain_projection_digest": receipt["projection_digest"],
            "engineering_domain_projected_asset_count": receipt["projected_asset_count"],
            "engineering_domain_transitive_gate_count": len(receipt["transitive_gate_ids"]),
            "registry_ref": registry["registry_id"],
            "registry_asset_count": len(registry["assets"]),
            "engineering_crosswalk_ref": receipt["crosswalk_ref"],
            "engineering_projection_coverage": {
                "required_engineering_gate_ids": list(receipt["direct_gate_ids"]),
                "engineering_registry_digest": receipt["engineering_registry_digest"],
            },
            "release_gate": {"status": "PASS", "coverage": {"asset_count": len(registry["assets"])}},
        }
        full = copy.deepcopy(coverage)
        full["required_engineering_gate_ids"] = list(receipt["direct_gate_ids"])
        full["engineering_registry_digest"] = receipt["engineering_registry_digest"]
        return summary, full

    def test_valid_projection_receipt_recomputes_every_asset(self):
        registry, receipt, engineering, _ = self.projected()
        result = validate_projection_binding(registry, receipt, engineering)
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(result["prerequisite_projection_count"], 0)
        self.assertGreater(result["projected_asset_count"], 0)

    def test_asset_digest_tamper_fails_closed(self):
        registry, receipt, engineering, _ = self.projected()
        bad = copy.deepcopy(receipt)
        bad["asset_projections"][0]["asset_digest"] = "0" * 64
        from project_engineering_to_domain_registry import digest
        bad["projection_digest"] = digest({k: v for k, v in bad.items() if k != "projection_digest"})
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_ASSET_DIGEST_MISMATCH"):
            validate_projection_binding(registry, bad, engineering)

    def test_registry_leaf_asset_removal_hits_projection_custody_gate(self):
        registry, receipt, engineering, _ = self.projected()
        bad_registry = copy.deepcopy(registry)
        by_id = {row["asset_id"]: row for row in bad_registry["assets"]}
        target = next(
            row["asset_id"] for row in receipt["asset_projections"]
            if by_id[row["asset_id"]]["asset_type"] == "VERIFICATION_RULE"
        )
        bad_registry["assets"] = [x for x in bad_registry["assets"] if x["asset_id"] != target]
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_TOTAL_ASSET_COUNT_DRIFT"):
            validate_projection_binding(bad_registry, receipt, engineering)

    def test_release_summary_count_drift_fails_closed(self):
        registry, receipt, engineering, coverage = self.projected()
        summary, full = self.release_context(registry, receipt, coverage)
        summary["engineering_domain_projected_asset_count"] += 1
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_SUMMARY_BINDING_DRIFT"):
            validate_release_projection_binding(registry, receipt, summary, full, engineering)

    def test_release_binding_passes_exact_direct_and_transitive_custody(self):
        registry, receipt, engineering, coverage = self.projected()
        summary, full = self.release_context(registry, receipt, coverage)
        result = validate_release_projection_binding(registry, receipt, summary, full, engineering)
        self.assertEqual(result["release_binding"], "PASS")
        self.assertEqual(result["direct_gate_count"], 1)
        self.assertGreater(result["transitive_gate_count"], result["direct_gate_count"])

    def test_same_gate_can_be_direct_in_one_scope_and_prerequisite_in_another(self):
        cap_poly = "MATH-TEST-POLY"
        cap_rad = "MATH-TEST-RAD"
        sid_poly = "SUB-TEST-POLY"
        sid_rad = "SUB-TEST-RAD"
        join_poly = "JOIN:TEST:POLY"
        join_rad = "JOIN:TEST:RAD"
        base = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "registry_id": "MATH-REG-TEST-MIXED-GATE-ROLE",
            "run_ref": "RUN-TEST-MIXED-GATE-ROLE",
            "source_manifest_refs": ["GT-TEST-MIXED-GATE-ROLE"],
            "join_refs": [join_poly, join_rad],
            "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
            "assets": [
                self.capability_asset("REG-MATH-CAP-TESTPOLY", sid_poly, cap_poly, join_poly),
                self.capability_asset("REG-MATH-CAP-TESTRAD", sid_rad, cap_rad, join_rad),
            ],
        }
        engineering = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
        direct_poly = "MATH-ALG-POLYNOMIALS"
        direct_rad = "MATH-NUM-RADICALS"
        coverage = {
            "crosswalk_id": "MATH-ENG-XWALK-TEST-MIXED-ROLE",
            "capability_gate_map": {cap_poly: [direct_poly], cap_rad: [direct_rad]},
            "bucket_gate_map": [
                {"bucket_id": "B-POLY", "capability_refs": [cap_poly], "engineering_gate_ids": [direct_poly], "engineering_gap_capability_refs": []},
                {"bucket_id": "B-RAD", "capability_refs": [cap_rad], "engineering_gate_ids": [direct_rad], "engineering_gap_capability_refs": []},
            ],
        }
        registry, receipt = project_engineering_to_domain_registry(
            base,
            engineering_registry=engineering,
            projection_coverage=coverage,
            bucket_plan={"buckets": [
                {"bucket_id": "B-POLY", "member_capability_refs": [cap_poly]},
                {"bucket_id": "B-RAD", "member_capability_refs": [cap_rad]},
            ]},
            bucket_sid={"B-POLY": sid_poly, "B-RAD": sid_rad},
            core2_pages=[
                {"question_ref": "QPOLY", "capability_refs": [cap_poly]},
                {"question_ref": "QRAD", "capability_refs": [cap_rad]},
            ],
        )
        radical_roles = {
            (row["subtopic_id"], row["engineering_gate_role"])
            for row in receipt["asset_projections"]
            if row["engineering_gate_id"] == direct_rad
        }
        self.assertIn((sid_poly, "PREREQUISITE_CLOSURE"), radical_roles)
        self.assertIn((sid_rad, "DIRECT"), radical_roles)

        summary, full = self.release_context(registry, receipt, coverage)
        result = validate_release_projection_binding(registry, receipt, summary, full, engineering)
        self.assertEqual(result["release_binding"], "PASS")
        self.assertGreater(result["locally_prerequisite_projection_count"], 0)


if __name__ == "__main__":
    unittest.main()
