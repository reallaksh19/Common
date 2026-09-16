from __future__ import annotations
import hashlib,json
from pathlib import Path
from typing import Any
from relaylib import load_yaml

NONE_IDS={None,"","NONE"}


def digest_mapping(value:Any)->str:
    payload=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,default=str).encode("utf-8")
    return "sha256:"+hashlib.sha256(payload).hexdigest()


def yaml_digest(path:Path)->str:
    return digest_mapping(load_yaml(path))


def predecessor_baton(state:dict[str,Any])->dict[str,Any]:
    join=state.get("predecessor_join") or {}
    if join.get("id") not in NONE_IDS:
        return {"type":"JOIN","id":join.get("id"),"path":join.get("path")}
    replan=state.get("predecessor_replan") or {}
    if replan.get("id") not in NONE_IDS:
        return {"type":"REPLAN","id":replan.get("id"),"path":replan.get("path")}
    cp=state.get("last_checkpoint") or {}
    if cp.get("id") not in NONE_IDS:
        return {"type":"CHECKPOINT","id":cp.get("id"),"path":cp.get("path")}
    return {"type":"NONE","id":"NONE","path":None}


def route_key(route:dict[str,Any])->str:
    mode=route.get("mode")
    if mode=="SERIAL":return f"SERIAL:{route.get('ep_id')}"
    if mode=="PARALLEL_LANE":return f"PARALLEL_LANE:{route.get('plan_id')}:{route.get('lane_id')}:{route.get('ep_id')}"
    return f"{mode}:{route.get('ep_id')}"


def current_routes(root:Path,state:dict[str,Any]|None=None)->list[dict[str,Any]]:
    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml")
    relay_state=state.get("relay_state")
    if relay_state=="ACTIVE":
        active=state.get("active_ep") or {};path=active.get("path")
        if not path:return []
        ep=load_yaml(root/path);ident=ep.get("identity") or {};basis=ep.get("git_basis") or {}
        return [{
            "mode":"SERIAL","execution_ref":ident.get("ep_id"),"ep_id":ident.get("ep_id"),"ep_path":path,
            "plan_id":None,"plan_path":None,"lane_id":None,"branch":ident.get("branch"),"worktree":None,
            "material_ref":basis.get("material_ref"),
        }]
    if relay_state=="PARALLEL":
        plan_path=(state.get("execution_policy") or {}).get("parallel_plan")
        if not plan_path:return []
        plan=load_yaml(root/plan_path);out=[]
        for lane in plan.get("lanes",[]) or []:
            ep_path=lane.get("ep_path")
            if not ep_path:continue
            ep=load_yaml(root/ep_path);ident=ep.get("identity") or {};basis=ep.get("git_basis") or {}
            out.append({
                "mode":"PARALLEL_LANE","execution_ref":plan.get("id"),"ep_id":ident.get("ep_id"),"ep_path":ep_path,
                "plan_id":plan.get("id"),"plan_path":plan_path,"lane_id":lane.get("id"),"branch":lane.get("branch"),
                "worktree":lane.get("worktree"),"material_ref":basis.get("material_ref"),
            })
        return out
    return []


def expected_basis(root:Path,state:dict[str,Any],route:dict[str,Any])->dict[str,Any]:
    roadmap=state.get("roadmap") or {};protocol=state.get("relay_protocol") or {}
    baton=predecessor_baton(state)
    if baton.get("path"):
        path=root/str(baton["path"])
        baton={**baton,"digest":yaml_digest(path) if path.exists() else None}
    else:baton={**baton,"digest":None}
    ep_path=root/str(route.get("ep_path"));profile_path=root/"agents/relay/REPO_PROFILE.yaml"
    return {
        "roadmap_id":roadmap.get("id"),"roadmap_revision":roadmap.get("revision"),
        "relay_protocol_basis_ref":protocol.get("basis_ref"),"route_key":route_key(route),
        "execution_ref":route.get("execution_ref"),"ep_id":route.get("ep_id"),"ep_path":route.get("ep_path"),
        "plan_id":route.get("plan_id"),"plan_path":route.get("plan_path"),"lane_id":route.get("lane_id"),
        "material_ref":route.get("material_ref"),
        "ep_contract_digest":yaml_digest(ep_path) if ep_path.exists() else None,
        "repo_profile_digest":yaml_digest(profile_path) if profile_path.exists() else None,
        "predecessor_baton":baton,
    }


def find_route(root:Path,state:dict[str,Any],route_key_value:str)->dict[str,Any]|None:
    for route in current_routes(root,state):
        if route_key(route)==route_key_value:return route
    return None


def find_admission(state:dict[str,Any],route_key_value:str,candidate_id:str|None=None)->dict[str,Any]|None:
    matches=[]
    for item in state.get("takeover_admissions",[]) or []:
        if not isinstance(item,dict):continue
        if str(item.get("route_key"))!=str(route_key_value):continue
        cid=str((item.get("candidate") or {}).get("agent_instance_id") or "")
        if candidate_id is not None and cid!=str(candidate_id):continue
        matches.append(item)
    return matches[0] if len(matches)==1 else None


def required_discovery_steps(ep:dict[str,Any])->list[str]:
    return [str(x.get("id")) for x in ep.get("repository_discovery",[]) or [] if isinstance(x,dict) and x.get("receipt_required") is True and x.get("id")]
