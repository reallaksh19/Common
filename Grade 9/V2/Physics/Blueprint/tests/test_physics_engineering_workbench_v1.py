#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from compile_engineering_closure import EngineeringClosureError, compile_closure, load  # noqa: E402
from compile_engineering_passport import EngineeringPassportError, compile_passport  # noqa: E402
from validate_ccu_engineering_ready import EngineeringCCUError, validate_engineered_ccu  # noqa: E402

REQUEST = load("fixtures/engineering-workbench/m2d-sba23-request.v1.json")
MANIFEST = load("fixtures/engineering-workbench/m2d-sba23-manifest.v1.json")
REGISTRY = load("policy/physics-technical-engineering-gates.v2.json")
CCU = load("topics/m2d-sba23-ccu.v1.json")
EXPECTED_CLOSURE = {
    "PHY-VEC-BASICS",
    "PHY-VEC-ADD-SUB",
    "PHY-VEC-COMPONENTS",
    "PHY-M2D-PROJECTILE-COMPONENTS",
    "PHY-M2D-SHARED-CLOCK",
    "PHY-M2D-MOVING-LAUNCHER",
}


def gate(doc, gate_id):
    return next(item for item in doc["gates"] if item["subtopic_id"] == gate_id)


def must_closure_fail(request, manifest, code, **kwargs):
    try:
        compile_closure(request, manifest, **kwargs)
    except EngineeringClosureError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def must_passport_fail(request, receipt, code):
    try:
        compile_passport(request, receipt)
    except EngineeringPassportError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


def must_ccu_fail(request, manifest, ccu, code):
    try:
        validate_engineered_ccu(request, manifest, ccu)
    except EngineeringCCUError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
        return
    raise AssertionError(f"expected {code}")


for schema_name in (
    "engineering-request.schema.json",
    "engineering-topic-manifest.schema.json",
    "engineering-closure-receipt.schema.json",
    "engineering-passport.schema.json",
    "engineering-research-dossier.schema.json",
    "engineering-claim-ledger.schema.json",
):
    Draft202012Validator.check_schema(load("contracts/" + schema_name))

receipt = compile_closure(REQUEST, MANIFEST)
assert receipt["closure_status"] == "READY"
assert set(receipt["transitive_gate_ids"]) == EXPECTED_CLOSURE
assert receipt["counts"] == {
    "direct_gate_count": 1,
    "transitive_gate_count": 6,
    "ready_gate_count": 6,
    "blocked_gate_count": 0,
}
assert receipt["source_item_status"] == "SOURCE_HELD"
assert receipt["registry_digest"].startswith("sha256:")
assert receipt["closure_digest"].startswith("sha256:")
assert receipt["manifest_digest"].startswith("sha256:")

# Passport is diagnostic only; it cannot authorize any consumer.
passport = compile_passport(REQUEST, receipt)
assert passport["technical_state"] == "ENGINEERING_READY"
assert passport["consumer_authorization"] == "NOT_EVALUATED"
assert passport["source_item_status"] == "SOURCE_HELD"
assert passport["closure_receipt_digest"].startswith("sha256:")

# Consumer authority is aggregate/global. Missing provider-owned prerequisites block the declared consumer.
must_ccu_fail(REQUEST, MANIFEST, CCU, "E_CCU_ENGINEERING_BLOCKED")

bad_manifest = copy.deepcopy(MANIFEST)
bad_manifest["required_gate_ids"] = ["PHY-M2D-NOT-REAL"]
blocked_receipt = compile_closure(REQUEST, bad_manifest)
assert blocked_receipt["closure_status"] == "BLOCKED"
assert blocked_receipt["blockers"][0]["code"] == "E_ENG_GATE_MISSING"
blocked_passport = compile_passport(REQUEST, blocked_receipt)
assert blocked_passport["technical_state"] == "BLOCKED_PENDING_ENGINEERING"
assert blocked_passport["consumer_authorization"] == "NOT_EVALUATED"
must_ccu_fail(REQUEST, bad_manifest, CCU, "E_CCU_ENGINEERING_BLOCKED")

bad_registry = copy.deepcopy(REGISTRY)
gate(bad_registry, "PHY-M2D-MOVING-LAUNCHER")["status"] = "ENGINEERING_GATE_INCOMPLETE"
blocked = compile_closure(REQUEST, MANIFEST, registry=bad_registry)
assert blocked["closure_status"] == "BLOCKED"
assert any(item["code"] == "E_ENG_GATE_NOT_READY" for item in blocked["blockers"])

bad_registry = copy.deepcopy(REGISTRY)
gate(bad_registry, "PHY-M2D-MOVING-LAUNCHER")["status"] = "SOURCE_SCOPE_HELD"
blocked = compile_closure(REQUEST, MANIFEST, registry=bad_registry)
assert blocked["closure_status"] == "BLOCKED"
assert any(state["status"] == "SOURCE_SCOPE_HELD" for state in blocked["gate_states"])

bad_registry = copy.deepcopy(REGISTRY)
gate(bad_registry, "PHY-VEC-BASICS")["prerequisites"].append("PHY-M2D-MOVING-LAUNCHER")
must_closure_fail(REQUEST, MANIFEST, "E_ENG_DEPENDENCY_CYCLE", registry=bad_registry)

bad_registry = copy.deepcopy(REGISTRY)
gate(bad_registry, "PHY-M2D-MOVING-LAUNCHER")["prerequisites"].append("PHY-NOT-REAL")
must_closure_fail(REQUEST, MANIFEST, "E_ENG_REGISTRY_INVALID", registry=bad_registry)

research_request = copy.deepcopy(REQUEST)
research_request["engineering_depth"] = "RESEARCH"
research_receipt = compile_closure(research_request, MANIFEST)
assert research_receipt["closure_status"] == "BLOCKED"
assert {item["code"] for item in research_receipt["blockers"]} >= {
    "E_ENG_RESEARCH_DOSSIER_REQUIRED",
    "E_ENG_CLAIM_LEDGER_REQUIRED",
}

bad_request = copy.deepcopy(REQUEST)
bad_request["engineering_ready"] = True
must_closure_fail(bad_request, MANIFEST, "E_ENG_REQUEST_SCHEMA")

tampered = copy.deepcopy(blocked_receipt)
tampered["closure_status"] = "READY"
must_passport_fail(REQUEST, tampered, "E_PASS_RECEIPT_INCONSISTENT")

bad_scope = copy.deepcopy(MANIFEST)
bad_scope["scope_ref"] = "M2D-SBA-OTHER"
must_ccu_fail(REQUEST, bad_scope, CCU, "E_CCU_ENGINEERING_SCOPE_MISMATCH")

print("Physics Engineering Workbench v1: PASS (legacy closure preserved; Passport diagnostic only; global consumer boundary enforced)")
