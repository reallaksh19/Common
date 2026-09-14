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
from validate_engineering_gates_v2 import GateValidationError, validate as validate_registry  # noqa: E402


class EngineeringClosureError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise EngineeringClosureError(code, message)


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical_digest(obj: dict) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_with_schema(obj: dict, schema_rel: str, code: str):
    try:
        jsonschema.validate(obj, load(schema_rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


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

    registry = registry if registry is not None else load(manifest["registry_ref"])
    try:
        validate_registry(registry)
    except GateValidationError as exc:
        fail("E_ENG_REGISTRY_INVALID", f"{exc.code}: {exc.message}")

    gate_map = {gate["subtopic_id"]: gate for gate in registry["gates"]}
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
            if prereq.startswith("PHY-"):
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
        status = gate["status"]
        gate_states.append({"gate_id": gate_id, "status": status, "direct": gate_id in direct_set})
        if status != "ENGINEERING_GATE_READY":
            blockers.append({"code": "E_ENG_GATE_NOT_READY", "gate_id": gate_id, "message": f"{gate_id} status is {status}"})

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
        authority_note = "technical engineering closure is BLOCKED; CCU may not consume this scope as technically ready"

    digest_payload = {
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "registry_digest": canonical_digest(registry),
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
        "registry_ref": manifest["registry_ref"],
        "registry_digest": digest_payload["registry_digest"],
        "closure_digest": canonical_digest(digest_payload),
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
    parser = argparse.ArgumentParser(description="Compile a Physics engineering prerequisite closure receipt")
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
