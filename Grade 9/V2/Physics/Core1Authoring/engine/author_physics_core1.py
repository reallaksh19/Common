#!/usr/bin/env python3
import argparse, copy, hashlib, json
from collections import Counter
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
PHYS=ROOT.parent
CONTRACTS=ROOT/"contracts"

FULL={"ACTIVE_STUDY","REPAIR_BEFORE","REPAIR_IN_UNIT"}
GRAPH_CAPS={"PHY-CAP-REPRESENTATION-TRANSLATE","PHY-CAP-XT-SLOPE-VELOCITY","PHY-CAP-GRAPH-ACCELERATION","PHY-CAP-VT-SIGNED-AREA"}

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v,field=None):
    x=copy.deepcopy(v)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()
def stable(prefix,payload): return prefix+digest(payload)[:16]
def fail(code,detail=""): raise ValueError(f"{code}: {detail}" if detail else code)
def uniq(xs): return sorted(set(xs))

def _validate_schema(v,name):
    Draft202012Validator(load(CONTRACTS/name)).validate(v)

def validate_pck_registries(candidates,promotions):
    if candidates.get("subject")!="PHYSICS" or candidates.get("registry_class")!="CANDIDATE":
        fail("PCK_CANDIDATE_REGISTRY_INVALID")
    if candidates.get("registry_digest")!=digest(candidates,"registry_digest"):
        fail("PCK_CANDIDATE_REGISTRY_DIGEST_MISMATCH")
    if promotions.get("subject")!="PHYSICS":
        fail("PCK_PROMOTION_REGISTRY_INVALID")
    if promotions.get("registry_digest")!=digest(promotions,"registry_digest"):
        fail("PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH")
    by={}
    for a in candidates["asset_documents"]:
        if a["asset_id"] in by: fail("DUPLICATE_PCK_ASSET",a["asset_id"])
        if a["asset_digest"]!=digest(a,"asset_digest"): fail("PCK_ASSET_DIGEST_MISMATCH",a["asset_id"])
        if a["lifecycle_status"]!="CANDIDATE" or a["review"]["status"]!="PENDING_HUMAN_REVIEW":
            fail("PCK_CANDIDATE_LIFECYCLE_INVALID",a["asset_id"])
        by[a["asset_id"]]=a
    promoted={}
    for p in promotions["promotions"]:
        if p["asset_id"] not in by: fail("PCK_PROMOTION_UNKNOWN_ASSET",p["asset_id"])
        if p["asset_digest"]!=by[p["asset_id"]]["asset_digest"]: fail("PCK_PROMOTION_ASSET_DIGEST_MISMATCH",p["asset_id"])
        if p["status"]!="PROMOTED" or p["subject_review_status"]!="APPROVED_BY_HUMAN" or p["pedagogy_review_status"]!="APPROVED_BY_HUMAN":
            fail("PCK_PROMOTION_REQUIRED",p["asset_id"])
        if len(p["human_review_evidence_refs"])<2: fail("PCK_PROMOTION_REQUIRED",p["asset_id"])
        if p["promotion_digest"]!=digest(p,"promotion_digest"): fail("PCK_PROMOTION_DIGEST_MISMATCH",p["asset_id"])
        promoted[p["asset_id"]]=p
    return by,promoted

def validate_policy_digests(author_profile,scope_policy,problem_profile):
    for obj,field,code in [
        (author_profile,"profile_digest","INSTRUCTIONAL_AUTHORING_PROFILE_DIGEST_MISMATCH"),
        (scope_policy,"policy_digest","CORE1_SCOPE_POLICY_DIGEST_MISMATCH"),
        (problem_profile,"profile_digest","PROBLEM_AUTHORING_PROFILE_DIGEST_MISMATCH"),
    ]:
        if obj.get(field)!=digest(obj,field): fail(code)

def asset_matches(cap,by):
    return sorted([a for a in by.values() if cap in a["capability_refs"]],key=lambda a:(len(a["capability_refs"]),a["asset_id"]))

def _payloads(assets,key):
    vals=[]
    for a in assets:
        v=a[key]
        if isinstance(v,list): vals.extend(v)
        else: vals.append(v)
    return vals

def _stage(name,payload): return {"stage":name,"payload":payload}

def verification_checks(record,assets):
    checks={"UNITS_DIMENSIONS","MODEL_CONSISTENCY"}
    if any(x["reference_frame"]["required"] or x["sign_convention"]["required"] for x in record["system_frame_obligations"]):
        checks.add("SIGN_DIRECTION")
    if any(x["phase_kind"]!="SINGLE_PHASE" or x["continuity_state_refs"] for x in record["state_phase_obligations"]):
        checks.add("CONTINUITY")
    if record["law_refs"] or record["physical_model_refs"]:
        checks.update({"MAGNITUDE_PLAUSIBILITY","LIMITING_OR_SCALING_CASE"})
    checks.update(record["verification_requirements"])
    for a in assets:
        for item in a["verification_method"]:
            if "unit" in item.lower(): checks.add("UNITS_DIMENSIONS")
            if "sign" in item.lower() or "direction" in item.lower(): checks.add("SIGN_DIRECTION")
    return sorted(checks)

def equation_contract(record,assets,treatment):
    applies=bool(record["law_refs"])
    if treatment=="PROBE_FIRST":
        return {"applies":applies,"mode":"PROBE_FIRST" if applies else "NO_EQUATION","see_equation":[],
                "realize_terms":[],"understand_origin":[],"connect_transfer":[],"unusual_features":[],
                "explanation_deferred_until_probe":True}
    if treatment=="READY_VERIFY_ONLY":
        return {"applies":applies,"mode":"VERIFY_ONLY" if applies else "NO_EQUATION",
                "see_equation":list(record["law_refs"]) if applies else [],
                "realize_terms":["VERIFY_EXISTING_TERM_MEANING"] if applies else [],
                "understand_origin":["VERIFY_MODEL_VALIDITY_AND_ORIGIN_WITHOUT_FULL_RETEACH"] if applies else [],
                "connect_transfer":["INDEPENDENT_PHYSICAL_CHECK"] if applies else [],
                "unusual_features":uniq(_payloads(assets,"equation_features_to_explain")) if assets else [],
                "explanation_deferred_until_probe":False}
    return {"applies":applies,"mode":"FULL_LEARNING" if applies else "NO_EQUATION",
            "see_equation":list(record["law_refs"]) if applies else [],
            "realize_terms":_payloads(assets,"ordinary_language_bridge") if applies else [],
            "understand_origin":uniq(_payloads(assets,"relation_reconstruction_route")+_payloads(assets,"model_validity_cue")) if applies else [],
            "connect_transfer":uniq(_payloads(assets,"transfer_family")) if applies else [],
            "unusual_features":uniq(_payloads(assets,"equation_features_to_explain")),
            "explanation_deferred_until_probe":False}

def graph_semantics(record,assets):
    required=record["capability_ref"] in GRAPH_CAPS or any(a["graph_semantics_required"] for a in assets)
    return {"required":required,
            "operations":["HEIGHT","SLOPE","AREA"] if required else [],
            "translation_chain":["WORDS","MOTION_PICTURE","GRAPH","EQUATION_OR_GRAPH_OPERATION"] if required else []}

def state_handoff(record,assets):
    required=any(a["state_handoff_required"] for a in assets) or any(
        x["phase_kind"]!="SINGLE_PHASE" or bool(x["continuity_state_refs"]) for x in record["state_phase_obligations"]
    )
    return {"required":required,"visible_terminal_to_next_initial":required}

def build_problem_plans(record,assets,problem_profile):
    if not record["problem_family_refs"]:
        fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",record["capability_ref"])
    family=sorted(record["problem_family_refs"])[0]
    refs=[a["asset_id"] for a in assets]
    out=[]
    for role in problem_profile["roles"]:
        seed={"capability":record["capability_ref"],"role":role,"family":family,"pck":refs}
        plan={
          "plan_id":stable("PHY-P-G-PROB-",seed),
          "role":role,
          "capability_ref":record["capability_ref"],
          "problem_family_ref":family,
          "must_be_new_instance":True,
          "source_question_reuse":False,
          "source_question_refs":[],
          "surface_changes":list(problem_profile["default_surface_changes"]),
          "inherited_model_validity_obligations":copy.deepcopy(record["model_validity_obligations"]),
          "inherited_verification_requirements":list(record["verification_requirements"]),
          "pck_asset_refs":refs,
          "plan_digest":""
        }
        plan["plan_digest"]=digest(plan,"plan_digest")
        _validate_schema(plan,"physics-problem-authoring-plan.schema.json")
        out.append(plan)
    return out

def full_stages(record,assets,problem_plans,author_profile):
    pmap={p["role"]:p["plan_id"] for p in problem_plans}
    anchors=_payloads(assets,"physical_anchor")
    setup=[a["system_frame_setup"] for a in assets]
    contrast=[a["minimal_contrast"] for a in assets]
    stages=[
      _stage("PHENOMENON",{"physical_anchors":anchors}),
      _stage("DEFINE_SYSTEM",{"system_definitions":[x["system_definition"] for x in setup],"source_obligations":record["system_frame_obligations"]}),
      _stage("CHOOSE_FRAME_SIGN",{"frame_rules":[x["frame_rule"] for x in setup],"sign_rules":[x["sign_rule"] for x in setup],"source_obligations":record["system_frame_obligations"]}),
      _stage("REPRESENT",{"representation_path":uniq(_payloads(assets,"representation_path")),"source_requirements":record["representation_requirements"]}),
      _stage("NOTICE_DECISIVE_FEATURE",{"decisive_features":[x["decisive_feature"] for x in contrast]}),
      _stage("ORDINARY_LANGUAGE",{"bridges":_payloads(assets,"ordinary_language_bridge")}),
      _stage("CHECK_MODEL_VALIDITY",{"cues":_payloads(assets,"model_validity_cue"),"source_obligations":record["model_validity_obligations"]}),
      _stage("RECONSTRUCT",{"routes":_payloads(assets,"relation_reconstruction_route"),"law_refs":record["law_refs"]}),
      _stage("MINIMAL_CONTRAST",{"contrasts":contrast,"wrong_models":_payloads(assets,"common_wrong_model"),"repair_routes":_payloads(assets,"repair_route")}),
      _stage("WORKED_REASONING",{"problem_plan_ref":pmap["WORKED"],"family_refs":record["problem_family_refs"],"answer_only":False}),
      _stage("GUIDED_ATTEMPT",{"problem_plan_ref":pmap["GUIDED"],"support":"HIGH"}),
      _stage("FADED_ATTEMPT",{"problem_plan_ref":pmap["FADED"],"support":"REDUCED"}),
      _stage("INDEPENDENT_ATTEMPT",{"problem_plan_ref":pmap["INDEPENDENT"],"support":"NONE"}),
      _stage("PHYSICAL_VERIFICATION",{"checks":verification_checks(record,assets),"verification_route_refs":record["verification_route_refs"]}),
      _stage("TRANSFER",{"problem_plan_ref":pmap["TRANSFER"],"transfer_families":_payloads(assets,"transfer_family")}),
    ]
    expected=author_profile["full_learning_stages"]
    if [s["stage"] for s in stages]!=expected: fail("CORE1_STAGE_PROFILE_DRIFT",record["capability_ref"])
    return stages

def build_core1(study_model,candidates,promotions,author_profile,scope_policy,problem_profile,generation_mode="PRE_REVIEW"):
    if generation_mode not in {"PRE_REVIEW","PRODUCTION"}: fail("CORE1_GENERATION_MODE_INVALID")
    validate_policy_digests(author_profile,scope_policy,problem_profile)
    if study_model["study_model_digest"]!=digest(study_model,"study_model_digest"):
        fail("STUDYMODEL_DIGEST_MISMATCH")
    by,promoted=validate_pck_registries(candidates,promotions)
    lessons=[]
    for record in sorted(study_model["capability_records"],key=lambda x:x["capability_ref"]):
        cap=record["capability_ref"]; treatment=record["treatment"]
        matches=asset_matches(cap,by)
        selected=[]
        promotion_status="NOT_REQUIRED_FOR_TREATMENT"
        if treatment in FULL:
            if not matches: fail("PCK_COVERAGE_GAP",cap)
            if generation_mode=="PRODUCTION":
                selected=[a for a in matches if a["asset_id"] in promoted]
                if not selected: fail("PCK_PROMOTION_REQUIRED",cap)
                promotion_status="PROMOTED"
            else:
                selected=matches
                promotion_status="PRE_REVIEW_ONLY"
        elif treatment=="READY_VERIFY_ONLY":
            selected=[]
        elif treatment=="PROBE_FIRST":
            selected=[]
        else:
            fail("UNKNOWN_TREATMENT",treatment)

        problem_plans=[]
        if treatment in FULL:
            problem_plans=build_problem_plans(record,selected,problem_profile)
            stages=full_stages(record,selected,problem_plans,author_profile)
        elif treatment=="READY_VERIFY_ONLY":
            stages=[
              _stage("ACTIVATE",{"mode":"BRIEF_ACTIVATION","canonical_refs":uniq(record["law_refs"]+record["physical_model_refs"])}),
              _stage("VERIFY",{"checks":verification_checks(record,[]),"independent":True}),
            ]
        else:
            stages=[_stage("DIAGNOSTIC_PROBE",{"probe_requirements":record["probe_requirements"],"explanation_before_probe":False})]

        lesson={
          "lesson_id":stable("PHY-P-G-LESSON-",{"cap":cap,"treatment":treatment,"scope":study_model["study_scope_digest"]}),
          "capability_ref":cap,"treatment":treatment,
          "source_scope_trace_item_refs":list(record["source_scope_trace_item_refs"]),
          "pck_asset_refs":[a["asset_id"] for a in selected],
          "promotion_status":promotion_status,
          "problem_family_refs":list(record["problem_family_refs"]),
          "system_frame_obligations":copy.deepcopy(record["system_frame_obligations"]),
          "state_phase_obligations":copy.deepcopy(record["state_phase_obligations"]),
          "model_validity_obligations":copy.deepcopy(record["model_validity_obligations"]),
          "representation_requirements":list(record["representation_requirements"]),
          "verification_requirements":list(record["verification_requirements"]),
          "instructional_stages":stages,
          "equation_contract":equation_contract(record,selected,treatment),
          "graph_semantics":graph_semantics(record,selected),
          "state_handoff":state_handoff(record,selected),
          "physical_verification":{"checks":verification_checks(record,selected)},
          "problem_authoring_plans":problem_plans,
          "lesson_digest":""
        }
        lesson["lesson_digest"]=digest(lesson,"lesson_digest")
        _validate_schema(lesson,"physics-core1-lesson.schema.json")
        lessons.append(lesson)

    counts=Counter(x["treatment"] for x in lessons)
    plan={
      "plan_id":stable("PHY-P-G-CORE1-",{"study_model":study_model["study_model_id"],"mode":generation_mode,"candidate_digest":candidates["registry_digest"],"promotion_digest":promotions["registry_digest"]}),
      "schema_version":"1.0.0","subject":"PHYSICS",
      "source_study_model_ref":study_model["study_model_id"],"source_study_model_digest":study_model["study_model_digest"],
      "generation_mode":generation_mode,
      "release_status":"PRODUCER_LEGAL" if generation_mode=="PRODUCTION" else "PRE_REVIEW_ONLY",
      "candidate_registry_ref":candidates["registry_id"],"promotion_registry_ref":promotions["registry_id"],
      "lessons":lessons,"scope_complete":True,"original_assessment_unspoiled":True,
      "summary":{"lesson_count":len(lessons),"treatment_counts":dict(sorted(counts.items())),
                 "full_learning_lesson_count":sum(counts[t] for t in FULL),
                 "promoted_pck_required_count":sum(counts[t] for t in FULL)},
      "plan_digest":""
    }
    plan["plan_digest"]=digest(plan,"plan_digest")
    validate_core1(plan,study_model,candidates,promotions,author_profile,scope_policy,problem_profile)
    _validate_schema(plan,"physics-core1-study-plan.schema.json")
    return plan

def validate_core1(plan,study_model,candidates,promotions,author_profile,scope_policy,problem_profile):
    validate_policy_digests(author_profile,scope_policy,problem_profile)
    by,promoted=validate_pck_registries(candidates,promotions)
    if plan["plan_digest"]!=digest(plan,"plan_digest"): fail("CORE1_PLAN_DIGEST_MISMATCH")
    expected={x["capability_ref"]:x for x in study_model["capability_records"]}
    got={x["capability_ref"]:x for x in plan["lessons"]}
    if set(got)!=set(expected) or len(got)!=len(plan["lessons"]):
        fail("CORE1_IS_ONLY_A_REPAIR_MEMO")
    if not plan.get("scope_complete") or not plan.get("original_assessment_unspoiled"):
        fail("CORE1_IS_ONLY_A_REPAIR_MEMO")
    for cap,lesson in got.items():
        record=expected[cap]
        if lesson["lesson_digest"]!=digest(lesson,"lesson_digest"): fail("CORE1_LESSON_DIGEST_MISMATCH",cap)
        if lesson["treatment"]!=record["treatment"]: fail("CORE1_TREATMENT_DRIFT",cap)
        if set(lesson["source_scope_trace_item_refs"])!=set(record["source_scope_trace_item_refs"]):
            fail("STUDYMODEL_WITHOUT_SOURCE_SCOPE_TRACE",cap)
        if lesson["model_validity_obligations"]!=record["model_validity_obligations"]:
            fail("MODEL_VALIDITY_CONDITION_DROPPED",cap)
        if lesson["system_frame_obligations"]!=record["system_frame_obligations"]:
            fail("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_CORE1",cap)
        if lesson["state_phase_obligations"]!=record["state_phase_obligations"]:
            fail("STATE_PHASE_REQUIREMENT_DROPPED_FROM_CORE1",cap)
        if set(lesson["problem_family_refs"])!=set(record["problem_family_refs"]):
            fail("PROBLEM_FAMILY_SCOPE_DRIFT",cap)
        if set(lesson["verification_requirements"])!=set(record["verification_requirements"]):
            fail("PHYSICAL_VERIFICATION_SCOPE_DRIFT",cap)

        stages=[s["stage"] for s in lesson["instructional_stages"]]
        if record["treatment"] in FULL:
            if stages!=author_profile["full_learning_stages"]:
                if "RECONSTRUCT" not in stages: fail("FULL_LEARNING_TREATMENT_WITHOUT_PHYSICAL_RECONSTRUCTION",cap)
                fail("CORE1_IS_ONLY_A_REPAIR_MEMO",cap)
            if not lesson["pck_asset_refs"]: fail("PCK_COVERAGE_GAP",cap)
            if plan["generation_mode"]=="PRODUCTION":
                if not all(a in promoted for a in lesson["pck_asset_refs"]):
                    fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY",cap)
            else:
                if lesson["promotion_status"]!="PRE_REVIEW_ONLY": fail("PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY",cap)
            eq=lesson["equation_contract"]
            if record["law_refs"] and (not eq["applies"] or not eq["see_equation"] or not eq["realize_terms"] or not eq["understand_origin"] or not eq["connect_transfer"]):
                fail("NAKED_EQUATION_COUNTS_AS_CONCEPT_TEACHING",cap)
            for pp in lesson["problem_authoring_plans"]:
                if pp["plan_digest"]!=digest(pp,"plan_digest"): fail("PROBLEM_AUTHORING_PLAN_DIGEST_MISMATCH",pp["plan_id"])
                if not pp["problem_family_ref"]: fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",cap)
                if pp["source_question_reuse"] or pp["source_question_refs"] or not pp["must_be_new_instance"]:
                    fail("CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE",cap)
                if pp["problem_family_ref"] not in record["problem_family_refs"]:
                    fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",cap)
                if len(pp["surface_changes"])<problem_profile["minimum_surface_changes"]:
                    fail("CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE",cap)
                if pp["inherited_model_validity_obligations"]!=record["model_validity_obligations"]:
                    fail("MODEL_VALIDITY_CONDITION_DROPPED",cap)
            if lesson["state_handoff"]["required"] and not lesson["state_handoff"]["visible_terminal_to_next_initial"]:
                fail("MULTIPHASE_TEACHING_WITHOUT_STATE_HANDOFF",cap)
            if lesson["graph_semantics"]["required"]:
                if set(lesson["graph_semantics"]["operations"])!={"HEIGHT","SLOPE","AREA"} or not lesson["graph_semantics"]["translation_chain"]:
                    fail("GRAPH_TEACHING_WITHOUT_HEIGHT_SLOPE_AREA_SEMANTICS",cap)
        elif record["treatment"]=="READY_VERIFY_ONLY":
            if stages!=author_profile["ready_stages"] or lesson["pck_asset_refs"] or lesson["problem_authoring_plans"]:
                fail("READY_CONTENT_PADDED_INTO_FULL_RETEACH",cap)
        elif record["treatment"]=="PROBE_FIRST":
            if stages!=author_profile["probe_first_stages"] or lesson["pck_asset_refs"]:
                fail("PROBE_FIRST_EXPLANATION_LEAK",cap)
            if not lesson["instructional_stages"][0]["payload"].get("probe_requirements"):
                fail("PROBE_REQUIREMENT_DROPPED",cap)
        checks=lesson["physical_verification"]["checks"]
        if len(checks)<author_profile["minimum_physical_verification_checks"] or checks==["NUMBER_ONLY"] or "NUMBER_ONLY" in checks:
            fail("PHYSICAL_CHECK_REDUCED_TO_NUMBER_ONLY",cap)
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--study-model",required=True); ap.add_argument("--pck-candidates",required=True)
    ap.add_argument("--pck-promotions",required=True); ap.add_argument("--author-profile",required=True)
    ap.add_argument("--scope-policy",required=True); ap.add_argument("--problem-profile",required=True)
    ap.add_argument("--mode",choices=["PRE_REVIEW","PRODUCTION"],default="PRE_REVIEW")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    plan=build_core1(load(a.study_model),load(a.pck_candidates),load(a.pck_promotions),
                     load(a.author_profile),load(a.scope_policy),load(a.problem_profile),a.mode)
    Path(a.out).write_text(json.dumps(plan,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"plan_id":plan["plan_id"],"release_status":plan["release_status"],"plan_digest":plan["plan_digest"]},sort_keys=True))
if __name__=="__main__": main()
