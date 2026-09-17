from __future__ import annotations
from pathlib import Path
from relaylib import load_yaml

BLUEPRINTS=("software-design","coding","ui-ux","testing","engineering-numerics","code-review","accessibility","performance","migration","github-delivery")
QUALITY_STATES={"CLEAR","NEEDS_ATTENTION","OWNER_REVIEW_REQUIRED"}
FINDING_CLASSES={"MAINTAINABILITY","DESIGN","UX","ACCESSIBILITY","PERFORMANCE","MIGRATION","NUMERICAL_RISK","TEST_GAP","DELIVERY_RISK","SAFETY","AUTHORITY","OTHER"}
SEVERITIES={"INFO","LOW","MEDIUM","HIGH","CRITICAL"}
DISPOSITIONS={"REMEDIATED","ACCEPTED_CURRENT_SLICE","DEFERRED","OWNER_REVIEW_REQUIRED","UNRESOLVED"}
PROCEDURE_RESULTS={"CLEAR","FINDINGS","NOT_RUN"}
HARD_STOPS={"OWNER_DECISION_REQUIRED","ESSENTIAL_INPUT_MISSING","AUTHORITY_VIOLATION","PROTECTED_INVARIANT_FAILURE","WRITE_COLLISION","SUPERSEDED_EP","ROADMAP_CONFLICT","REPOSITORY_STATE_CONFLICT","UNSAFE_ENGINEERING_RESULT"}
STOP_TRIGGERS={"AUTHORITY","ESSENTIAL_INPUT","PROTECTED_INVARIANT","UNSAFE_ENGINEERING_RESULT"}

def text(v):return isinstance(v,str) and bool(v.strip()) and not (v.strip().startswith("<") and v.strip().endswith(">"))
def items(v):return v if isinstance(v,list) else []
def ep_index(root:Path):
    out={}
    base=root/"agents/relay/execution-packages"
    if base.exists():
        for p in base.rglob("*.yaml"):
            try:
                ep=load_yaml(p);eid=str((ep.get("identity") or {}).get("ep_id") or "")
                if eid:out[eid]=(p,ep)
            except Exception:pass
    return out

def current_eps(root:Path,state:dict):
    if state.get("relay_state")=="ACTIVE":
        p=(state.get("active_ep") or {}).get("path")
        return [(str((state.get("active_ep") or {}).get("id") or "ACTIVE"),root/p)] if p else []
    if state.get("relay_state")=="PARALLEL":
        ref=(state.get("execution_policy") or {}).get("parallel_plan")
        if not ref:return []
        plan=load_yaml(root/ref);return [(str(x.get("ep_id") or x.get("id") or "lane"),root/x["ep_path"]) for x in items(plan.get("lanes")) if x.get("ep_path")]
    return []

def router_snapshot(ep:dict):
    q=ep.get("quality") or {}
    def norm(xs):return sorted([{"blueprint":str(x.get("blueprint")),"reason":str(x.get("reason")),"review_focus":list(x.get("review_focus") or [])} for x in items(xs) if isinstance(x,dict)],key=lambda x:x["blueprint"])
    return {"applicable":norm(q.get("applicable")),"not_applicable":norm(q.get("not_applicable"))}
