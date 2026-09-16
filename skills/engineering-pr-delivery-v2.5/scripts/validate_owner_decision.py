#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require

def validate_file(path:Path):
    e=[];w=[];odr=load_yaml(path);e+=require(odr,["schema_version","id","decision","impact","affected","required_reconciliation","status"],"ODR")
    if odr.get("schema_version")!="relay-v2.5":e.append("ODR: schema_version must be relay-v2.5")
    d=odr.get("decision") or {}
    if d.get("authority")!="OWNER":e.append("ODR.decision.authority must be OWNER")
    if not str(d.get("statement","")).strip():e.append("ODR.decision.statement is required")
    if odr.get("status") not in {"CAPTURED","APPLIED","SUPERSEDED"}:e.append("ODR.status invalid")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("odr");a=ap.parse_args()
    try:e,w=validate_file(Path(a.odr).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
