"""V3.5-R14 WP1/U1: typed, reference-only identity validation.

This is an additive schema candidate, not a DELP projector, provider oracle,
Owner authentication, reviewer decision, writer permit or successor lease.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

SCHEMA_NAME = "relay-lifecycle-source-identity-v1"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "lifecycle-v35" / "lifecycle-identity-v1.schema.json"


class IdentityContractError(ValueError):
    """Invalid or ambiguous source identity; fail closed."""


def _safe_path(value: str) -> bool:
    return (
        bool(value)
        and not value.startswith("/")
        and "\\" not in value
        and not any(part in {"", ".", ".."} for part in value.split("/"))
        and not any(ord(c) < 32 for c in value)
    )


def _schema() -> dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as stream:
        schema = json.load(stream)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_identity(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Check typed structural refs; return a fingerprint, NEVER attested authority.

    All REFERENCED values are caller assertions. The API does not resolve a
    ref against GitHub, validate graph approval, infer evidence policy, or
    mutate DELP progress. Cross-repository references are rejected at U1.
    """
    if not isinstance(payload, dict):
        raise IdentityContractError("IDENTITY_OBJECT_REQUIRED")
    faults = sorted(
        Draft202012Validator(_schema()).iter_errors(payload),
        key=lambda e: (tuple(str(x) for x in e.path), e.message),
    )
    if faults:
        first = faults[0]
        where = ".".join(str(p) for p in first.path) or "$"
        raise IdentityContractError(f"SCHEMA_INVALID:{where}:{first.message}")
    repo = payload["programme"]["repository"]
    for name in ("graph_source", "session_source", "candidate_source"):
        if payload[name]["repository"] != repo:
            raise IdentityContractError(f"CROSS_REPOSITORY_REFERENCE:{name}")
    graph = payload["graph_source"]
    if graph["path"] is not None and not _safe_path(graph["path"]):
        raise IdentityContractError("UNSAFE_GRAPH_PATH")
    # A matching byte string in two different roles is allowed: roles remain
    # typed, and no role may be promoted to another role or to authority.
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {
        "schema": SCHEMA_NAME,
        "identity_sha256": "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "identity_grade": "CALLER_REFERENCED_UNATTESTED",
        "graph_approval": "NOT_EVALUATED",
        "provider_acquisition": "NOT_EVALUATED",
        "evidence_acceptance": "NOT_EVALUATED",
        "owner_authorization": "NOT_GRANTED",
        "writer_authorization": "NOT_GRANTED",
    }
