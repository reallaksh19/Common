#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from report_projection import build,_current_issues
from takeoverlib import digest_mapping,yaml_digest

def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=build(root);p=r.get("progress") or {};cur=p.get("current") or {}
    if r.get("schema_version")!="relay-v2.5-report-projection":e.append("report projection schema_version mismatch")
    basis=r.get("generated_from") or {}
    if basis.get("roadmap_revision")!=(state.get("roadmap") or {}).get("revision"):e.append("report projection roadmap revision is stale")
    if basis.get("progress_basis")!=(state.get("progress") or {}).get("basis_revision"):e.append("report projection progress basis does not match repository state")
    if basis.get("owner_decisions_digest")!=digest_mapping(r.get("owner_decisions") or []):e.append("report projection owner-decision basis is stale")
    if p.get("overall_percent") is None:e.append("report projection requires authoritative overall progress")
    current_work=r.get("current_work") or {};position=state.get("current_position") or {}
    for key in ("objective","phase","work_package"):
        if current_work.get(key)!=position.get(key):e.append(f"report projection current_work.{key} diverges from REPO_STATE")
    if current_work.get("ep_id")!=(state.get("active_ep") or {}).get("id"):e.append("report projection current_work.ep_id diverges from REPO_STATE")
    issue_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml";issue_graph=load_yaml(issue_path) if issue_path.exists() else {"nodes":[]}
    expected_issues=_current_issues(issue_graph,position.get("work_package"))
    if current_work.get("issues")!=expected_issues:e.append("report projection current issues diverge from ISSUE_GRAPH")
    cp_ptr=state.get("last_checkpoint") or {};cp_path=cp_ptr.get("path")
    if cp_path and (root/cp_path).exists():
        cp=load_yaml(root/cp_path);qptr=cp.get("quality_review") or {};qpath=qptr.get("path")
        if qpath:
            if not (root/qpath).exists():e.append("report projection checkpoint quality_review path is missing")
            else:
                if basis.get("quality_review_id")!=qptr.get("id"):e.append("report projection quality_review id is stale")
                if basis.get("quality_review_digest")!=yaml_digest(root/qpath):e.append("report projection quality_review digest is stale")
                projected=((r.get("checkpoint") or {}).get("quality_review") or {});qrv=load_yaml(root/qpath)
                if projected.get("id")!=qrv.get("quality_review_id") or projected.get("overall_state")!=qrv.get("overall_state"):e.append("report projection checkpoint quality review does not match QRV")
                if projected.get("procedure_results")!=(qrv.get("procedure_results") or []):e.append("report projection quality procedure results do not match QRV")
                if projected.get("findings")!=(qrv.get("findings") or []):e.append("report projection quality findings do not match QRV")
        elif basis.get("quality_review_id") is not None or basis.get("quality_review_digest") is not None:e.append("report projection carries quality-review basis without checkpoint QRV")
        projected_cp=r.get("checkpoint") or {}
        if projected_cp.get("known_limitations")!=(cp.get("known_limitations") or []):e.append("report projection known limitations do not match checkpoint")
        if projected_cp.get("remaining_work")!=(cp.get("remaining_work") or []):e.append("report projection remaining work does not match checkpoint")
        if projected_cp.get("roadmap_reconciliation")!=(cp.get("roadmap_reconciliation") or {}):e.append("report projection roadmap reconciliation does not match checkpoint")
    if state.get("relay_state")=="ACTIVE":
        for key in ("phase_percent","work_package_percent","ep_percent"):
            if cur.get(key) is None:e.append(f"report projection current.{key} is missing")
        ep=load_yaml(root/(state.get("active_ep") or {})["path"]);expected={str(x.get("id")) for x in ep.get("acceptance",[]) or [] if isinstance(x,dict)};actual={str(x.get("id")) for x in r.get("acceptance",[]) or [] if isinstance(x,dict)}
        if actual!=expected:e.append(f"report projection acceptance does not exactly cover active EP: expected {sorted(expected)}, got {sorted(actual)}")
        contract=r.get("active_contract") or {};ctx=ep.get("context_capsule") or {}
        if contract.get("outcome")!=(ep.get("outcome") or {}):e.append("report projection active outcome does not match EP")
        if contract.get("scope")!=(ep.get("scope") or {}):e.append("report projection active scope does not match EP")
        if contract.get("known_problems")!=(ctx.get("known_problems") or []):e.append("report projection known problems do not match EP context")
        if contract.get("deliberate_non_goals")!=(ctx.get("deliberate_non_goals") or []):e.append("report projection deliberate non-goals do not match EP context")
        nw=r.get("next_work") or {}
        if not isinstance(nw.get("steps"),list) or not nw.get("steps"):e.append("report projection ACTIVE route requires structured next_work.steps")
    if state.get("relay_state")=="PARALLEL":
        lanes=r.get("parallel_lanes") or []
        if len(lanes)<2:e.append("parallel report projection must cover every active lane")
        for lane in lanes:
            if not ((lane.get("next_work") or {}).get("steps") or []):e.append(f"parallel lane {lane.get('lane_id')} lacks structured next work")
            if not isinstance(lane.get("contract"),dict):e.append(f"parallel lane {lane.get('lane_id')} lacks communication contract projection")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
