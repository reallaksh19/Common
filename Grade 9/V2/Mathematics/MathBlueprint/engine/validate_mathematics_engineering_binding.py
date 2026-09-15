#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

from compile_mathematics_engineering_workbench import (  # noqa: E402
    MathematicsEngineeringWorkbenchError,
    compile_closure,
    digest,
    load,
)


class MathematicsEngineeringBindingError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def validate(binding: dict, registry: dict | None = None, invariant_profile: dict | None = None) -> dict:
    schema = load("contracts/mathematics-engineering-binding.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(binding), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise MathematicsEngineeringBindingError("MATH_ENG_BIND_SCHEMA", f"{e.message}; path={list(e.path)}")
    if binding["subject"] != "MATHEMATICS":
        raise MathematicsEngineeringBindingError("MATH_ENG_BIND_SUBJECT", "binding subject must be MATHEMATICS")

    request = load(binding["request_ref"])
    manifest = load(binding["manifest_ref"])
    try:
        receipt = compile_closure(request, manifest, registry=registry, invariant_profile=invariant_profile)
    except MathematicsEngineeringWorkbenchError as exc:
        raise MathematicsEngineeringBindingError("MATH_ENG_BIND_RECOMPILE_FAILED", str(exc)) from exc

    if receipt["closure_status"] != "READY":
        raise MathematicsEngineeringBindingError("MATH_ENG_BIND_CLOSURE_BLOCKED", receipt["closure_status"])
    actual_receipt_digest = digest(receipt)
    checks = [
        ("closure_receipt_id", receipt["receipt_id"], "MATH_ENG_BIND_RECEIPT_ID_MISMATCH"),
        ("closure_receipt_digest", actual_receipt_digest, "MATH_ENG_BIND_RECEIPT_DIGEST_MISMATCH"),
        ("registry_digest", receipt["registry_digest"], "MATH_ENG_BIND_REGISTRY_DIGEST_MISMATCH"),
        ("invariant_profile_digest", receipt["invariant_profile_digest"], "MATH_ENG_BIND_PROFILE_DIGEST_MISMATCH"),
    ]
    for field, actual, code in checks:
        if binding[field] != actual:
            raise MathematicsEngineeringBindingError(code, f"expected {binding[field]} got {actual}")

    return {
        "status": "PASS",
        "subject": "MATHEMATICS",
        "binding_id": binding["binding_id"],
        "downstream_consumer": binding["downstream_consumer"],
        "closure_receipt_id": receipt["receipt_id"],
        "closure_receipt_digest": actual_receipt_digest,
        "registry_digest": receipt["registry_digest"],
        "invariant_profile_digest": receipt["invariant_profile_digest"],
        "technical_authorization": "ALLOWED",
        "publication_authorization": "NOT_IMPLIED",
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("binding")
    args = ap.parse_args()
    doc = json.loads(Path(args.binding).read_text(encoding="utf-8"))
    print(json.dumps(validate(doc), indent=2))
