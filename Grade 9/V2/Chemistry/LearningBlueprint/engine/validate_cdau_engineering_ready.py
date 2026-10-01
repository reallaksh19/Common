#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import digest, load  # noqa: E402
from compile_chemistry_engineering_authorization_binding import (  # noqa: E402
    ChemistryEngineeringBindingError,
    compile_binding,
)


class ChemistryCDAUEngineeringError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryCDAUEngineeringError(code, message)


def validate_engineered_cdau(request: dict, manifest: dict, cdau: dict, **closure_kwargs) -> dict:
    if manifest.get("scope_kind") != "SUBTOPIC":
        fail("CHEM_CDAU_ENGINEERING_SCOPE_KIND", "CDAU manifest must use SUBTOPIC")
    if manifest.get("scope_ref") != cdau.get("subtopic_id"):
        fail("CHEM_CDAU_ENGINEERING_SCOPE_MISMATCH", "manifest scope_ref and CDAU subtopic differ")
    if "CDAU" not in manifest.get("downstream_consumers", []):
        fail("CHEM_CDAU_ENGINEERING_NOT_AUTHORIZED", "manifest does not authorize CDAU")
    try:
        binding = compile_binding(request, manifest, **closure_kwargs)
    except ChemistryEngineeringBindingError as exc:
        fail("CHEM_CDAU_ENGINEERING_BLOCKED", f"{exc.code}: {exc.message}")
    if "CDAU" not in binding["authorized_consumers"]:
        fail("CHEM_CDAU_ENGINEERING_NOT_AUTHORIZED", "binding does not authorize CDAU")
    try:
        jsonschema.validate(cdau, load("contracts/cdau-governance-v6.schema.json"))
    except jsonschema.ValidationError as exc:
        fail("CHEM_CDAU_SCHEMA", exc.message)
    return {
        "status":"PASS",
        "subtopic_id":cdau["subtopic_id"],
        "engineering_binding_id":binding["binding_id"],
        "engineering_binding_digest":digest(binding),
        "engineering_closure_receipt_id":binding["closure_receipt_id"],
        "engineering_closure_digest":binding["closure_digest"],
        "source_audit_states":binding["source_audit_states"],
        "source_item_status":binding["source_item_status"],
    }
