#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def select_support(plan,state):
    if state["learning_design_id"] != plan["learning_design_id"]:
        raise ValueError("state/design mismatch")
    rungs={r["rung_id"]:r for r in plan["support_ladder"]}
    if state.get("access_request"):
        candidates=[r for r in rungs.values() if r["support_class"]=="ACCESS"]
    elif state["consecutive_unsuccessful_attempts"] >= 2:
        candidates=[r for r in rungs.values() if r["support_class"]=="CONCEPTUAL" and r["route"]=="ROUTE_CHANGE"]
    else:
        candidates=[r for r in rungs.values() if r["support_class"]=="CONCEPTUAL" and r["route"]=="SAME_ROUTE" and r["rung_id"] not in state["rungs_used"]]
    if not candidates: raise ValueError("no approved support rung")
    rung=sorted(candidates,key=lambda x:x["rung_id"])[0]
    return {"learning_design_id":plan["learning_design_id"],"state_id":state["state_id"],"rung_id":rung["rung_id"],"support_class":rung["support_class"],"route":rung["route"],"plan_digest":plan["design_digest"]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--plan",required=True); ap.add_argument("--state",required=True)
    a=ap.parse_args()
    plan=json.loads(Path(a.plan).read_text()); state=json.loads(Path(a.state).read_text())
    print(json.dumps(select_support(plan,state),sort_keys=True,indent=2))
if __name__=="__main__": main()
