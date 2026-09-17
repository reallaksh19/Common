#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml

def mark(state):return "[x]" if state=="COMPLETE" else "[~]" if state=="ACTIVE" else "[-]" if state in {"SUPERSEDED","CANCELLED"} else "[ ]"
def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);lines=[f"# {r['roadmap']['title']}","",f"Revision: `{r['roadmap']['revision']}`",f"Overall progress: **{s['progress']['overall_percent']}%**",""]
    for obj in r.get("objectives",[]) or []:
        lines.append(f"## {mark(obj.get('state'))} {obj.get('id')} — {obj.get('title')}")
        for ph in obj.get("phases",[]) or []:
            lines.append(f"- {mark(ph.get('state'))} {ph.get('id')} — {ph.get('title')} ({ph.get('definition')})")
            for wp in ph.get("work_packages",[]) or []:lines.append(f"  - {mark(wp.get('state'))} {wp.get('id')} — {wp.get('title')} [{wp.get('execution_status')}]")
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();text=render(Path(a.repo_root).resolve());Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")
if __name__=="__main__":main()
