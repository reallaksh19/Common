#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,json
from pathlib import Path
import yaml
from relaylib import load_yaml

DONE={"VERIFIED","SUPERSEDED"}

def _key(node):return str(node.get("id",node.get("issue","")))
def _list(v):return v if isinstance(v,list) else []
def _dump(path:Path,data:dict):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")

def _verify_observation(op:dict,obs:dict)->list[str]:
    e=[];kind=op.get("kind");desired=op.get("desired") or {};rb=obs.get("readback") or {};result=obs.get("result")
    if obs.get("schema_version")!="relay-v2.5-github-observation":e.append("observation schema_version invalid")
    if not _list(obs.get("candidate_basis")):e.append("observation candidate_basis must contain durable references")
    if result not in {"VERIFIED","UNCONFIRMED","FAILED"}:e.append(f"observation result invalid: {result}")
    if not str(obs.get("reason") or "").strip():e.append("observation reason must be explicit")
    if result=="VERIFIED":
        if rb.get("performed") is not True:e.append("VERIFIED observation requires external readback")
        if not _list(rb.get("basis")):e.append("VERIFIED observation requires readback basis")
        if kind=="CREATE":
            if rb.get("found") is not True:e.append("CREATE verification requires created issue to be found")
            if rb.get("marker_present") is not True:e.append("CREATE verification requires stable relay-operation marker")
            if rb.get("issue_number") is None and rb.get("issue_id") is None:e.append("CREATE verification requires observed issue locator")
            if rb.get("github_state")!="OPEN":e.append("CREATE verification requires observed GitHub OPEN state")
        elif kind=="CLOSE" and rb.get("github_state")!="CLOSED":e.append("CLOSE verification requires observed CLOSED state")
        elif kind=="REOPEN" and rb.get("github_state")!="OPEN":e.append("REOPEN verification requires observed OPEN state")
        elif kind in {"UPDATE","PUBLISH_HANDOVER","REVISE","SUPERSEDE"} and rb.get("marker_present") is not True:e.append(f"{kind} verification requires stable relay-operation marker")
        if kind in {"LINK","SUPERSEDE"}:
            want=_list(desired.get("relationships"));seen=_list(rb.get("relationships"))
            for rel in want:
                if rel not in seen:e.append(f"{kind} verification missing desired relationship {rel}")
    return e

def _apply_effects(graph:dict,op:dict,obs:dict):
    nodes={_key(n):n for n in _list(graph.get("nodes"))};node_id=str((op.get("subject") or {}).get("issue_node") or "");rb=obs.get("readback") or {}
    for effect in _list((op.get("reconciliation") or {}).get("issue_graph_effects")):
        if not isinstance(effect,dict):continue
        target_id=str(effect.get("node") or node_id);node=nodes.get(target_id)
        if not node:continue
        if "set_github_state" in effect:node["github_state"]=effect["set_github_state"]
        gh=node.setdefault("github",{})
        if effect.get("set_issue_number")=="OBSERVED":effect["set_issue_number"]=rb.get("issue_number")
        if effect.get("set_issue_id")=="OBSERVED":effect["set_issue_id"]=rb.get("issue_id")
        if "set_issue_number" in effect and effect.get("set_issue_number") is not None:gh["issue_number"]=effect["set_issue_number"]
        if "set_issue_id" in effect and effect.get("set_issue_id") is not None:gh["issue_id"]=effect["set_issue_id"]
    # CREATE always captures verified external identity even if the template omitted the locator effect.
    if op.get("kind")=="CREATE" and node_id in nodes:
        node=nodes[node_id];node["github_state"]="OPEN";gh=node.setdefault("github",{})
        if rb.get("issue_number") is not None:gh["issue_number"]=rb.get("issue_number")
        if rb.get("issue_id") is not None:gh["issue_id"]=rb.get("issue_id")
    # Keep aggregate child snapshots current without turning the projection snapshot into roadmap authority.
    for parent in nodes.values():
        roll=parent.get("child_rollup") or {}
        for snap in _list(roll.get("direct_children")):
            cid=str(snap.get("id") or "")
            if cid in nodes:
                snap["state"]=nodes[cid].get("state");snap["github_state"]=nodes[cid].get("github_state")

def reconcile(root:Path,observation_path:Path,apply:bool=False)->dict:
    state_path=root/"agents/relay/REPO_STATE.yaml";state=load_yaml(state_path);projection=state.get("projection") or {}
    if projection.get("adapter")!="GITHUB_ISSUES":return {"status":"ERROR","errors":["REPO_STATE projection adapter is not GITHUB_ISSUES"]}
    plan_path=root/str(projection.get("plan") or "");plan=load_yaml(plan_path);graph_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml";graph=load_yaml(graph_path);obs=load_yaml(observation_path)
    gid=str((plan.get("generation") or {}).get("id") or "");oid=str(obs.get("operation_id") or "")
    errors=[]
    if str(obs.get("generation_id") or "")!=gid:errors.append("observation generation_id does not match current generation")
    op=next((x for x in _list(plan.get("operations")) if str(x.get("id"))==oid),None)
    if op is None:errors.append(f"observation operation_id not found in generation: {oid}")
    if errors:return {"status":"ERROR","errors":errors}
    errors.extend(_verify_observation(op,obs))
    if errors:return {"status":"ERROR","errors":errors}

    plan=copy.deepcopy(plan);graph=copy.deepcopy(graph);state=copy.deepcopy(state);op=next(x for x in plan["operations"] if str(x.get("id"))==oid)
    pub=op.setdefault("publication",{});ver=op.setdefault("verification",{});publication=obs.get("publication") or {};rb=obs.get("readback") or {}
    if publication.get("attempted") is True:
        pub["attempt_count"]=int(pub.get("attempt_count") or 0)+1
        pub["last_attempt_basis"]=list(obs.get("candidate_basis") or [])
    if publication.get("receipt") not in {None,""}:pub["receipt"]=publication.get("receipt")
    if publication.get("error") not in {None,""}:pub["last_error"]=publication.get("error")
    result=obs.get("result")
    if result=="VERIFIED":
        op["state"]="VERIFIED";ver.update({"status":"PASS","observed_issue_number":rb.get("issue_number"),"observed_issue_id":rb.get("issue_id"),"observed_github_state":rb.get("github_state"),"observed_relationships":list(rb.get("relationships") or []),"basis":list(rb.get("basis") or [])})
        _apply_effects(graph,op,obs)
    elif result=="UNCONFIRMED":
        op["state"]="PUBLISHED_UNCONFIRMED" if pub.get("receipt") not in {None,""} else "ATTEMPTED_UNCONFIRMED";ver.update({"status":"NOT_RUN","basis":list(rb.get("basis") or [])})
    else:
        op["state"]="FAILED";op["failure_basis"]=list(obs.get("candidate_basis") or [])+list(rb.get("basis") or []);ver.update({"status":"FAIL","basis":list(rb.get("basis") or [])})

    ops=_list(plan.get("operations"));all_done=bool(ops) and all(x.get("state") in DONE for x in ops);uncertain=[x for x in ops if x.get("state") in {"ATTEMPTED_UNCONFIRMED","PUBLISHED_UNCONFIRMED"}]
    if all_done:
        plan["generation"]["state"]="IN_SYNC";state["projection"].update({"state":"IN_SYNC","receipt":f"github-generation:{gid}","basis":list(dict.fromkeys(list(state["projection"].get("basis") or [])+list(obs.get("candidate_basis") or [])+list(rb.get("basis") or [])))})
        state["relay_readiness"]["projection_ready"]=True;state["relay_readiness"]["handover_ready"]=bool(state["relay_readiness"].get("baton_ready"))
    elif uncertain:
        plan["generation"]["state"]="PUBLISHED_UNCONFIRMED";with_receipt=next((x for x in uncertain if (x.get("publication") or {}).get("receipt") not in {None,""}),None)
        if with_receipt:
            state["projection"].update({"state":"PUBLISHED_UNCONFIRMED","receipt":f"github-operation:{with_receipt['id']}:{(with_receipt.get('publication') or {}).get('receipt')}"})
        else:state["projection"].update({"state":"PENDING","receipt":None})
        state["relay_readiness"]["projection_ready"]=False;state["relay_readiness"]["handover_ready"]=False
    else:
        plan["generation"]["state"]="PUBLISHING" if any(x.get("state")=="VERIFIED" for x in ops) else "PREPARED";state["projection"].update({"state":"PENDING","receipt":None});state["relay_readiness"]["projection_ready"]=False;state["relay_readiness"]["handover_ready"]=False
    result_doc={"status":"OK","generation_id":gid,"operation_id":oid,"operation_state":op["state"],"generation_state":plan["generation"]["state"],"projection_state":state["projection"]["state"],"applied":apply}
    if apply:
        _dump(plan_path,plan);_dump(graph_path,graph);_dump(state_path,state)
    return result_doc

def main():
    ap=argparse.ArgumentParser();ap.add_argument("observation");ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--apply",action="store_true");a=ap.parse_args();print(json.dumps(reconcile(Path(a.repo_root).resolve(),Path(a.observation).resolve(),a.apply),indent=2,sort_keys=True))
if __name__=="__main__":main()
