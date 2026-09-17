#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from owner_change_projection import build


def _items(lines,title,items):
    lines += ["",f"## {title}"]
    if items:
        lines.extend(f"- {x}" for x in items)
    else:lines.append("- None recorded.")

def render(root:Path,odr:Path|None=None)->str:
    p=build(root,odr)
    if not p.get("available"):return "# Owner change report\n\nNo Owner intent-mutation change is selected or current.\n"
    d=p.get("decision") or {};c=p.get("concept") or {};ri=p.get("roadmap_impact") or {};pb=p.get("progress_basis_effect") or {};ii=p.get("issue_impact") or {};ep=p.get("current_ep_disposition") or {}
    applied="Applied to the current roadmap" if d.get("applied_to_current_roadmap") else "Not yet applied to the current roadmap"
    lines=["# Owner change report","",f"Decision: **{d.get('id')}** — {applied}.","", "## What is changing",f"Previous concept: {c.get('previous')}",f"Requested concept: {c.get('requested')}"]
    _items(lines,"What stays the same",c.get("retained_behavior") or [])
    _items(lines,"What is invalidated",c.get("invalidated_behavior") or [])
    _items(lines,"New scope",c.get("new_scope") or [])
    lines += ["","## Roadmap impact",f"Roadmap revision: **{ri.get('from_revision')} → {ri.get('to_revision')}**."]
    for label,key in (("Added","added"),("Removed","removed"),("Changed","changed"),("Explicitly unaffected","unaffected")):
        vals=ri.get(key) or [];lines.append(f"- {label}: {', '.join(str(x) for x in vals) if vals else 'none'}")
    changed_den=pb.get("old_total_weight")!=pb.get("new_total_weight")
    lines += ["","## Progress-basis effect",f"Basis: **{pb.get('old_basis')} → {pb.get('new_basis')}**.",f"Roadmap weight: **{pb.get('old_total_weight')} → {pb.get('new_total_weight')}**{' (denominator changed)' if changed_den else ''}."]
    lines += ["","## Issue impact",f"Affected issue records: {', '.join(ii.get('affected') or []) if ii.get('affected') else 'none' }.",f"Issue graph reconciled: **{ii.get('issue_graph_reconciled')}**."]
    lines += ["","## Current work disposition",f"Current EP: **{ep.get('ep_id') or 'none'}**; work package: **{ep.get('work_package') or 'none'}**.",f"Disposition: **{str(ep.get('disposition') or 'unknown').replace('_',' ')}** — {ep.get('basis') or ''}"]
    frontier=p.get("new_frontier");lines += ["","## Resulting frontier",f"{', '.join(str(x) for x in frontier) if frontier else ('Not computed until the decision is applied.' if not d.get('applied') else 'No executable frontier.')}"]
    rec=p.get("required_reconciliation") or [];_items(lines,"Required reconciliation",rec)
    lines += ["","## Decision status",f"Owner decision status: **{d.get('status')}**.",f"Applied to current roadmap: **{'YES' if d.get('applied_to_current_roadmap') else 'NO'}**.","","This report is derived from the Owner Decision Record and roadmap transaction. It is not an authority source."]
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--odr");ap.add_argument("--output");a=ap.parse_args();root=Path(a.repo_root).resolve();odr=(root/a.odr) if a.odr else None;text=render(root,odr)
    if a.output:Path(a.output).write_text(text,encoding="utf-8")
    else:print(text,end="")
if __name__=="__main__":main()
