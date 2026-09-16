#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from blueprint_common import digest, fail, load, validate_schema
from compile_physics_engineering_workbench import (
    compile_closure,
    compile_passport,
    load as load_engineering,
)
from validate_physics_engineering_binding import validate as validate_binding


NOTICE = (
    "This Engineering map is a derived visibility view of the exact technical authority bound to this product. "
    "It explains scope, prerequisites, depth, representations, misconceptions and verification obligations; "
    "it does not create physicsematical authority and does not authorize publication."
)


def _load_ref(ref: str, base_dir: Path | None) -> dict:
    path = Path(ref)
    if not path.is_absolute() and base_dir is not None:
        path = (base_dir / path).resolve()
    return load(path)


def _registry_index(registry: dict) -> dict[str, dict]:
    return {row["subtopic_id"]: row for row in registry["subtopic_gates"]}


def _learner_safe_gate_details(gate: dict) -> dict:
    return {
        "representations": [
            {
                "representation_id": row["representation_id"],
                "representation_type": row["representation_type"],
                "name": row["name"],
                "verification_method": row["verification_method"],
            }
            for row in gate.get("representations") or []
        ],
        "misconceptions": [
            {
                "misconception_id": row["misconception_id"],
                "incorrect_belief": row["incorrect_belief"],
                "required_technical_repair": row["required_technical_repair"],
            }
            for row in gate.get("misconceptions") or []
        ],
        "verification_obligations": list(gate.get("mandatory_verifications") or []),
    }


def validate_visibility_manifest(manifest: dict) -> dict:
    validate_schema(manifest, "physics-engineering-visibility-manifest.schema.json")
    if manifest["manifest_digest"] != digest(manifest, "manifest_digest"):
        fail("PHY_ENG_VISIBILITY_DIGEST_MISMATCH")
    expected_id = "PHY-ENG-VIS-" + digest({k: v for k, v in manifest.items() if k not in {"manifest_id", "manifest_digest"}})[:16]
    if manifest["manifest_id"] != expected_id:
        fail("PHY_ENG_VISIBILITY_ID_MISMATCH")
    if manifest["publication_authorization"] != "NOT_IMPLIED":
        fail("PHY_ENG_VISIBILITY_PUBLICATION_AUTHORITY_FORBIDDEN")
    if manifest["authorization_count"] != len(manifest["authorizations"]):
        fail("PHY_ENG_VISIBILITY_AUTHORIZATION_COUNT_DRIFT")
    if manifest["gate_count"] != len(manifest["gates"]):
        fail("PHY_ENG_VISIBILITY_GATE_COUNT_DRIFT")

    auth_ids = [row["authorization_id"] for row in manifest["authorizations"]]
    if len(auth_ids) != len(set(auth_ids)):
        fail("PHY_ENG_VISIBILITY_AUTHORIZATION_DUPLICATE")
    gate_ids = [row["gate_id"] for row in manifest["gates"]]
    if len(gate_ids) != len(set(gate_ids)):
        fail("PHY_ENG_VISIBILITY_GATE_DUPLICATE")
    auth_set = set(auth_ids)
    for gate in manifest["gates"]:
        unknown = sorted(set(gate["authorization_refs"]) - auth_set)
        if unknown:
            fail("PHY_ENG_VISIBILITY_GATE_AUTHORIZATION_UNKNOWN", ",".join(unknown))
        counts = gate["structure_counts"]
        if counts.get("representations") != len(gate["representations"]):
            fail("PHY_ENG_VISIBILITY_REPRESENTATION_COUNT_DRIFT", gate["gate_id"])
        if counts.get("misconceptions") != len(gate["misconceptions"]):
            fail("PHY_ENG_VISIBILITY_MISCONCEPTION_COUNT_DRIFT", gate["gate_id"])
        if counts.get("verification_obligations") != len(gate["verification_obligations"]):
            fail("PHY_ENG_VISIBILITY_VERIFICATION_COUNT_DRIFT", gate["gate_id"])
    return {
        "status": "PASS",
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": manifest["manifest_digest"],
        "authorization_count": manifest["authorization_count"],
        "gate_count": manifest["gate_count"],
        "publication_authorization": manifest["publication_authorization"],
    }


def compile_visibility_manifest(
    admission: dict,
    release_gate: dict,
    *,
    admission_base: Path | None = None,
    registry: dict | None = None,
) -> dict:
    if release_gate.get("status") != "PASS":
        fail("PHY_ENG_VISIBILITY_RELEASE_GATE_REQUIRED")
    if admission.get("subject") != "PHYSICS":
        fail("PHY_ENG_VISIBILITY_SUBJECT")
    if not admission.get("authorizations"):
        fail("PHY_ENG_VISIBILITY_AUTHORIZATION_REQUIRED")

    registry = registry or load_engineering("policies/physics-technical-engineering-gates.v1.json")
    gates_by_id = _registry_index(registry)
    authorization_rows = []
    gate_rows: dict[str, dict] = {}
    registry_digests = set()
    validator_digests = set()

    for auth in admission["authorizations"]:
        request = _load_ref(auth["engineering_request_ref"], admission_base)
        manifest = _load_ref(auth["engineering_manifest_ref"], admission_base)
        binding = _load_ref(auth["engineering_binding_ref"], admission_base)
        binding_audit = validate_binding(binding, request, manifest, registry)
        receipt = compile_closure(request, manifest, registry)
        passport = compile_passport(request, manifest, receipt, registry)
        if passport["blueprint_technical_authorization"] != "ALLOWED":
            fail("PHY_ENG_VISIBILITY_TECHNICAL_AUTHORIZATION_REQUIRED", auth["authorization_id"])
        if passport["publication_authorization"] != "NOT_IMPLIED":
            fail("PHY_ENG_VISIBILITY_PASSPORT_PUBLICATION_BOUNDARY", auth["authorization_id"])

        registry_digests.add(passport["registry_digest"])
        validator_digests.add(passport["validator_contract_digest"])
        authorization_rows.append({
            "authorization_id": auth["authorization_id"],
            "binding_id": binding["binding_id"],
            "request_id": request["request_id"],
            "engineering_depth": request["engineering_depth"],
            "direct_gate_ids": list(receipt["direct_gate_ids"]),
            "transitive_gate_ids": list(receipt["transitive_gate_ids"]),
            "closure_receipt_digest": binding_audit["closure_receipt_digest"],
            "passport_digest": digest(passport),
        })

        for surface in passport["engineering_surface"]["gates"]:
            gate_id = surface["gate_id"]
            gate = gates_by_id.get(gate_id)
            if gate is None:
                fail("PHY_ENG_VISIBILITY_GATE_MISSING_CURRENT_REGISTRY", gate_id)
            details = _learner_safe_gate_details(gate)
            if gate_id not in gate_rows:
                gate_rows[gate_id] = {
                    "gate_id": gate_id,
                    "scope_roles": [],
                    "authorization_refs": [],
                    "requested_engineering_depths": [],
                    "learner_title": surface["learner_title"],
                    "chapter": surface["chapter"],
                    "technical_state": surface["technical_state"],
                    "failure_codes": list(surface["failure_codes"]),
                    "prerequisite_ids": list(surface["prerequisite_ids"]),
                    "provenance": copy.deepcopy(surface["provenance"]),
                    "structure_counts": copy.deepcopy(surface["structure_counts"]),
                    "difficulty_profile": copy.deepcopy(surface["difficulty_profile"]),
                    "release_checklist_pass": surface["release_checklist_pass"],
                    **details,
                }
            row = gate_rows[gate_id]
            row["scope_roles"] = sorted(set(row["scope_roles"]) | {surface["scope_role"]})
            row["authorization_refs"] = sorted(set(row["authorization_refs"]) | {auth["authorization_id"]})
            row["requested_engineering_depths"] = sorted(set(row["requested_engineering_depths"]) | {request["engineering_depth"]})

    if len(registry_digests) != 1:
        fail("PHY_ENG_VISIBILITY_REGISTRY_CUSTODY_DISAGREEMENT")
    if len(validator_digests) != 1:
        fail("PHY_ENG_VISIBILITY_VALIDATOR_CUSTODY_DISAGREEMENT")

    out = {
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "manifest_id": "",
        "view_class": "DERIVED_ENGINEERING_PRODUCT_VISIBILITY",
        "authority": "NON_AUTHORITATIVE_VIEW_OF_BOUND_ENGINEERING_AUTHORITY",
        "visibility_purpose": "LEARNER_AND_AUTHOR_EXPLAINABILITY",
        "visibility_notice": NOTICE,
        "technical_authorization": "ALLOWED",
        "publication_authorization": "NOT_IMPLIED",
        "source_domain_admission_digest": digest(admission),
        "source_release_gate_digest": digest(release_gate),
        "registry_digest": next(iter(registry_digests)),
        "validator_contract_digest": next(iter(validator_digests)),
        "authorization_count": len(authorization_rows),
        "gate_count": len(gate_rows),
        "authorizations": authorization_rows,
        "gates": list(gate_rows.values()),
        "manifest_digest": "",
    }
    out["manifest_id"] = "PHY-ENG-VIS-" + digest({k: v for k, v in out.items() if k not in {"manifest_id", "manifest_digest"}})[:16]
    out["manifest_digest"] = digest(out, "manifest_digest")
    validate_visibility_manifest(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile learner/author Engineering visibility from exact bound Engineering custody")
    ap.add_argument("--engineering-admission", required=True)
    ap.add_argument("--release-gate", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    admission_path = Path(args.engineering_admission).resolve()
    result = compile_visibility_manifest(
        load(admission_path),
        load(args.release_gate),
        admission_base=admission_path.parent,
    )
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(validate_visibility_manifest(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
