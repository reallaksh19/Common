#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import index_roadmap,load_yaml

def mark(state):return "[x]" if state=="COMPLETE" else "[~]" if state=="ACTIVE" else "[ ]"
def label(value):return str(value or "UNKNOWN").replace("_"," ").title()
def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);ep=load_yaml(root/s["active_ep"]["path"]);_,phases,_=index_roadmap(r);cur=s["current_position"];phase=phases[cur["phase"]][1];planes=s.get("status_planes") or {};ex=planes.get("execution") or {};q=planes.get("quality") or {};ev=planes.get("evidence") or {};st=planes.get("stop") or {}
    lines=["# Engineering relay","",f"Overall roadmap: **{s['progress']['overall_percent']}%**",f"Current phase: **{cur['phase']} — {phase.get('title','')} — {s['progress']['phase_percent']}%**",f"Current work package: **{cur['work_package']}**",f"Current EP: **{s['active_ep']['id']} — {s['progress']['ep_percent']}%**","","## Status",f"- Execution: **{label(ex.get('state'))}**; can continue: **{'YES' if ex.get('can_continue') else 'NO'}**",f"- Quality: **{label(q.get('state'))}**",f"- Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}",f"- Hard stop: **{'NONE' if not st.get('active') else label(st.get('category'))}**",f"- Exact next action: {ex.get('next_action','')}","","## Overall roadmap"]
    for obj in r.get("objectives",[]) or []:
        lines.append(f"- {obj.get('title')} ({obj.get('state')})")
        for ph in obj.get("phases",[]) or []:lines.append(f"  - {mark(ph.get('state'))} {ph.get('id')} — {ph.get('title')}")
    lines+=["","## Current EP acceptance"]
    for ac in ep.get("acceptance",[]) or []:lines.append(f"- [ ] {ac.get('id')} — {ac.get('description')}")
    if q.get("findings"):lines+=["","## Quality findings",*[f"- {x}" for x in q.get("findings")]]
    if ev.get("not_run"):lines+=["","## Evidence not run",*[f"- {x.get('id')}: {x.get('reason')} ({x.get('cause')})" for x in ev.get("not_run")]]
    lines+=["","## Relay",f"- Can a replacement agent continue immediately? **{'YES' if s.get('chat_context_required') is False else 'NO'}**",f"- Conversation context required? **{'NO' if s.get('chat_context_required') is False else 'YES'}**"]
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
