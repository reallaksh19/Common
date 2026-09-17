#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Iterable
try:
    import yaml
except Exception:
    print("PyYAML is required for engineering-pr-delivery-v2.5 validators.", file=sys.stderr)
    raise SystemExit(2)

VALID_NODE_STATES={"FUTURE","PLANNED","ACTIVE","COMPLETE","SUPERSEDED","CANCELLED"}
VALID_DEFINITIONS={"DETAILED","DEFINED","PARTIALLY_DEFINED","DISCOVERY_REQUIRED","OWNER_REVIEW_REQUIRED"}
VALID_EXECUTION_STATUS={"WAITING","EXECUTABLE","ACTIVE","TERMINAL"}
CONTEXT_DEPENDENT_PHRASES=("as discussed","continue previous work","continue the previous work","use the earlier decision","same approach as before","follow the existing approach","follow the recent implementation","run relevant tests","run the relevant tests","fix remaining issues","review recent work")

def load_yaml(path: Path)->dict[str,Any]:
    if not path.exists(): raise FileNotFoundError(str(path))
    data=yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data,dict): raise ValueError(f"{path}: expected YAML mapping at document root")
    return data

def require(data:dict[str,Any],keys:Iterable[str],where:str)->list[str]:
    return [f"{where}: missing required key '{k}'" for k in keys if k not in data]

def iter_work_packages(roadmap:dict[str,Any]):
    for objective in roadmap.get("objectives",[]) or []:
        for phase in objective.get("phases",[]) or []:
            for wp in phase.get("work_packages",[]) or []:
                yield objective,phase,wp

def index_roadmap(roadmap:dict[str,Any]):
    objectives,phases,wps={},{},{}
    for objective in roadmap.get("objectives",[]) or []:
        objectives[objective.get("id")]=objective
        for phase in objective.get("phases",[]) or []:
            phases[phase.get("id")]=(objective,phase)
            for wp in phase.get("work_packages",[]) or []:
                wps[wp.get("id")]=(objective,phase,wp)
    return objectives,phases,wps

def compute_frontier(roadmap:dict[str,Any])->list[str]:
    """Derive eligibility from roadmap topology; execution_status is a projection, not authority."""
    _,_,idx=index_roadmap(roadmap);out=[]
    for _,_,wp in iter_work_packages(roadmap):
        if wp.get("state") not in {"PLANNED","ACTIVE"}:continue
        if wp.get("definition")!="DETAILED":continue
        if wp.get("execution_status")=="TERMINAL":continue
        deps=wp.get("depends_on",[]) or []
        if any(dep not in idx or idx[dep][2].get("state")!="COMPLETE" for dep in deps):continue
        if wp.get("id"):out.append(wp["id"])
    return out

def pct(earned:float,total:float)->float:
    return 0.0 if total<=0 else round(earned*100.0/total,2)

def print_result(errors:list[str],warnings:list[str]|None=None)->int:
    for x in warnings or []:print(f"WARN: {x}")
    if errors:
        for x in errors:print(f"FAIL: {x}")
        return 1
    print("PASS");return 0

def scan_context_phrases(value:Any,location:str="$")->list[str]:
    found=[]
    if isinstance(value,dict):
        for k,v in value.items():found.extend(scan_context_phrases(v,f"{location}.{k}"))
    elif isinstance(value,list):
        for i,v in enumerate(value):found.extend(scan_context_phrases(v,f"{location}[{i}]"))
    elif isinstance(value,str):
        low=value.lower()
        for phrase in CONTEXT_DEPENDENT_PHRASES:
            if phrase in low:found.append(f"{location}: context-dependent phrase '{phrase}'")
    return found
