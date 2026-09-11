#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path

D=Path(__file__).resolve().parents[1]
MATH=D.parent
sys.path.insert(0,str(MATH/"AssessmentScope"/"engine"))
from reconcile_math_assessment_scope import reconcile

BAD_ROUTE_KEYS={"hint","hint_text","hint_refs","solution","solution_text","worked_answer","final_answer","support_level","learner_state","diagnosis","misconception","treatment"}
DIMENSIONS={"reasoning_chain_length","algebraic_load","representation_shift","hidden_structure","state_tracking_load","method_selection_ambiguity","constraint_density","concept_combination","verification_demand","time_pressure"}

def cb(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def dg(x): return hashlib.sha256(cb(x)).hexdigest()
def dwo(x,k):
    y=copy.deepcopy(x); y.pop(k,None); return dg(y)
def fail(code,detail=""): raise ValueError(f"{code}: {detail}" if detail else code)
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def load_family_registry(p):
    p=Path(p); idx=load(p)
    if "family_shards" not in idx:
        return idx
    if idx["index_digest"]!=dwo(idx,"index_digest"):
        fail("PROBLEM_FAMILY_REGISTRY_INDEX_DIGEST_MISMATCH")
    families=[]
    for spec in idx["family_shards"]:
        sh=load(p.parent/spec["path"])
        if sh["shard_id"]!=spec["shard_id"] or sh["shard_digest"]!=spec["shard_digest"]:
            fail("PROBLEM_FAMILY_REGISTRY_SHARD_BINDING_MISMATCH",spec["path"])
        if sh["shard_digest"]!=dwo(sh,"shard_digest"):
            fail("PROBLEM_FAMILY_REGISTRY_SHARD_DIGEST_MISMATCH",spec["path"])
        if len(sh["families"])!=spec["family_count"]:
            fail("PROBLEM_FAMILY_REGISTRY_SHARD_COUNT_MISMATCH",spec["path"])
        families.extend(sh["families"])
    if len(families)!=idx["family_count"]:
        fail("PROBLEM_FAMILY_REGISTRY_COUNT_MISMATCH")
    full={k:v for k,v in idx.items() if k not in {"family_shards","assembled_registry_digest","family_count","index_digest"}}
    full["families"]=families; full["registry_digest"]=idx["assembled_registry_digest"]
    if full["registry_digest"]!=dwo(full,"registry_digest"):
        fail("PROBLEM_FAMILY_REGISTRY_ASSEMBLED_DIGEST_MISMATCH")
    return full
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

def idx(rows,key,code):
    out={}
    for r in rows:
        if r[key] in out: fail(code,r[key])
        out[r[key]]=r
    return out

def no_forbidden_route_payload(x,path="root"):
    if isinstance(x,dict):
        for k,v in x.items():
            if k.lower() in BAD_ROUTE_KEYS: fail("REASONING_ROUTE_EQUALS_HINT_COPY" if "hint" in k.lower() or "support" in k.lower() else "REASONING_ROUTE_EQUALS_SOLUTION_SUMMARY",f"{path}.{k}")
            no_forbidden_route_payload(v,f"{path}.{k}")
    elif isinstance(x,list):
        for i,v in enumerate(x): no_forbidden_route_payload(v,f"{path}[{i}]")

def validate_role_registry(reg):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("REASONING_ROLE_REGISTRY_DIGEST_MISMATCH")
    rows=idx(reg["roles"],"role_id","DUPLICATE_REASONING_ROLE")
    required={"INTERPRET","REPRESENT","SELECT_METHOD","MODEL","EXECUTE","TRANSFORM","COMPARE","INFER","CHECK_CONDITION","VERIFY","INTERPRET_RESULT"}
    if set(rows)!=required: fail("REASONING_ROLE_REGISTRY_COVERAGE")
    if any(r["learner_support_owner"] or r["solution_owner"] for r in rows.values()): fail("REASONING_ROUTE_AUTHORITY_DRIFT")
    return rows

def validate_family_registry(reg,scope_authority,roles):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("PROBLEM_FAMILY_REGISTRY_DIGEST_MISMATCH")
    if reg["upstream_scope_authority_ref"]!=scope_authority["authority_id"] or reg["upstream_scope_authority_digest"]!=scope_authority["authority_digest"]: fail("PROBLEM_FAMILY_SCOPE_AUTHORITY_MISMATCH")
    scope_families={x["problem_family_id"] for x in scope_authority["problem_families"]}; caps={x["capability_id"] for x in scope_authority["capabilities"]}; reps=set(scope_authority["representation_identities"]); obligations=set(scope_authority["verification_obligation_identities"])
    out=idx(reg["families"],"family_id","DUPLICATE_PROBLEM_FAMILY")
    if set(out)!=scope_families: fail("PROBLEM_FAMILY_IDENTITY_COVERAGE",f"missing={sorted(scope_families-set(out))}, extra={sorted(set(out)-scope_families)}")
    for f in out.values():
        if f.get("family_digest")!=dwo(f,"family_digest"): fail("PROBLEM_FAMILY_DIGEST_MISMATCH",f["family_id"])
        if f["semantic_owner_phase"]!="M-D": fail("PROBLEM_FAMILY_AUTHORITY_DRIFT",f["family_id"])
        if any(c not in caps for c in f["canonical_capability_refs"]): fail("UNKNOWN_PROBLEM_FAMILY_CAPABILITY",f["family_id"])
        if any(r not in roles for r in [s["role"] for s in f["reasoning_route_template"]]): fail("UNKNOWN_REASONING_ROLE",f["family_id"])
        declared_reps=set(f["representation_requirements"]["required_refs"]+f["representation_requirements"].get("optional_refs",[]))
        template_reps={r for s in f["reasoning_route_template"] for r in s["representation_refs"]}
        if not template_reps<=declared_reps: fail("PROBLEM_FAMILY_REPRESENTATION_DECLARATION_GAP",f["family_id"])
        if any(r not in reps for r in declared_reps): fail("UNKNOWN_PROBLEM_FAMILY_REPRESENTATION",f["family_id"])
        for s in f["reasoning_route_template"]:
            if any(c not in caps for c in s["capability_refs"]): fail("UNKNOWN_ROUTE_CAPABILITY",f["family_id"])
            if any(o not in obligations for o in s.get("verification_checkpoint_refs",[])): fail("UNKNOWN_ROUTE_VERIFICATION_OBLIGATION",f["family_id"])
        no_forbidden_route_payload(f["reasoning_route_template"],f["family_id"])
    return out

def validate_verification_registry(reg,families,scope_authority):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("VERIFICATION_ROUTE_REGISTRY_DIGEST_MISMATCH")
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

def validate_profiles(reg,coverage,families):
    if reg["registry_digest"]!=dwo(reg,"registry_digest"): fail("ITEM_SEMANTIC_PROFILE_REGISTRY_DIGEST_MISMATCH")
    out=idx(reg["profiles"],"item_ref","DUPLICATE_ITEM_SEMANTIC_PROFILE")
    mapped={r["item_ref"]:r for r in coverage["rows"] if r["mapping_state"]!="UNMAPPED"}
    if set(out)!=set(mapped): fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",f"missing={sorted(set(mapped)-set(out))}, extra={sorted(set(out)-set(mapped))}")
    for item,p in out.items():
        c=mapped[item]
        if set(p["family_refs"])!=set(c["problem_family_refs"]): fail("PROBLEM_INSTANCE_FAMILY_DRIFT",item)
        if p["primary_family_ref"] not in p["family_refs"] or p["primary_family_ref"] not in families: fail("PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY",item)
        dims=[d["dimension"] for d in p["demand_dimensions"]]
        if len(dims)!=len(set(dims)) or any(d not in DIMENSIONS for d in dims): fail("DEMAND_VECTOR_DIMENSION_INVALID",item)
        if len(dims)==1 and dims[0] in {"difficulty","overall_difficulty"}: fail("DIFFICULTY_UNEXPLAINED_SCALAR",item)
    return out,mapped

def validate_policy(p):
    if p["policy_digest"]!=dwo(p,"policy_digest"): fail("GUIDE_DEMAND_POLICY_DIGEST_MISMATCH")
    if p["badge_class"]!="GUIDE_ASSIGNED_REASONING_DEMAND" or p["psychometric_claim"] is not False: fail("GUIDE_BADGE_PSYCHOMETRIC_CLAIM")
    if set(p["dimension_catalog"])!=DIMENSIONS: fail("GUIDE_DEMAND_POLICY_DIMENSION_COVERAGE")

def _part_variant_index(cov):
    part=cov.get("part_ref")
    if not part or "." not in part: return 0
    suffix=part.rsplit(".",1)[-1].lower()
    if len(suffix)==1 and "a"<=suffix<="z": return ord(suffix)-ord("a")
    return 0

def _source_score(source,cov,role):
    caps=set(source.get("capability_refs",[])); reps=set(source.get("representation_refs",[]))
    wanted_caps=set(cov.get("canonical_capability_refs",[])); wanted_reps=set(cov.get("representation_demands",[]))
    return (4*len(caps&wanted_caps)+2*len(reps&wanted_reps)+(1 if source.get("role")==role else 0))

def _project_step(item,n,role,source,cov):
    source_role=source["role"]
    reps=list(source.get("representation_refs",[]))
    if source_role!=role and role=="REPRESENT":
        wanted=[r for r in cov.get("representation_demands",[]) if r in reps]
        if not wanted: wanted=list(cov.get("representation_demands",[]))[:1]
        label=" / ".join(wanted) if wanted else "required mathematical"
        semantic_job=f"make the required {label} representation explicit while preserving variable meaning"
        transition=f"given item state -> {label} representation"
        reps=wanted or reps
    else:
        semantic_job=source["semantic_job"]
        transition=source["mathematical_transition"]
    return {"step_id":f"{item}-R{n:02d}","role":role,"semantic_job":semantic_job,"mathematical_transition":transition,"capability_refs":source["capability_refs"],"representation_refs":reps,"verification_checkpoint_refs":source.get("verification_checkpoint_refs",[])}

def instantiate_route(item,cov,profile,family):
    template=family["reasoning_route_template"]
    wanted_caps=set(cov.get("canonical_capability_refs",[]))
    wanted_reps=set(cov.get("representation_demands",[]))
    variant=_part_variant_index(cov)
    used=Counter(); steps=[]
    for n,role in enumerate(cov["reasoning_role_expectations"],1):
        exact=[s for s in template if s["role"]==role]
        if wanted_caps:
            exact_cap=[s for s in exact if set(s.get("capability_refs",[]))&wanted_caps]
            family_cap=[s for s in template if set(s.get("capability_refs",[]))&wanted_caps]
            if exact_cap:
                exact=exact_cap
            elif family_cap:
                exact=[]
        if exact:
            i=used[role]; used[role]+=1
            source=exact[min(i+variant,len(exact)-1)]
        else:
            candidates=[s for s in template if (not wanted_caps or set(s.get("capability_refs",[]))&wanted_caps)]
            if wanted_reps:
                rep_candidates=[s for s in candidates if set(s.get("representation_refs",[]))&wanted_reps]
                if rep_candidates: candidates=rep_candidates
            if role!="VERIFY":
                non_verify=[s for s in candidates if s.get("role")!="VERIFY"]
                if non_verify: candidates=non_verify
            if not candidates: fail("PROBLEM_FAMILY_ROUTE_ROLE_GAP",f"{item}:{role}")
            source=max(enumerate(candidates),key=lambda pair:(_source_score(pair[1],cov,role),-pair[0]))[1]
        steps.append(_project_step(item,n,role,source,cov))
    if [s["role"] for s in steps]!=cov["reasoning_role_expectations"]: fail("PROBLEM_FAMILY_ROUTE_ROLE_DRIFT",item)
    route={"route_id":f"MATH-RR-{item.replace('.','-')}","schema_version":"1.0.0","subject":"MATHEMATICS","item_ref":item,"family_refs":profile["family_refs"],"primary_family_ref":profile["primary_family_ref"],"mapping_state":cov["mapping_state"],"learner_support_independent":True,"variant_context":profile["variant_context"],"steps":steps,"route_digest":""}
    no_forbidden_route_payload(route["steps"],route["route_id"]); route["route_digest"]=dwo(route,"route_digest"); return route

def build_vector(item,profile,policy,route):
    dims=[]
    for d in profile["demand_dimensions"]:
        dims.append({**d,"evidence_refs":[route["route_id"],profile["primary_family_ref"]]})
    v={"vector_id":f"MATH-DV-{item.replace('.','-')}","schema_version":"1.0.0","subject":"MATHEMATICS","item_ref":item,"family_refs":profile["family_refs"],"dimensions":dims,"guide_badge_policy_ref":policy["policy_id"],"psychometric_claim":False,"vector_digest":""}; v["vector_digest"]=dwo(v,"vector_digest"); return v

def derive_badge(v,route,verification_routes,policy):
    score=sum(x["level"]*policy["weights"][x["dimension"]] for x in v["dimensions"])
    roles={s["role"] for s in route["steps"]}; rules=policy["rules"]
    hard_eligible=len(route["steps"])>=rules["hard_min_route_steps"] and len(roles)>=rules["hard_min_distinct_roles"] and bool(roles&set(rules["hard_requires_role_any_of"])) and bool(verification_routes)
    if score>rules["medium_max_score"] and hard_eligible: label="HARD"
    elif score>rules["easy_max_score"]: label="MEDIUM"
    else: label="EASY"
    if label=="HARD" and not hard_eligible: fail("HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE",v["item_ref"])
    return {"badge_class":"GUIDE_ASSIGNED_REASONING_DEMAND","label":label,"policy_ref":policy["policy_id"],"vector_ref":v["vector_id"],"basis":f"vector_score={score}; route_steps={len(route['steps'])}; distinct_roles={len(roles)}; policy={policy['policy_id']}","psychometric_claim":False}

def build_package(q,s,review_reg,review_policy,scope_authority,scope_bindings,role_reg,family_reg,verification_reg,item_reg,badge_policy):
    scope_model,coverage,report,prereq=reconcile(q,s,review_reg,review_policy,scope_authority,scope_bindings)
    if item_reg["upstream_question_set_ref"]!=q["question_set_id"] or item_reg["upstream_scope_binding_registry_ref"]!=scope_bindings["binding_registry_id"]: fail("ITEM_SEMANTIC_PROFILE_UPSTREAM_MISMATCH")
    roles=validate_role_registry(role_reg); families=validate_family_registry(family_reg,scope_authority,roles); verification=validate_verification_registry(verification_reg,families,scope_authority); validate_policy(badge_policy); profiles,mapped=validate_profiles(item_reg,coverage,families)
    rows=[]
    for item in sorted(mapped,key=lambda x:(mapped[x]["question_ref"],mapped[x]["part_ref"] or "")):
        c=mapped[item]; p=profiles[item]; f=families[p["primary_family_ref"]]
        route=instantiate_route(item,c,p,f)
        if not set(c["canonical_capability_refs"])<=set(f["canonical_capability_refs"]): fail("PROBLEM_FAMILY_CAPABILITY_COVERAGE",item)
        declared_reps=set(f["representation_requirements"]["required_refs"]+f["representation_requirements"].get("optional_refs",[]))
        if not set(c["representation_demands"])<=declared_reps: fail("PROBLEM_FAMILY_REPRESENTATION_COVERAGE",item)
        vref=f["verification_route_ref"]; vr=verification[vref]
        if not set(c["verification_obligations"])<=set(x["obligation_ref"] for x in vr["checks"]): fail("VERIFICATION_ROUTE_MISSING",item)
        vector=build_vector(item,p,badge_policy,route); badge=derive_badge(vector,route,[vref],badge_policy)
        rows.append({"item_ref":item,"question_ref":c["question_ref"],"part_ref":c["part_ref"],"validity_state":c["validity_state"],"diagnostic_use":c["diagnostic_use"],"mapping_state":c["mapping_state"],"family_refs":p["family_refs"],"primary_family_ref":p["primary_family_ref"],"reasoning_route":route,"verification_route_refs":[vref],"demand_vector":vector,"guide_demand_badge":badge})
    pkg={"package_id":"MATH-G9-MIXED-PT2-PROBLEM-SEMANTICS-v1","schema_version":"1.0.0","subject":"MATHEMATICS","scope_model_ref":scope_model["scope_model_id"],"scope_model_digest":scope_model["scope_model_digest"],"coverage_matrix_ref":coverage["coverage_matrix_id"],"coverage_matrix_digest":coverage["matrix_digest"],"family_registry_ref":family_reg["registry_id"],"family_registry_digest":family_reg["registry_digest"],"role_registry_ref":role_reg["registry_id"],"role_registry_digest":role_reg["registry_digest"],"verification_registry_ref":verification_reg["registry_id"],"verification_registry_digest":verification_reg["registry_digest"],"item_profile_registry_ref":item_reg["registry_id"],"item_profile_registry_digest":item_reg["registry_digest"],"guide_badge_policy_ref":badge_policy["policy_id"],"guide_badge_policy_digest":badge_policy["policy_digest"],"assessment_item_semantics":rows,"summary":{"mapped_item_count":len(rows),"badge_counts":dict(sorted(Counter(x["guide_demand_badge"]["label"] for x in rows).items())),"family_count":len(families),"reasoning_route_count":len(rows),"verification_route_count":len(verification),"psychometric_claim":False},"package_digest":""}; pkg["package_digest"]=dwo(pkg,"package_digest"); return pkg

def main():
    p=argparse.ArgumentParser()
    for x in ["questions","topic-scope","review-registry","review-policy","scope-authority","scope-bindings","role-registry","family-registry","verification-registry","item-registry","badge-policy","out"]: p.add_argument("--"+x,required=True)
    a=p.parse_args(); vals=[]
    for x in ["questions","topic-scope","review-registry","review-policy","scope-authority","scope-bindings","role-registry","family-registry","verification-registry","item-registry","badge-policy"]:
        loader=load_family_registry if x=="family-registry" else load
        vals.append(loader(getattr(a,x.replace('-', '_'))))
    write(a.out,build_package(*vals))
if __name__=="__main__": main()
