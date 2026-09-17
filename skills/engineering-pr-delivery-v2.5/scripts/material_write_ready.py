#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from relaylib import load_yaml
from inspect_git_context import inspect as inspect_git
from takeoverlib import current_routes,route_key
from validate_baton_readiness import expected_baton_ready
from validate_takeover_certification import is_takeover_certified
from validate_drift_receipt import validate_ep as validate_drift_ep


def evaluate(root:Path,candidate_id:str,branch:str|None=None,worktree:str|None=None)->dict:
    errors=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    baton,baton_errors=expected_baton_ready(root)
    if not baton:errors.append("BATON_READY is false: "+"; ".join(baton_errors[:5]))
    try:live=inspect_git(root,branch,worktree)
    except Exception as exc:return {"status":"FAIL","material_write_ready":False,"candidate_id":candidate_id,"errors":[str(exc)]}
    routes=current_routes(root,state);route=None
    for item in routes:
        if str(item.get("ep_id"))!=str(live.get("ep_id")):continue
        if item.get("mode")=="PARALLEL_LANE" and str(item.get("lane_id"))!=str(live.get("lane_id")):continue
        route=item;break
    if route is None:errors.append("live route does not map to a current certified execution route")
    else:
        certified,cert_errors=is_takeover_certified(root,route,candidate_id)
        if not certified:errors.append("TAKEOVER_CERTIFIED is false: "+"; ".join(cert_errors[:5]))
    execution=((state.get("status_planes") or {}).get("execution") or {});stop=((state.get("status_planes") or {}).get("stop") or {})
    if execution.get("material_authority")!="WRITE":errors.append("material_authority is not WRITE")
    if execution.get("can_continue") is not True:errors.append("execution.can_continue is not true")
    if stop.get("active") is True:errors.append(f"hard stop is active: {stop.get('category')}")
    if live.get("status")=="NEEDS_DRIFT_RECEIPT" and route is not None:
        ep=load_yaml(root/str(route.get("ep_path")));ref=(ep.get("git_basis") or {}).get("drift_receipt")
        if not ref:errors.append("live base moved and current EP has no drift receipt")
        else:
            de,_=validate_drift_ep(root,str(route.get("ep_path")),"WRITE")
            errors.extend("drift: "+x for x in de)
            path=root/str(ref)
            if path.exists():
                receipt=load_yaml(path)
                if str(receipt.get("to_base"))!=str(live.get("current_base_ref")):errors.append("drift receipt to_base does not match currently observed base ref")
    elif live.get("status")!="PASS":errors.append(f"live Git context is not write-ready: {live.get('status')}")
    return {"status":"PASS" if not errors else "FAIL","material_write_ready":not errors,"candidate_id":candidate_id,"route_key":route_key(route) if route else None,"git":live,"errors":errors}


def main():
    ap=argparse.ArgumentParser(description="Derive MATERIAL_WRITE_READY for one candidate on the live execution route.")
    ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--candidate-id",required=True);ap.add_argument("--branch");ap.add_argument("--worktree");a=ap.parse_args()
    out=evaluate(Path(a.repo_root).resolve(),a.candidate_id,a.branch,a.worktree);print(json.dumps(out,indent=2));raise SystemExit(0 if out["material_write_ready"] else 1)
if __name__=="__main__":main()
