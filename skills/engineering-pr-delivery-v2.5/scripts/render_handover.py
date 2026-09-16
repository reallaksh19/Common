#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import index_roadmap,load_yaml

def mark(state):return "[x]" if state=="COMPLETE" else "[~]" if state=="ACTIVE" else "[ ]"
def label(value):return str(value or "UNKNOWN").replace("_"," ").title()
def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);_,phases,_=index_roadmap(r);cur=s["current_position"];phase=phases[cur["phase"]][1];planes=s.get("status_planes") or {};ex=planes.get("execution") or {};q=planes.get("quality") or {};ev=planes.get("evidence") or {};st=planes.get("stop") or {};active=s.get("active_ep") or {};relay_state=s.get("relay_state");projection=s.get("projection") or {};ready=s.get("relay_readiness") or {}
    ep=None;plan=None
    if relay_state=="ACTIVE":ep=load_yaml(root/active["path"])
    elif relay_state=="PARALLEL":plan=load_yaml(root/(s.get("execution_policy") or {})["parallel_plan"])
    current_ep=(f"{active.get('id')} — {s['progress']['ep_percent']}%" if relay_state=="ACTIVE" else "PARALLEL ROUTER" if relay_state=="PARALLEL" else "NONE")
    lines=["# Engineering relay","",f"Relay lifecycle: **{label(relay_state)}**",f"Overall roadmap: **{s['progress']['overall_percent']}%**",f"Current phase: **{cur['phase']} — {phase.get('title','')} — {s['progress']['phase_percent']}%**",f"Current work package: **{cur['work_package']}**",f"Current EP: **{current_ep}**","","## Status",f"- Execution: **{label(ex.get('state'))}**; can continue: **{'YES' if ex.get('can_continue') else 'NO'}**",f"- Quality: **{label(q.get('state'))}**",f"- Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}",f"- Hard stop: **{'NONE' if not st.get('active') else label(st.get('category'))}**",f"- Projection: **{label(projection.get('state'))}**; required: **{'YES' if projection.get('required') else 'NO'}**",f"- Exact next action: {ex.get('next_action','')}","","## Overall roadmap"]
    for obj in r.get("objectives",[]) or []:
        lines.append(f"- {obj.get('title')} ({obj.get('state')})")
        for ph in obj.get("phases",[]) or []:lines.append(f"  - {mark(ph.get('state'))} {ph.get('id')} — {ph.get('title')}")
    if ep is not None:
        lines+=["","## Current EP acceptance"]
        for ac in ep.get("acceptance",[]) or []:lines.append(f"- [ ] {ac.get('id')} — {ac.get('description')}")
    elif plan is not None:
        lines+=["",f"## Parallel plan {plan.get('id')}"]
        for lane in plan.get("lanes",[]) or []:
            lane_ep=load_yaml(root/lane["ep_path"]);lines.append(f"- {lane.get('id')}: `{lane.get('work_package')}` → `{lane.get('ep_id')}` on `{lane.get('branch')}`")
            for ac in lane_ep.get("acceptance",[]) or []:lines.append(f"  - [ ] {ac.get('id')} — {ac.get('description')}")
        integration=plan.get("integration") or {};lines.append(f"- Integration after lanes: `{integration.get('work_package')}`; planned EP `{integration.get('planned_ep_id')}`")
    else:
        lines+=["","## Current EP","- No active material EP. Follow the lifecycle/status next action rather than inventing work."]
    if q.get("findings"):lines+=["","## Quality findings",*[f"- {x}" for x in q.get("findings")]]
    if ev.get("not_run"):lines+=["","## Evidence not run",*[f"- {x.get('id')}: {x.get('reason')} ({x.get('cause')})" for x in ev.get("not_run")]]
    lines+=["","## Relay readiness",f"- Repository recovery ready? **{'YES' if ready.get('repository_ready') else 'NO'}**",f"- Required projection synchronized? **{'YES' if ready.get('projection_ready') else 'NO'}**",f"- Full custody handover ready? **{'YES' if ready.get('handover_ready') else 'NO'}**",f"- Conversation context required? **{'NO' if s.get('chat_context_required') is False else 'YES'}**"]
    if ready.get("reasons"):lines.extend(f"- Readiness note: {x}" for x in ready.get("reasons"))
    if relay_state=="PARALLEL":lines.append("- Material lane selection must match the approved branch/worktree routing; ambiguity means no material execution.")
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
