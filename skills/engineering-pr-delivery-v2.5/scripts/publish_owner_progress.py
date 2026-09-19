#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import yaml

from communication_projection import build as build_communication
from owner_publication import OWNER_PUBLICATION_PATH,load_cursor,make_cursor
from render_owner_status import render_projection


def _dump(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")


def publish(root:Path,apply:bool=False,force_record:bool=False)->dict:
    root=root.resolve()
    communication=build_communication(root)
    report=((communication.get("technical") or {}).get("report") or {})
    change=((communication.get("owner") or {}).get("change") or {})
    text=render_projection(communication)
    previous=load_cursor(root)
    should_record=bool(change.get("publication_due")) or previous is None or force_record
    cursor=make_cursor(report,text,change,previous_cursor=previous)
    recorded=False
    if apply and should_record:
        _dump(root/OWNER_PUBLICATION_PATH,cursor)
        recorded=True
    return {
        "status":"OK",
        "event_class":change.get("event_class"),
        "changed_dimensions":change.get("changed_dimensions") or [],
        "publication_due":bool(change.get("publication_due")),
        "record_required":should_record,
        "recorded":recorded,
        "publication_id":cursor["publication"]["id"] if should_record else ((previous or {}).get("publication") or {}).get("id"),
        "cursor_path":OWNER_PUBLICATION_PATH,
        "owner_status":text,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repo_root",nargs="?",default=".")
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--force-record",action="store_true",help="Record an explicit heartbeat/no-material-progress publication.")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    result=publish(Path(a.repo_root),apply=a.apply,force_record=a.force_record)
    if a.json:print(json.dumps(result,indent=2,sort_keys=True))
    else:
        print(result["owner_status"],end="")
        print(f"\nPublication cursor: {result['cursor_path']}")
        print(f"Event: {result['event_class']}")
        print(f"Publication due: {'YES' if result['publication_due'] else 'NO'}")
        print(f"Cursor recorded: {'YES' if result['recorded'] else 'NO'}")


if __name__=="__main__":
    main()
