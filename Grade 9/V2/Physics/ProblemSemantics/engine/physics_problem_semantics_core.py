#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter
from pathlib import Path

D=Path(__file__).resolve().parents[1]
PHYSICS=D.parent
sys.path.insert(0,str(PHYSICS/"AssessmentScope"/"engine"))
from reconcile_physics_assessment_scope import reconcile

CANONICAL_ROLES={"READ_PHENOMENON","DEFINE_SYSTEM","CHOOSE_FRAME","REPRESENT","IDENTIFY_PHASES","EXTRACT_KNOWNS_AND_HIDDEN_FACTS","SELECT_MODEL","CHECK_MODEL_VALIDITY","PROPAGATE_STATE","CHOOSE_RELATION","SOLVE","INTERPRET_SIGN_DIRECTION","CHECK_UNITS","CHECK_CONTINUITY_OR_BOUNDARY","VERIFY_PHYSICAL_PLAUSIBILITY","INTERPRET_RESULT"}
DIMENSIONS={"physical_model_selection","reference_frame_sign_load","representation_translation","state_tracking_load","phase_count","vector_spatial_reasoning","graph_interpretation_load","equation_construction_or_elimination","hidden_condition_load","reasoning_chain_length","constraint_density","concept_combination","verification_demand","numerical_execution_load","time_pressure"}
BAD_ROUTE_KEYS={"hint","hint_text","hint_refs","solution","solution_text","worked_answer","final_answer","answer","support_level","learner_state","diagnosis","misconception","treatment","attempt_set","observed_answer"}
GRAPH_OPERATIONS={"SIGNED_AREA","AREA_MAGNITUDE","ZERO_CROSSING","SLOPE","HEIGHT","CURVATURE","OPTION_DISCRIMINATION","UNRESOLVED_DUE_SOURCE"}

def cb(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def dg(x): return hashlib.sha256(cb(x)).hexdigest()
def dwo(x,k):
    y=copy.deepcopy(x); y.pop(k,None); return dg(y)
def fail(code,detail=""): raise ValueError(f"{code}: {detail}" if detail else code)
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
def idx(rows,key,code):
    out={}
    for r in rows:
        if r[key] in out: fail(code,r[key])
        out[r[key]]=r
    return out

def scan_forbidden(x,path="root"):
    if isinstance(x,dict):
        for k,v in x.items():
            lk=k.lower()
            if lk in BAD_ROUTE_KEYS or any(token in lk for token in ["hint_text","solution_text","final_answer","worked_answer"]):
                code="REASONING_ROUTE_EQUALS_HINT_COPY" if "hint" in lk or "support" in lk else "REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY"
                fail(code,f"{path}.{k}")
            scan_forbidden(v,f"{path}.{k}")
    elif isinstance(x,list):
        for i,v in enumerate(x): scan_forbidden(v,f"{path}[{i}]")

def validate_role_registry(reg,scope_authority):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("REASONING_ROLE_REGISTRY_DIGEST_MISMATCH")
    roles=idx(reg["roles"],"role_id","DUPLICATE_REASONING_ROLE")
    if set(roles)!=CANONICAL_ROLES: fail("REASONING_ROLE_REGISTRY_COVERAGE")
    if any(r["learner_support_owner"] or r["solution_owner"] for r in roles.values()): fail("REASONING_ROUTE_AUTHORITY_DRIFT")
    aliases=reg["scope_role_aliases"]
    upstream=set(scope_authority["reasoning_role_expectations"])
    if set(aliases)!=upstream: fail("SCOPE_REASONING_ROLE_ALIAS_COVERAGE",f"missing={sorted(upstream-set(aliases))},extra={sorted(set(aliases)-upstream)}")
    for sr,a in aliases.items():
        if a["coverage_mode"] not in {"ALL","ANY"} or not a["canonical_roles"] or any(r not in roles for r in a["canonical_roles"]): fail("SCOPE_REASONING_ROLE_ALIAS_INVALID",sr)
    return roles,aliases

def validate_family_registry(reg,scope_authority,roles):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("PROBLEM_FAMILY_REGISTRY_DIGEST_MISMATCH")
    if reg["upstream_scope_authority_ref"]!=scope_authority["authority_id"] or reg["upstream_scope_authority_digest"]!=scope_authority["authority_digest"]: fail("PROBLEM_FAMILY_SCOPE_AUTHORITY_MISMATCH")
    scope_fams={x["problem_family_id"] for x in scope_authority["problem_families"]}; caps={x["capability_id"] for x in scope_authority["capabilities"]}
    reps=set(scope_authority["representation_identities"]); models=set(scope_authority["physical_model_identities"]); laws=set(scope_authority["law_identities"]); obligations=set(scope_authority["verification_obligation_identities"]); states=set(scope_authority["state_variable_identities"])
    out=idx(reg["families"],"family_id","DUPLICATE_PROBLEM_FAMILY")
    if set(out)!=scope_fams: fail("PROBLEM_FAMILY_IDENTITY_COVERAGE",f"missing={sorted(scope_fams-set(out))}, extra={sorted(set(out)-scope_fams)}")
    for f in out.values():
        fid=f["family_id"]
        if f["family_digest"]!=dwo(f,"family_digest"): fail("PROBLEM_FAMILY_DIGEST_MISMATCH",fid)
        if f["semantic_owner_phase"]!="P-D": fail("PROBLEM_FAMILY_AUTHORITY_DRIFT",fid)
        if any(c not in caps for c in f["canonical_capability_refs"]): fail("UNKNOWN_PROBLEM_FAMILY_CAPABILITY",fid)
        if any(s not in states for s in f["state_variables"]): fail("UNKNOWN_PROBLEM_FAMILY_STATE_VARIABLE",fid)
        declared_reps=set(f["representation_requirements"]["required_refs"]+f["representation_requirements"].get("optional_refs",[]))
        if any(r not in reps for r in declared_reps): fail("UNKNOWN_PROBLEM_FAMILY_REPRESENTATION",fid)
        if any(m not in models for m in f["model_refs"]): fail("UNKNOWN_PROBLEM_FAMILY_MODEL",fid)
        if any(l not in laws for l in f["law_refs"]): fail("UNKNOWN_PROBLEM_FAMILY_LAW",fid)
        route_roles=[s["role"] for s in f["reasoning_route_template"]]
        if any(r not in roles for r in route_roles): fail("UNKNOWN_REASONING_ROLE",fid)
        scan_forbidden(f["reasoning_route_template"],fid)
        for s in f["reasoning_route_template"]:
            if any(c not in caps for c in s["capability_refs"]): fail("UNKNOWN_ROUTE_CAPABILITY",fid)
            if any(r not in declared_reps for r in s["representation_refs"]): fail("PROBLEM_FAMILY_REPRESENTATION_DECLARATION_GAP",fid)
            if any(m not in models for m in s["model_refs"]): fail("UNKNOWN_ROUTE_MODEL",fid)
            if any(l not in laws for l in s["law_refs"]): fail("UNKNOWN_ROUTE_LAW",fid)
            if any(o not in obligations for o in s["verification_checkpoint_refs"]): fail("UNKNOWN_ROUTE_VERIFICATION_OBLIGATION",fid)
        model_required=bool(f["model_validity_conditions"])
        if model_required and "CHECK_MODEL_VALIDITY" not in route_roles: fail("MODEL_VALIDITY_ROUTE_MISSING",fid)
        if f["reference_frame_requirements"]["required"] and "CHOOSE_FRAME" not in route_roles: fail("FRAME_DEPENDENT_ITEM_WITHOUT_FRAME_BINDING",fid)
        if f["phase_topology"]["state_handoff_required"]:
            need={"IDENTIFY_PHASES","PROPAGATE_STATE","CHECK_CONTINUITY_OR_BOUNDARY"}
            if not need<=set(route_roles): fail("MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF",fid)
        ops=set(f["representation_requirements"]["graph_operation_kinds"])
        if any(o not in GRAPH_OPERATIONS for o in ops): fail("GRAPH_ROUTE_COLLAPSES_HEIGHT_SLOPE_AREA",fid)
    return out

def validate_verification_registry(reg,families,scope_authority):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("VERIFICATION_ROUTE_REGISTRY_DIGEST_MISMATCH")
    if reg["upstream_scope_authority_ref"]!=scope_authority["authority_id"] or reg["upstream_scope_authority_digest"]!=scope_authority["authority_digest"]: fail("VERIFICATION_ROUTE_SCOPE_AUTHORITY_MISMATCH")
    obligations=set(scope_authority["verification_obligation_identities"])
    out=idx(reg["routes"],"verification_route_id","DUPLICATE_VERIFICATION_ROUTE")
    for rid,r in out.items():
        if r["route_digest"]!=dwo(r,"route_digest"): fail("VERIFICATION_ROUTE_DIGEST_MISMATCH",rid)
        if r["family_ref"] not in families: fail("VERIFICATION_ROUTE_UNKNOWN_FAMILY",rid)
        if families[r["family_ref"]]["verification_route_ref"]!=rid: fail("VERIFICATION_ROUTE_FAMILY_MISMATCH",rid)
        if any(c["obligation_ref"] not in obligations for c in r["checks"]): fail("UNKNOWN_VERIFICATION_OBLIGATION",rid)
    for f in families.values():
        if f["verification_route_ref"] not in out: fail("VERIFICATION_ROUTE_MISSING",f["family_id"])
    return out

def validate_item_registry(reg,coverage,families):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("ITEM_SEMANTIC_PROFILE_REGISTRY_DIGEST_MISMATCH")
    mapped={r["item_ref"]:r for r in coverage["rows"] if r["mapping_state"]!="UNMAPPED"}
    out=idx(reg["profiles"],"item_ref","DUPLICATE_ITEM_SEMANTIC_PROFILE")
    if set(out)!=set(mapped): fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",f"missing={sorted(set(mapped)-set(out))},extra={sorted(set(out)-set(mapped))}")
    for item,p in out.items():
        if p["profile_digest"]!=dwo(p,"profile_digest"): fail("ITEM_SEMANTIC_PROFILE_DIGEST_MISMATCH",item)
        if "difficulty" in p or "overall_difficulty" in p: fail("DIFFICULTY_UNEXPLAINED_SCALAR",item)
        c=mapped[item]
        if set(p["family_refs"])!=set(c["problem_family_refs"]): fail("PROBLEM_INSTANCE_FAMILY_DRIFT",item)
        if p["primary_family_ref"] not in p["family_refs"] or p["primary_family_ref"] not in families: fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",item)
        dims=[d["dimension"] for d in p["demand_dimensions"]]
        if len(dims)!=len(set(dims)) or not dims or any(d not in DIMENSIONS for d in dims): fail("DEMAND_VECTOR_DIMENSION_INVALID",item)
        fam=families[p["primary_family_ref"]]; allowed=set(fam["representation_requirements"]["graph_operation_kinds"])
        ops=set(p["graph_operations"])
        if ops and (not allowed or not ops<=allowed): fail("GRAPH_ROUTE_COLLAPSES_HEIGHT_SLOPE_AREA",item)
        if allowed and not ops: fail("GRAPH_ROUTE_COLLAPSES_HEIGHT_SLOPE_AREA",item)
        if c["resolution_status"]=="BLOCKED" and p["blocked_behavior"]!="PRESERVE_UPSTREAM_BLOCK": fail("UPSTREAM_BLOCK_SILENTLY_PROMOTED",item)
    return out,mapped

def validate_policy(p):
    if p["policy_digest"]!=dwo(p,"policy_digest"): fail("GUIDE_DEMAND_POLICY_DIGEST_MISMATCH")
    if p["badge_class"]!="GUIDE_ASSIGNED_REASONING_DEMAND" or p["psychometric_claim"] is not False: fail("GUIDE_BADGE_PSYCHOMETRIC_CLAIM")
    if set(p["dimension_catalog"])!=DIMENSIONS or set(p["weights"])!=DIMENSIONS: fail("GUIDE_DEMAND_POLICY_DIMENSION_COVERAGE")

def alias_coverage(scope_roles,aliases,route_roles,item):
    result={}
    rr=set(route_roles)
    for sr in scope_roles:
        if sr not in aliases: fail("SCOPE_REASONING_ROLE_ALIAS_COVERAGE",f"{item}:{sr}")
        spec=aliases[sr]; need=set(spec["canonical_roles"])
        ok=(need<=rr) if spec["coverage_mode"]=="ALL" else bool(need&rr)
        if not ok: fail("SCOPE_REASONING_ROLE_ALIAS_NOT_REALIZED",f"{item}:{sr}")
        result[sr]=sorted(need&rr)
    return result

def instantiate_route(item,cov,profile,family,aliases):
    steps=[]
    for n,t in enumerate(family["reasoning_route_template"],1):
        relation_basis=t["relation_selection_basis"]
        if t["role"]=="CHOOSE_RELATION" and not relation_basis:
            relation_basis=family["relation_selection_rule"]
        validity_refs=list(cov["model_validity_conditions"]) if t["role"]=="CHECK_MODEL_VALIDITY" else []
        reps=[r for r in t["representation_refs"] if r in set(cov["representation_demands"])]
        if t["role"]=="REPRESENT" and not reps:
            reps=list(cov["representation_demands"])
        model_refs=sorted(set(t["model_refs"]) & set(cov["physical_model_refs"]))
        if t["role"] in {"SELECT_MODEL","CHECK_MODEL_VALIDITY"} and not model_refs:
            model_refs=list(cov["physical_model_refs"])
        law_refs=sorted(set(t["law_refs"]) & set(cov["law_refs"]))
        if t["role"]=="CHOOSE_RELATION" and not law_refs:
            law_refs=list(cov["law_refs"])
        s={"step_id":f"{item.replace('.','-')}-R{n:02d}","role":t["role"],"semantic_job":t["semantic_job"],
           "capability_refs":sorted(set(t["capability_refs"])|set(cov["canonical_capability_refs"]) if t["role"] in {"SELECT_MODEL","CHOOSE_RELATION"} else set(t["capability_refs"])),
           "system_refs":list(cov["system_refs"]),"state_variable_refs":list(cov["state_variable_refs"]),"representation_refs":reps,
           "model_refs":model_refs,"law_refs":law_refs,"model_validity_condition_refs":validity_refs,
           "state_transition":t["state_transition"],"relation_selection_basis":relation_basis,"verification_checkpoint_refs":list(t["verification_checkpoint_refs"])}
        steps.append(s)
    scan_forbidden(steps,item)
    roles=[s["role"] for s in steps]
    coverage=alias_coverage(cov["reasoning_role_expectations"],aliases,roles,item)
    route={"route_id":f"PHY-PD-RR-{item.replace('.','-')}","schema_version":"1.0.0","subject":"PHYSICS","item_ref":item,
           "family_refs":profile["family_refs"],"primary_family_ref":profile["primary_family_ref"],"mapping_state":cov["mapping_state"],"resolution_status":cov["resolution_status"],
           "learner_support_independent":True,"scope_role_expectations":cov["reasoning_role_expectations"],"scope_role_alias_coverage":coverage,"steps":steps,"route_digest":""}
    route["route_digest"]=dwo(route,"route_digest"); return route

def build_validity_binding(item,cov,family,route):
    required=bool(family["model_validity_conditions"])
    check_steps=[s["step_id"] for s in route["steps"] if s["role"]=="CHECK_MODEL_VALIDITY"]
    if required and not check_steps: fail("MODEL_VALIDITY_ROUTE_MISSING",item)
    if required and not cov["model_validity_conditions"] and cov["resolution_status"]!="BLOCKED": fail("MODEL_VALIDITY_ROUTE_MISSING",f"{item}: no upstream validity conditions")
    status="NOT_REQUIRED"
    if required: status="BLOCKED_UPSTREAM" if cov["resolution_status"]=="BLOCKED" else "SATISFIED"
    b={"binding_id":f"PHY-PD-MV-{item.replace('.','-')}","item_ref":item,"required":required,
       "physical_model_refs":cov["physical_model_refs"],"conditions":cov["model_validity_conditions"] if required else [],"route_step_refs":check_steps,"status":status,"binding_digest":""}
    b["binding_digest"]=dwo(b,"binding_digest"); return b

def validate_frame_and_phase(item,cov,family,route):
    if family["reference_frame_requirements"]["required"]:
        fr=cov["reference_frame"]
        unresolved=cov["resolution_status"]=="BLOCKED" and "REFERENCE_FRAME" in cov["unresolved_requirements"]
        if not fr.get("required") or (not fr.get("frame_text") and not unresolved): fail("FRAME_DEPENDENT_ITEM_WITHOUT_FRAME_BINDING",item)
        if "CHOOSE_FRAME" not in {s["role"] for s in route["steps"]}: fail("FRAME_DEPENDENT_ITEM_WITHOUT_FRAME_BINDING",item)
    if family["phase_topology"]["state_handoff_required"]:
        roles={s["role"] for s in route["steps"]}
        need={"IDENTIFY_PHASES","PROPAGATE_STATE","CHECK_CONTINUITY_OR_BOUNDARY"}
        if not need<=roles: fail("MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF",item)
        ph=cov["phase_structure"]
        if ph.get("kind")!="MULTI_PHASE" and cov["resolution_status"]!="BLOCKED": fail("MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF",f"{item}: upstream phase topology")
        if not ph.get("continuity_state_refs") and cov["resolution_status"]!="BLOCKED": fail("MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF",f"{item}: continuity state")

def build_vector(item,profile,policy,route):
    dims=[{**d,"evidence_refs":[route["route_id"],profile["primary_family_ref"]]} for d in profile["demand_dimensions"]]
    v={"vector_id":f"PHY-PD-DV-{item.replace('.','-')}","schema_version":"1.0.0","subject":"PHYSICS","item_ref":item,"family_refs":profile["family_refs"],
       "dimensions":dims,"guide_badge_policy_ref":policy["policy_id"],"psychometric_claim":False,"vector_digest":""}
    v["vector_digest"]=dwo(v,"vector_digest"); return v

def hard_eligible(route,verification_routes,policy):
    rules=policy["rules"]; roles={s["role"] for s in route["steps"]}; checks=sum(len(r["checks"]) for r in verification_routes)
    return len(route["steps"])>=rules["hard_min_route_steps"] and len(roles)>=rules["hard_min_distinct_roles"] and checks>=rules["hard_min_verification_checks"] and bool(roles&set(rules["hard_requires_any_role"]))

def validate_badge_assignment(label,vector,route,verification_routes,policy,item):
    eligible=hard_eligible(route,verification_routes,policy)
    if label=="HARD" and not eligible: fail("HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE",item)
    return eligible

def derive_badge(item,cov,vector,route,verification_routes,policy):
    if cov["resolution_status"]=="BLOCKED":
        return {"badge_class":"GUIDE_ASSIGNED_REASONING_DEMAND","status":"WITHHELD_UPSTREAM_BLOCK","label":None,"policy_ref":policy["policy_id"],"vector_ref":vector["vector_id"],"basis":"upstream scope/source resolution is BLOCKED; demand vector retained but learner-facing badge withheld","psychometric_claim":False}
    score=sum(d["level"]*policy["weights"][d["dimension"]] for d in vector["dimensions"])
    rules=policy["rules"]
    # Candidate label by score, then hard gate prevents scalar-score inflation.
    candidate="HARD" if score>rules["medium_max_score"] else ("MEDIUM" if score>rules["easy_max_score"] else "EASY")
    label="HARD" if candidate=="HARD" and hard_eligible(route,verification_routes,policy) else ("MEDIUM" if candidate=="HARD" else candidate)
    validate_badge_assignment(label,vector,route,verification_routes,policy,item)
    return {"badge_class":"GUIDE_ASSIGNED_REASONING_DEMAND","status":"DERIVED","label":label,"policy_ref":policy["policy_id"],"vector_ref":vector["vector_id"],"basis":f"weighted_vector_score={score};route_steps={len(route['steps'])};distinct_roles={len(set(s['role'] for s in route['steps']))};verification_checks={sum(len(r['checks']) for r in verification_routes)}","psychometric_claim":False}

def build_package(q,s,review_reg,review_policy,canonical_caps,scope_authority,scope_bindings,role_reg,family_reg,verification_reg,item_reg,badge_policy):
    scope_model,coverage,report,prereq=reconcile(q,s,review_reg,review_policy,canonical_caps,scope_authority,scope_bindings)
    if scope_model["attempt_data_consumed"] or report["attempt_data_consumed"]: fail("P_D_CONSUMES_LEARNER_DATA")
    if item_reg["upstream_question_set_ref"]!=q["question_set_id"] or item_reg["upstream_scope_binding_registry_ref"]!=scope_bindings["binding_registry_id"]: fail("ITEM_SEMANTIC_PROFILE_UPSTREAM_MISMATCH")
    roles,aliases=validate_role_registry(role_reg,scope_authority)
    families=validate_family_registry(family_reg,scope_authority,roles)
    verification=validate_verification_registry(verification_reg,families,scope_authority)
    profiles,mapped=validate_item_registry(item_reg,coverage,families)
    validate_policy(badge_policy)
    items=[]
    for item in sorted(mapped):
        cov=mapped[item]; p=profiles[item]; f=families[p["primary_family_ref"]]
        route=instantiate_route(item,cov,p,f,aliases)
        validate_frame_and_phase(item,cov,f,route)
        mv=build_validity_binding(item,cov,f,route)
        vr=[verification[families[x]["verification_route_ref"]] for x in p["family_refs"]]
        covered={c["obligation_ref"] for r in vr for c in r["checks"]}
        if not set(cov["verification_obligations"])<=covered: fail("VERIFICATION_ROUTE_MISSING",f"{item}:{sorted(set(cov['verification_obligations'])-covered)}")
        vector=build_vector(item,p,badge_policy,route)
        badge=derive_badge(item,cov,vector,route,vr,badge_policy)
        entry={"item_ref":item,"question_ref":cov["question_ref"],"part_ref":cov["part_ref"],"mapping_state":cov["mapping_state"],"resolution_status":cov["resolution_status"],
               "source_integrity_state":cov["source_integrity_state"],"validity_state":cov["validity_state"],"diagnostic_use":cov["diagnostic_use"],
               "family_refs":p["family_refs"],"primary_family_ref":p["primary_family_ref"],"graph_operations":p["graph_operations"],
               "reference_frame":cov["reference_frame"],"phase_structure":cov["phase_structure"],"reasoning_route":route,"model_validity_binding":mv,
               "verification_route_refs":[r["verification_route_id"] for r in vr],"demand_vector":vector,"guide_demand_badge":badge}
        items.append(entry)
    summary={"item_count":len(items),"blocked_count":sum(1 for x in items if x["resolution_status"]=="BLOCKED"),
             "family_count":len(families),"badge_counts":dict(sorted(Counter((x["guide_demand_badge"]["label"] or "WITHHELD") for x in items).items()))}
    pkg={"package_id":"PHY-G9-MOTION-PD-PROBLEM-SEMANTICS-v1","schema_version":"1.0.0","subject":"PHYSICS","question_set_ref":q["question_set_id"],
         "scope_model_ref":scope_model["scope_model_id"],"scope_coverage_ref":coverage["coverage_matrix_id"],"scope_reconciliation_ref":report["reconciliation_id"],
         "role_registry_ref":role_reg["registry_id"],"family_registry_ref":family_reg["registry_id"],"verification_registry_ref":verification_reg["registry_id"],"badge_policy_ref":badge_policy["policy_id"],
         "learner_support_independent":True,"attempt_data_consumed":False,"items":items,"summary":summary,"package_digest":""}
    pkg["package_digest"]=dwo(pkg,"package_digest"); return pkg

def main():
    ap=argparse.ArgumentParser()
    for x in ["questions","topic-scope","review-registry","review-policy","canonical-capabilities","scope-authority","scope-bindings","role-registry","family-registry","verification-registry","item-registry","badge-policy","out"]: ap.add_argument("--"+x,required=True)
    a=ap.parse_args(); pkg=build_package(load(a.questions),load(a.topic_scope),load(a.review_registry),load(a.review_policy),load(a.canonical_capabilities),load(a.scope_authority),load(a.scope_bindings),load(a.role_registry),load(a.family_registry),load(a.verification_registry),load(a.item_registry),load(a.badge_policy)); write(a.out,pkg)
if __name__=="__main__": main()
