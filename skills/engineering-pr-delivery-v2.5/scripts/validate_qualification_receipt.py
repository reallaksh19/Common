#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from relaylib import load_yaml,print_result,require
from takeoverlib import current_routes,route_key,yaml_digest
from validate_question_set import validate_file as validate_question_set

EVALUATORS={"INDEPENDENT_AGENT","OWNER","DETERMINISTIC_VALIDATOR"}
QUESTIONS=("Q1","Q2","Q3","Q4","Q5")


def _text(v:Any)->bool:return isinstance(v,str) and bool(v.strip()) and not (v.strip().startswith("<") and v.strip().endswith(">"))
def _basis(v:Any)->bool:return isinstance(v,list) and bool(v) and all(_text(x) for x in v)
def _route_fields(route:dict)->dict:
    return {"route_key":route_key(route),"mode":route.get("mode"),"execution_ref":route.get("execution_ref"),"ep_id":route.get("ep_id"),"ep_path":route.get("ep_path"),"plan_id":route.get("plan_id"),"plan_path":route.get("plan_path"),"lane_id":route.get("lane_id")}

def _find_route(root:Path,state:dict,rkey:str)->dict|None:
    for route in current_routes(root,state):
        if route_key(route)==rkey:return route
    return None

def _nonempty_output(value:Any)->bool:
    if value is None:return False
    if isinstance(value,str):return bool(value.strip())
    if isinstance(value,(list,dict,tuple,set)):return bool(value)
    return True

def validate_file(root:Path,path:Path,state:dict|None=None,expected_route:dict|None=None,expected_candidate:str|None=None):
    e=[];w=[]
    try:qual=load_yaml(path)
    except Exception as exc:return [f"QUALIFICATION_RECEIPT: {exc}"],w
    label=f"QUALIFICATION_RECEIPT {qual.get('id','?')}"
    e+=require(qual,["schema_version","id","candidate","question_set","route","answers","evaluated_by","evaluations","self_evaluation","result","conversation_context_used"],label)
    if qual.get("schema_version")!="relay-v2.5-qualification":e.append(f"{label}.schema_version must be relay-v2.5-qualification")
    if not str(qual.get("id") or "").startswith("QUAL-"):e.append(f"{label}.id must use QUAL-* namespace")
    candidate=str((qual.get("candidate") or {}).get("agent_instance_id") or "")
    if not _text(candidate):e.append(f"{label}.candidate.agent_instance_id must be explicit")
    if expected_candidate is not None and candidate!=str(expected_candidate):e.append(f"{label}.candidate does not match takeover candidate")
    if qual.get("conversation_context_used") is not False:e.append(f"{label}.conversation_context_used must be false")
    if (qual.get("self_evaluation") or {}).get("allowed") is not False:e.append(f"{label}.self_evaluation.allowed must be false")

    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml");rdata=qual.get("route") or {};rkey=str(rdata.get("route_key") or "")
    route=expected_route or _find_route(root,state,rkey)
    if route is None:return e+[f"{label}.route_key does not resolve to current execution route: {rkey}"],w
    for key,val in _route_fields(route).items():
        if str(rdata.get(key))!=str(val):e.append(f"{label}.route.{key} does not match current route")
    ep_path=root/str(route.get("ep_path"));ep=load_yaml(ep_path);src=ep.get("roadmap_source") or {}
    if str(rdata.get("roadmap_revision"))!=str(src.get("roadmap_revision")):e.append(f"{label}.route.roadmap_revision mismatch")
    if str(rdata.get("work_package"))!=str(src.get("work_package")):e.append(f"{label}.route.work_package mismatch")
    if str(rdata.get("ep_contract_digest"))!=str(yaml_digest(ep_path)):e.append(f"{label}.route.ep_contract_digest does not match current EP")

    qref=qual.get("question_set") or {};qpath=qref.get("path")
    if not str(qref.get("id") or "").startswith("QSET-"):e.append(f"{label}.question_set.id must use QSET-* namespace")
    if not _text(qpath):e.append(f"{label}.question_set.path must be explicit")
    elif not (root/str(qpath)).exists():e.append(f"{label}.question_set.path does not exist: {qpath}")
    else:
        qe,qw=validate_question_set(root,root/str(qpath),state,route);e.extend(qe);w.extend(qw)
        qset=load_yaml(root/str(qpath))
        if str(qset.get("id"))!=str(qref.get("id")):e.append(f"{label}.question_set.id does not match question set file")
        qb=ep.get("qualification_boundary") or {};ep_qref=qb.get("question_set") or {}
        if str(ep_qref.get("id"))!=str(qref.get("id")) or str(ep_qref.get("path"))!=str(qpath):e.append(f"{label}: question set does not match EP qualification boundary")
        preparer=str((qset.get("prepared_by") or {}).get("agent_instance_id") or "")
        if candidate and preparer==candidate:e.append(f"{label}: candidate cannot prepare its own qualification question set")

        questions={str(x.get("id")):x for x in qset.get("questions",[]) or [] if isinstance(x,dict) and x.get("id")}
        answers=qual.get("answers")
        if not isinstance(answers,list) or len(answers)!=5:e.append(f"{label}.answers must contain exactly Q1-Q5")
        else:
            seen=set()
            for i,ans in enumerate(answers):
                al=f"{label}.answers[{i}]"
                if not isinstance(ans,dict):e.append(f"{al} must be a mapping");continue
                qid=str(ans.get("id") or "")
                if qid not in QUESTIONS:e.append(f"{al}.id invalid: {qid}")
                if qid in seen:e.append(f"{label}.answers duplicate {qid}")
                seen.add(qid)
                if not _text(ans.get("response")):e.append(f"{al}.response must be explicit")
                outputs=ans.get("outputs")
                if not isinstance(outputs,dict):e.append(f"{al}.outputs must be a mapping");outputs={}
                q=questions.get(qid) or {};required=q.get("required_output_keys") or []
                for key in required:
                    if key not in outputs or not _nonempty_output(outputs.get(key)):e.append(f"{al}.outputs.{key} is required and must be non-empty")
                if q.get("evidence_required") is True and not _basis(ans.get("evidence")):e.append(f"{al}.evidence must contain durable basis")
            missing=[q for q in QUESTIONS if q not in seen]
            if missing:e.append(f"{label}.answers missing {missing}")
    evaluator=qual.get("evaluated_by") or {};etype=evaluator.get("type");eid=str(evaluator.get("identity") or "")
    if etype not in EVALUATORS:e.append(f"{label}.evaluated_by.type invalid: {etype}")
    if not _text(eid):e.append(f"{label}.evaluated_by.identity must be explicit")
    if not _basis(evaluator.get("basis")):e.append(f"{label}.evaluated_by.basis must contain durable independent basis")
    if etype=="INDEPENDENT_AGENT" and eid==candidate:e.append(f"{label}: independent evaluator cannot be the candidate")
    if etype=="DETERMINISTIC_VALIDATOR":
        if eid!="validate_qualification_receipt.py":e.append(f"{label}: deterministic evaluator identity must be validate_qualification_receipt.py")
        qset=load_yaml(root/str(qpath)) if _text(qpath) and (root/str(qpath)).exists() else {}
        expected={str(q.get("id")):q.get("deterministic_expected") for q in qset.get("questions",[]) or [] if isinstance(q,dict)}
        answers_by={str(a.get("id")):a.get("outputs") for a in qual.get("answers",[]) or [] if isinstance(a,dict)}
        for qid in QUESTIONS:
            if not isinstance(expected.get(qid),dict) or not expected.get(qid):e.append(f"{label}: deterministic evaluation requires {qid}.deterministic_expected in question set")
            elif answers_by.get(qid)!=expected.get(qid):e.append(f"{label}: deterministic answer mismatch for {qid}")

    evaluations=qual.get("evaluations")
    if not isinstance(evaluations,list) or len(evaluations)!=5:e.append(f"{label}.evaluations must contain exactly Q1-Q5")
    else:
        seen=set();all_pass=True
        for i,item in enumerate(evaluations):
            el=f"{label}.evaluations[{i}]"
            if not isinstance(item,dict):e.append(f"{el} must be a mapping");all_pass=False;continue
            qid=str(item.get("id") or "")
            if qid not in QUESTIONS:e.append(f"{el}.id invalid: {qid}")
            if qid in seen:e.append(f"{label}.evaluations duplicate {qid}")
            seen.add(qid)
            status=item.get("status")
            if status not in {"PASS","FAIL"}:e.append(f"{el}.status must be PASS or FAIL");all_pass=False
            elif status!="PASS":all_pass=False
            if not _basis(item.get("basis")):e.append(f"{el}.basis must contain durable evaluation basis")
        missing=[q for q in QUESTIONS if q not in seen]
        if missing:e.append(f"{label}.evaluations missing {missing}")
        result=qual.get("result")
        if result not in {"PASS","FAIL"}:e.append(f"{label}.result must be PASS or FAIL")
        if result=="PASS" and (not all_pass or missing):e.append(f"{label}.result PASS requires all five evaluations PASS")
    return e,w

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    for admission in state.get("takeover_admissions",[]) or []:
        if not isinstance(admission,dict):continue
        candidate=str((admission.get("candidate") or {}).get("agent_instance_id") or "")
        tcptr=admission.get("certification") or {};tcpath=tcptr.get("path")
        if not tcpath or not (root/str(tcpath)).exists():continue
        tc=load_yaml(root/str(tcpath));qual=tc.get("qualification") or {}
        if qual.get("required") is not True:continue
        qpath=qual.get("receipt_path")
        if not qpath:e.append(f"TC {tc.get('id')} requires qualification receipt path");continue
        route=_find_route(root,state,str(admission.get("route_key") or ""))
        if route is None:e.append(f"takeover admission route missing for qualification: {admission.get('route_key')}");continue
        qp=root/str(qpath)
        if not qp.exists():e.append(f"qualification receipt does not exist: {qpath}");continue
        ce,cw=validate_file(root,qp,state,route,candidate);e.extend(ce);w.extend(cw)
        receipt=load_yaml(qp)
        if str(receipt.get("id"))!=str(qual.get("receipt_id")):e.append(f"TC {tc.get('id')} qualification receipt_id mismatch")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
