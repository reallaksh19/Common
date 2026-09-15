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

    def projected(self):
        base = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "registry_id": "MATH-REG-TEST-PROJECTION-BINDING",
            "run_ref": "RUN-TEST-PROJECTION-BINDING",
            "source_manifest_refs": ["GT-TEST-PROJECTION-BINDING"],
            "join_refs": ["JOIN:TEST:PROJECTION:BINDING"],
            "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
            "assets": [{
                "asset_id": "REG-MATH-CAP-TESTPROJECTIONBINDING",
                "asset_type": "CAPABILITY",
                "subtopic_id": "SUB-TEST-PROJECTION-BINDING",
                "title": "Test capability",
                "authority_class": "CORE1_SEMANTIC",
                "admission_status": "ADMITTED",
                "confidence": "HIGH",
                "ground_truth_refs": ["GT:" + self.CAP],
                "core1_refs": [self.CAP],
                "core2_refs": [],
                "validation_refs": ["VAL:TEST"],
                "join_ref": "JOIN:TEST:PROJECTION:BINDING",
                "depends_on": [],
                "payload": {
                    "statement": "Use the exact test mathematical capability.",
                    "prerequisite_refs": [],
                    "implications": ["The capability is available to the projection binding test."],
                    "boundary_notes": [],
                },
                "provenance_note": "Synthetic same-run capability for projection binding tests."
            }]
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
        return registry, receipt

    def release_context(self, registry, receipt):
        summary = {
            "engineering_domain_projection_ref": receipt["projection_id"],
            "engineering_domain_projection_digest": receipt["projection_digest"],
            "engineering_domain_projected_asset_count": receipt["projected_asset_count"],
            "engineering_domain_transitive_gate_count": len(receipt["transitive_gate_ids"]),
            "registry_ref": registry["registry_id"],
            "registry_asset_count": len(registry["assets"]),
            "engineering_crosswalk_ref": receipt["crosswalk_ref"],
            "engineering_projection_coverage": {
                "required_engineering_gate_ids": [self.DIRECT],
                "engineering_registry_digest": receipt["engineering_registry_digest"],
            },
            "release_gate": {"status": "PASS", "coverage": {"asset_count": len(registry["assets"])}},
        }
        full = {
            "required_engineering_gate_ids": [self.DIRECT],
            "engineering_registry_digest": receipt["engineering_registry_digest"],
            "crosswalk_id": receipt["crosswalk_ref"],
        }
        return summary, full

    def test_valid_projection_receipt_recomputes_every_asset(self):
        registry, receipt = self.projected()
        result = validate_projection_binding(registry, receipt)
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(result["prerequisite_projection_count"], 0)
        self.assertGreater(result["projected_asset_count"], 0)

    def test_asset_digest_tamper_fails_closed(self):
        registry, receipt = self.projected()
        bad = copy.deepcopy(receipt)
        bad["asset_projections"][0]["asset_digest"] = "0" * 64
        from project_engineering_to_domain_registry import digest
        bad["projection_digest"] = digest({k: v for k, v in bad.items() if k != "projection_digest"})
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_ASSET_DIGEST_MISMATCH"):
            validate_projection_binding(registry, bad)

    def test_registry_leaf_asset_removal_hits_projection_custody_gate(self):
        registry, receipt = self.projected()
        bad_registry = copy.deepcopy(registry)
        by_id = {row["asset_id"]: row for row in bad_registry["assets"]}
        target = next(
            row["asset_id"] for row in receipt["asset_projections"]
            if by_id[row["asset_id"]]["asset_type"] == "VERIFICATION_RULE"
        )
        bad_registry["assets"] = [x for x in bad_registry["assets"] if x["asset_id"] != target]
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_TOTAL_ASSET_COUNT_DRIFT"):
            validate_projection_binding(bad_registry, receipt)

    def test_release_summary_count_drift_fails_closed(self):
        registry, receipt = self.projected()
        summary, full = self.release_context(registry, receipt)
        summary["engineering_domain_projected_asset_count"] += 1
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_SUMMARY_BINDING_DRIFT"):
            validate_release_projection_binding(registry, receipt, summary, full)

    def test_release_binding_passes_exact_direct_and_transitive_custody(self):
        registry, receipt = self.projected()
        summary, full = self.release_context(registry, receipt)
        result = validate_release_projection_binding(registry, receipt, summary, full)
        self.assertEqual(result["release_binding"], "PASS")
        self.assertEqual(result["direct_gate_count"], 1)
        self.assertGreater(result["transitive_gate_count"], result["direct_gate_count"])


if __name__ == "__main__":
    unittest.main()
