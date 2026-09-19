#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from relaylib import load_yaml,print_result,require

LIFECYCLE={"DRAFT","OPEN","CLOSED","MERGED","UNKNOWN"}
MERGEABILITY={"MERGEABLE","CONFLICTING","UNKNOWN"}
CHECKS={"PASS","FAIL","PENDING","NOT_RUN","STALE","UNKNOWN"}
REVIEWS={"CLEAR","CHANGES_REQUESTED","PENDING","UNKNOWN"}


def validate_file(path:Path,expected_repository:str|None=None,expected_id:str|None=None):
    e=[];w=[];obs=load_yaml(path)
    e+=require(obs,["schema_version","id","provider","repository","vehicle","mergeability","checks","review","readback_basis"],"DELIVERY_OBSERVATION")
    if obs.get("schema_version")!="relay-v2.5-delivery-observation":e.append("delivery observation schema_version invalid")
    if not str(obs.get("id") or "").startswith("DOBS-"):e.append("delivery observation id must use DOBS-* namespace")
    if expected_id and str(obs.get("id"))!=str(expected_id):e.append("delivery observation id does not match REPO_STATE pointer")
    if obs.get("provider")!="GITHUB":e.append("delivery observation provider must be GITHUB")
    if expected_repository and str(obs.get("repository"))!=str(expected_repository):e.append("delivery observation repository does not match REPO_STATE.repository.remote")

    vehicle=obs.get("vehicle") or {};e+=require(vehicle,["kind","number","url","lifecycle","head","base"],"delivery.vehicle")
    if vehicle.get("kind")!="PULL_REQUEST":e.append("delivery vehicle kind must be PULL_REQUEST")
    if not isinstance(vehicle.get("number"),int) or vehicle.get("number")<1:e.append("delivery PR number must be positive integer")
    if not str(vehicle.get("url") or "").strip():e.append("delivery PR URL must be explicit")
    if vehicle.get("lifecycle") not in LIFECYCLE:e.append(f"delivery lifecycle invalid: {vehicle.get('lifecycle')}")
    head=vehicle.get("head") or {};base=vehicle.get("base") or {}
    for name,value in (("head",head),("base",base)):
        if not isinstance(value,dict):e.append(f"delivery vehicle {name} must be mapping")
        else:
            if "ref" not in value or "sha" not in value:e.append(f"delivery vehicle {name} requires ref and sha")

    merge=obs.get("mergeability") or {}
    if merge.get("state") not in MERGEABILITY:e.append(f"delivery mergeability invalid: {merge.get('state')}")

    checks=obs.get("checks") or {};check_state=checks.get("state")
    if check_state not in CHECKS:e.append(f"delivery checks state invalid: {check_state}")
    if not isinstance(checks.get("required"),list) or not isinstance(checks.get("observations"),list):e.append("delivery checks required/observations must be lists")
    vehicle_head=head.get("sha");check_head=checks.get("head_sha")
    if check_state in {"PASS","FAIL","PENDING"}:
        if not vehicle_head or not check_head:e.append(f"delivery checks {check_state} requires exact vehicle/check head SHA")
        elif str(vehicle_head)!=str(check_head):e.append(f"delivery checks {check_state} must bind to current PR head; use STALE for an older head")
    if check_state=="STALE":
        if not vehicle_head or not check_head or str(vehicle_head)==str(check_head):e.append("delivery checks STALE requires a non-current observed check head SHA")

    review=obs.get("review") or {};review_state=review.get("state")
    if review_state not in REVIEWS:e.append(f"delivery review state invalid: {review_state}")
    for key in ("unresolved_threads","change_requests"):
        value=review.get(key)
        if value is not None and (not isinstance(value,int) or value<0):e.append(f"delivery review {key} must be non-negative integer or null")
    if review_state=="CLEAR":
        if review.get("unresolved_threads") not in {0,None} or review.get("change_requests") not in {0,None}:e.append("delivery review CLEAR cannot retain unresolved threads/change requests")

    basis=obs.get("readback_basis")
    if not isinstance(basis,list) or not basis or any(not str(x).strip() for x in basis):e.append("delivery observation requires durable provider readback_basis")
    return e,w


def validate(root:Path):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");delivery=state.get("delivery")
    if delivery is None:return [],[]
    e=[];w=[]
    if not isinstance(delivery,dict):return ["REPO_STATE.delivery must be mapping"],w
    required=delivery.get("required")
    if not isinstance(required,bool):e.append("REPO_STATE.delivery.required must be boolean")
    provider=delivery.get("provider");ptr=delivery.get("observation") or {}
    if required is False:
        if provider not in {None,""}:e.append("delivery not required must not name a provider")
        if ptr.get("id") not in {None,""} or ptr.get("path") not in {None,""}:e.append("delivery not required must not point at an observation")
        return e,w
    if provider!="GITHUB":e.append("required delivery currently supports provider GITHUB")
    oid=ptr.get("id");opath=ptr.get("path")
    if not str(oid or "").startswith("DOBS-"):e.append("required delivery observation.id must use DOBS-* namespace")
    if not str(opath or "").strip():e.append("required delivery observation.path must be explicit")
    elif not (root/str(opath)).exists():e.append(f"delivery observation path missing: {opath}")
    else:
        ce,cw=validate_file(root/str(opath),(state.get("repository") or {}).get("remote"),oid)
        e.extend(ce);w.extend(cw)
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("target",nargs="?",default=".");a=ap.parse_args();target=Path(a.target).resolve()
    try:e,w=validate_file(target) if target.is_file() else validate(target)
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))


if __name__=="__main__":
    main()
