#!/usr/bin/env python3
"""Read-only generic V2.5 stress runner for one or more repository roots."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from cold_start_check import validate as cold_start
from validate_relay_conformance import validate as relay

def run(root:Path):
    relay_errors,relay_warnings=relay(root);cold_errors,cold_warnings=cold_start(root)
    return {"repo_root":str(root),"relay_conformance":{"pass":not relay_errors,"errors":relay_errors,"warnings":relay_warnings},"cold_start":{"pass":not cold_errors,"errors":cold_errors,"warnings":cold_warnings},"pass":not relay_errors and not cold_errors}

def main():
    ap=argparse.ArgumentParser(description="Run repository-agnostic V2.5 relay stress validation without mutating targets.");ap.add_argument("repo_roots",nargs="+");ap.add_argument("--json",action="store_true");a=ap.parse_args();results=[run(Path(x).resolve()) for x in a.repo_roots]
    if a.json:print(json.dumps({"results":results},indent=2))
    else:
        for result in results:
            print(f"{'PASS' if result['pass'] else 'FAIL'} {result['repo_root']}")
            for section in ("relay_conformance","cold_start"):
                for warning in result[section]["warnings"]:print(f"  WARN {section}: {warning}")
                for error in result[section]["errors"]:print(f"  FAIL {section}: {error}")
    raise SystemExit(0 if all(x["pass"] for x in results) else 1)
if __name__=="__main__":main()
