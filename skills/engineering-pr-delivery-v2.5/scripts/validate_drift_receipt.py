#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require

CLASSIFICATIONS={"DISJOINT","OVERLAPPING","UNKNOWN"}


def validate_ep(root:Path,ep_path:str):
    e=[];w=[];ep=load_yaml(root/ep_path);basis=ep.get("git_basis") or {}
    e+=require(basis,["expected_branch","material_ref","base_branch","base_observed_ref","drift_policy","drift_receipt"],f"{ep_path}.git_basis")
    if basis.get("drift_policy")!="RECHECK_BEFORE_WRITE":e.append(f"{ep_path}: git_basis.drift_policy must be RECHECK_BEFORE_WRITE")
    receipt_ref=basis.get("drift_receipt")
    if not receipt_ref:return e,w
    path=root/receipt_ref
    if not path.exists():return e+[f"{ep_path}: drift receipt does not exist: {receipt_ref}"],w
    receipt=load_yaml(path);e+=require(receipt,["schema_version","from_base","to_base","classification","changed_paths","affected_scope","rationale"],"DRIFT_RECEIPT")
    if receipt.get("schema_version")!="relay-v2.5-drift":e.append("DRIFT_RECEIPT.schema_version must be relay-v2.5-drift")
    if str(receipt.get("from_base"))!=str(basis.get("base_observed_ref")):e.append(f"{ep_path}: drift receipt from_base does not match EP base_observed_ref")
    classification=receipt.get("classification")
    if classification not in CLASSIFICATIONS:e.append(f"DRIFT_RECEIPT.classification invalid: {classification}")
    if not isinstance(receipt.get("changed_paths"),list):e.append("DRIFT_RECEIPT.changed_paths must be a list")
    if not isinstance(receipt.get("affected_scope"),list):e.append("DRIFT_RECEIPT.affected_scope must be a list")
    if not str(receipt.get("rationale","")).strip():e.append("DRIFT_RECEIPT.rationale must be explicit")
    if classification=="DISJOINT" and receipt.get("affected_scope"):e.append("DISJOINT drift receipt must have empty affected_scope")
    if classification in {"OVERLAPPING","UNKNOWN"}:e.append(f"{ep_path}: base drift is {classification}; EP must be reconciled before material execution")
    return e,w


def ep_paths(root:Path,state:dict):
    if state.get("relay_state")=="ACTIVE":return [(state.get("active_ep") or {}).get("path")]
    if state.get("relay_state")=="PARALLEL":
        plan=load_yaml(root/(state.get("execution_policy") or {})["parallel_plan"])
        return [x.get("ep_path") for x in plan.get("lanes",[]) or []]
    return []


def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    for path in ep_paths(root,s):
        if not path:e.append("active execution route is missing EP path");continue
        ce,cw=validate_ep(root,path);e.extend(ce);w.extend(cw)
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
