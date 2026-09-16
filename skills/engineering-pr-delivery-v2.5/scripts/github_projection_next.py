#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from relaylib import load_yaml
from validate_github_projection import validate as validate_projection

UNCONFIRMED={"ATTEMPTED_UNCONFIRMED","PUBLISHED_UNCONFIRMED"}
DONE={"VERIFIED","SUPERSEDED"}

def next_action(root:Path)->dict:
    errors,_=validate_projection(root)
    if errors:return {"action":"INVALID","errors":errors}
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");projection=state.get("projection") or {};plan=load_yaml(root/projection["plan"]);ops=plan.get("operations",[]) or []
    uncertain=[x for x in ops if x.get("state") in UNCONFIRMED]
    if uncertain:
        op=uncertain[0]
        return {"action":"RECONCILE","generation_id":plan["generation"]["id"],"operation_id":op["id"],"kind":op["kind"],"idempotency_key":op["idempotency_key"],"reason":"An earlier external attempt is not verified. Read back the external surface before any retry or later publication."}
    failed=[x for x in ops if x.get("state")=="FAILED"]
    if failed:
        return {"action":"REVISE_GENERATION","generation_id":plan["generation"]["id"],"failed_operations":[x["id"] for x in failed],"reason":"A failed operation has no automatic retry authority; reconcile repository intent and prepare a successor generation."}
    by_id={x.get("id"):x for x in ops}
    for op in ops:
        if op.get("state")!="PREPARED":continue
        deps=op.get("depends_on",[]) or []
        if all((by_id.get(d) or {}).get("state") in DONE for d in deps):
            return {"action":"PUBLISH","generation_id":plan["generation"]["id"],"operation_id":op["id"],"kind":op["kind"],"idempotency_key":op["idempotency_key"],"desired":op.get("desired") or {},"subject":op.get("subject") or {},"reason":"This is the first prepared operation whose dependencies are reconciled."}
    if ops and all(x.get("state") in DONE for x in ops):return {"action":"COMPLETE","generation_id":plan["generation"]["id"],"reason":"Every operation is verified or superseded."}
    return {"action":"WAIT","generation_id":plan["generation"]["id"],"reason":"No operation is currently publishable; inspect dependency state."}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();print(json.dumps(next_action(Path(a.repo_root).resolve()),indent=2,sort_keys=True))
if __name__=="__main__":main()
