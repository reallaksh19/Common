#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml, print_result
from validate_checkpoint import validate_file

NONE_IDS = {None, "", "NONE"}

def validate(root: Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml");last=s.get("last_checkpoint")
    if not isinstance(last,dict):return ["REPO_STATE.last_checkpoint must be a mapping"],w
    active=s.get("active_ep") or {};active_none=active.get("state")=="NONE"
    checkpoint_id=last.get("id");checkpoint_path=last.get("path")

    if checkpoint_id in NONE_IDS:
        if checkpoint_path not in {None,""}:e.append("last_checkpoint.path must be null/empty when last_checkpoint.id is NONE")
        if not active_none:
            ep=load_yaml(root/active["path"]);previous=(ep.get("identity") or {}).get("previous_checkpoint")
            if previous not in NONE_IDS:e.append("active EP previous_checkpoint must be NONE when repository has no last checkpoint")
        return e,w

    if not checkpoint_path:return ["last_checkpoint.path is required when last_checkpoint.id is set"],w
    path=root/checkpoint_path
    if not path.exists():return [f"last checkpoint file does not exist: {checkpoint_path}"],w
    ce,cw=validate_file(path);e.extend(f"checkpoint: {x}" for x in ce);w.extend(f"checkpoint: {x}" for x in cw);cp=load_yaml(path)
    if str(cp.get("checkpoint_id"))!=str(checkpoint_id):e.append("last_checkpoint.id does not match checkpoint file")
    successor=cp.get("successor") or {}

    if active_none:
        if active.get("path") not in {None,""}:e.append("active_ep.path must be null/empty when active_ep.state is NONE")
        if successor.get("ep_id") not in NONE_IDS:e.append("terminal/idle checkpoint successor.ep_id must be NONE")
        if successor.get("frontier_work_package") not in NONE_IDS:e.append("terminal/idle checkpoint successor.frontier_work_package must be NONE")
        return e,w

    ep=load_yaml(root/active["path"]);previous=(ep.get("identity") or {}).get("previous_checkpoint")
    if str(previous)!=str(checkpoint_id):e.append("active EP identity.previous_checkpoint does not match REPO_STATE.last_checkpoint.id")
    if str(successor.get("ep_id"))!=str(active.get("id")):e.append("last checkpoint successor.ep_id does not match active EP")
    if str(successor.get("frontier_work_package"))!=str((s.get("current_position") or {}).get("work_package")):e.append("last checkpoint successor.frontier_work_package does not match current roadmap position")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
