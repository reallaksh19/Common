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


def render(root:Path)->str:
    c=build(root);o=c["owner"];cap=o["capability"];progress=(o.get("roadmap") or {}).get("progress") or {};roadmap=(o.get("roadmap") or {}).get("summary") or {}
    lines=["# Owner status","","## What can happen now",f"{cap.get('summary')}",f"Overall progress: **{_pct(progress.get('overall_percent'))}**."]
    phase=progress.get("phase_title") or progress.get("phase");wp=progress.get("work_package_title") or progress.get("work_package")
    if phase or wp:lines.append(f"Current roadmap position: **{phase or 'current phase'}** → **{wp or 'current work package'}**.")
    current=o.get("current_work") or {};purpose=o.get("purpose") or {};lines += ["","## What this work is for"]
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
    recon=(o.get("roadmap") or {}).get("last_reconciliation") or {};lines += ["","## Roadmap and progress",f"Roadmap: **{roadmap.get('title') or roadmap.get('id') or 'current roadmap'}**, revision **{roadmap.get('revision') or 'unknown'}**.",f"Current phase progress: **{_pct(progress.get('phase_percent'))}**; current work-package progress: **{_pct(progress.get('work_package_percent'))}**; active execution-package progress: **{_pct(progress.get('ep_percent'))}**."]
    if recon:lines.append(f"Last checkpoint roadmap reconciliation: **{str(recon.get('result') or 'recorded').replace('_',' ').title()}**.")
    decisions=o.get("decisions") or {};required=decisions.get("required_now") or [];lines += ["","## Decisions for you"]
    if required:
        for item in required:lines.append(f"- {item.get('reason')}")
    else:lines.append("- No Owner decision is currently required to continue the already-authorized slice.")
    lines += ["","## What happens next"]
    steps=(o.get("next_work") or {}).get("steps") or []
    if steps:
        for idx,step in enumerate(steps,1):
            lane=f" ({step.get('lane_id')})" if step.get("lane_id") else "";lines.append(f"{idx}. {step.get('action')}{lane} → {step.get('expected_result')}")
    else:lines.append("- No active material next step is authorized; do not invent work.")
    lines += ["","## What would stop progress"]
    active_stop=cap.get("active_stop")
    if active_stop:lines.append(f"- Current stop: {active_stop.get('reason') or active_stop.get('category')}")
    stop_conditions=o.get("stop_conditions") or []
    if stop_conditions:
        for condition in stop_conditions:lines.append(f"- {condition}")
    elif not active_stop:lines.append("- No additional current stop condition is recorded beyond the active work contract.")
    return "\n".join(lines)+"\n"


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
