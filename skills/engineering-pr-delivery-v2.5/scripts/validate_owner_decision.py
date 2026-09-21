#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require

KINDS={"INTENT_MUTATION","DEFERRAL","AUTHORIZATION","DECLINE","NO_CHANGE_CONFIRMATION"}
REQUIREMENT={"NOT_APPLICABLE","SATISFIED","PENDING_NOT_SATISFIED"}
STATUSES={"CAPTURED","APPLIED","SUPERSEDED"}

def validate_file(path:Path):
    e=[];w=[];odr=load_yaml(path);e+=require(odr,["schema_version","id","decision","effects","impact","affected","required_reconciliation","status"],"ODR")
    if odr.get("schema_version")!="relay-v2.5":e.append("ODR: schema_version must be relay-v2.5")
    d=odr.get("decision") or {};e+=require(d,["authority","kind","statement","source"],"ODR.decision")
    if d.get("authority")!="OWNER":e.append("ODR.decision.authority must be OWNER")
    kind=d.get("kind")
    if kind not in KINDS:e.append(f"ODR.decision.kind invalid: {kind}")
    if not str(d.get("statement","")).strip():e.append("ODR.decision.statement is required")
    if not str(d.get("source","")).strip():e.append("ODR.decision.source is required")
    effects=odr.get("effects") or {};e+=require(effects,["requirement_disposition","grants_material_write_authority","pending_items"],"ODR.effects")
    disposition=effects.get("requirement_disposition")
    if disposition not in REQUIREMENT:e.append(f"ODR.effects.requirement_disposition invalid: {disposition}")
    if not isinstance(effects.get("grants_material_write_authority"),bool):e.append("ODR.effects.grants_material_write_authority must be boolean")
    if not isinstance(effects.get("pending_items"),list):e.append("ODR.effects.pending_items must be a list")
    if kind=="DEFERRAL":
        if disposition!="PENDING_NOT_SATISFIED":e.append("DEFERRAL must keep requirement_disposition PENDING_NOT_SATISFIED")
        if effects.get("grants_material_write_authority") is not False:e.append("DEFERRAL must not grant material write authority")
        if not effects.get("pending_items"):e.append("DEFERRAL must name at least one pending item")
    if disposition=="SATISFIED" and effects.get("pending_items"):e.append("SATISFIED requirement disposition must not retain pending_items")
    override=odr.get("execution_override")
    if override is not None:
        if kind!="AUTHORIZATION":e.append("execution_override is valid only for decision.kind AUTHORIZATION")
        if not isinstance(override,dict):e.append("execution_override must be mapping or null")
        else:
            if override.get("disposition") not in {"GRANTED","REVOKED"}:e.append("execution_override.disposition invalid")
            scope=override.get("scope") or {}
            e+=require(scope,["repository","branch","allowed_write_paths"],"ODR.execution_override.scope")
            if not str(scope.get("repository") or "").strip():e.append("execution_override.scope.repository must be explicit")
            if not str(scope.get("branch") or "").strip():e.append("execution_override.scope.branch must be explicit")
            paths=scope.get("allowed_write_paths")
            if not isinstance(paths,list) or not paths or any(not str(x).strip() for x in paths):e.append("execution_override.scope.allowed_write_paths must be a non-empty explicit list")
            defers=override.get("defers")
            allowed_defers={"CANDIDATE_ADMISSION","ROUTE_RECONCILIATION","LOCAL_VALIDATION_ENVIRONMENT","EVIDENCE_COLLECTION"}
            if not isinstance(defers,list) or not defers:e.append("execution_override.defers must be a non-empty list")
            elif any(x not in allowed_defers for x in defers):e.append("execution_override.defers contains unsupported/non-deferrable control")
            allows=override.get("allows")
            allowed_actions={"BOUNDED_PRODUCT_WRITES","TESTS","DRAFT_PR_UPDATES"}
            if not isinstance(allows,list) or not allows:e.append("execution_override.allows must be a non-empty list")
            elif any(x not in allowed_actions for x in allows):e.append("execution_override.allows contains unsupported action")
            blocks=override.get("blocks")
            allowed_blocks={"PR_READY","MERGE","CHECKPOINT","RELEASE"}
            if not isinstance(blocks,list) or not blocks:e.append("execution_override.blocks must be a non-empty list")
            elif any(x not in allowed_blocks for x in blocks):e.append("execution_override.blocks contains unsupported boundary")
            pending=override.get("pending_obligations")
            if not isinstance(pending,list) or not pending or any(not str(x).startswith("PEND-") for x in pending):
                e.append("execution_override.pending_obligations must name at least one PEND-* obligation")
            if override.get("disposition")=="GRANTED":
                if effects.get("grants_material_write_authority") is not True:e.append("GRANTED execution_override requires effects.grants_material_write_authority=true")
                if "BOUNDED_PRODUCT_WRITES" in (allows or []) and not {"PR_READY","MERGE"}.issubset(set(blocks or [])):
                    e.append("bounded product-write override must keep PR_READY and MERGE blocked")
            if override.get("disposition")=="REVOKED" and effects.get("grants_material_write_authority") is not False:
                e.append("REVOKED execution_override must not grant material write authority")
    auth=odr.get("delivery_authorization")
    if auth is not None:
        if kind!="AUTHORIZATION":e.append("delivery_authorization is valid only for decision.kind AUTHORIZATION")
        if not isinstance(auth,dict):e.append("delivery_authorization must be mapping or null")
        else:
            if auth.get("action")!="MERGE":e.append("delivery_authorization.action must be MERGE")
            if auth.get("provider")!="GITHUB":e.append("delivery_authorization.provider must be GITHUB")
            if auth.get("vehicle")!="PULL_REQUEST":e.append("delivery_authorization.vehicle must be PULL_REQUEST")
            if not str(auth.get("repository") or "").strip():e.append("delivery_authorization.repository must be explicit")
            if not isinstance(auth.get("number"),int) or auth.get("number")<1:e.append("delivery_authorization.number must be positive integer")
            if not str(auth.get("head_sha") or "").strip():e.append("delivery_authorization.head_sha must be explicit exact PR head")
            if auth.get("disposition") not in {"GRANTED","REVOKED"}:e.append("delivery_authorization.disposition invalid")
            if effects.get("grants_material_write_authority") is not False:e.append("delivery merge authorization must not grant material write authority")
    elif kind=="AUTHORIZATION" and override is None:
        w.append("AUTHORIZATION decision has no structured delivery_authorization or execution_override; it grants no structured execution/delivery authority")
    if odr.get("status") not in STATUSES:e.append("ODR.status invalid")
    return e,w

def validate(root:Path):
    base=root/"agents/relay/roadmap/owner-decisions"
    if not base.exists():return [],[]
    e=[];w=[]
    for path in sorted(list(base.glob("*.yaml"))+list(base.glob("*.yml"))):
        ce,cw=validate_file(path);e.extend(f"{path.name}: {x}" for x in ce);w.extend(f"{path.name}: {x}" for x in cw)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("target",nargs="?",default=".");a=ap.parse_args();target=Path(a.target).resolve()
    try:e,w=validate_file(target) if target.is_file() else validate(target)
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
