#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from relaylib import index_roadmap,load_yaml,print_result
from roadmap_events import EVENT_PATH,load_events

EVENT_CLASSES={
    "TASK_PROGRESS","IMPLEMENTATION_CHANGE","EVIDENCE_PROGRESS",
    "DELIVERY_OR_CUSTODY_PROGRESS","WAITING_OR_MONITORING",
    "ENGINEERING_DISCOVERY","BLOCKER_CHANGE","OWNER_DECISION","ROADMAP_REVISION",
}
CONCEPT_CHANGE={"NO_CONCEPT_CHANGE","CONCEPT_CHANGE_PROPOSED","CONCEPT_CHANGE_APPLIED"}
FOLLOW_UP={"NONE","NEW_EXECUTION_WORK","ROADMAP_PROPOSAL","OWNER_DECISION_REQUIRED"}


def validate_event(root:Path,event:dict,roadmap:dict,expected_sequence:int|None=None)->list[str]:
    e=[];eid=str(event.get("id") or "")
    if not eid.startswith("EVT-"):e.append("roadmap event id must use EVT-* namespace")
    seq=event.get("sequence")
    if not isinstance(seq,int) or seq<1:e.append(f"{eid or 'event'} sequence must be positive integer")
    if expected_sequence is not None and seq!=expected_sequence:e.append(f"{eid or 'event'} sequence must be {expected_sequence}")
    if event.get("event_class") not in EVENT_CLASSES:e.append(f"{eid or 'event'} event_class invalid: {event.get('event_class')}")
    if not str(event.get("summary") or "").strip():e.append(f"{eid or 'event'} summary must be explicit")

    objectives,phases,wps=index_roadmap(roadmap)
    refs=event.get("concept_refs")
    if not isinstance(refs,list) or not refs:e.append(f"{eid or 'event'} concept_refs must contain at least one objective/phase concept")
    else:
        seen=set()
        for ref in refs:
            key=str(ref)
            if key in seen:e.append(f"{eid or 'event'} duplicate concept_ref {key}")
            seen.add(key)
            if key in wps:e.append(f"{eid or 'event'} concept_ref {key} is a work package; execution work must be linked through execution_refs")
            elif key not in objectives and key not in phases:e.append(f"{eid or 'event'} concept_ref does not resolve to objective/phase: {key}")

    xr=event.get("execution_refs")
    if not isinstance(xr,dict):e.append(f"{eid or 'event'} execution_refs must be mapping")
    else:
        for key in ("work_package","execution_package","checkpoint","issue","pull_request"):
            if key not in xr:e.append(f"{eid or 'event'} execution_refs missing {key}")
        wp=xr.get("work_package")
        if wp not in {None,""} and str(wp) not in wps:e.append(f"{eid or 'event'} execution_refs.work_package missing from roadmap: {wp}")

    basis=event.get("basis")
    if not isinstance(basis,list) or not basis or any(not str(x).strip() for x in basis):e.append(f"{eid or 'event'} basis must contain durable references")

    change=event.get("concept_change")
    if change not in CONCEPT_CHANGE:e.append(f"{eid or 'event'} concept_change invalid: {change}")
    follow=event.get("follow_up")
    if follow not in FOLLOW_UP:e.append(f"{eid or 'event'} follow_up invalid: {follow}")
    rev=event.get("roadmap_revision")
    if not isinstance(rev,dict):e.append(f"{eid or 'event'} roadmap_revision must be mapping")
    else:
        rid=rev.get("id");rpath=rev.get("path")
        if change=="CONCEPT_CHANGE_APPLIED":
            if not str(rid or "").strip() or not str(rpath or "").strip():
                e.append(f"{eid or 'event'} applied concept change requires roadmap revision id/path")
            else:
                path=root/str(rpath)
                if not path.exists():e.append(f"{eid or 'event'} roadmap revision path missing: {rpath}")
                else:
                    data=load_yaml(path);info=data.get("revision") or {}
                    if str(info.get("id") or "")!=str(rid):e.append(f"{eid or 'event'} roadmap revision id does not match referenced record")
        if change=="CONCEPT_CHANGE_PROPOSED" and follow not in {"ROADMAP_PROPOSAL","OWNER_DECISION_REQUIRED"}:
            e.append(f"{eid or 'event'} proposed concept change must route to ROADMAP_PROPOSAL or OWNER_DECISION_REQUIRED")
    if event.get("event_class")=="ROADMAP_REVISION" and change!="CONCEPT_CHANGE_APPLIED":
        e.append(f"{eid or 'event'} ROADMAP_REVISION event must declare CONCEPT_CHANGE_APPLIED")
    return e


def validate(root:Path):
    e=[];w=[];path=root/EVENT_PATH
    if not path.exists():return e,w
    data=load_events(root)
    if data.get("schema_version")!="relay-v2.5-roadmap-events":e.append("ROADMAP_EVENTS schema_version must be relay-v2.5-roadmap-events")
    revision=data.get("ledger_revision")
    if not isinstance(revision,int) or revision<0:e.append("ROADMAP_EVENTS ledger_revision must be non-negative integer")
    events=data.get("events")
    if not isinstance(events,list):return e+["ROADMAP_EVENTS events must be list"],w
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");roadmap=load_yaml(root/state["roadmap"]["path"])
    ids=set()
    for index,event in enumerate(events,1):
        if not isinstance(event,dict):e.append(f"roadmap event[{index}] must be mapping");continue
        eid=str(event.get("id") or "")
        if eid in ids:e.append(f"duplicate roadmap event id {eid}")
        ids.add(eid)
        e.extend(validate_event(root,event,roadmap,expected_sequence=index))
    if isinstance(revision,int) and revision<len(events):e.append("ROADMAP_EVENTS ledger_revision cannot be less than event count")
    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))


if __name__=="__main__":
    main()
