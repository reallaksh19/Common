#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml
from report_projection import build

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args();data=build(Path(a.repo_root).resolve());text=yaml.safe_dump(data,sort_keys=False)
    if a.output:Path(a.output).write_text(text,encoding="utf-8")
    else:print(text,end="")
if __name__=="__main__":main()
