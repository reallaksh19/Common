#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load
from compile_chemistry_product_engineering_custody import (
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


def validate_pal_engineering_ready(request: dict, manifest: dict, ccbom: dict, custody: dict) -> dict:
    try:
        jsonschema.validate(custody, load("contracts/chemistry-product-engineering-custody-v1.schema.json"))
    except jsonschema.ValidationError as exc:
        fail("CHEM_PAL_ENGINEERING_CUSTODY_SCHEMA", exc.message)

    try:
        expected = compile_product_custody(request, manifest, ccbom)
    except ChemistryProductEngineeringCustodyError as exc:
        fail("CHEM_PAL_ENGINEERING_BLOCKED", f"{exc.code}: {exc.message}")

    if custody != expected:
        differing = sorted(k for k in set(custody) | set(expected) if custody.get(k) != expected.get(k))
        fail("CHEM_PAL_ENGINEERING_CUSTODY_STALE", f"custody differs from current engineering state: {differing}")

    return {
        "status": "PASS",
        "ccbom_id": custody["ccbom_id"],
        "scope_ref": custody["scope_ref"],
        "engineering_binding_id": custody["engineering_binding_id"],
        "engineering_binding_digest": custody["engineering_binding_digest"],
        "closure_digest": custody["closure_digest"],
        "registry_digest": custody["registry_digest"],
        "source_audit_count": len(custody["source_audit_states"]),
        "source_item_status": custody["source_item_status"],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("request")
    p.add_argument("manifest")
    p.add_argument("ccbom")
    p.add_argument("custody")
    a = p.parse_args()
    try:
        result = validate_pal_engineering_ready(
            load(a.request), load(a.manifest), load(a.ccbom), load(a.custody)
        )
    except ChemistryPALEngineeringError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
