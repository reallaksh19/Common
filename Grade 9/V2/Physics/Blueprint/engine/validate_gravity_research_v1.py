#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from build_physics_engineering_gate_registry_v3 import build_registry as build_registry_v3  # noqa: E402
from compile_engineering_closure import compile_closure, load  # noqa: E402
from compile_engineering_passport import compile_passport  # noqa: E402
from validate_engineering_gates_v3 import PhysicsEngineeringGateV3Error, validate as validate_registry_v3  # noqa: E402


class GravityResearchValidationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise GravityResearchValidationError(code, message)


def validate_schema(obj: dict, rel: str, code: str):
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def ids(items: list[dict], key: str) -> set[str]:
    return {item[key] for item in items}


EXPECTED = {
    "PHY-GRAV-FORCE": {
        "invariants": {"INV-GRAV-FORCE-ATTRACTIVE","INV-GRAV-FORCE-INVERSE-SQUARE","INV-GRAV-FORCE-DISTINCT-BODIES","INV-GRAV-FORCE-SOURCE-DISTANCE-SCOPE"},
        "concepts": {"CON-GRAV-FORCE-ATTRACTION","CON-GRAV-SPHERICAL-EXTERNAL"},
        "relations": {"EQ-GRAV-FORCE-MAGNITUDE","EQ-GRAV-FORCE-VECTOR"},
        "representations": {"REP-GRAV-FORCE-PAIR"},
        "prerequisites": {"PHY-NLM-INTERACTION","PHY-NLM-THIRD-LAW","PHY-VEC-BASICS"},
    },
    "PHY-GRAV-FIELD": {
        "invariants": {"INV-GRAV-FIELD-FORCE-PER-MASS","INV-GRAV-FIELD-TEST-MASS-INDEPENDENCE","INV-GRAV-FIELD-RADIAL-INWARD","INV-GRAV-FIELD-INVERSE-SQUARE","INV-GRAV-FIELD-SUPERPOSITION","INV-GRAV-FIELD-MODEL-SCOPE"},
        "concepts": {"CON-GRAV-FIELD-FORCE-PER-MASS","CON-GRAV-FIELD-RADIAL","CON-GRAV-FIELD-SUPERPOSITION"},
        "relations": {"EQ-GRAV-FIELD-DEFINITION","EQ-GRAV-FIELD-POINT-MASS","EQ-GRAV-FIELD-SUPERPOSITION"},
        "representations": {"REP-GRAV-RADIAL-FIELD","REP-GRAV-FIELD-SUPERPOSITION"},
        "prerequisites": {"PHY-GRAV-FORCE","PHY-VEC-COMPONENTS","PHY-NLM-SECOND-LAW"},
    },
}

EXPECTED_CLOSURE = {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-NLM-INTERACTION",
    "PHY-NLM-FBD",
    "PHY-NLM-FIRST-LAW",
    "PHY-NLM-SECOND-LAW",
    "PHY-NLM-THIRD-LAW",
    "PHY-GRAV-FORCE",
    "PHY-GRAV-FIELD",
}


def require_subset(gate_id: str, category: str, actual: set[str], expected: set[str]):
    missing = expected - actual
    if missing:
        fail("E_GRAV_GATE_INVARIANT", f"{gate_id} missing {category}: {sorted(missing)}")


def validate(
    request: dict,
    discovery: dict,
    manifest: dict,
    dossier: dict,
    ledger: dict,
    *,
    registry: dict | None = None,
) -> dict:
    validate_schema(request, "contracts/engineering-request.schema.json", "E_GRAV_SCHEMA")
    validate_schema(discovery, "contracts/engineering-discovery-decision.schema.json", "E_GRAV_SCHEMA")
    validate_schema(manifest, "contracts/engineering-topic-manifest.schema.json", "E_GRAV_SCHEMA")
    validate_schema(dossier, "contracts/engineering-research-dossier.schema.json", "E_GRAV_SCHEMA")
    validate_schema(ledger, "contracts/engineering-claim-ledger.schema.json", "E_GRAV_SCHEMA")

    request_id = request["request_id"]
    if any(obj["request_id"] != request_id for obj in (discovery, manifest, dossier, ledger)):
        fail("E_GRAV_SCHEMA", "request_id drift across Gravity engineering artifacts")
    if request["engineering_depth"] != "RESEARCH":
        fail("E_GRAV_SCHEMA", "Gravity field pilot must remain RESEARCH depth")

    create_children = {op["gate_id"] for op in discovery["operations"] if op["operation"] == "CREATE_CHILD"}
    if create_children != {"PHY-GRAV-FORCE", "PHY-GRAV-FIELD"}:
        fail("E_GRAV_DISCOVERY", f"CREATE_CHILD decision drift: {sorted(create_children)}")
    field_ops = [op for op in discovery["operations"] if op["gate_id"] == "PHY-GRAV-FIELD"]
    if len(field_ops) != 1 or field_ops[0].get("parent_gate_id") != "PHY-GRAV-FORCE":
        fail("E_GRAV_DISCOVERY", "PHY-GRAV-FIELD must be a child of PHY-GRAV-FORCE")
    if manifest["required_gate_ids"] != ["PHY-GRAV-FIELD"]:
        fail("E_GRAV_DISCOVERY", "manifest must declare only gravitational field as the direct gate")
    if manifest["registry_ref"] != "GENERATED:physics-technical-engineering-gates.v3":
        fail("E_GRAV_DISCOVERY", "Gravity manifest must consume the canonical subject-wide v3 registry")
    if manifest.get("gate_extension_refs"):
        fail("E_GRAV_DISCOVERY", "canonical v3 Gravity must not use the legacy v2 extension mechanism")

    registry = registry if registry is not None else build_registry_v3()
    try:
        validate_registry_v3(registry)
    except PhysicsEngineeringGateV3Error as exc:
        fail("E_GRAV_GATE_INVARIANT", f"{exc.code}: {exc.message}")
    gate_map = {gate["subtopic_id"]: gate for gate in registry["gates"]}

    for gate_id, expected in EXPECTED.items():
        gate = gate_map.get(gate_id)
        if gate is None:
            fail("E_GRAV_GATE_INVARIANT", f"missing canonical Gravity gate {gate_id}")
        require_subset(gate_id, "invariants", set(gate["required_invariants"]), expected["invariants"])
        require_subset(gate_id, "concepts", ids(gate["concepts"], "concept_id"), expected["concepts"])
        require_subset(gate_id, "relations", ids(gate["relations"], "relation_id"), expected["relations"])
        require_subset(gate_id, "representations", ids(gate["representations"], "representation_id"), expected["representations"])
        require_subset(gate_id, "prerequisites", set(gate["prerequisites"]), expected["prerequisites"])

    dossier_sources = {item["source_ref"] for item in dossier["authoritative_source_set"]}
    claim_map = {claim["claim_id"]: claim for claim in ledger["claims"]}
    if len(claim_map) != len(ledger["claims"]):
        fail("E_GRAV_PROVENANCE", "duplicate claim_id")
    if ledger["status"] != "CLAIM_LEDGER_READY" or dossier["status"] != "RESEARCH_DOSSIER_READY":
        fail("E_GRAV_PROVENANCE", "research artifacts are not release-ready")
    for claim in ledger["claims"]:
        unknown_sources = set(claim["source_refs"]) - dossier_sources
        if unknown_sources:
            fail("E_GRAV_PROVENANCE", f"{claim['claim_id']} uses sources absent from dossier: {sorted(unknown_sources)}")
        if claim["claim_status"] != "VERIFIED":
            fail("E_GRAV_PROVENANCE", f"ready claim ledger contains non-verified claim {claim['claim_id']}")

    gravity_assets: set[str] = set()
    for gate_id in EXPECTED:
        gate = gate_map[gate_id]
        gravity_assets |= set(gate["required_invariants"])
        gravity_assets |= ids(gate["concepts"], "concept_id")
        gravity_assets |= ids(gate["relations"], "relation_id")
        gravity_assets |= ids(gate["representations"], "representation_id")
        gravity_assets |= ids(gate["misconceptions"], "misconception_id")
        gravity_assets |= ids(gate["problem_families"], "family_id")
        for authority in gate["authority_basis"]:
            prefix = "ENG-CLAIMS-GRAV-FIELD-V1:"
            if not authority["source_ref"].startswith(prefix):
                fail("E_GRAV_PROVENANCE", f"{gate_id} authority does not bind the Gravity claim ledger")
            claim_id = authority["source_ref"][len(prefix):]
            if claim_id not in claim_map:
                fail("E_GRAV_PROVENANCE", f"{gate_id} references unknown claim {claim_id}")

    for claim in ledger["claims"]:
        unknown_targets = set(claim["used_by"]) - gravity_assets
        if unknown_targets:
            fail("E_GRAV_PROVENANCE", f"{claim['claim_id']} used_by has unknown Gravity targets: {sorted(unknown_targets)}")

    receipt = compile_closure(
        request,
        manifest,
        registry=registry,
        research_dossier=dossier,
        claim_ledger=ledger,
    )
    if receipt["closure_status"] != "READY" or set(receipt["transitive_gate_ids"]) != EXPECTED_CLOSURE:
        fail("E_GRAV_CLOSURE", f"unexpected Gravity closure: {receipt['closure_status']} {receipt['transitive_gate_ids']}")
    if receipt["counts"] != {"direct_gate_count":1,"transitive_gate_count":10,"ready_gate_count":10,"blocked_gate_count":0}:
        fail("E_GRAV_CLOSURE", f"unexpected Gravity closure counts: {receipt['counts']}")

    # The subject Passport is diagnostic only. Research validation proves technical
    # closure/provenance; downstream consumer permission belongs exclusively to the
    # global Engineering Gate and is intentionally not evaluated here.
    passport = compile_passport(request, receipt)
    if passport["technical_state"] != "ENGINEERING_READY":
        fail("E_GRAV_CLOSURE", "Gravity technical closure did not become ENGINEERING_READY")
    if passport["consumer_authorization"] != "NOT_EVALUATED":
        fail("E_GRAV_CLOSURE", "subject Passport must not issue downstream consumer authority")

    return {
        "status": "PASS",
        "request_id": request_id,
        "decision_id": discovery["decision_id"],
        "registry_id": registry["registry_id"],
        "gravity_gates": sorted(EXPECTED),
        "claim_count": len(ledger["claims"]),
        "closure_gate_count": receipt["counts"]["transitive_gate_count"],
        "closure_digest": receipt["closure_digest"],
        "passport_id": passport["passport_id"],
    }


def main():
    request = load("fixtures/engineering-workbench/grav-field-request.v1.json")
    discovery = load("fixtures/engineering-workbench/grav-field-discovery.v1.json")
    manifest = load("fixtures/engineering-workbench/grav-field-manifest.v3.json")
    dossier = load("fixtures/engineering-workbench/grav-field-research-dossier.v1.json")
    ledger = load("fixtures/engineering-workbench/grav-field-claim-ledger.v1.json")
    print(json.dumps(validate(request, discovery, manifest, dossier, ledger), indent=2))


if __name__ == "__main__":
    main()
