#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import compile_closure, load  # noqa: E402


class ChemistryEngineeringBindingError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def compile_binding(request: dict, manifest: dict, **closure_kwargs) -> dict:
    receipt = compile_closure(request, manifest, **closure_kwargs)
    if receipt["closure_status"] != "READY":
        raise ChemistryEngineeringBindingError(
            "CHEM_BIND_ENGINEERING_BLOCKED",
            f"closure blocked: {[b['code'] for b in receipt['blockers']]}",
        )
    binding = {
        "schema_version": "2.0.0",
        "binding_id": manifest["manifest_id"].replace("CHEM-ENG-MAN-", "CHEM-ENG-BIND-", 1),
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "scope_ref": manifest["scope_ref"],
        "registry_ref": receipt["registry_ref"],
        "registry_digest": receipt["registry_digest"],
        "source_audit_states": receipt["source_audit_states"],
        "closure_receipt_id": receipt["receipt_id"],
        "closure_digest": receipt["closure_digest"],
        "authorized_consumers": manifest["downstream_consumers"],
        "source_item_status": receipt["source_item_status"],
        "status": "ENGINEERING_AUTHORIZED",
    }
    if "topology_id" in receipt:
        binding.update({
            "topology_id": receipt["topology_id"],
            "topology_digest": receipt["topology_digest"],
            "topology_extension_id": receipt["topology_extension_id"],
            "topology_extension_digest": receipt["topology_extension_digest"],
        })
    try:
        jsonschema.validate(binding, load("contracts/chemistry-engineering-authorization-binding.schema.json"))
    except jsonschema.ValidationError as exc:
        raise ChemistryEngineeringBindingError("CHEM_BIND_SCHEMA", exc.message) from exc
    return binding
