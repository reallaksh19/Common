#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_authorization_binding import compile_binding  # noqa: E402
from compile_chemistry_engineering_closure import compile_closure, digest as engineering_digest, load  # noqa: E402
from validate_chemistry_core_source_scope import validate_core_source_scope  # noqa: E402

OBLIGATION_SCHEMA_REL = "contracts/chemistry-engineering-blueprint-obligations.schema.json"
AUTH_SCHEMA_REL = "contracts/chemistry-core-authority.schema.json"
CUSTODY_SCHEMA_REL = "contracts/chemistry-core-product-custody.schema.json"


class ChemistryCoreProductCustodyError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryCoreProductCustodyError(code, message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def digest_without(obj: dict[str, Any], field: str) -> str:
    payload = copy.deepcopy(obj)
    payload.pop(field, None)
    return digest(payload)


def _schema(obj: dict[str, Any], rel: str, code: str) -> None:
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def compile_core_product_custody(
    request: dict[str, Any],
    manifest: dict[str, Any],
    obligation_packet: dict[str, Any],
    source_scope: dict[str, Any],
    authority: dict[str, Any],
    *,
    registry: dict[str, Any] | None = None,
    source_audit_payloads: dict[str, dict[str, Any]] | None = None,
    research_dossier: dict[str, Any] | None = None,
    claim_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _schema(obligation_packet, OBLIGATION_SCHEMA_REL, "CHEM_CORE_CUSTODY_OBLIGATION_SCHEMA")
    _schema(authority, AUTH_SCHEMA_REL, "CHEM_CORE_CUSTODY_AUTHORITY_SCHEMA")
    if obligation_packet["packet_digest"] != digest_without(obligation_packet, "packet_digest"):
        fail("CHEM_CORE_CUSTODY_OBLIGATION_DIGEST_MISMATCH")
    if authority["authority_digest"] != digest_without(authority, "authority_digest"):
        fail("CHEM_CORE_CUSTODY_AUTHORITY_DIGEST_MISMATCH")

    closure_kwargs = {
        "registry": registry,
        "source_audit_payloads": source_audit_payloads,
        "research_dossier": research_dossier,
        "claim_ledger": claim_ledger,
    }
    receipt = compile_closure(request, manifest, **closure_kwargs)
    if receipt["closure_status"] != "READY":
        fail("CHEM_CORE_CUSTODY_ENGINEERING_NOT_READY")
    binding = compile_binding(request, manifest, **closure_kwargs)
    if "PAL" not in binding["authorized_consumers"]:
        fail("CHEM_CORE_CUSTODY_PAL_NOT_AUTHORIZED")

    if obligation_packet["request_id"] != request["request_id"] or obligation_packet["manifest_id"] != manifest["manifest_id"]:
        fail("CHEM_CORE_CUSTODY_OBLIGATION_REQUEST_DRIFT")
    if obligation_packet["engineering_binding_id"] != binding["binding_id"]:
        fail("CHEM_CORE_CUSTODY_BINDING_ID_DRIFT")
    if obligation_packet["engineering_binding_digest"] != engineering_digest(binding):
        fail("CHEM_CORE_CUSTODY_BINDING_DIGEST_DRIFT")
    if obligation_packet["closure_digest"] != receipt["closure_digest"]:
        fail("CHEM_CORE_CUSTODY_CLOSURE_DRIFT")
    if obligation_packet["registry_digest"] != receipt["registry_digest"]:
        fail("CHEM_CORE_CUSTODY_REGISTRY_DRIFT")
    if authority["obligation_packet_id"] != obligation_packet["packet_id"] or authority["obligation_packet_digest"] != obligation_packet["packet_digest"]:
        fail("CHEM_CORE_CUSTODY_AUTHORITY_OBLIGATION_DRIFT")
    if authority["subtopic_id"] != manifest["scope_ref"]:
        fail("CHEM_CORE_CUSTODY_SUBTOPIC_DRIFT")
    if source_scope["subtopic_id"] != authority["subtopic_id"] or source_scope["product_mode"] != authority["product_mode"]:
        fail("CHEM_CORE_CUSTODY_SCOPE_AUTHORITY_DRIFT")

    gate_id = source_scope["gate_id"]
    if gate_id not in obligation_packet["direct_gate_ids"]:
        fail("CHEM_CORE_CUSTODY_SOURCE_GATE_NOT_DIRECT", gate_id)
    if len(obligation_packet["direct_gate_ids"]) != 1:
        fail("CHEM_CORE_CUSTODY_MULTI_DIRECT_GATE_UNSUPPORTED", "compile one core product per direct engineering gate")

    audit_state = next((row for row in binding["source_audit_states"] if row["gate_id"] == gate_id), None)
    if audit_state is None:
        fail("CHEM_CORE_CUSTODY_SOURCE_AUDIT_MISSING", gate_id)
    if audit_state["audit_role"] != "PRODUCTION_SOURCE_AUDIT":
        fail("CHEM_CORE_CUSTODY_SOURCE_AUDIT_NOT_PRODUCTION")
    if source_scope["source_audit_ref"] != audit_state["audit_ref"]:
        fail("CHEM_CORE_CUSTODY_SOURCE_AUDIT_REF_DRIFT")

    audit = None
    if source_audit_payloads:
        audit = source_audit_payloads.get(audit_state["audit_ref"])
    if audit is None:
        audit = load(audit_state["audit_ref"])
    if engineering_digest(audit) != audit_state["audit_digest"]:
        fail("CHEM_CORE_CUSTODY_SOURCE_AUDIT_DIGEST_DRIFT")

    current_registry = registry if registry is not None else load(manifest["registry_ref"])
    scope_result = validate_core_source_scope(source_scope, audit, authority, current_registry)

    suffix = manifest["manifest_id"].replace("CHEM-ENG-MAN-", "", 1)
    custody = {
        "schema_version": "1.0.0",
        "custody_id": f"CHEM-CORE-CUSTODY-{suffix}-{authority['product_mode']}",
        "subject": "CHEMISTRY",
        "product_mode": authority["product_mode"],
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "subtopic_id": authority["subtopic_id"],
        "engineering_binding_id": binding["binding_id"],
        "engineering_binding_digest": engineering_digest(binding),
        "closure_receipt_id": receipt["receipt_id"],
        "closure_digest": receipt["closure_digest"],
        "registry_digest": receipt["registry_digest"],
        "obligation_packet_id": obligation_packet["packet_id"],
        "obligation_packet_digest": obligation_packet["packet_digest"],
        "source_scope_contract_id": source_scope["scope_contract_id"],
        "source_scope_contract_digest": digest(source_scope),
        "core_authority_id": authority["authority_id"],
        "core_authority_digest": authority["authority_digest"],
        "source_audit_ref": audit_state["audit_ref"],
        "source_audit_digest": audit_state["audit_digest"],
        "status": "CORE_PRODUCT_CUSTODY_READY",
        "custody_digest": "",
    }
    custody["custody_digest"] = digest_without(custody, "custody_digest")
    _schema(custody, CUSTODY_SCHEMA_REL, "CHEM_CORE_CUSTODY_SCHEMA")
    if scope_result["status"] != "PASS":
        fail("CHEM_CORE_CUSTODY_SCOPE_NOT_PASS")
    return custody
