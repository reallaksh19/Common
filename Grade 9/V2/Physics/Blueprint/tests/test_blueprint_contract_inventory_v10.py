#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
SHARED = REPO / "Grade 9" / "V2" / "Shared" / "CrossDomain"
SHARED_GATE = REPO / "Grade 9" / "V2" / "Shared" / "EngineeringGate"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def load_shared(rel: str):
    return json.loads((SHARED / rel).read_text(encoding="utf-8"))


def load_shared_gate(rel: str):
    return json.loads((SHARED_GATE / rel).read_text(encoding="utf-8"))


def test_v10_contract_schemas_are_valid():
    local_names = [
        "contracts/scoped-execution-envelope.schema.json",
        "contracts/scoped-evidence-receipt.schema.json",
        "contracts/domain-prerequisite-closure.schema.json",
        "contracts/engineering-readiness-envelope.schema.json",
        "contracts/seven-core-stress-test-request.schema.json",
        "contracts/seven-core-stress-test-receipt.schema.json",
        "contracts/join-packet.schema.json",
        "contracts/physics-curriculum-scope-binding-registry.schema.json",
        "contracts/physics-blueprint-authority-projection.schema.json",
    ]
    shared_names = [
        "contracts/domain-prerequisite-authority.schema.json",
        "contracts/domain-prerequisite-demand.schema.json",
    ]
    shared_gate_names = [
        "contracts/domain-prerequisite-closure.schema.json",
        "contracts/engineering-readiness-envelope.schema.json",
    ]
    for rel in local_names:
        Draft202012Validator.check_schema(load(rel))
    for rel in shared_names:
        Draft202012Validator.check_schema(load_shared(rel))
    for rel in shared_gate_names:
        Draft202012Validator.check_schema(load_shared_gate(rel))


def test_v10_physics_curriculum_binding_is_exact_and_fail_closed():
    registry = load("registry/physics-curriculum-scope-bindings.v1.json")
    schema = load("contracts/physics-curriculum-scope-binding-registry.schema.json")
    Draft202012Validator(schema).validate(registry)
    assert registry["selector_semantics"] == "EXACT_GRADE_CURRICULUM_SCOPE_AND_GATE_SET"
    ids = [row["binding_id"] for row in registry["bindings"]]
    assert len(ids) == len(set(ids))


def test_v10_cross_domain_transport_is_shared_not_physics_shadowed():
    for rel in (
        "contracts/domain-prerequisite-authority.schema.json",
        "contracts/domain-prerequisite-demand.schema.json",
        "policy/domain-prerequisite-routing.v1.json",
    ):
        assert not (ROOT / rel).exists(), "PHYSICS_LOCAL_CROSS_DOMAIN_PROTOCOL_SHADOW:" + rel
    closure = load("contracts/domain-prerequisite-closure.schema.json")
    demand_ref = closure["properties"]["demands"]["items"]["$ref"]
    assert demand_ref == "https://schemas.common/v2/shared/cross-domain/domain-prerequisite-demand.schema.json"
    assert closure["x-authority-ref"] == "Grade 9/V2/Shared/EngineeringGate/contracts/domain-prerequisite-closure.schema.json"


def test_v10_shared_demand_contract_is_subject_neutral_transport():
    demand = load_shared("contracts/domain-prerequisite-demand.schema.json")
    assert demand["properties"]["requester_subject"] == {"type": "string", "minLength": 1}
    assert demand["properties"]["demand_id"]["pattern"] == "^DOMAIN-DEMAND-[A-Z0-9-]+$"
    assert demand["properties"]["authority_contract_ref"]["const"] == "Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-authority.schema.json"


def test_v10_join_policy_keeps_verified_absence_distinct_from_unknown():
    policy = load("policy/join-policy.v2.json")
    assert policy["policy_id"] == "PHY-JOIN-v2"
    assert policy["assessment_coverage_states"] == [
        "DEMANDS_PRESENT",
        "VERIFIED_NO_TARGET_DEMAND",
        "COVERAGE_UNKNOWN",
    ]
    assert policy["verified_no_target_demand_is_reconciled_state"] is True
    assert policy["verified_no_target_demand_allows_assimilation"] is True
    assert policy["coverage_unknown_blocks_assimilation"] is True
    assert policy["zero_demand_requires_scoped_coverage_receipt"] is True


def test_v10_domain_provider_registry_routes_math_without_self_certifying_it():
    policy = load_shared("registry/domain-provider-registry.v1.json")
    assert policy["registry_id"] == "V2-CROSS-DOMAIN-PROVIDER-REGISTRY-v1"
    math = next(row for row in policy["providers"] if row["prerequisite_prefix"] == "MATH-")
    assert math["provider_subject"] == "MATHEMATICS"
    assert math["provider_root"] == "Grade 9/V2/Mathematics"
    assert math["authority_entrypoint_ref"] == "Grade 9/V2/Mathematics/V2_GENERATION_ENTRYPOINT.md"
    assert policy["authority_contract_ref"] == "Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-authority.schema.json"
    assert policy["demand_contract_ref"] == "Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-demand.schema.json"
    assert policy["unknown_provider_policy"] == "OPEN_UNROUTABLE_AND_HOLD"
    assert all(policy["rules"].values())


def test_v10_state_semantics_forbid_surrogate_passes():
    policy = load("policy/stress-test-state-semantics.v1.json")
    assert set(policy["states"]) == {
        "PASS", "READY", "HELD", "BLOCKED", "NOT_AUTHORIZED", "NOT_INSTANTIATED", "NOT_APPLICABLE", "NOT_RUN", "NOT_ISSUED",
    }
    assert set(policy["forbidden_surrogate_pass_labels"]) == {
        "PASS_BY_NONFABRICATION", "PASS_FAIL_CLOSED_DIFFERENTIATION",
    }
    assert policy["rules"]["topic_route_may_not_be_reused_for_narrower_scope_without_scoped_evidence"] is True
    assert policy["rules"]["technical_gate_difficulty_is_not_an_sdu_receipt"] is True
    assert policy["rules"]["stress_test_fail_requires_architecture_violation_not_merely_missing_authority"] is True
    assert policy["rules"]["not_authorized_cannot_be_promoted_by_blueprint"] is True


def test_v10_normative_architecture_exists_and_declares_canonicality():
    text = (ROOT / "SELF_HELP_ARCHITECTURE_V10.md").read_text(encoding="utf-8")
    assert "V10 supersedes V9 as the canonical learner-product architecture" in text
    assert "Topic-wide evidence may not be silently reused" in text
    assert "A seven-core stress test is a governed compiler execution" in text
    assert "Shared/CrossDomain" in text


def test_v10_engineering_kernel_defers_consumer_authority_to_global_gate():
    text = (ROOT / "ENGINEERING_READINESS_KERNEL.md").read_text(encoding="utf-8")
    assert "Discovery is permissive; promotion and consumption are strict" in text
    assert "ENGINEERING READINESS ENVELOPE" in text
    assert "Blueprint must never be modified to recognize a topic, subtopic, bucket, prerequisite, downstream consumer, or exception merely because a particular case needs it" in text
    assert "If data is absent, the system holds or rejects. It does not infer from model memory." in text
    assert (SHARED_GATE / "engine" / "evaluate_readiness.py").exists()
    assert (SHARED_GATE / "tests" / "test_readiness_policy.py").exists()
    readiness_mirror = load("contracts/engineering-readiness-envelope.schema.json")
    assert readiness_mirror["x-authority-ref"] == "Grade 9/V2/Shared/EngineeringGate/contracts/engineering-readiness-envelope.schema.json"
    assert (ROOT / "engine" / "compile_engineering_readiness.py").exists()
    assert (ROOT / "engine" / "compile_all_engineering_readiness.py").exists()
    assert (ROOT / "engine" / "compile_physics_blueprint_authority.py").exists()


def main():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"Blueprint V10 contract inventory: PASS ({len(tests)} tests)")


if __name__ == "__main__":
    main()
