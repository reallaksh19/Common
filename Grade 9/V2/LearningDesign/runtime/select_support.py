#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()

def digest(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def select_support(plan, state):
    if state["learning_design_id"] != plan["learning_design_id"]:
        raise ValueError("live state references different frozen design")
    if state["unit_id"] not in {u["unit_id"] for u in plan["units"]}:
        raise ValueError("live state references unknown unit")
    approved=plan["runtime_support_contract"]["approved_rungs"]
    by_id={r["rung_id"]:r for r in approved}
    for used in state["rungs_used"]:
        if used not in by_id:
            raise ValueError(f"unapproved rung in runtime state: {used}")
    if state["response_status"]=="CORRECT":
        rung=None; reason="CORRECT_NO_SUPPORT"
    elif state["access_request"]:
        rung=next((r for r in approved if r["support_class"]=="ACCESS" and r["rung_id"] not in state["rungs_used"]),None)
        reason="ACCESS_REQUEST"
    elif state["consecutive_unsuccessful_attempts"] >= plan["runtime_support_contract"]["max_same_route_failures"]:
        rung=next((r for r in approved if r["support_class"]=="CONCEPTUAL" and r["route_mode"]=="ROUTE_CHANGE" and r["rung_id"] not in state["rungs_used"]),None)
        reason="REPEATED_SAME_ROUTE_FAILURE"
    else:
        rung=next((r for r in approved if r["support_class"]=="CONCEPTUAL" and r["route_mode"]=="SAME_ROUTE" and r["rung_id"] not in state["rungs_used"]),None)
        reason="NEXT_APPROVED_SUPPORT"
    return {
      "selection_id":"SEL-"+hashlib.sha256((plan["learning_design_id"]+"|"+state["state_id"]+"|"+(rung["rung_id"] if rung else "NONE")).encode()).hexdigest()[:16],
      "learning_design_id":plan["learning_design_id"],
      "frozen_design_digest":digest(plan),
      "unit_id":state["unit_id"],
      "rung_id":None if rung is None else rung["rung_id"],
      "support_class":None if rung is None else rung["support_class"],
      "route_mode":None if rung is None else rung["route_mode"],
      "support_features":[] if rung is None else copy.deepcopy(rung["support_features"]),
      "reason":reason
    }

def validate_selection(plan, selection):
    if selection["learning_design_id"]!=plan["learning_design_id"] or selection["frozen_design_digest"]!=digest(plan):
        raise ValueError("runtime selection not bound to exact frozen design")
    approved={r["rung_id"]:r for r in plan["runtime_support_contract"]["approved_rungs"]}
    rid=selection["rung_id"]
    if rid is not None and rid not in approved:
        raise ValueError("runtime selected unapproved rung")
    if rid is not None:
        r=approved[rid]
        for k in ("support_class","route_mode","support_features"):
            if selection[k]!=r[k]:
                raise ValueError("runtime altered approved rung semantics")
    return True

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--plan",required=True); ap.add_argument("--state",required=True)
    a=ap.parse_args()
    plan=json.loads(Path(a.plan).read_text()); state=json.loads(Path(a.state).read_text())
    sel=select_support(plan,state); validate_selection(plan,sel)
    sys.stdout.write(json.dumps(sel,sort_keys=True,indent=2)+"\n")
if __name__=="__main__": main()
