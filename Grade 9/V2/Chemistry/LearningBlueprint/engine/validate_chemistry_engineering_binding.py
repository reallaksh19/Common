#!/usr/bin/env python3
"""Validation for Chemistry Engineering Custody Binding."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import compile_closure, digest, load  # noqa: E402
from compile_chemistry_engineering_workbench import resolve_manifest  # noqa: E402


class ChemistryEngineeringBindingError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def validate(
    binding: dict,
    request: dict,
    manifest: dict | None = None,
    registry: dict | None = None,
) -> dict:
    try:
        jsonschema.validate(binding, load("contracts/chemistry-engineering-authorization-binding.schema.json"))
    except jsonschema.ValidationError as exc:
        raise ChemistryEngineeringBindingError("CHEM_BIND_SCHEMA", exc.message) from exc

    if binding.get("status") != "ENGINEERING_AUTHORIZED":
        raise ChemistryEngineeringBindingError("CHEM_BIND_STATUS", f"Invalid binding status {binding.get('status')}")

    registry = registry or load(binding["registry_ref"])
    man = manifest or resolve_manifest(request, registry)
    receipt = compile_closure(request, man, registry=registry)

    if receipt["closure_status"] != "READY":
        raise ChemistryEngineeringBindingError("CHEM_BIND_CLOSURE_NOT_READY", "Closure status not READY")

    if binding["request_id"] != request["request_id"]:
        raise ChemistryEngineeringBindingError("CHEM_BIND_REQUEST_MISMATCH", "request_id mismatch")
    if binding["manifest_id"] != man["manifest_id"]:
        raise ChemistryEngineeringBindingError("CHEM_BIND_MANIFEST_MISMATCH", "manifest_id mismatch")
    if binding["closure_digest"] != receipt["closure_digest"]:
        raise ChemistryEngineeringBindingError("CHEM_BIND_CLOSURE_DIGEST_MISMATCH", "closure digest mismatch")

    return {
        "status": "PASS",
        "binding_id": binding["binding_id"],
        "closure_digest": binding["closure_digest"],
        "registry_digest": binding["registry_digest"],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate Chemistry Engineering Binding")
    ap.add_argument("--binding", required=True)
    ap.add_argument("--request", required=True)
    args = ap.parse_args()
    res = validate(load(args.binding), load(args.request))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
