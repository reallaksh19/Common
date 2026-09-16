#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from relaylib import load_yaml,print_result

TRANSFER_FIELDS=("unresolved_acceptance","inputs","risks","decisions","evidence")
EVIDENCE_STATUS={"PASS","FAIL","NOT_RUN","NA"}
RESOLUTION_DISPOSITIONS={"RESOLVED","CANCELLED_BY_OWNER","NOT_APPLICABLE"}

def key(node):return str(node.get("id",node.get("issue","")))
def _sig(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def _validate_acceptance(items,label,e):
    if not isinstance(items,list):e.append(f"{label} must be a list");return
    seen=set()
    for i,item in enumerate(items):
        p=f"{label}[{i}]"
        if not isinstance(item,dict):e.append(f"{p} must be a mapping with id/state/basis");continue
        for field in ("id","state","basis"):
            if field not in item:e.append(f"{p} missing {field}")
        rid=str(item.get("id","")).strip()
        if rid in seen:e.append(f"{label} duplicate id {rid}")
        seen.add(rid)
        if not rid:e.append(f"{p}.id must be non-empty")
        if not str(item.get("state","")).strip():e.append(f"{p}.state must preserve predecessor disposition")
        if not isinstance(item.get("basis"),list) or not item.get("basis"):e.append(f"{p}.basis must contain durable references")

def _validate_evidence(items,label,e):
    if not isinstance(items,list):e.append(f"{label} must be a list");return
    seen=set()
    for i,item in enumerate(items):
        p=f"{label}[{i}]"
        if not isinstance(item,dict):e.append(f"{p} must be a mapping with id/status/basis_ref");continue
        for field in ("id","status","basis_ref"):
            if field not in item:e.append(f"{p} missing {field}")
        rid=str(item.get("id","")).strip()
        if rid in seen:e.append(f"{label} duplicate id {rid}")
        seen.add(rid)
        status=item.get("status")
        if status not in EVIDENCE_STATUS:e.append(f"{p}.status invalid: {status}")
        if status in {"PASS","FAIL","NOT_RUN"} and not str(item.get("basis_ref","")).strip():e.append(f"{p}.basis_ref must preserve exact evidence basis")
        if status=="NOT_RUN" and not str(item.get("reason","")).strip():e.append(f"{p} NOT_RUN requires reason")

def _resolution_map(node,kind,e):
    res=(node.get("supersession_resolution") or {}).get(kind,[]) or []
    out={}
    for i,item in enumerate(res):
        label=f"issue {key(node)} supersession_resolution.{kind}[{i}]"
        if not isinstance(item,dict):e.append(f"{label} must be a mapping");continue
        rid=str(item.get("id","")).strip()
        if not rid:e.append(f"{label} requires id");continue
        if rid in out:e.append(f"issue {key(node)} duplicate resolved {kind} id {rid}")
        if item.get("disposition") not in RESOLUTION_DISPOSITIONS:e.append(f"{label} disposition invalid: {item.get('disposition')}")
        if not isinstance(item.get("basis"),list) or not item.get("basis"):e.append(f"{label} requires durable basis")
        out[rid]=item
    return out

def _preserve_inherited(node,incoming,outgoing,field,e):
    old=incoming.get(field) or [];new=outgoing.get(field) or []
    out_by={str(x.get("id")):x for x in new if isinstance(x,dict) and x.get("id") is not None}
    kind="acceptance" if field=="unresolved_acceptance" else "evidence"
    resolved=_resolution_map(node,kind,e)
    for item in old:
        if not isinstance(item,dict):continue
        rid=str(item.get("id",""))
        if rid in out_by:
            if _sig(out_by[rid])!=_sig(item):e.append(f"supersession lineage {key(node)} mutates inherited {field} item {rid}")
            if rid in resolved:e.append(f"supersession lineage {key(node)} both carries and resolves inherited {field} item {rid}")
        elif rid not in resolved:
            e.append(f"supersession lineage {key(node)} drops inherited {field} item {rid} without resolution")

def validate(root:Path):
    e=[];w=[];g=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");nodes={key(n):n for n in g.get("nodes",[]) or []}
    rels=[r for r in (g.get("relationships",[]) or []) if r.get("relation")=="SUPERSEDES"]
    successor_for_old={};predecessor_for_new={}
    for rel in rels:
        new,old=str(rel.get("from","")),str(rel.get("to",""))
        if old in successor_for_old and successor_for_old[old]!=new:e.append(f"superseded issue {old} has multiple successors")
        if new in predecessor_for_new and predecessor_for_new[new]!=old:e.append(f"supersession successor {new} has multiple direct predecessors")
        successor_for_old[old]=new;predecessor_for_new[new]=old
    # Supersession lineage must be acyclic.
    for start in list(successor_for_old):
        seen=[];cur=start
        while cur in successor_for_old:
            if cur in seen:
                e.append("supersession cycle: "+" -> ".join(seen+[cur]));break
            seen.append(cur);cur=successor_for_old[cur]

    for rel in rels:
        new,old=str(rel.get("from","")),str(rel.get("to",""));on=nodes.get(old) or {};nn=nodes.get(new) or {}
        if not on or not nn:continue
        if on.get("state")!="SUPERSEDED":e.append(f"superseded predecessor {old} must have state SUPERSEDED")
        if nn.get("state")=="SUPERSEDED" and new not in successor_for_old:e.append(f"superseded intermediate successor {new} must identify its own successor")
        if on.get("github_state")=="OPEN":w.append(f"superseded predecessor {old} remains GitHub OPEN; external projection/closure is still pending")
        transfer=on.get("supersession_receipt") or {}
        if str(transfer.get("successor",""))!=new:e.append(f"superseded predecessor {old} missing successor receipt to {new}")
        if not isinstance(transfer.get("basis"),list) or not transfer.get("basis"):e.append(f"supersession {old}->{new} requires durable transfer basis")
        for field in TRANSFER_FIELDS:
            if field not in transfer:e.append(f"supersession {old}->{new} missing transfer field {field}")
        if "unresolved_acceptance" in transfer:_validate_acceptance(transfer.get("unresolved_acceptance"),f"supersession {old}->{new}.unresolved_acceptance",e)
        if "evidence" in transfer:_validate_evidence(transfer.get("evidence"),f"supersession {old}->{new}.evidence",e)

        inherited=nn.get("supersession_inheritance") or {}
        if str(inherited.get("predecessor",""))!=old:e.append(f"supersession successor {new} missing predecessor inheritance from {old}")
        if inherited.get("basis")!=transfer.get("basis"):e.append(f"supersession {old}->{new} transfer mismatch for basis")
        for field in TRANSFER_FIELDS:
            if field not in inherited:e.append(f"supersession successor {new} missing inherited field {field}")
            elif field in transfer and inherited.get(field)!=transfer.get(field):e.append(f"supersession {old}->{new} transfer mismatch for {field}")

    # If an inherited successor is superseded again, unresolved inherited acceptance/evidence
    # must either be carried forward byte-for-byte semantically or explicitly resolved.
    for node_id,node in nodes.items():
        pred=predecessor_for_new.get(node_id);nxt=successor_for_old.get(node_id)
        if not pred or not nxt:continue
        incoming=node.get("supersession_inheritance") or {};outgoing=node.get("supersession_receipt") or {}
        _preserve_inherited(node,incoming,outgoing,"unresolved_acceptance",e)
        _preserve_inherited(node,incoming,outgoing,"evidence",e)
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
