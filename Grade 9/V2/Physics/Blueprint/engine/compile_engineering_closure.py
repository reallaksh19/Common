#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_engineering_gates_v2 import GateValidationError as GateValidationErrorV2, validate as validate_registry_v2  # noqa: E402
from build_physics_engineering_gate_registry_v3 import build_registry as build_registry_v3  # noqa: E402
from validate_engineering_gates_v3 import PhysicsEngineeringGateV3Error, validate as validate_registry_v3  # noqa: E402

V3_REGISTRY_REF = "GENERATED:physics-technical-engineering-gates.v3"
LEGACY_V3_REGISTRY_REF = "GENERATED:physics-technical-engineering-gates.v3-sba23"
V3_REGISTRY_REFS = {V3_REGISTRY_REF, LEGACY_V3_REGISTRY_REF}


class EngineeringClosureError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise EngineeringClosureError(code, message)


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical_digest(obj: object) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_with_schema(obj: dict, schema_rel: str, code: str):
    try:
        jsonschema.validate(obj, load(schema_rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def compose_registry(manifest: dict, supplied_registry: dict | None = None) -> dict:
    if supplied_registry is not None:
        return supplied_registry

    extension_refs = list(manifest.get("gate_extension_refs", []))
    if manifest["registry_ref"] in V3_REGISTRY_REFS:
        if extension_refs:
            fail("E_ENG_GATE_EXTENSION_INVALID", "canonical v3 generated registry does not accept v2 gate extensions")
        return build_registry_v3()

    base = load(manifest["registry_ref"])
    if not extension_refs:
        return base

    composed = {**base, "gates": list(base["gates"])}
    extension_schema = load("contracts/physics-technical-engineering-gate-extension-v1.schema.json")
    for rel in extension_refs:
        try:
            extension = load(rel)
            jsonschema.validate(extension, extension_schema)
        except (OSError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
            fail("E_ENG_GATE_EXTENSION_INVALID", f"{rel}: {exc}")
        if extension["base_registry_ref"] != manifest["registry_ref"]:
            fail("E_ENG_GATE_EXTENSION_BASE_MISMATCH", f"{rel} targets {extension['base_registry_ref']}")
        composed["gates"].extend(extension["gates"])
    return composed


def validated_status_map(registry: dict) -> dict[str, str]:
    version = registry.get("schema_version")
    if version == "3.0.0":
        try:
            validate_registry_v3(registry)
        except PhysicsEngineeringGateV3Error as exc:
            fail("E_ENG_REGISTRY_INVALID", f"{exc.code}: {exc.message}")
        return {
            gate["subtopic_id"]: (
                "ENGINEERING_GATE_READY" if gate["scope_state"] == "ACTIVE"
                else "SOURCE_SCOPE_HELD" if gate["scope_state"] == "SOURCE_SCOPE_HELD"
                else "ENGINEERING_GATE_INCOMPLETE"
            )
            for gate in registry["gates"]
        }
    if version == "2.0.0":
        try:
            validate_registry_v2(registry)
        except GateValidationErrorV2 as exc:
            fail("E_ENG_REGISTRY_INVALID", f"{exc.code}: {exc.message}")
        return {gate["subtopic_id"]: gate["status"] for gate in registry["gates"]}
    fail("E_ENG_REGISTRY_INVALID", f"unsupported engineering registry schema_version {version}")


def validate_research_artifact(
    *,
    request: dict,
    manifest: dict,
    ref_key: str,
    schema_rel: str,
    ready_status: str,
    missing_code: str,
    invalid_code: str,
    supplied: dict | None,
    blockers: list[dict],
):
    rel = manifest.get(ref_key)
    if not rel:
        blockers.append({"code": missing_code, "message": f"RESEARCH request requires {ref_key}"})
        return
    try:
        artifact = supplied if supplied is not None else load(rel)
        jsonschema.validate(artifact, load(schema_rel))
        if artifact["request_id"] != request["request_id"]:
            raise ValueError("request_id does not match engineering request")
        if artifact["status"] != ready_status:
            raise ValueError(f"status must be {ready_status}")
    except (OSError, json.JSONDecodeError, jsonschema.ValidationError, KeyError, ValueError) as exc:
        blockers.append({"code": invalid_code, "message": f"{ref_key} is not release-ready: {exc}"})


def compile_closure(
    request: dict,
    manifest: dict,
    *,
    registry: dict | None = None,
    research_dossier: dict | None = None,
    claim_ledger: dict | None = None,
) -> dict:
    validate_with_schema(request, "contracts/engineering-request.schema.json", "E_ENG_REQUEST_SCHEMA")
    validate_with_schema(manifest, "contracts/engineering-topic-manifest.schema.json", "E_ENG_MANIFEST_SCHEMA")

    if request["request_id"] != manifest["request_id"]:
        fail("E_ENG_REQUEST_MANIFEST_MISMATCH", "manifest request_id does not match request")

    registry = compose_registry(manifest, registry)
    status_map = validated_status_map(registry)

    gate_map = {gate["subtopic_id"]: gate for gate in registry["gates"]}
    internal_prefixes = tuple(sorted({gate_id.split("-", 1)[0] + "-" for gate_id in gate_map}))
    if not internal_prefixes:
        fail("E_ENG_REGISTRY_INVALID", "registry contains no gate namespace")

    direct = list(manifest["required_gate_ids"])
    direct_set = set(direct)
    seen: set[str] = set()
    visiting: list[str] = []
    ordered: list[str] = []
    missing: set[str] = set()

    def walk(gate_id: str):
        if gate_id in seen:
            return
        if gate_id in visiting:
            cycle_start = visiting.index(gate_id)
            cycle = visiting[cycle_start:] + [gate_id]
            fail("E_ENG_DEPENDENCY_CYCLE", " -> ".join(cycle))
        gate = gate_map.get(gate_id)
        if gate is None:
            missing.add(gate_id)
            seen.add(gate_id)
            ordered.append(gate_id)
            return
        visiting.append(gate_id)
        for prereq in gate["prerequisites"]:
            if prereq.startswith(internal_prefixes):
                walk(prereq)
        visiting.pop()
        seen.add(gate_id)
        ordered.append(gate_id)

    for gate_id in direct:
        walk(gate_id)

    blockers: list[dict] = []
    gate_states: list[dict] = []
    for gate_id in ordered:
        gate = gate_map.get(gate_id)
        if gate is None:
            gate_states.append({"gate_id": gate_id, "status": "MISSING", "direct": gate_id in direct_set})
            blockers.append({"code": "E_ENG_GATE_MISSING", "gate_id": gate_id, "message": f"required technical gate {gate_id} is not present"})
            continue
        status = status_map[gate_id]
        gate_states.append({"gate_id": gate_id, "status": status, "direct": gate_id in direct_set})
        if status != "ENGINEERING_GATE_READY":
            blockers.append({"code": "E_ENG_GATE_NOT_READY", "gate_id": gate_id, "message": f"{gate_id} derived status is {status}"})

    if request["engineering_depth"] == "RESEARCH":
        validate_research_artifact(
            request=request,
            manifest=manifest,
            ref_key="research_dossier_ref",
            schema_rel="contracts/engineering-research-dossier.schema.json",
            ready_status="RESEARCH_DOSSIER_READY",
            missing_code="E_ENG_RESEARCH_DOSSIER_REQUIRED",
            invalid_code="E_ENG_RESEARCH_DOSSIER_INVALID",
            supplied=research_dossier,
            blockers=blockers,
        )
        validate_research_artifact(
            request=request,
            manifest=manifest,
            ref_key="claim_ledger_ref",
            schema_rel="contracts/engineering-claim-ledger.schema.json",
            ready_status="CLAIM_LEDGER_READY",
            missing_code="E_ENG_CLAIM_LEDGER_REQUIRED",
            invalid_code="E_ENG_CLAIM_LEDGER_INVALID",
            supplied=claim_ledger,
            blockers=blockers,
        )

    ready_gate_count = sum(1 for state in gate_states if state["status"] == "ENGINEERING_GATE_READY")
    blocked_gate_count = sum(1 for state in gate_states if state["status"] != "ENGINEERING_GATE_READY")
    closure_status = "BLOCKED" if blockers else "READY"

    source_status = manifest["source_item_status"]
    if closure_status == "READY" and source_status == "SOURCE_HELD":
        authority_note = "technical engineering closure is READY; source/legal custody remains independently held downstream"
    elif closure_status == "READY":
        authority_note = "technical engineering closure is READY; downstream custody, pedagogy and learner-evidence gates remain independent"
    else:
        authority_note = "technical engineering closure is BLOCKED; declared downstream technical consumers may not consume this scope as ready"

    extension_refs = list(manifest.get("gate_extension_refs", []))
    request_digest = canonical_digest(request)
    manifest_digest = canonical_digest(manifest)
    registry_digest = canonical_digest(registry)

    # Scope-stable custody intentionally excludes the aggregate registry digest. It binds
    # the exact request/manifest plus the exact content and derived state of only the gates
    # reachable from this scope. Unrelated subject growth therefore changes registry_digest
    # (provenance) without changing scoped_closure_digest (authority for this closure).
    scoped_gate_custody = [
        {
            "gate_id": gate_id,
            "gate_digest": canonical_digest(gate_map[gate_id]) if gate_id in gate_map else None,
        }
        for gate_id in ordered
    ]
    scoped_digest_payload = {
        "request_digest": request_digest,
        "manifest_digest": manifest_digest,
        "gate_extension_refs": extension_refs,
        "direct_gate_ids": direct,
        "transitive_gate_ids": ordered,
        "scoped_gate_custody": scoped_gate_custody,
        "gate_states": gate_states,
        "blockers": blockers,
        "closure_status": closure_status,
        "source_item_status": source_status,
    }
    scoped_closure_digest = canonical_digest(scoped_digest_payload)

    # Legacy closure_digest remains aggregate-registry-sensitive for backward-compatible
    # receipt identity. New downstream custody must use scoped_closure_digest instead.
    digest_payload = {
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": manifest_digest,
        "registry_digest": registry_digest,
        "gate_extension_refs": extension_refs,
        "direct_gate_ids": direct,
        "transitive_gate_ids": ordered,
        "gate_states": gate_states,
        "blockers": blockers,
        "closure_status": closure_status,
        "source_item_status": source_status,
    }

    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": manifest["manifest_id"].replace("ENG-MAN-", "ENG-CLOSURE-", 1),
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": manifest_digest,
        "registry_ref": manifest["registry_ref"],
        "gate_extension_refs": extension_refs,
        "registry_digest": registry_digest,
        "closure_digest": canonical_digest(digest_payload),
        "scoped_closure_digest": scoped_closure_digest,
        "direct_gate_ids": direct,
        "transitive_gate_ids": ordered,
        "gate_states": gate_states,
        "blockers": blockers,
        "counts": {
            "direct_gate_count": len(direct),
            "transitive_gate_count": len(ordered),
            "ready_gate_count": ready_gate_count,
            "blocked_gate_count": blocked_gate_count,
        },
        "closure_status": closure_status,
        "source_item_status": source_status,
        "authority_note": authority_note,
    }
    validate_with_schema(receipt, "contracts/engineering-closure-receipt.schema.json", "E_ENG_RECEIPT_SCHEMA")
    return receipt


def main():
    parser = argparse.ArgumentParser(description="Compile an Engineering Gate prerequisite closure receipt")
    parser.add_argument("request")
    parser.add_argument("manifest")
    parser.add_argument("--out")
    args = parser.parse_args()

    receipt = compile_closure(load(args.request), load(args.manifest))
    rendered = json.dumps(receipt, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()