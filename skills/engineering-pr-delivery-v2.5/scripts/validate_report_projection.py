#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from report_projection import build
from takeoverlib import yaml_digest

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=build(root);p=r.get("progress") or {};cur=p.get("current") or {}
    if r.get("schema_version")!="relay-v2.5-report-projection":e.append("report projection schema_version mismatch")
    basis=r.get("generated_from") or {}
    if basis.get("roadmap_revision")!=(state.get("roadmap") or {}).get("revision"):e.append("report projection roadmap revision is stale")
    if basis.get("progress_basis")!=(state.get("progress") or {}).get("basis_revision"):e.append("report projection progress basis does not match repository state")
    if p.get("overall_percent") is None:e.append("report projection requires authoritative overall progress")
    cp_ptr=state.get("last_checkpoint") or {};cp_path=cp_ptr.get("path")
    if cp_path and (root/cp_path).exists():
        cp=load_yaml(root/cp_path);qptr=cp.get("quality_review") or {};qpath=qptr.get("path")
        if qpath:
            if not (root/qpath).exists():e.append("report projection checkpoint quality_review path is missing")
            else:
                if basis.get("quality_review_id")!=qptr.get("id"):e.append("report projection quality_review id is stale")
                if basis.get("quality_review_digest")!=yaml_digest(root/qpath):e.append("report projection quality_review digest is stale")
                projected=((r.get("checkpoint") or {}).get("quality_review") or {})
                qrv=load_yaml(root/qpath)
                if projected.get("id")!=qrv.get("quality_review_id") or projected.get("overall_state")!=qrv.get("overall_state"):e.append("report projection checkpoint quality review does not match QRV")
                if projected.get("findings")!=(qrv.get("findings") or []):e.append("report projection quality findings do not match QRV")
        elif basis.get("quality_review_id") is not None or basis.get("quality_review_digest") is not None:e.append("report projection carries quality-review basis without checkpoint QRV")
    if state.get("relay_state")=="ACTIVE":
        for key in ("phase_percent","work_package_percent","ep_percent"):
            if cur.get(key) is None:e.append(f"report projection current.{key} is missing")
        ep=load_yaml(root/(state.get("active_ep") or {})["path"]);expected={str(x.get("id")) for x in ep.get("acceptance",[]) or [] if isinstance(x,dict)};actual={str(x.get("id")) for x in r.get("acceptance",[]) or [] if isinstance(x,dict)}
        if actual!=expected:e.append(f"report projection acceptance does not exactly cover active EP: expected {sorted(expected)}, got {sorted(actual)}")
        nw=r.get("next_work") or {}
        if not isinstance(nw.get("steps"),list) or not nw.get("steps"):e.append("report projection ACTIVE route requires structured next_work.steps")
    if state.get("relay_state")=="PARALLEL":
        lanes=r.get("parallel_lanes") or []
        if len(lanes)<2:e.append("parallel report projection must cover every active lane")
        for lane in lanes:
            if not ((lane.get("next_work") or {}).get("steps") or []):e.append(f"parallel lane {lane.get('lane_id')} lacks structured next work")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
