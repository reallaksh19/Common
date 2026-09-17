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

from compile_chemistry_engineering_gate_topology import (  # noqa: E402
    ChemistryEngineeringTopologyError,
    compile_gate_topology,
)
from validate_chemistry_engineering_registry_runtime import (  # noqa: E402
    ChemistryEngineeringRegistryError,
    validate as validate_registry,
)
from validate_chemistry_gate_source_audit import (  # noqa: E402
    ChemistrySourceAuditError,
    validate as validate_source_audit,
)


class ChemistryEngineeringClosureError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str):
    raise ChemistryEngineeringClosureError(code, message)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def digest(obj: dict) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_schema(obj: dict, rel: str, code: str):
    try:
        jsonschema.validate(obj, load(rel))
    except jsonschema.ValidationError as exc:
        fail(code, exc.message)


def _research_artifact(request, manifest, ref_key, schema, ready, supplied, missing_code, invalid_code, blockers):
    rel = manifest.get(ref_key)
    if not rel:
        blockers.append({"code": missing_code, "message": f"RESEARCH request requires {ref_key}"})
        return
    try:
        art = supplied if supplied is not None else load(rel)
        jsonschema.validate(art, load(schema))
        if art["request_id"] != request["request_id"] or art["status"] != ready:
            raise ValueError("request/status mismatch")
    except Exception as exc:
        blockers.append({"code": invalid_code, "message": f"{ref_key} not ready: {exc}"})


def _legacy_only_topology_extension(registry: dict) -> dict:
    """Return a deterministic empty extension for an injected non-canonical registry.

    The repository default topology sidecar is authority for the registry referenced by
    the manifest. A caller that injects a different registry must not accidentally inherit
    production typed edges merely because it reuses the same registry_id. Legacy
    prerequisite_ids on the injected registry remain authoritative unless the caller also
    injects a matching topology_extension.
    """
    return {
        "schema_version": "1.0.0",
        "extension_id": "CHEM-ENG-TOPOLOGY-EXT-registry-override-legacy-v1",
        "subject": "CHEMISTRY",
        "registry_id": registry["registry_id"],
        "additive_only": True,
        "legacy_coverage": "ALLOW_PARTIAL",
        "edges": [],
    }


def _resolve_topology_extension(manifest: dict, registry: dict, supplied) -> dict | None:
    if supplied is not None:
        return supplied
    try:
        canonical_registry = load(manifest["registry_ref"])
    except (FileNotFoundError, json.JSONDecodeError):
        return _legacy_only_topology_extension(registry)
    if digest(registry) == digest(canonical_registry):
        return None
    return _legacy_only_topology_extension(registry)


def compile_closure(
    request: dict,
    manifest: dict,
    *,
    registry=None,
    topology_extension=None,
    research_dossier=None,
    claim_ledger=None,
    source_audit_payloads=None,
) -> dict:
    validate_schema(request, "contracts/chemistry-engineering-request.schema.json", "CHEM_ENG_REQUEST_SCHEMA")
    validate_schema(manifest, "contracts/chemistry-engineering-topic-manifest.schema.json", "CHEM_ENG_MANIFEST_SCHEMA")
    if request["request_id"] != manifest["request_id"]:
        fail("CHEM_ENG_REQUEST_MANIFEST_MISMATCH", "request_id mismatch")

    registry = registry if registry is not None else load(manifest["registry_ref"])
    try:
        validate_registry(registry)
    except ChemistryEngineeringRegistryError as exc:
        fail("CHEM_ENG_REGISTRY_INVALID", f"{exc.code}: {exc.message}")
    effective_topology_extension = _resolve_topology_extension(manifest, registry, topology_extension)
    try:
        topology = compile_gate_topology(registry, topology_extension=effective_topology_extension)
    except ChemistryEngineeringTopologyError as exc:
        fail("CHEM_ENG_TOPOLOGY_INVALID", f"{exc.code}: {exc.message}")

    gate_map = {g["subtopic_id"]: g for g in registry["subtopic_gates"]}
    edges_by_source: dict[str, list[dict]] = {}
    for edge in topology["edges"]:
        edges_by_source.setdefault(edge["source_gate_id"], []).append(edge)

    direct = list(manifest["required_gate_ids"])
    optional = list(manifest["optional_gate_ids"])
    out_of_scope = list(manifest["out_of_scope_gate_ids"])
    direct_set = set(direct)
    optional_set = set(optional)
    out_of_scope_set = set(out_of_scope)

    overlaps = {
        "required_optional": sorted(direct_set & optional_set),
        "required_out_of_scope": sorted(direct_set & out_of_scope_set),
        "optional_out_of_scope": sorted(optional_set & out_of_scope_set),
    }
    nonempty_overlaps = {key: values for key, values in overlaps.items() if values}
    if nonempty_overlaps:
        fail("CHEM_ENG_GATE_SCOPE_SET_OVERLAP", json.dumps(nonempty_overlaps, sort_keys=True))

    for label, gate_ids in (("optional", optional), ("out_of_scope", out_of_scope)):
        missing_declared = sorted(gid for gid in gate_ids if gid not in gate_map)
        if missing_declared:
            fail(
                "CHEM_ENG_DECLARED_GATE_MISSING",
                f"{label}:" + ",".join(missing_declared),
            )

    seen: set[str] = set()
    visiting: list[str] = []
    ordered: list[str] = []
    external: set[str] = set()

    def walk(gid: str):
        if gid in seen:
            return
        if gid in out_of_scope_set:
            fail("CHEM_ENG_REQUIRED_DEPENDENCY_OUT_OF_SCOPE", gid)
        if gid in optional_set and gid not in direct_set:
            fail("CHEM_ENG_OPTIONAL_GATE_REQUIRED_BY_CLOSURE", gid)
        if gid in visiting:
            i = visiting.index(gid)
            fail("CHEM_ENG_DEPENDENCY_CYCLE", " -> ".join(visiting[i:] + [gid]))
        gate = gate_map.get(gid)
        if gate is None:
            seen.add(gid)
            ordered.append(gid)
            return
        visiting.append(gid)
        for edge in edges_by_source.get(gid, []):
            effect = edge["closure_effect"]
            if effect == "REQUIRED_GATE":
                walk(edge["target_id"])
            elif effect == "REQUIRED_EXTERNAL_RESOLUTION":
                external.add(edge["target_id"])
            elif effect == "NON_REQUIRED_REFERENCE":
                continue
            else:
                fail("CHEM_ENG_TOPOLOGY_EFFECT_UNKNOWN", effect)
        visiting.pop()
        seen.add(gid)
        ordered.append(gid)

    for gid in direct:
        walk(gid)

    blockers: list[dict] = []
    gate_states: list[dict] = []
    for gid in ordered:
        gate = gate_map.get(gid)
        if gate is None:
            gate_states.append({"gate_id": gid, "status": "MISSING", "direct": gid in direct_set})
            blockers.append({"code": "CHEM_ENG_GATE_MISSING", "gate_id": gid, "message": f"required gate {gid} missing"})
            continue
        status = gate["technical_readiness"]
        gate_states.append({"gate_id": gid, "status": status, "direct": gid in direct_set})
        if status != "ENGINEERING_GATE_READY":
            blockers.append({"code": "CHEM_ENG_GATE_NOT_READY", "gate_id": gid, "message": f"{gid} status is {status}"})

    source_audit_payloads = source_audit_payloads or {}
    source_audit_states: list[dict] = []
    audited_gates: set[str] = set()
    for declaration in manifest["source_audits"]:
        gid = declaration["gate_id"]
        if gid in audited_gates:
            fail("CHEM_ENG_SOURCE_AUDIT_DUPLICATE", f"multiple source audits declared for {gid}")
        audited_gates.add(gid)
        if gid not in ordered:
            fail("CHEM_ENG_SOURCE_AUDIT_OUTSIDE_CLOSURE", f"source audit gate {gid} is not in closure")
        audit_ref = declaration["audit_ref"]
        audit = source_audit_payloads.get(audit_ref)
        if audit is None:
            audit = load(audit_ref)
        if audit.get("gate_id") != gid:
            fail("CHEM_ENG_SOURCE_AUDIT_GATE_MISMATCH", f"manifest={gid} audit={audit.get('gate_id')}")
        if audit.get("base_registry_ref") != manifest["registry_ref"]:
            fail("CHEM_ENG_SOURCE_AUDIT_REGISTRY_MISMATCH", f"{audit_ref} binds a different registry")
        try:
            result = validate_source_audit(audit, registry)
        except ChemistrySourceAuditError as exc:
            fail("CHEM_ENG_SOURCE_AUDIT_INVALID", f"{exc.code}: {exc.message}")
        source_audit_states.append({
            "gate_id": gid,
            "audit_ref": audit_ref,
            "audit_digest": digest(audit),
            "status": result["audit_status"],
            "scope_policy": audit["effective_provenance"]["scope_policy"],
            "audit_role": result["audit_role"],
            "authority_effect": result["authority_effect"],
        })

    resolution_map = {r["dependency_id"]: r for r in manifest["external_prerequisite_resolutions"]}
    external_states: list[dict] = []
    for dep in sorted(external):
        resolution = resolution_map.get(dep)
        if not resolution:
            external_states.append({"dependency_id": dep, "status": "UNRESOLVED", "evidence_ref": "NONE"})
            blockers.append({"code": "CHEM_ENG_EXTERNAL_PREREQ_UNRESOLVED", "dependency_id": dep, "message": f"external prerequisite {dep} unresolved"})
            continue
        external_states.append({"dependency_id": dep, "status": resolution["status"], "evidence_ref": resolution["evidence_ref"]})
        if resolution["status"] == "BLOCKED":
            blockers.append({"code": "CHEM_ENG_EXTERNAL_PREREQ_UNRESOLVED", "dependency_id": dep, "message": f"external prerequisite {dep} blocked"})

    if request["engineering_depth"] == "RESEARCH":
        _research_artifact(request, manifest, "research_dossier_ref", "contracts/chemistry-engineering-research-dossier.schema.json", "RESEARCH_DOSSIER_READY", research_dossier, "CHEM_ENG_RESEARCH_DOSSIER_REQUIRED", "CHEM_ENG_RESEARCH_DOSSIER_INVALID", blockers)
        _research_artifact(request, manifest, "claim_ledger_ref", "contracts/chemistry-engineering-claim-ledger.schema.json", "CLAIM_LEDGER_READY", claim_ledger, "CHEM_ENG_RESEARCH_DOSSIER_REQUIRED", "CHEM_ENG_RESEARCH_DOSSIER_INVALID", blockers)

    ready_count = sum(s["status"] == "ENGINEERING_GATE_READY" for s in gate_states)
    blocked_count = len(gate_states) - ready_count
    external_blocked = sum(s["status"] in {"BLOCKED", "UNRESOLVED"} for s in external_states)
    closure_status = "BLOCKED" if blockers else "READY"
    registry_digest = digest(registry)
    production_audits = sum(s["audit_role"] == "PRODUCTION_SOURCE_AUDIT" for s in source_audit_states)
    stress_audits = sum(s["audit_role"] == "STRESS_TEST_SOURCE_AUDIT" for s in source_audit_states)
    typed_topology = topology["counts"]["explicit_edge_count"] > 0

    payload = {
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "registry_digest": registry_digest,
        "source_audit_states": source_audit_states,
        "direct_gate_ids": direct,
        "optional_gate_ids": optional,
        "out_of_scope_gate_ids": out_of_scope,
        "closure_gate_ids": ordered,
        "gate_states": gate_states,
        "external_dependency_states": external_states,
        "blockers": blockers,
        "closure_status": closure_status,
        "source_item_status": manifest["source_item_status"],
    }
    if typed_topology:
        payload.update({
            "topology_id": topology["topology_id"],
            "topology_digest": topology["topology_digest"],
            "topology_extension_id": topology["extension_id"],
            "topology_extension_digest": topology["extension_digest"],
        })
    note = (
        "technical engineering closure READY; source-scope authorization, pedagogy, learner state and publication remain independent"
        if closure_status == "READY"
        else "technical engineering closure BLOCKED; downstream engineering consumption forbidden"
    )
    receipt = {
        "schema_version": "2.0.0",
        "receipt_id": manifest["manifest_id"].replace("CHEM-ENG-MAN-", "CHEM-ENG-CLOSURE-", 1),
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "registry_ref": manifest["registry_ref"],
        "registry_digest": registry_digest,
        "source_audit_states": source_audit_states,
        "closure_digest": digest(payload),
        "direct_gate_ids": direct,
        "optional_gate_ids": optional,
        "out_of_scope_gate_ids": out_of_scope,
        "closure_gate_ids": ordered,
        "gate_states": gate_states,
        "external_dependency_states": external_states,
        "blockers": blockers,
        "counts": {
            "direct_gate_count": len(direct),
            "optional_gate_count": len(optional),
            "out_of_scope_gate_count": len(out_of_scope),
            "closure_gate_count": len(ordered),
            "ready_gate_count": ready_count,
            "blocked_gate_count": blocked_count,
            "external_dependency_count": len(external_states),
            "external_blocked_count": external_blocked,
            "source_audit_count": len(source_audit_states),
            "production_source_audit_count": production_audits,
            "stress_source_audit_count": stress_audits,
        },
        "closure_status": closure_status,
        "source_item_status": manifest["source_item_status"],
        "authority_note": note,
    }
    if typed_topology:
        receipt.update({
            "topology_id": topology["topology_id"],
            "topology_digest": topology["topology_digest"],
            "topology_extension_id": topology["extension_id"],
            "topology_extension_digest": topology["extension_digest"],
        })
    validate_schema(receipt, "contracts/chemistry-engineering-closure-receipt.schema.json", "CHEM_ENG_RECEIPT_SCHEMA")
    return receipt


def main():
    p = argparse.ArgumentParser()
    p.add_argument("request")
    p.add_argument("manifest")
    p.add_argument("--out")
    args = p.parse_args()
    receipt = compile_closure(load(args.request), load(args.manifest))
    text = json.dumps(receipt, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
