#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from relaylib import load_yaml, print_result

INPUT_APPLICABILITY={"CURRENT_STEP_REQUIRED","CURRENT_EP_REQUIRED","FUTURE_STEP","INFORMATIONAL"}
RESOLUTION={"READY","OWNER_EDITABLE_READY","DEFERRED_NOT_CURRENTLY_REQUIRED","MISSING_BLOCKING","INVALID","STALE"}
CURRENT_REQUIRED={"CURRENT_STEP_REQUIRED","CURRENT_EP_REQUIRED"}
ORACLE_CLASSES={"ANALYTICAL","REFERENCE_DATA","INDEPENDENT_IMPLEMENTATION","FROZEN_GOLDEN","EXTERNAL_STANDARD","MANUAL_RECONSTRUCTION","OBSERVATIONAL"}
DISCOVERY_ACTIONS={"LOCATE","TRACE","VERIFY","COMPARE","INSPECT","RESOLVE","VERIFY_GIT"}
ANTI_DRIFT_EFFECTS={"STALE","STOP","OWNER_REVIEW","RECONCILE"}
MANDATORY_REPORT_SECTIONS=("Executive state","Overall / phase / EP progress","Work completed","Files changed","Acceptance matrix","Tests and evidence","Quality findings","Known limitations","Owner decisions required","GitHub issue changes","Roadmap changes","Exact next actions","Successor EP")

def _text(value:Any)->bool:
    if not isinstance(value,str):return False
    value=value.strip();return bool(value) and not (value.startswith("<") and value.endswith(">"))
def _items(value:Any)->list:return value if isinstance(value,list) else []
def _text_list(value:Any)->bool:return isinstance(value,list) and all(_text(x) for x in value)
def _require_text(errors:list[str],obj:dict,key:str,label:str):
    if not _text(obj.get(key)):errors.append(f"{label}.{key} must be explicit non-placeholder text")
def _check_scope_entries(errors:list[str],entries:Any,label:str,locator_keys:tuple[str,...]):
    if not isinstance(entries,list):errors.append(f"{label} must be a list");return
    for i,item in enumerate(entries):
        il=f"{label}[{i}]"
        if not isinstance(item,dict):errors.append(f"{il} must be a mapping");continue
        if not any(_text(item.get(k)) for k in locator_keys):errors.append(f"{il} must identify one of {', '.join(locator_keys)}")
        _require_text(errors,item,"reason",il)

def validate_ep_data(root:Path,ep:dict,label:str="EP"):
    e=[];w=[];identity=ep.get("identity") or {};executable=identity.get("execution_state") in {"EXECUTABLE","ACTIVE"}
    outcome=ep.get("outcome") or {}
    if not any(_items(outcome.get(k)) for k in ("user_visible","engineering")):e.append(f"{label}.outcome must state at least one user-visible or engineering result")
    for key in ("user_visible","engineering"):
        value=outcome.get(key,[])
        if value is not None and not _text_list(value):e.append(f"{label}.outcome.{key} must contain explicit non-placeholder text")
    context=ep.get("context_capsule") or {}
    for key in ("product_goal","roadmap_position","why_this_work_exists","current_architecture","current_implementation_state"):_require_text(e,context,key,f"{label}.context_capsule")
    discovery=ep.get("repository_discovery")
    if not isinstance(discovery,list) or not discovery:e.append(f"{label}.repository_discovery must contain executable discovery steps")
    else:
        seen=set()
        for i,step in enumerate(discovery):
            sl=f"{label}.repository_discovery[{i}]"
            if not isinstance(step,dict):e.append(f"{sl} must be a mapping");continue
            sid=step.get("id")
            if not _text(sid):e.append(f"{sl}.id must be explicit")
            elif not str(sid).startswith("DSTEP-"):e.append(f"{sl}.id must use DSTEP-* namespace; DISC-* is reserved for Discovery Receipts")
            elif sid in seen:e.append(f"{sl}.id duplicates {sid}")
            else:seen.add(sid)
            if step.get("action") not in DISCOVERY_ACTIONS:e.append(f"{sl}.action invalid: {step.get('action')}")
            targets=[]
            if _text(step.get("target")):targets.append(step.get("target"))
            if isinstance(step.get("targets"),list):targets.extend(x for x in step["targets"] if _text(x))
            if not targets:e.append(f"{sl} must identify target or targets")
            _require_text(e,step,"question",sl)
            if not _text_list(step.get("expected_outputs")) or not step.get("expected_outputs"):e.append(f"{sl}.expected_outputs must contain explicit outputs")
            if not isinstance(step.get("receipt_required"),bool):e.append(f"{sl}.receipt_required must be boolean")
            _require_text(e,step,"on_failure",sl)
    inputs=ep.get("inputs")
    if not isinstance(inputs,list):e.append(f"{label}.inputs must be a list")
    else:
        seen=set()
        for i,item in enumerate(inputs):
            il=f"{label}.inputs[{i}]"
            if not isinstance(item,dict):e.append(f"{il} must be a mapping");continue
            for key in ("id","name","description","authority","source","type"):_require_text(e,item,key,il)
            iid=item.get("id")
            if _text(iid):
                if iid in seen:e.append(f"{il}.id duplicates {iid}")
                seen.add(iid)
            if "units" not in item or not _text(str(item.get("units"))):e.append(f"{il}.units must be explicit; use NA when not applicable")
            if not isinstance(item.get("editable"),bool):e.append(f"{il}.editable must be boolean")
            app=item.get("applicability");res=item.get("resolution")
            if app not in INPUT_APPLICABILITY:e.append(f"{il}.applicability invalid: {app}")
            if res not in RESOLUTION:e.append(f"{il}.resolution invalid: {res}")
            if app in CURRENT_REQUIRED and res=="DEFERRED_NOT_CURRENTLY_REQUIRED":e.append(f"{il}: current-required input cannot be deferred")
            if executable and app in CURRENT_REQUIRED and res in {"MISSING_BLOCKING","INVALID","STALE"}:e.append(f"{il}: executable EP cannot carry unresolved current-required input with resolution {res}")
            if res in {"READY","OWNER_EDITABLE_READY"} and "value" not in item and not _text(item.get("resolution_method")):e.append(f"{il}: ready input requires value or resolution_method")
            if not _text_list(item.get("consumers")) or not item.get("consumers"):e.append(f"{il}.consumers must identify consuming STEP/AC/TEST ids")
            if not _text_list(item.get("validation")) or not item.get("validation"):e.append(f"{il}.validation must define how authority/value is checked")
            if not _text_list(item.get("stale_if")) or not item.get("stale_if"):e.append(f"{il}.stale_if must define invalidation conditions")
    benchmarks=ep.get("benchmarks")
    if not isinstance(benchmarks,list):e.append(f"{label}.benchmarks must be a list")
    else:
        seen=set()
        for i,item in enumerate(benchmarks):
            bl=f"{label}.benchmarks[{i}]"
            if not isinstance(item,dict):e.append(f"{bl} must be a mapping");continue
            for key in ("id","name","purpose","source","independence"):_require_text(e,item,key,bl)
            bid=item.get("id")
            if _text(bid):
                if bid in seen:e.append(f"{bl}.id duplicates {bid}")
                seen.add(bid)
            if item.get("oracle_class") not in ORACLE_CLASSES:e.append(f"{bl}.oracle_class invalid: {item.get('oracle_class')}")
            app=item.get("applicability");res=item.get("resolution")
            if app not in INPUT_APPLICABILITY:e.append(f"{bl}.applicability invalid: {app}")
            if res not in RESOLUTION:e.append(f"{bl}.resolution invalid: {res}")
            if app in CURRENT_REQUIRED and res=="DEFERRED_NOT_CURRENTLY_REQUIRED":e.append(f"{bl}: current-required benchmark cannot be deferred")
            if executable and app in CURRENT_REQUIRED and res in {"MISSING_BLOCKING","INVALID","STALE"}:e.append(f"{bl}: executable EP cannot carry unresolved current-required benchmark with resolution {res}")
            if "payload" not in item or item.get("payload") in (None,"",[],{}):e.append(f"{bl}.payload must contain the benchmark/oracle payload or resolvable reference")
            if "expected" not in item or item.get("expected") in (None,"",[],{}):e.append(f"{bl}.expected must define the expected result")
            if "tolerance" not in item:e.append(f"{bl}.tolerance must be explicit; use null only for exact/non-numeric oracles")
            if not _text_list(item.get("verifies")) or not item.get("verifies"):e.append(f"{bl}.verifies must map to AC/TEST ids")
            if not _text_list(item.get("stale_if")) or not item.get("stale_if"):e.append(f"{bl}.stale_if must define invalidation conditions")
    scope=ep.get("scope") or {}
    for key in ("allowed","allowed_reads","protected","prohibited","owner_reserved"):
        if key not in scope:e.append(f"{label}.scope missing semantic domain '{key}'")
    _check_scope_entries(e,scope.get("allowed"),f"{label}.scope.allowed",("path","domain"))
    if executable and isinstance(scope.get("allowed"),list) and not scope.get("allowed"):e.append(f"{label}.scope.allowed must not be empty for an executable EP")
    _check_scope_entries(e,scope.get("allowed_reads"),f"{label}.scope.allowed_reads",("path","domain"));_check_scope_entries(e,scope.get("protected"),f"{label}.scope.protected",("path","domain","invariant"));_check_scope_entries(e,scope.get("prohibited"),f"{label}.scope.prohibited",("path","domain","invariant"));_check_scope_entries(e,scope.get("owner_reserved"),f"{label}.scope.owner_reserved",("path","domain","decision"))
    anti=ep.get("anti_drift") or {};do_not=anti.get("do_not");stale=anti.get("stale_if")
    if not isinstance(do_not,list) or not do_not:e.append(f"{label}.anti_drift.do_not must contain structured restrictions")
    else:
        for i,item in enumerate(do_not):
            al=f"{label}.anti_drift.do_not[{i}]"
            if not isinstance(item,dict):e.append(f"{al} must be a mapping");continue
            for key in ("id","restriction","reason"):_require_text(e,item,key,al)
    if not isinstance(stale,list) or not stale:e.append(f"{label}.anti_drift.stale_if must contain structured invalidation rules")
    else:
        for i,item in enumerate(stale):
            al=f"{label}.anti_drift.stale_if[{i}]"
            if not isinstance(item,dict):e.append(f"{al} must be a mapping");continue
            for key in ("id","condition","rationale"):_require_text(e,item,key,al)
            if item.get("effect") not in ANTI_DRIFT_EFFECTS:e.append(f"{al}.effect invalid: {item.get('effect')}")
    ac_ids={x.get("id") for x in _items(ep.get("acceptance")) if isinstance(x,dict) and x.get("id")};test_ids={x.get("id") for x in _items(ep.get("validation")) if isinstance(x,dict) and x.get("id")};input_ids={x.get("id") for x in _items(ep.get("inputs")) if isinstance(x,dict) and x.get("id")};bench_ids={x.get("id") for x in _items(ep.get("benchmarks")) if isinstance(x,dict) and x.get("id")}
    steps=ep.get("implementation_plan")
    if not isinstance(steps,list) or not steps:e.append(f"{label}.implementation_plan must contain executable steps")
    else:
        seen=set()
        for i,step in enumerate(steps):
            sl=f"{label}.implementation_plan[{i}]"
            if not isinstance(step,dict):e.append(f"{sl} must be a mapping");continue
            for key in ("id","objective","expected_state"):_require_text(e,step,key,sl)
            sid=step.get("id")
            if _text(sid):
                if sid in seen:e.append(f"{sl}.id duplicates {sid}")
                seen.add(sid)
            for key in ("targets","reads","writes","inputs","acceptance","tests","stop_conditions"):
                if not isinstance(step.get(key),list):e.append(f"{sl}.{key} must be a list")
            if not _text_list(step.get("targets")) or not step.get("targets"):e.append(f"{sl}.targets must identify concrete targets")
            if not _text_list(step.get("acceptance")) or not step.get("acceptance"):e.append(f"{sl}.acceptance must map to acceptance ids")
            if not _text_list(step.get("tests")) or not step.get("tests"):e.append(f"{sl}.tests must map to validation ids")
            if not _text_list(step.get("stop_conditions")) or not step.get("stop_conditions"):e.append(f"{sl}.stop_conditions must be explicit")
            for iid in _items(step.get("inputs")):
                if iid not in input_ids:e.append(f"{sl}.inputs references unknown input {iid}")
            for aid in _items(step.get("acceptance")):
                if aid not in ac_ids:e.append(f"{sl}.acceptance references unknown acceptance id {aid}")
            for tid in _items(step.get("tests")):
                if tid not in test_ids:e.append(f"{sl}.tests references unknown validation id {tid}")
    next_work=ep.get("next_work") or {};nw_steps=next_work.get("steps")
    if not isinstance(next_work.get("phase_transition"),bool):e.append(f"{label}.next_work.phase_transition must be boolean")
    if not isinstance(nw_steps,list) or not nw_steps:e.append(f"{label}.next_work.steps must contain ordered successor/current next work")
    else:
        orders=[];req_seen=set()
        for i,item in enumerate(nw_steps):
            nl=f"{label}.next_work.steps[{i}]"
            if not isinstance(item,dict):e.append(f"{nl} must be a mapping");continue
            order=item.get("order");orders.append(order)
            if not isinstance(order,int) or order<1:e.append(f"{nl}.order must be a positive integer")
            _require_text(e,item,"action",nl);_require_text(e,item,"expected_result",nl)
            for key in ("targets","inputs","tests","benchmarks","acceptance","stop_if"):
                if not isinstance(item.get(key),list):e.append(f"{nl}.{key} must be a list")
            if not _text_list(item.get("targets")) or not item.get("targets"):e.append(f"{nl}.targets must identify concrete targets")
            if not _text_list(item.get("acceptance")) or not item.get("acceptance"):e.append(f"{nl}.acceptance must identify acceptance ids")
            if not _text_list(item.get("stop_if")) or not item.get("stop_if"):e.append(f"{nl}.stop_if must state reconciliation/stop conditions")
            for iid in _items(item.get("inputs")):
                if iid not in input_ids:e.append(f"{nl}.inputs references unknown input {iid}")
            for tid in _items(item.get("tests")):
                if tid not in test_ids:e.append(f"{nl}.tests references unknown validation id {tid}")
            for bid in _items(item.get("benchmarks")):
                if bid not in bench_ids:e.append(f"{nl}.benchmarks references unknown benchmark id {bid}")
            for aid in _items(item.get("acceptance")):
                if aid not in ac_ids:e.append(f"{nl}.acceptance references unknown acceptance id {aid}")
            req=item.get("execution_requirement")
            if req is not None:
                if not isinstance(req,dict):e.append(f"{nl}.execution_requirement must be a mapping or null")
                else:
                    rl=f"{nl}.execution_requirement"
                    rid=req.get("id")
                    if not _text(rid) or not str(rid).startswith("EXECREQ-"):e.append(f"{rl}.id must use EXECREQ-* namespace")
                    elif rid in req_seen:e.append(f"{rl}.id duplicates {rid}")
                    else:req_seen.add(rid)
                    if req.get("type") not in {"LOCAL_ENVIRONMENT","EXTERNAL_ENVIRONMENT"}:e.append(f"{rl}.type invalid: {req.get('type')}")
                    _require_text(e,req,"actor",rl)
                    env=req.get("environment")
                    if not isinstance(env,dict):e.append(f"{rl}.environment must be a mapping")
                    else:
                        _require_text(e,env,"kind",f"{rl}.environment");_require_text(e,env,"description",f"{rl}.environment")
                    if not (_text(req.get("command")) or _text(req.get("instruction"))):e.append(f"{rl} requires command or executable instruction")
                    _require_text(e,req,"working_directory",rl);_require_text(e,req,"unavailable_here_reason",rl);_require_text(e,req,"success_condition",rl)
                    for key in ("required_basis","expected_evidence","blocks","clears"):
                        if not _text_list(req.get(key)) or not req.get(key):e.append(f"{rl}.{key} must contain explicit values")
                    for tid in _items(req.get("expected_evidence")):
                        if tid not in test_ids:e.append(f"{rl}.expected_evidence references unknown validation id {tid}")
                    delegation=req.get("delegation")
                    if not isinstance(delegation,dict):e.append(f"{rl}.delegation must be a mapping")
                    else:
                        dl=f"{rl}.delegation"
                        if delegation.get("mode")!="LOCAL_AGENT":e.append(f"{dl}.mode must be LOCAL_AGENT")
                        _require_text(e,delegation,"prompt",dl)
                        publication=delegation.get("publication")
                        if not isinstance(publication,dict):e.append(f"{dl}.publication must be a mapping")
                        else:
                            if publication.get("target")!="CURRENT_WORK_ISSUE":e.append(f"{dl}.publication.target must be CURRENT_WORK_ISSUE")
                            if publication.get("method") not in {"COMMENT","SUB_ISSUE"}:e.append(f"{dl}.publication.method must be COMMENT or SUB_ISSUE")
                            if publication.get("local_result_update")!="SAME_LOCATION":e.append(f"{dl}.publication.local_result_update must be SAME_LOCATION")
                            if publication.get("readback_required") is not True:e.append(f"{dl}.publication.readback_required must be true")
                        check=delegation.get("response_check")
                        if not isinstance(check,dict):e.append(f"{dl}.response_check must be a mapping")
                        else:
                            if check.get("timer_required") is not True:e.append(f"{dl}.response_check.timer_required must be true")
                            _require_text(e,check,"timer_title",f"{dl}.response_check")
                            if check.get("after_minutes") not in {30,60}:e.append(f"{dl}.response_check.after_minutes must be 30 or 60")
                            for key in ("selection_reason","on_due","on_no_response"):_require_text(e,check,key,f"{dl}.response_check")
        if orders and orders!=list(range(1,len(orders)+1)):e.append(f"{label}.next_work.steps order must be contiguous starting at 1")
    qb=ep.get("qualification_boundary") or {}
    q_required=qb.get("required")
    q_na=qb.get("not_applicable_reason")
    if q_na is not None:
        if q_na!="THREE_PASS_COMPLETE":e.append(f"{label}.qualification_boundary.not_applicable_reason invalid: {q_na}")
        if q_required is not False:e.append(f"{label}.qualification_boundary THREE_PASS_COMPLETE requires required=false")
        if qb.get("question_set") not in (None,{}):e.append(f"{label}.qualification_boundary THREE_PASS_COMPLETE cannot reference QSET")
        basis=qb.get("basis")
        if not _text_list(basis) or not basis:e.append(f"{label}.qualification_boundary THREE_PASS_COMPLETE requires explicit basis")
        elif not any("THREE_PASS_COMPLETE" in str(x) for x in basis):e.append(f"{label}.qualification_boundary THREE_PASS_COMPLETE basis must carry THREE_PASS_COMPLETE marker")
    elif q_required is True and qb.get("question_set") in (None,{}):
        e.append(f"{label}.qualification_boundary required=true requires question_set")
    for i,ac in enumerate(_items(ep.get("acceptance"))):
        if isinstance(ac,dict):_require_text(e,ac,"description",f"{label}.acceptance[{i}]")
    for i,test in enumerate(_items(ep.get("validation"))):
        if isinstance(test,dict):
            _require_text(e,test,"method",f"{label}.validation[{i}]")
            if not _text_list(test.get("proves")) or not test.get("proves"):e.append(f"{label}.validation[{i}].proves must map to acceptance ids")
    report=ep.get("report_contract") or {}
    cadence=report.get("status_publication")
    if cadence is not None:
        if not isinstance(cadence,dict):e.append(f"{label}.report_contract.status_publication must be a mapping")
        else:
            if cadence.get("default_after_minutes")!=25:e.append(f"{label}.report_contract.status_publication.default_after_minutes must be 25")
            override=cadence.get("owner_override")
            if override is not None:
                cl=f"{label}.report_contract.status_publication.owner_override"
                if not isinstance(override,dict):e.append(f"{cl} must be a mapping or null")
                else:
                    if override.get("source")!="OWNER":e.append(f"{cl}.source must be OWNER")
                    mode=override.get("mode")
                    if mode not in {"DISABLED","INTERVAL"}:e.append(f"{cl}.mode must be DISABLED or INTERVAL")
                    after=override.get("after_minutes")
                    if mode=="INTERVAL" and (not isinstance(after,int) or after<1):e.append(f"{cl}.after_minutes must be a positive integer for INTERVAL")
                    if mode=="DISABLED" and after not in {None,0}:e.append(f"{cl}.after_minutes must be null for DISABLED")
                    if not _text_list(override.get("basis")) or not override.get("basis"):e.append(f"{cl}.basis must contain explicit Owner basis")
    sections=report.get("sections") or [];payloads=report.get("payloads")
    if not isinstance(payloads,list):e.append(f"{label}.report_contract.payloads must be a list")
    else:
        by_section={}
        for i,item in enumerate(payloads):
            pl=f"{label}.report_contract.payloads[{i}]"
            if not isinstance(item,dict):e.append(f"{pl} must be a mapping");continue
            for key in ("id","section"):_require_text(e,item,key,pl)
            if _text(item.get("section")):by_section[item["section"]]=item
            if not _text_list(item.get("sources")) or not item.get("sources"):e.append(f"{pl}.sources must identify source objects")
            if not _text_list(item.get("required_fields")) or not item.get("required_fields"):e.append(f"{pl}.required_fields must define reconciliation payload")
        for section in MANDATORY_REPORT_SECTIONS:
            if section in sections and section not in by_section:e.append(f"{label}.report_contract has heading without payload contract: {section}")
    successor=ep.get("successor_relay") or {};outputs=successor.get("required_outputs")
    if not _text_list(outputs) or not outputs:e.append(f"{label}.successor_relay.required_outputs must define durable successor outputs")
    else:
        for required in ("checkpoint","next_frontier","successor_ep_or_terminal_disposition"):
            if required not in outputs:e.append(f"{label}.successor_relay.required_outputs missing {required}")
    return e,w

def validate(root:Path):
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml");ep=load_yaml(root/state["active_ep"]["path"]);return validate_ep_data(root,ep)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
