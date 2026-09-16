from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from compile_physics_engineering_workbench import load as load_engineering
from project_engineering_to_domain_registry import digest
from project_engineering_to_domain_registry_v2 import project_engineering_to_domain_registry_v2
from validate_engineering_domain_projection_binding_v2 import validate_projection_binding_v2


class EngineeringDomainProjectionV2Tests(unittest.TestCase):
    VEC_BASICS = "PHY-VEC-BASICS"
    VEC_ADD = "PHY-VEC-ADD-SUB"
    CAP_B = "PHY-CAP-VEC-BASICS"
    CAP_A = "PHY-CAP-VEC-ADD"

    def fixture(self):
        base = {
            "schema_version": "1.0.0",
            "subject": "PHYSICS",
            "registry_id": "PHY-REG-TEST-CANONICAL-PROJECTION",
            "run_ref": "RUN-TEST-CANONICAL-PROJECTION",
            "source_manifest_refs": ["GT-TEST-CANONICAL-PROJECTION"],
            "join_refs": ["JOIN:VB", "JOIN:VA"],
            "admission_policy_ref": "PHY-CANONICAL-DOMAIN-REGISTRY-v1",
            "assets": [
                self.capability_asset("REG-PHY-CAP-TESTVB", "SUB-VB", "JOIN:VB", self.CAP_B),
                self.capability_asset("REG-PHY-CAP-TESTVA", "SUB-VA", "JOIN:VA", self.CAP_A),
            ],
        }
        engineering = load_engineering("policies/physics-technical-engineering-gates.v1.json")
        coverage = {
            "crosswalk_id": "PHY-ENG-XWALK-TEST-CANONICAL",
            "capability_gate_map": {
                self.CAP_B: [self.VEC_BASICS],
                self.CAP_A: [self.VEC_ADD],
            },
            "bucket_gate_map": [
                {
                    "bucket_id": "BUCKET-VB",
                    "capability_refs": [self.CAP_B],
                    "engineering_gate_ids": [self.VEC_BASICS],
                    "engineering_gap_capability_refs": [],
                },
                {
                    "bucket_id": "BUCKET-VA",
                    "capability_refs": [self.CAP_A],
                    "engineering_gate_ids": [self.VEC_ADD],
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
                    {"bucket_id": "BUCKET-VB", "member_capability_refs": [self.CAP_B]},
                    {"bucket_id": "BUCKET-VA", "member_capability_refs": [self.CAP_A]},
                ]
            },
            bucket_sid={"BUCKET-VB": "SUB-VB", "BUCKET-VA": "SUB-VA"},
            core2_pages=[
                {"question_ref": "QB", "capability_refs": [self.CAP_B]},
                {"question_ref": "QA", "capability_refs": [self.CAP_A]},
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
                "statement": "Use the exact synthetic physics capability in its declared scope.",
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

        vec_basics_core = next(
            row for row in receipt["canonical_assets"]
            if row["engineering_gate_id"] == self.VEC_BASICS and row["engineering_source_kind"] == "TECHNICAL_CORE"
        )
        memberships = [
            row for row in receipt["scope_memberships"]
            if row["asset_ref"] == vec_basics_core["asset_id"]
        ]
        self.assertEqual(len(memberships), 2)
        roles = {(m["subtopic_id"], m["engineering_gate_role"]) for m in memberships}
        self.assertEqual(roles, {("SUB-VB", "DIRECT"), ("SUB-VA", "PREREQUISITE_CLOSURE")})

    def test_tampered_canonical_asset_digest_fails_validation(self):
        registry, receipt, engineering, coverage = self.fixture()
        assets = {row["asset_id"]: row for row in registry["assets"]}
        target = receipt["canonical_assets"][0]["asset_id"]
        assets[target]["payload"]["statement"] += " tampered"
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_V2_ASSET_DIGEST_MISMATCH"):
            validate_projection_binding_v2(
                registry, receipt,
                engineering_registry=engineering,
                projection_coverage=coverage,
            )

    def test_tampered_local_role_fails_validation(self):
        registry, receipt, engineering, coverage = self.fixture()
        prereq_member = next(
            row for row in receipt["scope_memberships"]
            if row["engineering_gate_role"] == "PREREQUISITE_CLOSURE"
        )
        prereq_member["engineering_gate_role"] = "DIRECT"
        prereq_member["membership_digest"] = digest({k: v for k, v in prereq_member.items() if k != "membership_digest"})
        self.reseal(receipt)
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_V2_LOCAL_ROLE_DRIFT"):
            validate_projection_binding_v2(
                registry, receipt,
                engineering_registry=engineering,
                projection_coverage=coverage,
            )

    def test_unmapped_membership_capability_fails_closed(self):
        registry, receipt, engineering, coverage = self.fixture()
        coverage_broken = copy.deepcopy(coverage)
        coverage_broken["capability_gate_map"].pop(self.CAP_B)
        with self.assertRaisesRegex(ValueError, "DOMAIN_PROJECTION_V2_MEMBERSHIP_CAPABILITY_UNMAPPED"):
            validate_projection_binding_v2(
                registry, receipt,
                engineering_registry=engineering,
                projection_coverage=coverage_broken,
            )


if __name__ == "__main__":
    unittest.main()
