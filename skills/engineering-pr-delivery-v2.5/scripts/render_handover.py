#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml
from report_projection import build

def label(v):return str(v or "UNKNOWN").replace("_"," ").title()
def pct(v):return "NA" if v is None else f"{v:g}%" if isinstance(v,(int,float)) else str(v)
def mark(v):return "[x]" if v in {"COMPLETE","TERMINAL"} else "[~]" if v in {"ACTIVE","IN_PROGRESS"} else "[ ]"
def render(root:Path):
    r=build(root);s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=r["progress"];cur=p.get("current") or {};ex=r.get("execution") or {};ev=r.get("evidence") or {};ready=r.get("relay_readiness") or {}
    lines=["# Engineering relay handover","",f"Overall: **{pct(p.get('overall_percent'))}**",f"Current phase: **{cur.get('phase')} — {pct(cur.get('phase_percent'))}**",f"Current work package: **{cur.get('work_package')} — {pct(cur.get('work_package_percent'))}**",f"Current EP: **{cur.get('ep_id') or 'NONE'} — {pct(cur.get('ep_percent'))}**","","## Overall checklist"]
    for obj in p.get("hierarchy",[]) or []:
        lines.append(f"- {mark(obj.get('state'))} {obj.get('id')} — {obj.get('title','')} — **{pct(obj.get('percent'))}**")
        for ph in obj.get("phases",[]) or []:
            lines.append(f"  - {mark(ph.get('state'))} {ph.get('id')} — {ph.get('title','')} — **{pct(ph.get('percent'))}**")
            for wp in ph.get("work_packages",[]) or []:
                lines.append(f"    - {mark(wp.get('state'))} {wp.get('id')} — {wp.get('title','')} — **{pct(wp.get('percent'))}**{' ← CURRENT' if wp.get('current') else ''}")
                for step in wp.get("steps",[]) or []:
                    st="COMPLETE" if step.get("percent")==100 else "ACTIVE" if (step.get("percent") or 0)>0 else "PLANNED"
                    lines.append(f"      - {mark(st)} {step.get('id')} — {step.get('objective','')} — **{pct(step.get('percent'))}**")
                    for ac in step.get("acceptance",[]) or []:lines.append(f"        - {mark(ac.get('status'))} {ac.get('id')} — {ac.get('description','')} — **{pct(ac.get('percent'))}** — {label(ac.get('status'))}")
    lines += ["","## Current execution",f"- State: **{label(ex.get('state'))}**; can continue: **{'YES' if ex.get('can_continue') else 'NO'}**; material authority: **{label(ex.get('material_authority'))}**",f"- Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}","","## Exact next work"]
    nw=r.get("next_work") or {}
    if nw.get("steps"):
        for step in nw["steps"]:
            lines.append(f"{step.get('order')}. **{step.get('action')}**")
            lines.append(f"   Targets: {', '.join(step.get('targets') or [])}; inputs: {', '.join(step.get('inputs') or []) or 'none'}")
            lines.append(f"   Tests: {', '.join(step.get('tests') or []) or 'none'}; benchmarks: {', '.join(step.get('benchmarks') or []) or 'none'}; acceptance: {', '.join(step.get('acceptance') or [])}")
            lines.append(f"   Expected: {step.get('expected_result')}; stop/reconcile if: {'; '.join(step.get('stop_if') or [])}")
    elif r.get("parallel_lanes"):
        for lane in r["parallel_lanes"]:
            lines.append(f"- {lane.get('lane_id')} / {lane.get('ep_id')} on `{lane.get('branch')}`")
            for step in (lane.get("next_work") or {}).get("steps",[]) or []:lines.append(f"  {step.get('order')}. {step.get('action')} → {step.get('expected_result')}")
    else:lines.append("- No active material next-work contract; do not invent work.")
    if ev.get("not_run"):
        lines += ["","## Evidence not run"]+[f"- {x.get('id')}: {x.get('reason')} ({x.get('cause')})" for x in ev.get("not_run")]
    lines += ["","## Relay readiness",f"- Baton ready: **{'YES' if ready.get('baton_ready') else 'NO'}**",f"- Projection ready: **{'YES' if ready.get('projection_ready') else 'NO'}**",f"- Handover ready: **{'YES' if ready.get('handover_ready') else 'NO'}**",f"- Conversation context required: **{'NO' if s.get('chat_context_required') is False else 'YES'}**"]
    return "\n".join(lines)+"\n"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
