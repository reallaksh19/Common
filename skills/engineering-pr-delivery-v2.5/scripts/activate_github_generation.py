#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,json
from pathlib import Path
import yaml
from relaylib import load_yaml
from validate_projection_convergence import expected_execution_ref

def _dump(path:Path,data:dict):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")
def _has_attempt(plan:dict)->bool:return any((x.get("publication") or {}).get("attempt_count",0)>0 for x in (plan.get("operations") or []))
def _has_receipt(plan:dict)->bool:return any((x.get("publication") or {}).get("receipt") not in {None,""} for x in (plan.get("operations") or []))

def activate(root:Path,new_plan_rel:str,apply:bool=False)->dict:
    state_path=root/"agents/relay/REPO_STATE.yaml";state=load_yaml(state_path);new_path=root/new_plan_rel
    if not new_path.exists():return {"status":"ERROR","errors":[f"new generation missing: {new_plan_rel}"]}
    new=load_yaml(new_path);gen=new.get("generation") or {};gid=str(gen.get("id") or "")
    errors=[]
    if new.get("schema_version")!="relay-v2.5-github-projection":errors.append("new generation schema_version invalid")
    if not gid.startswith("GHGEN-"):errors.append("new generation id must use GHGEN-* namespace")
    if gen.get("state")!="PREPARED":errors.append("new generation must begin PREPARED")
    if str(gen.get("roadmap_revision") or "")!=str((state.get("roadmap") or {}).get("revision") or ""):errors.append("new generation roadmap_revision must equal current roadmap")
    if str(gen.get("execution_ref") or "")!=expected_execution_ref(root,state):errors.append("new generation execution_ref must equal current execution route")
    if errors:return {"status":"ERROR","errors":errors}
    state=copy.deepcopy(state);new=copy.deepcopy(new);projection=state.setdefault("projection",{});old_rel=projection.get("plan");old=None;old_path=None
    if old_rel and str(old_rel)!=new_plan_rel:
        old_path=root/str(old_rel);old=copy.deepcopy(load_yaml(old_path));old_gen=old.get("generation") or {};old_id=str(old_gen.get("id") or "")
        if old_id==gid:return {"status":"ERROR","errors":["new generation id reuses current generation id"]}
        new["generation"]["supersedes_generation"]=old_id
        old_was_sync=old_gen.get("state")=="IN_SYNC" and projection.get("state")=="IN_SYNC"
        old_gen["state"]="SUPERSEDED"
        for op in old.get("operations",[]) or []:
            if op.get("state") not in {"VERIFIED","FAILED","SUPERSEDED"}:
                op["state"]="SUPERSEDED";op["superseded_by"]=gid
        if old_was_sync:
            projection["observed"]={"operation_id":old_id,"target":projection.get("target"),"roadmap_revision":old_gen.get("roadmap_revision"),"execution_ref":old_gen.get("execution_ref"),"receipt":projection.get("receipt") or f"github-generation:{old_id}","basis":list(projection.get("basis") or [f"generation:{old_id}"])}
        else:
            if _has_receipt(old):disposition="SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED"
            elif _has_attempt(old):disposition="SUPERSEDED_AFTER_ATTEMPT_UNCONFIRMED"
            else:disposition="SUPERSEDED_BEFORE_PUBLICATION"
            receipt=projection.get("receipt") if disposition=="SUPERSEDED_AFTER_PUBLICATION_UNCONFIRMED" else None
            history=projection.setdefault("superseded_operations",[])
            history.append({"operation_id":old_id,"target":projection.get("target"),"roadmap_revision":old_gen.get("roadmap_revision"),"execution_ref":old_gen.get("execution_ref"),"disposition":disposition,"superseded_by":gid,"receipt":receipt,"basis":[f"generation:{old_id}",f"superseded_by:{gid}"]})
    projection.update({"required":True,"operation_id":gid,"target":f"github:{gen.get('repository')}:issues","adapter":"GITHUB_ISSUES","plan":new_plan_rel,"roadmap_revision":gen.get("roadmap_revision"),"execution_ref":gen.get("execution_ref"),"receipt":None,"basis":list(gen.get("basis") or [])})
    projection["state"]="STALE" if projection.get("observed") else "PENDING"
    state.setdefault("relay_readiness",{})["projection_ready"]=False;state["relay_readiness"]["handover_ready"]=False
    if apply:
        if old is not None and old_path is not None:_dump(old_path,old)
        _dump(new_path,new);_dump(state_path,state)
    return {"status":"OK","generation_id":gid,"projection_state":projection["state"],"supersedes_generation":new["generation"].get("supersedes_generation"),"applied":apply}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("new_generation_path");ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--apply",action="store_true");a=ap.parse_args();print(json.dumps(activate(Path(a.repo_root).resolve(),a.new_generation_path,a.apply),indent=2,sort_keys=True))
if __name__=="__main__":main()
