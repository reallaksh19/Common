#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import index_roadmap,load_yaml,print_result
REL={"PARENT_OF","DEPENDS_ON","BLOCKS","SUPERSEDES","REVISION_OF","RELATES_TO","INTEGRATED_BY","DUPLICATES"}
WORK_STATES={"OPEN","ACTIVE","COMPLETE","SUPERSEDED","CANCELLED"}
# github_state is the last verified external state, never a desired-state assertion.
# ABSENT means no GitHub issue has yet been verified for this repository node.
# UNKNOWN is permitted only when a prior locator exists but current state must be re-observed.
GITHUB_STATES={"ABSENT","OPEN","CLOSED","UNKNOWN"}

def key(node):return str(node.get("id",node.get("issue","")))
def validate(root:Path):
    e=[];w=[];path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml"
    if not path.exists():return ["ISSUE_GRAPH.yaml missing"],w
    g=load_yaml(path);s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);_,_,wps=index_roadmap(r);nodes={}
    for n in g.get("nodes",[]) or []:
        k=key(n)
        if not k:e.append("issue graph node requires id or issue");continue
        if k in nodes:e.append(f"duplicate issue graph node {k}")
        nodes[k]=n
        if n.get("state") not in WORK_STATES:e.append(f"issue node {k} state invalid: {n.get('state')}")
        if n.get("github_state") not in GITHUB_STATES:e.append(f"issue node {k} github_state invalid: {n.get('github_state')}")
        locator=n.get("github") or {};gh_state=n.get("github_state");number=locator.get("issue_number");gid=locator.get("issue_id")
        if gh_state=="ABSENT" and (number is not None or gid is not None):e.append(f"issue node {k} github_state ABSENT cannot retain verified GitHub locator")
        if gh_state=="UNKNOWN" and number is None and gid is None:e.append(f"issue node {k} github_state UNKNOWN requires a prior GitHub locator to reconcile")
        rn=n.get("roadmap_node")
        if rn and rn not in wps:e.append(f"issue node {k} references missing roadmap work package {rn}")
    for rel in g.get("relationships",[]) or []:
        a,b,kind=str(rel.get("from","")),str(rel.get("to","")),rel.get("relation")
        if kind not in REL:e.append(f"invalid issue relation {kind}")
        if a not in nodes:e.append(f"issue relation source missing: {a}")
        if b not in nodes:e.append(f"issue relation target missing: {b}")
        if a==b and kind in {"PARENT_OF","DEPENDS_ON","BLOCKS","SUPERSEDES"}:e.append(f"self relation not allowed: {a} {kind}")
    mapped={n.get("roadmap_node") for n in nodes.values()}
    for wid,(_,_,wp) in wps.items():
        if wp.get("issue") is not None and wid not in mapped:e.append(f"roadmap work package {wid} declares issue but is absent from ISSUE_GRAPH")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
