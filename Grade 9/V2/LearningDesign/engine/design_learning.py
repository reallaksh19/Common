#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

TEACHING_ROLES = {"RECONSTRUCT","WORKED_REASONING","MINIMAL_CONTRAST","MISCONCEPTION_REPAIR"}

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")

def digest(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def walk_keys(value):
    if isinstance(value, dict):
        for k,v in value.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_keys(v)

def _blocked(reason, refs):
    return {"schema_version":"1.0.0","status":"BLOCKED",
            "gaps":[{"gap_type":"LEARNING_DESIGN_GAP","reason":reason,"refs":sorted(set(refs))}]}

def _support_progression(full):
    if not full:
        empty={"support_features":[],"removed_since_previous":[]}
        return {k:copy.deepcopy(empty) for k in ("worked","guided","faded","independent")}
    return {
        "worked":{"support_features":["MODEL_SELECTED","FIRST_STEP_PROVIDED","INTERMEDIATE_STEPS_PROVIDED","ERROR_CHECK_CUE"],"removed_since_previous":[]},
        "guided":{"support_features":["FIRST_STEP_PROVIDED","ERROR_CHECK_CUE"],"removed_since_previous":["MODEL_SELECTED","INTERMEDIATE_STEPS_PROVIDED"]},
        "faded":{"support_features":["ERROR_CHECK_CUE"],"removed_since_previous":["FIRST_STEP_PROVIDED"]},
        "independent":{"support_features":[],"removed_since_previous":["ERROR_CHECK_CUE"]},
    }

def _make_step(target_id, seq, role, ob, payload, learner_action):
    return {
      "step_id":f"STEP-{target_id}-{seq:02d}",
      "role":role,
      "obligation_refs":[ob["obligation_id"]],
      "learner_job":ob.get("semantic_payload",{}).get("learner_job") or ob["description"],
      "payload":copy.deepcopy(payload),
      "learner_action":learner_action
    }

def _build_unit(target):
    obs=target["obligations"]
    by_kind={}
    for ob in obs: by_kind.setdefault(ob["kind"],[]).append(ob)
    steps=[]; seq=0
    def add(role,ob,payload,action):
        nonlocal seq
        seq+=1
        s=_make_step(target["target_id"],seq,role,ob,payload,action)
        steps.append(s); return s

    if target["readiness"]=="PROBE_FIRST":
        probes=by_kind.get("DIAGNOSTIC_PROBE",[])
        if not probes:
            raise ValueError(f"PROBE_FIRST target lacks DIAGNOSTIC_PROBE obligation: {target['target_id']}")
        for ob in probes:
            p=ob.get("semantic_payload",{})
            add("DIAGNOSTIC_PROBE",ob,{"probe_intent":p.get("probe_intent",""),"minimal_unrelated_load":True},True)
        extra=[o["obligation_id"] for o in obs if o["kind"]!="DIAGNOSTIC_PROBE"]
        if extra:
            raise ValueError(f"PROBE_FIRST contains premature teaching obligations: {extra}")
        return steps, _support_progression(False)

    for ob in by_kind.get("CONCEPTUAL_BRIDGE",[]):
        p=ob.get("semantic_payload",{})
        add("ANCHOR",ob,{"anchor_statement":p.get("anchor_statement",""),"mode":"USE_DEMONSTRATED_CAPABILITY"},False)
        add("GUIDED_ATTEMPT",ob,{"prompt_intent":"Use the demonstrated capability to initiate the next reasoning move.","support_features":["ERROR_CHECK_CUE"]},True)

    for ob in by_kind.get("RECONSTRUCTION",[]):
        p=ob.get("semantic_payload",{})
        add("PREDICT",ob,{"prompt_intent":"Predict what must remain invariant before a formal move."},True)
        add("RECONSTRUCT",ob,{"relation_or_object":p.get("relation_or_object"),"term_origins":p.get("term_origins",[]),"conditions":p.get("conditions",[]),"reconstruction_route":p.get("reconstruction_route",[])},False)
        add("GUIDED_ATTEMPT",ob,{"prompt_intent":"Reconstruct the relation with one cue removed.","support_features":["FIRST_STEP_PROVIDED","ERROR_CHECK_CUE"]},True)

    for ob in by_kind.get("REPRESENTATION_TRANSLATION",[]):
        p=ob.get("semantic_payload",{})
        add("REPRESENTATION_TRANSLATE",ob,{"from":p.get("from"),"to":p.get("to"),"translation_job":p.get("translation_job"),"invariant_to_preserve":p.get("invariant_to_preserve")},True)

    for ob in by_kind.get("MISCONCEPTION_CONTRAST",[]):
        p=ob.get("semantic_payload",{})
        add("PREDICT",ob,{"prompt_intent":"Predict which route preserves the target invariant before resolution."},True)
        add("MINIMAL_CONTRAST",ob,{"controlled_shared_features":p.get("controlled_shared_features",[]),"focal_difference":p.get("focal_difference",""),"prediction_required":bool(p.get("prediction_required",False))},False)
        add("GUIDED_ATTEMPT",ob,{"prompt_intent":"Use the focal difference to choose and justify the valid route.","support_features":["ERROR_CHECK_CUE"]},True)

    for ob in by_kind.get("MISCONCEPTION_REPAIR",[]):
        p=ob.get("semantic_payload",{})
        add("MISCONCEPTION_REPAIR",ob,{"wrong_model":p.get("wrong_model"),"discriminator":p.get("discriminator"),"repair_route":p.get("repair_route")},False)
        add("GUIDED_ATTEMPT",ob,{"prompt_intent":"Apply the repair route to a controlled case.","support_features":["ERROR_CHECK_CUE"]},True)

    worked_steps=[]
    for ob in by_kind.get("WORKED_REASONING",[]):
        p=ob.get("semantic_payload",{})
        worked_steps.append(add("WORKED_REASONING",ob,{"reasoning_moves":p.get("reasoning_moves",[]),"self_check":p.get("self_check",""),"answer_only":False},False))
        worked_steps.append(add("GUIDED_ATTEMPT",ob,{"prompt_intent":"Repeat the reasoning with intermediate steps removed.","support_features":["FIRST_STEP_PROVIDED","ERROR_CHECK_CUE"]},True))
        worked_steps.append(add("FADED_ATTEMPT",ob,{"prompt_intent":"Repeat with only a self-check cue.","support_features":["ERROR_CHECK_CUE"]},True))
        worked_steps.append(add("INDEPENDENT_ATTEMPT",ob,{"prompt_intent":"Solve without conceptual support.","support_features":[]},True))

    for ob in by_kind.get("VERIFICATION",[]):
        p=ob.get("semantic_payload",{})
        check_route=p.get("check_route","")
        for s in worked_steps:
            s["obligation_refs"].append(ob["obligation_id"])
            s["obligation_refs"]=sorted(set(s["obligation_refs"]))
            s["payload"]["verification_embedded"]=check_route
        add("VERIFICATION",ob,{"check_route":check_route,"self_initiated_required":target["readiness"]!="READY"},True)

    for ob in by_kind.get("TRANSFER",[]):
        p=ob.get("semantic_payload",{})
        add("TRANSFER",ob,{"changed_dimensions":p.get("changed_dimensions",[]),"non_isomorphic":bool(p.get("non_isomorphic",False))},True)

    for ob in by_kind.get("COMPLETION_EVIDENCE",[]):
        p=ob.get("semantic_payload",{})
        add("COMPLETION_EVIDENCE",ob,{"success_evidence":p.get("success_evidence",""),"independent":True},True)

    supported={"CONCEPTUAL_BRIDGE","RECONSTRUCTION","REPRESENTATION_TRANSLATION","MISCONCEPTION_CONTRAST","MISCONCEPTION_REPAIR","WORKED_REASONING","VERIFICATION","TRANSFER","COMPLETION_EVIDENCE"}
    unsupported=sorted({o["kind"] for o in obs}-supported)
    if unsupported:
        raise ValueError(f"unsupported obligation kinds: {unsupported}")
    return steps, _support_progression(bool(by_kind.get("WORKED_REASONING")))

def validate_design_semantics(plan, study_model, policy):
    forbidden=set(policy.get("forbidden_design_keys",[]))
    found=forbidden.intersection(set(walk_keys(plan)))
    if found:
        raise ValueError(f"forbidden design keys: {sorted(found)}")
    study_targets={t["target_id"]:t for t in study_model["targets"]}
    all_obs={o["obligation_id"]:(t,o) for t in study_model["targets"] for o in t["obligations"]}
    coverage={c["obligation_id"]:c for c in plan["obligation_coverage"]}
    if set(coverage)!=set(all_obs): raise ValueError("StudyModel obligation coverage mismatch")
    unit_by_target={u["target_ref"]:u for u in plan["units"]}
    if set(unit_by_target)!=set(study_targets): raise ValueError("StudyModel target set changed")
    stepmap={s["step_id"]:s for u in plan["units"] for s in u["choreography"]}
    for oid,c in coverage.items():
        if not c["realized_step_refs"]: raise ValueError(f"uncovered obligation: {oid}")
        for ref in c["realized_step_refs"]:
            if ref not in stepmap or oid not in stepmap[ref]["obligation_refs"]: raise ValueError(f"bad obligation coverage ref: {oid}->{ref}")
    for tid,src in study_targets.items():
        u=unit_by_target[tid]
        if u["study_treatment"]!=src["study_treatment"] or u["readiness"]!=src["readiness"]: raise ValueError(f"StudyModel treatment/readiness reclassified: {tid}")
        roles=[s["role"] for s in u["choreography"]]
        if src["readiness"]=="PROBE_FIRST" and roles[0]!="DIAGNOSTIC_PROBE": raise ValueError(f"PROBE_FIRST must start with diagnostic probe: {tid}")
        if "WORKED_REASONING" in roles:
            sp=u["support_progression"]; w,g,f,i=(set(sp[k]["support_features"]) for k in ("worked","guided","faded","independent"))
            if not (g < w and f < g and i < f): raise ValueError(f"fake fading: {tid}")
            if i: raise ValueError(f"independent attempt retains support: {tid}")
        def pos(role): return next((i for i,r in enumerate(roles) if r==role),None)
        if pos("RECONSTRUCT") is not None and pos("WORKED_REASONING") is not None and pos("RECONSTRUCT")>pos("WORKED_REASONING"): raise ValueError("reconstruction occurs after worked reasoning")
        if pos("MINIMAL_CONTRAST") is not None and pos("WORKED_REASONING") is not None and pos("MINIMAL_CONTRAST")>pos("WORKED_REASONING"): raise ValueError("contrast occurs after worked reasoning")
        if pos("TRANSFER") is not None and pos("INDEPENDENT_ATTEMPT") is not None and pos("TRANSFER")<pos("INDEPENDENT_ATTEMPT"): raise ValueError("transfer occurs before independent attempt")
        steps=u["choreography"]
        for idx,s in enumerate(steps):
            if s["role"] in TEACHING_ROLES:
                later=steps[idx+1:]; next_teach=next((j for j,x in enumerate(later) if x["role"] in TEACHING_ROLES),None); window=later if next_teach is None else later[:next_teach]
                if not any(x["learner_action"] for x in window): raise ValueError(f"teaching without learner action: {s['step_id']}")
            p=s["payload"]; role=s["role"]
            if role=="WORKED_REASONING" and (p.get("answer_only") or len(p.get("reasoning_moves",[]))<3 or not p.get("self_check")): raise ValueError("worked reasoning insufficient")
            elif role=="RECONSTRUCT" and (not p.get("relation_or_object") or len(p.get("term_origins",[]))<2 or not p.get("conditions") or len(p.get("reconstruction_route",[]))<3): raise ValueError("naked formula reconstruction")
            elif role=="MINIMAL_CONTRAST" and (not p.get("controlled_shared_features") or not p.get("focal_difference") or p.get("prediction_required") is not True): raise ValueError("uncontrolled contrast")
            elif role=="TRANSFER":
                dims=p.get("changed_dimensions",[])
                if not p.get("non_isomorphic") or not dims or set(dims)<= {"NUMBER_CHANGE"}: raise ValueError("number-only transfer")
            elif role=="REPRESENTATION_TRANSLATE" and not all(p.get(k) for k in ("from","to","translation_job","invariant_to_preserve")): raise ValueError("representation without translation job")
            elif role=="INDEPENDENT_ATTEMPT" and p.get("support_features"): raise ValueError("independent with conceptual hints")
        verify_ids=[o["obligation_id"] for o in src["obligations"] if o["kind"]=="VERIFICATION"]
        if verify_ids and "WORKED_REASONING" in roles:
            worked_family=[s for s in steps if s["role"] in {"WORKED_REASONING","GUIDED_ATTEMPT","FADED_ATTEMPT","INDEPENDENT_ATTEMPT"}]
            for vid in verify_ids:
                if not any(vid in s["obligation_refs"] and s["payload"].get("verification_embedded") for s in worked_family): raise ValueError(f"verification not integrated into reasoning path: {vid}")
    return True

def build_design(study_model, publication_view, publication_target, policy, **extra):
    payload={"study_model":study_model,"publication_view":publication_view,"publication_target":publication_target,"policy":policy,**extra}
    forbidden=set(policy.get("forbidden_input_keys",[])); found=forbidden.intersection(set(walk_keys(payload)))
    if found: return _blocked(f"forbidden producer input keys: {sorted(found)}", list(found))
    if publication_view.get("publication_planning_view_id") is None: return _blocked("missing frozen PublicationPlanningView", ["PublicationPlanningView"])
    units=[]; coverage=[]
    try:
        for target in study_model["targets"]:
            steps,support=_build_unit(target)
            units.append({"unit_id":"UNIT-"+target["target_id"],"target_ref":target["target_id"],"study_treatment":target["study_treatment"],"readiness":target["readiness"],"choreography":steps,"support_progression":support})
            for ob in target["obligations"]:
                realized=[s["step_id"] for s in steps if ob["obligation_id"] in s["obligation_refs"]]
                coverage.append({"obligation_id":ob["obligation_id"],"target_ref":target["target_id"],"realized_step_refs":realized})
    except ValueError as e: return _blocked(str(e), [study_model["learner_study_model_id"]])
    plan={"learning_design_id":f"LD-{study_model['learner_study_model_id']}-{policy['policy_version']}","schema_version":"1.0.0","learner_study_model_id":study_model["learner_study_model_id"],"study_model_digest":digest(study_model),"publication_planning_view_id":publication_view["publication_planning_view_id"],"publication_target_id":publication_target["publication_target_id"],"policy_version":policy["policy_version"],"units":units,"obligation_coverage":sorted(coverage,key=lambda x:x["obligation_id"]),"runtime_support_contract":{"max_same_route_failures":policy["max_same_route_failures"],"approved_rungs":copy.deepcopy(policy["approved_support_rungs"])}}
    try: validate_design_semantics(plan,study_model,policy)
    except ValueError as e: return _blocked(str(e), [study_model["learner_study_model_id"]])
    return {"schema_version":"1.0.0","status":"READY","learning_design_plan":plan}

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--study-model",required=True); ap.add_argument("--publication-view",required=True); ap.add_argument("--publication-target",required=True); ap.add_argument("--policy",required=True); ap.add_argument("--out")
    a=ap.parse_args(); load=lambda p: json.loads(Path(p).read_text())
    result=build_design(load(a.study_model),load(a.publication_view),load(a.publication_target),load(a.policy)); out=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if a.out: Path(a.out).write_text(out)
    else: sys.stdout.write(out)
if __name__=="__main__": main()
