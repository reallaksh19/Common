#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load  # noqa: E402
from compile_chemistry_product_engineering_custody import (  # noqa: E402
    ChemistryProductEngineeringCustodyError,
    compile_product_custody,
)


class ChemistryPALEngineeringError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryPALEngineeringError(code, message)


def validate_pal_engineering_ready(request: dict, manifest: dict, ccbom: dict, source_scope_contract: dict, product_authority: dict, custody: dict, **custody_kwargs) -> dict:
    try:
        jsonschema.validate(custody, load("contracts/chemistry-product-engineering-custody-v1.schema.json"))
    except jsonschema.ValidationError as exc:
        fail("CHEM_PAL_ENGINEERING_CUSTODY_SCHEMA", exc.message)
    try:
        expected = compile_product_custody(
            request,
            manifest,
            ccbom,
            source_scope_contract,
            product_authority,
            **custody_kwargs,
        )
    except ChemistryProductEngineeringCustodyError as exc:
        fail("CHEM_PAL_ENGINEERING_BLOCKED", f"{exc.code}: {exc.message}")
    if custody != expected:
        differing = sorted(k for k in set(custody) | set(expected) if custody.get(k) != expected.get(k))
        fail("CHEM_PAL_ENGINEERING_CUSTODY_STALE", f"custody differs from current state: {differing}")
    return {
        "status":"PASS",
        "ccbom_id":custody["ccbom_id"],
        "scope_ref":custody["scope_ref"],
        "product_scope_contract_id":custody["product_scope_contract_id"],
        "product_authority_id":custody["product_authority_id"],
        "engineering_binding_id":custody["engineering_binding_id"],
        "closure_digest":custody["closure_digest"],
        "registry_digest":custody["registry_digest"],
        "source_audit_count":len(custody["source_audit_states"]),
        "source_item_status":custody["source_item_status"],
    }
