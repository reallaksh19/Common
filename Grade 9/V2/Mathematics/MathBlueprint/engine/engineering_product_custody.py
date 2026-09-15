#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from compile_mathematics_engineering_workbench import digest as engineering_digest
from validate_engineered_domain_admission import validate as validate_engineered_domain_admission


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
