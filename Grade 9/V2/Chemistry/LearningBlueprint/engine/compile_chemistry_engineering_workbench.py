#!/usr/bin/env python3
"""Chemistry Engineering Workbench CLI & Registry Proof Compiler."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import compile_closure  # noqa: E402
from compile_chemistry_engineering_authorization_binding import compile_binding  # noqa: E402
from compile_chemistry_engineering_passport import compile_passport  # noqa: E402

REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"


class ChemistryEngineeringWorkbenchError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(val).encode("utf-8")).hexdigest()


def load(rel_or_path: str | Path) -> dict:
    p = Path(rel_or_path) if Path(rel_or_path).is_absolute() else ROOT / rel_or_path
    return json.loads(p.read_text(encoding="utf-8"))


def engineering_validator_contract_digest() -> str:
    validator_path = ROOT / "engine" / "validate_chemistry_engineering_gates.py"
    return "sha256:" + hashlib.sha256(validator_path.read_bytes()).hexdigest()


def resolve_manifest(request: dict, registry: dict, gate_id: str | None = None) -> dict:
    if not gate_id:
        gate_id = request.get("notes") or request.get("requested_topic")
    gate_map = {g["subtopic_id"]: g for g in registry.get("subtopic_gates", [])}
    if gate_id not in gate_map:
        # Try matching by title or first gate
        matched = next((g["subtopic_id"] for g in registry.get("subtopic_gates", []) if g["subtopic_id"] in request.get("requested_scope", "")), None)
        if matched:
            gate_id = matched
        else:
            raise ChemistryEngineeringWorkbenchError("CHEM_GATE_NOT_FOUND", f"Gate {gate_id} not found in registry")

    external = []
    closure = {gate_id}
    changed = True
    while changed:
        changed = False
        for gid in list(closure):
            row = gate_map.get(gid)
            if not row:
                continue
            for prereq in row.get("prerequisite_ids", []):
                if prereq.startswith("CHEM-"):
                    if prereq not in closure:
                        closure.add(prereq)
                        changed = True
                elif prereq not in {x["dependency_id"] for x in external}:
                    external.append({"dependency_id": prereq, "status": "RESOLVED_BY_AUTHORITY", "evidence_ref": "CANONICAL_EXTERNAL"})

    req_suffix = request["request_id"].removeprefix("CHEM-ENG-REQ-")
    return {
        "schema_version": "2.0.0",
        "manifest_id": f"CHEM-ENG-MAN-{req_suffix}",
        "request_id": request["request_id"],
        "scope_kind": "SUBTOPIC",
        "scope_ref": gate_id,
        "topic_id": gate_id,
        "title": gate_map[gate_id]["learner_title"],
        "registry_ref": REGISTRY_REL,
        "required_gate_ids": [gate_id],
        "optional_gate_ids": [],
        "out_of_scope_gate_ids": [],
        "source_audits": [],
        "external_prerequisite_resolutions": external,
        "source_item_status": "INDEPENDENT_OF_TECHNICAL_GATE",
        "downstream_consumers": request.get("requested_for") or ["CDAU", "PAL"],
    }


def compile_registry_proof(registry: dict | None = None) -> dict:
    registry = registry or load(REGISTRY_REL)
    results: list[dict[str, Any]] = []
    for gate in registry.get("subtopic_gates", []):
        gate_id = gate["subtopic_id"]
        req = {
            "schema_version": "2.0.0",
            "request_id": f"CHEM-ENG-REQ-REGISTRY-PROOF-{gate_id}",
            "subject": "CHEMISTRY",
            "requested_topic": gate["learner_title"],
            "requested_scope": f"Gate {gate_id}",
            "engineering_depth": "STANDARD",
            "requested_action": "DECLARE_DIRECT_GATES",
            "requested_for": ["CDAU", "PAL"],
        }
        man = resolve_manifest(req, registry, gate_id=gate_id)
        receipt = compile_closure(req, man, registry=registry)
        results.append({
            "gate_id": gate_id,
            "closure_status": receipt["closure_status"],
            "direct_gate_ids": receipt["direct_gate_ids"],
            "transitive_gate_ids": receipt.get("closure_gate_ids", receipt.get("transitive_gate_ids", [])),
            "closure_receipt_digest": receipt["closure_digest"],
        })
    blocked = [r["gate_id"] for r in results if r["closure_status"] != "READY"]
    return {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "validator_contract_digest": engineering_validator_contract_digest(),
        "gate_count": len(results),
        "ready_gate_count": len(results) - len(blocked),
        "blocked_gate_ids": blocked,
        "all_registry_gates_blueprint_admissible": not blocked,
        "gate_proofs": results,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Chemistry Engineering Workbench CLI")
    ap.add_argument("--request-json")
    ap.add_argument("--manifest-json")
    ap.add_argument("--registry-proof-out")
    args = ap.parse_args()

    if args.registry_proof_out:
        proof = compile_registry_proof()
        out_p = Path(args.registry_proof_out)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
        print(f"Registry proof compiled ({proof['ready_gate_count']}/{proof['gate_count']} READY): {out_p}")
        return

    if args.request_json:
        req = load(args.request_json)
        reg = load(REGISTRY_REL)
        man = load(args.manifest_json) if args.manifest_json else resolve_manifest(req, reg)
        receipt = compile_closure(req, man, registry=reg)
        print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
