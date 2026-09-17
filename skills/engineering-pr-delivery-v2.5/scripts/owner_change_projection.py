#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml
from relaylib import compute_frontier, load_yaml
from takeoverlib import yaml_digest


def _rel(root:Path,path:Path)->str:
    try:return str(path.relative_to(root))
    except ValueError:return str(path)


def _revision_files(root:Path):
    base=root/"agents/relay/roadmap/revisions"
    if not base.exists():return []
    return sorted(list(base.glob("*.yaml"))+list(base.glob("*.yml")))


def _odr_ref(revision:dict):
    trigger=((revision.get("revision") or {}).get("trigger") or {})
    ref=trigger.get("path") or trigger.get("ref")
    return ref if isinstance(ref,str) and ref.endswith((".yaml",".yml")) else None


def _find_revision_for_odr(root:Path,odr_path:Path):
    want=_rel(root,odr_path)
    matches=[]
    for path in _revision_files(root):
        rev=load_yaml(path);ref=_odr_ref(rev)
        if ref==want:matches.append((path,rev))
    return matches


def _current_odr_path(root:Path):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    roadmap=load_yaml(root/(state.get("roadmap") or {})["path"])
    record=((roadmap.get("roadmap") or {}).get("revision_record"))
    if not record:return None
    rpath=root/record
    if not rpath.exists():return None
    revision=load_yaml(rpath)
    if ((revision.get("revision") or {}).get("classification"))!="OWNER_INTENT_MUTATION":return None
    ref=_odr_ref(revision)
    return (root/ref) if ref else None


def _current_ep_disposition(state:dict,revision:dict):
    active=state.get("active_ep") or {};ep_id=active.get("id")
    if not ep_id:return {"ep_id":None,"work_package":None,"disposition":"NO_ACTIVE_EP","basis":"no active EP"}
    wp=(state.get("current_position") or {}).get("work_package")
    invalid={str(x) for x in (revision.get("invalidated_execution_packages") or [])}
    if str(ep_id) in invalid:
        return {"ep_id":ep_id,"work_package":wp,"disposition":"INVALIDATED","basis":"listed in invalidated_execution_packages"}
    changes=revision.get("changes") or {}
    removed={str(x) for x in (changes.get("removed") or [])};changed={str(x) for x in (changes.get("changed") or [])};unaffected={str(x) for x in (changes.get("unaffected") or [])}
    if wp and str(wp) in removed:return {"ep_id":ep_id,"work_package":wp,"disposition":"INVALIDATED","basis":"active work package removed"}
    if wp and str(wp) in changed:return {"ep_id":ep_id,"work_package":wp,"disposition":"RECONCILE_REQUIRED","basis":"active work package changed"}
    if wp and str(wp) in unaffected:return {"ep_id":ep_id,"work_package":wp,"disposition":"CONTINUE_UNCHANGED","basis":"active work package explicitly unaffected"}
    return {"ep_id":ep_id,"work_package":wp,"disposition":"UNCLASSIFIED","basis":"revision does not classify active work package"}


def build(root:Path,odr_path:Path|None=None)->dict:
    root=root.resolve();state_path=root/"agents/relay/REPO_STATE.yaml";state=load_yaml(state_path)
    roadmap_path=root/(state.get("roadmap") or {})["path"];roadmap=load_yaml(roadmap_path);rmeta=roadmap.get("roadmap") or {}
    progress_path=root/"agents/relay/roadmap/PROGRESS.yaml";progress=load_yaml(progress_path) if progress_path.exists() else {}
    issue_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml";issues=load_yaml(issue_path) if issue_path.exists() else {"nodes":[],"relationships":[]}
    odr_path=(odr_path.resolve() if odr_path else _current_odr_path(root))
    if not odr_path or not odr_path.exists():
        return {"schema_version":"relay-v2.5-owner-change-projection","available":False,"reason":"no Owner intent-mutation decision selected/current"}
    odr=load_yaml(odr_path);decision=odr.get("decision") or {};intake=odr.get("change_intake") or {};affected=odr.get("affected") or {}
    matches=_find_revision_for_odr(root,odr_path);revision_path=None;revision=None
    if len(matches)==1:revision_path,revision=matches[0]
    status=odr.get("status");applied=status=="APPLIED" and revision is not None
    current=False
    if revision:
        info=revision.get("revision") or {};current=str(info.get("to_revision"))==str(rmeta.get("revision"))
    changes=(revision or {}).get("changes") or {};basis_change=(revision or {}).get("progress_basis_change") or {}
    current_frontier=compute_frontier(roadmap)
    new_frontier=((revision or {}).get("frontier_after") if applied else None)
    disposition=_current_ep_disposition(state,revision or {"changes":{}}) if applied else {"ep_id":((state.get("active_ep") or {}).get("id")),"work_package":((state.get("current_position") or {}).get("work_package")),"disposition":"PENDING_OWNER_CHANGE","basis":"Owner decision has not been applied to a roadmap revision"}
    nodes=issues.get("nodes") or [];issue_ids={str(x.get("id")) for x in nodes if isinstance(x,dict)}
    impacted=[str(x) for x in (affected.get("issues") or [])]
    return {
        "schema_version":"relay-v2.5-owner-change-projection",
        "available":True,
        "generated_from":{
            "odr_path":_rel(root,odr_path),"odr_digest":yaml_digest(odr_path),
            "roadmap_path":_rel(root,roadmap_path),"roadmap_digest":yaml_digest(roadmap_path),"roadmap_revision":rmeta.get("revision"),
            "revision_path":_rel(root,revision_path) if revision_path else None,"revision_digest":yaml_digest(revision_path) if revision_path else None,
            "progress_path":_rel(root,progress_path) if progress_path.exists() else None,"progress_digest":yaml_digest(progress_path) if progress_path.exists() else None,
            "issue_graph_path":_rel(root,issue_path) if issue_path.exists() else None,"issue_graph_digest":yaml_digest(issue_path) if issue_path.exists() else None,
            "repo_state_digest":yaml_digest(state_path),
        },
        "decision":{
            "id":odr.get("id"),"kind":decision.get("kind"),"statement":decision.get("statement"),"source":decision.get("source"),
            "status":status,"applied":bool(applied),"applied_to_current_roadmap":bool(applied and current),
        },
        "concept":{
            "previous":intake.get("previous_concept"),"requested":intake.get("requested_concept") or decision.get("statement"),
            "retained_behavior":intake.get("retained_behavior") or [],"invalidated_behavior":intake.get("invalidated_behavior") or [],"new_scope":intake.get("new_scope") or [],
        },
        "roadmap_impact":{
            "from_revision":((revision or {}).get("revision") or {}).get("from_revision"),"to_revision":((revision or {}).get("revision") or {}).get("to_revision"),
            "added":changes.get("added") or [],"removed":changes.get("removed") or [],"changed":changes.get("changed") or [],"unaffected":changes.get("unaffected") or [],
        },
        "progress_basis_effect":{
            "old_basis":basis_change.get("old_basis"),"new_basis":basis_change.get("new_basis"),"old_total_weight":basis_change.get("old_total_weight"),"new_total_weight":basis_change.get("new_total_weight"),
            "current_basis":((progress.get("progress_basis") or {}).get("id")),
        },
        "issue_impact":{
            "affected":impacted,"known_in_current_graph":[x for x in impacted if x in issue_ids],"issue_graph_reconciled":(revision or {}).get("issue_graph_reconciled"),
        },
        "current_ep_disposition":disposition,
        "new_frontier":new_frontier,
        "current_frontier":current_frontier,
        "required_reconciliation":odr.get("required_reconciliation") or [],
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--odr");ap.add_argument("--output");a=ap.parse_args();root=Path(a.repo_root).resolve();odr=(root/a.odr) if a.odr else None;data=build(root,odr);text=yaml.safe_dump(data,sort_keys=False)
    if a.output:Path(a.output).write_text(text,encoding="utf-8")
    else:print(text,end="")
if __name__=="__main__":main()
