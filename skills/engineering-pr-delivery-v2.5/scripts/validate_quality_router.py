#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from qualitylib import BLUEPRINTS,current_eps,items,text

REQ_OUTPUTS={"procedure_results","findings","owner_report","successor_handover"}

def validate_ep(ep:dict,label:str):
    e=[];w=[];q=ep.get("quality")
    if not isinstance(q,dict):return [f"{label}.quality must be a mapping"],w
    for key in ("applicable","not_applicable","review_contract","findings_policy"):
        if key not in q:e.append(f"{label}.quality missing {key}")
    seen={};app_names=[];na_names=[]
    for bucket,names in (("applicable",app_names),("not_applicable",na_names)):
        vals=q.get(bucket)
        if not isinstance(vals,list):e.append(f"{label}.quality.{bucket} must be a list");continue
        for i,item in enumerate(vals):
            il=f"{label}.quality.{bucket}[{i}]"
            if not isinstance(item,dict):e.append(f"{il} must be a mapping");continue
            name=item.get("blueprint")
            if name not in BLUEPRINTS:e.append(f"{il}.blueprint unknown: {name}")
            if name in seen:e.append(f"{label}.quality blueprint {name} appears more than once")
            seen[name]=bucket;names.append(name)
            if not text(item.get("reason")):e.append(f"{il}.reason must explain applicability")
            focus=item.get("review_focus")
            if not isinstance(focus,list) or not focus or not all(text(x) for x in focus):e.append(f"{il}.review_focus must contain explicit review concerns")
    missing=set(BLUEPRINTS)-set(seen)
    if missing:e.append(f"{label}.quality router must classify every built-in blueprint; missing {sorted(missing)}")
    extra=set(seen)-set(BLUEPRINTS)
    if extra:e.append(f"{label}.quality router contains unsupported blueprints {sorted(extra)}")
    rc=q.get("review_contract") or {}
    if rc.get("required") is not True:e.append(f"{label}.quality.review_contract.required must be true")
    if rc.get("required_before_checkpoint") is not True:e.append(f"{label}.quality.review_contract.required_before_checkpoint must be true")
    if rc.get("receipt_namespace")!="QRV-":e.append(f"{label}.quality.review_contract.receipt_namespace must be QRV-")
    outputs=rc.get("required_outputs")
    if not isinstance(outputs,list) or set(outputs)!=REQ_OUTPUTS:e.append(f"{label}.quality.review_contract.required_outputs must equal {sorted(REQ_OUTPUTS)}")
    if not text(q.get("findings_policy")):e.append(f"{label}.quality.findings_policy must be explicit")
    if q.get("ordinary_findings_are_hard_stops") is not False:e.append(f"{label}.quality.ordinary_findings_are_hard_stops must be false")
    return e,w

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    for eid,path in current_eps(root,state):
        if not path.exists():e.append(f"quality route EP missing: {path}");continue
        ce,cw=validate_ep(load_yaml(path),f"EP {eid}");e.extend(ce);w.extend(cw)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
