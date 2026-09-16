#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require
REQ=["schema_version","checkpoint_id","ep_id","roadmap_basis","implementation_result","acceptance_results","validation_results","quality_findings","discoveries","roadmap_reconciliation","successor"]

def validate_file(path:Path):
    e=[];w=[];cp=load_yaml(path);e+=require(cp,REQ,"CP")
    if cp.get("schema_version")!="relay-v2.5":e.append("CP: schema_version must be relay-v2.5")
    if (cp.get("roadmap_reconciliation") or {}).get("result") not in {"NO_ROADMAP_CHANGE","STATUS_UPDATE","ROADMAP_PROPOSAL","OWNER_DECISION_REQUIRED"}:e.append("CP: invalid roadmap_reconciliation.result")
    successor=cp.get("successor") or {};e+=require(successor,["mode","frontier_work_package","ep_id","parallel_plan","lanes"],"CP.successor")
    mode=successor.get("mode")
    if mode not in {"SERIAL","PARALLEL","NONE"}:e.append(f"CP.successor.mode invalid: {mode}")
    if mode=="SERIAL":
        if not successor.get("frontier_work_package") or not successor.get("ep_id"):e.append("SERIAL successor requires frontier_work_package and ep_id")
        if successor.get("parallel_plan") not in {None,""} or successor.get("lanes"):e.append("SERIAL successor must not declare parallel plan/lanes")
    elif mode=="PARALLEL":
        if not successor.get("parallel_plan"):e.append("PARALLEL successor requires parallel_plan id")
        if len(successor.get("lanes") or [])<2:e.append("PARALLEL successor requires at least two lane receipts")
        if successor.get("frontier_work_package") not in {None,""} or successor.get("ep_id") not in {None,""}:e.append("PARALLEL successor uses lane receipts, not singular frontier_work_package/ep_id")
    elif mode=="NONE":
        if successor.get("frontier_work_package") not in {None,""} or successor.get("ep_id") not in {None,""} or successor.get("parallel_plan") not in {None,""} or successor.get("lanes"):e.append("NONE successor must not declare downstream work")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("checkpoint");a=ap.parse_args()
    try:e,w=validate_file(Path(a.checkpoint).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
