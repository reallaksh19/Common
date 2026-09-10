#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True,type=Path); ap.add_argument('--out',required=True,type=Path); a=ap.parse_args()
    here=Path(__file__).resolve(); grade9=here.parents[3]
    validator=here.parent/'validate_math_research_input.py'
    builder=grade9/'Architecture'/'core1'/'build_research_package.py'
    subprocess.run([sys.executable,str(validator),str(a.input)],check=True)
    if not builder.exists(): raise SystemExit(f'Missing PR #160 Core (1) builder: {builder}')
    subprocess.run([sys.executable,str(builder),'--input',str(a.input),'--out',str(a.out)],check=True)
    return 0
if __name__=='__main__': raise SystemExit(main())
