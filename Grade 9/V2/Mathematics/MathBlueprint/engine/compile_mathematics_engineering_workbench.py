#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

from validate_mathematics_engineering_gates import (  # noqa: E402
    MathematicsEngineeringGateValidationError,
    validate as validate_registry,
)


class MathematicsEngineeringWorkbenchError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def load(rel_or_path: str | Path) -> dict:
    p = Path(rel_or_path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def schema_validate(doc: dict, schema_name: str, code: str) -> None:
    schema = load(f"contracts/{schema_name}")
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise MathematicsEngineeringWorkbenchError(code, f"{e.message}; path={list(e.path)}")


def _ids(gate: dict, field: str, id_field: str) -> set[str]:
    return {row[id_field] for row in gate.get(field, [])}


def derive_gate_state(gate: dict, invariant_profile: dict) -> dict:
    gid = gate["subtopic_id"]
    req = invariant_profile["required_gates"].get(gid)
    failures: list[str] = []

    source_scope = gate.get("provenance", {}).get("source_scope", "UNRESOLVED")
    if gate.get("authority_tier") == "SOURCE_SCOPE_HELD" or source_scope == "HELD_SCOPE":
        return {
            "gate_id": gid,
            "derived_status": "SOURCE_SCOPE_HELD",
            "source_scope": source_scope,
            "declared_technical_readiness_ignored": True,
            "declared_release_checklist_ignored": True,
            "failure_codes": ["MATH_ENG_SOURCE_SCOPE_HELD"],
        }

    if req is None:
        failures.append("MATH_ENG_INVARIANT_PROFILE_MISSING")
    else:
        concepts = _ids(gate, "technical_core", "concept_id")
        equations = _ids(gate, "mandatory_equations", "equation_id")
        reps = _ids(gate, "representations", "representation_id")
        miscs = _ids(gate, "misconceptions", "misconception_id")
        prereqs = set(gate.get("prerequisite_ids", []))
        checks = [
            (set(req.get("required_concepts", [])), concepts, "MATH_ENG_REQUIRED_CONCEPT_MISSING"),
            (set(req.get("required_equations", [])), equations, "MATH_ENG_REQUIRED_EQUATION_MISSING"),
            (set(req.get("required_representations", [])), reps, "MATH_ENG_REQUIRED_REPRESENTATION_MISSING"),
            (set(req.get("required_misconceptions", [])), miscs, "MATH_ENG_REQUIRED_MISCONCEPTION_MISSING"),
            (set(req.get("required_prerequisites", [])), prereqs, "MATH_ENG_REQUIRED_PREREQUISITE_MISSING"),
        ]
        for required, actual, code in checks:
            if not required.issubset(actual):
                failures.append(code)

    generic = invariant_profile["generic_requirements"]
    if len(gate.get("reasoning_sequence", [])) < generic["minimum_reasoning_steps"]:
        failures.append("MATH_ENG_REASONING_SEQUENCE_INCOMPLETE")
    transforms = gate.get("required_transformations", [])
    if len(transforms) < generic["minimum_transformations"]:
        failures.append("MATH_ENG_TRANSFORMATIONS_INCOMPLETE")
    roles = {x.get("target_core_role") for x in transforms}
    for role in generic["required_transformation_roles"]:
        if role not in roles:
            failures.append("MATH_ENG_REQUIRED_CORE_TRANSFORMATION_MISSING")
    if len(gate.get("mandatory_verifications", [])) < generic["minimum_verifications"]:
        failures.append("MATH_ENG_VERIFICATION_MISSING")
    if len(gate.get("problem_families", [])) < generic["minimum_problem_families"]:
        failures.append("MATH_ENG_PROBLEM_FAMILY_MISSING")

    linked = set(gate.get("linked_problem_family_ids", []))
    defined = {x["family_id"] for x in gate.get("problem_families", [])}
    if not linked.issubset(defined):
        failures.append("MATH_ENG_PROBLEM_FAMILY_LINK_BROKEN")

    dp = gate.get("difficulty_profile", {})
    if dp.get("maturity") != "ENGINEERING":
        failures.append("MATH_ENG_DIFFICULTY_MATURITY_INVALID")
    for dim in generic["difficulty_dimensions"]:
        value = dp.get(dim)
        if not isinstance(value, int) or value < 0 or value > 3:
            failures.append("MATH_ENG_DIFFICULTY_DIMENSION_INVALID")
            break

    claim_status = gate.get("provenance", {}).get("claim_status")
    if claim_status not in {"VERIFIED_CANONICAL", "DERIVED"}:
        failures.append("MATH_ENG_PROVENANCE_NOT_READY")

    return {
        "gate_id": gid,
        "derived_status": "ENGINEERING_GATE_READY" if not failures else "ENGINEERING_GATE_INCOMPLETE",
        "source_scope": source_scope,
        "declared_technical_readiness_ignored": True,
        "declared_release_checklist_ignored": True,
        "failure_codes": sorted(set(failures)),
    }


def _closure(gates: dict[str, dict], direct_gate_ids: list[str]) -> list[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    ordered: list[str] = []

    def walk(gid: str) -> None:
        if gid in visited:
            return
        if gid in visiting:
            raise MathematicsEngineeringWorkbenchError("MATH_ENG_DEPENDENCY_CYCLE", gid)
        if gid not in gates:
            raise MathematicsEngineeringWorkbenchError("MATH_ENG_GATE_UNKNOWN", gid)
        visiting.add(gid)
        for prereq in gates[gid].get("prerequisite_ids", []):
            if prereq.startswith("MATH-"):
                walk(prereq)
        visiting.remove(gid)
        visited.add(gid)
        ordered.append(gid)

    for gid in direct_gate_ids:
        walk(gid)
    return ordered


def compile_closure(request: dict, manifest: dict, registry: dict | None = None, invariant_profile: dict | None = None) -> dict:
    schema_validate(request, "mathematics-engineering-request.schema.json", "MATH_ENG_REQUEST_SCHEMA")
    schema_validate(manifest, "mathematics-engineering-manifest.schema.json", "MATH_ENG_MANIFEST_SCHEMA")

    if request["subject"] != "MATHEMATICS" or manifest["subject"] != "MATHEMATICS":
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_SUBJECT_MISMATCH", "Workbench accepts MATHEMATICS only")
    if manifest["request_id"] != request["request_id"]:
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_REQUEST_MANIFEST_MISMATCH", "request_id differs")
    if manifest["scope_kind"] != request["scope_kind"] or manifest["scope_ref"] != request["scope_ref"]:
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_SCOPE_MISMATCH", "request and manifest scopes differ")

    registry = registry or load(manifest["registry_ref"])
    invariant_profile = invariant_profile or load(manifest["invariant_profile_ref"])
    if invariant_profile.get("subject") != "MATHEMATICS":
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_SUBJECT_MISMATCH", "invariant profile is not Mathematics")
    if registry.get("registry_id") != invariant_profile.get("registry_id"):
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_REGISTRY_PROFILE_MISMATCH", "registry/profile ids differ")

    try:
        validate_registry(registry)
    except MathematicsEngineeringGateValidationError as exc:
        raise MathematicsEngineeringWorkbenchError("MATH_ENG_REGISTRY_INVALID", str(exc)) from exc

    gates = {g["subtopic_id"]: g for g in registry["subtopic_gates"]}
    transitive = _closure(gates, manifest["direct_gate_ids"])
    states = [derive_gate_state(gates[gid], invariant_profile) for gid in transitive]
    ready = sum(1 for x in states if x["derived_status"] == "ENGINEERING_GATE_READY")
    blocked = len(states) - ready
    receipt = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "receipt_id": "MATH-ENG-CLOSURE-" + manifest["manifest_id"].removeprefix("MATH-ENG-MANIFEST-"),
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "invariant_profile_digest": digest(invariant_profile),
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
        "publication_authorization": "NOT_IMPLIED",
    }
    schema_validate(receipt, "mathematics-engineering-closure-receipt.schema.json", "MATH_ENG_RECEIPT_SCHEMA")
    return receipt


def compile_passport(request: dict, receipt: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "passport_id": "MATH-ENG-PASSPORT-" + receipt["receipt_id"].removeprefix("MATH-ENG-CLOSURE-"),
        "request_id": request["request_id"],
        "scope_ref": request["scope_ref"],
        "engineering_depth": request["engineering_depth"],
        "learning_purpose": request["learning_purpose"],
        "technical_state": "ENGINEERING_READY" if receipt["closure_status"] == "READY" else "BLOCKED",
        "gate_count": receipt["counts"]["transitive_gate_count"],
        "registry_digest": receipt["registry_digest"],
        "invariant_profile_digest": receipt["invariant_profile_digest"],
        "closure_receipt_digest": digest(receipt),
        "ccu_technical_authorization": "ALLOWED" if receipt["closure_status"] == "READY" else "BLOCKED",
        "publication_authorization": "NOT_IMPLIED",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile Mathematics Engineering Workbench closure")
    ap.add_argument("--request", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--receipt-out")
    ap.add_argument("--passport-out")
    args = ap.parse_args()
    request = load(args.request)
    manifest = load(args.manifest)
    receipt = compile_closure(request, manifest)
    passport = compile_passport(request, receipt)
    if args.receipt_out:
        Path(args.receipt_out).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if args.passport_out:
        Path(args.passport_out).write_text(json.dumps(passport, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": receipt, "passport": passport}, indent=2))


if __name__ == "__main__":
    main()
