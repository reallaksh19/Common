from __future__ import annotations
import hashlib,json
from typing import Mapping,Sequence

DIMENSIONS={"STRUCTURAL_DISTANCE","REPRESENTATION_CHANGE","MODEL_DISCRIMINATION","MULTI_STEP_BRIDGE","SYNTHESIS","COMPETITIVE_MIXING"}
LOW_HINTS={"NO_HINT","RETRIEVAL_CUE"}
STATE_RANK={"INDEPENDENT":1,"TRANSFER_READY":2,"ROBUST":3}
LABEL_ORDER={"T0_DIRECT":0,"T1_NEAR_TRANSFER":1,"T2_REPRESENTATION_TRANSFER":2,"T3_REVERSED_TARGET":3,"T4_CONSTRAINT_TRANSFER":4,"T5_DISCRIMINATION":5,"T6_MULTI_STEP_BRIDGE":6,"T7_SYNTHESIS":7,"T8_COMPETITIVE_MIXED":8}

class Core2BRuntimeError(ValueError):pass

def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v):return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()
def digest_without(row,key):
    x=dict(row);x.pop(key,None);return digest(x)

def legal_pool_index(pool:Mapping):
    out={}
    for item in pool.get("source_items") or []:
        out[item["item_id"]]={"item":item,"lane":"SOURCE_CORE2","problem_family_ref":item["problem_family_ref"],"required_capability_refs":list(item["teaching_release"]["required_capability_refs"]),"structural_distance":"DIRECT","representation_shift_authorized":False}
    for item in pool.get("generated_items") or []:
        arch=item.get("archetype")
        structural={"NEAR_TRANSFER":"NEAR","REVERSED_TARGET":"REVERSED","CONSTRAINT_TRANSFER":"CONSTRAINT"}.get(arch,"DIRECT")
        out[item["item_id"]]={"item":item,"lane":"GENERATED_ORIGINAL","problem_family_ref":item["problem_family_ref"],"required_capability_refs":list(item["required_capability_refs"]),"structural_distance":structural,"representation_shift_authorized":arch=="REPRESENTATION_SHIFT"}
    if not out:raise Core2BRuntimeError("CORE2B_CORE2A_LEGAL_POOL_EMPTY")
    return out

def validate_core1b_receipt(receipt:Mapping)->None:
    if receipt.get("state")!="INDEPENDENT" or receipt.get("semantics")!="OBSERVED_INDEPENDENT_RELEASE_NOT_TRANSFER_LEGALITY":raise Core2BRuntimeError("CORE2B_CORE1B_RELEASE_INVALID")
    if receipt.get("receipt_digest")!=digest_without(receipt,"receipt_digest"):raise Core2BRuntimeError("CORE2B_CORE1B_RELEASE_DIGEST_MISMATCH")
    if not receipt.get("observed_events"):raise Core2BRuntimeError("CORE2B_CORE1B_OBSERVED_EVIDENCE_REQUIRED")

def validate_transfer_events(events:Sequence[Mapping])->None:
    seen=set();expected=1
    for e in events:
        if e.get("event_id") in seen:raise Core2BRuntimeError("CORE2B_TRANSFER_EVENT_DUPLICATE")
        if e.get("event_sequence")!=expected:raise Core2BRuntimeError("CORE2B_TRANSFER_EVENT_SEQUENCE_NOT_APPEND_ONLY")
        if e.get("event_digest")!=digest_without(e,"event_digest"):raise Core2BRuntimeError("CORE2B_TRANSFER_EVENT_DIGEST_MISMATCH")
        if len(str(e.get("evidence_digest","")))!=64:raise Core2BRuntimeError("CORE2B_TRANSFER_EVENT_EVIDENCE_DIGEST_REQUIRED")
        if not set(e.get("dimensions") or [])<=DIMENSIONS:raise Core2BRuntimeError("CORE2B_TRANSFER_EVENT_DIMENSION_INVALID")
        seen.add(e["event_id"]);expected+=1

def capability_snapshot(binding:Mapping,receipt:Mapping)->dict:
    validate_core1b_receipt(receipt)
    if binding.get("core1b_release_ref")!=receipt.get("receipt_id") or binding.get("core1b_release_digest")!=receipt.get("receipt_digest"):raise Core2BRuntimeError("CORE2B_CORE1B_RELEASE_BINDING_MISMATCH")
    if binding.get("capability_ref")!=receipt.get("capability_id") or binding.get("problem_family_ref")!=receipt.get("problem_family_ref"):raise Core2BRuntimeError("CORE2B_CAPABILITY_BINDING_DRIFT")
    events=list(binding.get("transfer_events") or []);validate_transfer_events(events)
    successful=[e for e in events if e.get("outcome")=="PASS" and e.get("hint_level_used") in LOW_HINTS]
    state="INDEPENDENT"
    if successful:state="TRANSFER_READY"
    if len(successful)>=2 and any(e.get("delayed_retrieval") for e in successful) and any(set(e.get("dimensions") or [])&{"SYNTHESIS","COMPETITIVE_MIXING"} for e in successful):state="ROBUST"
    reps=set(receipt.get("representation_evidence") or [])
    for e in successful:
        if e.get("representation_used"):reps.add(e["representation_used"])
    return {"state":state,"representation_success":sorted(reps),"events":events}

def demand_min_state(overlay:Mapping)->str:
    if overlay.get("synthesis") or overlay.get("competitive_mixing"):return "ROBUST"
    if overlay.get("model_discrimination") or overlay.get("multi_step_bridge") or overlay.get("structural_distance") in {"REVERSED","CONSTRAINT"}:return "TRANSFER_READY"
    return "INDEPENDENT"

def validate_session(session:Mapping,legal_pool:Mapping,core1b_receipts:Mapping[str,Mapping],hint_policy:Mapping)->dict:
    if session.get("subject")!="PHYSICS":raise Core2BRuntimeError("CORE2B_SUBJECT_INVALID")
    binding=session.get("core2a_binding") or {}
    if binding.get("legal_pool_ref")!=legal_pool.get("product_id") or binding.get("legal_pool_digest")!=digest(legal_pool):raise Core2BRuntimeError("CORE2B_CORE2A_LEGAL_POOL_BINDING_MISMATCH")
    index=legal_pool_index(legal_pool);bindings={}
    for b in session.get("capability_bindings") or []:
        cap=b.get("capability_ref")
        if cap in bindings:raise Core2BRuntimeError("CORE2B_CAPABILITY_BINDING_DUPLICATE")
        receipt=core1b_receipts.get(b.get("core1b_release_ref"))
        if receipt is None:raise Core2BRuntimeError("CORE2B_CORE1B_RELEASE_UNKNOWN")
        bindings[cap]={"binding":b,"snapshot":capability_snapshot(b,receipt)}
    forbidden=tuple(hint_policy.get("learner_surface_forbidden_tokens") or [])
    seen=set()
    for o in session.get("item_overlays") or []:
        ref=o.get("core2a_item_ref")
        if ref in seen:raise Core2BRuntimeError("CORE2B_ITEM_OVERLAY_DUPLICATE")
        if ref not in index:raise Core2BRuntimeError("CORE2B_ITEM_NOT_IN_CORE2A_LEGAL_POOL")
        seen.add(ref);up=index[ref]
        if o.get("structural_distance")!=up["structural_distance"]:raise Core2BRuntimeError("CORE2B_TRANSFER_DEMAND_DRIFT")
        if o.get("representation_change") and not up["representation_shift_authorized"]:raise Core2BRuntimeError("CORE2B_REPRESENTATION_SHIFT_NOT_AUTHORIZED_UPSTREAM")
        if o.get("display_transfer_label") not in LABEL_ORDER:raise Core2BRuntimeError("CORE2B_TRANSFER_LABEL_INVALID")
        text=json.dumps(up["item"],ensure_ascii=False).upper()
        leaked=[t for t in forbidden if t.upper() in text]
        if leaked:raise Core2BRuntimeError("CORE2B_INTERNAL_LABEL_LEAK:"+",".join(leaked))
    return {"index":index,"bindings":bindings}

def eligible_items(session:Mapping,legal_pool:Mapping,core1b_receipts:Mapping[str,Mapping],hint_policy:Mapping)->list[dict]:
    ctx=validate_session(session,legal_pool,core1b_receipts,hint_policy);index=ctx["index"];bindings=ctx["bindings"];eligible=[]
    for o in session["item_overlays"]:
        up=index[o["core2a_item_ref"]];minimum=demand_min_state(o);ok=True
        for cap in up["required_capability_refs"]:
            b=bindings.get(cap)
            if b is None or STATE_RANK[b["snapshot"]["state"]]<STATE_RANK[minimum]:ok=False;break
            if b["binding"].get("problem_family_ref")!=up["problem_family_ref"]:ok=False;break
            req=o.get("required_representation")
            if req and req not in set(b["snapshot"]["representation_success"]):ok=False;break
        if ok:eligible.append({"overlay":o,"upstream":up["item"],"derived_min_state":minimum})
    return eligible

def demand_score(o:Mapping)->int:
    score={"DIRECT":0,"NEAR":1,"REVERSED":3,"CONSTRAINT":4}[o["structural_distance"]]
    score+=2*int(bool(o.get("representation_change")))+2*int(bool(o.get("model_discrimination")))+2*int(bool(o.get("multi_step_bridge")))+3*int(bool(o.get("synthesis")))+4*int(bool(o.get("competitive_mixing")))
    return score

def choose_next_item(session:Mapping,legal_pool:Mapping,core1b_receipts:Mapping[str,Mapping],hint_policy:Mapping)->dict:
    candidates=eligible_items(session,legal_pool,core1b_receipts,hint_policy)
    if not candidates:raise Core2BRuntimeError("CORE2B_NO_EVIDENCE_ELIGIBLE_ITEM")
    purpose=session.get("purpose");due=(session.get("retrieval_state") or {}).get("next_due_bucket")=="NOW"
    if due:return min(candidates,key=lambda x:demand_score(x["overlay"]))
    if purpose=="FIRST_STUDY":return min(candidates,key=lambda x:demand_score(x["overlay"]))
    if purpose=="PRACTICE":
        near=[x for x in candidates if x["overlay"]["structural_distance"]=="NEAR"]
        if near:return near[0]
    return max(candidates,key=lambda x:demand_score(x["overlay"]))

def validate_attempt_event(event:Mapping,previous_events:Sequence[Mapping]=())->None:
    if event.get("event_digest")!=digest_without(event,"event_digest"):raise Core2BRuntimeError("CORE2B_ATTEMPT_DIGEST_MISMATCH")
    if len(str(event.get("evidence_digest","")))!=64:raise Core2BRuntimeError("CORE2B_ATTEMPT_EVIDENCE_DIGEST_REQUIRED")
    expected=(max([e.get("event_sequence",0) for e in previous_events]) if previous_events else 0)+1
    if event.get("event_sequence")!=expected:raise Core2BRuntimeError("CORE2B_ATTEMPT_SEQUENCE_NOT_APPEND_ONLY")
    if event.get("event_id") in {e.get("event_id") for e in previous_events}:raise Core2BRuntimeError("CORE2B_ATTEMPT_DUPLICATE")

def classify_attempt_hypothesis(event:Mapping,error_taxonomy:Mapping)->dict|None:
    if event.get("outcome")=="CORRECT":return None
    allowed=set(error_taxonomy.get("error_classes") or []);declared=list(event.get("declared_error_hypotheses") or [])
    if declared:
        if not set(declared)<=allowed:raise Core2BRuntimeError("CORE2B_ERROR_HYPOTHESIS_UNKNOWN")
        return {"classification_state":"HYPOTHESIS","error_classes":declared,"confidence":"UNVERIFIED","basis":"DECLARED_OR_TEACHER_TAG"}
    ev=event.get("response_evidence") or {}
    if not ev.get("model_selected"):cls="MODEL_SELECTION"
    elif not ev.get("applicability_statement"):cls="APPLICABILITY"
    elif not ev.get("first_move"):cls="EQUATION_FORMATION"
    elif not ev.get("final_answer"):cls="SYMBOLIC_MANIPULATION"
    elif not ev.get("physical_check"):cls="PHYSICAL_CHECK"
    else:cls="CARELESS_EXECUTION"
    return {"classification_state":"HYPOTHESIS","error_classes":[cls],"confidence":"LOW","basis":"RUNTIME_HEURISTIC_REQUIRES_CORROBORATION"}

def build_core1b_repair_request(learner_profile_ref:str,capability_ref:str,item_ref:str,hypothesis:Mapping|None,error_taxonomy:Mapping)->dict|None:
    if not hypothesis:return None
    atoms=[]
    for cls in hypothesis.get("error_classes") or []:
        for ref in (error_taxonomy.get("repair_routes") or {}).get(cls,[]):
            if ref not in atoms:atoms.append(ref)
    if not atoms:return None
    return {"schema_version":"1.0.0","request_id":"C2B-TO-C1B-"+digest({"learner":learner_profile_ref,"cap":capability_ref,"item":item_ref,"atoms":atoms}),"learner_profile_ref":learner_profile_ref,"capability_ref":capability_ref,"return_to_core2a_item_ref":item_ref,"classification_state":"HYPOTHESIS","error_hypotheses":list(hypothesis.get("error_classes") or []),"repair_atom_refs":atoms,"authority_mutation_allowed":False,"instruction":"Repair only the smallest listed prerequisite set, recheck with observed evidence, then return to the original transfer item."}

def update_retrieval_state(current:Mapping,event:Mapping)->dict:
    if event.get("event_digest")!=digest_without(event,"event_digest"):raise Core2BRuntimeError("CORE2B_ATTEMPT_DIGEST_MISMATCH")
    if len(str(event.get("evidence_digest","")))!=64:raise Core2BRuntimeError("CORE2B_ATTEMPT_EVIDENCE_DIGEST_REQUIRED")
    expected=int(current.get("last_event_sequence",0))+1
    if event.get("event_sequence")!=expected:raise Core2BRuntimeError("CORE2B_ATTEMPT_SEQUENCE_NOT_APPEND_ONLY")
    previous_digest=current.get("state_digest");state={"schema_version":"1.0.0","retrieval_count":int(current.get("retrieval_count",0))+1,"success_streak":int(current.get("success_streak",0)),"next_due_bucket":"SHORT","hint_dependence":"HIGH","representation_success":list(current.get("representation_success") or []),"last_event_ref":event["event_id"],"last_event_sequence":event["event_sequence"],"previous_state_digest":previous_digest}
    if event.get("outcome")=="CORRECT":
        state["success_streak"]+=1;state["next_due_bucket"]="LONG" if state["success_streak"]>=3 else "MEDIUM"
    else:state["success_streak"]=0
    h=event.get("hint_level_used");state["hint_dependence"]="NONE" if h=="NO_HINT" else "LOW" if h in {"RETRIEVAL_CUE","REPRESENTATION_CUE"} else "MEDIUM" if h in {"MODEL_CUE","FIRST_MOVE_CUE"} else "HIGH"
    if event.get("outcome")=="CORRECT" and h in LOW_HINTS and event.get("representation_used") and event["representation_used"] not in state["representation_success"]:state["representation_success"].append(event["representation_used"])
    state["representation_success"]=sorted(state["representation_success"]);state["state_digest"]=digest(state);return state
