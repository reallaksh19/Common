#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml

def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=s["current_position"];a=s["active_ep"];g=s["progress"]
    return "\n".join(["# Relay status","",f"Roadmap: `{s['roadmap']['id']}` / `{s['roadmap']['revision']}`",f"Position: `{p['objective']}` → `{p['phase']}` → `{p['work_package']}`",f"Active EP: `{a['id']}` ({a['state']})",f"Progress: overall {g['overall_percent']}% | phase {g['phase_percent']}% | EP {g['ep_percent']}%",f"Execution: `{s['execution_policy']['mode']}`","Conversation context required: **NO**",""])
def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();print(render(Path(a.repo_root).resolve()),end="")
if __name__=="__main__":main()
