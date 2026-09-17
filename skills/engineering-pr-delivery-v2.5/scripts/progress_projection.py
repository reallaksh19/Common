from __future__ import annotations
from pathlib import Path
from typing import Any
from relaylib import load_yaml

GROUPS=("objectives","phases","work_packages","execution_packages","implementation_steps","acceptance_criteria")

def _idx(items:Any)->dict[str,dict]:
    return {str(x.get("id")):x for x in (items or []) if isinstance(x,dict) and x.get("id")}

def _pct(item:dict|None):
    if not item:return None
    value=item.get("percent")
    return float(value) if isinstance(value,(int,float)) else None

def snapshot(root:Path)->dict:
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    roadmap=load_yaml(root/state["roadmap"]["path"])
    progress=load_yaml(root/"agents/relay/roadmap/PROGRESS.yaml")
    current=state.get("current_position") or {}
    idx={g:_idx(progress.get(g)) for g in GROUPS}
    active=state.get("active_ep") or {};ep=None
    if state.get("relay_state")=="ACTIVE" and active.get("path"):
        ep=load_yaml(root/active["path"])
    hierarchy=[]
    for obj in roadmap.get("objectives",[]) or []:
        op=idx["objectives"].get(str(obj.get("id")))
        o={"id":obj.get("id"),"title":obj.get("title"),"state":obj.get("state"),"percent":_pct(op),"phases":[]}
        for ph in obj.get("phases",[]) or []:
            pp=idx["phases"].get(str(ph.get("id")))
            p={"id":ph.get("id"),"title":ph.get("title"),"state":ph.get("state"),"percent":_pct(pp),"work_packages":[]}
            for wp in ph.get("work_packages",[]) or []:
                wppr=idx["work_packages"].get(str(wp.get("id")))
                w={"id":wp.get("id"),"title":wp.get("title"),"state":wp.get("state"),"percent":_pct(wppr),"current":str(wp.get("id"))==str(current.get("work_package")),"steps":[]}
                if ep is not None and str((ep.get("roadmap_source") or {}).get("work_package"))==str(wp.get("id")):
                    for step in ep.get("implementation_plan",[]) or []:
                        sp=idx["implementation_steps"].get(str(step.get("id")))
                        row={"id":step.get("id"),"objective":step.get("objective"),"percent":_pct(sp),"acceptance":[]}
                        for aid in step.get("acceptance",[]) or []:
                            ap=idx["acceptance_criteria"].get(str(aid))
                            ac=next((x for x in ep.get("acceptance",[]) or [] if str(x.get("id"))==str(aid)),{})
                            row["acceptance"].append({"id":aid,"description":ac.get("description"),"status":(ap or {}).get("status","UNKNOWN"),"percent":_pct(ap),"basis":(ap or {}).get("basis",[])})
                        w["steps"].append(row)
                p["work_packages"].append(w)
            o["phases"].append(p)
        hierarchy.append(o)
    ep_row=idx["execution_packages"].get(str(active.get("id"))) if active.get("id") else None
    phase_row=idx["phases"].get(str(current.get("phase")))
    wp_row=idx["work_packages"].get(str(current.get("work_package")))
    return {
        "progress_basis":progress.get("progress_basis") or {},
        "overall_percent":_pct(progress.get("overall") or {}),
        "current":{"objective":current.get("objective"),"phase":current.get("phase"),"work_package":current.get("work_package"),"ep_id":active.get("id"),"phase_percent":_pct(phase_row),"work_package_percent":_pct(wp_row),"ep_percent":_pct(ep_row)},
        "hierarchy":hierarchy,
    }
