from __future__ import annotations

from pathlib import Path
from typing import Any

from relaylib import load_yaml

EVENT_PATH="agents/relay/roadmap/ROADMAP_EVENTS.yaml"


def load_events(root:Path)->dict:
    path=root/EVENT_PATH
    if not path.exists():
        return {"schema_version":"relay-v2.5-roadmap-events","ledger_revision":0,"events":[]}
    return load_yaml(path)


def recent_for_concepts(root:Path,concept_refs:list[str],limit:int=8)->list[dict]:
    wanted={str(x) for x in concept_refs if x}
    rows=[]
    for event in load_events(root).get("events",[]) or []:
        if not isinstance(event,dict):continue
        refs={str(x) for x in event.get("concept_refs",[]) or []}
        if refs & wanted:rows.append(event)
    rows.sort(key=lambda x:int(x.get("sequence") or 0),reverse=True)
    return rows[:max(0,int(limit))]


def event_summary(event:dict[str,Any])->dict:
    return {
        "id":event.get("id"),
        "sequence":event.get("sequence"),
        "event_class":event.get("event_class"),
        "summary":event.get("summary"),
        "concept_refs":event.get("concept_refs") or [],
        "execution_refs":event.get("execution_refs") or {},
        "concept_change":event.get("concept_change"),
        "follow_up":event.get("follow_up"),
        "roadmap_revision":event.get("roadmap_revision") or {},
        "basis":event.get("basis") or [],
    }
