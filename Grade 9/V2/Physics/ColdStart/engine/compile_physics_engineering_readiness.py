#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
COLD = HERE.parents[1]
PHYS = HERE.parents[2]
REPO = HERE.parents[5]
BLUEPRINT = PHYS / "Blueprint"
SHARED_GATE = REPO / "Grade 9" / "V2" / "Shared" / "EngineeringGate"

sys.path[:0] = [
    str(BLUEPRINT / "engine"),
    str(SHARED_GATE / "engine"),
]

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from compile_domain_prerequisite_closure import compile_domain_prerequisite_closure  # noqa: E402
from compile_engineering_closure import V3_REGISTRY_REF, compile_closure  # noqa: E402
from evaluate_readiness import build_envelope, require_consumer  # noqa: E402


BINDING_SCHEMA = COLD / "contracts" / "physics-engineering-scope-binding.schema.json"
READINESS_SCHEMA = COLD / "contracts" / "physics-cold-start-engineering-readiness.schema.json"
REQUEST_SCHEMA = BLUEPRINT / "contracts" / "engineering-request.schema.json"
MANIFEST_SCHEMA = BLUEPRINT / "contracts" / "engineering-topic-manifest.schema.json"
BINDING_REGISTRY_REF = "Grade 9/V2/Physics/ColdStart/registry/physics-engineering-scope-bindings.v1.json"
REQUIRED_CONSUMER = "PROBLEM_SEMANTICS"


class PhysicsColdStartEngineeringError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise PhysicsColdStartEngineeringError(code, message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_hex(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def digest_prefixed(value: Any) -> str:
    return "sha256:" + digest_hex(value)


def digest_without_field(value: dict[str, Any], field: str) -> str:
    clone = copy.deepcopy(value)
    clone.pop(field, None)
    return digest_hex(clone)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json(value: dict[str, Any], schema_path: Path, code: str) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        fail(code, errors[0].message)


def _binding_map(scope_authority: dict[str, Any], registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    validate_json(registry, BINDING_SCHEMA, "ENGINEERING_SCOPE_BINDING_SCHEMA_INVALID")
    if registry["registry_digest"] != digest_without_field(registry, "registry_digest"):
        fail("ENGINEERING_SCOPE_BINDING_DIGEST_MISMATCH")
    if registry["subject"] != "PHYSICS":
        fail("ENGINEERING_SCOPE_BINDING_SUBJECT_MISMATCH")
    if registry["engineering_registry_ref"] != V3_REGISTRY_REF:
        fail("ENGINEERING_SCOPE_BINDING_REGISTRY_REF_MISMATCH")

    if scope_authority.get("authority_digest") != digest_without_field(scope_authority, "authority_digest"):
        fail("ENGINEERING_SCOPE_AUTHORITY_DIGEST_MISMATCH")
    if (
        registry["scope_authority_id"] != scope_authority.get("authority_id")
        or registry["scope_authority_digest"] != scope_authority.get("authority_digest")
    ):
        fail("ENGINEERING_SCOPE_BINDING_AUTHORITY_MISMATCH")

    authority_caps = {row["capability_id"] for row in scope_authority.get("capabilities", [])}
    rows: dict[str, dict[str, Any]] = {}
    for row in registry["bindings"]:
        cap = row["capability_ref"]
        if cap in rows:
            fail("ENGINEERING_SCOPE_BINDING_DUPLICATE_CAPABILITY", cap)
        rows[cap] = row

    if set(rows) != authority_caps:
        missing = sorted(authority_caps - set(rows))
        extra = sorted(set(rows) - authority_caps)
        fail("ENGINEERING_SCOPE_BINDING_COVERAGE_MISMATCH", f"missing={missing},extra={extra}")

    gate_ids = {row["subtopic_id"] for row in build_registry()["gates"]}
    for row in rows.values():
        if row["authority_route"] == "ENGINEERING_GATE":
            unknown = sorted(set(row["engineering_gate_ids"]) - gate_ids)
            if unknown:
                fail("ENGINEERING_SCOPE_GATE_UNKNOWN", ",".join(unknown))
        elif row["engineering_gate_ids"]:
            fail("ENGINEERING_SCOPE_NON_GATE_ROUTE_HAS_GATES", row["capability_ref"])
    return rows


def _required_capabilities(scope_model: dict[str, Any]) -> list[str]:
    if scope_model.get("subject") != "PHYSICS":
        fail("ENGINEERING_SCOPE_MODEL_SUBJECT_MISMATCH")
    expected = digest_without_field(scope_model, "scope_model_digest")
    if scope_model.get("scope_model_digest") != expected:
        fail("ENGINEERING_SCOPE_MODEL_DIGEST_MISMATCH")
    return sorted(
        set(scope_model.get("assessed_capability_refs", []))
        | set(scope_model.get("required_prerequisite_capability_refs", []))
    )


def compile_physics_engineering_readiness(
    scope_model: dict[str, Any],
    scope_authority: dict[str, Any],
    binding_registry: dict[str, Any],
    *,
    scope_model_ref: str = "DERIVED:P-C:PhysicsAssessmentScopeModel",
    binding_registry_ref: str = BINDING_REGISTRY_REF,
) -> dict[str, Any]:
    if scope_model.get("authority_ref") != scope_authority.get("authority_id"):
        fail("ENGINEERING_SCOPE_MODEL_AUTHORITY_MISMATCH")

    binding_map = _binding_map(scope_authority, binding_registry)
    required_caps = _required_capabilities(scope_model)
    missing = [cap for cap in required_caps if cap not in binding_map]
    if missing:
        fail("ENGINEERING_SCOPE_CAPABILITY_UNBOUND", ",".join(missing))

    routes = [copy.deepcopy(binding_map[cap]) for cap in required_caps]
    direct_gate_ids = sorted(
        {
            gate_id
            for row in routes
            if row["authority_route"] == "ENGINEERING_GATE"
            for gate_id in row["engineering_gate_ids"]
        }
    )
    gate_requirement_state = "REQUIRED_AND_READY" if direct_gate_ids else "NOT_REQUIRED_FOR_THIS_SCOPE"

    suffix = scope_model["scope_model_digest"][:16].upper()
    request = {
        "schema_version": "1.0.0",
        "request_id": f"ENG-REQ-COLDSTART-{suffix}",
        "subject": "PHYSICS",
        "requested_topic": scope_model["declared_topic_scope_ref"],
        "requested_scope": scope_model["scope_model_id"],
        "engineering_depth": "STANDARD",
        "requested_action": "AUTO_DISCOVER",
        "requested_for": [REQUIRED_CONSUMER],
        "notes": "Generated from exact P-C scope capability bindings; no topic-name inference is permitted.",
    }
    manifest = {
        "schema_version": "1.0.0",
        "manifest_id": f"ENG-MAN-COLDSTART-{suffix}",
        "request_id": request["request_id"],
        "scope_kind": "ASSESSMENT_SCOPE",
        "scope_ref": scope_model["scope_model_id"],
        "topic_id": None,
        "title": "Assessment-scope Engineering readiness",
        "registry_ref": V3_REGISTRY_REF,
        "required_gate_ids": direct_gate_ids,
        "optional_gate_ids": [],
        "out_of_scope_gate_ids": [],
        "source_item_status": "INDEPENDENT_OF_TECHNICAL_GATE",
        "downstream_consumers": [REQUIRED_CONSUMER],
        "notes": "Gate IDs are the union of explicit scope-capability bindings; zero-gate scopes remain valid only when every capability has an explicit upstream-authority route.",
    }
    validate_json(request, REQUEST_SCHEMA, "ENGINEERING_SCOPE_REQUEST_SCHEMA_INVALID")
    validate_json(manifest, MANIFEST_SCHEMA, "ENGINEERING_SCOPE_MANIFEST_SCHEMA_INVALID")

    engineering = compile_closure(request, manifest)
    domain = compile_domain_prerequisite_closure(engineering)
    envelope = build_envelope(request, manifest, engineering, domain)

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "readiness_id": f"PHY-ENG-READINESS-{suffix}",
        "subject": "PHYSICS",
        "authority_layer": "ENGINEERING_GATE",
        "scope_model_ref": scope_model_ref,
        "scope_model_digest": scope_model["scope_model_digest"],
        "scope_authority_ref": binding_registry["scope_authority_ref"],
        "scope_authority_digest": scope_authority["authority_digest"],
        "binding_registry_ref": binding_registry_ref,
        "binding_registry_digest": binding_registry["registry_digest"],
        "required_capability_refs": required_caps,
        "capability_routes": routes,
        "technical_gate_requirement_state": gate_requirement_state,
        "engineering_request": request,
        "engineering_manifest": manifest,
        "engineering_closure": engineering,
        "domain_closure": domain,
        "readiness_envelope": envelope,
        "required_consumer": REQUIRED_CONSUMER,
        "consumer_status": envelope["consumer_permissions"][REQUIRED_CONSUMER]["status"],
        "readiness_digest": "",
    }
    result["readiness_digest"] = digest_prefixed({k: v for k, v in result.items() if k != "readiness_digest"})
    validate_json(result, READINESS_SCHEMA, "ENGINEERING_SCOPE_READINESS_SCHEMA_INVALID")
    return result


def require_problem_semantics(readiness: dict[str, Any]) -> None:
    """Enforce the global Engineering Gate permission only at the consumption boundary."""
    validate_json(readiness, READINESS_SCHEMA, "ENGINEERING_SCOPE_READINESS_SCHEMA_INVALID")
    require_consumer(readiness["readiness_envelope"], REQUIRED_CONSUMER)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Compile mandatory P-C.5 Physics Engineering readiness from exact P-C scope authority")
    ap.add_argument("--scope-model", required=True, type=Path)
    ap.add_argument("--scope-authority", required=True, type=Path)
    ap.add_argument("--bindings", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    result = compile_physics_engineering_readiness(
        load_json(args.scope_model),
        load_json(args.scope_authority),
        load_json(args.bindings),
        scope_model_ref=str(args.scope_model),
        binding_registry_ref=str(args.bindings),
    )
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
