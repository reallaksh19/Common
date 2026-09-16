#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
HERE=Path(__file__).resolve(); MATH=HERE.parents[3]; COMMON=MATH/'ProductionKits'/'common'/'engine'; UP=MATH/'Core2Transfer'/'engine'
sys.path[:0]=[str(COMMON),str(UP)]
from production_primitives import canonical, validate_source_bundle, validate_bound_object, validate_answer_contract
from build_math_core2_transfer import build_plan, load
REQUIRED_ROLES={'QUESTION_SET','ASSESSMENT_REVIEW_REGISTRY','ASSESSMENT_REVIEW_POLICY','SCOPE_BINDINGS','CANONICAL_MATH_AUTHORITY','PROBLEM_SEMANTICS','VERIFICATION_REGISTRY','TEACHING_PRIMITIVE_REGISTRY','PAGE_INTENT_PROFILE','CORE2_AUTHORING_PROFILE'}
def bind(bundle,role,obj,refs=(),digs=()): validate_bound_object(bundle,role,obj,ref_fields=tuple(refs),digest_fields=tuple(digs))
def answer_contract(page,independent):
    q=page['question_ref']; audit=independent.get('answers',{}).get(q)
    if not audit: raise ValueError(f'CORE2_KIT_INDEPENDENT_ANSWER_MISSING:{q}')
    if audit.get('status')!='PASS': raise ValueError(f'CORE2_KIT_INDEPENDENT_ANSWER_NOT_PASS:{q}')
    authoritative=page['solution_route']['final_answer']
    if canonical(audit.get('canonical_answer'))!=canonical(authoritative): raise ValueError(f'CORE2_KIT_INDEPENDENT_ANSWER_MISMATCH:{q}')
    final=authoritative if isinstance(authoritative,dict) else {}; labels=final.get('accepted_option_labels') or []; uniqueness=str(final.get('uniqueness_status') or 'UNIQUE').upper()
    mult={'MULTIPLE':'MULTIPLE_DISTINCT','UNDERDETERMINED':'UNDERDETERMINED','UNIQUE':'SINGLE_CANONICAL'}.get(uniqueness,'SINGLE_CANONICAL')
    checks=[{'method':'UPSTREAM_VERIFICATION','status':'PASS','evidence':x if isinstance(x,str) else canonical(x)} for x in page['solution_route'].get('verification_checks') or []]
    checks.append({'method':'INDEPENDENT_SOLVER','status':'PASS','evidence':audit['evidence']})
    ans={'question_ref':q,'answer_type':'MULTIPLE_CHOICE' if labels else 'OPEN_RESPONSE','canonical_answer':authoritative,'accepted_equivalents':final.get('accepted_answers') or labels,'solution_paths':[{'path_id':'CORE2_AUTHORIZED','steps':[str(x) for x in page['solution_route']['steps']]}],'verification_checks':checks,'domain_conditions':[],'solution_multiplicity':mult,'independent_solver_status':'PASS'}
    validate_answer_contract(ans); return ans

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-bundle',required=True)
    for n in ['questions','review-registry','review-policy','scope-bindings','authority','problem-semantics','verification-registry','primitive-registry','page-intent-profile','authoring-profile','independent-answer-audit']: ap.add_argument('--'+n,required=True)
    ap.add_argument('--core1-plan'); ap.add_argument('--out-dir',required=True); a=ap.parse_args()
    bundle=load(a.source_bundle); validate_source_bundle(bundle,REQUIRED_ROLES)
    Q=load(a.questions); RR=load(a.review_registry); RP=load(a.review_policy); SB=load(a.scope_bindings); A=load(a.authority); PS=load(a.problem_semantics); V=load(a.verification_registry); PR=load(a.primitive_registry); PI=load(a.page_intent_profile); AP=load(a.authoring_profile); C1=load(a.core1_plan) if a.core1_plan else None; IA=load(a.independent_answer_audit)
    bind(bundle,'QUESTION_SET',Q,('question_set_id',),('question_set_digest',)); bind(bundle,'ASSESSMENT_REVIEW_REGISTRY',RR,('registry_id',),('registry_digest',)); bind(bundle,'ASSESSMENT_REVIEW_POLICY',RP,('policy_id',),('policy_digest',)); bind(bundle,'SCOPE_BINDINGS',SB,('registry_id','binding_set_id'),('registry_digest','binding_set_digest')); bind(bundle,'CANONICAL_MATH_AUTHORITY',A,('authority_id','registry_id'),('authority_digest','registry_digest')); bind(bundle,'PROBLEM_SEMANTICS',PS,('package_id',),('package_digest',)); bind(bundle,'VERIFICATION_REGISTRY',V,('registry_id',),('registry_digest',)); bind(bundle,'TEACHING_PRIMITIVE_REGISTRY',PR,('registry_id',),('registry_digest',)); bind(bundle,'PAGE_INTENT_PROFILE',PI,('profile_id','policy_id'),('profile_digest','policy_digest')); bind(bundle,'CORE2_AUTHORING_PROFILE',AP,('profile_id',),('profile_digest',))
    plan=build_plan(Q,RR,RP,SB,A,PS,V,PR,PI,AP,C1); answers=[answer_contract(p,IA) for p in plan['pages']]
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); (out/'core2_transfer_plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); (out/'core2_answer_contracts.json').write_text(json.dumps({'answers':answers},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    audit={'kit_id':'MATH-PRODUCTION-KIT-CORE2-v1','status':'PASS','source_question_count':len(plan['pages']),'answer_contract_count':len(answers),'source_fidelity':plan['summary']['source_fidelity'],'attempt_first':plan['summary']['attempt_first'],'release_class':plan['release_class']}; (out/'core2_kit_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8'); print(json.dumps(audit,indent=2))
if __name__=='__main__': main()
