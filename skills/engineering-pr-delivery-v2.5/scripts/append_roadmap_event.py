#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import yaml

from relaylib import load_yaml
from roadmap_events import EVENT_PATH,load_events
from validate_roadmap_events import validate_event


def _dump(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")


def append_event(root:Path,event_path:Path,apply:bool=False)->dict:
    root=root.resolve();event=load_yaml(event_path)
    if "event" in event and isinstance(event.get("event"),dict):event=event["event"]
    ledger=load_events(root);events=ledger.get("events") or []
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");roadmap=load_yaml(root/state["roadmap"]["path"])
    event=copy.deepcopy(event);event["sequence"]=len(events)+1
    errors=validate_event(root,event,roadmap,expected_sequence=len(events)+1)
    ids={str(x.get("id")) for x in events if isinstance(x,dict)}
    if str(event.get("id") or "") in ids:errors.append(f"roadmap event id already exists: {event.get('id')}")
    if errors:return {"status":"ERROR","errors":errors,"applied":False}

    next_ledger=copy.deepcopy(ledger)
    next_ledger["schema_version"]="relay-v2.5-roadmap-events"
    next_ledger["events"]=list(events)+[event]
    next_ledger["ledger_revision"]=max(int(next_ledger.get("ledger_revision") or 0)+1,len(next_ledger["events"]))
    result={"status":"OK","event":event,"ledger_revision":next_ledger["ledger_revision"],"path":EVENT_PATH,"applied":apply}
    if apply:_dump(root/EVENT_PATH,next_ledger)
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument("event");ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--apply",action="store_true");a=ap.parse_args()
    print(json.dumps(append_event(Path(a.repo_root),Path(a.event).resolve(),a.apply),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
