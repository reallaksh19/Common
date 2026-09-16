#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_ep_semantics import MANDATORY_REPORT_SECTIONS


def _text_list(value):
    return isinstance(value,list) and bool(value) and all(isinstance(x,str) and x.strip() for x in value)


def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);report=ep.get("report_contract") or {}
    sections=[str(x) for x in report.get("sections",[]) or []]
    for item in MANDATORY_REPORT_SECTIONS:
        if item not in sections:e.append(f"EP report_contract missing mandatory section: {item}")
    payloads=report.get("payloads")
    if not isinstance(payloads,list):return e+["EP report_contract.payloads must be a list"],w
    by_section={}
    for i,item in enumerate(payloads):
        label=f"EP report_contract.payloads[{i}]"
        if not isinstance(item,dict):e.append(f"{label} must be a mapping");continue
        section=str(item.get("section","")).strip()
        if not section:e.append(f"{label}.section must be explicit")
        elif section in by_section:e.append(f"{label}.section duplicates payload for {section}")
        else:by_section[section]=item
        if not str(item.get("id","")).strip():e.append(f"{label}.id must be explicit")
        if not _text_list(item.get("sources")):e.append(f"{label}.sources must identify source objects")
        if not _text_list(item.get("required_fields")):e.append(f"{label}.required_fields must define reconciliation payload")
    for section in MANDATORY_REPORT_SECTIONS:
        if section in sections and section not in by_section:e.append(f"EP report_contract heading has no reconciliation payload: {section}")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
