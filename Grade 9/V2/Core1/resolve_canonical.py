#!/usr/bin/env python3
"""Deterministic V2 Core1 canonical dependency resolver.

No historical PR module is imported. This module is intentionally dependency-free.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1.0"
FORBIDDEN_KEYS = {"learner","learner_state","learner_profile","mastery","mastery_score","study_decision","study_priority","teaching_decision","teaching_sequence","reteach","repair_decision","benchmark","benchmark_id","benchmark_refs","benchmark_page","pr156_reference","pr157_reference"}

class CanonicalError(ValueError):
    pass

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_obj(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def _semantic_projection(asset: dict[str, Any]) -> dict[str, Any]:
    return {"canonical_id":asset["canonical_id"],"asset_version":asset["asset_version"],"subject_domain":asset["subject_domain"],"semantic_kind":asset["semantic_kind"],"semantic_payload":asset["semantic_payload"],"conditions":asset["conditions"],"dependencies":asset["dependencies"],"representation_refs":asset["representation_refs"]}

def compute_asset_digest(asset: dict[str, Any]) -> str:
    return sha256_obj(_semantic_projection(asset))

def _scan_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                raise CanonicalError(f"forbidden producer field {path}.{key}")
            _scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_forbidden(child, f"{path}[{index}]")

def validate_registry(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if set(registry) != {"schema_version","registry_version","resolver_policy_version","assets"}:
        raise CanonicalError("registry fields do not match V2 contract")
    if registry["schema_version"] != SCHEMA_VERSION:
        raise CanonicalError("unsupported registry schema_version")
    if not registry["registry_version"] or not registry["resolver_policy_version"]:
        raise CanonicalError("registry/policy version must be explicit")
    if not isinstance(registry["assets"], list):
        raise CanonicalError("assets must be a list")
    _scan_forbidden(registry)
    by_id = {}
    required = {"canonical_id","asset_version","subject_domain","semantic_kind","promotion_state","semantic_payload","conditions","dependencies","provenance_refs","representation_refs","requires_revalidation","semantic_digest"}
    for asset in registry["assets"]:
        if set(asset) != required:
            raise CanonicalError(f"asset fields invalid for {asset.get('canonical_id','<unknown>')}")
        cid = asset["canonical_id"]
        if cid in by_id:
            raise CanonicalError(f"duplicate canonical_id: {cid}")
        if asset["promotion_state"] not in {"RESEARCH_CANDIDATE","SUBJECT_AUTHORITY_REVIEW","PROMOTED","REJECTED"}:
            raise CanonicalError(f"invalid promotion_state: {cid}")
        if not asset["provenance_refs"]:
            raise CanonicalError(f"missing provenance_refs: {cid}")
        for dep in asset["dependencies"]:
            if set(dep) != {"canonical_id","relation","reason"} or dep["relation"] not in {"REQUIRES","USES_SHARED","REFINES"} or not dep["reason"]:
                raise CanonicalError(f"invalid dependency shape/relation: {cid}")
        if asset["semantic_digest"] != compute_asset_digest(asset):
            raise CanonicalError(f"semantic digest mismatch: {cid}")
        by_id[cid] = asset
    visiting, visited = set(), set()
    def walk(cid: str) -> None:
        if cid in visiting:
            raise CanonicalError(f"dependency cycle detected at {cid}")
        if cid in visited or cid not in by_id:
            return
        visiting.add(cid)
        for dep in by_id[cid]["dependencies"]:
            if dep["canonical_id"] in by_id:
                walk(dep["canonical_id"])
        visiting.remove(cid); visited.add(cid)
    for cid in sorted(by_id): walk(cid)
    return by_id

def _resolved_asset(asset: dict[str, Any]) -> dict[str, Any]:
    return {k:asset[k] for k in ("canonical_id","asset_version","subject_domain","semantic_kind","semantic_digest")}

def _gap(requested_canonical_id: str, requested_by: str, reason: str, registry_version: str, resolution_failure: str) -> dict[str, Any]:
    seed = {"requested_canonical_id":requested_canonical_id,"requested_by":requested_by,"reason":reason,"registry_version":registry_version,"resolution_failure":resolution_failure}
    return {"gap_id":"GAP-"+sha256_obj(seed)[:16], **seed, "status":"OPEN"}

def resolve_canonical(registry: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    by_id = validate_registry(registry)
    if set(request) != {"schema_version","request_id","expected_registry_version","primary_ids"}:
        raise CanonicalError("request fields do not match V2 contract")
    if request["schema_version"] != SCHEMA_VERSION or request["expected_registry_version"] != registry["registry_version"]:
        raise CanonicalError("request schema/registry version mismatch")
    if not isinstance(request["primary_ids"], list) or not request["primary_ids"] or len(set(request["primary_ids"])) != len(request["primary_ids"]):
        raise CanonicalError("primary_ids must be a non-empty unique list")
    _scan_forbidden(request)
    primary_ids = sorted(request["primary_ids"]); primary_set = set(primary_ids)
    dependencies, edges, gaps = set(), {}, {}
    def require(cid: str, requested_by: str, reason: str, role: str) -> None:
        asset = by_id.get(cid)
        if asset is None:
            g = _gap(cid, requested_by, reason, registry["registry_version"], "MISSING_ASSET"); gaps[g["gap_id"]] = g; return
        if asset["promotion_state"] != "PROMOTED":
            g = _gap(cid, requested_by, reason, registry["registry_version"], "NOT_PROMOTED"); gaps[g["gap_id"]] = g; return
        if role == "DEPENDENCY" and cid not in primary_set: dependencies.add(cid)
        for dep in sorted(asset["dependencies"], key=lambda d:(d["canonical_id"],d["relation"],d["reason"])):
            edge = {"from":cid,"to":dep["canonical_id"],"relation":dep["relation"],"reason":dep["reason"]}; edges[(edge["from"],edge["to"],edge["relation"],edge["reason"])] = edge
            require(dep["canonical_id"], cid, dep["reason"], "DEPENDENCY")
    for cid in primary_ids: require(cid, request["request_id"], "primary request", "PRIMARY")
    if gaps:
        return {"schema_version":SCHEMA_VERSION,"status":"CANONICAL_GAP","request_id":request["request_id"],"canonical_registry_version":registry["registry_version"],"resolver_policy_version":registry["resolver_policy_version"],"gap_candidates":[gaps[k] for k in sorted(gaps)]}
    result = {"schema_version":SCHEMA_VERSION,"status":"SUCCESS","request_id":request["request_id"],"canonical_registry_version":registry["registry_version"],"resolver_policy_version":registry["resolver_policy_version"],"primary_assets":[_resolved_asset(by_id[c]) for c in primary_ids],"dependency_assets":[_resolved_asset(by_id[c]) for c in sorted(dependencies)],"dependency_edges":[edges[k] for k in sorted(edges)],"resolution_records":[]}
    for cid in primary_ids:
        result["resolution_records"].append({"canonical_id":cid,"role":"PRIMARY","action":"REVALIDATE" if by_id[cid]["requires_revalidation"] else "REUSE_EXISTING"})
    for cid in sorted(dependencies):
        result["resolution_records"].append({"canonical_id":cid,"role":"DEPENDENCY","action":"REVALIDATE" if by_id[cid]["requires_revalidation"] else "COMPOSE_DEPENDENCY"})
    result["knowledge_set_digest"] = sha256_obj(result)
    return result

def render_bytes(result: dict[str, Any]) -> bytes:
    return (canonical_json(result)+"\n").encode("utf-8")

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--registry",required=True,type=Path); p.add_argument("--request",required=True,type=Path); p.add_argument("--out",type=Path); a=p.parse_args()
    try: result=resolve_canonical(json.loads(a.registry.read_text()),json.loads(a.request.read_text()))
    except (CanonicalError,KeyError,TypeError,json.JSONDecodeError) as exc: print(f"CORE1_CANONICAL_FAIL: {exc}"); return 1
    data=render_bytes(result); a.out.write_bytes(data) if a.out else print(data.decode(),end="")
    return 2 if result["status"]=="CANONICAL_GAP" else 0
if __name__ == "__main__": raise SystemExit(main())
