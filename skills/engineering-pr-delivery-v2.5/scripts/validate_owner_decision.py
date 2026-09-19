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
    elif kind=="AUTHORIZATION":
        w.append("AUTHORIZATION decision has no structured delivery_authorization; it does not grant merge authority")
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
