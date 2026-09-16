#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from takeoverlib import yaml_digest
from qualitylib import BLUEPRINTS,DISPOSITIONS,FINDING_CLASSES,HARD_STOPS,PROCEDURE_RESULTS,QUALITY_STATES,SEVERITIES,STOP_TRIGGERS,ep_index,items,router_snapshot,text

NOT_RUN_CAUSES={"INFRASTRUCTURE","UNAVAILABLE_TOOL","NOT_SCHEDULED","DEPENDENCY_WAIT","OTHER"}

def validate_file(root:Path,path:Path,epmap=None):
    e=[];w=[];q=load_yaml(path);epmap=epmap or ep_index(root)
    if q.get("schema_version")!="relay-v2.5-quality-review":e.append("QRV schema_version must be relay-v2.5-quality-review")
    qid=str(q.get("quality_review_id") or "")
    if not qid.startswith("QRV-"):e.append("quality_review_id must use QRV-* namespace")
    epref=q.get("ep") or {};eid=str(epref.get("id") or "");entry=epmap.get(eid)
    if not entry:e.append(f"QRV references unknown EP {eid}");ep=None;ep_path=None
    else:
        ep_path,ep=entry
        if str(epref.get("path") or "")!=str(ep_path.relative_to(root)):e.append("QRV ep.path does not match repository EP path")
        if epref.get("contract_digest")!=yaml_digest(ep_path):e.append("QRV EP contract digest is stale")
        if str(q.get("roadmap_revision") or "")!=str((ep.get("roadmap_source") or {}).get("roadmap_revision") or ""):e.append("QRV roadmap_revision does not match EP")
        if str(q.get("material_ref") or "")!=str((ep.get("git_basis") or {}).get("material_ref") or ""):e.append("QRV material_ref does not match EP")
        if q.get("router_snapshot")!=router_snapshot(ep):e.append("QRV router_snapshot does not exactly match EP quality router")
    reviewer=q.get("reviewer") or {}
    if reviewer.get("type") not in {"AGENT","OWNER","DETERMINISTIC_VALIDATOR"}:e.append("QRV reviewer.type invalid")
    if not text(reviewer.get("identity")):e.append("QRV reviewer.identity must be explicit")
    results=items(q.get("procedure_results"));expected=set()
    if ep:expected={x.get("blueprint") for x in items((ep.get("quality") or {}).get("applicable")) if isinstance(x,dict)}
    actual=set();seen=set()
    for i,r in enumerate(results):
        label=f"QRV.procedure_results[{i}]"
        if not isinstance(r,dict):e.append(f"{label} must be a mapping");continue
        bp=r.get("blueprint");actual.add(bp)
        if bp in seen:e.append(f"duplicate QRV procedure result {bp}")
        seen.add(bp)
        if bp not in BLUEPRINTS:e.append(f"{label}.blueprint unknown: {bp}")
        if r.get("result") not in PROCEDURE_RESULTS:e.append(f"{label}.result invalid: {r.get('result')}")
        if r.get("result") in {"CLEAR","FINDINGS"} and (not isinstance(r.get("evidence"),list) or not r.get("evidence")):e.append(f"{label} requires evidence")
        if r.get("result")=="NOT_RUN":
            if not text(r.get("reason")):e.append(f"{label} NOT_RUN requires reason")
            if r.get("cause") not in NOT_RUN_CAUSES:e.append(f"{label} NOT_RUN cause invalid: {r.get('cause')}")
    if ep and actual!=expected:e.append(f"QRV procedure_results must exactly cover applicable blueprints: expected {sorted(expected)}, got {sorted(actual)}")
    findings=items(q.get("findings"));blocking=[];owner=False;attention=any(r.get("result")=="NOT_RUN" for r in results if isinstance(r,dict))
    fids=set()
    for i,f in enumerate(findings):
        label=f"QRV.findings[{i}]"
        if not isinstance(f,dict):e.append(f"{label} must be a mapping");continue
        fid=str(f.get("id") or "")
        if not fid.startswith("QF-"):e.append(f"{label}.id must use QF-* namespace")
        if fid in fids:e.append(f"duplicate QRV finding {fid}")
        fids.add(fid)
        if f.get("blueprint") not in expected:e.append(f"{label}.blueprint was not applicable to the EP")
        if f.get("classification") not in FINDING_CLASSES:e.append(f"{label}.classification invalid")
        if f.get("severity") not in SEVERITIES:e.append(f"{label}.severity invalid")
        if f.get("disposition") not in DISPOSITIONS:e.append(f"{label}.disposition invalid")
        if not text(f.get("statement")):e.append(f"{label}.statement must be explicit")
        if not isinstance(f.get("evidence"),list) or not f.get("evidence"):e.append(f"{label}.evidence must contain durable basis")
        blocks=f.get("blocks_execution")
        if not isinstance(blocks,bool):e.append(f"{label}.blocks_execution must be boolean")
        hs=f.get("hard_stop")
        if blocks:
            blocking.append(f)
            if not isinstance(hs,dict):e.append(f"{label} blocking finding requires hard_stop mapping")
            else:
                if hs.get("category") not in HARD_STOPS:e.append(f"{label}.hard_stop.category invalid")
                if hs.get("trigger") not in STOP_TRIGGERS:e.append(f"{label}.hard_stop.trigger invalid")
                if not isinstance(hs.get("basis"),list) or not hs.get("basis"):e.append(f"{label}.hard_stop.basis must be durable")
        elif hs not in {None,"NONE"}:e.append(f"{label} non-blocking finding must not declare hard_stop")
        if f.get("disposition")=="OWNER_REVIEW_REQUIRED":owner=True
        if f.get("disposition")!="REMEDIATED":attention=True
    derived="OWNER_REVIEW_REQUIRED" if owner else ("NEEDS_ATTENTION" if attention else "CLEAR")
    if q.get("overall_state") not in QUALITY_STATES:e.append("QRV overall_state invalid")
    elif q.get("overall_state")!=derived:e.append(f"QRV overall_state must be derived as {derived}")
    eff=q.get("execution_effect") or {}
    if eff.get("blocks_execution") is not bool(blocking):e.append("QRV execution_effect.blocks_execution must equal presence of true blocking findings")
    ids=[x.get("id") for x in blocking]
    if list(eff.get("blocking_findings") or [])!=ids:e.append("QRV execution_effect.blocking_findings must exactly list blocking findings in order")
    if not isinstance(q.get("owner_report"),dict) or not text((q.get("owner_report") or {}).get("summary")):e.append("QRV owner_report.summary must be explicit")
    if not isinstance(q.get("successor_handover"),dict) or not isinstance((q.get("successor_handover") or {}).get("unresolved_findings"),list):e.append("QRV successor_handover.unresolved_findings must be a list")
    return e,w

def validate(root:Path):
    e=[];w=[];epmap=ep_index(root);qdir=root/"agents/relay/quality";validated={}
    if qdir.exists():
        for p in qdir.rglob("QRV-*.yaml"):
            ce,cw=validate_file(root,p,epmap);e.extend(f"{p.relative_to(root)}: {x}" for x in ce);w.extend(cw);validated[str(p.relative_to(root))]=load_yaml(p)
    cdir=root/"agents/relay/checkpoints"
    if cdir.exists():
        for cp_path in cdir.rglob("*.yaml"):
            try:cp=load_yaml(cp_path)
            except Exception:continue
            eid=str(cp.get("ep_id") or "");entry=epmap.get(eid)
            if not entry:continue
            _,ep=entry;rc=((ep.get("quality") or {}).get("review_contract") or {})
            if rc.get("required_before_checkpoint") is not True:continue
            ptr=cp.get("quality_review")
            if not isinstance(ptr,dict):e.append(f"checkpoint {cp_path.relative_to(root)} requires quality_review for EP {eid}");continue
            qpath=str(ptr.get("path") or "")
            if not qpath or not (root/qpath).exists():e.append(f"checkpoint {cp_path.relative_to(root)} quality_review path missing: {qpath}");continue
            qrv=load_yaml(root/qpath)
            if str(ptr.get("id") or "")!=str(qrv.get("quality_review_id") or ""):e.append(f"checkpoint {cp_path.relative_to(root)} quality_review.id mismatch")
            if str((qrv.get("ep") or {}).get("id") or "")!=eid:e.append(f"checkpoint {cp_path.relative_to(root)} quality review belongs to different EP")
            if str(qrv.get("material_ref") or "")!=str((cp.get("execution_basis") or {}).get("material_ref") or ""):e.append(f"checkpoint {cp_path.relative_to(root)} quality review material_ref differs from checkpoint")
            if ptr.get("digest")!=yaml_digest(root/qpath):e.append(f"checkpoint {cp_path.relative_to(root)} quality_review digest is stale")
            qfids=[str(x.get("id")) for x in items(qrv.get("findings")) if isinstance(x,dict)]
            cpfids=[str(x.get("id")) for x in items(cp.get("quality_findings")) if isinstance(x,dict)]
            if cpfids!=qfids:e.append(f"checkpoint {cp_path.relative_to(root)} quality_findings must mirror QRV finding ids in order")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
