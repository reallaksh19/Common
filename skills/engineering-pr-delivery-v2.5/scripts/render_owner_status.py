#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from communication_projection import build


def _pct(value):return "not calculated" if value is None else f"{value:g}%" if isinstance(value,(int,float)) else str(value)
def _text(item,keys):
    if isinstance(item,str):return item
    if not isinstance(item,dict):return str(item)
    for key in keys:
        value=item.get(key)
        if value is not None and value != "" and value != []:return str(value)
    return str(item)
def _scope_line(item):
    if not isinstance(item,dict):return str(item)
    subject=item.get("invariant") or item.get("domain") or item.get("path") or item.get("decision") or "protected area"
    reason=item.get("reason")
    return f"{subject} — {reason}" if reason else str(subject)


def render_projection(c:dict)->str:
    o=c["owner"];cap=o["capability"];rmap=o.get("roadmap") or {};progress=rmap.get("progress") or {};roadmap=rmap.get("summary") or {}
    current=o.get("current_work") or {};delivery=o.get("delivery") or {};recon=rmap.get("last_reconciliation") or {};control=o.get("control") or {}
    phase=progress.get("phase_title") or progress.get("phase");wp=progress.get("work_package_title") or progress.get("work_package")
    issues=current.get("issues") or [];issue=issues[0] if issues else {};vehicle=delivery.get("vehicle") or {}
    pb=progress.get("progress_basis") or {};roadmap_disposition=str(recon.get("result") or "NOT_RECONCILED").replace("_"," ").title()
    issue_label=f"#{issue.get('issue_number')}" if issue.get("issue_number") is not None else "not mapped"
    pr_label=f"#{vehicle.get('number')}" if vehicle.get("number") is not None else "not observed"
    pr_state=str(vehicle.get("lifecycle") or "UNKNOWN").replace("_"," ").title()
    lines=[
        "# Owner Roadmap","",
        f"Roadmap revision: **{roadmap.get('revision') or 'unknown'}**",
        f"Progress basis: **{pb.get('id') or 'unknown'}**",
        "",
        "## Executive state",
        f"Overall progress: **{_pct(progress.get('overall_percent'))}**.",
        f"Current phase: **{phase or 'unknown'}** — **{_pct(progress.get('phase_percent'))}**.",
        f"Current work: **{wp or 'unknown'}** — **{_pct(progress.get('work_package_percent'))}**.",
        f"Current issue: **{issue_label}**.",
        f"Current PR: **{pr_label} — {pr_state}**.",
        f"Roadmap disposition: **{roadmap_disposition}**.",
        "",
        "## Phase status",
        "| Phase | State | Progress | Current / next |",
        "| --- | --- | ---: | --- |",
    ]
    cur_phase=str(progress.get("phase") or "")
    for obj in progress.get("hierarchy") or []:
        for ph in obj.get("phases") or []:
            marker="current" if str(ph.get("id"))==cur_phase else ""
            lines.append(f"| {ph.get('title') or ph.get('id')} | {str(ph.get('state') or 'UNKNOWN').replace('_',' ').title()} | {_pct(ph.get('percent'))} | {marker} |")
    lines += ["","## Concept roadmap","| Concept | State | Progress | Current focus |","| --- | --- | ---: | --- |"]
    cur_obj=str(progress.get("objective") or "")
    for obj in progress.get("hierarchy") or []:
        focus=", ".join(str(ph.get("title") or ph.get("id")) for ph in (obj.get("phases") or []) if str(ph.get("id"))==cur_phase) or ("current" if str(obj.get("id"))==cur_obj else "—")
        lines.append(f"| {obj.get('id')} — {obj.get('title') or ''} | {str(obj.get('state') or 'UNKNOWN').replace('_',' ').title()} | {_pct(obj.get('percent'))} | {focus} |")
    lines += ["","## Active work","| WP | Issue | State | Acceptance / progress | Delivery |","| --- | --- | --- | ---: | --- |"]
    cur_wp=str(progress.get("work_package") or "")
    added=False
    for obj in progress.get("hierarchy") or []:
        for ph in obj.get("phases") or []:
            for row in ph.get("work_packages") or []:
                if str(row.get("id"))!=cur_wp and str(row.get("state") or "").upper() not in {"ACTIVE","BLOCKED"}:continue
                ilabel=issue_label if str(row.get("id"))==cur_wp else "—"
                dlabel=f"PR {pr_label} / {pr_state}" if str(row.get("id"))==cur_wp and vehicle else "—"
                lines.append(f"| {row.get('id')} — {row.get('title') or ''} | {ilabel} | {str(row.get('state') or 'UNKNOWN').replace('_',' ').title()} | {_pct(row.get('percent'))} | {dlabel} |")
                added=True
    if not added:lines.append("| — | — | No active roadmap work | — | — |")
    lines += ["","## Completed work log","| WP | Result |","| --- | --- |"]
    completed=[]
    for obj in progress.get("hierarchy") or []:
        for ph in obj.get("phases") or []:
            for row in ph.get("work_packages") or []:
                if str(row.get("state") or "").upper()=="COMPLETE" or row.get("percent")==100:
                    completed.append(row)
    if completed:
        for row in completed[-10:]:
            lines.append(f"| {row.get('id')} — {row.get('title') or ''} | Complete — {_pct(row.get('percent'))} |")
    else:lines.append("| — | No completed work package is present on the current progress basis. |")
    events=rmap.get("recent_events") or []
    discovered=[e for e in events if isinstance(e,dict) and e.get("follow_up")=="NEW_EXECUTION_WORK"]
    lines += ["","## Newly discovered work"]
    if discovered:
        for e in discovered[-5:]:
            xr=e.get("execution_refs") or {}
            lines.append(f"- {e.get('id')}: {e.get('summary')} — current execution ref: {xr.get('work_package') or 'not yet mapped'}; concept effect: {e.get('concept_change')}.")
    else:lines.append("- No unresolved newly discovered execution work is recorded in the recent material-event window.")
    lines += ["","## Blocked / waiting"]
    active_stop=cap.get("active_stop")
    ext=o.get("external_actions") or [];not_run=(o.get("evidence") or {}).get("not_run") or []
    pending_controls=control.get("pending_validations") or [];delegations=control.get("delegations") or []
    if active_stop:lines.append(f"- Active stop: {active_stop.get('reason') or active_stop.get('category')}")
    for item in pending_controls:
        boundaries=", ".join(str(x).replace("_"," ").title() for x in (item.get("must_resolve_before") or [])) or "a later boundary"
        allowed=", ".join(str(x).replace("_"," ").title() for x in (item.get("allowed_before_resolution") or [])) or "read-only work"
        lines.append(f"- Pending control {item.get('id')}: {item.get('summary')} — may continue: {allowed}; must resolve before: {boundaries}.")
    for item in delegations:lines.append(f"- Delegated check {item.get('id')}: {item.get('summary')} — monitoring is read-only until its success condition is met.")
    for item in ext:lines.append(f"- External/local action: {item.get('action')} — blocks {', '.join(str(x) for x in (item.get('blocks') or []))}.")
    for item in not_run:lines.append(f"- Evidence not run: {_text(item,['reason','summary'])}")
    if not active_stop and not pending_controls and not delegations and not ext and not not_run:lines.append("- No current blocker, pending control, waiting external action, or NOT_RUN evidence is recorded.")
    lines += ["","## What can happen now",f"{cap.get('summary')}"]
    overrides=control.get("active_execution_overrides") or []
    if overrides:
        blocks=sorted({str(x) for row in overrides for x in (row.get("blocks") or [])})
        lines.append(f"A recorded bounded Owner execution override is active. It permits only its declared scope and does not mark deferred controls PASS. Blocked boundaries remain: {', '.join(x.replace('_',' ').title() for x in blocks) or 'none recorded'}.")

    if phase or wp:lines.append(f"Current roadmap position: **{phase or 'current phase'}** → **{wp or 'current work package'}**.")
    cadence=o.get("status_cadence") or {}
    if cadence.get("required"):
        lines.append(f"Owner status heartbeat: **{cadence.get('effective_after_minutes') or 25} minutes** from task start unless the task completes earlier.")
    else:
        lines.append("Owner status heartbeat: **disabled by explicit Owner override** for this task.")
    change=o.get("change") or {};details=change.get("details") or {};event=str(change.get("event_class") or "UNKNOWN").replace("_"," ").title()
    lines += ["","## What changed",f"Publication event: **{event}**."]
    if change.get("event_class")=="INITIAL_SNAPSHOT":
        lines.append("- Initial Owner publication baseline established from current repository truth.")
    elif change.get("event_class")=="NO_MATERIAL_PROGRESS":
        lines.append("- No material engineering, evidence, delivery/custody, roadmap, blocker, decision, issue, or next-work state changed since the last Owner publication.")
    else:
        dims=", ".join(str(x).replace("_"," ") for x in (change.get("changed_dimensions") or []))
        lines.append(f"- Changed dimensions: {dims or 'none'}.")
        if "task" not in (change.get("changed_dimensions") or []):lines.append("- Acceptance/progress did not move.")
        if "implementation" not in (change.get("changed_dimensions") or []):lines.append("- No newly recorded implementation/file change occurred in this publication delta.")
    for row in details.get("acceptance_transitions") or []:
        lines.append(f"- Acceptance {row.get('id')}: {row.get('from_status') or 'absent'} ({_pct(row.get('from_percent'))}) → {row.get('to_status') or 'absent'} ({_pct(row.get('to_percent'))}).")
    if details.get("completed_steps"):lines.append(f"- Completed steps recorded now: {', '.join(str(x) for x in details.get('completed_steps') or [])}.")
    if details.get("files_changed"):lines.append(f"- Files changed in the current checkpoint result: {', '.join(str(x) for x in details.get('files_changed') or [])}.")
    ev_change=details.get("evidence_state") or {}
    if ev_change.get("from")!=ev_change.get("to"):lines.append(f"- Evidence state: {ev_change.get('from') or 'none'} → {ev_change.get('to') or 'none'}.")
    basis_change=details.get("progress_basis") or {}
    if basis_change.get("from")!=basis_change.get("to"):
        before=basis_change.get("from") or {};after=basis_change.get("to") or {}
        lines.append(f"- Progress basis: {before.get('id') or 'none'} → {after.get('id') or 'none'}; roadmap basis: {before.get('roadmap_revision') or 'none'} → {after.get('roadmap_revision') or 'none'}.")
    rm_change=details.get("roadmap_revision") or {}
    if rm_change.get("from")!=rm_change.get("to"):lines.append(f"- Roadmap revision: {rm_change.get('from') or 'none'} → {rm_change.get('to') or 'none'}.")
    if details.get("issue_change"):lines.append("- Current issue/coordination identity or state changed.")
    if details.get("stop_change"):lines.append("- Active stop/blocker state changed.")
    if details.get("next_work_change"):lines.append("- Exact next-work contract changed.")
    purpose=o.get("purpose") or {};lines += ["","## What this work is for"]
    current_wp=current.get("work_package_title") or current.get("work_package");current_ep=current.get("ep_id")
    if current_wp:lines.append(f"- Current work: **{current_wp}**{f' / {current_ep}' if current_ep else ''}.")
    for issue in current.get("issues") or []:
        number=issue.get("issue_number");state=str(issue.get("github_state") or issue.get("engineering_state") or "unknown").replace("_"," ").title();url=issue.get("url")
        label=f"Issue #{number}" if number is not None else str(issue.get("id") or "Current issue")
        suffix=f" — {url}" if url else ""
        lines.append(f"- {label}: **{state}**{suffix}")
    goals=(purpose.get("user_visible") or [])+(purpose.get("engineering") or [])
    if goals:
        for goal in goals:lines.append(f"- {goal}")
    else:lines.append("- No active material work is currently defined.")
    scope=o.get("scope") or {};lines += ["","## What will not change without authority"]
    protected=(scope.get("protected") or [])+(scope.get("prohibited") or [])+(scope.get("deliberate_non_goals") or [])
    if protected:
        for item in protected:lines.append(f"- {_scope_line(item)}")
    else:lines.append("- No additional protected or prohibited scope is recorded for the current slice.")
    reserved=scope.get("owner_reserved") or []
    if reserved:
        lines.append("- The following choices remain reserved to you if they become necessary:")
        for item in reserved:lines.append(f"  - {_scope_line(item)}")
    ev=o.get("evidence") or {};lines += ["","## Evidence and confidence",f"Evidence state: **{str(ev.get('state') or 'unknown').replace('_',' ').title()}**. {ev.get('summary') or ''}".rstrip()]
    if ev.get("not_run"):
        lines.append("Evidence still missing or not run:")
        for item in ev["not_run"]:lines.append(f"- {_text(item,['reason','summary'])}")
    acceptance=ev.get("acceptance") or []
    if acceptance:
        done=sum(1 for item in acceptance if isinstance(item,dict) and item.get("percent")==100);lines.append(f"Acceptance: {done} of {len(acceptance)} criteria are complete on the recorded progress basis.")
        for item in acceptance:
            if not isinstance(item,dict):continue
            basis=", ".join(str(x) for x in (item.get("basis") or [])) or "none recorded"
            lines.append(f"- {item.get('id')}: **{str(item.get('status') or 'UNKNOWN').replace('_',' ').title()}** — {_pct(item.get('percent'))}; basis: {basis}.")
    quality=o.get("quality") or {};lines += ["","## Quality and known risks",f"Quality state: **{str(quality.get('state') or 'unknown').replace('_',' ').title()}**."]
    risks=quality.get("visible_risks") or []
    if risks:
        for risk in risks:
            statement=_text(risk,["statement"]);severity=(risk.get("severity") if isinstance(risk,dict) else None);suffix=f" ({str(severity).lower()} severity)" if severity else "";lines.append(f"- {statement}{suffix}")
    else:lines.append("- No unresolved quality finding is currently recorded.")
    if quality.get("procedure_gaps"):
        lines.append("Quality checks not completed:")
        for gap in quality["procedure_gaps"]:lines.append(f"- {gap.get('procedure')}: {gap.get('reason')}")
    for limitation in quality.get("known_limitations") or []:lines.append(f"- Known limitation: {_text(limitation,['statement','description','reason'])}")
    for problem in quality.get("known_problems") or []:lines.append(f"- Known problem: {_text(problem,['statement','description','reason'])}")
    for item in control.get("known_issues") or []:lines.append(f"- Known issue {item.get('id')}: {item.get('summary')} — revisit when: {item.get('revisit_when') or 'explicitly scheduled'}.")
    recon=(o.get("roadmap") or {}).get("last_reconciliation") or {};pb=progress.get("progress_basis") or {};lines += ["","## Roadmap and progress",f"Roadmap: **{roadmap.get('title') or roadmap.get('id') or 'current roadmap'}**, revision **{roadmap.get('revision') or 'unknown'}**.",f"Progress basis: **{pb.get('id') or 'unknown'}** on roadmap revision **{pb.get('roadmap_revision') or roadmap.get('revision') or 'unknown'}**.",f"Current phase progress: **{_pct(progress.get('phase_percent'))}**; current work-package progress: **{_pct(progress.get('work_package_percent'))}**; active execution-package progress: **{_pct(progress.get('ep_percent'))}**."]
    if recon:lines.append(f"Last checkpoint roadmap reconciliation: **{str(recon.get('result') or 'recorded').replace('_',' ').title()}**.")
    lines += ["","## Delivery"]
    if delivery.get("applicability")=="NOT_APPLICABLE":
        lines.append("- No pull-request delivery vehicle is currently required.")
    else:
        vehicle=delivery.get("vehicle") or {}
        if vehicle:
            number=vehicle.get("number");url=vehicle.get("url");lifecycle=str(vehicle.get("lifecycle") or "UNKNOWN").replace("_"," ").title()
            label=f"PR #{number}" if number is not None else "Current pull request"
            suffix=f" — {url}" if url else ""
            lines.append(f"- {label}: **{lifecycle}**{suffix}")
            head=vehicle.get("head") or {};base=vehicle.get("base") or {}
            lines.append(f"- Head: `{head.get('ref') or 'unknown'}` @ `{head.get('sha') or 'unknown'}`; base: `{base.get('ref') or 'unknown'}`.")
        else:lines.append("- Current PR identity/head is unknown; provider readback is missing.")
        checks=(delivery.get("checks") or {}).get("state") or "UNKNOWN"
        merge=(delivery.get("mergeability") or {}).get("state") or "UNKNOWN"
        review=(delivery.get("review") or {}).get("state") or "UNKNOWN"
        ready=(delivery.get("ready_for_review") or {}).get("state") or "UNKNOWN"
        technical=(delivery.get("technical_ready_to_merge") or {}).get("state") or "UNKNOWN"
        authorization=(delivery.get("merge_authorization") or {}).get("state") or "UNKNOWN"
        lines.append(f"- Exact-head checks: **{str(checks).replace('_',' ').title()}**; mergeability: **{str(merge).replace('_',' ').title()}**; review state: **{str(review).replace('_',' ').title()}**.")
        lines.append(f"- Ready for review: **{ready}**; technically ready to merge: **{technical}**; merge authorization: **{str(authorization).replace('_',' ').title()}**.")
        boundary_blockers=control.get("boundary_blockers") or {}
        if boundary_blockers.get("PR_READY"):
            lines.append(f"- PR-ready is blocked by pending controls: {', '.join(str(x) for x in boundary_blockers.get('PR_READY') or [])}.")
        if boundary_blockers.get("MERGE"):
            lines.append(f"- Merge is blocked by pending controls: {', '.join(str(x) for x in boundary_blockers.get('MERGE') or [])}.")
        for reason in (delivery.get("technical_ready_to_merge") or {}).get("reasons") or []:lines.append(f"  - Technical readiness: {reason}")
        auth_reason=(delivery.get("merge_authorization") or {}).get("reason")
        if auth_reason:lines.append(f"  - Authorization: {auth_reason}")
        carried=delivery.get("unmerged_prs") or []
        lines.append("- Unmerged PRs carried forward:")
        if not carried:
            lines.append("  - none")
        for item in carried:
            v=item.get("vehicle") or {};num=v.get("number");url=v.get("url");life=str(v.get("lifecycle") or "UNKNOWN").replace("_"," ").title()
            head=(v.get("head") or {}).get("sha") or "unknown"
            lines.append(f"  - PR #{num if num is not None else 'unknown'} — **{life}** — head `{head}`{f' — {url}' if url else ''}")
            correlations=item.get("correlations") or []
            if correlations:
                for row in correlations:
                    lines.append(f"    - Issue #{row.get('issue_number')} ↔ {row.get('ep_id')} / {row.get('work_package')} — {row.get('relationship')}: {row.get('meaning')}")
            else:
                lines.append("    - Issue↔EP description correlation is not available.")
    actions=o.get("external_actions") or [];lines += ["","## Action required outside this environment"]
    if actions:
        for idx,item in enumerate(actions,1):
            env=item.get("environment") or {};lines.append(f"{idx}. {item.get('action')}")
            lines.append(f"   - Environment: {env.get('description') or env.get('kind') or 'specified external environment'}")
            if item.get("command"):lines.append(f"   - Command: `{item.get('command')}`")
            elif item.get("instruction"):lines.append(f"   - Instruction: {item.get('instruction')}")
            lines.append(f"   - Working location: {item.get('working_directory')}")
            lines.append(f"   - Why it cannot run here: {item.get('unavailable_here_reason')}")
            lines.append(f"   - Evidence produced: {', '.join(str(x) for x in (item.get('expected_evidence') or []))}")
            lines.append(f"   - Currently prevents: {', '.join(str(x) for x in (item.get('blocks') or []))}")
            lines.append(f"   - Success condition: {item.get('success_condition')}")
            lines.append(f"   - Success clears: {', '.join(str(x) for x in (item.get('clears') or []))}")
            delegation=item.get("delegation") or {}
            if delegation:
                publication=delegation.get("publication") or {};check=delegation.get("response_check") or {}
                method=str(publication.get("method") or "COMMENT").replace("_"," ").title()
                lines.append(f"   - Local-agent handoff: publish as **{method}** on the current work issue; local result returns to the same location; provider readback required.")
                lines.append(f"   - Response check: create timer **{check.get('timer_title')}** for {check.get('after_minutes')} minutes — {check.get('selection_reason')}")
                lines.append(f"   - When timer is due: {check.get('on_due')}")
                lines.append("   - Timer role: **read-only monitor**. It must not create a new candidate, DISC/QUAL/TC cycle, product write, or recursive delegation.")
                lines.append(f"   - If no response: {check.get('on_no_response')}")
                lines.append("   - Copy-paste prompt for the local agent:")
                for row in str(delegation.get("prompt") or "").splitlines():
                    lines.append(f"     {row}")
    else:lines.append("- No action outside the current environment is presently required.")
    decisions=o.get("decisions") or {};required=decisions.get("required_now") or [];lines += ["","## Owner decisions"]
    if required:
        for item in required:lines.append(f"- {item.get('reason')}")
    else:lines.append("- No Owner decision is currently required to continue the already-authorized slice.")
    lines += ["","## Recommended forward sequence"]
    steps=(o.get("next_work") or {}).get("steps") or []
    if steps:
        for idx,step in enumerate(steps,1):
            lane=f" ({step.get('lane_id')})" if step.get("lane_id") else "";lines.append(f"{idx}. {step.get('action')}{lane} → {step.get('expected_result')}")
    else:lines.append("- No active material next step is authorized; do not invent work.")
    lines += ["","## Roadmap revision history"]
    revisions=[e for e in events if isinstance(e,dict) and (e.get("event_class")=="ROADMAP_REVISION" or (e.get("roadmap_revision") or {}).get("id"))]
    if revisions:
        for e in revisions[-5:]:
            rr=e.get("roadmap_revision") or {}
            lines.append(f"- {rr.get('id') or e.get('id')}: {e.get('summary')}")
    else:lines.append(f"- Current revision {roadmap.get('revision') or 'unknown'}; no additional revision event is present in the recent event window.")
    lines += ["","## What would stop progress"]
    active_stop=cap.get("active_stop")
    if active_stop:lines.append(f"- Current stop: {active_stop.get('reason') or active_stop.get('category')}")
    boundary_blockers=control.get("boundary_blockers") or {}
    for boundary,ids in boundary_blockers.items():
        if ids:lines.append(f"- Pending controls {', '.join(str(x) for x in ids)} must resolve before {str(boundary).replace('_',' ').title()}.")
    stop_conditions=o.get("stop_conditions") or []
    if stop_conditions:
        for condition in stop_conditions:lines.append(f"- {condition}")
    elif not active_stop:lines.append("- No additional current stop condition is recorded beyond the active work contract.")
    return "\n".join(lines)+"\n"


def render(root:Path)->str:
    return render_projection(build(root))


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
