import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def validator(name):
    schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def assert_valid(testcase, name, record):
    errors = sorted(validator(name).iter_errors(record), key=lambda e: str(e.path))
    testcase.assertEqual([], [e.message for e in errors])


class AcceptanceSchemaTests(unittest.TestCase):
    def test_authority_grant_schema(self):
        assert_valid(self, "authority-grant", {
            "record": "AUTHORITY_GRANT",
            "version": "1",
            "grant_id": "AUTH-17",
            "principal": "coordinator",
            "capability": "ACCEPTANCE_POLICY_WRITE",
            "scope": {
                "parent_task_id": "PARENT-492",
                "responsibility_task_id": "PRD-017",
                "acceptance_epoch_id": "AE-001",
            },
            "issued_by": "owner",
            "instruction_ref": "issuecomment-1",
            "issued_at": "2026-10-05T06:00:00Z",
            "expires_at": None,
            "revoked_at": None,
            "source_kind": "GITHUB_PROVIDER",
            "source_digest": "a" * 64,
            "authentication_status": "OBSERVED_TRUSTED_PROVIDER",
        })

    def test_change_proposal_schema_keeps_risk_effect_orthogonal(self):
        assert_valid(self, "acceptance-change-proposal", {
            "record": "ACCEPTANCE_CHANGE_PROPOSAL",
            "version": "1",
            "proposal_id": "ACP-2",
            "parent_task_id": "PARENT-492",
            "responsibility_task_id": "PRD-017",
            "previous_epoch_id": "AE-001",
            "new_epoch_id": "AE-002",
            "proposed_by": "reviewer",
            "implemented_by": "reviewer",
            "adopted_by": "coordinator",
            "risk_accepted_by": None,
            "change_kind": "DEFECT_REPAIR",
            "risk_effect": "STRENGTHENING",
            "rationale": "Repair a broken protected harness helper.",
            "evidence_refs": ["EV-1"],
            "proposed_project_protocol_ref": "owner/repo@" + "1" * 40 + ":review/protocol.json",
            "proposed_project_protocol_digest": "b" * 64,
            "proposed_protected_surface_digest": "c" * 64,
            "affected_profile_ids": ["APR-PRD-017-AE001"],
            "affected_method_ids": ["VM-1"],
            "status": "ADOPTED",
            "proposed_at": "2026-10-05T06:05:00Z",
            "adopted_at": "2026-10-05T06:10:00Z",
            "adoption_ref": "issuecomment-2",
            "risk_acceptance_ref": None,
        })

    def test_relaxing_proposal_requires_risk_provenance(self):
        record = {
            "record": "ACCEPTANCE_CHANGE_PROPOSAL",
            "version": "1",
            "proposal_id": "ACP-3",
            "parent_task_id": "PARENT-492",
            "responsibility_task_id": "PRD-017",
            "previous_epoch_id": "AE-001",
            "new_epoch_id": "AE-002",
            "proposed_by": "reviewer",
            "implemented_by": "reviewer",
            "adopted_by": "coordinator",
            "risk_accepted_by": None,
            "change_kind": "TOLERANCE_CHANGE",
            "risk_effect": "RELAXING",
            "rationale": "Proposed tolerance relaxation.",
            "evidence_refs": ["EV-2"],
            "proposed_project_protocol_ref": "owner/repo@" + "1" * 40 + ":review/protocol.json",
            "proposed_project_protocol_digest": "b" * 64,
            "proposed_protected_surface_digest": "c" * 64,
            "affected_profile_ids": ["APR-PRD-017-AE001"],
            "affected_method_ids": ["VM-1"],
            "status": "ADOPTED",
            "proposed_at": "2026-10-05T06:05:00Z",
            "adopted_at": "2026-10-05T06:10:00Z",
            "adoption_ref": "issuecomment-2",
            "risk_acceptance_ref": None,
        }
        errors = list(validator("acceptance-change-proposal").iter_errors(record))
        self.assertTrue(errors)

    def test_epoch_schema_contains_basis_not_candidate_freshness(self):
        record = {
            "record": "ACCEPTANCE_EPOCH",
            "version": "1",
            "epoch_id": "AE-002",
            "parent_task_id": "PARENT-492",
            "previous_epoch_id": "AE-001",
            "project_protocol_ref": "owner/repo@" + "1" * 40 + ":review/protocol.json",
            "project_protocol_digest": "b" * 64,
            "protected_surface_digest": "c" * 64,
            "adopted_by": "coordinator",
            "adoption_ref": "issuecomment-2",
            "adopted_at": "2026-10-05T06:10:00Z",
            "change_proposal_ref": "ACP-2",
            "change_kind": "COVERAGE_EXTENSION",
            "risk_effect": "STRENGTHENING",
            "digest": "d" * 64,
        }
        assert_valid(self, "acceptance-epoch", record)
        self.assertNotIn("candidate_sha", record)
        self.assertNotIn("environment_digest", record)

    def test_profile_schema_binds_role_methods_and_digest(self):
        assert_valid(self, "acceptance-profile", {
            "record": "ACCEPTANCE_PROFILE",
            "version": "1",
            "profile_id": "APR-PRD-017-AE002",
            "task_id": "PRD-017",
            "acceptance_epoch_id": "AE-002",
            "project_protocol_ref": "owner/repo@" + "1" * 40 + ":review/protocol.json",
            "project_protocol_digest": "b" * 64,
            "acceptance_set_refs": ["DXF-WRITER"],
            "criterion_refs": ["DXF-001"],
            "excluded_criteria": [],
            "parameters": {"target_version": "ACAD_2024"},
            "role_bindings": {
                "REVIEWER": [{
                    "criterion_id": "DXF-001",
                    "verification_method_id": "VM-REV",
                    "harness_id": None,
                    "external_gate_id": None,
                    "required_evidence_classes": ["REVIEWER_INDEPENDENT"],
                }],
                "COORDINATOR": [{
                    "criterion_id": "DXF-001",
                    "verification_method_id": "VM-SUPER",
                    "harness_id": "SR-DXF",
                    "external_gate_id": None,
                    "required_evidence_classes": ["SUPER_REVIEW_INDEPENDENT"],
                }],
            },
            "external_gate_ids": [],
            "dependency_requirements": [],
            "digest": "e" * 64,
        })

    def test_review_lease_accepts_legacy_and_new_basis_fields(self):
        schema = json.loads((SCHEMAS / "review-lease.schema.json").read_text(encoding="utf-8"))
        self.assertIn("acceptance_epoch_id", schema["properties"])
        self.assertIn("acceptance_profile_digest", schema["properties"])
        self.assertNotIn("acceptance_epoch_id", schema["required"])
        self.assertNotIn("acceptance_profile_digest", schema["required"])


if __name__ == "__main__":
    unittest.main()
