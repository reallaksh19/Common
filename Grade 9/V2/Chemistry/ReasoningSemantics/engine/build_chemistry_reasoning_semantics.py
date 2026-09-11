#!/usr/bin/env python3
import argparse, copy, json
from pathlib import Path

ROLES={"READ_GIVEN","IDENTIFY_CHEMICAL_ENTITIES","IDENTIFY_REPRESENTATION_LEVEL","PARSE_FORMULA_OR_EQUATION","SELECT_RULE_OR_MODEL","CHECK_CONDITION_OR_EXCEPTION","TRANSLATE_REPRESENTATION","APPLY_CONSERVATION","TRACK_SPECIES_OR_STATE_CHANGE","COMPARE","CLASSIFY","INFER_FROM_OBSERVATION","EXECUTE_QUANTITATIVE_STEP","INTERPRET_CHEMICAL_MEANING","CHECK_ATOMS","CHECK_CHARGE","CHECK_UNITS","CHECK_CONDITIONS","VERIFY_RESULT"}
DEMAND_KEYS=["representation_translation","chemical_entity_tracking","formula_charge_parsing","condition_exception_handling","conservation_reasoning","reaction_process_reasoning","classification_discrimination","experimental_inference","structure_recognition","hidden_condition_load","reasoning_chain_length","concept_combination","quantitative_execution_load","verification_demand","time_pressure"]
VERIFY_ALLOWED={"CHECK_ATOMS","CHECK_CHARGE","CHECK_UNITS","CHECK_CONDITIONS","CHECK_SPECIES_IDENTITY","VERIFY_RESULT"}

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def fail(code,detail=""): raise ValueError(f"{code}: {detail}" if detail else code)
def unique(seq):
    out=[]
    for x in seq:
        if x not in out: out.append(x)
    return out

def validate_registry(registry,roles,badges):
    if set(roles["roles"])!=ROLES or len(roles["roles"])!=len(ROLES): fail("REASONING_ROLE_REGISTRY_INCOMPLETE")
    fams=registry["families"]; by_id={f["family_id"]:f for f in fams}
    if len(fams)<12: fail("PROBLEM_FAMILY_REGISTRY_TOO_THIN")
    if len(by_id)!=len(fams): fail("DUPLICATE_PROBLEM_FAMILY")
    for qf,fid in registry["question_family_aliases"].items():
        if fid not in by_id: fail("UNKNOWN_PROBLEM_FAMILY_ALIAS",qf)
    for f in fams:
        route=f["reasoning_route_template"]
        if not route: fail("REASONING_ROUTE_ROLE_INVALID",f["family_id"])
        if "SOLUTION_SUMMARY" in route: fail("REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY",f["family_id"])
        if any(x.startswith(("H1","H2","H3")) for x in route): fail("REASONING_ROUTE_EQUALS_HINT_COPY",f["family_id"])
        if any(x not in ROLES for x in route): fail("REASONING_ROUTE_ROLE_INVALID",f["family_id"])
        if not f["verification_route"]: fail("VERIFICATION_ROUTE_MISSING",f["family_id"])
        if any(k not in DEMAND_KEYS for k in f.get("demand_defaults",{})): fail("DEMAND_VECTOR_UNKNOWN_DIMENSION",f["family_id"])
        if f["family_id"]=="PF-MACRO_PARTICLE_SYMBOL_TRANSLATION" and not {"MACROSCOPIC","PARTICULATE","SYMBOLIC"}.issubset(set(f["representation_levels"])): fail("MACRO_PARTICLE_SYMBOLIC_TRANSLATION_COLLAPSED")
        if f["family_id"]=="PF-EVIDENCE_TO_CLAIM" and not {"OBSERVATION","CLAIM"}.issubset(set(f["entity_roles"])): fail("EXPERIMENTAL_OBSERVATION_AND_CLAIM_COLLAPSED")
        if f["family_id"]=="PF-STRUCTURE_SITE_REASONING" and "STRUCTURE" not in f["representation_requirements"]: fail("STRUCTURE_DEPENDENCY_DROPPED")
        if f["family_id"]=="PF-AGENT_ROLE_ASSIGNMENT" and not any("reputation" in x.lower() for x in f["transfer_boundaries"]): fail("REAGENT_MEMORIZATION_REPLACES_EQUATION_REASONING")
    if [x["badge"] for x in badges["thresholds"]] != ["FOUNDATION","STANDARD","DEEP","VERY_DEEP"]: fail("DEMAND_BADGE_POLICY_INVALID")
    if set(badges["prohibited_bases"])!={"SOURCE_DIFFICULTY_ONLY","KEYWORD_ONLY"}: fail("DIFFICULTY_UNEXPLAINED_SCALAR")
    return by_id

def choose_family(record,registry,by_id):
    qfs=record.get("problem_family_refs",[])
    if qfs:
        fid=registry["question_family_aliases"].get(qfs[0])
        if fid in by_id: return by_id[fid]
    for cap in record.get("canonical_capability_refs",[]):
        fid=registry["capability_family_defaults"].get(cap)
        if fid in by_id: return by_id[fid]
    fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",record.get("item_ref",record.get("obligation_id","unknown")))

def semantic_action(role):
    return {"READ_GIVEN":"Read only the chemically relevant givens and target.","IDENTIFY_CHEMICAL_ENTITIES":"Identify the species, particles, sites or apparatus carrying the chemistry.","IDENTIFY_REPRESENTATION_LEVEL":"Name the macroscopic, particulate or symbolic level.","PARSE_FORMULA_OR_EQUATION":"Parse symbols, subscripts, coefficients, charges and arrows without conflation.","SELECT_RULE_OR_MODEL":"Select the source-authorized rule or model matching givens and target.","CHECK_CONDITION_OR_EXCEPTION":"Check whether a stated condition or exception changes valid use.","TRANSLATE_REPRESENTATION":"Translate representations while preserving chemical identity and meaning.","APPLY_CONSERVATION":"Apply the explicitly required conservation ledger.","TRACK_SPECIES_OR_STATE_CHANGE":"Track the same chemical entity or state through the transformation.","COMPARE":"Compare alternatives on the stated chemical criterion.","CLASSIFY":"Assign the requested class only after evidence or rule is established.","INFER_FROM_OBSERVATION":"Separate observation from the chemical claim supported by it.","EXECUTE_QUANTITATIVE_STEP":"Execute only the source-authorized quantitative relation.","INTERPRET_CHEMICAL_MEANING":"State what the result means chemically.","CHECK_ATOMS":"Verify atom conservation where required.","CHECK_CHARGE":"Verify ionic/charge consistency where required.","CHECK_UNITS":"Verify units where a quantitative relation is authorized.","CHECK_CONDITIONS":"Verify decisive conditions/exceptions remain attached.","VERIFY_RESULT":"Check the result against identity, representation and target."}[role]

def normalize_verification(record,family):
    raw=record.get("verification_obligations",[]) or family["verification_route"]
    mapped=[x if x in VERIFY_ALLOWED else "VERIFY_RESULT" for x in raw]
    return unique(mapped or ["VERIFY_RESULT"])

def build_record(record,target,family,badges,scope_status):
    expected=record.get("reasoning_role_expectations",[])
    route=unique(family["reasoning_route_template"]+expected)
    if not route: fail("REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY",target)
    cond=list(record.get("conditions_exceptions",record.get("condition_model_refs",[])))
    if "conservation_obligations" in record: conservation=list(record.get("conservation_obligations",[]))
    else: conservation=list(family["conservation_requirements"])
    if family["condition_or_exception_requirements"] and scope_status=="ELIGIBLE_IN_SCOPE" and not cond and family["family_id"] in {"PF-RULE_WITH_EXCEPTION","PF-CONDITION_VALIDITY"}: fail("CONDITION_EXCEPTION_ROUTE_MISSING",target)
    if family["conservation_requirements"] and scope_status=="ELIGIBLE_IN_SCOPE" and not conservation: fail("CONSERVATION_REQUIREMENT_DROPPED",target)
    levels=list(record.get("representation_levels",[])) or list(family["representation_levels"])
    reps=list(record.get("representation_demands",record.get("representation_requirements",[])))
    if family["family_id"]=="PF-MACRO_PARTICLE_SYMBOL_TRANSLATION" and scope_status=="ELIGIBLE_IN_SCOPE" and "TRANSLATE_REPRESENTATION" in expected:
        if "SYMBOLIC" not in levels or not ({"PARTICULATE","MACROSCOPIC"}&set(levels)): fail("MACRO_PARTICLE_SYMBOLIC_TRANSLATION_COLLAPSED",target)
    if family["family_id"]=="PF-STRUCTURE_SITE_REASONING" and "STRUCTURE" not in reps: fail("STRUCTURE_DEPENDENCY_DROPPED",target)
    verification=normalize_verification(record,family)
    if not verification: fail("VERIFICATION_ROUTE_MISSING",target)
    dims={k:0 for k in DEMAND_KEYS}; dims.update(family.get("demand_defaults",{}))
    dims["reasoning_chain_length"]=max(dims["reasoning_chain_length"],1 if len(route)<=3 else 2 if len(route)<=5 else 3)
    dims["concept_combination"]=max(dims["concept_combination"],min(3,max(0,len(record.get("canonical_concept_refs",[]))-1)))
    if cond:
        dims["condition_exception_handling"]=max(dims["condition_exception_handling"],2); dims["hidden_condition_load"]=max(dims["hidden_condition_load"],1)
    if conservation: dims["conservation_reasoning"]=max(dims["conservation_reasoning"],2)
    if len(levels)>1: dims["representation_translation"]=max(dims["representation_translation"],2)
    score=sum(dims.values()); badge=next(x["badge"] for x in badges["thresholds"] if score<=x["max_score"])
    if badge in {"DEEP","VERY_DEEP"} and len(route)<4: fail("HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE",target)
    steps=[{"step_index":i,"role":role,"capability_refs":list(record.get("canonical_capability_refs",[])),"representation_levels":levels,"chemical_entity_refs":list(record.get("chemical_entity_refs",[])),"condition_or_exception_refs":cond,"conservation_refs":conservation,"semantic_action":semantic_action(role)} for i,role in enumerate(route,1)]
    return {"target_ref":target,"scope_status":scope_status,"problem_family_ref":family["family_id"],"reasoning_route":{"route_id":f"ROUTE-{target}","subject":"CHEMISTRY","target_ref":target,"problem_family_ref":family["family_id"],"scope_status":scope_status,"steps":steps,"verification_route":verification,"learner_support_independent":True},"condition_validity":{"target_ref":target,"required_conditions":cond,"required_exceptions":[x for x in cond if "EXCEPTION" in x.upper()],"model_validity_statement":"Apply only within the recorded condition/exception boundary." if cond else "No additional condition/exception is required by this record.","status":"EXPLICIT" if cond else "NOT_REQUIRED"},"verification_route":{"target_ref":target,"checkpoints":verification,"status":"CLOSED" if scope_status=="ELIGIBLE_IN_SCOPE" else "UNRESOLVED"},"demand_vector":{"target_ref":target,"vector_version":"1.0.0","dimensions":dims,"source_difficulty_preserved_separately":True,"source_difficulty":record.get("source_difficulty")},"guide_demand_badge":badge if scope_status=="ELIGIBLE_IN_SCOPE" else None}

def build_semantics(source_ledger,question_bindings,registry,role_registry,badge_policy):
    by_id=validate_registry(registry,role_registry,badge_policy)
    source=[]
    for r in source_ledger["obligations"]:
        source.append(build_record(r,r["obligation_id"],choose_family(r,registry,by_id),badge_policy,r["scope_status"]))
    questions=[]
    for r in question_bindings["bindings"]:
        questions.append(build_record(r,r["item_ref"],choose_family(r,registry,by_id),badge_policy,r["scope_status"]))
    return {"bundle_id":"CHEM-C-D-SEMANTICS-v1","schema_version":"1.0.0","subject":"CHEMISTRY","source_semantics":source,"question_semantics":questions,"summary":{"source_record_count":len(source),"question_record_count":len(questions),"eligible_question_count":sum(x["scope_status"]=="ELIGIBLE_IN_SCOPE" for x in questions),"reasoning_route_is_hint_independent":True,"difficulty_scalar_is_not_authority":True}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source-ledger",required=True); ap.add_argument("--question-bindings",required=True); ap.add_argument("--family-registry",required=True); ap.add_argument("--role-registry",required=True); ap.add_argument("--badge-policy",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    out=build_semantics(load(a.source_ledger),load(a.question_bindings),load(a.family_registry),load(a.role_registry),load(a.badge_policy))
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
