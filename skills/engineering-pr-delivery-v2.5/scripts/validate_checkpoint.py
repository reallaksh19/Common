#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from relaylib import load_yaml,print_result,require

REQ=["schema_version","checkpoint_id","ep_id","roadmap_basis","execution_basis","implementation_result","acceptance_results","validation_results","quality_findings","discoveries","roadmap_reconciliation","successor"]
V2_REQUIRED=["known_limitations","remaining_work"]
VALIDATION_STATUS={"PASS","FAIL","NOT_RUN","NA"}
RECONCILIATION_RESULTS={"NO_ROADMAP_CHANGE","STATUS_UPDATE","ROADMAP_PROPOSAL","OWNER_DECISION_REQUIRED"}


def _text(v):
    return isinstance(v,str) and bool(v.strip())


def _nonempty_list_items(errors:list[str],value,label:str):
    if not isinstance(value,list):
        errors.append(f"{label} must be a list")
        return
    for i,item in enumerate(value):
        il=f"{label}[{i}]"
        if isinstance(item,str):
            if not item.strip():errors.append(f"{il} must not be empty")
        elif isinstance(item,dict):
            statement=item.get("statement") or item.get("description") or item.get("action")
            if not _text(statement):errors.append(f"{il} mapping requires statement/description/action")
            basis=item.get("basis")
            if basis is not None and not isinstance(basis,list):errors.append(f"{il}.basis must be a list when present")
        else:
            errors.append(f"{il} must be a non-empty string or mapping")


def _validate_v2(cp:dict,e:list[str]):
    e+=require(cp,V2_REQUIRED,"CP v2")
    result=cp.get("implementation_result")
    if not isinstance(result,dict):
        e.append("CP v2 implementation_result must be a mapping")
    else:
        e+=require(result,["summary","completed_steps","files_changed"],"CP v2 implementation_result")
        if not _text(result.get("summary")):e.append("CP v2 implementation_result.summary must be explicit")
        completed=result.get("completed_steps")
        files=result.get("files_changed")
        if not isinstance(completed,list):e.append("CP v2 implementation_result.completed_steps must be a list")
        else:
            if len(completed)!=len(set(str(x) for x in completed)):e.append("CP v2 implementation_result.completed_steps must not contain duplicates")
            for i,item in enumerate(completed):
                if not _text(item):e.append(f"CP v2 implementation_result.completed_steps[{i}] must be non-empty string")
        if not isinstance(files,list):e.append("CP v2 implementation_result.files_changed must be a list")
        else:
            if len(files)!=len(set(str(x) for x in files)):e.append("CP v2 implementation_result.files_changed must not contain duplicates")
            for i,item in enumerate(files):
                if not _text(item):e.append(f"CP v2 implementation_result.files_changed[{i}] must be non-empty repository-relative path")

    if not isinstance(cp.get("acceptance_results"),list):e.append("CP v2 acceptance_results must be a list")
    if not isinstance(cp.get("validation_results"),list):e.append("CP v2 validation_results must be a list")
    if not isinstance(cp.get("quality_findings"),list):e.append("CP v2 quality_findings must be a list")
    if not isinstance(cp.get("discoveries"),list):e.append("CP v2 discoveries must be a list")
    _nonempty_list_items(e,cp.get("known_limitations"),"CP v2 known_limitations")
    _nonempty_list_items(e,cp.get("remaining_work"),"CP v2 remaining_work")

    recon=cp.get("roadmap_reconciliation")
    if not isinstance(recon,dict):
        e.append("CP v2 roadmap_reconciliation must be a mapping")
    else:
        e+=require(recon,["result","status_updates","proposals","owner_decisions_required"],"CP v2 roadmap_reconciliation")
        for key in ("status_updates","proposals","owner_decisions_required"):
            value=recon.get(key)
            if not isinstance(value,list):e.append(f"CP v2 roadmap_reconciliation.{key} must be a list")
            elif key=="owner_decisions_required":
                _nonempty_list_items(e,value,f"CP v2 roadmap_reconciliation.{key}")


def validate_file(path:Path):
    e=[];w=[];cp=load_yaml(path);e+=require(cp,REQ,"CP")
    if cp.get("schema_version")!="relay-v2.5":e.append("CP: schema_version must be relay-v2.5")

    contract=cp.get("contract_version")
    if contract is None:
        w.append("legacy checkpoint contract: contract_version missing; v2 checkpoint publication fields are not strictly enforced")
    elif contract not in {1,2}:
        e.append(f"CP.contract_version invalid: {contract}")
    elif contract==1:
        w.append("legacy checkpoint contract_version 1; migrate newly produced checkpoints to contract_version 2")
    else:
        _validate_v2(cp,e)

    if not _text(cp.get("checkpoint_id")) or not str(cp.get("checkpoint_id")).startswith("CP-"):e.append("CP.checkpoint_id must use CP-* namespace")
    if not _text(cp.get("ep_id")) or not str(cp.get("ep_id")).startswith("EP-"):e.append("CP.ep_id must use EP-* namespace")

    roadmap_basis=cp.get("roadmap_basis")
    if not isinstance(roadmap_basis,dict):
        e.append("CP.roadmap_basis must be a mapping")
    else:
        e+=require(roadmap_basis,["roadmap_id","revision"],"CP.roadmap_basis")
        for key in ("roadmap_id","revision"):
            if not _text(roadmap_basis.get(key)):e.append(f"CP.roadmap_basis.{key} must be explicit")

    execution_basis=cp.get("execution_basis") or {};e+=require(execution_basis,["material_ref"],"CP.execution_basis");material_ref=execution_basis.get("material_ref")
    if not str(material_ref or "").strip():e.append("CP.execution_basis.material_ref must be explicit")

    seen=set()
    validation_results=cp.get("validation_results")
    if validation_results is not None and not isinstance(validation_results,list):e.append("CP.validation_results must be a list")
    for i,result in enumerate(validation_results or []):
        label=f"CP.validation_results[{i}]"
        if not isinstance(result,dict):e.append(f"{label} must be a mapping");continue
        e+=require(result,["id","status","basis_ref"],label)
        rid=result.get("id")
        if rid in seen:e.append(f"duplicate checkpoint validation result {rid}")
        seen.add(rid)
        status=result.get("status")
        if status not in VALIDATION_STATUS:e.append(f"{label}.status invalid: {status}")
        if status in {"PASS","FAIL","NOT_RUN"} and str(result.get("basis_ref"))!=str(material_ref):e.append(f"{label}.basis_ref must match checkpoint material_ref")
        if status=="NOT_RUN" and not str(result.get("reason","")).strip():e.append(f"{label} NOT_RUN requires reason")

    qr=cp.get("quality_review")
    if qr is not None:
        if not isinstance(qr,dict):e.append("CP.quality_review must be a mapping or null")
        else:
            e+=require(qr,["id","path","digest"],"CP.quality_review")
            if _text(qr.get("id")) and not str(qr.get("id")).startswith("QRV-"):e.append("CP.quality_review.id must use QRV-* namespace")
            for key in ("path","digest"):
                if not _text(qr.get(key)):e.append(f"CP.quality_review.{key} must be explicit")

    qseen=set()
    quality_findings=cp.get("quality_findings")
    if quality_findings is not None and not isinstance(quality_findings,list):e.append("CP.quality_findings must be a list")
    for i,item in enumerate(quality_findings or []):
        label=f"CP.quality_findings[{i}]"
        if not isinstance(item,dict):e.append(f"{label} must be a mapping");continue
        fid=item.get("id")
        if not _text(fid) or not str(fid).startswith("QF-"):e.append(f"{label}.id must use QF-* namespace")
        elif fid in qseen:e.append(f"duplicate checkpoint quality finding {fid}")
        else:qseen.add(fid)

    recon=cp.get("roadmap_reconciliation") or {}
    if recon.get("result") not in RECONCILIATION_RESULTS:e.append("CP: invalid roadmap_reconciliation.result")

    successor=cp.get("successor") or {};e+=require(successor,["mode","frontier_work_package","ep_id","parallel_plan","lanes"],"CP.successor")
    mode=successor.get("mode")
    if mode not in {"SERIAL","PARALLEL","JOIN","NONE"}:e.append(f"CP.successor.mode invalid: {mode}")
    if mode=="SERIAL":
        if not successor.get("frontier_work_package") or not successor.get("ep_id"):e.append("SERIAL successor requires frontier_work_package and ep_id")
        if successor.get("parallel_plan") not in {None,""} or successor.get("lanes"):e.append("SERIAL successor must not declare parallel plan/lanes")
        if successor.get("lane_id") not in {None,""}:e.append("SERIAL successor must not declare lane_id")
    elif mode=="PARALLEL":
        if not successor.get("parallel_plan"):e.append("PARALLEL successor requires parallel_plan id")
        if len(successor.get("lanes") or [])<2:e.append("PARALLEL successor requires at least two lane receipts")
        if successor.get("frontier_work_package") not in {None,""} or successor.get("ep_id") not in {None,""}:e.append("PARALLEL successor uses lane receipts, not singular frontier_work_package/ep_id")
        if successor.get("lane_id") not in {None,""}:e.append("PARALLEL fork successor must not declare lane_id")
    elif mode=="JOIN":
        if not successor.get("parallel_plan"):e.append("JOIN successor requires parallel_plan id")
        if not str(successor.get("lane_id","")).strip():e.append("JOIN successor requires lane_id")
        if successor.get("frontier_work_package") not in {None,""} or successor.get("ep_id") not in {None,""} or successor.get("lanes"):e.append("JOIN successor routes through the parallel join receipt, not a singular EP or lane list")
    elif mode=="NONE":
        if successor.get("frontier_work_package") not in {None,""} or successor.get("ep_id") not in {None,""} or successor.get("parallel_plan") not in {None,""} or successor.get("lane_id") not in {None,""} or successor.get("lanes"):e.append("NONE successor must not declare downstream work")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("checkpoint");a=ap.parse_args()
    try:e,w=validate_file(Path(a.checkpoint).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))


if __name__=="__main__":
    main()
