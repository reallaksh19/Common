#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_REL = "policies/mathematics-technical-engineering-gates.v1.json"
ENGINEERING_SCHEMA_REL = "contracts/mathematics-technical-engineering-gate.schema.json"
ENGINEERING_VALIDATOR_PATH = ROOT / "engine" / "validate_mathematics_engineering_gates.py"
ENGINEERING_COMPOSER_PATH = ROOT / "engine" / "engineering_registry_composition.py"
ENGINEERING_INVARIANT_PROFILE_PATH = ROOT / "policies" / "mathematics-engineering-gate-invariants.v1.json"
ENGINEERING_DEPTH_POLICY_PATH = ROOT / "policies" / "mathematics-engineering-depth-policy.v1.json"

from engineering_registry_composition import (  # noqa: E402
    BASE_REGISTRY_REL,
    CANONICAL_EXTENSION_RELS,
    EXTENSION_CATALOG_REL,
    load_canonical_engineering_registry,
)
from validate_mathematics_engineering_gates import (  # noqa: E402
    MathematicsEngineeringGateValidationError,
    validate as validate_engineering_registry,
)


class MathematicsEngineeringWorkbenchError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _resolved_path(rel_or_path: str | Path) -> Path:
    p = Path(rel_or_path)
    if not p.is_absolute():
        p = ROOT / p
    return p


def load(rel_or_path: str | Path) -> dict:
    p = _resolved_path(rel_or_path)
    if p.resolve() == (ROOT / BASE_REGISTRY_REL).resolve():
        return load_canonical_engineering_registry(p)
    return json.loads(p.read_text(encoding="utf-8"))


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _bytes_digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def engineering_validator_contract_digest() -> str:
    """Digest every executable/data input that defines Engineering admission."""
    payload = {
        "schema": load(ENGINEERING_SCHEMA_REL),
        "validator_source_sha256": _bytes_digest(ENGINEERING_VALIDATOR_PATH.read_bytes()),
        "registry_composer_source_sha256": _bytes_digest(ENGINEERING_COMPOSER_PATH.read_bytes()),
        "extension_catalog_source_sha256": _bytes_digest((ROOT / EXTENSION_CATALOG_REL).read_bytes()),
        "invariant_profile_source_sha256": _bytes_digest(ENGINEERING_INVARIANT_PROFILE_PATH.read_bytes()),
        "depth_policy_source_sha256": _bytes_digest(ENGINEERING_DEPTH_POLICY_PATH.read_bytes()),
        "canonical_extension_source_sha256": [
            _bytes_digest((ROOT / rel).read_bytes()) for rel in CANONICAL_EXTENSION_RELS
        ],
    }
    return digest(payload)


def schema_validate(doc: dict, schema_name: str, code: str) -> None:
    schema = load(f"contracts/{schema_name}")
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise MathematicsEngineeringWorkbenchError(code, f"{e.message}; path={list(e.path)}")


def _validate_authoritative_registry(registry: dict) -> None:
    if registry.get("registry_id") != "REG-MATH-TECH-GATE-V1":
        raise MathematicsEngineeringWorkbenchError(
            "MATH_ENG_REGISTRY_ID_MISMATCH",
            f"expected REG-MATH-TECH-GATE-V1, got {registry.get('registry_id')}",
        )
    try:
        validate_engineering_registry(registry)
    except MathematicsEngineeringGateValidationError as exc:
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_REGISTRY_INVALID", str(exc)) from exc


def _gate_index(registry: dict) -> dict[str, dict]:
    return {gate["subtopic_id"]: gate for gate in registry["subtopic_gates"]}


def _load_depth_policy() -> dict:
    policy = json.loads(ENGINEERING_DEPTH_POLICY_PATH.read_text(encoding="utf-8"))
    if (
        policy.get("schema_version") != "1.0.0"
        or policy.get("subject") != "MATHEMATICS"
        or set(policy.get("profiles", {})) != {"FOUNDATION", "STANDARD", "RESEARCH"}
    ):
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_DEPTH_POLICY_INVALID", "top-level policy shape")

    required = {
        "min_reasoning_steps",
        "min_model_conditions",
        "min_misconceptions",
        "min_required_transformations",
        "min_falsification_cases",
        "required_transformation_roles",
        "require_non_provisional_provenance",
    }
    for depth, row in policy["profiles"].items():
        if set(row) != required:
            raise MathematicsEngineeringWorkbenchError(
                "MATH_ENG_DEPTH_POLICY_INVALID",
                f"{depth}: fields={sorted(row)}",
            )
        for key in (
            "min_reasoning_steps",
            "min_model_conditions",
            "min_misconceptions",
            "min_required_transformations",
            "min_falsification_cases",
        ):
            value = row[key]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise MathematicsEngineeringWorkbenchError(
                    "MATH_ENG_DEPTH_POLICY_INVALID",
                    f"{depth}:{key}={value!r}",
                )
        roles = row["required_transformation_roles"]
        if not isinstance(roles, list) or len(roles) != len(set(roles)) or any(
            not isinstance(role, str) or not role for role in roles
        ):
            raise MathematicsEngineeringWorkbenchError(
                "MATH_ENG_DEPTH_POLICY_INVALID",
                f"{depth}:required_transformation_roles",
            )
        if not isinstance(row["require_non_provisional_provenance"], bool):
            raise MathematicsEngineeringWorkbenchError(
                "MATH_ENG_DEPTH_POLICY_INVALID",
                f"{depth}:require_non_provisional_provenance",
            )
    return policy


def _depth_failures(gate: dict, engineering_depth: str) -> list[str]:
    policy = _load_depth_policy()
    profile = policy["profiles"].get(engineering_depth)
    if profile is None:
        raise MathematicsEngineeringWorkbenchError(
            "MATH_ENG_DEPTH_UNKNOWN",
            engineering_depth,
        )

    failures: list[str] = []
    checks = (
        ("reasoning_sequence", "min_reasoning_steps", "MATH_ENG_DEPTH_REASONING_INSUFFICIENT"),
        ("model_conditions", "min_model_conditions", "MATH_ENG_DEPTH_MODEL_CONDITIONS_INSUFFICIENT"),
        ("misconceptions", "min_misconceptions", "MATH_ENG_DEPTH_MISCONCEPTION_COVERAGE_INSUFFICIENT"),
        ("required_transformations", "min_required_transformations", "MATH_ENG_DEPTH_TRANSFORMATIONS_INSUFFICIENT"),
        ("falsification_cases", "min_falsification_cases", "MATH_ENG_DEPTH_FALSIFICATION_INSUFFICIENT"),
    )
    for collection, minimum_key, code in checks:
        if len(gate.get(collection) or []) < profile[minimum_key]:
            failures.append(code)

    required_roles = set(profile["required_transformation_roles"])
    actual_roles = {
        row.get("target_core_role")
        for row in gate.get("required_transformations") or []
        if row.get("target_core_role")
    }
    if not required_roles.issubset(actual_roles):
        failures.append("MATH_ENG_DEPTH_TRANSFORMATION_COVERAGE_INSUFFICIENT")

    if profile["require_non_provisional_provenance"]:
        if gate.get("provenance", {}).get("claim_status") == "PROVISIONAL":
            failures.append("MATH_ENG_DEPTH_PROVENANCE_PROVISIONAL")

    return failures


def resolve_manifest(request: dict, registry: dict | None = None) -> dict:
    """Resolve Blueprint scope to Engineering Gate IDs using registry data only.

    No title matching, fuzzy matching, remembered topic aliases, or case-specific
    fallback is permitted. ENGINEERING_GATE scopes resolve by exact identity;
    BUCKET scopes resolve only through gate.linked_buckets.
    """
    schema_validate(request, "mathematics-engineering-request.schema.json", "MATH_ENG_REQUEST_SCHEMA")
    if request["subject"] != "MATHEMATICS":
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_SUBJECT_MISMATCH", "request is not MATHEMATICS")

    registry = registry or load(REGISTRY_REL)
    _validate_authoritative_registry(registry)
    gates = registry["subtopic_gates"]
    by_id = _gate_index(registry)

    if request["scope_kind"] == "ENGINEERING_GATE":
        missing = [ref for ref in request["scope_refs"] if ref not in by_id]
        if missing:
            raise MathematicsEngineeringWorkbenchError(
                "MATH_ENG_SCOPE_UNMAPPED",
                f"unknown exact Engineering Gate refs: {missing}",
            )
        direct_gate_ids = list(request["scope_refs"])
        resolution_mode = "GATE_IDENTITY"
    elif request["scope_kind"] == "BUCKET":
        resolved: list[str] = []
        for scope_ref in request["scope_refs"]:
            matches = [
                gate["subtopic_id"]
                for gate in gates
                if scope_ref in set(gate.get("linked_buckets") or [])
            ]
            if not matches:
                raise MathematicsEngineeringWorkbenchError(
                    "MATH_ENG_SCOPE_UNMAPPED",
                    f"bucket {scope_ref} has no exact linked_buckets mapping in Engineering registry",
                )
            for gate_id in matches:
                if gate_id not in resolved:
                    resolved.append(gate_id)
        direct_gate_ids = resolved
        resolution_mode = "REGISTRY_LINKED_BUCKET"
    else:
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_SCOPE_KIND_INVALID", request["scope_kind"])

    suffix = request["request_id"].removeprefix("MATH-ENG-REQ-")
    manifest = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "manifest_id": f"MATH-ENG-MANIFEST-{suffix}",
        "request_id": request["request_id"],
        "scope_kind": request["scope_kind"],
        "scope_refs": list(request["scope_refs"]),
        "registry_ref": REGISTRY_REL,
        "resolution_mode": resolution_mode,
        "direct_gate_ids": direct_gate_ids,
    }
    schema_validate(manifest, "mathematics-engineering-manifest.schema.json", "MATH_ENG_MANIFEST_SCHEMA")
    return manifest


def _closure(gates: dict[str, dict], direct_gate_ids: list[str]) -> list[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    ordered: list[str] = []

    def walk(gate_id: str) -> None:
        if gate_id in visited:
            return
        if gate_id in visiting:
            raise MathematicsEngineeringWorkbenchError("MATH_ENG_DEPENDENCY_CYCLE", gate_id)
        gate = gates.get(gate_id)
        if gate is None:
            raise MathematicsEngineeringWorkbenchError("MATH_ENG_GATE_UNKNOWN", gate_id)
        visiting.add(gate_id)
        for prereq in gate.get("prerequisite_ids", []):
            if isinstance(prereq, str) and prereq.startswith("MATH-"):
                walk(prereq)
        visiting.remove(gate_id)
        visited.add(gate_id)
        ordered.append(gate_id)

    for gate_id in direct_gate_ids:
        walk(gate_id)
    return ordered


def authoritative_gate_state(gate: dict, engineering_depth: str = "STANDARD") -> dict:
    source_scope = gate.get("provenance", {}).get("source_scope", "UNRESOLVED")
    readiness = gate.get("technical_readiness", "ENGINEERING_GATE_INCOMPLETE")
    failures: list[str] = []

    if gate.get("authority_tier") == "SOURCE_SCOPE_HELD" or source_scope == "HELD_SCOPE":
        failures.append("MATH_ENG_SOURCE_SCOPE_HELD")
    if readiness != "ENGINEERING_GATE_READY":
        failures.append("MATH_ENG_GATE_NOT_READY")
    failures.extend(_depth_failures(gate, engineering_depth))

    return {
        "gate_id": gate["subtopic_id"],
        "authoritative_technical_readiness": readiness,
        "source_scope": source_scope,
        "blueprint_admissible": not failures,
        "failure_codes": list(dict.fromkeys(failures)),
    }


def _verify_manifest_against_resolution(request: dict, manifest: dict, registry: dict) -> None:
    schema_validate(manifest, "mathematics-engineering-manifest.schema.json", "MATH_ENG_MANIFEST_SCHEMA")
    expected = resolve_manifest(request, registry)
    fields = (
        "request_id",
        "scope_kind",
        "scope_refs",
        "registry_ref",
        "resolution_mode",
        "direct_gate_ids",
    )
    for field in fields:
        if manifest.get(field) != expected.get(field):
            raise MathematicsEngineeringWorkbenchError(
                "MATH_ENG_MANIFEST_STALE_OR_FORGED",
                f"{field}: expected {expected.get(field)!r}, got {manifest.get(field)!r}",
            )


def compile_closure(
    request: dict,
    manifest: dict | None = None,
    registry: dict | None = None,
) -> dict:
    schema_validate(request, "mathematics-engineering-request.schema.json", "MATH_ENG_REQUEST_SCHEMA")
    registry = registry or load(REGISTRY_REL)
    _validate_authoritative_registry(registry)

    manifest = manifest or resolve_manifest(request, registry)
    _verify_manifest_against_resolution(request, manifest, registry)

    gates = _gate_index(registry)
    transitive = _closure(gates, manifest["direct_gate_ids"])
    states = [
        authoritative_gate_state(gates[gate_id], request["engineering_depth"])
        for gate_id in transitive
    ]
    ready = sum(1 for state in states if state["blueprint_admissible"])
    blocked = len(states) - ready

    suffix = request["request_id"].removeprefix("MATH-ENG-REQ-")
    receipt = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "receipt_id": f"MATH-ENG-CLOSURE-{suffix}",
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "validator_contract_digest": engineering_validator_contract_digest(),
        "resolution_mode": manifest["resolution_mode"],
        "scope_refs": list(request["scope_refs"]),
        "direct_gate_ids": list(manifest["direct_gate_ids"]),
        "transitive_gate_ids": transitive,
        "gate_states": states,
        "counts": {
            "direct_gate_count": len(manifest["direct_gate_ids"]),
            "transitive_gate_count": len(transitive),
            "ready_gate_count": ready,
            "blocked_gate_count": blocked,
        },
        "closure_status": "READY" if blocked == 0 else "BLOCKED",
        "technical_authorization": "ALLOWED" if blocked == 0 else "BLOCKED",
        "publication_authorization": "NOT_IMPLIED",
    }
    schema_validate(receipt, "mathematics-engineering-closure-receipt.schema.json", "MATH_ENG_RECEIPT_SCHEMA")
    return receipt


def _engineering_surface(request: dict, receipt: dict, registry: dict) -> dict:
    if digest(registry) != receipt["registry_digest"]:
        raise MathematicsEngineeringWorkbenchError(
            "MATH_ENG_PASSPORT_REGISTRY_CUSTODY_DRIFT",
            "passport view must be derived from the exact registry bound by the closure receipt",
        )
    gates = _gate_index(registry)
    states = {row["gate_id"]: row for row in receipt["gate_states"]}
    direct = set(receipt["direct_gate_ids"])
    rows = []
    for gate_id in receipt["transitive_gate_ids"]:
        gate = gates[gate_id]
        state = states[gate_id]
        provenance = gate.get("provenance") or {}
        rows.append({
            "gate_id": gate_id,
            "scope_role": "DIRECT" if gate_id in direct else "PREREQUISITE_CLOSURE",
            "learner_title": gate.get("learner_title"),
            "chapter": gate.get("chapter"),
            "requested_engineering_depth": request["engineering_depth"],
            "technical_state": "READY" if state["blueprint_admissible"] else "BLOCKED",
            "failure_codes": list(state["failure_codes"]),
            "prerequisite_ids": list(gate.get("prerequisite_ids") or []),
            "provenance": {
                "authority_tier": gate.get("authority_tier"),
                "source_scope": provenance.get("source_scope"),
                "claim_status": provenance.get("claim_status"),
                "source_reference": provenance.get("source_reference"),
            },
            "structure_counts": {
                "canonical_concepts": len(gate.get("technical_core") or []),
                "mandatory_equations": len(gate.get("mandatory_equations") or []),
                "representations": len(gate.get("representations") or []),
                "model_conditions": len(gate.get("model_conditions") or []),
                "reasoning_steps": len(gate.get("reasoning_sequence") or []),
                "transformations": len(gate.get("required_transformations") or []),
                "misconceptions": len(gate.get("misconceptions") or []),
                "verification_obligations": len(gate.get("mandatory_verifications") or []),
                "problem_families": len(gate.get("problem_families") or []),
                "falsification_cases": len(gate.get("falsification_cases") or []),
            },
            "difficulty_profile": copy.deepcopy(gate.get("difficulty_profile") or {}),
            "release_checklist_pass": all((gate.get("release_checklist") or {}).values()),
        })
    return {
        "view_class": "DERIVED_ENGINEERING_VISIBILITY",
        "authority": "NON_AUTHORITATIVE_VIEW_OF_BOUND_ENGINEERING_RECEIPT",
        "requested_engineering_depth": request["engineering_depth"],
        "technical_authorization": receipt["technical_authorization"],
        "closure_status": receipt["closure_status"],
        "direct_gate_count": receipt["counts"]["direct_gate_count"],
        "transitive_gate_count": receipt["counts"]["transitive_gate_count"],
        "ready_gate_count": receipt["counts"]["ready_gate_count"],
        "blocked_gate_count": receipt["counts"]["blocked_gate_count"],
        "gates": rows,
    }


def compile_passport(
    request: dict,
    manifest: dict,
    receipt: dict,
    registry: dict | None = None,
) -> dict:
    registry = registry or load(REGISTRY_REL)
    surface = _engineering_surface(request, receipt, registry)
    return {
        "schema_version": "1.1.0",
        "subject": "MATHEMATICS",
        "passport_id": "MATH-ENG-PASSPORT-" + request["request_id"].removeprefix("MATH-ENG-REQ-"),
        "request_id": request["request_id"],
        "scope_kind": request["scope_kind"],
        "scope_refs": list(request["scope_refs"]),
        "engineering_depth": request["engineering_depth"],
        "learning_purpose": request["learning_purpose"],
        "resolution_mode": manifest["resolution_mode"],
        "technical_state": "ENGINEERING_READY" if receipt["closure_status"] == "READY" else "BLOCKED",
        "direct_gate_ids": list(receipt["direct_gate_ids"]),
        "transitive_gate_ids": list(receipt["transitive_gate_ids"]),
        "gate_count": receipt["counts"]["transitive_gate_count"],
        "registry_digest": receipt["registry_digest"],
        "validator_contract_digest": receipt["validator_contract_digest"],
        "closure_receipt_digest": digest(receipt),
        "blueprint_technical_authorization": receipt["technical_authorization"],
        "publication_authorization": "NOT_IMPLIED",
        "engineering_surface": surface,
        "engineering_surface_digest": digest(surface),
    }


def compile_binding(
    request: dict,
    manifest: dict,
    receipt: dict,
    downstream_consumer: str,
) -> dict:
    suffix = request["request_id"].removeprefix("MATH-ENG-REQ-")
    binding = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "binding_id": f"MATH-ENG-BIND-{suffix}",
        "request_digest": digest(request),
        "manifest_digest": digest(manifest),
        "closure_receipt_id": receipt["receipt_id"],
        "closure_receipt_digest": digest(receipt),
        "registry_digest": receipt["registry_digest"],
        "validator_contract_digest": receipt["validator_contract_digest"],
        "scope_refs": list(receipt["scope_refs"]),
        "direct_gate_ids": list(receipt["direct_gate_ids"]),
        "transitive_gate_ids": list(receipt["transitive_gate_ids"]),
        "downstream_consumer": downstream_consumer,
    }
    schema_validate(binding, "mathematics-engineering-binding.schema.json", "MATH_ENG_BIND_SCHEMA")
    return binding


def compile_registry_proof(registry: dict | None = None) -> dict:
    """Exercise every current Engineering gate without naming any topic in Blueprint."""
    registry = registry or load(REGISTRY_REL)
    _validate_authoritative_registry(registry)
    results: list[dict[str, Any]] = []
    for gate in registry["subtopic_gates"]:
        gate_id = gate["subtopic_id"]
        request = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "request_id": f"MATH-ENG-REQ-REGISTRY-PROOF-{gate_id}",
            "scope_kind": "ENGINEERING_GATE",
            "scope_refs": [gate_id],
            "engineering_depth": "STANDARD",
            "learning_purpose": "FIRST_STUDY",
            "owner_decision_ref": None,
        }
        manifest = resolve_manifest(request, registry)
        receipt = compile_closure(request, manifest, registry)
        results.append(
            {
                "gate_id": gate_id,
                "closure_status": receipt["closure_status"],
                "direct_gate_ids": receipt["direct_gate_ids"],
                "transitive_gate_ids": receipt["transitive_gate_ids"],
                "closure_receipt_digest": digest(receipt),
            }
        )
    blocked = [row["gate_id"] for row in results if row["closure_status"] != "READY"]
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "validator_contract_digest": engineering_validator_contract_digest(),
        "gate_count": len(results),
        "ready_gate_count": len(results) - len(blocked),
        "blocked_gate_ids": blocked,
        "all_registry_gates_blueprint_admissible": not blocked,
        "gate_proofs": results,
    }


def _write(path: str | None, value: object) -> None:
    if path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile registry-driven Mathematics Engineering authorization")
    ap.add_argument("--request")
    ap.add_argument("--manifest")
    ap.add_argument("--manifest-out")
    ap.add_argument("--receipt-out")
    ap.add_argument("--passport-out")
    ap.add_argument("--binding-out")
    ap.add_argument("--downstream-consumer", default="CANONICAL_DOMAIN_REGISTRY")
    ap.add_argument("--registry-proof-out")
    args = ap.parse_args()

    if args.registry_proof_out:
        proof = compile_registry_proof()
        _write(args.registry_proof_out, proof)
        print(json.dumps(proof, indent=2))
        return

    if not args.request:
        ap.error("--request is required unless --registry-proof-out is used")

    request = load(args.request)
    registry = load(REGISTRY_REL)
    manifest = load(args.manifest) if args.manifest else resolve_manifest(request, registry)
    receipt = compile_closure(request, manifest, registry)
    passport = compile_passport(request, manifest, receipt, registry)
    binding = compile_binding(request, manifest, receipt, args.downstream_consumer)

    _write(args.manifest_out, manifest)
    _write(args.receipt_out, receipt)
    _write(args.passport_out, passport)
    _write(args.binding_out, binding)
    print(json.dumps({"manifest": manifest, "receipt": receipt, "passport": passport, "binding": binding}, indent=2))


if __name__ == "__main__":
    main()
