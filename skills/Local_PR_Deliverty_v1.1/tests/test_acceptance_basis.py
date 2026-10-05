import copy
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import acceptance_basis as basis


DIGEST = "d" * 64
SURFACE = "e" * 64


def grant(capability, principal="coordinator", epoch="AE-001"):
    return {
        "record": "AUTHORITY_GRANT",
        "version": "1",
        "grant_id": f"G-{capability}",
        "principal": principal,
        "capability": capability,
        "scope": {
            "parent_task_id": "PARENT-492",
            "responsibility_task_id": "PRD-017",
            "acceptance_epoch_id": epoch,
        },
        "issued_by": "owner",
        "instruction_ref": "issuecomment-1",
        "issued_at": "2026-10-05T06:00:00Z",
        "expires_at": None,
        "revoked_at": None,
        "source_kind": "GITHUB_PROVIDER",
        "source_digest": "a" * 64,
        "authentication_status": "OBSERVED_TRUSTED_PROVIDER",
    }


def proposal(risk_effect="STRENGTHENING", risk_accepted_by=None):
    return {
        "record": "ACCEPTANCE_CHANGE_PROPOSAL",
        "version": "1",
        "proposal_id": "ACP-002",
        "parent_task_id": "PARENT-492",
        "responsibility_task_id": "PRD-017",
        "previous_epoch_id": "AE-001",
        "new_epoch_id": "AE-002",
        "proposed_by": "reviewer",
        "implemented_by": "reviewer",
        "adopted_by": "coordinator",
        "risk_accepted_by": risk_accepted_by,
        "change_kind": "COVERAGE_EXTENSION",
        "risk_effect": risk_effect,
        "rationale": "Add a missing malformed-input acceptance case.",
        "evidence_refs": ["EV-17"],
        "proposed_project_protocol_ref": "example/project@" + "1" * 40 + ":review/protocol.json",
        "proposed_project_protocol_digest": DIGEST,
        "proposed_protected_surface_digest": SURFACE,
        "affected_profile_ids": ["APR-PRD-017-AE001"],
        "affected_method_ids": ["VM-NEG"],
        "status": "ADOPTED",
        "proposed_at": "2026-10-05T06:05:00Z",
        "adopted_at": "2026-10-05T06:10:00Z",
        "adoption_ref": "issuecomment-2",
        "risk_acceptance_ref": "issuecomment-risk" if risk_accepted_by else None,
    }


def project_protocol():
    return {
        "acceptance_sets": [
            {
                "id": "WRITER",
                "criteria": [
                    {
                        "id": "AC-1",
                        "required": True,
                        "reviewer_check_required": True,
                        "super_review_required": True,
                        "verification_method_ids": ["VM-REV", "VM-SUPER"],
                    }
                ],
            }
        ],
        "verification_methods": [
            {
                "id": "VM-REV",
                "verification_class": "NEGATIVE",
                "harness_id": None,
                "external_gate_id": None,
                "required_evidence_classes": ["REVIEWER_INDEPENDENT"],
                "material_inputs": ["SOURCE", "FIXTURE"],
                "rerun_policy": "DECLARED_MATERIAL_INPUTS",
                "applies_to_roles": ["REVIEWER"],
            },
            {
                "id": "VM-SUPER",
                "verification_class": "ROUND_TRIP",
                "harness_id": "H-1",
                "external_gate_id": None,
                "required_evidence_classes": ["SUPER_REVIEW_INDEPENDENT"],
                "material_inputs": ["SOURCE", "HARNESS", "ORACLE"],
                "rerun_policy": "DECLARED_MATERIAL_INPUTS",
                "applies_to_roles": ["COORDINATOR"],
            },
        ],
        "external_gates": [],
    }


def epoch():
    return {
        "epoch_id": "AE-002",
        "project_protocol_ref": "example/project@" + "1" * 40 + ":review/protocol.json",
        "project_protocol_digest": DIGEST,
    }


def profile():
    value = {
        "record": "ACCEPTANCE_PROFILE",
        "version": "1",
        "profile_id": "APR-PRD-017-AE002",
        "task_id": "PRD-017",
        "acceptance_epoch_id": "AE-002",
        "project_protocol_ref": epoch()["project_protocol_ref"],
        "project_protocol_digest": DIGEST,
        "acceptance_set_refs": ["WRITER"],
        "criterion_refs": ["AC-1"],
        "excluded_criteria": [],
        "parameters": {},
        "role_bindings": {
            "REVIEWER": [
                {
                    "criterion_id": "AC-1",
                    "verification_method_id": "VM-REV",
                    "harness_id": None,
                    "external_gate_id": None,
                    "required_evidence_classes": ["REVIEWER_INDEPENDENT"],
                }
            ],
            "COORDINATOR": [
                {
                    "criterion_id": "AC-1",
                    "verification_method_id": "VM-SUPER",
                    "harness_id": "H-1",
                    "external_gate_id": None,
                    "required_evidence_classes": ["SUPER_REVIEW_INDEPENDENT"],
                }
            ],
        },
        "external_gate_ids": [],
        "dependency_requirements": [],
    }
    value["digest"] = basis.canonical_digest(value)
    return value


class AcceptanceBasisTests(unittest.TestCase):
    def test_strengthening_adoption_needs_policy_grant_not_risk_grant(self):
        p = proposal()
        basis.validate_adoption_authority(p, [grant("ACCEPTANCE_POLICY_WRITE")])

    def test_relaxing_adoption_requires_separate_risk_grant(self):
        p = proposal("RELAXING", risk_accepted_by="owner")
        with self.assertRaises(basis.AcceptanceBasisError):
            basis.validate_adoption_authority(p, [grant("ACCEPTANCE_POLICY_WRITE")])

        risk = grant("RISK_RELAXATION", principal="owner")
        basis.validate_adoption_authority(p, [grant("ACCEPTANCE_POLICY_WRITE"), risk])

    def test_build_epoch_is_content_addressed_and_candidate_free(self):
        value = basis.build_epoch(proposal(), [grant("ACCEPTANCE_POLICY_WRITE")])
        self.assertEqual(value["digest"], basis.canonical_digest(value))
        self.assertNotIn("candidate_sha", value)
        self.assertNotIn("base_sha", value)
        self.assertNotIn("environment_digest", value)

    def test_profile_requires_role_applicable_method_binding(self):
        value = profile()
        basis.validate_profile(value, project_protocol(), epoch())

        broken = copy.deepcopy(value)
        broken["role_bindings"]["REVIEWER"][0]["verification_method_id"] = "VM-SUPER"
        broken["role_bindings"]["REVIEWER"][0]["harness_id"] = "H-1"
        broken["role_bindings"]["REVIEWER"][0]["required_evidence_classes"] = ["SUPER_REVIEW_INDEPENDENT"]
        broken["digest"] = basis.canonical_digest(broken)
        with self.assertRaises(basis.AcceptanceBasisError):
            basis.validate_profile(broken, project_protocol(), epoch())

    def test_evidence_validity_is_derived_without_mutating_history(self):
        evidence = {
            "evidence_id": "EV-17",
            "candidate_sha": "a" * 40,
            "acceptance_epoch_id": "AE-001",
            "project_protocol_digest": DIGEST,
            "acceptance_profile_digest": "1" * 64,
            "protected_surface_digest": SURFACE,
            "environment_digest": "2" * 64,
            "dependency_heads": {"PRD-5": "b" * 40},
        }
        before = copy.deepcopy(evidence)
        view = basis.evidence_validity_projection(
            evidence,
            candidate_sha="a" * 40,
            acceptance_epoch_id="AE-002",
            project_protocol_digest=DIGEST,
            acceptance_profile_digest="1" * 64,
            protected_surface_digest=SURFACE,
            environment_digest="2" * 64,
            dependency_heads={"PRD-5": "b" * 40},
        )
        self.assertFalse(view["current"])
        self.assertIn("ACCEPTANCE_BASIS_CHANGED", view["reasons"])
        self.assertEqual(evidence, before)

    def test_unknown_replay_impact_fails_conservative(self):
        plan = basis.replay_plan(
            required_method_ids={"VM-REV", "VM-SUPER"},
            method_material_inputs={"VM-REV": {"SOURCE"}, "VM-SUPER": {"ORACLE"}},
            method_rerun_policy={"VM-REV": "DECLARED_MATERIAL_INPUTS", "VM-SUPER": "DECLARED_MATERIAL_INPUTS"},
            changed_inputs=None,
        )
        self.assertEqual(plan["mode"], "CONSERVATIVE_FULL_REQUIRED_SET")
        self.assertEqual(set(plan["rerun_method_ids"]), {"VM-REV", "VM-SUPER"})

    def test_selective_replay_uses_declared_material_inputs(self):
        plan = basis.replay_plan(
            required_method_ids={"VM-REV", "VM-SUPER"},
            method_material_inputs={"VM-REV": {"SOURCE", "FIXTURE"}, "VM-SUPER": {"SOURCE", "ORACLE"}},
            method_rerun_policy={"VM-REV": "DECLARED_MATERIAL_INPUTS", "VM-SUPER": "DECLARED_MATERIAL_INPUTS"},
            changed_inputs={"FIXTURE"},
        )
        self.assertEqual(plan["mode"], "SELECTIVE_DECLARED_INPUTS")
        self.assertEqual(plan["rerun_method_ids"], ["VM-REV"])


if __name__ == "__main__":
    unittest.main()
