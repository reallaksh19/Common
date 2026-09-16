#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import digest, load  # noqa: E402


class ChemistryEngineeringPassportError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryEngineeringPassportError(code, message)


def schema(obj: dict, rel: str, code: str):
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def validate_receipt(receipt: dict):
    states = receipt["gate_states"]
    external = receipt["external_dependency_states"]
    counts = receipt["counts"]
    ready = sum(x["status"] == "ENGINEERING_GATE_READY" for x in states)
    blocked = len(states) - ready
    ext_blocked = sum(x["status"] in {"BLOCKED", "UNRESOLVED"} for x in external)
    expected = {
        "direct_gate_count": len(receipt["direct_gate_ids"]),
        "optional_gate_count": len(receipt["optional_gate_ids"]),
        "out_of_scope_gate_count": len(receipt["out_of_scope_gate_ids"]),
        "closure_gate_count": len(receipt["closure_gate_ids"]),
        "ready_gate_count": ready,
        "blocked_gate_count": blocked,
        "external_dependency_count": len(external),
        "external_blocked_count": ext_blocked,
        "source_audit_count": len(receipt["source_audit_states"]),
        "production_source_audit_count": sum(x["audit_role"] == "PRODUCTION_SOURCE_AUDIT" for x in receipt["source_audit_states"]),
        "stress_source_audit_count": sum(x["audit_role"] == "STRESS_TEST_SOURCE_AUDIT" for x in receipt["source_audit_states"]),
    }
    if counts != expected:
        fail("CHEM_PASS_RECEIPT_INCONSISTENT", f"receipt counts inconsistent: {counts} != {expected}")
    should_block = bool(receipt["blockers"]) or blocked > 0 or ext_blocked > 0
    if (receipt["closure_status"] == "BLOCKED") != should_block:
        fail("CHEM_PASS_RECEIPT_INCONSISTENT", "closure_status contradicts blockers/states")


def compile_passport(request: dict, receipt: dict) -> dict:
    schema(request, "contracts/chemistry-engineering-request.schema.json", "CHEM_PASS_REQUEST_SCHEMA")
    schema(receipt, "contracts/chemistry-engineering-closure-receipt.schema.json", "CHEM_PASS_RECEIPT_SCHEMA")
    validate_receipt(receipt)
    if request["request_id"] != receipt["request_id"]:
        fail("CHEM_PASS_REQUEST_RECEIPT_MISMATCH", "request mismatch")
    ready = receipt["closure_status"] == "READY"
    next_action = (
        "Proceed to CDAU technical boundary; source-scope authorization, pedagogy, learner fit and publication remain separate."
        if ready
        else (receipt["blockers"][0]["message"] if receipt["blockers"] else "Resolve engineering blockers.")
    )
    passport = {
        "schema_version":"2.0.0",
        "passport_id":receipt["receipt_id"].replace("CHEM-ENG-CLOSURE-","CHEM-ENG-PASS-",1),
        "request_id":request["request_id"],
        "manifest_id":receipt["manifest_id"],
        "closure_receipt_id":receipt["receipt_id"],
        "closure_receipt_digest":digest(receipt),
        "requested_topic":request["requested_topic"],
        "requested_scope":request["requested_scope"],
        "engineering_depth":request["engineering_depth"],
        "technical_state":"ENGINEERING_READY" if ready else "BLOCKED_PENDING_ENGINEERING",
        "counts":receipt["counts"],
        "gate_states":receipt["gate_states"],
        "source_audit_states":receipt["source_audit_states"],
        "external_dependency_states":receipt["external_dependency_states"],
        "source_item_status":receipt["source_item_status"],
        "cdau_technical_authorization":"ALLOWED" if ready else "BLOCKED",
        "next_action":next_action,
    }
    schema(passport, "contracts/chemistry-engineering-passport.schema.json", "CHEM_PASS_SCHEMA")
    return passport
