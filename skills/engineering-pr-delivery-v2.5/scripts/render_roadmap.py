#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from relaylib import load_yaml
from roadmap_events import load_events


def mark(state):
    return "[x]" if state=="COMPLETE" else "[~]" if state=="ACTIVE" else "[-]" if state in {"SUPERSEDED","CANCELLED"} else "[ ]"


def _execution_ref_text(refs:dict)->str:
    parts=[]
    for key,label in (
        ("work_package","WP"),
        ("execution_package","EP"),
        ("checkpoint","CP"),
        ("issue","Issue"),
        ("pull_request","PR"),
    ):
        value=refs.get(key)
        if value not in {None,""}:parts.append(f"{label} {value}")
    return ", ".join(parts) if parts else "no execution reference"


def render(root:Path):
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    r=load_yaml(root/s["roadmap"]["path"])
    events=load_events(root).get("events",[]) or []
    lines=[
        f"# {r['roadmap']['title']}",
        "",
        f"Revision: `{r['roadmap']['revision']}`",
        f"Overall progress: **{s['progress']['overall_percent']}%**",
        "",
        "## Concept roadmap",
        "",
        "Objectives and phases describe programme purpose. Work packages remain execution units below this concept layer.",
    ]

    for obj in r.get("objectives",[]) or []:
        lines.append(f"### {mark(obj.get('state'))} {obj.get('id')} — {obj.get('title')}")
        for ph in obj.get("phases",[]) or []:
            lines.append(f"- {mark(ph.get('state'))} {ph.get('id')} — {ph.get('title')} ({ph.get('definition')})")

    lines += ["","## Execution under the concepts"]
    for obj in r.get("objectives",[]) or []:
        for ph in obj.get("phases",[]) or []:
            for wp in ph.get("work_packages",[]) or []:
                deps=", ".join(str(x) for x in (wp.get("depends_on") or [])) or "none"
                lines.append(
                    f"- {mark(wp.get('state'))} **{wp.get('id')} — {wp.get('title')}** "
                    f"[{wp.get('execution_status')}], concept: {obj.get('id')} / {ph.get('id')}, depends on: {deps}"
                )

    lines += ["","## Recent material events"]
    if not events:
        lines.append("- No roadmap events have been recorded.")
    else:
        for event in sorted(
            [x for x in events if isinstance(x,dict)],
            key=lambda x:int(x.get("sequence") or 0),
            reverse=True,
        )[:12]:
            concepts=", ".join(str(x) for x in (event.get("concept_refs") or []))
            lines.append(
                f"- **{event.get('id')} / {event.get('event_class')}** — {event.get('summary')} "
                f"(concepts: {concepts}; {_execution_ref_text(event.get('execution_refs') or {})}; "
                f"concept effect: {event.get('concept_change')}; follow-up: {event.get('follow_up')})"
            )

    lines += [
        "",
        "Roadmap events are historical/source-bound context. They do not change concept-roadmap authority unless a referenced roadmap revision applies that change.",
    ]
    return "\n".join(lines)+"\n"


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output");a=ap.parse_args()
    text=render(Path(a.repo_root).resolve())
    Path(a.output).write_text(text,encoding="utf-8") if a.output else print(text,end="")


if __name__=="__main__":
    main()
