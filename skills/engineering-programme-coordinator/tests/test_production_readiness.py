import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from production_readiness import (
    CRITICAL_REQUIRED,
    DEFAULT_REQUIRED,
    validate_readiness,
)


SHA = "a" * 40
DIGEST = "b" * 64


def component(state="UNKNOWN", evidence_refs=None, note=None):
    row = {
        "state": state,
        "evidence_refs": list(evidence_refs or []),
    }
    if note is not None:
        row["note"] = note
    return row


def readiness():
    names = [
        "canonical_local_projection",
        "active_authority_resolution",
        "activation_state_derivation",
        "role_succession_semantics",
        "acceptance_denominator_closure",
        "reviewer_definition",
        "real_artifact_horizontal_integration",
        "execution_kernel",
        "proof_obligation_runtime",
        "evidence_gate",
        "shadow_rollout",
        "rollback",
    ]
    return {
        "schema_version": "PRODUCTION_READINESS_V1",
        "authority": "PRODUCTION_READINESS_PROJECTION",
        "target": {
            "local_runtime": "skills/Local_PR_Deliverty_v1.1",
            "coder_runtime": "skills/engineering-pr-delivery-v3.5",
            "coordinator": "skills/engineering-programme-coordinator",
        },
        "exact_basis": {
            "target_ref": "main",
            "target_sha": SHA,
            "local_protocol_ref": f"reallaksh19/Common@{SHA}:skills/Local_PR_Deliverty_v1.1",
            "local_protocol_digest": DIGEST,
            "v35_protocol_ref": f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.5",
            "v35_protocol_digest": DIGEST,
        },
        "components": {name: component() for name in names},
        "production_mode": "OFF",
        "cutover_authorization": {
            "authorized": False,
            "authority_ref": None,
            "authorized_at": None,
        },
        "cutover_blockers": [],
        "non_blocking_residuals": [],
        "deferred_research": [],
    }


def verify(items, value):
    for name in items:
        value["components"][name] = component(
            "VERIFIED",
            [f"evidence://{name}"],
        )


class ProductionReadinessTests(unittest.TestCase):
    def test_off_projection_allows_explicit_unknowns(self):
        self.assertEqual(validate_readiness(readiness()), [])

    def test_verified_component_requires_evidence(self):
        value = readiness()
        value["components"]["canonical_local_projection"]["state"] = "VERIFIED"
        errors = validate_readiness(value)
        self.assertTrue(
            any(
                "canonical_local_projection" in error
                and "requires at least one evidence_ref" in error
                for error in errors
            ),
            errors,
        )

    def test_not_applicable_requires_reason_or_evidence(self):
        value = readiness()
        value["components"]["reviewer_definition"]["state"] = "NOT_APPLICABLE"
        errors = validate_readiness(value)
        self.assertTrue(any("NOT_APPLICABLE" in error for error in errors), errors)

    def test_schema_rejects_benchmark_progress_as_readiness_input(self):
        value = readiness()
        value["benchmark_progress"] = 99.9
        errors = validate_readiness(value)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors), errors)

    def test_critical_gate_fails_closed_when_components_are_unknown(self):
        value = readiness()
        value["production_mode"] = "CRITICAL_GATE"
        errors = validate_readiness(value)
        self.assertTrue(any("canonical_local_projection" in error for error in errors), errors)
        self.assertTrue(any("explicit cutover_authorization" in error for error in errors), errors)

    def test_critical_gate_accepts_only_verified_required_components(self):
        value = readiness()
        verify(CRITICAL_REQUIRED, value)
        value["production_mode"] = "CRITICAL_GATE"
        value["cutover_authorization"] = {
            "authorized": True,
            "authority_ref": "owner://decision/critical-gate",
            "authorized_at": "2026-10-06T03:00:00Z",
        }
        self.assertEqual(validate_readiness(value), [])

    def test_critical_gate_rejects_open_hard_blocker(self):
        value = readiness()
        verify(CRITICAL_REQUIRED, value)
        value["production_mode"] = "CRITICAL_GATE"
        value["cutover_authorization"] = {
            "authorized": True,
            "authority_ref": "owner://decision/critical-gate",
            "authorized_at": "2026-10-06T03:00:00Z",
        }
        value["cutover_blockers"] = [{
            "id": "BLOCK-1",
            "severity": "HARD",
            "state": "OPEN",
            "reason": "authority state unresolved",
            "evidence_refs": ["issue://block-1"],
        }]
        errors = validate_readiness(value)
        self.assertTrue(any("open HARD blockers" in error for error in errors), errors)

    def test_default_gate_rejects_any_open_blocker(self):
        value = readiness()
        verify(DEFAULT_REQUIRED, value)
        value["production_mode"] = "DEFAULT_GATE"
        value["cutover_authorization"] = {
            "authorized": True,
            "authority_ref": "owner://decision/default-gate",
            "authorized_at": "2026-10-06T03:00:00Z",
        }
        value["cutover_blockers"] = [{
            "id": "BLOCK-2",
            "severity": "SOFT",
            "state": "OPEN",
            "reason": "rollout residual still active",
            "evidence_refs": ["issue://block-2"],
        }]
        errors = validate_readiness(value)
        self.assertTrue(any("forbidden with open blockers" in error for error in errors), errors)

    def test_default_gate_requires_verified_shadow_rollout(self):
        value = readiness()
        verify(CRITICAL_REQUIRED, value)
        value["production_mode"] = "DEFAULT_GATE"
        value["cutover_authorization"] = {
            "authorized": True,
            "authority_ref": "owner://decision/default-gate",
            "authorized_at": "2026-10-06T03:00:00Z",
        }
        errors = validate_readiness(value)
        self.assertTrue(any("shadow_rollout" in error for error in errors), errors)

    def test_exact_protocol_refs_are_sha_bound(self):
        value = readiness()
        value["exact_basis"]["v35_protocol_ref"] = "reallaksh19/Common@main:skills/engineering-pr-delivery-v3.5"
        errors = validate_readiness(value)
        self.assertTrue(any("v35_protocol_ref" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
