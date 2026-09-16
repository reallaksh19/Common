#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "engine") not in sys.path:
    sys.path.insert(0, str(ROOT / "engine"))

from compile_physics_engineering_workbench import digest, load  # noqa: E402
from validate_canonical_domain_registry import validate_registry as validate_domain_registry  # noqa: E402
from validate_physics_engineering_binding import (  # noqa: E402
    PhysicsEngineeringBindingError,
    validate as validate_engineering_binding,
)


class PhysicsEngineeredDomainAdmissionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _schema_validate(doc: dict) -> None:
    schema = load("contracts/physics-engineered-domain-admission.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_ADMISSION_SCHEMA",
            f"{e.message}; path={list(e.path)}",
        )


def _load_authorization_bundle(row: dict, injected: dict[str, dict] | None) -> tuple[dict, dict, dict]:
    auth_id = row["authorization_id"]
    if injected is not None:
        bundle = injected.get(auth_id)
        if bundle is None:
            raise PhysicsEngineeredDomainAdmissionError(
                "PHY_ENG_DOMAIN_AUTHORIZATION_INPUT_MISSING",
                auth_id,
            )
        try:
            return bundle["request"], bundle["manifest"], bundle["binding"]
        except KeyError as exc:
            raise PhysicsEngineeredDomainAdmissionError(
                "PHY_ENG_DOMAIN_AUTHORIZATION_INPUT_INCOMPLETE",
                f"{auth_id}:{exc.args[0]}",
            ) from exc
    return (
        load(row["engineering_request_ref"]),
        load(row["engineering_manifest_ref"]),
        load(row["engineering_binding_ref"]),
    )


def validate(
    admission: dict,
    *,
    domain_registry: dict | None = None,
    engineering_authorizations: dict[str, dict] | None = None,
    technical_registry: dict | None = None,
) -> dict:
    """Authorize Canonical Domain admission from one or more bounded Engineering closures.

    Every domain subtopic is mapped explicitly to one or more exact *direct* gate IDs.
    The corresponding authorization is independently recompiled against current
    Engineering authority. Prerequisite closure is preserved for technical custody,
    but a prerequisite-only gate cannot silently become a semantic admission target.

    No title matching, fuzzy matching, remembered aliases, topic-specific fallbacks,
    or conversational memory are used anywhere in this validator.
    """
    _schema_validate(admission)
    if admission["subject"] != "PHYSICS":
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_SUBJECT_MISMATCH",
            "subject must be PHYSICS",
        )

    domain_registry = domain_registry or load(admission["domain_registry_ref"])
    if domain_registry.get("subject") != "PHYSICS":
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_SUBJECT_MISMATCH",
            "domain registry is not PHYSICS",
        )

    try:
        domain_result = validate_domain_registry(domain_registry)
    except Exception as exc:
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_REGISTRY_INVALID",
            str(exc),
        ) from exc

    auth_rows = admission["authorizations"]
    auth_ids = [row["authorization_id"] for row in auth_rows]
    if len(auth_ids) != len(set(auth_ids)):
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_DUPLICATE_AUTHORIZATION_ID",
            "duplicate authorization_id",
        )

    auth_results: dict[str, dict] = {}
    direct_gate_owner: dict[str, str] = {}
    registry_digests: set[str] = set()
    validator_digests: set[str] = set()

    for row in auth_rows:
        auth_id = row["authorization_id"]
        request, manifest, binding = _load_authorization_bundle(row, engineering_authorizations)
        try:
            result = validate_engineering_binding(
                binding,
                request,
                manifest,
                technical_registry,
            )
        except PhysicsEngineeringBindingError as exc:
            raise PhysicsEngineeredDomainAdmissionError(
                "PHY_ENG_DOMAIN_BINDING_INVALID",
                f"{auth_id}:{exc}",
            ) from exc

        if binding["downstream_consumer"] != "CANONICAL_DOMAIN_REGISTRY":
            raise PhysicsEngineeredDomainAdmissionError(
                "PHY_ENG_DOMAIN_WRONG_CONSUMER",
                f"{auth_id}:{binding['downstream_consumer']}",
            )

        for gate_id in result["direct_gate_ids"]:
            previous = direct_gate_owner.get(gate_id)
            if previous is not None and previous != auth_id:
                raise PhysicsEngineeredDomainAdmissionError(
                    "PHY_ENG_DOMAIN_DIRECT_GATE_AUTHORIZATION_OVERLAP",
                    f"{gate_id}:{previous},{auth_id}",
                )
            direct_gate_owner[gate_id] = auth_id

        registry_digests.add(result["registry_digest"])
        validator_digests.add(result["validator_contract_digest"])
        auth_results[auth_id] = {
            "authorization_id": auth_id,
            "engineering_binding_id": result["binding_id"],
            "engineering_closure_receipt_id": result["closure_receipt_id"],
            "engineering_closure_receipt_digest": result["closure_receipt_digest"],
            "engineering_registry_digest": result["registry_digest"],
            "validator_contract_digest": result["validator_contract_digest"],
            "scope_refs": list(result["scope_refs"]),
            "direct_gate_ids": list(result["direct_gate_ids"]),
            "transitive_gate_ids": list(result["transitive_gate_ids"]),
        }

    if len(registry_digests) != 1:
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_ENGINEERING_REGISTRY_DRIFT",
            ",".join(sorted(registry_digests)),
        )
    if len(validator_digests) != 1:
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_VALIDATOR_CONTRACT_DRIFT",
            ",".join(sorted(validator_digests)),
        )

    rows = admission["subtopic_gate_map"]
    subtopic_ids = [row["subtopic_id"] for row in rows]
    if len(subtopic_ids) != len(set(subtopic_ids)):
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_DUPLICATE_SUBTOPIC_MAP",
            "duplicate subtopic mapping",
        )

    registry_subtopics = {asset["subtopic_id"] for asset in domain_registry["assets"]}
    mapped_subtopics = set(subtopic_ids)
    if mapped_subtopics != registry_subtopics:
        missing = sorted(registry_subtopics - mapped_subtopics)
        stale = sorted(mapped_subtopics - registry_subtopics)
        raise PhysicsEngineeredDomainAdmissionError(
            "PHY_ENG_DOMAIN_SUBTOPIC_COVERAGE_MISMATCH",
            f"missing={missing}, stale={stale}",
        )

    used_direct_by_auth: dict[str, set[str]] = {auth_id: set() for auth_id in auth_ids}
    normalized_rows: list[dict[str, Any]] = []
    for row in rows:
        seen_gates: set[str] = set()
        normalized_bindings: list[dict[str, str]] = []
        for gate_binding in row["gate_bindings"]:
            gate_id = gate_binding["engineering_gate_id"]
            auth_ref = gate_binding["authorization_ref"]
            if gate_id in seen_gates:
                raise PhysicsEngineeredDomainAdmissionError(
                    "PHY_ENG_DOMAIN_DUPLICATE_GATE_MAPPING",
                    f"{row['subtopic_id']}:{gate_id}",
                )
            seen_gates.add(gate_id)
            result = auth_results.get(auth_ref)
            if result is None:
                raise PhysicsEngineeredDomainAdmissionError(
                    "PHY_ENG_DOMAIN_AUTHORIZATION_REF_UNKNOWN",
                    f"{row['subtopic_id']}:{auth_ref}",
                )
            if gate_id not in set(result["direct_gate_ids"]):
                relation = "PREREQUISITE_ONLY" if gate_id in set(result["transitive_gate_ids"]) else "OUTSIDE_CLOSURE"
                raise PhysicsEngineeredDomainAdmissionError(
                    "PHY_ENG_DOMAIN_GATE_NOT_DIRECTLY_AUTHORIZED",
                    f"{row['subtopic_id']}->{gate_id}:{auth_ref}:{relation}",
                )
            used_direct_by_auth[auth_ref].add(gate_id)
            normalized_bindings.append({
                "engineering_gate_id": gate_id,
                "authorization_ref": auth_ref,
            })
        normalized_rows.append({
            "subtopic_id": row["subtopic_id"],
            "gate_bindings": sorted(
                normalized_bindings,
                key=lambda x: (x["engineering_gate_id"], x["authorization_ref"]),
            ),
        })

    for auth_id, result in auth_results.items():
        declared = set(result["direct_gate_ids"])
        unused = sorted(declared - used_direct_by_auth[auth_id])
        if unused:
            raise PhysicsEngineeredDomainAdmissionError(
                "PHY_ENG_DOMAIN_UNUSED_DIRECT_GATE_AUTHORITY",
                f"{auth_id}:{','.join(unused)}",
            )

    authorization_custody = [auth_results[auth_id] for auth_id in sorted(auth_results)]
    normalized_rows.sort(key=lambda x: x["subtopic_id"])
    authorized_direct_gate_ids = sorted({
        gate["engineering_gate_id"]
        for row in normalized_rows
        for gate in row["gate_bindings"]
    })

    return {
        "status": "PASS",
        "subject": "PHYSICS",
        "admission_id": admission["admission_id"],
        "admission_digest": digest(admission),
        "domain_registry_id": domain_registry["registry_id"],
        "domain_registry_digest": digest(domain_registry),
        "domain_asset_count": domain_result["asset_count"],
        "engineering_registry_digest": next(iter(registry_digests)),
        "validator_contract_digest": next(iter(validator_digests)),
        "authorization_custody": authorization_custody,
        "subtopic_gate_map": normalized_rows,
        "subtopic_gate_map_digest": digest(normalized_rows),
        "mapped_subtopic_count": len(normalized_rows),
        "authorized_direct_gate_ids": authorized_direct_gate_ids,
        "technical_authorization": "ALLOWED",
        "publication_authorization": "NOT_IMPLIED",
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Validate Engineering-gated Physics Canonical Domain Registry admission"
    )
    ap.add_argument("--admission", required=True)
    args = ap.parse_args()
    admission = json.loads(Path(args.admission).read_text(encoding="utf-8"))
    print(json.dumps(validate(admission), indent=2))


if __name__ == "__main__":
    main()
