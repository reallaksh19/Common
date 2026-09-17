#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require,scan_context_phrases
REQ=["schema_version","identity","git_basis","roadmap_source","outcome","context_capsule","repository_discovery","inputs","benchmarks","scope","anti_drift","implementation_plan","quality","acceptance","validation","failure_and_stop_conditions","report_contract","checkpoint_contract","successor_relay"]
NONE_IDS={None,"","NONE"}

def validate_ep_data(root:Path,ep:dict,label="EP"):
    e=[];w=[];e+=require(ep,REQ,label)
    if ep.get("schema_version")!="relay-v2.5":e.append(f"{label}: schema_version must be relay-v2.5")
    e+=[f"{label}{x[1:]}" if x.startswith("$") else f"{label}: {x}" for x in scan_context_phrases(ep)]
    identity=ep.get("identity") or {};e+=require(identity,["ep_id","branch","base_ref","execution_state","previous_checkpoint"],f"{label}.identity")
    predecessor_values=[identity.get("previous_checkpoint"),identity.get("previous_join"),identity.get("previous_replan")]
    if sum(x not in NONE_IDS for x in predecessor_values)>1:e.append(f"{label}.identity may declare only one of previous_checkpoint, previous_join, previous_replan")
    if identity.get("previous_replan") not in NONE_IDS:
        inh=ep.get("replan_inheritance") or {}
        if str(inh.get("from_replan"))!=str(identity.get("previous_replan")):e.append(f"{label}.replan_inheritance.from_replan must match identity.previous_replan")
        if "unresolved_acceptance" not in inh or "evidence" not in inh:e.append(f"{label}.replan_inheritance must retain unresolved_acceptance and evidence")
    elif ep.get("replan_inheritance") not in (None,{}):
        e.append(f"{label}.replan_inheritance requires identity.previous_replan")
    git_basis=ep.get("git_basis") or {};e+=require(git_basis,["expected_branch","material_ref","base_branch","base_observed_ref","drift_policy","drift_receipt"],f"{label}.git_basis")
    if git_basis.get("drift_policy")!="RECHECK_BEFORE_WRITE":e.append(f"{label}.git_basis.drift_policy must be RECHECK_BEFORE_WRITE")
    if git_basis.get("expected_branch") and identity.get("branch") and git_basis.get("expected_branch")!=identity.get("branch"):e.append(f"{label}.git_basis.expected_branch must match identity.branch")
    if git_basis.get("material_ref") and identity.get("base_ref") and str(git_basis.get("material_ref"))!=str(identity.get("base_ref")):e.append(f"{label}.git_basis.material_ref must match identity.base_ref")
    e+=require(ep.get("roadmap_source") or {},["roadmap_id","roadmap_revision","objective","phase","work_package"],f"{label}.roadmap_source")
    e+=require(ep.get("scope") or {},["allowed","prohibited"],f"{label}.scope")
    if not ep.get("repository_discovery"):e.append(f"{label}.repository_discovery must contain at least one concrete step")
    if not ep.get("acceptance"):e.append(f"{label}.acceptance must contain at least one criterion")
    suc=ep.get("successor_relay") or {}
    if suc.get("required") is not True:e.append(f"{label}.successor_relay.required must be true")
    duties=suc.get("duties") or []
    for expected in ("compute next executable frontier","run cold-start check","update REPO_STATE"):
        if not any(expected.lower() in str(d).lower() for d in duties):e.append(f"{label}.successor_relay missing duty: {expected}")
    for step in ep.get("repository_discovery",[]) or []:
        targets=([step["target"]] if step.get("target") else [])+(step.get("targets",[]) or [])
        for target in targets:
            if isinstance(target,str) and target.startswith("agents/relay/") and not any(c in target for c in "*?[") and not (root/target).exists():e.append(f"{label} discovery target does not exist: {target}")
    return e,w

def validate(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/s["active_ep"]["path"]);return validate_ep_data(root,ep)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
