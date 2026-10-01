#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_authorization_binding import (  # noqa: E402
    ChemistryEngineeringBindingError,
    compile_binding,
)
from compile_chemistry_engineering_closure import digest, load  # noqa: E402
from validate_product_source_scope import (  # noqa: E402
    ChemistryProductSourceScopeError,
    validate_product_source_scope,
)


class ChemistryProductEngineeringCustodyError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryProductEngineeringCustodyError(code, message)


def validate_schema(obj: dict, rel: str, code: str):
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def compile_product_custody(request: dict, manifest: dict, ccbom: dict, source_scope_contract: dict, product_authority: dict, *, registry=None, source_audit_payloads=None) -> dict:
    validate_schema(ccbom, "contracts/content-bill-of-materials-v7.schema.json", "CHEM_PRODUCT_CCBOM_SCHEMA")
    validate_schema(source_scope_contract, "contracts/chemistry-product-source-scope-v1.schema.json", "CHEM_PRODUCT_SOURCE_SCOPE_SCHEMA")

    if manifest["scope_ref"] != ccbom["subtopic_id"]:
        fail("CHEM_PRODUCT_ENGINEERING_SCOPE_MISMATCH", "manifest and CCBOM subtopic differ")
    if product_authority.get("subtopic_id") != ccbom["subtopic_id"]:
        fail("CHEM_PRODUCT_AUTHORITY_SCOPE_MISMATCH", "product authority and CCBOM subtopic differ")
    if source_scope_contract["subtopic_id"] != ccbom["subtopic_id"]:
        fail("CHEM_PRODUCT_SOURCE_SCOPE_MISMATCH", "source scope and CCBOM subtopic differ")

    try:
        binding = compile_binding(
            request,
            manifest,
            registry=registry,
            source_audit_payloads=source_audit_payloads,
        )
    except ChemistryEngineeringBindingError as exc:
        fail("CHEM_PRODUCT_ENGINEERING_BLOCKED", f"{exc.code}: {exc.message}")
    if "PAL" not in binding["authorized_consumers"]:
        fail("CHEM_PRODUCT_PAL_NOT_AUTHORIZED", "engineering binding does not authorize PAL")

    gate_id = source_scope_contract["gate_id"]
    audit_state = next((row for row in binding["source_audit_states"] if row["gate_id"] == gate_id), None)
    if audit_state is None:
        fail("CHEM_PRODUCT_SOURCE_AUDIT_MISSING", f"engineering binding has no source audit for {gate_id}")
    if audit_state["audit_role"] != "PRODUCTION_SOURCE_AUDIT":
        fail("CHEM_PRODUCT_SOURCE_AUDIT_NOT_PRODUCTION", "stress audit cannot establish product custody")
    if audit_state["audit_ref"] != source_scope_contract["source_audit_ref"]:
        fail("CHEM_PRODUCT_SOURCE_AUDIT_REF_MISMATCH", "scope contract binds a different source audit")

    audit = None
    if source_audit_payloads:
        audit = source_audit_payloads.get(audit_state["audit_ref"])
    if audit is None:
        try:
            audit = load(audit_state["audit_ref"])
        except Exception as exc:
            fail("CHEM_PRODUCT_SOURCE_AUDIT_UNREADABLE", str(exc))
    if digest(audit) != audit_state["audit_digest"]:
        fail("CHEM_PRODUCT_SOURCE_AUDIT_DIGEST_MISMATCH", "engineering binding source audit is stale")

    current_registry = registry if registry is not None else load(manifest["registry_ref"])
    try:
        validate_product_source_scope(source_scope_contract, audit, product_authority, current_registry)
    except ChemistryProductSourceScopeError as exc:
        fail("CHEM_PRODUCT_SOURCE_SCOPE_INVALID", f"{exc.code}: {exc.message}")

    authority_id = str(product_authority.get("authority_id", "")).strip()
    if not authority_id:
        fail("CHEM_PRODUCT_AUTHORITY_ID_MISSING", "product authority requires authority_id")

    custody = {
        "schema_version":"2.0.0",
        "custody_id":manifest["manifest_id"].replace("CHEM-ENG-MAN-","CHEM-PRODUCT-ENG-CUSTODY-",1),
        "request_id":request["request_id"],
        "manifest_id":manifest["manifest_id"],
        "scope_ref":manifest["scope_ref"],
        "ccbom_id":ccbom["ccbom_id"],
        "ccbom_digest":digest(ccbom),
        "product_scope_contract_id":source_scope_contract["scope_contract_id"],
        "product_scope_contract_digest":digest(source_scope_contract),
        "product_authority_id":authority_id,
        "product_authority_digest":digest(product_authority),
        "engineering_binding_id":binding["binding_id"],
        "engineering_binding_digest":digest(binding),
        "closure_receipt_id":binding["closure_receipt_id"],
        "closure_digest":binding["closure_digest"],
        "registry_digest":binding["registry_digest"],
        "source_audit_states":binding["source_audit_states"],
        "authorized_consumer":"PAL",
        "source_item_status":binding["source_item_status"],
        "status":"ENGINEERING_CUSTODY_READY",
    }
    validate_schema(custody, "contracts/chemistry-product-engineering-custody-v1.schema.json", "CHEM_PRODUCT_ENGINEERING_CUSTODY_SCHEMA")
    return custody
