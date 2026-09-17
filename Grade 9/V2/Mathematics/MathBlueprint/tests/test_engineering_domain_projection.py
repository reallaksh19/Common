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
from validate_canonical_domain_registry import validate_registry


class EngineeringDomainProjectionTests(unittest.TestCase):
    def base_registry(self, capability_ref="MATH-TEST-CAP"):
        return {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "registry_id": "MATH-REG-TEST-PROJECTION",
            "run_ref": "RUN-TEST-PROJECTION",
            "source_manifest_refs": ["GT-TEST-PROJECTION"],
            "join_refs": ["JOIN:TEST:PROJECTION"],
            "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
            "assets": [
                {
                    "asset_id": "REG-MATH-CAP-TESTPROJECTION",
                    "asset_type": "CAPABILITY",
                    "subtopic_id": "SUB-TEST-PROJECTION",
                    "title": "Test capability",
                    "authority_class": "CORE1_SEMANTIC",
                    "admission_status": "ADMITTED",
                    "confidence": "HIGH",
                    "ground_truth_refs": ["GT:" + capability_ref],
                    "core1_refs": [capability_ref],
                    "core2_refs": [],
                    "validation_refs": ["VAL:TEST"],
                    "join_ref": "JOIN:TEST:PROJECTION",
                    "depends_on": [],
                    "payload": {
                        "statement": "Use the exact test mathematical capability.",
                        "prerequisite_refs": [],
                        "implications": ["The capability is available to the projection test."],
                        "boundary_notes": [],
                    },
                    "provenance_note": "Synthetic same-run capability used only for projector contract tests."
                }
            ]
        }

    def project(self, direct_gate="MATH-GEO-EUCLID-FOUNDATIONS"):
        cap = "MATH-TEST-CAP"
        base = self.base_registry(cap)
        engineering = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
        coverage = {
            "crosswalk_id": "MATH-ENG-XWALK-TEST",
            "capability_gate_map": {cap: [direct_gate]},
            "bucket_gate_map": [
                {
                    "bucket_id": "BUCKET-TEST",
                    "capability_refs": [cap],
                    "engineering_gate_ids": [direct_gate],
                    "engineering_gap_capability_refs": []
                }
            ]
        }
        bucket_plan = {
            "buckets": [
                {"bucket_id": "BUCKET-TEST", "member_capability_refs": [cap]}
            ]
        }
        pages = [
            {"question_ref": "QTEST", "capability_refs": [cap]}
        ]
        return project_engineering_to_domain_registry(
            base,
            engineering_registry=engineering,
            projection_coverage=coverage,
            bucket_plan=bucket_plan,
            bucket_sid={"BUCKET-TEST": "SUB-TEST-PROJECTION"},
            core2_pages=pages,
        )

    def test_euclid_projects_rich_typed_assets_with_exact_provenance(self):
        registry, receipt = self.project()
        validate_registry(registry)
        kinds = {row["asset_type"] for row in registry["assets"]}
        self.assertTrue({
            "CONCEPT", "MODEL", "EQUATION", "REPRESENTATION", "LEARNING_ATOM",
            "MISCONCEPTION", "VERIFICATION_RULE", "PROBLEM_FAMILY"
        }.issubset(kinds))
        self.assertGreater(receipt["projected_asset_count"], 0)
        self.assertEqual(receipt["direct_gate_ids"], ["MATH-GEO-EUCLID-FOUNDATIONS"])
        for row in receipt["asset_projections"]:
            self.assertEqual(row["engineering_gate_id"], "MATH-GEO-EUCLID-FOUNDATIONS")
            self.assertEqual(row["capability_refs"], ["MATH-TEST-CAP"])
            self.assertIn("QTEST", row["core2_refs"] if row["engineering_source_kind"] != "PROBLEM_FAMILY" else row["core2_refs"])

    def test_prerequisite_closure_is_projected_not_only_direct_gate(self):
        registry, receipt = self.project("MATH-ALG-POLYNOMIALS")
        validate_registry(registry)
        self.assertIn("MATH-ALG-POLYNOMIALS", receipt["direct_gate_ids"])
        self.assertIn("MATH-NUM-RADICALS", receipt["transitive_gate_ids"])
        roles = {
            (row["engineering_gate_id"], row["engineering_gate_role"])
            for row in receipt["asset_projections"]
        }
        self.assertIn(("MATH-ALG-POLYNOMIALS", "DIRECT"), roles)
        self.assertIn(("MATH-NUM-RADICALS", "PREREQUISITE_CLOSURE"), roles)

    def test_unknown_gate_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_ENGINEERING_GATE_UNKNOWN"):
            self.project("MATH-NOT-A-REAL-GATE")

    def test_missing_capability_asset_fails_closed(self):
        registry, _ = self.project()
        self.assertTrue(registry)
        base = self.base_registry("MATH-OTHER-CAP")
        engineering = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
        coverage = {
            "crosswalk_id": "MATH-ENG-XWALK-TEST",
            "capability_gate_map": {"MATH-TEST-CAP": ["MATH-GEO-EUCLID-FOUNDATIONS"]},
            "bucket_gate_map": [{
                "bucket_id": "BUCKET-TEST", "capability_refs": ["MATH-TEST-CAP"],
                "engineering_gate_ids": ["MATH-GEO-EUCLID-FOUNDATIONS"],
                "engineering_gap_capability_refs": []
            }]
        }
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_CAPABILITY_ASSET_MISSING"):
            project_engineering_to_domain_registry(
                base,
                engineering_registry=engineering,
                projection_coverage=coverage,
                bucket_plan={"buckets": [{"bucket_id": "BUCKET-TEST", "member_capability_refs": ["MATH-TEST-CAP"]}]},
                bucket_sid={"BUCKET-TEST": "SUB-TEST-PROJECTION"},
                core2_pages=[],
            )


if __name__ == "__main__":
    unittest.main()
