#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require
REQ=["schema_version","checkpoint_id","ep_id","roadmap_basis","execution_basis","implementation_result","acceptance_results","validation_results","quality_findings","discoveries","roadmap_reconciliation","successor"]
VALIDATION_STATUS={"PASS","FAIL","NOT_RUN","NA"}

def _text(v):return isinstance(v,str) and bool(v.strip())

def validate_file(path:Path):
    e=[];w=[];cp=load_yaml(path);e+=require(cp,REQ,"CP")
    if cp.get("schema_version")!="relay-v2.5":e.append("CP: schema_version must be relay-v2.5")
    execution_basis=cp.get("execution_basis") or {};e+=require(execution_basis,["material_ref"],"CP.execution_basis");material_ref=execution_basis.get("material_ref")
    if not str(material_ref or "").strip():e.append("CP.execution_basis.material_ref must be explicit")
    seen=set()
    for i,result in enumerate(cp.get("validation_results",[]) or []):
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
    for i,item in enumerate(cp.get("quality_findings",[]) or []):
        label=f"CP.quality_findings[{i}]"
        if not isinstance(item,dict):e.append(f"{label} must be a mapping");continue
        fid=item.get("id")
        if not _text(fid) or not str(fid).startswith("QF-"):e.append(f"{label}.id must use QF-* namespace")
        elif fid in qseen:e.append(f"duplicate checkpoint quality finding {fid}")
        else:qseen.add(fid)
    if (cp.get("roadmap_reconciliation") or {}).get("result") not in {"NO_ROADMAP_CHANGE","STATUS_UPDATE","ROADMAP_PROPOSAL","OWNER_DECISION_REQUIRED"}:e.append("CP: invalid roadmap_reconciliation.result")
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
if __name__=="__main__":main()
