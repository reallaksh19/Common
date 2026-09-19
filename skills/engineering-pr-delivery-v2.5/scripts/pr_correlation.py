from __future__ import annotations

from pathlib import Path
from typing import Any

from relaylib import load_yaml
from takeoverlib import current_routes


NONTERMINAL_LIFECYCLE={"DRAFT","OPEN","UNKNOWN"}


def delivery_pointers(state:dict)->list[dict]:
    delivery=state.get("delivery") or {}
    out=[]
    primary=delivery.get("observation")
    if isinstance(primary,dict) and primary.get("path"):out.append(primary)
    for item in delivery.get("observations",[]) or []:
        if not isinstance(item,dict) or not item.get("path"):continue
        if not any(str(x.get("path"))==str(item.get("path")) for x in out):out.append(item)
    return out


def load_observations(root:Path,state:dict|None=None)->list[dict]:
    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml")
    rows=[]
    for ptr in delivery_pointers(state):
        path=root/str(ptr.get("path"))
        if not path.exists():continue
        obs=load_yaml(path)
        rows.append({"pointer":ptr,"path":str(ptr.get("path")),"observation":obs})
    return rows


def _issue_nodes(graph:dict)->dict[str,dict]:
    out={}
    for node in graph.get("nodes",[]) or []:
        if not isinstance(node,dict):continue
        nid=node.get("id",node.get("issue"))
        if nid not in {None,""}:out[str(nid)]=node
    return out


def _ep_work_package(ep:dict)->str|None:
    value=(ep.get("roadmap_source") or {}).get("work_package")
    return str(value) if value not in {None,""} else None


def validate_correlation_rows(root:Path,obs:dict,graph:dict|None=None)->list[str]:
    errors=[];graph=graph or load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml")
    nodes=_issue_nodes(graph)
    correlations=((obs.get("description_contract") or {}).get("correlations") or [])
    for index,row in enumerate(correlations):
        if not isinstance(row,dict):continue
        label=f"PR #{(obs.get('vehicle') or {}).get('number')} correlation[{index}]"
        issue_node=str(row.get("issue_node") or "")
        node=nodes.get(issue_node)
        if node is None:
            errors.append(f"{label} issue_node does not exist in ISSUE_GRAPH: {issue_node}")
            continue
        github=node.get("github") or {}
        if github.get("issue_number")!=row.get("issue_number"):
            errors.append(f"{label} issue number does not match ISSUE_GRAPH provider identity")
        ep_path=row.get("ep_path")
        if not ep_path or not (root/str(ep_path)).exists():
            errors.append(f"{label} EP path missing: {ep_path}")
            continue
        ep=load_yaml(root/str(ep_path));ep_id=(ep.get("identity") or {}).get("ep_id")
        if str(ep_id)!=str(row.get("ep_id")):
            errors.append(f"{label} EP id does not match EP file identity")
        wp=_ep_work_package(ep)
        if str(wp)!=str(row.get("work_package")):
            errors.append(f"{label} work package does not match EP roadmap_source")
        if str(node.get("roadmap_node"))!=str(row.get("work_package")):
            errors.append(f"{label} Issue and EP are not meaningfully correlated to the same roadmap work package")
    return errors


def correlations_for_observation(obs:dict)->list[dict]:
    return [x for x in ((obs.get("description_contract") or {}).get("correlations") or []) if isinstance(x,dict)]


def nonterminal_observations(root:Path,state:dict|None=None)->list[dict]:
    rows=[]
    for item in load_observations(root,state):
        obs=item["observation"];lifecycle=(obs.get("vehicle") or {}).get("lifecycle")
        if lifecycle in NONTERMINAL_LIFECYCLE:rows.append(item)
    return rows


def current_ep_ids(root:Path,state:dict|None=None)->set[str]:
    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml")
    return {str(x.get("ep_id")) for x in current_routes(root,state) if x.get("ep_id")}


def checkpoint_ep_id(root:Path,state:dict|None=None)->str|None:
    state=state or load_yaml(root/"agents/relay/REPO_STATE.yaml")
    ptr=state.get("last_checkpoint") or {};path=ptr.get("path")
    if not path or not (root/str(path)).exists():return None
    cp=load_yaml(root/str(path));value=cp.get("ep_id")
    return str(value) if value not in {None,"","NONE"} else None


def covered_ep_ids(rows:list[dict])->set[str]:
    out=set()
    for item in rows:
        for row in correlations_for_observation(item["observation"]):
            if row.get("ep_id"):out.add(str(row.get("ep_id")))
    return out


def _find_ep_path(root:Path,ep_id:str,state:dict)->str|None:
    for route in current_routes(root,state):
        if str(route.get("ep_id"))==str(ep_id):return str(route.get("ep_path"))
    base=root/"agents/relay/execution-packages"
    if base.exists():
        for path in sorted(list(base.glob("*.yaml"))+list(base.glob("*.yml"))):
            try:ep=load_yaml(path)
            except Exception:continue
            if str((ep.get("identity") or {}).get("ep_id"))==str(ep_id):return str(path.relative_to(root))
    return None


def derive_current_correlations(root:Path)->tuple[list[dict],list[str]]:
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");graph=load_yaml(root/"agents/relay/roadmap/ISSUE_GRAPH.yaml")
    ep_ids=list(current_ep_ids(root,state));cp_ep=checkpoint_ep_id(root,state)
    if cp_ep and cp_ep not in ep_ids:ep_ids.append(cp_ep)
    rows=[];errors=[]
    for ep_id in ep_ids:
        ep_path=_find_ep_path(root,ep_id,state)
        if not ep_path:
            errors.append(f"cannot locate EP path for {ep_id}")
            continue
        ep=load_yaml(root/ep_path);wp=_ep_work_package(ep)
        candidates=[]
        for node in graph.get("nodes",[]) or []:
            if not isinstance(node,dict) or str(node.get("roadmap_node"))!=str(wp):continue
            gh=node.get("github") or {}
            if gh.get("issue_number") is None:continue
            candidates.append(node)
        active=[x for x in candidates if x.get("state")=="ACTIVE" and x.get("github_state")=="OPEN"]
        chosen=active if active else [x for x in candidates if x.get("github_state")=="OPEN"]
        if len(chosen)!=1:
            errors.append(f"{ep_id} / {wp} requires exactly one verified open owning issue to render PR correlation; found {len(chosen)}")
            continue
        node=chosen[0];gh=node.get("github") or {};nid=node.get("id",node.get("issue"))
        rows.append({
            "issue_node":str(nid),
            "issue_number":gh.get("issue_number"),
            "ep_id":ep_id,
            "ep_path":ep_path,
            "work_package":wp,
            "relationship":"IMPLEMENTS",
            "meaning":f"{ep_id} delivers the authorized work for {wp} owned by GitHub issue #{gh.get('issue_number')}.",
        })
    return rows,errors


def render_markdown(correlations:list[dict])->str:
    lines=[
        "<!-- relay-pr-correlation:v1 -->",
        "## Engineering correlation",
        "",
        "| Issue | Execution package | Work package | Relationship | Meaning |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in correlations:
        meaning=str(row.get("meaning") or "").replace("|","\\|")
        lines.append(
            f"| #{row.get('issue_number')} | \`{row.get('ep_id')}\` | \`{row.get('work_package')}\` | "
            f"{row.get('relationship')} | {meaning} |"
        )
    lines += [
        "",
        "Correlation source:",
    ]
    for row in correlations:
        lines.append(f"- Issue node \`{row.get('issue_node')}\` ↔ EP \`{row.get('ep_id')}\` at \`{row.get('ep_path')}\`.")
    return "\n".join(lines)+"\n"
