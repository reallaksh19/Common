#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result,require


def _text(value)->bool:
    return isinstance(value,str) and bool(value.strip()) and not (value.strip().startswith("<") and value.strip().endswith(">"))


def validate(root:Path):
    e=[];w=[];path=root/"agents/relay/REPO_PROFILE.yaml"
    if not path.exists():return ["REPO_PROFILE.yaml is required for deterministic repository discovery"],w
    profile=load_yaml(path)
    e+=require(profile,["schema_version","repository_type","default_branch","important_paths","commands"],"REPO_PROFILE")
    if profile.get("schema_version")!="relay-v2.5":e.append("REPO_PROFILE.schema_version must be relay-v2.5")
    if not _text(profile.get("repository_type")):e.append("REPO_PROFILE.repository_type must be explicit non-placeholder text")
    if not _text(profile.get("default_branch")):e.append("REPO_PROFILE.default_branch must be explicit non-placeholder text")
    important=profile.get("important_paths")
    if not isinstance(important,dict):e.append("REPO_PROFILE.important_paths must be a mapping")
    else:
        for key,value in important.items():
            if not isinstance(value,list):e.append(f"REPO_PROFILE.important_paths.{key} must be a list")
            elif any(not _text(x) for x in value):e.append(f"REPO_PROFILE.important_paths.{key} contains empty/placeholder path")
    commands=profile.get("commands")
    if not isinstance(commands,dict):e.append("REPO_PROFILE.commands must be a mapping")
    else:
        for key,value in commands.items():
            if not isinstance(value,str):e.append(f"REPO_PROFILE.commands.{key} must be a string; empty is allowed when unavailable")
    for key in ("protected_domains","generated_paths","repository_rules"):
        value=profile.get(key,[])
        if not isinstance(value,list):e.append(f"REPO_PROFILE.{key} must be a list")
        elif any(not isinstance(x,(str,dict)) for x in value):e.append(f"REPO_PROFILE.{key} entries must be strings or mappings")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
