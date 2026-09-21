#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from communication_projection import build
from render_owner_status import render as render_owner
from takeoverlib import digest_mapping
from owner_publication import cursor_digest,publication_status

FORBIDDEN_OWNER_TOKENS=("BATON_READY","TAKEOVER_CERTIFIED","MATERIAL_WRITE_READY","GHGEN-","GHOP-","QSET-","QUAL-","DISC-","QRV-","ODR-","REPO_STATE","material_authority")
OWNER_HEADINGS=("# Owner Roadmap","## Executive state","## Phase status","## Concept roadmap","## Active work","## Completed work log","## Newly discovered work","## Blocked / waiting","## Deferred validations / known issues / delegated checks","## What can happen now","## What changed","## What this work is for","## What will not change without authority","## Evidence and confidence","## Quality and known risks","## Roadmap and progress","## Delivery","## Action required outside this environment","## Owner decisions","## Recommended forward sequence","## Roadmap revision history","## What would stop progress")


def _subjects(items):
    out=[]
    for item in items or []:
        if isinstance(item,dict):out.append(str(item.get("invariant") or item.get("domain") or item.get("path") or item.get("decision") or ""))
        else:out.append(str(item))
    return [x for x in out if x]


def _source_next(report:dict):
    nw=report.get("next_work") or {}
    if nw.get("steps"):
        return [{**x,"lane_id":None,"ep_id":(report.get("generated_from") or {}).get("ep_id")} for x in nw["steps"] if isinstance(x,dict)]
    out=[]
    for lane in report.get("parallel_lanes",[]) or []:
        for step in (lane.get("next_work") or {}).get("steps",[]) or []:
            if isinstance(step,dict):out.append({**step,"lane_id":lane.get("lane_id"),"ep_id":lane.get("ep_id")})
    return out


def validate(root:Path):
    e=[];w=[];c=build(root);owner=c.get("owner") or {};report=((c.get("technical") or {}).get("report") or {})
    if c.get("schema_version")!="relay-v2.5-communication-projection":e.append("communication projection schema_version mismatch")
    if (c.get("generated_from") or {}).get("report_projection_digest")!=digest_mapping(report):e.append("communication projection is not bound to its technical report projection")
    if (c.get("generated_from") or {}).get("report_sources")!=(report.get("generated_from") or {}):e.append("communication projection source bindings diverge from report projection")
    if (c.get("generated_from") or {}).get("owner_publication_cursor_digest")!=cursor_digest(root):e.append("communication projection Owner publication cursor binding is stale")
    expected_change=publication_status(root,report);owner_change=owner.get("change") or {}
    for key in ("event_class","changed_dimensions","publication_due","current_digest","previous_publication_id","previous_sequence","cursor_path","cursor_present"):
        if owner_change.get(key)!=expected_change.get(key):e.append(f"Owner publication change {key} diverges from current cursor/report truth")
    if owner_change.get("details")!=expected_change.get("details"):e.append("Owner publication change details diverge from current cursor/report truth")
    source_work=report.get("current_work") or {};owner_work=owner.get("current_work") or {}
    for key in ("objective","phase","work_package","ep_id"):
        if owner_work.get(key)!=source_work.get(key):e.append(f"Owner current_work {key} diverges from source report")
    if owner_work.get("issues")!=(source_work.get("issues") or []):e.append("Owner current issues diverge from source report")
    progress=report.get("progress") or {};cur=progress.get("current") or {};op=((owner.get("roadmap") or {}).get("progress") or {})
    expected_progress={"progress_basis":progress.get("progress_basis") or {},"overall_percent":progress.get("overall_percent"),"phase_percent":cur.get("phase_percent"),"work_package_percent":cur.get("work_package_percent"),"ep_percent":cur.get("ep_percent")}
    for key,value in expected_progress.items():
        if op.get(key)!=value:e.append(f"Owner progress {key} diverges from source report")
    if (owner.get("delivery") or {})!=(report.get("delivery") or {}):e.append("Owner delivery vector diverges from source report")
    control=owner.get("control") or {};source_obligations=[x for x in (report.get("control_obligations") or []) if isinstance(x,dict) and x.get("state")=="OPEN"]
    expected_pending=[x for x in source_obligations if x.get("kind")=="DEFERRED_VALIDATION"]
    expected_known=[x for x in source_obligations if x.get("kind")=="KNOWN_ISSUE"]
    expected_delegations=[x for x in source_obligations if x.get("kind")=="DELEGATION"]
    if control.get("pending_validations")!=expected_pending:e.append("Owner control projection drops or changes OPEN deferred validations")
    if control.get("known_issues")!=expected_known:e.append("Owner control projection drops or changes OPEN known issues")
    if control.get("delegations")!=expected_delegations:e.append("Owner control projection drops or changes OPEN delegations")
    if (control.get("execution_custody") or {})!=(report.get("execution_custody") or {"enforced":False,"leases":[]}):e.append("Owner control projection execution custody diverges from source report")
    evidence=report.get("evidence") or {};oe=owner.get("evidence") or {}
    if oe.get("state")!=evidence.get("state") or oe.get("summary")!=evidence.get("summary"):e.append("Owner evidence summary diverges from source report")
    if oe.get("not_run")!=(evidence.get("not_run") or []):e.append("Owner view must preserve every NOT_RUN evidence item")
    if oe.get("acceptance")!=(report.get("acceptance") or []):e.append("Owner view must preserve current acceptance projection")
    contract=report.get("active_contract") or {};scope=contract.get("scope") or {};os=owner.get("scope") or {}
    for key in ("protected","prohibited","owner_reserved"):
        if os.get(key)!=(scope.get(key) or []):e.append(f"Owner scope {key} diverges from active contract")
    source_steps=_source_next(report);owner_steps=((owner.get("next_work") or {}).get("steps") or [])
    if [(x.get("action"),x.get("expected_result"),x.get("stop_if") or []) for x in owner_steps] != [(x.get("action"),x.get("expected_result"),x.get("stop_if") or []) for x in source_steps]:e.append("Owner next work must preserve exact action/expected-result/stop semantics")
    expected_external=[{**x.get("execution_requirement"),"action":x.get("action"),"expected_result":x.get("expected_result"),"ep_id":x.get("ep_id"),"lane_id":x.get("lane_id")} for x in source_steps if isinstance(x.get("execution_requirement"),dict)]
    if (owner.get("external_actions") or [])!=expected_external:e.append("Owner external actions diverge from EP next-work execution requirements")
    stop=report.get("stop") or {};required=((owner.get("decisions") or {}).get("required_now") or [])
    if stop.get("active") and stop.get("category")=="OWNER_DECISION_REQUIRED" and not required:e.append("Owner decision-required hard stop must appear in Owner decisions")
    if not (stop.get("active") and stop.get("category")=="OWNER_DECISION_REQUIRED"):
        recon=((report.get("checkpoint") or {}).get("roadmap_reconciliation") or {});recon_required=recon.get("owner_decisions_required") or []
        if not recon_required and required:e.append("Owner view must not invent a current Owner decision requirement")
    qrv=((report.get("checkpoint") or {}).get("quality_review") or {});source_risks=[x for x in qrv.get("findings",[]) or [] if isinstance(x,dict) and x.get("disposition")!="REMEDIATED"]
    visible=(owner.get("quality") or {}).get("visible_risks") or []
    statements={str(x.get("statement")) for x in visible if isinstance(x,dict)}
    for finding in source_risks:
        if str(finding.get("statement")) not in statements:e.append(f"Owner view hides unresolved quality finding {finding.get('id')}")
    text=render_owner(root)
    for item in expected_pending:
        oid=str(item.get("id") or "")
        if oid and oid not in text:e.append(f"Owner status hides pending control {oid}")
        if str(item.get("summary") or "") and str(item.get("summary")) not in text:e.append(f"Owner status hides pending-control summary {oid}")
        for boundary in item.get("must_resolve_before") or []:
            label=str(boundary).replace("_"," ").title()
            if label not in text:e.append(f"Owner status hides pending-control boundary {oid}: {boundary}")
    for item in expected_known:
        oid=str(item.get("id") or "")
        if oid and oid not in text:e.append(f"Owner status hides known issue {oid}")
        if str(item.get("summary") or "") and str(item.get("summary")) not in text:e.append(f"Owner status hides known-issue summary {oid}")
    for item in expected_delegations:
        oid=str(item.get("id") or "")
        if oid and oid not in text:e.append(f"Owner status hides delegation {oid}")
        if "read-only" not in text.lower():e.append("Owner status must identify delegated monitor work as read-only")
    for heading in OWNER_HEADINGS:
        if heading not in text:e.append(f"Owner status missing required section {heading}")
    for token in FORBIDDEN_OWNER_TOKENS:
        if token in text:e.append(f"Owner status leaks relay-internal jargon: {token}")
    event_text=str(owner_change.get("event_class") or "").replace("_"," ").title()
    if event_text and event_text not in text:e.append("Owner status hides deterministic publication event class")
    if owner_change.get("event_class")=="NO_MATERIAL_PROGRESS" and "No material engineering" not in text:e.append("Owner status must explicitly report no material progress")
    if "task" not in (owner_change.get("changed_dimensions") or []) and owner_change.get("event_class") not in {"INITIAL_SNAPSHOT","NO_MATERIAL_PROGRESS"} and "Acceptance/progress did not move." not in text:e.append("Owner status hides unchanged acceptance/progress fact")
    if stop.get("active") and str(stop.get("reason") or "") not in text:e.append("Owner status hides active stop reason")
    for item in evidence.get("not_run",[]) or []:
        if str(item.get("reason") or "") and str(item.get("reason")) not in text:e.append(f"Owner status hides missing-evidence reason for {item.get('id')}")
    for item in report.get("acceptance") or []:
        if not isinstance(item,dict):continue
        aid=str(item.get("id") or "")
        if aid and aid not in text:e.append(f"Owner status hides acceptance criterion {aid}")
        status=str(item.get("status") or "").replace("_"," ").title()
        if status and status not in text:e.append(f"Owner status hides acceptance status for {aid}")
        percent=item.get("percent")
        if isinstance(percent,(int,float)) and f"{percent:g}%" not in text:e.append(f"Owner status hides acceptance percent for {aid}")
        for basis in item.get("basis") or []:
            if str(basis) not in text:e.append(f"Owner status hides acceptance basis for {aid}: {basis}")
    for finding in source_risks:
        if str(finding.get("statement") or "") and str(finding.get("statement")) not in text:e.append(f"Owner status hides unresolved quality risk {finding.get('id')}")
    for issue in source_work.get("issues") or []:
        number=issue.get("issue_number");url=issue.get("url")
        if number is not None and f"#{number}" not in text:e.append(f"Owner status hides current issue number {number}")
        if url and str(url) not in text:e.append(f"Owner status hides current issue URL {url}")
    delivery=report.get("delivery") or {}
    if delivery.get("applicability")=="APPLICABLE":
        vehicle=delivery.get("vehicle") or {};number=vehicle.get("number");url=vehicle.get("url")
        if number is not None and f"PR #{number}" not in text:e.append("Owner status hides current PR number")
        if url and str(url) not in text:e.append("Owner status hides current PR URL")
        for value in (
            (delivery.get("checks") or {}).get("state"),
            (delivery.get("mergeability") or {}).get("state"),
            (delivery.get("review") or {}).get("state"),
            (delivery.get("ready_for_review") or {}).get("state"),
            (delivery.get("technical_ready_to_merge") or {}).get("state"),
            (delivery.get("merge_authorization") or {}).get("state"),
        ):
            if value and str(value).replace("_"," ").title() not in text and str(value) not in text:e.append(f"Owner status hides delivery state {value}")
        carried=delivery.get("unmerged_prs") or []
        if carried and "Unmerged PRs carried forward" not in text:e.append("Owner status hides unmerged PR carry-forward section")
        for item in carried:
            v=item.get("vehicle") or {};number=v.get("number");url=v.get("url")
            if number is not None and f"PR #{number}" not in text:e.append(f"Owner status drops carried-forward PR #{number}")
            if url and str(url) not in text:e.append(f"Owner status drops carried-forward PR URL {url}")
            for row in item.get("correlations") or []:
                if f"Issue #{row.get('issue_number')}" not in text:e.append(f"Owner status drops carried-forward Issue correlation #{row.get('issue_number')}")
                if str(row.get("ep_id") or "") not in text:e.append(f"Owner status drops carried-forward EP correlation {row.get('ep_id')}")
    for key in ("protected","prohibited"):
        for subject in _subjects(scope.get(key)):
            if subject not in text:e.append(f"Owner status hides {key} scope: {subject}")
    pb=progress.get("progress_basis") or {}
    if pb.get("id") and str(pb.get("id")) not in text:e.append("Owner status hides current progress-basis id")
    basis_delta=(owner_change.get("details") or {}).get("progress_basis") or {}
    if basis_delta.get("from")!=basis_delta.get("to"):
        before=basis_delta.get("from") or {};after=basis_delta.get("to") or {}
        if before.get("id") and str(before.get("id")) not in text:e.append("Owner status hides prior progress-basis id")
        if after.get("id") and str(after.get("id")) not in text:e.append("Owner status hides new progress-basis id")
    if cur.get("ep_percent") is not None and f"{cur.get('ep_percent'):g}%" not in text:e.append("Owner status hides active execution-package progress")
    for item in expected_external:
        for value in (item.get("command") or item.get("instruction"),item.get("unavailable_here_reason"),item.get("success_condition")):
            if value and str(value) not in text:e.append("Owner status hides external execution requirement detail")
        for value in (item.get("blocks") or [])+(item.get("clears") or [])+(item.get("expected_evidence") or []):
            if str(value) not in text:e.append("Owner status hides external execution consequence/evidence")
    for step in source_steps:
        if str(step.get("action") or "") not in text or str(step.get("expected_result") or "") not in text:e.append("Owner status hides exact next-work action or expected result")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    from relaylib import print_result
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
