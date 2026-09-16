#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import print_result
from qualitylib import BLUEPRINTS

SECTIONS=("WHEN TO APPLY","REQUIRED INPUTS","PROCEDURE","BEST-PRACTICE CHECKLIST","ANTI-PATTERNS","REQUIRED ARTIFACTS","VERIFICATION","QUALITY FINDING CLASSIFICATION","TRUE HARD-STOP CONDITIONS","OWNER REPORT","SUCCESSOR HANDOVER")

def validate(root:Path):
    e=[];w=[];base=Path(__file__).resolve().parents[1]/"blueprints"
    for name in BLUEPRINTS:
        p=base/f"{name}.md"
        if not p.exists():e.append(f"quality blueprint missing: {name}");continue
        text=p.read_text(encoding="utf-8")
        for sec in SECTIONS:
            marker=f"## {sec}"
            if marker not in text:e.append(f"blueprint {name} missing section {sec}")
        if len(text)<1200:e.append(f"blueprint {name} is too thin to be a procedural contract")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args();e,w=validate(Path(a.repo_root).resolve());raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
