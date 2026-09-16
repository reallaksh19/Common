from __future__ import annotations
from pathlib import Path
from relaylib import load_yaml
from progress_projection import snapshot as progress_snapshot
from takeoverlib import yaml_digest

def _maybe(root:Path,path):
    if not path:return None
    p=root/str(path)
    return load_yaml(p) if p.exists() else None

def build(root:Path)->dict:
    state_path=root/"agents/relay/REPO_STATE.yaml";state=load_yaml(state_path)
    roadmap_path=root/state["roadmap"]["path"];progress_path=root/"agents/relay/roadmap/PROGRESS.yaml";issue_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml"
    active=state.get("active_ep") or {};ep=_maybe(root,active.get("path"));cp=_maybe(root,(state.get("last_checkpoint") or {}).get("path"));issues=load_yaml(issue_path) if issue_path.exists() else {"nodes":[],"relationships":[]}
    projection={
        "schema_version":"relay-v2.5-report-projection",
        "generated_from":{
            "roadmap_revision":(state.get("roadmap") or {}).get("revision"),
            "progress_basis":(load_yaml(progress_path).get("progress_basis") or {}).get("id"),
            "repo_state_digest":yaml_digest(state_path),
            "roadmap_digest":yaml_digest(roadmap_path),
            "progress_digest":yaml_digest(progress_path),
            "issue_graph_digest":yaml_digest(issue_path) if issue_path.exists() else None,
            "ep_id":active.get("id"),
            "ep_digest":yaml_digest(root/active["path"]) if active.get("path") and (root/active["path"]).exists() else None,
            "checkpoint_id":(state.get("last_checkpoint") or {}).get("id"),
            "checkpoint_digest":yaml_digest(root/(state.get("last_checkpoint") or {})["path"]) if (state.get("last_checkpoint") or {}).get("path") and (root/(state.get("last_checkpoint") or {})["path"]).exists() else None,
        },
        "relay_state":state.get("relay_state"),
        "current_position":state.get("current_position") or {},
        "progress":progress_snapshot(root),
        "execution":(state.get("status_planes") or {}).get("execution") or {},
        "quality":(state.get("status_planes") or {}).get("quality") or {},
        "evidence":(state.get("status_planes") or {}).get("evidence") or {},
        "stop":(state.get("status_planes") or {}).get("stop") or {},
        "projection":state.get("projection") or {},
        "relay_readiness":state.get("relay_readiness") or {},
        "takeover_admissions":state.get("takeover_admissions") or [],
        "next_work":(ep.get("next_work") if ep else None),
        "acceptance":[],
        "parallel_lanes":[],
        "issue_summary":{"nodes":len(issues.get("nodes",[]) or []),"relationships":len(issues.get("relationships",[]) or [])},
    }
    for obj in projection["progress"].get("hierarchy",[]):
        for ph in obj.get("phases",[]):
            for wp in ph.get("work_packages",[]):
                if wp.get("current"):
                    for step in wp.get("steps",[]):projection["acceptance"].extend(step.get("acceptance",[]))
    if state.get("relay_state")=="PARALLEL":
        plan_path=(state.get("execution_policy") or {}).get("parallel_plan");plan=_maybe(root,plan_path)
        for lane in (plan or {}).get("lanes",[]) or []:
            lep=_maybe(root,lane.get("ep_path")) or {}
            projection["parallel_lanes"].append({"lane_id":lane.get("id"),"work_package":lane.get("work_package"),"ep_id":lane.get("ep_id"),"branch":lane.get("branch"),"next_work":lep.get("next_work") or {}})
    if cp:
        projection["checkpoint"]={"id":cp.get("checkpoint_id"),"implementation_result":cp.get("implementation_result") or {},"acceptance_results":cp.get("acceptance_results") or [],"validation_results":cp.get("validation_results") or [],"quality_findings":cp.get("quality_findings") or []}
    else:projection["checkpoint"]=None
    return projection
