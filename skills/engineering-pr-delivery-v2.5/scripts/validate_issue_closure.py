#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import index_roadmap,load_yaml,print_result
from validate_issue_projection_tree import validate as validate_projection_tree

TERMINAL_WORK={"COMPLETE","SUPERSEDED","CANCELLED"}
REMAINING={"NONE","TRANSFERRED_TO_SUCCESSOR","SUPERSEDED_BY_SUCCESSOR","CANCELLED_BY_OWNER"}
ACCEPTANCE_DISPOSITIONS={"SATISFIED","FAILED_TERMINAL","TRANSFERRED","SUPERSEDED","CANCELLED_BY_OWNER"}
EVIDENCE_STATUS={"PASS","FAIL","NOT_RUN","NA"}
EVIDENCE_DISPOSITIONS={"SATISFIED","RETAINED_LIMITATION","TRANSFERRED","SUPERSEDED","NOT_APPLICABLE"}
ITEM_KINDS={"ACCEPTANCE","EVIDENCE","INPUT","RISK","DECISION","OTHER"}

def key(node):return str(node.get("id",node.get("issue","")))

def _validate_acceptance(items,label,e):
    if not isinstance(items,list):e.append(f"closed issue {label} closure_receipt.acceptance must be a list");return
    for i,item in enumerate(items):
        p=f"closed issue {label} acceptance[{i}]"
        if not isinstance(item,dict):e.append(f"{p} must be a mapping");continue
        for f in ("id","status","disposition","basis"):
            if f not in item:e.append(f"{p} missing {f}")
        if item.get("disposition") not in ACCEPTANCE_DISPOSITIONS:e.append(f"{p} disposition invalid: {item.get('disposition')}")
        if not isinstance(item.get("basis"),list) or not item.get("basis"):e.append(f"{p} basis must contain durable references")

def _validate_evidence(items,label,e):
    if not isinstance(items,list):e.append(f"closed issue {label} closure_receipt.evidence must be a list");return
    for i,item in enumerate(items):
        p=f"closed issue {label} evidence[{i}]"
        if not isinstance(item,dict):e.append(f"{p} must be a mapping");continue
        for f in ("id","status","disposition","basis_ref"):
            if f not in item:e.append(f"{p} missing {f}")
        status=item.get("status");disp=item.get("disposition")
        if status not in EVIDENCE_STATUS:e.append(f"{p} status invalid: {status}")
        if disp not in EVIDENCE_DISPOSITIONS:e.append(f"{p} disposition invalid: {disp}")
        if status in {"PASS","FAIL","NOT_RUN"} and not str(item.get("basis_ref","")).strip():e.append(f"{p} basis_ref must preserve exact evidence basis")
        if status=="NOT_RUN" and not str(item.get("reason","")).strip():e.append(f"{p} NOT_RUN requires reason")
        if status in {"FAIL","NOT_RUN"} and disp=="SATISFIED":e.append(f"{p} {status} evidence cannot be marked SATISFIED")
        if status=="NA" and disp not in {"NOT_APPLICABLE","RETAINED_LIMITATION"}:e.append(f"{p} NA evidence requires NOT_APPLICABLE or RETAINED_LIMITATION disposition")

def _validate_unresolved(items,label,e):
    if not isinstance(items,list):e.append(f"closed issue {label} closure_receipt.unresolved_items must be a list");return []
    for i,item in enumerate(items):
        p=f"closed issue {label} unresolved_items[{i}]"
        if not isinstance(item,dict):e.append(f"{p} must be a mapping");continue
        for f in ("id","kind","state","basis"):
            if f not in item:e.append(f"{p} missing {f}")
        if item.get("kind") not in ITEM_KINDS:e.append(f"{p} kind invalid: {item.get('kind')}")
        if not str(item.get("state","")).strip():e.append(f"{p} state must preserve unresolved disposition")
        if not isinstance(item.get("basis"),list) or not item.get("basis"):e.append(f"{p} basis must contain durable references")
    return items

def validate(root:Path):
    e=[];w=[]
    pe,pw=validate_projection_tree(root);e.extend(pe);w.extend(pw)
    g=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");s=load_yaml(root/"agents/relay/REPO_STATE.yaml");r=load_yaml(root/s["roadmap"]["path"]);_,_,wps=index_roadmap(r)
    nodes={key(n):n for n in g.get("nodes",[]) or []};relationships=g.get("relationships",[]) or []
    for n in nodes.values():
        if n.get("github_state")!="CLOSED":continue
        label=key(n);rn=n.get("roadmap_node");receipt=n.get("closure_receipt") or {};work_state=n.get("state")
        if work_state not in TERMINAL_WORK:e.append(f"closed issue {label} has non-terminal work state {work_state}")
        if rn in wps and wps[rn][2].get("state") not in TERMINAL_WORK:e.append(f"closed issue {label} maps to non-terminal roadmap node {rn}")
        for k in ("acceptance_terminal","evidence_terminal","acceptance","evidence","pr_disposition","remaining_work_disposition","unresolved_items","successor","checkpoint"):
            if k not in receipt:e.append(f"closed issue {label} missing closure_receipt.{k}")
        if receipt.get("acceptance_terminal") is not True:e.append(f"closed issue {label} acceptance is not terminal")
        if receipt.get("evidence_terminal") is not True:e.append(f"closed issue {label} evidence is not terminal")
        _validate_acceptance(receipt.get("acceptance"),label,e);_validate_evidence(receipt.get("evidence"),label,e);unresolved=_validate_unresolved(receipt.get("unresolved_items"),label,e)
        if not str(receipt.get("pr_disposition","")).strip():e.append(f"closed issue {label} pr_disposition must be explicit")
        if not str(receipt.get("checkpoint","")).strip():e.append(f"closed issue {label} checkpoint must identify final durable checkpoint")
        disposition=receipt.get("remaining_work_disposition")
        if disposition not in REMAINING:e.append(f"closed issue {label} remaining_work_disposition invalid: {disposition}")
        successor=str(receipt.get("successor") or "").strip()
        if unresolved and disposition=="NONE":e.append(f"closed issue {label} has unresolved items but remaining_work_disposition is NONE")
        if disposition in {"TRANSFERRED_TO_SUCCESSOR","SUPERSEDED_BY_SUCCESSOR"}:
            if not successor:e.append(f"closed issue {label} {disposition} requires successor")
            elif successor not in nodes:e.append(f"closed issue {label} successor missing from ISSUE_GRAPH: {successor}")
        if work_state=="SUPERSEDED":
            if disposition!="SUPERSEDED_BY_SUCCESSOR":e.append(f"closed superseded issue {label} requires remaining_work_disposition SUPERSEDED_BY_SUCCESSOR")
            if successor and not any(str(x.get("from"))==successor and x.get("relation")=="SUPERSEDES" and str(x.get("to"))==label for x in relationships):e.append(f"closed superseded issue {label} lacks successor SUPERSEDES relationship")
        if work_state=="CANCELLED" and disposition!="CANCELLED_BY_OWNER":e.append(f"closed cancelled issue {label} requires CANCELLED_BY_OWNER disposition")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
