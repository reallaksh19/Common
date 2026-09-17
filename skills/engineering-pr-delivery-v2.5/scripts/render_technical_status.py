#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from communication_projection import build


def _label(v):return str(v or "UNKNOWN").replace("_"," ").title()
def _pct(v):return "NA" if v is None else f"{v:g}%" if isinstance(v,(int,float)) else str(v)

def render(root:Path)->str:
    c=build(root);r=(c.get("technical") or {}).get("report") or {};src=(c.get("generated_from") or {}).get("report_sources") or {};p=r.get("progress") or {};cur=p.get("current") or {};ex=r.get("execution") or {};ev=r.get("evidence") or {};q=r.get("quality") or {};st=r.get("stop") or {};ready=r.get("relay_readiness") or {};contract=r.get("active_contract") or {};scope=contract.get("scope") or {};cp=r.get("checkpoint") or {};qrv=cp.get("quality_review") or {}
    lines=["# Technical status","",f"Report projection digest: `{(c.get('generated_from') or {}).get('report_projection_digest')}`",f"Roadmap revision: `{src.get('roadmap_revision')}` | Progress basis: `{src.get('progress_basis')}`",f"Relay lifecycle: **{_label(r.get('relay_state'))}**",f"Current position: `{cur.get('objective')}` → `{cur.get('phase')}` → `{cur.get('work_package')}` → `{cur.get('ep_id') or 'NONE'}`",f"Progress: overall {_pct(p.get('overall_percent'))} | phase {_pct(cur.get('phase_percent'))} | work package {_pct(cur.get('work_package_percent'))} | EP {_pct(cur.get('ep_percent'))}","", "## Execution and readiness",f"- State: **{_label(ex.get('state'))}**; can continue: **{'YES' if ex.get('can_continue') else 'NO'}**; material authority: **{_label(ex.get('material_authority'))}**",f"- Stop: **{'ACTIVE' if st.get('active') else 'NONE'}** — {st.get('category') or 'NONE'} {st.get('reason') or ''}".rstrip(),f"- Baton ready: **{'YES' if ready.get('baton_ready') else 'NO'}**; projection ready: **{'YES' if ready.get('projection_ready') else 'NO'}**; handover ready: **{'YES' if ready.get('handover_ready') else 'NO'}**",f"- Certified takeover admissions: **{len(r.get('takeover_admissions') or [])}**",f"- External projection: **{_label((r.get('projection') or {}).get('state'))}**"]
    lines += ["","## Evidence and quality",f"- Evidence: **{_label(ev.get('state'))}** — {ev.get('summary') or ''}",f"- Quality state: **{_label(q.get('state'))}**"]
    if ev.get("not_run"):
        for item in ev["not_run"]:lines.append(f"- NOT_RUN `{item.get('id')}`: {item.get('reason')} ({item.get('cause')})")
    if qrv:
        lines.append(f"- Checkpoint quality review: `{qrv.get('id')}` — **{_label(qrv.get('overall_state'))}**; blocks execution: **{'YES' if (qrv.get('execution_effect') or {}).get('blocks_execution') else 'NO'}**")
        for finding in qrv.get("findings",[]) or []:lines.append(f"  - `{finding.get('id')}` {finding.get('classification')}/{finding.get('severity')}/{finding.get('disposition')}: {finding.get('statement')}")
    lines += ["","## Current contract scope"]
    for key in ("allowed","protected","prohibited","owner_reserved"):
        lines.append(f"### {key.replace('_',' ').title()}")
        vals=scope.get(key) or []
        if not vals:lines.append("- none")
        for item in vals:
            if isinstance(item,dict):
                subject=item.get("path") or item.get("domain") or item.get("invariant") or item.get("decision");lines.append(f"- {subject}: {item.get('reason') or ''}".rstrip())
            else:lines.append(f"- {item}")
    lines += ["","## Owner-decision records"]
    records=r.get("owner_decisions") or []
    if not records:lines.append("- none")
    for item in records:lines.append(f"- `{item.get('id')}` {item.get('status')}/{item.get('kind')}: {item.get('statement')}; requirement={item.get('requirement_disposition')}; pending={item.get('pending_items') or []}")
    lines += ["","## Exact next work"]
    steps=((r.get("next_work") or {}).get("steps") or [])
    if steps:
        for step in steps:lines.append(f"{step.get('order')}. {step.get('action')} | targets={step.get('targets') or []} | inputs={step.get('inputs') or []} | tests={step.get('tests') or []} | benchmarks={step.get('benchmarks') or []} | acceptance={step.get('acceptance') or []} | expected={step.get('expected_result')} | stop_if={step.get('stop_if') or []}")
    elif r.get("parallel_lanes"):
        for lane in r["parallel_lanes"]:
            lines.append(f"- Lane `{lane.get('lane_id')}` / `{lane.get('ep_id')}`")
            for step in (lane.get("next_work") or {}).get("steps",[]) or []:lines.append(f"  {step.get('order')}. {step.get('action')} → {step.get('expected_result')}")
    else:lines.append("- No active material next-work contract.")
    lines += ["","## Source bindings"]
    for key,value in src.items():lines.append(f"- {key}: `{value}`")
    return "\n".join(lines)+"\n"


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
