from __future__ import annotations

from pathlib import Path

from relaylib import load_yaml


def _authorization(owner_decisions:list[dict],repository:str|None,number:int|None,head_sha:str|None)->dict:
    if not number:return {"state":"NOT_APPLICABLE","basis":[],"reason":"No pull request delivery vehicle is applicable."}
    exact=[];stale=[]
    for item in owner_decisions or []:
        if not isinstance(item,dict) or item.get("status")!="APPLIED" or item.get("kind")!="AUTHORIZATION":continue
        auth=item.get("delivery_authorization")
        if not isinstance(auth,dict) or auth.get("action")!="MERGE":continue
        if str(auth.get("repository"))!=str(repository) or auth.get("number")!=number:continue
        if str(auth.get("head_sha"))==str(head_sha):exact.append(item)
        elif auth.get("disposition")=="GRANTED":stale.append(item)
    states={str((x.get("delivery_authorization") or {}).get("disposition")) for x in exact}
    if len(states)>1:return {"state":"UNKNOWN","basis":[x.get("id") for x in exact],"reason":"Conflicting applied Owner merge-authorization records exist for the current PR head."}
    if exact:
        item=exact[-1];auth=item.get("delivery_authorization") or {};disposition=auth.get("disposition")
        return {"state":"GRANTED" if disposition=="GRANTED" else "REVOKED","basis":[item.get("id")],"reason":"Applied Owner authorization record is bound to this exact PR/head."}
    if stale:return {"state":"STALE","basis":[x.get("id") for x in stale],"reason":"An Owner merge authorization exists for this PR, but not for the current head SHA."}
    return {"state":"NOT_GRANTED","basis":[],"reason":"No applied Owner merge authorization is bound to this exact PR/head."}


def _technical(report:dict,obs:dict)->dict:
    no=[];unknown=[]
    acceptance=report.get("acceptance") or []
    if not acceptance:unknown.append("acceptance state is unavailable")
    elif any(x.get("percent")!=100 for x in acceptance if isinstance(x,dict)):no.append("current acceptance criteria are not complete")

    evidence=(report.get("evidence") or {}).get("state")
    if evidence not in {"COMPLETE","NA"}:
        if evidence in {None,""}:unknown.append("engineering evidence state is unavailable")
        else:no.append(f"engineering evidence is {evidence}")

    if (report.get("stop") or {}).get("active"):no.append("an active execution stop remains")

    vehicle=obs.get("vehicle") or {};lifecycle=vehicle.get("lifecycle")
    if lifecycle!="OPEN":
        if lifecycle=="UNKNOWN":unknown.append("pull request lifecycle is unknown")
        else:no.append(f"pull request lifecycle is {lifecycle}")

    checks=obs.get("checks") or {};check_state=checks.get("state")
    if check_state!="PASS":
        if check_state=="UNKNOWN":unknown.append("exact-head check state is unknown")
        else:no.append(f"exact-head checks are {check_state}")

    merge=(obs.get("mergeability") or {}).get("state")
    if merge!="MERGEABLE":
        if merge=="UNKNOWN":unknown.append("mergeability is unknown")
        else:no.append(f"mergeability is {merge}")

    review=(obs.get("review") or {}).get("state")
    if review!="CLEAR":
        if review=="UNKNOWN":unknown.append("review/change-request state is unknown")
        else:no.append(f"review state is {review}")

    if no:return {"state":"NO","reasons":no+unknown}
    if unknown:return {"state":"UNKNOWN","reasons":unknown}
    return {"state":"YES","reasons":[]}


def snapshot(root:Path,report:dict)->dict:
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");delivery=state.get("delivery")
    if not delivery or delivery.get("required") is False:
        return {
            "applicability":"NOT_APPLICABLE","provider":None,"observation_id":None,"observation_path":None,
            "vehicle":None,"mergeability":{"state":"NOT_APPLICABLE"},"checks":{"state":"NOT_APPLICABLE"},
            "review":{"state":"NOT_APPLICABLE"},"ready_for_review":{"state":"NOT_APPLICABLE","reason":"No PR delivery vehicle is required."},
            "technical_ready_to_merge":{"state":"NOT_APPLICABLE","reasons":[]},"merge_authorization":{"state":"NOT_APPLICABLE","basis":[],"reason":"No PR delivery vehicle is required."},
        }
    ptr=delivery.get("observation") or {};path=ptr.get("path")
    if not path or not (root/str(path)).exists():
        return {
            "applicability":"APPLICABLE","provider":delivery.get("provider"),"observation_id":ptr.get("id"),"observation_path":path,
            "vehicle":None,"mergeability":{"state":"UNKNOWN"},"checks":{"state":"UNKNOWN"},"review":{"state":"UNKNOWN"},
            "ready_for_review":{"state":"UNKNOWN","reason":"A current provider delivery observation is missing."},
            "technical_ready_to_merge":{"state":"UNKNOWN","reasons":["current provider delivery observation is missing"]},
            "merge_authorization":{"state":"UNKNOWN","basis":[],"reason":"Current PR identity/head is unavailable."},
        }
    obs=load_yaml(root/str(path));vehicle=obs.get("vehicle") or {};lifecycle=vehicle.get("lifecycle")
    if lifecycle=="OPEN":ready={"state":"YES","reason":"The pull request is open and not draft."}
    elif lifecycle=="DRAFT":ready={"state":"NO","reason":"The pull request is still draft."}
    elif lifecycle=="UNKNOWN":ready={"state":"UNKNOWN","reason":"The pull request lifecycle is unknown."}
    else:ready={"state":"NO","reason":f"The pull request lifecycle is {lifecycle}."}
    authorization=_authorization(report.get("owner_decisions") or [],obs.get("repository"),vehicle.get("number"),(vehicle.get("head") or {}).get("sha"))
    return {
        "applicability":"APPLICABLE",
        "provider":obs.get("provider"),
        "repository":obs.get("repository"),
        "observation_id":obs.get("id"),
        "observation_path":str(path),
        "vehicle":vehicle,
        "mergeability":obs.get("mergeability") or {"state":"UNKNOWN"},
        "checks":obs.get("checks") or {"state":"UNKNOWN"},
        "review":obs.get("review") or {"state":"UNKNOWN"},
        "readback_basis":obs.get("readback_basis") or [],
        "ready_for_review":ready,
        "technical_ready_to_merge":_technical(report,obs),
        "merge_authorization":authorization,
    }
