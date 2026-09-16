#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml

def label(value):return str(value or "UNKNOWN").replace("_"," ").title()
def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=s["current_position"];a=s["active_ep"];g=s["progress"];planes=s.get("status_planes") or {};ex=planes.get("execution") or {};q=planes.get("quality") or {};ev=planes.get("evidence") or {};st=planes.get("stop") or {};relay_state=s.get("relay_state");projection=s.get("projection") or {};ready=s.get("relay_readiness") or {};join=s.get("predecessor_join") or {};replan=s.get("predecessor_replan") or {};admissions=s.get("takeover_admissions") or []
    hard="None" if not st.get("active") else f"{label(st.get('category'))}: {st.get('reason','')}"
    lines=["# Relay status","",f"Relay lifecycle: **{label(relay_state)}**",f"Roadmap: `{s['roadmap']['id']}` / `{s['roadmap']['revision']}`",f"Position: `{p['objective']}` → `{p['phase']}` → `{p['work_package']}`",f"Progress: overall {g['overall_percent']}% | phase {g['phase_percent']}% | EP {g['ep_percent']}%",f"Execution policy: `{s['execution_policy']['mode']}`"]
    if relay_state=="PARALLEL":
        plan=load_yaml(root/(s.get("execution_policy") or {})["parallel_plan"]);lines.append(f"Parallel plan: `{plan.get('id')}`")
        for lane in plan.get("lanes",[]) or []:lines.append(f"- {lane.get('id')}: `{lane.get('work_package')}` → `{lane.get('ep_id')}` on `{lane.get('branch')}`")
        lines.append(f"Integration: `{(plan.get('integration') or {}).get('work_package')}` after all lanes")
    else:
        lines.append(f"Active EP: `{a.get('id')}` ({a.get('state')})")
        if a.get("continuity_receipt"):
            receipt=load_yaml(root/a["continuity_receipt"]);lines.append(f"Roadmap continuity: `{receipt.get('id')}` — **{label(receipt.get('disposition'))}** (`{receipt.get('from_revision')}` → `{receipt.get('to_revision')}`)")
        if join.get("id"):lines.append(f"Parallel join predecessor: `{join.get('id')}`")
    if replan.get("id"):lines.append(f"Parallel replan predecessor: `{replan.get('id')}`")
    lines += [f"Execution state: **{label(ex.get('state'))}** | Can continue: **{'YES' if ex.get('can_continue') else 'NO'}** | Material authority: **{label(ex.get('material_authority'))}**",f"Quality: **{label(q.get('state'))}**",f"Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}",f"Hard stop: **{hard}**",f"Projection: **{label(projection.get('state'))}** | Required: **{'YES' if projection.get('required') else 'NO'}**",f"Baton ready for a replacement: **{'YES' if ready.get('baton_ready') else 'NO'}**",f"Certified takeover routes: **{len(admissions)}**",f"Projection ready: **{'YES' if ready.get('projection_ready') else 'NO'}**",f"Handover ready: **{'YES' if ready.get('handover_ready') else 'NO'}**",f"Material write readiness: **RUNTIME CHECK REQUIRED PER CANDIDATE/ROUTE**",f"Exact next action: {ex.get('next_action','')}","Conversation context required: **NO**",""]
    for item in admissions:
        if isinstance(item,dict):lines.append(f"Certified admission: `{item.get('route_key')}` → `{(item.get('candidate') or {}).get('agent_instance_id')}` / `{(item.get('certification') or {}).get('id')}`")
    return "\n".join(lines)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();print(render(Path(a.repo_root).resolve()),end="")
if __name__=="__main__":main()
