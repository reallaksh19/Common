#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
from relaylib import load_yaml
from resolve_execution_route import resolve


def git(root:Path,*args):return subprocess.check_output(["git","-C",str(root),*args],text=True,stderr=subprocess.STDOUT).strip()


def inspect(root:Path,branch:str|None=None,worktree:str|None=None):
    route=resolve(root,branch,worktree)
    if not route.get("ep_path"):return {"status":"NO_ACTIVE_EP",**route}
    ep=load_yaml(root/route["ep_path"]);basis=ep.get("git_basis") or {}
    actual_branch=branch or git(root,"branch","--show-current")
    head=git(root,"rev-parse","HEAD")
    expected=basis.get("expected_branch") or (ep.get("identity") or {}).get("branch")
    if expected and actual_branch!=expected:raise ValueError(f"checked-out branch {actual_branch} != expected {expected}")
    material=basis.get("material_ref")
    if material:
        try:git(root,"merge-base","--is-ancestor",str(material),"HEAD")
        except subprocess.CalledProcessError:raise ValueError(f"material_ref {material} is not an ancestor of current HEAD {head}")
    base_branch=basis.get("base_branch");observed=basis.get("base_observed_ref")
    if not base_branch or not observed:raise ValueError("EP git_basis must define base_branch and base_observed_ref")
    current_base=git(root,"rev-parse",str(base_branch))
    if current_base==str(observed):
        return {"status":"PASS","branch":actual_branch,"head":head,"base_branch":base_branch,"base_observed_ref":observed,"current_base_ref":current_base,"base_drift":"UNCHANGED",**route}
    changed=[x for x in git(root,"diff","--name-only",f"{observed}..{current_base}").splitlines() if x]
    return {"status":"NEEDS_DRIFT_RECEIPT","branch":actual_branch,"head":head,"base_branch":base_branch,"base_observed_ref":observed,"current_base_ref":current_base,"changed_paths":changed,**route}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--branch");ap.add_argument("--worktree");a=ap.parse_args()
    try:out=inspect(Path(a.repo_root).resolve(),a.branch,a.worktree)
    except Exception as exc:print(json.dumps({"status":"FAIL","error":str(exc)},indent=2));raise SystemExit(1)
    print(json.dumps(out,indent=2));raise SystemExit(2 if out.get("status")=="NEEDS_DRIFT_RECEIPT" else 0)
if __name__=="__main__":main()
