#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import jsonschema

from compile_mathematics_engineering_workbench import digest as engineering_digest
from emit_stage_governance import digest as receipt_digest
from validate_engineered_domain_admission import validate as validate_engineered_domain_admission


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_SCHEMA = ROOT / "contracts" / "math-stage-governance-receipt.schema.json"
UNBOUND_REASON = "ENGINEERING_DOMAIN_ADMISSION_NOT_SUPPLIED"


def unbound_custody(reason: str = UNBOUND_REASON) -> dict:
    return {
        "status": "UNBOUND",
        "reason": reason,
    }


def custody_from_validation(result: dict) -> dict:
    if result.get("status") != "PASS" or result.get("technical_authorization") != "ALLOWED":
        raise ValueError("ENGINEERING_PRODUCT_CUSTODY_VALIDATION_NOT_AUTHORIZED")
    custody = {
        "status": "BOUND",
        "admission_id": result["admission_id"],
        "admission_digest": result["admission_digest"],
        "domain_registry_id": result["domain_registry_id"],
        "domain_registry_digest": result["domain_registry_digest"],
        "engineering_registry_digest": result["engineering_registry_digest"],
        "validator_contract_digest": result["validator_contract_digest"],
        "subtopic_gate_map_digest": result["subtopic_gate_map_digest"],
        "authorized_direct_gate_ids": list(result["authorized_direct_gate_ids"]),
        "authorization_custody": [dict(row) for row in result["authorization_custody"]],
    }
    custody["custody_digest"] = engineering_digest(custody)
    return custody


def build_custody(
    admission: dict,
    domain_registry: dict,
    *,
    engineering_authorizations: dict[str, dict] | None = None,
    technical_registry: dict | None = None,
) -> dict:
    result = validate_engineered_domain_admission(
        admission,
        domain_registry=domain_registry,
        engineering_authorizations=engineering_authorizations,
        technical_registry=technical_registry,
    )
    custody = custody_from_validation(result)
    expected_registry_digest = engineering_digest(domain_registry)
    if custody["domain_registry_id"] != domain_registry.get("registry_id"):
        raise ValueError("ENGINEERING_PRODUCT_CUSTODY_DOMAIN_REGISTRY_ID_MISMATCH")
    if custody["domain_registry_digest"] != expected_registry_digest:
        raise ValueError("ENGINEERING_PRODUCT_CUSTODY_DOMAIN_REGISTRY_DIGEST_MISMATCH")
    return custody


def load_custody(admission_path: str | Path | None, domain_registry: dict | None) -> dict:
    if admission_path is None:
        return unbound_custody()
    if domain_registry is None:
        raise ValueError("ENGINEERING_PRODUCT_CUSTODY_REQUIRES_DOMAIN_REGISTRY")
    admission = json.loads(Path(admission_path).read_text(encoding="utf-8"))
    return build_custody(admission, domain_registry)


def stamp_receipt(receipt: dict, custody: dict) -> dict:
    """Attach Engineering custody and recompute stage readiness deterministically.

    The low-level receipt primitive may be used by isolated unit tests without an
    Engineering admission. Real producer entrypoints call this function on every run,
    so an unstamped receipt cannot be mistaken for a release-capable producer output.
    """
    out = copy.deepcopy(receipt)
    primitive_ready = out.get("release_state") == "READY_FOR_CROSS_CORE_AUDIT"
    registry_bound = out.get("registry_binding", {}).get("status") == "BOUND"
    engineering_bound = custody.get("status") == "BOUND"
    if engineering_bound:
        if not registry_bound:
            raise ValueError("ENGINEERING_PRODUCT_CUSTODY_WITHOUT_DOMAIN_REGISTRY_BINDING")
        if custody.get("domain_registry_id") != out["registry_binding"].get("registry_ref"):
            raise ValueError("ENGINEERING_PRODUCT_CUSTODY_RECEIPT_REGISTRY_MISMATCH")
    out["engineering_custody"] = copy.deepcopy(custody)
    if out.get("release_state") == "BLOCKED_GOVERNANCE":
        pass
    elif primitive_ready and registry_bound and engineering_bound:
        out["release_state"] = "READY_FOR_CROSS_CORE_AUDIT"
    else:
        out["release_state"] = "UNBOUND_PRE_RELEASE"
    out["receipt_id"] = ""
    out["receipt_id"] = f"MATH-STAGE-GOV-{out['stage']}-{receipt_digest(out)[:16]}"
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(out, schema)
    return out


def assert_same_custody(left: dict, right: dict, *, code: str = "ENGINEERING_PRODUCT_CUSTODY_DRIFT") -> None:
    if left != right:
        raise ValueError(code)


def custody_summary(custody: dict) -> dict[str, Any]:
    if custody.get("status") != "BOUND":
        return {"status": "UNBOUND", "reason": custody.get("reason", UNBOUND_REASON)}
    return {
        "status": "BOUND",
        "admission_id": custody["admission_id"],
        "custody_digest": custody["custody_digest"],
        "authorization_count": len(custody["authorization_custody"]),
        "authorized_direct_gate_count": len(custody["authorized_direct_gate_ids"]),
    }
