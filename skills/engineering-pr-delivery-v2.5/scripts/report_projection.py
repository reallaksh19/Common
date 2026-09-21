from __future__ import annotations
from pathlib import Path
from relaylib import load_yaml
from progress_projection import snapshot as progress_snapshot
from takeoverlib import digest_mapping,yaml_digest
from delivery_projection import snapshot as delivery_snapshot


def _maybe(root:Path,path):
    if not path:return None
    p=root/str(path)
    return load_yaml(p) if p.exists() else None


def _owner_decisions(root:Path)->list[dict]:
    base=root/"agents/relay/roadmap/owner-decisions"
    if not base.exists():return []
    out=[]
    for path in sorted(list(base.glob("*.yaml"))+list(base.glob("*.yml"))):
        try:odr=load_yaml(path)
        except Exception:continue
        decision=odr.get("decision") or {};effects=odr.get("effects") or {}
        out.append({
            "id":odr.get("id"),"path":str(path.relative_to(root)),"status":odr.get("status"),
            "kind":decision.get("kind"),"statement":decision.get("statement"),"source":decision.get("source"),
            "requirement_disposition":effects.get("requirement_disposition"),
            "grants_material_write_authority":effects.get("grants_material_write_authority"),
            "pending_items":effects.get("pending_items") or [],
            "delivery_authorization":odr.get("delivery_authorization"),
            "execution_override":odr.get("execution_override"),
        })
    return out


def _active_contract(ep:dict|None)->dict|None:
    if not ep:return None
    context=ep.get("context_capsule") or {}
    return {
        "outcome":ep.get("outcome") or {},
        "scope":ep.get("scope") or {},
        "known_problems":context.get("known_problems") or [],
        "deliberate_non_goals":context.get("deliberate_non_goals") or [],
        "quality_router":ep.get("quality") or {},
        "status_publication":((ep.get("report_contract") or {}).get("status_publication") or {"default_after_minutes":25,"owner_override":None}),
    }


def _issue_id(node:dict)->str|None:
    value=node.get("id",node.get("issue"))
    return str(value) if value not in {None,""} else None


def _current_issues(issue_graph:dict,work_package)->list[dict]:
    out=[]
    for node in issue_graph.get("nodes",[]) or []:
        if not isinstance(node,dict) or str(node.get("roadmap_node"))!=str(work_package):continue
        github=node.get("github") or {}
        out.append({
            "id":_issue_id(node),
            "engineering_state":node.get("state"),
            "github_state":node.get("github_state"),
            "issue_number":github.get("issue_number"),
            "issue_id":github.get("issue_id"),
            "url":github.get("url"),
        })
    return sorted(out,key=lambda x:str(x.get("id")))


def build(root:Path)->dict:
    state_path=root/"agents/relay/REPO_STATE.yaml";state=load_yaml(state_path)
    roadmap_path=root/state["roadmap"]["path"];roadmap=load_yaml(roadmap_path);progress_path=root/"agents/relay/roadmap/PROGRESS.yaml";issue_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml"
    active=state.get("active_ep") or {};ep=_maybe(root,active.get("path"));cp=_maybe(root,(state.get("last_checkpoint") or {}).get("path"));issues=load_yaml(issue_path) if issue_path.exists() else {"nodes":[],"relationships":[]}
    qptr=(cp or {}).get("quality_review") or {};qpath=qptr.get("path");qrv=_maybe(root,qpath)
    dptr=((state.get("delivery") or {}).get("observation") or {});dpath=dptr.get("path")
    owner_decisions=_owner_decisions(root);current_position=state.get("current_position") or {}
    projection={
        "schema_version":"relay-v2.5-report-projection",
        "generated_from":{
            "roadmap_revision":(state.get("roadmap") or {}).get("revision"),
            "progress_basis":(load_yaml(progress_path).get("progress_basis") or {}).get("id"),
            "repo_state_digest":yaml_digest(state_path),
            "roadmap_digest":yaml_digest(roadmap_path),
            "progress_digest":yaml_digest(progress_path),
            "issue_graph_digest":yaml_digest(issue_path) if issue_path.exists() else None,
            "owner_decisions_digest":digest_mapping(owner_decisions),
            "ep_id":active.get("id"),
            "ep_digest":yaml_digest(root/active["path"]) if active.get("path") and (root/active["path"]).exists() else None,
            "checkpoint_id":(state.get("last_checkpoint") or {}).get("id"),
            "checkpoint_digest":yaml_digest(root/(state.get("last_checkpoint") or {})["path"]) if (state.get("last_checkpoint") or {}).get("path") and (root/(state.get("last_checkpoint") or {})["path"]).exists() else None,
            "quality_review_id":qptr.get("id"),
            "quality_review_digest":yaml_digest(root/qpath) if qpath and (root/qpath).exists() else None,
            "delivery_observation_id":dptr.get("id"),
            "delivery_observation_digest":yaml_digest(root/dpath) if dpath and (root/dpath).exists() else None,
        },
        "roadmap_summary":{"id":(roadmap.get("roadmap") or {}).get("id"),"revision":(roadmap.get("roadmap") or {}).get("revision"),"title":(roadmap.get("roadmap") or {}).get("title")},
        "relay_state":state.get("relay_state"),
        "current_position":current_position,
        "current_work":{
            "objective":current_position.get("objective"),
            "phase":current_position.get("phase"),
            "work_package":current_position.get("work_package"),
            "ep_id":active.get("id"),
            "outcome":(ep.get("outcome") if ep else {}) or {},
            "issues":_current_issues(issues,current_position.get("work_package")),
        },
        "progress":progress_snapshot(root),
        "execution":(state.get("status_planes") or {}).get("execution") or {},
        "quality":(state.get("status_planes") or {}).get("quality") or {},
        "evidence":(state.get("status_planes") or {}).get("evidence") or {},
        "stop":(state.get("status_planes") or {}).get("stop") or {},
        "projection":state.get("projection") or {},
        "relay_readiness":state.get("relay_readiness") or {},
        "takeover_admissions":state.get("takeover_admissions") or [],
        "execution_custody":state.get("execution_custody") or {"enforced":False,"leases":[]},
        "control_obligations":state.get("control_obligations") or [],
        "active_contract":_active_contract(ep),
        "owner_decisions":owner_decisions,
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
            projection["parallel_lanes"].append({"lane_id":lane.get("id"),"work_package":lane.get("work_package"),"ep_id":lane.get("ep_id"),"branch":lane.get("branch"),"next_work":lep.get("next_work") or {},"contract":_active_contract(lep)})
    if cp:
        projection["checkpoint"]={
            "id":cp.get("checkpoint_id"),"implementation_result":cp.get("implementation_result") or {},
            "acceptance_results":cp.get("acceptance_results") or [],"validation_results":cp.get("validation_results") or [],
            "quality_review":({"id":qrv.get("quality_review_id"),"overall_state":qrv.get("overall_state"),"execution_effect":qrv.get("execution_effect") or {},"procedure_results":qrv.get("procedure_results") or [],"findings":qrv.get("findings") or [],"owner_report":qrv.get("owner_report") or {},"successor_handover":qrv.get("successor_handover") or {}} if qrv else None),
            "quality_findings":cp.get("quality_findings") or [],"known_limitations":cp.get("known_limitations") or [],
            "remaining_work":cp.get("remaining_work") or [],"roadmap_reconciliation":cp.get("roadmap_reconciliation") or {},
        }
    else:projection["checkpoint"]=None
    projection["delivery"]=delivery_snapshot(root,projection)
    return projection
