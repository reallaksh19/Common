#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result

TERMINAL={"COMPLETE","SUPERSEDED","CANCELLED"}

def key(node):return str(node.get("id",node.get("issue","")))

def _derived(children):
    states=[str(x.get("state")) for x in children]
    if any(x=="ACTIVE" for x in states):return "ACTIVE"
    if any(x=="OPEN" for x in states):return "OPEN"
    if states and all(x in TERMINAL for x in states):return "COMPLETE"
    return "OPEN"

def validate(root:Path):
    e=[];w=[];g=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");nodes={key(n):n for n in g.get("nodes",[]) or []}
    parent_of=[x for x in (g.get("relationships",[]) or []) if x.get("relation")=="PARENT_OF"]
    if not parent_of:return e,w
    revision=str(g.get("graph_revision","")).strip()
    if not revision:e.append("ISSUE_GRAPH with PARENT_OF relationships requires graph_revision")
    children={};parents={}
    for rel in parent_of:
        p,c=str(rel.get("from","")),str(rel.get("to",""))
        if p not in nodes or c not in nodes:continue
        children.setdefault(p,[]).append(c);parents.setdefault(c,[]).append(p)
    for child,ps in parents.items():
        if len(ps)>1:e.append(f"issue projection child {child} has multiple parents: {sorted(ps)}")
    # PARENT_OF must be a DAG.
    visiting=set();done=set()
    def visit(n,path):
        if n in visiting:
            e.append("issue projection PARENT_OF cycle: "+" -> ".join(path+[n]));return
        if n in done:return
        visiting.add(n)
        for c in children.get(n,[]):visit(c,path+[n])
        visiting.remove(n);done.add(n)
    for n in nodes:visit(n,[])

    for parent,child_ids in children.items():
        node=nodes[parent];roll=node.get("child_rollup") or {}
        if not roll:
            e.append(f"aggregate issue {parent} requires child_rollup");continue
        if str(roll.get("graph_revision",""))!=revision:e.append(f"aggregate issue {parent} child_rollup.graph_revision != ISSUE_GRAPH.graph_revision")
        snaps=roll.get("direct_children")
        if not isinstance(snaps,list):e.append(f"aggregate issue {parent} child_rollup.direct_children must be a list");continue
        seen=set();snap_by_id={}
        for i,snap in enumerate(snaps):
            if not isinstance(snap,dict):e.append(f"aggregate issue {parent} child_rollup.direct_children[{i}] must be a mapping");continue
            cid=str(snap.get("id",""))
            if not cid:e.append(f"aggregate issue {parent} child snapshot missing id");continue
            if cid in seen:e.append(f"aggregate issue {parent} duplicate child snapshot {cid}")
            seen.add(cid);snap_by_id[cid]=snap
        if set(child_ids)!=set(snap_by_id):e.append(f"aggregate issue {parent} child_rollup must cover exactly direct PARENT_OF children")
        actual=[]
        for cid in child_ids:
            child=nodes[cid];actual.append(child);snap=snap_by_id.get(cid) or {}
            if snap.get("state")!=child.get("state"):e.append(f"aggregate issue {parent} child {cid} state snapshot is stale")
            if snap.get("github_state")!=child.get("github_state"):e.append(f"aggregate issue {parent} child {cid} github_state snapshot is stale")
        derived=_derived(actual)
        if roll.get("derived_state")!=derived:e.append(f"aggregate issue {parent} child_rollup.derived_state must be {derived}")
        all_terminal=bool(actual) and all(x.get("state") in TERMINAL for x in actual)
        if roll.get("all_children_terminal") is not all_terminal:e.append(f"aggregate issue {parent} child_rollup.all_children_terminal must be {str(all_terminal).lower()}")
        if node.get("state") not in {"SUPERSEDED","CANCELLED"} and node.get("state")!=derived:e.append(f"aggregate issue {parent} state must project direct children as {derived}")
        if node.get("github_state")=="CLOSED" and any(x.get("github_state")!="CLOSED" for x in actual):e.append(f"closed aggregate issue {parent} has direct child still GitHub OPEN")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
