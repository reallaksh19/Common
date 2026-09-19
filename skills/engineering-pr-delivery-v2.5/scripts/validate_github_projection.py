#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import load_yaml,print_result
from validate_projection_convergence import expected_execution_ref

KINDS={"CREATE","LINK","UPDATE","PUBLISH_HANDOVER","SUPERSEDE","REVISE","CLOSE","REOPEN"}
OP_STATES={"PREPARED","ATTEMPTED_UNCONFIRMED","PUBLISHED_UNCONFIRMED","VERIFIED","SUPERSEDED","FAILED"}
GEN_STATES={"PREPARED","PUBLISHING","PUBLISHED_UNCONFIRMED","IN_SYNC","STALE","SUPERSEDED"}
TERMINAL_WORK={"COMPLETE","SUPERSEDED","CANCELLED"}
NONE={None,""}

def _key(node):return str(node.get("id",node.get("issue","")))
def _explicit(v):return isinstance(v,str) and bool(v.strip())
def _list(v):return v if isinstance(v,list) else []

def _effect_matches(node:dict,effect:dict)->bool:
    if "set_github_state" in effect and node.get("github_state")!=effect.get("set_github_state"):return False
    gh=node.get("github") or {}
    if "set_issue_number" in effect and gh.get("issue_number")!=effect.get("set_issue_number"):return False
    if "set_issue_id" in effect and str(gh.get("issue_id"))!=str(effect.get("set_issue_id")):return False
    if "set_published_handover_snapshot" in effect and node.get("published_handover_snapshot")!=effect.get("set_published_handover_snapshot"):return False
    return True

def _has_locator(node:dict)->bool:
    gh=node.get("github") or {};return gh.get("issue_number") is not None or gh.get("issue_id") is not None

def validate(root:Path):
    e=[];w=[]
    s=load_yaml(root/"agents/relay/REPO_STATE.yaml");p=s.get("projection") or {}
    adapter=p.get("adapter");plan_path=p.get("plan")
    if adapter in NONE and plan_path in NONE:return e,w
    if adapter!="GITHUB_ISSUES":return [f"projection adapter unsupported: {adapter}"],w
    if not _explicit(plan_path):return ["GITHUB_ISSUES projection requires projection.plan"],w
    path=root/str(plan_path)
    if not path.exists():return [f"GitHub projection plan missing: {plan_path}"],w
    g=load_yaml(path);gen=g.get("generation") or {};ops=_list(g.get("operations"))
    graph=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml");nodes={_key(n):n for n in _list(graph.get("nodes"))};rels=_list(graph.get("relationships"))
    if g.get("schema_version")!="relay-v2.5-github-projection":e.append("GitHub projection schema_version must be relay-v2.5-github-projection")
    gid=str(gen.get("id") or "")
    if not gid.startswith("GHGEN-"):e.append("generation.id must use GHGEN-* namespace")
    if gen.get("state") not in GEN_STATES:e.append(f"generation.state invalid: {gen.get('state')}")
    remote=str((s.get("repository") or {}).get("remote") or "")
    if remote and str(gen.get("repository") or "")!=remote:e.append("generation.repository must match REPO_STATE.repository.remote")
    if str(p.get("operation_id") or "")!=gid:e.append("REPO_STATE.projection.operation_id must equal current GitHub generation id")
    if str(gen.get("roadmap_revision") or "")!=str((s.get("roadmap") or {}).get("revision") or ""):e.append("GitHub generation roadmap_revision must match current roadmap")
    if str(gen.get("execution_ref") or "")!=expected_execution_ref(root,s):e.append("GitHub generation execution_ref must match current execution route")
    graph_rev=str(graph.get("graph_revision") or "")
    if str(gen.get("issue_graph_revision") or "")!=graph_rev:e.append("GitHub generation issue_graph_revision must match ISSUE_GRAPH.graph_revision")
    if not isinstance(gen.get("basis"),list) or not gen.get("basis"):e.append("GitHub generation requires durable basis")
    if gen.get("state")=="SUPERSEDED":e.append("REPO_STATE cannot point at a SUPERSEDED GitHub generation")

    ids=[];keys=[]
    for i,op in enumerate(ops):
        label=f"operation[{i}]";oid=str(op.get("id") or "")
        if not oid.startswith("GHOP-"):e.append(f"{label}.id must use GHOP-* namespace")
        if oid in ids:e.append(f"duplicate GitHub operation id {oid}")
        ids.append(oid)
        key=str(op.get("idempotency_key") or "")
        if not key:e.append(f"{label}.idempotency_key must be explicit")
        elif key in keys:e.append(f"duplicate GitHub idempotency_key {key}")
        keys.append(key)
    idset=set(ids)
    deps={}
    for i,op in enumerate(ops):
        oid=str(op.get("id") or "");label=f"GitHub operation {oid or i}";kind=op.get("kind");op_state=op.get("state")
        if kind not in KINDS:e.append(f"{label} kind invalid: {kind}")
        if op_state not in OP_STATES:e.append(f"{label} state invalid: {op_state}")
        depends=_list(op.get("depends_on"));deps[oid]=depends
        for d in depends:
            if d not in idset:e.append(f"{label} depends_on unknown operation {d}")
            if d==oid:e.append(f"{label} cannot depend on itself")
        subject=op.get("subject") or {};node_id=str(subject.get("issue_node") or "");related=[str(x) for x in _list(subject.get("related_nodes"))]
        if node_id not in nodes:e.append(f"{label} subject issue node missing from ISSUE_GRAPH: {node_id}")
        for rid in related:
            if rid not in nodes:e.append(f"{label} related issue node missing from ISSUE_GRAPH: {rid}")
        node=nodes.get(node_id) or {};desired=op.get("desired") or {};pub=op.get("publication") or {};ver=op.get("verification") or {};rec=op.get("reconciliation") or {}
        attempts=pub.get("attempt_count")
        if not isinstance(attempts,int) or attempts<0:e.append(f"{label} publication.attempt_count must be non-negative integer")
        receipt=pub.get("receipt");vstatus=ver.get("status")
        if op_state=="PREPARED":
            if attempts not in {0,None}:e.append(f"{label} PREPARED cannot have publication attempts")
            if receipt not in NONE:e.append(f"{label} PREPARED cannot have receipt")
            if vstatus not in {"NOT_RUN",None}:e.append(f"{label} PREPARED verification must be NOT_RUN")
        elif op_state=="ATTEMPTED_UNCONFIRMED":
            if not isinstance(attempts,int) or attempts<1:e.append(f"{label} ATTEMPTED_UNCONFIRMED requires attempt_count >= 1")
            if receipt not in NONE:e.append(f"{label} ATTEMPTED_UNCONFIRMED must not invent receipt")
            if not _list(pub.get("last_attempt_basis")):e.append(f"{label} ATTEMPTED_UNCONFIRMED requires last_attempt_basis")
            if vstatus not in {"NOT_RUN",None}:e.append(f"{label} ATTEMPTED_UNCONFIRMED verification must be NOT_RUN")
            w.append(f"{label} may have executed externally; reconcile by locator/idempotency marker before retry")
        elif op_state=="PUBLISHED_UNCONFIRMED":
            if not isinstance(attempts,int) or attempts<1:e.append(f"{label} PUBLISHED_UNCONFIRMED requires attempt_count >= 1")
            if receipt in NONE:e.append(f"{label} PUBLISHED_UNCONFIRMED requires publication receipt")
            if vstatus not in {"NOT_RUN",None}:e.append(f"{label} PUBLISHED_UNCONFIRMED verification must remain NOT_RUN until readback")
        elif op_state=="VERIFIED":
            if receipt in NONE:e.append(f"{label} VERIFIED requires publication/recovery receipt")
            if vstatus!="PASS":e.append(f"{label} VERIFIED requires verification.status PASS")
            if not _list(ver.get("basis")):e.append(f"{label} VERIFIED requires verification basis")
            for d in depends:
                dep=next((x for x in ops if str(x.get("id"))==d),{})
                if dep.get("state") not in {"VERIFIED","SUPERSEDED"}:e.append(f"{label} VERIFIED before dependency {d} reached terminal verified state")
            for effect in _list(rec.get("issue_graph_effects")):
                if isinstance(effect,dict):
                    target=nodes.get(str(effect.get("node") or node_id)) or {}
                    if not _effect_matches(target,effect):e.append(f"{label} VERIFIED but ISSUE_GRAPH reconciliation effect is not applied")
        elif op_state=="SUPERSEDED":
            if not _explicit(op.get("superseded_by")):e.append(f"{label} SUPERSEDED requires superseded_by")
        elif op_state=="FAILED":
            if not _list(op.get("failure_basis")):e.append(f"{label} FAILED requires failure_basis")
        if not isinstance(rec.get("issue_graph_effects"),list):e.append(f"{label} reconciliation.issue_graph_effects must be a list")
        if not _list(rec.get("complete_when")):e.append(f"{label} reconciliation.complete_when must be explicit")

        marker=str(desired.get("body_marker") or "")
        if kind in {"CREATE","UPDATE","PUBLISH_HANDOVER","SUPERSEDE","REVISE"} and oid and f"relay-operation:{oid}" not in marker:e.append(f"{label} requires stable body_marker containing relay-operation:{oid}")
        if kind=="CREATE":
            if op_state!="VERIFIED" and node.get("github_state") not in {"ABSENT","UNKNOWN"}:e.append(f"{label} CREATE requires subject last verified GitHub state ABSENT/UNKNOWN before verification")
            if op_state=="VERIFIED":
                if node.get("github_state")!="OPEN":e.append(f"{label} verified CREATE requires reconciled github_state OPEN")
                if not _has_locator(node):e.append(f"{label} verified CREATE requires reconciled GitHub locator")
            if not _explicit(desired.get("title")):e.append(f"{label} CREATE requires desired.title")
            if not _explicit(desired.get("body_projection")):e.append(f"{label} CREATE requires desired.body_projection")
            if desired.get("github_state")!="OPEN":e.append(f"{label} CREATE desired.github_state must be OPEN")
        elif kind=="LINK":
            if not related:e.append(f"{label} LINK requires related_nodes")
            desired_rels=_list(desired.get("relationships"))
            if not desired_rels:e.append(f"{label} LINK requires desired.relationships")
            for rel in desired_rels:
                if not isinstance(rel,dict):e.append(f"{label} LINK relationship must be mapping");continue
                triple=(str(rel.get("from")),rel.get("relation"),str(rel.get("to")))
                if not any((str(x.get("from")),x.get("relation"),str(x.get("to")))==triple for x in rels):e.append(f"{label} LINK attempts relationship absent from ISSUE_GRAPH: {triple}")
        elif kind in {"UPDATE","PUBLISH_HANDOVER","REVISE"}:
            if node.get("github_state") not in {"OPEN","CLOSED","UNKNOWN"}:e.append(f"{label} {kind} requires an existing or reconcilable GitHub issue")
            if not _has_locator(node):e.append(f"{label} {kind} requires GitHub locator")
            if not _explicit(desired.get("body_projection")):e.append(f"{label} {kind} requires desired.body_projection")
        elif kind=="SUPERSEDE":
            if len(related)!=1:e.append(f"{label} SUPERSEDE requires exactly one related successor/predecessor node")
            pair={node_id,*related}
            if len(pair)==2 and not any(x.get("relation")=="SUPERSEDES" and {str(x.get("from")),str(x.get("to"))}==pair for x in rels):e.append(f"{label} SUPERSEDE requires matching ISSUE_GRAPH SUPERSEDES relationship")
            if not _has_locator(node) or any(not _has_locator(nodes.get(rid) or {}) for rid in related):e.append(f"{label} SUPERSEDE requires GitHub locators for both issues")
            if not _explicit(desired.get("body_projection")):e.append(f"{label} SUPERSEDE requires desired.body_projection")
        elif kind=="CLOSE":
            if node.get("state") not in TERMINAL_WORK:e.append(f"{label} CLOSE requires terminal repository work state")
            if not isinstance(node.get("closure_receipt"),dict):e.append(f"{label} CLOSE requires repository closure_receipt before external close")
            if not _has_locator(node):e.append(f"{label} CLOSE requires GitHub locator")
            if op_state!="VERIFIED" and node.get("github_state") not in {"OPEN","UNKNOWN"}:e.append(f"{label} CLOSE requires last verified github_state OPEN/UNKNOWN before verification")
            if op_state=="VERIFIED" and node.get("github_state")!="CLOSED":e.append(f"{label} verified CLOSE requires reconciled github_state CLOSED")
            if desired.get("github_state")!="CLOSED":e.append(f"{label} CLOSE desired.github_state must be CLOSED")
        elif kind=="REOPEN":
            if not _has_locator(node):e.append(f"{label} REOPEN requires GitHub locator")
            if node.get("state") not in {"OPEN","ACTIVE"}:e.append(f"{label} REOPEN requires repository work state OPEN or ACTIVE")
            if op_state!="VERIFIED" and node.get("github_state")!="CLOSED":e.append(f"{label} REOPEN requires last verified github_state CLOSED before verification")
            if op_state=="VERIFIED" and node.get("github_state")!="OPEN":e.append(f"{label} verified REOPEN requires reconciled github_state OPEN")
            if desired.get("github_state")!="OPEN":e.append(f"{label} REOPEN desired.github_state must be OPEN")

    visiting=set();done=set()
    def visit(n,path):
        if n in visiting:e.append("GitHub operation dependency cycle: "+" -> ".join(path+[n]));return
        if n in done:return
        visiting.add(n)
        for d in deps.get(n,[]):visit(d,path+[n])
        visiting.remove(n);done.add(n)
    for oid in ids:visit(oid,[])

    active=[x for x in ops if x.get("state") not in {"VERIFIED","SUPERSEDED","FAILED"}]
    all_done=bool(ops) and all(x.get("state") in {"VERIFIED","SUPERSEDED"} for x in ops)
    gen_state=gen.get("state")
    if gen_state=="IN_SYNC" and not all_done:e.append("GitHub generation IN_SYNC requires every operation VERIFIED or SUPERSEDED")
    if all_done and gen_state!="IN_SYNC":e.append("GitHub generation with every operation reconciled must be IN_SYNC")
    if gen_state=="PREPARED" and any(x.get("state")!="PREPARED" for x in ops):e.append("GitHub generation PREPARED cannot contain attempted/terminal operations")
    if gen_state=="PUBLISHED_UNCONFIRMED" and not any(x.get("state") in {"ATTEMPTED_UNCONFIRMED","PUBLISHED_UNCONFIRMED"} for x in ops):e.append("GitHub generation PUBLISHED_UNCONFIRMED requires unconfirmed operation evidence")
    if gen_state=="STALE":w.append("GitHub generation is stale; create a successor GHGEN and do not publish obsolete operations")
    if active and p.get("state")=="IN_SYNC":e.append("REPO_STATE projection cannot be IN_SYNC while GitHub operations remain unreconciled")
    if all_done and p.get("state")!="IN_SYNC":e.append("fully reconciled GitHub generation requires REPO_STATE projection IN_SYNC")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
