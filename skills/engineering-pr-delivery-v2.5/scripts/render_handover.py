#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import index_roadmap,load_yaml

def mark(state):return "[x]" if state=="COMPLETE" else "[~]" if state=="ACTIVE" else "[ ]"
def label(value):return str(value or "UNKNOWN").replace("_"," ").title()
def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);_,phases,_=index_roadmap(r);cur=s["current_position"];phase=phases[cur["phase"]][1];planes=s.get("status_planes") or {};ex=planes.get("execution") or {};q=planes.get("quality") or {};ev=planes.get("evidence") or {};st=planes.get("stop") or {};active=s.get("active_ep") or {};relay_state=s.get("relay_state");projection=s.get("projection") or {};ready=s.get("relay_readiness") or {};join_ref=s.get("predecessor_join") or {};replan_ref=s.get("predecessor_replan") or {};admissions=s.get("takeover_admissions") or []
    ep=None;plan=None;join=None;replan=None;continuity=None
    if relay_state=="ACTIVE":ep=load_yaml(root/active["path"])
    elif relay_state=="PARALLEL":plan=load_yaml(root/(s.get("execution_policy") or {})["parallel_plan"])
    if join_ref.get("path"):join=load_yaml(root/join_ref["path"])
    if replan_ref.get("path"):replan=load_yaml(root/replan_ref["path"])
    if active.get("continuity_receipt"):continuity=load_yaml(root/active["continuity_receipt"])
    current_ep=(f"{active.get('id')} — {s['progress']['ep_percent']}%" if relay_state=="ACTIVE" else "PARALLEL ROUTER" if relay_state=="PARALLEL" else "NONE")
    lines=["# Engineering relay","",f"Relay lifecycle: **{label(relay_state)}**",f"Overall roadmap: **{s['progress']['overall_percent']}%**",f"Current phase: **{cur['phase']} — {phase.get('title','')} — {s['progress']['phase_percent']}%**",f"Current work package: **{cur['work_package']}**",f"Current EP: **{current_ep}**","","## Status",f"- Execution: **{label(ex.get('state'))}**; can continue: **{'YES' if ex.get('can_continue') else 'NO'}**; material authority: **{label(ex.get('material_authority'))}**",f"- Quality: **{label(q.get('state'))}**",f"- Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}",f"- Hard stop: **{'NONE' if not st.get('active') else label(st.get('category'))}**",f"- Projection: **{label(projection.get('state'))}**; required: **{'YES' if projection.get('required') else 'NO'}**",f"- Exact next action: {ex.get('next_action','')}","","## Overall roadmap"]
    for obj in r.get("objectives",[]) or []:
        lines.append(f"- {obj.get('title')} ({obj.get('state')})")
        for ph in obj.get("phases",[]) or []:lines.append(f"  - {mark(ph.get('state'))} {ph.get('id')} — {ph.get('title')}")
    if continuity is not None:
        lines+=["",f"## Roadmap continuity {continuity.get('id')}",f"- EP `{continuity.get('ep_id')}` / WP `{continuity.get('work_package')}`: **{label(continuity.get('disposition'))}**",f"- Covered roadmap revisions: `{continuity.get('from_revision')}` → `{continuity.get('to_revision')}`",f"- Revision records checked: **{len(continuity.get('revision_chain') or [])}**"]
        impacts=continuity.get("impact_checks") or {};changed=[k for k,v in impacts.items() if v]
        lines.append(f"- Contract impacts requiring reconciliation: {', '.join(changed) if changed else 'none'}")
    if replan is not None:
        lines+=["",f"## Parallel replan {replan.get('id')}"]
        trigger=replan.get("trigger") or {};lines.append(f"- Trigger: {label(trigger.get('type'))}; lane `{trigger.get('lane_id')}` — {trigger.get('reason','')}")
        for item in replan.get("lane_dispositions",[]) or []:
            if item.get("disposition")=="COMPLETE":detail=f"checkpoint `{(item.get('checkpoint') or {}).get('id')}`"
            else:
                targets=[str(x.get("work_package")) for x in (item.get("transfers") or []) if isinstance(x,dict) and x.get("work_package")]
                detail="transfer → "+(", ".join(f"`{x}`" for x in targets) if targets else "NONE")
            lines.append(f"- {item.get('lane_id')}: `{item.get('work_package')}` — **{label(item.get('disposition'))}**; {detail}")
        route=replan.get("successor_route") or {};lines.append(f"- Recomputed route: **{label(route.get('mode'))}** → `{route.get('work_package') or route.get('parallel_plan_id') or 'NONE'}`")
    if ep is not None:
        if join is not None:
            lines+=["",f"## Parallel convergence {join.get('id')}"]
            for item in join.get("lane_checkpoints",[]) or []:lines.append(f"- {item.get('lane_id')}: `{item.get('work_package')}` → checkpoint `{item.get('checkpoint_id')}`")
            lines.append(f"- Integration frontier: `{(join.get('integration') or {}).get('work_package')}` → `{(join.get('integration') or {}).get('ep_id')}`")
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
    lines+=["","## Relay readiness",f"- Complete baton available for a zero-context replacement? **{'YES' if ready.get('baton_ready') else 'NO'}**",f"- Required projection synchronized? **{'YES' if ready.get('projection_ready') else 'NO'}**",f"- Full custody handover ready? **{'YES' if ready.get('handover_ready') else 'NO'}**",f"- Certified candidate routes: **{len(admissions)}**",f"- Material write readiness: **derived live per candidate/route; not persisted**",f"- Conversation context required? **{'NO' if s.get('chat_context_required') is False else 'YES'}**"]
    for item in admissions:
        if isinstance(item,dict):lines.append(f"- `{item.get('route_key')}` certified for `{(item.get('candidate') or {}).get('agent_instance_id')}` via `{(item.get('certification') or {}).get('id')}`")
    if ready.get("reasons"):lines.extend(f"- Readiness note: {x}" for x in ready.get("reasons"))
    if relay_state=="PARALLEL":lines.append("- Material lane selection must match the approved branch/worktree routing; ambiguity means no material execution.")
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
