#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import yaml
from relaylib import load_yaml
from github_projection_next import next_action

def _dump(path:Path,data:dict):path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def begin(root:Path,basis:list[str],apply:bool=False)->dict:
    action=next_action(root)
    if action.get("action")!="PUBLISH":return {"status":"ERROR","next":action,"applied":False}
    state_path=root/"agents/relay/REPO_STATE.yaml";state=load_yaml(state_path);plan_path=root/state["projection"]["plan"];plan=load_yaml(plan_path);oid=action["operation_id"]
    op=next(x for x in plan.get("operations",[]) if x.get("id")==oid);pub=op.setdefault("publication",{})
    op["state"]="ATTEMPTED_UNCONFIRMED";pub["attempt_count"]=int(pub.get("attempt_count") or 0)+1;pub["last_attempt_basis"]=list(basis);pub["receipt"]=None;pub["last_error"]=None
    plan["generation"]["state"]="PUBLISHING";state["projection"]["state"]="PENDING";state["projection"]["receipt"]=None;state["relay_readiness"]["projection_ready"]=False;state["relay_readiness"]["handover_ready"]=False
    if apply:_dump(plan_path,plan);_dump(state_path,state)
    return {"status":"OK","action":"CALL_EXTERNAL_GITHUB","generation_id":plan["generation"]["id"],"operation_id":oid,"kind":op["kind"],"idempotency_key":op["idempotency_key"],"subject":op.get("subject") or {},"desired":op.get("desired") or {},"attempt_count":pub["attempt_count"],"applied":apply}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--basis",action="append",required=True);ap.add_argument("--apply",action="store_true");a=ap.parse_args();print(json.dumps(begin(Path(a.repo_root).resolve(),a.basis,a.apply),indent=2,sort_keys=True))
if __name__=="__main__":main()
