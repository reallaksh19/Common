from __future__ import annotations

from pathlib import Path
from typing import Any

from relaylib import load_yaml
from report_projection import build as build_report
from roadmap_events import event_summary,recent_for_concepts
from takeoverlib import digest_mapping

TERMINAL_ACCEPTANCE={"COMPLETE","NA"}
SENSITIVE_TOKENS=("password","passwd","api_key","apikey","access_token","auth_token","secret=","token=","private_key")


def _list(value:Any)->list:
    return value if isinstance(value,list) else []


def _mapping(value:Any)->dict:
    return value if isinstance(value,dict) else {}


def _text(value:Any)->str:
    return str(value or "").strip()


def _current_ep(root:Path,report:dict)->tuple[dict|None,str|None]:
    ep_id=(report.get("current_work") or {}).get("ep_id")
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    path=(state.get("active_ep") or {}).get("path")
    if not ep_id or not path or not (root/path).exists():return None,None
    return load_yaml(root/path),str(path)


def _verified_issue_candidates(report:dict)->list[dict]:
    candidates=[]
    for issue in _list((report.get("current_work") or {}).get("issues")):
        if not isinstance(issue,dict):continue
        has_locator=issue.get("issue_number") is not None or issue.get("issue_id") is not None
        if issue.get("github_state")!="OPEN" or not has_locator:continue
        rank=0 if issue.get("engineering_state")=="ACTIVE" else 1
        candidates.append({**issue,"_rank":rank})
    return sorted(candidates,key=lambda x:(x["_rank"],str(x.get("id"))))


def resolve_work_contract(root:Path,report:dict|None=None)->dict:
    report=report or build_report(root);current=report.get("current_work") or {};candidates=_verified_issue_candidates(report)
    if candidates:
        best_rank=candidates[0]["_rank"];best=[x for x in candidates if x["_rank"]==best_rank]
        if len(best)>1:
            return {
                "status":"AMBIGUOUS",
                "kind":"GITHUB_ISSUE",
                "reason":"Multiple equally authoritative verified current issues map to the active work package.",
                "candidates":[{k:v for k,v in x.items() if k!="_rank"} for x in best],
            }
        issue={k:v for k,v in best[0].items() if k!="_rank"}
        return {"status":"RESOLVED","kind":"GITHUB_ISSUE","id":issue.get("id"),"issue":issue,"work_package":current.get("work_package")}

    if current.get("ep_id"):
        return {
            "status":"RESOLVED","kind":"ACTIVE_TASK",
            "id":current.get("ep_id"),"work_package":current.get("work_package"),
            "outcome":current.get("outcome") or {},
        }

    if current.get("work_package"):
        return {
            "status":"RESOLVED","kind":"ROADMAP_WORK_PACKAGE",
            "id":current.get("work_package"),"work_package":current.get("work_package"),
            "outcome":current.get("outcome") or {},
        }

    return {"status":"UNRESOLVED","kind":"NONE","reason":"No verified current issue, active task/EP, or current roadmap work package is available."}


def _pending_acceptance(report:dict)->list[dict]:
    out=[]
    for item in _list(report.get("acceptance")):
        if not isinstance(item,dict):continue
        if item.get("status") in TERMINAL_ACCEPTANCE or item.get("percent")==100:continue
        out.append({
            "id":f"AC:{item.get('id')}",
            "kind":"ACCEPTANCE",
            "source_id":item.get("id"),
            "what_remains":item.get("description") or f"Complete acceptance criterion {item.get('id')}.",
            "why_it_remains":f"Current acceptance state is {item.get('status') or 'not complete'} at {item.get('percent')}%.",
            "basis":item.get("basis") or [],
            "done_when":f"{item.get('id')} is COMPLETE on durable acceptance/evidence basis.",
        })
    return out


def _pending_evidence(report:dict)->list[dict]:
    out=[]
    for item in _list((report.get("evidence") or {}).get("not_run")):
        if not isinstance(item,dict):continue
        out.append({
            "id":f"EVIDENCE:{item.get('id')}",
            "kind":"EVIDENCE",
            "source_id":item.get("id"),
            "what_remains":f"Produce the missing evidence for {item.get('id')}.",
            "why_it_remains":item.get("reason") or "Required evidence is NOT_RUN.",
            "cause":item.get("cause"),
            "basis":[],
            "done_when":f"{item.get('id')} has a terminal evidence disposition on the required material basis.",
        })
    return out


def _pending_next_work(report:dict)->list[dict]:
    out=[];nw=report.get("next_work") or {}
    for step in _list(nw.get("steps")):
        if not isinstance(step,dict):continue
        out.append({
            "id":f"NEXT:{(report.get('generated_from') or {}).get('ep_id')}:{step.get('order')}",
            "kind":"NEXT_WORK",
            "source_id":step.get("order"),
            "what_remains":step.get("action"),
            "why_it_remains":"This is part of the current EP successor/current next-work contract.",
            "basis":[f"EP:{(report.get('generated_from') or {}).get('ep_id')}"],
            "done_when":step.get("expected_result"),
            "targets":step.get("targets") or [],
            "inputs":step.get("inputs") or [],
            "tests":step.get("tests") or [],
            "benchmarks":step.get("benchmarks") or [],
            "acceptance":step.get("acceptance") or [],
            "execution_requirement":step.get("execution_requirement"),
        })
    return out


def _pending_checkpoint(report:dict)->list[dict]:
    out=[];cp=report.get("checkpoint") or {}
    for index,item in enumerate(_list(cp.get("remaining_work")),1):
        if isinstance(item,dict):
            statement=item.get("action") or item.get("statement") or item.get("description") or str(item)
            basis=item.get("basis") or []
        else:statement=str(item);basis=[]
        out.append({
            "id":f"CHECKPOINT_REMAINING:{index}",
            "kind":"REMAINING_WORK",
            "source_id":index,
            "what_remains":statement,
            "why_it_remains":"The last checkpoint retained this item as remaining work.",
            "basis":basis,
            "done_when":"The retained work is completed or explicitly dispositioned by current authority.",
        })
    return out


def _required_owner_decisions(report:dict)->list[dict]:
    out=[];stop=report.get("stop") or {}
    if stop.get("active") and stop.get("category")=="OWNER_DECISION_REQUIRED":
        out.append({
            "id":"OWNER_DECISION:STOP","kind":"OWNER_DECISION","source_id":"STOP",
            "what_remains":stop.get("reason") or "Owner decision required.",
            "why_it_remains":"Current execution is stopped on an Owner-reserved decision.",
            "basis":stop.get("basis") or [],
            "done_when":"An explicit Owner decision is durably recorded and the stop is reconciled.",
        })
    recon=((report.get("checkpoint") or {}).get("roadmap_reconciliation") or {})
    for index,item in enumerate(_list(recon.get("owner_decisions_required")),1):
        if isinstance(item,dict):statement=item.get("reason") or item.get("statement") or str(item);basis=item.get("basis") or []
        else:statement=str(item);basis=[]
        out.append({
            "id":f"OWNER_DECISION:RECON:{index}","kind":"OWNER_DECISION","source_id":index,
            "what_remains":statement,"why_it_remains":"The last checkpoint requires an Owner planning decision.",
            "basis":basis,"done_when":"The required Owner decision is recorded and reconciled.",
        })
    return out


def pending_intent(report:dict)->list[dict]:
    items=_pending_acceptance(report)+_pending_evidence(report)+_pending_next_work(report)+_pending_checkpoint(report)+_required_owner_decisions(report)
    seen=set();out=[]
    for item in items:
        key=str(item.get("id"))
        if key in seen:continue
        seen.add(key);out.append(item)
    return out


def _durable_ref(ep_path:str|None,section:str,item:dict,repository:str|None,material_ref:str|None)->dict:
    iid=item.get("id");source=_text(item.get("source"))
    definition=f"{ep_path}#{section}/{iid}" if ep_path and iid else ep_path
    definition_url=None;source_url=None
    if repository and "/" in repository and material_ref and ep_path:
        definition_url=f"https://github.com/{repository}/blob/{material_ref}/{ep_path}"
        if source and "://" not in source and not source.startswith("<"):
            source_url=f"https://github.com/{repository}/blob/{material_ref}/{source}"
    return {
        "id":iid,
        "name":item.get("name"),
        "definition_path":definition,
        "definition_url":definition_url,
        "source":source or None,
        "source_url":source_url,
        "authority":item.get("authority"),
        "resolution":item.get("resolution"),
    }


def _requirements_safe(requirements:list[str])->tuple[list[str],list[str]]:
    safe=[];errors=[]
    for idx,requirement in enumerate(requirements,1):
        value=_text(requirement)
        if not value:continue
        lower=value.lower()
        if any(token in lower for token in SENSITIVE_TOKENS):
            errors.append(f"Owner requirement {idx} appears to contain sensitive credential/secret material; redact it before GitHub publication.")
        else:safe.append(value)
    return safe,errors



def _previous_handover_snapshot(root:Path,handover_key:str)->dict:
    graph_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml"
    if not graph_path.exists():return {}
    graph=load_yaml(graph_path);matches=[]
    for node in graph.get("nodes",[]) or []:
        if not isinstance(node,dict):continue
        if node.get("role")!="HANDOVER" or node.get("handover_key")!=handover_key:continue
        if node.get("github_state")!="OPEN":continue
        matches.append(node)
    if len(matches)!=1:return {}
    node=matches[0];snapshot=node.get("published_handover_snapshot") or {}
    return {
        "issue_node":node.get("id",node.get("issue")),
        "issue_number":(node.get("github") or {}).get("issue_number"),
        "issue_url":(node.get("github") or {}).get("url"),
        "snapshot":snapshot if isinstance(snapshot,dict) else {},
    }


def _incremental_delta(root:Path,handover_key:str,current_intent:list[dict])->dict:
    prior=_previous_handover_snapshot(root,handover_key);snapshot=prior.get("snapshot") or {}
    previous=[x for x in snapshot.get("intent",[]) or [] if isinstance(x,dict)]
    old={str(x.get("id")):x for x in previous if x.get("id")}
    new={str(x.get("id")):x for x in current_intent if x.get("id")}
    return {
        "prior_publication_present":bool(snapshot),
        "prior_issue_node":prior.get("issue_node"),
        "prior_issue_number":prior.get("issue_number"),
        "prior_issue_url":prior.get("issue_url"),
        "prior_source_report_digest":snapshot.get("source_report_digest"),
        "newly_pending":[new[k] for k in sorted(new.keys()-old.keys())],
        "retained_pending":[new[k] for k in sorted(new.keys()&old.keys())],
        "completed_since_prior":[old[k] for k in sorted(old.keys()-new.keys())],
    }

def _expected_outcomes(report:dict)->dict:
    contract=report.get("active_contract") or {};outcome=contract.get("outcome") or {}
    return {
        "user_visible":outcome.get("user_visible") or [],
        "engineering":outcome.get("engineering") or [],
        "next_results":[x.get("expected_result") for x in _list((report.get("next_work") or {}).get("steps")) if isinstance(x,dict) and x.get("expected_result")],
    }


def _text_requirements(report:dict)->dict:
    contract=report.get("active_contract") or {};scope=contract.get("scope") or {}
    return {
        "protected":scope.get("protected") or [],
        "prohibited":scope.get("prohibited") or [],
        "owner_reserved":scope.get("owner_reserved") or [],
        "deliberate_non_goals":contract.get("deliberate_non_goals") or [],
        "known_problems":contract.get("known_problems") or [],
    }



def parse_handover_command(command:str)->dict:
    normalized=" ".join(str(command or "").strip().lower().replace(","," ").split())
    if not normalized.startswith("plan for handover"):
        return {"status":"ERROR","reason":"Command is not a Plan for Handover invocation.","complex_project":False}
    tail=normalized[len("plan for handover"):].strip()
    complex_project="complex" in tail.split()
    return {
        "status":"READY",
        "command":"PLAN_FOR_HANDOVER",
        "complex_project":complex_project,
        "visible_q1_q5":complex_project,
    }

def build_handover_plan(root:Path,owner_requirements:list[str]|None=None,complex_project:bool=False,handover_issue_url:str|None=None)->dict:
    report=build_report(root);contract=resolve_work_contract(root,report)
    if contract.get("status")!="RESOLVED":
        return {"status":"ERROR","errors":[contract.get("reason") or "Work contract could not be resolved."],"work_contract":contract}

    requirements,errors=_requirements_safe(owner_requirements or [])
    if errors:return {"status":"ERROR","errors":errors,"work_contract":contract}

    ep,ep_path=_current_ep(root,report)
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");repository=(state.get("repository") or {}).get("remote")
    material_ref=(ep.get("git_basis") or {}).get("material_ref") if ep else None
    inputs=[_durable_ref(ep_path,"inputs",x,repository,material_ref) for x in _list((ep or {}).get("inputs")) if isinstance(x,dict)]
    benchmarks=[_durable_ref(ep_path,"benchmarks",x,repository,material_ref) for x in _list((ep or {}).get("benchmarks")) if isinstance(x,dict)]
    intent=pending_intent(report)
    identity_basis={
        "kind":contract.get("kind"),
        "id":contract.get("id"),
        "work_package":contract.get("work_package"),
        "repository":repository,
    }
    handover_key=digest_mapping(identity_basis)
    parent=(contract.get("issue") or {}) if contract.get("kind")=="GITHUB_ISSUE" else {}
    incremental=_incremental_delta(root,handover_key,intent)
    current=report.get("current_work") or {}
    concept_refs=[x for x in [current.get("objective"),current.get("phase")] if x]
    recent_events=[event_summary(x) for x in recent_for_concepts(root,concept_refs,limit=8)]
    issue_strategy={
        "handover_key":handover_key,
        "body_marker":f"<!-- relay-handover-key:{handover_key} -->",
        "reuse_rule":"UPDATE_MATCHING_OPEN_HANDOVER_ISSUE_FOR_SAME_KEY_ELSE_CREATE",
        "repository":identity_basis.get("repository"),
        "parent_issue_number":parent.get("issue_number"),
        "parent_issue_url":parent.get("url"),
        "relationship_preference":"NATIVE_SUB_ISSUE_IF_SUPPORTED_AND_VERIFIED",
        "relationship_fallback":"VERIFIED_RECIPROCAL_REFERENCE",
        "relationship_claim":"UNVERIFIED_UNTIL_PROVIDER_READBACK",
    }
    generator={
        "compatibility_path":"skills/engineering-pr-delivery-v2.5/schemas/three-pass-prompt-generator.schema.md",
        "canonical_launcher":"skills/three-pass-prompt-generator/SKILL.md",
        "canonical_schema":"skills/three-pass-prompt-generator/schema.md",
        "mode":"THREE_PASS_ONLY",
        "complex_mode":bool(complex_project),
        "visible_q1_q5":bool(complex_project),
        "target_status":"READY" if handover_issue_url else "AWAITING_HANDOVER_ISSUE_READBACK",
        "target":handover_issue_url,
        "authorized_actions_rule":"MUST_NOT_EXCEED_GOVERNING_OWNER_AND_WORK_AUTHORITY",
    }
    return {
        "status":"READY",
        "schema_version":"relay-v2.5-handover-plan",
        "source_report_digest":digest_mapping(report),
        "work_contract":contract,
        "intent":intent,
        "inputs":inputs,
        "benchmarks":benchmarks,
        "expected_outcomes":_expected_outcomes(report),
        "text_requirements":_text_requirements(report),
        "owner_core_requirements":requirements,
        "recent_concept_events":recent_events,
        "incremental":incremental,
        "issue_strategy":issue_strategy,
        "generator":generator,
    }


def render_issue_body(plan:dict)->str:
    if plan.get("status")!="READY":raise ValueError("handover plan is not READY")
    wc=plan["work_contract"];lines=[
        plan["issue_strategy"]["body_marker"],
        "# Engineering handover intent","",
        "## Source work",
        f"- Selection: **{wc.get('kind')}**",
        f"- Source identity: **{wc.get('id')}**",
        f"- Work package: **{wc.get('work_package') or 'NA'}**",
    ]
    issue=wc.get("issue") or {}
    if issue.get("issue_number") is not None:lines.append(f"- Source GitHub issue: #{issue.get('issue_number')}")
    if issue.get("url"):lines.append(f"- Source URL: {issue.get('url')}")
    lines += ["","## INTENT — pending items"]
    if plan.get("intent"):
        for item in plan["intent"]:
            lines.append(f"- **{item.get('id')} / {item.get('kind')}** — {item.get('what_remains')}")
            lines.append(f"  - Why pending: {item.get('why_it_remains')}")
            lines.append(f"  - Done when: {item.get('done_when')}")
    else:lines.append("- No pending items remain on the derived current-work basis.")

    delta=plan.get("incremental") or {};lines += ["","## Changes since prior handover"]
    if delta.get("prior_publication_present"):
        if delta.get("completed_since_prior"):
            lines.append("Completed/dispositioned since the prior verified handover:")
            for item in delta["completed_since_prior"]:lines.append(f"- {item.get('id')}: {item.get('what_remains')}")
        if delta.get("newly_pending"):
            lines.append("Newly pending since the prior verified handover:")
            for item in delta["newly_pending"]:lines.append(f"- {item.get('id')}: {item.get('what_remains')}")
        if not delta.get("completed_since_prior") and not delta.get("newly_pending"):lines.append("- Pending INTENT is unchanged from the prior verified handover publication.")
    else:lines.append("- Initial handover publication for this ownership boundary.")

    lines += ["","## Inputs"]
    if plan.get("inputs"):
        for item in plan["inputs"]:
            url=f"; pinned file: {item.get('definition_url')}" if item.get("definition_url") else ""
            lines.append(f"- **{item.get('id')}** — definition: `{item.get('definition_path')}`{url}; source: {item.get('source') or 'embedded/resolved at definition'}")
    else:lines.append("- None recorded for the active task.")

    lines += ["","## Benchmarks"]
    if plan.get("benchmarks"):
        for item in plan["benchmarks"]:
            url=f"; pinned file: {item.get('definition_url')}" if item.get("definition_url") else ""
            lines.append(f"- **{item.get('id')}** — definition: `{item.get('definition_path')}`{url}; source: {item.get('source') or 'embedded/resolved at definition'}")
    else:lines.append("- None recorded for the active task.")

    outcomes=plan.get("expected_outcomes") or {};lines += ["","## Expected outcomes"]
    for value in outcomes.get("user_visible") or []:lines.append(f"- User-visible: {value}")
    for value in outcomes.get("engineering") or []:lines.append(f"- Engineering: {value}")
    for value in outcomes.get("next_results") or []:lines.append(f"- Next-work result: {value}")
    if not any(outcomes.values()):lines.append("- No outcome text is currently recorded.")

    req=plan.get("text_requirements") or {};lines += ["","## Textual requirements and boundaries"]
    for key,label in (("protected","Protected"),("prohibited","Prohibited"),("owner_reserved","Owner-reserved"),("deliberate_non_goals","Non-goal"),("known_problems","Known problem")):
        for item in req.get(key) or []:lines.append(f"- {label}: {item}")

    lines += ["","## Recent concept-linked material events"]
    if plan.get("recent_concept_events"):
        for event in plan["recent_concept_events"]:
            refs=event.get("execution_refs") or {}
            execution=", ".join(str(x) for x in [refs.get("work_package"),refs.get("execution_package"),refs.get("checkpoint"),refs.get("issue"),refs.get("pull_request")] if x not in {None,""})
            lines.append(f"- **{event.get('id')} / {event.get('event_class')}** — {event.get('summary')} (execution: {execution or 'none'}; concept effect: {event.get('concept_change')})")
    else:lines.append("- No material event is recorded for the current objective/phase concepts.")

    lines += ["","## Owner core requirements from this session"]
    if plan.get("owner_core_requirements"):
        for value in plan["owner_core_requirements"]:lines.append(f"- {value}")
    else:lines.append("- No additional user-authored session requirement was supplied to the planner.")

    lines += ["","## Completion test"]
    if plan.get("intent"):
        lines.append("- Every INTENT item above is complete on its governing acceptance/evidence basis or explicitly dispositioned by current authority.")
    else:lines.append("- No pending INTENT remains.")
    lines += ["","## Linkage rule",f"- Preferred: {plan['issue_strategy']['relationship_preference']}.",f"- Fallback: {plan['issue_strategy']['relationship_fallback']}.","- Do not claim native parent/sub-issue state before provider readback."]
    return "\n".join(lines)+"\n"


def render_generator_request(plan:dict)->str:
    if plan.get("status")!="READY":raise ValueError("handover plan is not READY")
    target=plan.get("generator",{}).get("target")
    if not target:raise ValueError("handover issue readback URL is required before three-pass generation")
    intent="\n".join(f"- {x.get('id')}: {x.get('what_remains')} | done when: {x.get('done_when')}" for x in plan.get("intent") or []) or "- No pending INTENT."
    outcomes=(plan.get("expected_outcomes") or {}).get("user_visible",[])+(plan.get("expected_outcomes") or {}).get("engineering",[])
    human_goal="; ".join(str(x) for x in outcomes) or "Complete the current owned engineering work safely and verifiably."
    boundary=plan.get("text_requirements") or {}
    boundaries=[]
    for key in ("protected","prohibited","owner_reserved","deliberate_non_goals"):
        if boundary.get(key):boundaries.append(f"{key}: {boundary.get(key)}")
    mode_line="COMPLEX MODE: ON — show visible Q1 through Q5 inside Prompt 1." if plan.get("generator",{}).get("complex_mode") else "COMPLEX MODE: OFF."
    return f"""TARGET:
{target}

HUMAN GOAL:
{human_goal}

USER INTENT:
{intent}

AUTHORIZED ACTIONS:
Only actions already authorized by the governing work contract and explicit Owner instructions.

INTENT BOUNDARY:
{'; '.join(boundaries) if boundaries else 'Current protected scope, non-goals and Owner-reserved decisions remain binding.'}

INTENT COMPLETION TEST:
Every INTENT item is accepted/verified or explicitly dispositioned by current authority.

IMPORTANT EXPECTATIONS:
Use the handover issue as the target. Inspect live repository/issue/PR/evidence state in Prompt 2 and Prompt 3. Do not trust stale issue prose over repository authority.
{mode_line}
"""
