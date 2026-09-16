#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require
REQ=["schema_version","checkpoint_id","ep_id","roadmap_basis","implementation_result","acceptance_results","validation_results","quality_findings","discoveries","roadmap_reconciliation"]

def validate_file(path:Path):
    e=[];w=[];cp=load_yaml(path);e+=require(cp,REQ,"CP")
    if cp.get("schema_version")!="relay-v2.5":e.append("CP: schema_version must be relay-v2.5")
    if (cp.get("roadmap_reconciliation") or {}).get("result") not in {"NO_ROADMAP_CHANGE","STATUS_UPDATE","ROADMAP_PROPOSAL","OWNER_DECISION_REQUIRED"}:e.append("CP: invalid roadmap_reconciliation.result")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("checkpoint");a=ap.parse_args()
    try:e,w=validate_file(Path(a.checkpoint).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
