#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml
from report_projection import build

def label(v):return str(v or "UNKNOWN").replace("_"," ").title()
def fmt(v):return "NA" if v is None else f"{v:g}%" if isinstance(v,(int,float)) else str(v)
def render(root:Path):
    r=build(root);s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=r["progress"];cur=p.get("current") or {};ex=r.get("execution") or {};q=r.get("quality") or {};ev=r.get("evidence") or {};st=r.get("stop") or {};proj=r.get("projection") or {};ready=r.get("relay_readiness") or {}
    hard="None" if not st.get("active") else f"{label(st.get('category'))}: {st.get('reason','')}"
    lines=["# Relay status","",f"Relay lifecycle: **{label(r.get('relay_state'))}**",f"Roadmap: `{s['roadmap']['id']}` / `{s['roadmap']['revision']}`",f"Position: `{cur.get('objective')}` → `{cur.get('phase')}` → `{cur.get('work_package')}`",f"Progress: overall {fmt(p.get('overall_percent'))} | phase {fmt(cur.get('phase_percent'))} | work package {fmt(cur.get('work_package_percent'))} | EP {fmt(cur.get('ep_percent'))}",f"Execution policy: `{(s.get('execution_policy') or {}).get('mode')}`"]
    if s.get("relay_state")=="PARALLEL":
        pp=(s.get("execution_policy") or {}).get("parallel_plan");plan=load_yaml(root/pp);lines.append(f"Parallel plan: `{plan.get('id')}`")
        for lane in plan.get("lanes",[]) or []:lines.append(f"- {lane.get('id')}: `{lane.get('work_package')}` → `{lane.get('ep_id')}` on `{lane.get('branch')}`")
        lines.append(f"Integration: `{(plan.get('integration') or {}).get('work_package')}` after all lanes")
    else:lines.append(f"Active EP: `{(s.get('active_ep') or {}).get('id')}` ({(s.get('active_ep') or {}).get('state')})")
    if (s.get("predecessor_join") or {}).get("id"):lines.append(f"Parallel join predecessor: `{s['predecessor_join']['id']}`")
    if (s.get("predecessor_replan") or {}).get("id"):lines.append(f"Parallel replan predecessor: `{s['predecessor_replan']['id']}`")
    lines += [f"Execution state: **{label(ex.get('state'))}** | Can continue: **{'YES' if ex.get('can_continue') else 'NO'}** | Material authority: **{label(ex.get('material_authority'))}**",f"Quality: **{label(q.get('state'))}**",f"Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}",f"Hard stop: **{hard}**",f"Projection: **{label(proj.get('state'))}** | Required: **{'YES' if proj.get('required') else 'NO'}**",f"Baton ready for a replacement: **{'YES' if ready.get('baton_ready') else 'NO'}**",f"Certified takeover routes: **{len(r.get('takeover_admissions') or [])}**",f"Projection ready: **{'YES' if ready.get('projection_ready') else 'NO'}**",f"Handover ready: **{'YES' if ready.get('handover_ready') else 'NO'}**","Material write readiness: **RUNTIME CHECK REQUIRED PER CANDIDATE/ROUTE**","","## Ordered next work"]
    nw=r.get("next_work") or {}
    if nw.get("steps"):
        for step in nw["steps"]:lines.append(f"{step.get('order')}. {step.get('action')} → {step.get('expected_result')}")
    elif r.get("parallel_lanes"):
        for lane in r["parallel_lanes"]:
            lines.append(f"- {lane.get('lane_id')} / {lane.get('ep_id')}")
            for step in (lane.get("next_work") or {}).get("steps",[]) or []:lines.append(f"  {step.get('order')}. {step.get('action')}")
    else:lines.append("- No active material next-work contract.")
    lines+=["","Conversation context required: **NO**",""]
    return "\n".join(lines)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();print(render(Path(a.repo_root).resolve()),end="")
if __name__=="__main__":main()
