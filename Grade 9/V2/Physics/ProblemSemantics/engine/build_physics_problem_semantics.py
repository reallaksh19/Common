#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,hashlib,json,sys
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve(); D=HERE.parents[1]; PHYSICS=HERE.parents[2]
sys.path.insert(0,str(PHYSICS/'AssessmentScope'/'engine'))
from reconcile_physics_assessment_scope import reconcile  # noqa: E402

def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def dwo(x,field):
    y=copy.deepcopy(x); y.pop(field,None); return hashlib.sha256(canonical(y).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)

def validate_role_registry(role_reg,scope_authority):
    if role_reg['authority_ref']!=scope_authority['authority_id']: fail('ROLE_REGISTRY_AUTHORITY_MISMATCH')
    roles={r['role'] for r in role_reg['roles']}; aliases=role_reg.get('aliases',{})
    if len(roles)!=len(role_reg['roles']): fail('DUPLICATE_REASONING_ROLE')
    if any(v not in roles for v in aliases.values()): fail('ROLE_ALIAS_TARGET_UNKNOWN')
    return roles,aliases

def validate_family_registry(reg,scope_authority,roles):
    if reg['authority_ref']!=scope_authority['authority_id']: fail('FAMILY_REGISTRY_AUTHORITY_MISMATCH')
    caps={c['capability_id'] for c in scope_authority['capabilities']}; fam={}
    for f in reg['families']:
        if f['family_id'] in fam: fail('DUPLICATE_PROBLEM_FAMILY',f['family_id'])
        if any(c not in caps for c in f['required_capability_refs']): fail('FAMILY_REFERENCES_UNKNOWN_CAPABILITY',f['family_id'])
        for step in f['reasoning_template']:
            if step['role'] not in roles: fail('FAMILY_UNKNOWN_REASONING_ROLE',f["family_id"])
        fam[f['family_id']]=f
    return fam

def validate_verification_registry(reg,families,scope_authority):
    if reg['authority_ref']!=scope_authority['authority_id']: fail('VERIFICATION_REGISTRY_AUTHORITY_MISMATCH')
    out={}
    for row in reg['routes']:
        rid=row['verification_route_id']
        if rid in out: fail('DUPLICATE_VERIFICATION_ROUTE',rid)
        if row['family_ref'] not in families: fail('VERIFICATION_UNKNOWN_FAMILY',rid)
        out[rid]=row
    return out

def validate_item_registry(reg,coverage,families):
    mapped={r['item_ref']:r for r in coverage['rows']}; profiles={}
    for p in reg['items']:
        if p['item_ref'] in profiles: fail('DUPLICATE_ITEM_SEMANTICS',p['item_ref'])
        if p['item_ref'] not in mapped: fail('ITEM_SEMANTICS_OUTSIDE_SCOPE_COVERAGE',p['item_ref'])
        if p['primary_family_ref'] not in families or any(x not in families for x in p['family_refs']): fail('ITEM_SEMANTICS_UNKNOWN_FAMILY',p['item_ref'])
        profiles[p['item_ref']]=p
    if set(profiles)!=set(mapped): fail('ITEM_SEMANTICS_COVERAGE_MISMATCH')
    return profiles,mapped

def validate_policy(policy):
    dims={d['dimension'] for d in policy['dimensions']}
    if set(policy['weights'])!=dims: fail('BADGE_POLICY_DIMENSION_DRIFT')

def instantiate_route(item,cov,profile,family,aliases):
    steps=[]
    for i,tmpl in enumerate(family['reasoning_template'],1):
        role=aliases.get(tmpl['role'],tmpl['role'])
        evidence=[]
        if role in {'FRAME_SETUP','STATE_SETUP'}:
            evidence=[cov['reference_frame'],cov['sign_convention']]+cov['state_variable_refs']
        elif role in {'MODEL_SELECTION','LAW_SELECTION'}:
            evidence=cov['physical_model_refs']+cov['law_refs']+cov['model_validity_conditions']
        elif role in {'REPRESENTATION_INTERPRETATION','REPRESENTATION_TRANSLATION'}:
            evidence=cov['representation_demands']+cov['source_representation_refs']
        elif role in {'INVARIANT_IDENTIFICATION','CONSTRAINT_EXTRACTION'}:
            evidence=cov['canonical_concept_refs']+cov['canonical_capability_refs']
        elif role in {'SYMBOLIC_DERIVATION','CONSTRUCTIVE_PROCEDURE'}:
            evidence=cov['canonical_capability_refs']+cov['problem_family_refs']
        elif role in {'VERIFICATION','SANITY_CHECK'}:
            evidence=cov['verification_obligations']
        else: evidence=cov['canonical_capability_refs']
        steps.append({'step_index':i,'role':role,'action':tmpl['action'],'why':tmpl['why'],'evidence_refs':sorted(set(evidence))})
    route={'route_id':f"PHY-PD-RR-{item.replace('.','-')}",'schema_version':'1.0.0','subject':'PHYSICS','item_ref':item,'primary_family_ref':family['family_id'],'steps':steps,'route_digest':''}
    route['route_digest']=dwo(route,'route_digest'); return route

def build_validity_binding(item,cov,family,route):
    required=bool(cov['model_validity_conditions']) or bool(family.get('required_model_conditions'))
    visible=sorted(set(cov['model_validity_conditions'])|set(family.get('required_model_conditions',[])))
    if required and not visible and cov['resolution_status']!='BLOCKED': fail('MODEL_VALIDITY_NOT_EXPOSED',item)
    return {'binding_id':f"PHY-PD-MV-{item.replace('.','-')}",'item_ref':item,'required':required,'conditions':visible,'route_ref':route['route_id']}

def validate_frame_and_phase(item,cov,family,route):
    if family.get('requires_reference_frame') and not cov['reference_frame'] and cov['resolution_status']!='BLOCKED': fail('FRAME_SIGN_REQUIREMENT_DROPPED',item)
    if family.get('requires_multiphase'):
        ph=cov['phase_structure']
        if ph.get('kind')!='MULTI_PHASE' and cov['resolution_status']!='BLOCKED': fail('MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF',f'{item}: upstream phase topology')
        if not ph.get('continuity_state_refs') and cov['resolution_status']!='BLOCKED': fail('MULTIPHASE_ROUTE_WITHOUT_STATE_HANDOFF',f'{item}: continuity state')

def build_vector(item,profile,policy,route):
    dims=[{**d,'evidence_refs':[route['route_id'],profile['primary_family_ref']]} for d in profile['demand_dimensions']]
    v={'vector_id':f"PHY-PD-DV-{item.replace('.','-')}",'schema_version':'1.0.0','subject':'PHYSICS','item_ref':item,'family_refs':profile['family_refs'],
       'dimensions':dims,'guide_badge_policy_ref':policy['policy_id'],'psychometric_claim':False,'vector_digest':''}
    v['vector_digest']=dwo(v,'vector_digest'); return v

def hard_eligible(route,verification_routes,policy):
    rules=policy['rules']; roles={s['role'] for s in route['steps']}; checks=sum(len(r['checks']) for r in verification_routes)
    return len(route['steps'])>=rules['hard_min_route_steps'] and len(roles)>=rules['hard_min_distinct_roles'] and checks>=rules['hard_min_verification_checks'] and bool(roles&set(rules['hard_requires_any_role']))

def validate_badge_assignment(label,vector,route,verification_routes,policy,item):
    eligible=hard_eligible(route,verification_routes,policy)
    if label=='HARD' and not eligible: fail('HARD_BADGE_WITHOUT_DEEPER_REASONING_ROUTE',item)
    return eligible

def derive_badge(item,cov,vector,route,verification_routes,policy):
    if cov['resolution_status']=='BLOCKED':
        return {'badge_class':'GUIDE_ASSIGNED_REASONING_DEMAND','status':'WITHHELD_UPSTREAM_BLOCK','label':None,'policy_ref':policy['policy_id'],'vector_ref':vector['vector_id'],'basis':'upstream scope/source resolution is BLOCKED; demand vector retained but learner-facing badge withheld','psychometric_claim':False}
    score=sum(d['level']*policy['weights'][d['dimension']] for d in vector['dimensions'])
    rules=policy['rules']
    candidate='HARD' if score>rules['medium_max_score'] else ('MEDIUM' if score>rules['easy_max_score'] else 'EASY')
    label='HARD' if candidate=='HARD' and hard_eligible(route,verification_routes,policy) else ('MEDIUM' if candidate=='HARD' else candidate)
    validate_badge_assignment(label,vector,route,verification_routes,policy,item)
    return {'badge_class':'GUIDE_ASSIGNED_REASONING_DEMAND','status':'DERIVED','label':label,'policy_ref':policy['policy_id'],'vector_ref':vector['vector_id'],'basis':f"weighted_vector_score={score};route_steps={len(route['steps'])};distinct_roles={len(set(s['role'] for s in route['steps']))};verification_checks={sum(len(r['checks']) for r in verification_routes)}",'psychometric_claim':False}

def _consume_scope_bundle(precomputed_scope,scope_authority,scope_bindings):
    if not isinstance(precomputed_scope,(tuple,list)) or len(precomputed_scope)!=4: fail('P_D_PRECOMPUTED_SCOPE_SHAPE')
    scope_model,coverage,report,prereq=copy.deepcopy(precomputed_scope)
    if scope_model.get('scope_model_digest')!=dwo(scope_model,'scope_model_digest'): fail('P_D_PRECOMPUTED_SCOPE_DIGEST')
    if coverage.get('matrix_digest')!=dwo(coverage,'matrix_digest'): fail('P_D_PRECOMPUTED_COVERAGE_DIGEST')
    if report.get('report_digest')!=dwo(report,'report_digest'): fail('P_D_PRECOMPUTED_RECONCILIATION_DIGEST')
    if prereq.get('closure_digest')!=dwo(prereq,'closure_digest'): fail('P_D_PRECOMPUTED_PREREQUISITE_DIGEST')
    if scope_model.get('authority_ref')!=scope_authority['authority_id'] or report.get('authority_ref')!=scope_authority['authority_id']: fail('P_D_PRECOMPUTED_SCOPE_AUTHORITY_MISMATCH')
    if scope_model.get('binding_registry_ref')!=scope_bindings['binding_registry_id'] or report.get('binding_registry_ref')!=scope_bindings['binding_registry_id']: fail('P_D_PRECOMPUTED_SCOPE_BINDING_MISMATCH')
    if coverage.get('scope_model_ref')!=scope_model['scope_model_id']: fail('P_D_PRECOMPUTED_COVERAGE_SCOPE_MISMATCH')
    if scope_model.get('attempt_data_consumed') or report.get('attempt_data_consumed'): fail('P_D_CONSUMES_LEARNER_DATA')
    return scope_model,coverage,report,prereq

def build_package(q,s,review_reg,review_policy,canonical_caps,scope_authority,scope_bindings,role_reg,family_reg,verification_reg,item_reg,badge_policy,precomputed_scope=None):
    if precomputed_scope is None:
        scope_model,coverage,report,prereq=reconcile(q,s,review_reg,review_policy,canonical_caps,scope_authority,scope_bindings)
    else:
        scope_model,coverage,report,prereq=_consume_scope_bundle(precomputed_scope,scope_authority,scope_bindings)
    if scope_model['attempt_data_consumed'] or report['attempt_data_consumed']: fail('P_D_CONSUMES_LEARNER_DATA')
    if item_reg['upstream_question_set_ref']!=q['question_set_id'] or item_reg['upstream_scope_binding_registry_ref']!=scope_bindings['binding_registry_id']: fail('ITEM_SEMANTIC_PROFILE_UPSTREAM_MISMATCH')
    roles,aliases=validate_role_registry(role_reg,scope_authority)
    families=validate_family_registry(family_reg,scope_authority,roles)
    verification=validate_verification_registry(verification_reg,families,scope_authority)
    profiles,mapped=validate_item_registry(item_reg,coverage,families)
    validate_policy(badge_policy)
    items=[]
    for item in sorted(mapped):
        cov=mapped[item]; p=profiles[item]; f=families[p['primary_family_ref']]
        route=instantiate_route(item,cov,p,f,aliases)
        validate_frame_and_phase(item,cov,f,route)
        mv=build_validity_binding(item,cov,f,route)
        vr=[verification[families[x]['verification_route_ref']] for x in p['family_refs']]
        covered={c['obligation_ref'] for r in vr for c in r['checks']}
        if not set(cov['verification_obligations'])<=covered: fail('VERIFICATION_ROUTE_MISSING',f"{item}:{sorted(set(cov['verification_obligations'])-covered)}")
        vector=build_vector(item,p,badge_policy,route)
        badge=derive_badge(item,cov,vector,route,vr,badge_policy)
        entry={'item_ref':item,'question_ref':cov['question_ref'],'part_ref':cov['part_ref'],'mapping_state':cov['mapping_state'],'resolution_status':cov['resolution_status'],
               'source_integrity_state':cov['source_integrity_state'],'validity_state':cov['validity_state'],'diagnostic_use':cov['diagnostic_use'],
               'family_refs':p['family_refs'],'primary_family_ref':p['primary_family_ref'],'graph_operations':p['graph_operations'],
               'reference_frame':cov['reference_frame'],'phase_structure':cov['phase_structure'],'reasoning_route':route,'model_validity_binding':mv,
               'verification_route_refs':[r['verification_route_id'] for r in vr],'demand_vector':vector,'guide_demand_badge':badge}
        items.append(entry)
    summary={'item_count':len(items),'blocked_count':sum(1 for x in items if x['resolution_status']=='BLOCKED'),
             'family_count':len(families),'badge_counts':dict(sorted(Counter((x['guide_demand_badge']['label'] or 'WITHHELD') for x in items).items()))}
    pkg={'package_id':'PHY-G9-MOTION-PD-PROBLEM-SEMANTICS-v1','schema_version':'1.0.0','subject':'PHYSICS','question_set_ref':q['question_set_id'],
         'scope_model_ref':scope_model['scope_model_id'],'scope_coverage_ref':coverage['coverage_matrix_id'],'scope_reconciliation_ref':report['reconciliation_id'],
         'role_registry_ref':role_reg['registry_id'],'family_registry_ref':family_reg['registry_id'],'verification_registry_ref':verification_reg['registry_id'],'badge_policy_ref':badge_policy['policy_id'],
         'learner_support_independent':True,'attempt_data_consumed':False,'items':items,'summary':summary,'package_digest':''}
    pkg['package_digest']=dwo(pkg,'package_digest'); return pkg

def main():
    ap=argparse.ArgumentParser()
    for x in ['questions','topic-scope','review-registry','review-policy','canonical-capabilities','scope-authority','scope-bindings','role-registry','family-registry','verification-registry','item-registry','badge-policy','out']: ap.add_argument('--'+x,required=True)
    a=ap.parse_args(); pkg=build_package(load(a.questions),load(a.topic_scope),load(a.review_registry),load(a.review_policy),load(a.canonical_capabilities),load(a.scope_authority),load(a.scope_bindings),load(a.role_registry),load(a.family_registry),load(a.verification_registry),load(a.item_registry),load(a.badge_policy)); write(a.out,pkg)
if __name__=='__main__': main()
