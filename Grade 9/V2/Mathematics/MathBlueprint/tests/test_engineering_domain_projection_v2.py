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
from project_engineering_to_domain_registry import digest
from project_engineering_to_domain_registry_v2 import project_engineering_to_domain_registry_v2
from validate_engineering_domain_projection_binding_v2 import validate_projection_binding_v2


class EngineeringDomainProjectionV2Tests(unittest.TestCase):
    RAD = "MATH-NUM-RADICALS"
    POLY = "MATH-ALG-POLYNOMIALS"
    CAP_R = "MATH-TEST-RADICAL-CAP"
    CAP_P = "MATH-TEST-POLY-CAP"

    def fixture(self):
        base = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "registry_id": "MATH-REG-TEST-CANONICAL-PROJECTION",
            "run_ref": "RUN-TEST-CANONICAL-PROJECTION",
            "source_manifest_refs": ["GT-TEST-CANONICAL-PROJECTION"],
            "join_refs": ["JOIN:RAD", "JOIN:POLY"],
            "admission_policy_ref": "MATH-CANONICAL-DOMAIN-REGISTRY-v1",
            "assets": [
                self.capability_asset("REG-MATH-CAP-TESTRADICAL", "SUB-RAD", "JOIN:RAD", self.CAP_R),
                self.capability_asset("REG-MATH-CAP-TESTPOLY", "SUB-POLY", "JOIN:POLY", self.CAP_P),
            ],
        }
        engineering = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
        coverage = {
            "crosswalk_id": "MATH-ENG-XWALK-TEST-CANONICAL",
            "capability_gate_map": {
                self.CAP_R: [self.RAD],
                self.CAP_P: [self.POLY],
            },
            "bucket_gate_map": [
                {
                    "bucket_id": "BUCKET-RAD",
                    "capability_refs": [self.CAP_R],
                    "engineering_gate_ids": [self.RAD],
                    "engineering_gap_capability_refs": [],
                },
                {
                    "bucket_id": "BUCKET-POLY",
                    "capability_refs": [self.CAP_P],
                    "engineering_gate_ids": [self.POLY],
                    "engineering_gap_capability_refs": [],
                },
            ],
        }
        registry, receipt = project_engineering_to_domain_registry_v2(
            base,
            engineering_registry=engineering,
            projection_coverage=coverage,
            bucket_plan={
                "buckets": [
                    {"bucket_id": "BUCKET-RAD", "member_capability_refs": [self.CAP_R]},
                    {"bucket_id": "BUCKET-POLY", "member_capability_refs": [self.CAP_P]},
                ]
            },
            bucket_sid={"BUCKET-RAD": "SUB-RAD", "BUCKET-POLY": "SUB-POLY"},
            core2_pages=[
                {"question_ref": "QR", "capability_refs": [self.CAP_R]},
                {"question_ref": "QP", "capability_refs": [self.CAP_P]},
            ],
        )
        return registry, receipt, engineering, coverage

    @staticmethod
    def capability_asset(asset_id, sid, join_ref, cap):
        return {
            "asset_id": asset_id,
            "asset_type": "CAPABILITY",
            "subtopic_id": sid,
            "title": "Synthetic exact capability",
            "authority_class": "CORE1_SEMANTIC",
            "admission_status": "ADMITTED",
            "confidence": "HIGH",
            "ground_truth_refs": ["GT:" + cap],
            "core1_refs": [cap],
            "core2_refs": [],
            "validation_refs": ["VAL:TEST"],
            "join_ref": join_ref,
            "depends_on": [],
            "payload": {
                "statement": "Use the exact synthetic mathematical capability in its declared scope.",
                "prerequisite_refs": [],
                "implications": ["The capability is available to the canonicalization test."],
                "boundary_notes": [],
            },
            "provenance_note": "Synthetic same-run capability for canonical Engineering projection tests.",
        }

    @staticmethod
    def reseal(receipt):
        receipt["projection_digest"] = digest({k: v for k, v in receipt.items() if k != "projection_digest"})

    def test_same_engineering_source_is_one_asset_with_multiple_memberships(self):
        registry, receipt, engineering, coverage = self.fixture()
        result = validate_projection_binding_v2(
            registry, receipt,
            engineering_registry=engineering,
            projection_coverage=coverage,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertLess(receipt["projected_asset_count"], receipt["scope_membership_count"])
        keys = [
            (r["engineering_gate_id"], r["engineering_source_kind"], r["engineering_source_ref"])
            for r in receipt["canonical_assets"]
        ]
        self.assertEqual(len(keys), len(set(keys)))

        radical = next(
            row for row in receipt["canonical_assets"]
            if row["engineering_gate_id"] == self.RAD and row["engineering_source_kind"] == "TECHNICAL_CORE"
        )
        memberships = [
            row for row in receipt["scope_memberships"]
            if row["asset_ref"] == radical["asset_id"]
        ]
        self.assertEqual({m["subtopic_id"] for m in memberships}, {"SUB-RAD", "SUB-POLY"})
        self.assertEqual(
            {m["engineering_gate_role"] for m in memberships},
            {"DIRECT", "PREREQUISITE_CLOSURE"},
        )

    def test_local_role_tamper_fails_after_valid_reseal(self):
        registry, receipt, engineering, coverage = self.fixture()
        bad = copy.deepcopy(receipt)
        member = next(
            row for row in bad["scope_memberships"]
            if row["engineering_gate_id"] == self.RAD
            and row["subtopic_id"] == "SUB-POLY"
            and row["engineering_gate_role"] == "PREREQUISITE_CLOSURE"
        )
        member["engineering_gate_role"] = "DIRECT"
        member["membership_digest"] = digest({k: v for k, v in member.items() if k != "membership_digest"})
        self.reseal(bad)
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_V2_LOCAL_ROLE_DRIFT"):
            validate_projection_binding_v2(
                registry, bad,
                engineering_registry=engineering,
                projection_coverage=coverage,
            )

    def test_asset_digest_tamper_fails_closed(self):
        registry, receipt, engineering, coverage = self.fixture()
        bad = copy.deepcopy(receipt)
        bad["canonical_assets"][0]["asset_digest"] = "0" * 64
        self.reseal(bad)
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_V2_ASSET_DIGEST_MISMATCH"):
            validate_projection_binding_v2(
                registry, bad,
                engineering_registry=engineering,
                projection_coverage=coverage,
            )

    def test_duplicate_source_identity_fails_closed(self):
        registry, receipt, engineering, coverage = self.fixture()
        bad = copy.deepcopy(receipt)
        first, second = bad["canonical_assets"][0], bad["canonical_assets"][1]
        second["engineering_gate_id"] = first["engineering_gate_id"]
        second["engineering_source_kind"] = first["engineering_source_kind"]
        second["engineering_source_ref"] = first["engineering_source_ref"]
        self.reseal(bad)
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_V2_SOURCE_IDENTITY_DUPLICATE"):
            validate_projection_binding_v2(
                registry, bad,
                engineering_registry=engineering,
                projection_coverage=coverage,
            )


if __name__ == "__main__":
    unittest.main()
