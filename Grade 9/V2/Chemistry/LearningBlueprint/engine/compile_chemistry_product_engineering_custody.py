#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_authorization_binding import ChemistryEngineeringBindingError, compile_binding
from compile_chemistry_engineering_closure import digest, load


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


def compile_product_custody(request: dict, manifest: dict, ccbom: dict) -> dict:
    validate_schema(ccbom, "contracts/content-bill-of-materials-v7.schema.json", "CHEM_PRODUCT_CCBOM_SCHEMA")

    if manifest.get("scope_ref") != ccbom.get("subtopic_id"):
        fail(
            "CHEM_PRODUCT_ENGINEERING_SCOPE_MISMATCH",
            f"manifest scope_ref {manifest.get('scope_ref')} != CCBOM subtopic_id {ccbom.get('subtopic_id')}",
        )

    try:
        binding = compile_binding(request, manifest)
    except ChemistryEngineeringBindingError as exc:
        fail("CHEM_PRODUCT_ENGINEERING_BLOCKED", f"{exc.code}: {exc.message}")

    if "PAL" not in binding.get("authorized_consumers", []):
        fail("CHEM_PRODUCT_PAL_NOT_AUTHORIZED", "engineering binding does not authorize PAL")

    custody = {
        "schema_version": "1.0.0",
        "custody_id": manifest["manifest_id"].replace(
            "CHEM-ENG-MAN-", "CHEM-PRODUCT-ENG-CUSTODY-", 1
        ),
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "scope_ref": manifest["scope_ref"],
        "ccbom_id": ccbom["ccbom_id"],
        "ccbom_digest": digest(ccbom),
        "engineering_binding_id": binding["binding_id"],
        "engineering_binding_digest": digest(binding),
        "closure_receipt_id": binding["closure_receipt_id"],
        "closure_digest": binding["closure_digest"],
        "registry_digest": binding["registry_digest"],
        "source_audit_states": binding["source_audit_states"],
        "authorized_consumer": "PAL",
        "source_item_status": binding["source_item_status"],
        "status": "ENGINEERING_CUSTODY_READY",
    }
    validate_schema(
        custody,
        "contracts/chemistry-product-engineering-custody-v1.schema.json",
        "CHEM_PRODUCT_ENGINEERING_CUSTODY_SCHEMA",
    )
    return custody


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("request")
    p.add_argument("manifest")
    p.add_argument("ccbom")
    p.add_argument("--out")
    a = p.parse_args()
    try:
        custody = compile_product_custody(load(a.request), load(a.manifest), load(a.ccbom))
    except ChemistryProductEngineeringCustodyError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
        return 1
    text = json.dumps(custody, indent=2) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
