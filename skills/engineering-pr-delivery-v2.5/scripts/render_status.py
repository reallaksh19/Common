#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml

def label(value):return str(value or "UNKNOWN").replace("_"," ").title()
def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=s["current_position"];a=s["active_ep"];g=s["progress"];planes=s.get("status_planes") or {};ex=planes.get("execution") or {};q=planes.get("quality") or {};ev=planes.get("evidence") or {};st=planes.get("stop") or {}
    hard="None" if not st.get("active") else f"{label(st.get('category'))}: {st.get('reason','')}"
    return "\n".join(["# Relay status","",f"Roadmap: `{s['roadmap']['id']}` / `{s['roadmap']['revision']}`",f"Position: `{p['objective']}` → `{p['phase']}` → `{p['work_package']}`",f"Active EP: `{a['id']}` ({a['state']})",f"Progress: overall {g['overall_percent']}% | phase {g['phase_percent']}% | EP {g['ep_percent']}%",f"Execution policy: `{s['execution_policy']['mode']}`",f"Execution state: **{label(ex.get('state'))}** | Can continue: **{'YES' if ex.get('can_continue') else 'NO'}**",f"Quality: **{label(q.get('state'))}**",f"Evidence: **{label(ev.get('state'))}** — {ev.get('summary','')}",f"Hard stop: **{hard}**",f"Exact next action: {ex.get('next_action','')}","Conversation context required: **NO**",""])
def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();print(render(Path(a.repo_root).resolve()),end="")
if __name__=="__main__":main()
