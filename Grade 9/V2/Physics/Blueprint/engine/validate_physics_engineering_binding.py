#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

from compile_physics_engineering_workbench import (  # noqa: E402
    PhysicsEngineeringWorkbenchError,
    compile_closure,
    digest,
    load,
    resolve_manifest,
)


class PhysicsEngineeringBindingError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _schema_validate(binding: dict) -> None:
    schema = load("contracts/physics-engineering-binding.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(binding), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise PhysicsEngineeringBindingError("PHY_ENG_BIND_SCHEMA", f"{e.message}; path={list(e.path)}")


def validate(
    binding: dict,
    request: dict,
    manifest: dict | None = None,
    registry: dict | None = None,
) -> dict:
    """Recompile Engineering authorization from current authority and verify custody.

    Bindings are runtime artifacts. They do not carry topic-specific file refs and
    they never reconstruct gate semantics from memory.
    """
    _schema_validate(binding)
    if binding["subject"] != "PHYSICS":
        raise PhysicsEngineeringBindingError("PHY_ENG_BIND_SUBJECT", "binding subject must be PHYSICS")

    try:
        current_manifest = manifest or resolve_manifest(request, registry)
        receipt = compile_closure(request, current_manifest, registry)
    except PhysicsEngineeringWorkbenchError as exc:
        raise PhysicsEngineeringBindingError("PHY_ENG_BIND_RECOMPILE_FAILED", str(exc)) from exc

    if receipt["closure_status"] != "READY":
        raise PhysicsEngineeringBindingError("PHY_ENG_BIND_CLOSURE_BLOCKED", receipt["closure_status"])

    checks = [
        ("request_digest", digest(request), "PHY_ENG_BIND_REQUEST_DIGEST_MISMATCH"),
        ("manifest_digest", digest(current_manifest), "PHY_ENG_BIND_MANIFEST_DIGEST_MISMATCH"),
        ("closure_receipt_id", receipt["receipt_id"], "PHY_ENG_BIND_RECEIPT_ID_MISMATCH"),
        ("closure_receipt_digest", digest(receipt), "PHY_ENG_BIND_RECEIPT_DIGEST_MISMATCH"),
        ("registry_digest", receipt["registry_digest"], "PHY_ENG_BIND_REGISTRY_DIGEST_MISMATCH"),
        ("validator_contract_digest", receipt["validator_contract_digest"], "PHY_ENG_BIND_VALIDATOR_DIGEST_MISMATCH"),
        ("scope_refs", receipt["scope_refs"], "PHY_ENG_BIND_SCOPE_MISMATCH"),
        ("direct_gate_ids", receipt["direct_gate_ids"], "PHY_ENG_BIND_DIRECT_GATE_MISMATCH"),
        ("transitive_gate_ids", receipt["transitive_gate_ids"], "PHY_ENG_BIND_CLOSURE_MISMATCH"),
    ]
    for field, actual, code in checks:
        if binding[field] != actual:
            raise PhysicsEngineeringBindingError(code, f"expected {binding[field]!r} got {actual!r}")

    return {
        "status": "PASS",
        "subject": "PHYSICS",
        "binding_id": binding["binding_id"],
        "downstream_consumer": binding["downstream_consumer"],
        "closure_receipt_id": receipt["receipt_id"],
        "closure_receipt_digest": digest(receipt),
        "registry_digest": receipt["registry_digest"],
        "validator_contract_digest": receipt["validator_contract_digest"],
        "scope_refs": receipt["scope_refs"],
        "direct_gate_ids": receipt["direct_gate_ids"],
        "transitive_gate_ids": receipt["transitive_gate_ids"],
        "technical_authorization": "ALLOWED",
        "publication_authorization": "NOT_IMPLIED",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate runtime Physics Engineering custody binding")
    ap.add_argument("--binding", required=True)
    ap.add_argument("--request", required=True)
    ap.add_argument("--manifest")
    args = ap.parse_args()
    binding = json.loads(Path(args.binding).read_text(encoding="utf-8"))
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8")) if args.manifest else None
    print(json.dumps(validate(binding, request, manifest), indent=2))


if __name__ == "__main__":
    main()
