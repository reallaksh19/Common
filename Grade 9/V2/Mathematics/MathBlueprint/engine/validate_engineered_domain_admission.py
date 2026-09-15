#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "engine") not in sys.path:
    sys.path.insert(0, str(ROOT / "engine"))

from compile_mathematics_engineering_workbench import digest, load  # noqa: E402
from validate_canonical_domain_registry import validate_registry as validate_domain_registry  # noqa: E402
from validate_mathematics_engineering_binding import (  # noqa: E402
    MathematicsEngineeringBindingError,
    validate as validate_engineering_binding,
)


class MathematicsEngineeredDomainAdmissionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _schema_validate(doc: dict) -> None:
    schema = load("contracts/mathematics-engineered-domain-admission.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_ADMISSION_SCHEMA",
            f"{e.message}; path={list(e.path)}",
        )


def validate(
    admission: dict,
    *,
    domain_registry: dict | None = None,
    engineering_request: dict | None = None,
    engineering_manifest: dict | None = None,
    engineering_binding: dict | None = None,
    technical_registry: dict | None = None,
) -> dict:
    """Authorize Canonical Domain admission from current Engineering custody.

    The subtopic→gate mapping is runtime data. The validator accepts only exact
    gate IDs that are already present in the current Engineering closure. It
    never derives mappings from titles, remembered examples, aliases, or prose.
    """
    _schema_validate(admission)
    if admission["subject"] != "MATHEMATICS":
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_SUBJECT_MISMATCH",
            "subject must be MATHEMATICS",
        )

    domain_registry = domain_registry or load(admission["domain_registry_ref"])
    engineering_request = engineering_request or load(admission["engineering_request_ref"])
    engineering_manifest = engineering_manifest or load(admission["engineering_manifest_ref"])
    engineering_binding = engineering_binding or load(admission["engineering_binding_ref"])

    if domain_registry.get("subject") != "MATHEMATICS":
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_SUBJECT_MISMATCH",
            "domain registry is not MATHEMATICS",
        )

    try:
        domain_result = validate_domain_registry(domain_registry)
    except Exception as exc:
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_REGISTRY_INVALID",
            str(exc),
        ) from exc

    try:
        binding_result = validate_engineering_binding(
            engineering_binding,
            engineering_request,
            engineering_manifest,
            technical_registry,
        )
    except MathematicsEngineeringBindingError as exc:
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_BINDING_INVALID",
            str(exc),
        ) from exc

    if engineering_binding["downstream_consumer"] != "CANONICAL_DOMAIN_REGISTRY":
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_WRONG_CONSUMER",
            engineering_binding["downstream_consumer"],
        )

    rows = admission["subtopic_gate_map"]
    subtopic_ids = [row["subtopic_id"] for row in rows]
    if len(subtopic_ids) != len(set(subtopic_ids)):
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_DUPLICATE_SUBTOPIC_MAP",
            "duplicate subtopic mapping",
        )

    registry_subtopics = {asset["subtopic_id"] for asset in domain_registry["assets"]}
    mapped_subtopics = set(subtopic_ids)
    if mapped_subtopics != registry_subtopics:
        missing = sorted(registry_subtopics - mapped_subtopics)
        stale = sorted(mapped_subtopics - registry_subtopics)
        raise MathematicsEngineeredDomainAdmissionError(
            "MATH_ENG_DOMAIN_SUBTOPIC_COVERAGE_MISMATCH",
            f"missing={missing}, stale={stale}",
        )

    closure = set(binding_result["transitive_gate_ids"])
    for row in rows:
        if row["engineering_gate_id"] not in closure:
            raise MathematicsEngineeredDomainAdmissionError(
                "MATH_ENG_DOMAIN_GATE_OUTSIDE_CLOSURE",
                f"{row['subtopic_id']}->{row['engineering_gate_id']}",
            )

    return {
        "status": "PASS",
        "subject": "MATHEMATICS",
        "admission_id": admission["admission_id"],
        "domain_registry_id": domain_registry["registry_id"],
        "domain_registry_digest": digest(domain_registry),
        "domain_asset_count": domain_result["asset_count"],
        "engineering_binding_id": binding_result["binding_id"],
        "engineering_closure_receipt_id": binding_result["closure_receipt_id"],
        "engineering_closure_receipt_digest": binding_result["closure_receipt_digest"],
        "mapped_subtopic_count": len(rows),
        "authorized_gate_ids": sorted({row["engineering_gate_id"] for row in rows}),
        "technical_authorization": "ALLOWED",
        "publication_authorization": "NOT_IMPLIED",
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Validate Engineering-gated Mathematics Canonical Domain Registry admission"
    )
    ap.add_argument("--admission", required=True)
    args = ap.parse_args()
    admission = json.loads(Path(args.admission).read_text(encoding="utf-8"))
    print(json.dumps(validate(admission), indent=2))


if __name__ == "__main__":
    main()
