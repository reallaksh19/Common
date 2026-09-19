from __future__ import annotations
from pathlib import Path
from report_projection import build as build_report
from takeoverlib import digest_mapping
from owner_publication import cursor_digest,publication_status


def _current_titles(progress:dict)->dict:
    cur=progress.get("current") or {};out={"objective":cur.get("objective"),"phase":cur.get("phase"),"work_package":cur.get("work_package"),"ep_id":cur.get("ep_id")}
    for obj in progress.get("hierarchy",[]) or []:
        if str(obj.get("id"))==str(cur.get("objective")):out["objective_title"]=obj.get("title")
        for ph in obj.get("phases",[]) or []:
            if str(ph.get("id"))==str(cur.get("phase")):out["phase_title"]=ph.get("title")
            for wp in ph.get("work_packages",[]) or []:
                if str(wp.get("id"))==str(cur.get("work_package")):out["work_package_title"]=wp.get("title")
    out.update({"overall_percent":progress.get("overall_percent"),"phase_percent":cur.get("phase_percent"),"work_package_percent":cur.get("work_package_percent"),"ep_percent":cur.get("ep_percent")})
    return out


def _exact_next_work(report:dict)->list[dict]:
    nw=report.get("next_work") or {}
    if isinstance(nw.get("steps"),list) and nw.get("steps"):
        return [{**step,"lane_id":None,"ep_id":(report.get("generated_from") or {}).get("ep_id")} for step in nw["steps"] if isinstance(step,dict)]
    out=[]
    for lane in report.get("parallel_lanes",[]) or []:
        for step in (lane.get("next_work") or {}).get("steps",[]) or []:
            if isinstance(step,dict):out.append({**step,"lane_id":lane.get("lane_id"),"ep_id":lane.get("ep_id")})
    return out


def _visible_quality(report:dict)->tuple[list[dict],list[dict]]:
    risks=[];gaps=[];checkpoint=report.get("checkpoint") or {};qrv=checkpoint.get("quality_review") or {}
    for finding in qrv.get("findings",[]) or []:
        if not isinstance(finding,dict) or finding.get("disposition")=="REMEDIATED":continue
        risks.append({
            "statement":finding.get("statement"),"severity":finding.get("severity"),"classification":finding.get("classification"),
            "disposition":finding.get("disposition"),"blocks_execution":bool(finding.get("blocks_execution")),
        })
    for result in qrv.get("procedure_results",[]) or []:
        if isinstance(result,dict) and result.get("result")=="NOT_RUN":
            gaps.append({"procedure":result.get("blueprint"),"reason":result.get("reason"),"cause":result.get("cause")})
    for finding in (report.get("quality") or {}).get("findings",[]) or []:
        if isinstance(finding,dict):
            statement=finding.get("statement") or finding.get("summary") or finding.get("reason")
            item={"statement":statement,"severity":finding.get("severity"),"classification":finding.get("classification"),"disposition":finding.get("disposition"),"blocks_execution":bool(finding.get("blocks_execution"))}
        else:item={"statement":str(finding),"severity":None,"classification":None,"disposition":None,"blocks_execution":False}
        if item not in risks:risks.append(item)
    return risks,gaps


def _required_owner_decisions(report:dict)->list[dict]:
    out=[];stop=report.get("stop") or {}
    if stop.get("active") and stop.get("category")=="OWNER_DECISION_REQUIRED":
        out.append({"reason":stop.get("reason"),"basis":stop.get("basis") or [],"source":"current execution stop"})
    recon=((report.get("checkpoint") or {}).get("roadmap_reconciliation") or {})
    for item in recon.get("owner_decisions_required",[]) or []:
        if isinstance(item,dict):out.append({"reason":item.get("reason") or item.get("statement") or str(item),"basis":item.get("basis") or [],"source":"last checkpoint roadmap reconciliation"})
        else:out.append({"reason":str(item),"basis":[],"source":"last checkpoint roadmap reconciliation"})
    return out


def _capability(report:dict)->dict:
    ex=report.get("execution") or {};stop=report.get("stop") or {};relay=report.get("relay_state");authority=ex.get("material_authority")
    if stop.get("active"):
        summary=f"Engineering work is stopped until this issue is resolved: {stop.get('reason') or stop.get('category')}."
    elif relay in {"TERMINAL","IDLE"} or authority=="NONE":summary="No material engineering changes are currently authorized."
    elif ex.get("can_continue") and authority=="WRITE":summary="Engineering work may continue within the current authorized slice. A replacement agent must still pass the live takeover and Git checks before changing files."
    elif ex.get("can_continue") and authority=="READ_ONLY":summary="Inspection and reconciliation may continue, but material file changes are not currently authorized."
    elif authority=="READ_ONLY":summary="Only read-only investigation or reconciliation is currently allowed."
    else:summary="The current engineering slice is waiting and should not advance until its stated condition is resolved."
    return {"summary":summary,"can_continue":bool(ex.get("can_continue")),"material_authority":authority,"active_stop":stop if stop.get("active") else None}


def build(root:Path)->dict:
    report=build_report(root);contract=report.get("active_contract") or {};scope=contract.get("scope") or {};risks,quality_gaps=_visible_quality(report);evidence=report.get("evidence") or {};checkpoint=report.get("checkpoint") or {}
    recorded=[x for x in report.get("owner_decisions",[]) or [] if isinstance(x,dict) and x.get("status")!="SUPERSEDED"]
    next_steps=_exact_next_work(report)
    external_actions=[]
    for step in next_steps:
        req=step.get("execution_requirement")
        if isinstance(req,dict):
            external_actions.append({**req,"action":step.get("action"),"expected_result":step.get("expected_result"),"ep_id":step.get("ep_id"),"lane_id":step.get("lane_id")})
    titles=_current_titles(report.get("progress") or {});current_work=report.get("current_work") or {}
    change=publication_status(root,report)
    owner={
        "change":change,
        "capability":_capability(report),
        "current_work":{**titles,"issues":current_work.get("issues") or [],"outcome":current_work.get("outcome") or {}},
        "purpose":contract.get("outcome") or {},
        "scope":{"protected":scope.get("protected") or [],"prohibited":scope.get("prohibited") or [],"owner_reserved":scope.get("owner_reserved") or [],"deliberate_non_goals":contract.get("deliberate_non_goals") or []},
        "evidence":{"state":evidence.get("state"),"summary":evidence.get("summary"),"not_run":evidence.get("not_run") or [],"acceptance":report.get("acceptance") or []},
        "quality":{"state":(report.get("quality") or {}).get("state"),"visible_risks":risks,"procedure_gaps":quality_gaps,"known_limitations":checkpoint.get("known_limitations") or [],"known_problems":contract.get("known_problems") or []},
        "roadmap":{"summary":report.get("roadmap_summary") or {},"progress":_current_titles(report.get("progress") or {}),"last_reconciliation":checkpoint.get("roadmap_reconciliation") or {}},
        "delivery":report.get("delivery") or {},
        "decisions":{"required_now":_required_owner_decisions(report),"recorded":recorded,"reserved":scope.get("owner_reserved") or []},
        "next_work":{"steps":next_steps},
        "external_actions":external_actions,
        "stop_conditions":[condition for step in next_steps for condition in (step.get("stop_if") or [])],
    }
    return {
        "schema_version":"relay-v2.5-communication-projection",
        "generated_from":{"report_projection_digest":digest_mapping(report),"report_sources":report.get("generated_from") or {},"owner_publication_cursor_digest":cursor_digest(root)},
        "owner":owner,
        "technical":{"report":report},
    }
