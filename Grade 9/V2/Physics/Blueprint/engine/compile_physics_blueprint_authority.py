#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = ROOT.parents[3]
SHARED_GATE = REPO / "Grade 9" / "V2" / "Shared" / "EngineeringGate"
sys.path.insert(0, str(SHARED_GATE / "engine"))

from evaluate_readiness import build_envelope  # noqa: E402


class PhysicsBlueprintAuthorityError(Exception):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def _schema() -> dict[str, Any]:
    return json.loads((ROOT / "contracts" / "physics-blueprint-authority-projection.schema.json").read_text(encoding="utf-8"))


def compile_physics_blueprint_authority(
    scoped_evidence: dict[str, Any],
    engineering_request: dict[str, Any],
    engineering_manifest: dict[str, Any],
    engineering_receipt: dict[str, Any],
    domain_receipt: dict[str, Any],
) -> dict[str, Any]:
    if engineering_request.get("subject") != "PHYSICS":
        raise PhysicsBlueprintAuthorityError("PHY_BP_AUTH_NON_PHYSICS_REQUEST")
    grades = set(int(x) for x in engineering_request.get("curriculum_scope", {}).get("grades", []))
    if int(scoped_evidence["grade"]) not in grades:
        raise PhysicsBlueprintAuthorityError("PHY_BP_AUTH_SCOPE_ENGINEERING_GRADE_MISMATCH")
    if set(scoped_evidence["required_gate_ids"]) != set(engineering_manifest.get("required_gate_ids", [])):
        raise PhysicsBlueprintAuthorityError("PHY_BP_AUTH_SCOPE_ENGINEERING_GATE_MISMATCH")

    readiness = build_envelope(engineering_request, engineering_manifest, engineering_receipt, domain_receipt)
    publication_permission = readiness["consumer_permissions"].get("PUBLICATION")
    if readiness["publication_authorization"] != "NOT_IMPLIED":
        raise PhysicsBlueprintAuthorityError("PHY_BP_AUTH_ENGINEERING_PUBLICATION_ESCALATION")
    if publication_permission and publication_permission["status"] != "NOT_AUTHORIZED":
        raise PhysicsBlueprintAuthorityError("PHY_BP_AUTH_PUBLICATION_CONSUMER_ESCALATION")

    curriculum_binding = scoped_evidence["curriculum_binding"]
    projection = {
        "schema_version": "1.0.0",
        "projection_id": "PHY-BP-AUTH-" + scoped_evidence["receipt_id"].removeprefix("SCOPED-EVIDENCE-PHY-"),
        "authority_class": "PHYSICS_BLUEPRINT_AUTHORITY_PROJECTION",
        "scope": {
            "scope_digest": scoped_evidence["scope_digest"],
            "curriculum_status": scoped_evidence["curriculum_status"],
            "curriculum_binding_state": curriculum_binding["state"],
            "curriculum_binding_id": curriculum_binding["binding_id"],
            "curriculum_binding_digest": curriculum_binding["binding_digest"],
        },
        "engineering_gate": {
            "envelope_id": readiness["envelope_id"],
            "envelope_digest": readiness["envelope_digest"],
            "dimensions": dict(readiness["dimensions"]),
            "consumer_permissions": dict(readiness["consumer_permissions"]),
            "publication_authorization": readiness["publication_authorization"],
        },
        "release_authority": "NOT_GRANTED_BY_PROJECTION",
        "projection_digest": "",
    }
    projection["projection_digest"] = digest({k: v for k, v in projection.items() if k != "projection_digest"})
    Draft202012Validator(_schema()).validate(projection)
    return projection
