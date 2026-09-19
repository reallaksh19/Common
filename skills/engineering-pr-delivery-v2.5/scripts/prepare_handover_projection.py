#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import yaml

from activate_github_generation import activate
from handover_planning import build_handover_plan, render_issue_body
from relaylib import load_yaml
from takeoverlib import digest_mapping
from validate_projection_convergence import expected_execution_ref


UNCONFIRMED={"ATTEMPTED_UNCONFIRMED","PUBLISHED_UNCONFIRMED"}
TERMINAL_OP={"VERIFIED","SUPERSEDED"}


def _dump(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")


def _node_id(node:dict)->str:
    return str(node.get("id",node.get("issue","")))


def _current_generation(root:Path,state:dict)->dict|None:
    projection=state.get("projection") or {};path=projection.get("plan")
    if not path or not (root/str(path)).exists():return None
    return load_yaml(root/str(path))


def _projection_guard(root:Path,state:dict,handover_key:str)->dict|None:
    current=_current_generation(root,state)
    if not current:return None
    gen=current.get("generation") or {};ops=current.get("operations") or []
    for op in ops:
        body=str((op.get("desired") or {}).get("body_projection") or "")
        if handover_key in body and op.get("state") in UNCONFIRMED:
            return {
                "status":"RECONCILE_REQUIRED",
                "reason":"A prior handover GitHub write may already have executed. Read back and reconcile the existing stable operation before any retry.",
                "generation_id":gen.get("id"),
                "operation_id":op.get("id"),
            }
    if gen.get("state")!="IN_SYNC" and any(op.get("state") not in TERMINAL_OP for op in ops):
        return {
            "status":"PROJECTION_BUSY",
            "reason":"The current GitHub projection contains unreconciled operations. Reconcile it before preparing a new handover generation so unrelated desired writes are not discarded.",
            "generation_id":gen.get("id"),
        }
    return None


def _find_open_handover(graph:dict,handover_key:str)->dict|None:
    matches=[]
    for node in graph.get("nodes",[]) or []:
        if not isinstance(node,dict):continue
        if node.get("role")!="HANDOVER" or node.get("handover_key")!=handover_key:continue
        if node.get("github_state")=="OPEN" and ((node.get("github") or {}).get("issue_number") is not None or (node.get("github") or {}).get("issue_id") is not None):
            matches.append(node)
    if len(matches)>1:raise ValueError("multiple open handover ISSUE_GRAPH nodes share the same handover key")
    return matches[0] if matches else None


def _new_node_id(plan:dict)->str:
    key=str(plan["issue_strategy"]["handover_key"]).split(":")[-1]
    state=str(plan["source_report_digest"]).split(":")[-1]
    return f"HANDOVER-{key[:8].upper()}-{state[:8].upper()}"


def _generation_ids(plan:dict,operation_kind:str)->tuple[str,str]:
    digest=digest_mapping({
        "handover_key":plan["issue_strategy"]["handover_key"],
        "source_report_digest":plan["source_report_digest"],
        "intent":plan["intent"],
        "kind":operation_kind,
    }).split(":")[-1][:12].upper()
    return f"GHGEN-HO-{digest}",f"GHOP-HO-{digest}"


def prepare(root:Path,owner_requirements:list[str]|None=None,complex_project:bool=False,apply:bool=False)->dict:
    root=root.resolve();plan=build_handover_plan(root,owner_requirements=owner_requirements or [],complex_project=complex_project)
    if plan.get("status")!="READY":return plan

    state_path=root/"agents/relay/REPO_STATE.yaml";graph_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml"
    state=load_yaml(state_path);graph=load_yaml(graph_path);handover_key=plan["issue_strategy"]["handover_key"]
    guard=_projection_guard(root,state,handover_key)
    if guard:return guard

    graph=copy.deepcopy(graph);existing=_find_open_handover(graph,handover_key)
    kind="PUBLISH_HANDOVER" if existing else "CREATE"
    node_id=_node_id(existing) if existing else _new_node_id(plan)
    gid,oid=_generation_ids(plan,kind)
    operation_marker=f"<!-- relay-operation:{oid} -->"
    body=operation_marker+"\n"+render_issue_body(plan)
    source=plan.get("work_contract") or {};source_issue=source.get("issue") or {}

    if existing is None:
        node={
            "id":node_id,
            "role":"HANDOVER",
            "handover_key":handover_key,
            "state":"ACTIVE",
            "github_state":"ABSENT",
            "github":{},
            "source_contract":{"kind":source.get("kind"),"id":source.get("id"),"work_package":source.get("work_package")},
        }
        graph.setdefault("nodes",[]).append(node)
        source_node=source.get("id") if source.get("kind")=="GITHUB_ISSUE" else None
        if source_node and any(_node_id(x)==str(source_node) for x in graph.get("nodes",[]) or []):
            rel={"from":node_id,"relation":"RELATES_TO","to":str(source_node)}
            if rel not in (graph.get("relationships") or []):graph.setdefault("relationships",[]).append(rel)
    else:node=existing

    graph_revision=graph.get("graph_revision")
    if not graph_revision:
        graph_revision=f"IG-HANDOVER-{handover_key.split(':')[-1][:8].upper()}"
        graph["graph_revision"]=graph_revision

    repository=(state.get("repository") or {}).get("remote") or (state.get("repository") or {}).get("name") or "UNKNOWN_REPOSITORY"
    generation_rel=f"agents/relay/projection/generations/{gid}.yaml"
    desired={
        "body_marker":operation_marker,
        "body_projection":body,
        "github_state":"OPEN",
        "relationships":[],
    }
    if kind=="CREATE":desired["title"]=f"Engineering handover — {source.get('id')}";desired["source_issue_number"]=source_issue.get("issue_number")
    operation={
        "id":oid,
        "kind":kind,
        "state":"PREPARED",
        "idempotency_key":f"relay:{gid}:{oid}",
        "depends_on":[],
        "subject":{"issue_node":node_id,"related_nodes":[]},
        "preconditions":{
            "repository_issue_state":node.get("github_state"),
            "work_state":node.get("state"),
            "handover_key":handover_key,
        },
        "desired":desired,
        "publication":{"attempt_count":0,"last_attempt_basis":[],"receipt":None,"last_error":None},
        "verification":{"status":"NOT_RUN","observed_issue_number":None,"observed_issue_id":None,"observed_github_state":None,"observed_relationships":[],"basis":[]},
        "reconciliation":{
            "issue_graph_effects":([{"node":node_id,"set_github_state":"OPEN","set_issue_number":"OBSERVED","set_issue_id":"OBSERVED"}] if kind=="CREATE" else []),
            "complete_when":(["issue identity verified","relay-operation marker verified"] if kind=="CREATE" else ["handover body marker verified on existing issue"]),
        },
    }
    generation={
        "schema_version":"relay-v2.5-github-projection",
        "generation":{
            "id":gid,
            "repository":repository,
            "roadmap_revision":(state.get("roadmap") or {}).get("revision"),
            "issue_graph_revision":graph_revision,
            "execution_ref":expected_execution_ref(root,state),
            "state":"PREPARED",
            "supersedes_generation":None,
            "basis":[
                "agents/relay/REPO_STATE.yaml",
                "agents/relay/roadmap/ISSUE_GRAPH.yaml",
                f"handover-plan:{plan['source_report_digest']}",
            ],
        },
        "operations":[operation],
    }

    result={
        "status":"READY",
        "action":"UPDATE_HANDOVER_ISSUE" if kind=="PUBLISH_HANDOVER" else "CREATE_HANDOVER_ISSUE",
        "handover_key":handover_key,
        "issue_node":node_id,
        "generation_id":gid,
        "operation_id":oid,
        "generation_path":generation_rel,
        "proposed_issue_graph":graph,
        "proposed_generation":generation,
        "relationship":{
            "source_issue_number":source_issue.get("issue_number"),
            "source_issue_url":source_issue.get("url"),
            "repository_relation":"RELATES_TO" if source.get("kind")=="GITHUB_ISSUE" else None,
            "native_parent_claim":"UNVERIFIED",
            "native_parent_preference":plan["issue_strategy"]["relationship_preference"],
            "fallback":plan["issue_strategy"]["relationship_fallback"],
        },
        "applied":False,
    }
    if not apply:return result

    old_graph=load_yaml(graph_path)
    gen_path=root/generation_rel
    if gen_path.exists():return {"status":"ERROR","errors":[f"generation path already exists: {generation_rel}"]}
    try:
        _dump(graph_path,graph);_dump(gen_path,generation)
        activation=activate(root,generation_rel,apply=True)
        if activation.get("status")!="OK":raise RuntimeError("; ".join(activation.get("errors") or ["generation activation failed"]))
    except Exception as exc:
        _dump(graph_path,old_graph)
        if gen_path.exists():gen_path.unlink()
        return {"status":"ERROR","errors":[str(exc)],"applied":False}

    result["applied"]=True;result["activation"]=activation
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repo_root",nargs="?",default=".")
    ap.add_argument("--owner-requirement",action="append",default=[])
    ap.add_argument("--complex-project",action="store_true")
    ap.add_argument("--apply",action="store_true")
    a=ap.parse_args()
    print(json.dumps(prepare(Path(a.repo_root),a.owner_requirement,a.complex_project,a.apply),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
