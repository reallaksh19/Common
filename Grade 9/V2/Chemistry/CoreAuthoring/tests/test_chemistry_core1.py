#!/usr/bin/env python3
import copy, hashlib, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[str(D/'engine'),str(CHEM/'AssessmentReview'/'engine'),str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine'),str(CHEM/'LearnerEvidence'/'engine'),str(CHEM/'LearnerStudy'/'engine')]
from build_chemistry_core1 import build_plan,validate_plan,load_pck_registry,digest,canonical
from review_chemistry_assessment import build_review,load_registry as load_review_registry
from build_chemistry_scope import build_scope
from build_chemistry_reasoning_semantics import build_semantics
from infer_chemistry_learner_evidence import build_snapshot
from build_chemistry_learner_study_model import derive_study_scope,build_model

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError('expected '+code)
def redigest_plan(p): p['plan_digest']=''; p['plan_digest']=digest(p,'plan_digest'); return p
def lesson(p,c): return next(x for x in p['lessons'] if x['capability_ref']==c)
def redigest_pck(reg):
    for a in reg['assets']:
        a['asset_digest']=''; x=copy.deepcopy(a); x.pop('asset_digest'); a['asset_digest']=hashlib.sha256(canonical(x).encode()).hexdigest()
    reg['registry_digest']=''; x=copy.deepcopy(reg); x.pop('registry_digest'); reg['registry_digest']=hashlib.sha256(canonical(x).encode()).hexdigest(); return reg

A=CHEM/'AssessmentIntake'/'fixtures'; R=CHEM/'AssessmentReview'; S=CHEM/'AssessmentScope'; RS=CHEM/'ReasoningSemantics'; E=CHEM/'LearnerEvidence'; LS=CHEM/'LearnerStudy'
sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
review_reg,manifest_digest=load_review_registry(R/'registry'/'chemistry-item-validity-registry.json')
review=build_review(copy.deepcopy(sources),copy.deepcopy(questions),review_reg,load(R/'policies'/'chemistry-diagnostic-use-policy.json'),load(R/'registry'/'chemistry-qc-events.json'),registry_manifest_digest=manifest_digest)
source_ledger=load(S/'registry'/'chemistry-source-obligation-ledger.json'); qbindings=load(S/'registry'/'chemistry-question-capability-bindings.json'); external=load(S/'registry'/'chemistry-external-corpus-classification.json'); authority=load(S/'authority'/'chemistry-canonical-authority.json')
scope_bundle=build_scope(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(authority))
semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),load(RS/'registry'/'chemistry-problem-family-registry.json'),load(RS/'registry'/'chemistry-reasoning-role-registry.json'),load(RS/'registry'/'chemistry-guide-demand-badge-policy.json'))
obs=load(E/'registry'/'chemistry-observation-code-registry.json'); diag_policy=load(E/'registry'/'chemistry-diagnostic-policy.json'); attempts=load(E/'fixtures'/'chemistry-diagnostic-attempt-set.fixture.json'); evidence=load(E/'fixtures'/'chemistry-learner-evidence-ledger.fixture.json')
no_attempt=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(obs),copy.deepcopy(diag_policy))
with_attempt=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(obs),copy.deepcopy(diag_policy),copy.deepcopy(attempts),copy.deepcopy(evidence))
study_scope=derive_study_scope(copy.deepcopy(scope_bundle),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
treatment=load(LS/'registry'/'chemistry-treatment-policy.json')
model_a=build_model(copy.deepcopy(study_scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(no_attempt),copy.deepcopy(treatment),'CHEM-C-G-UPSTREAM-NO-ATTEMPT')
model_b=build_model(copy.deepcopy(study_scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(with_attempt),copy.deepcopy(treatment),'CHEM-C-G-UPSTREAM-WITH-ATTEMPT')
pck=load_pck_registry(); profile=load(D/'registry'/'chemistry-instructional-authoring-profile.json'); completeness=load(D/'registry'/'chemistry-core1-scope-completeness-policy.json'); problems=load(D/'registry'/'chemistry-problem-authoring-profile.json')
plan_a=build_plan(copy.deepcopy(model_a),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(profile),copy.deepcopy(completeness),copy.deepcopy(problems),'CHEM-C-G-PLAN-NO-ATTEMPT')
plan_b=build_plan(copy.deepcopy(model_b),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(profile),copy.deepcopy(completeness),copy.deepcopy(problems),'CHEM-C-G-PLAN-WITH-ATTEMPT')
required=set(study_scope['required_capability_refs'])
assert {x['capability_ref'] for x in plan_a['lessons']}==required
assert all(x['lesson_mode']=='FULL_LEARNING' for x in plan_a['lessons'])
assert lesson(plan_b,'CAP-PARSE-ION-CHARGE')['lesson_mode']=='CONCISE_VERIFY_ONLY'
assert any(x['lesson_mode']=='PROBE' for x in plan_b['lessons'])
assert not any(a['topic_scope_refs'] for l in plan_a['lessons'] for aid in l['pck_asset_refs'] for a in pck['assets'] if a['asset_id']==aid)
assert plan_a['appendices']['appendix_c']['answer_free'] is True and plan_a['appendices']['appendix_c']['introduced_capability_refs']==[]
assert {x['primary_capability_ref'] for x in plan_a['appendices']['appendix_a']['items']}==required
assert {x['item_ref'] for x in plan_a['appendices']['appendix_b']['solutions']}=={x['item_id'] for x in plan_a['appendices']['appendix_a']['items']}
assert not any(x['external_candidate_refs'] for x in plan_a['appendices']['appendix_a']['items'])
assert not any((l['worked_example'] or {}).get('external_candidate_refs') for l in plan_a['lessons'])

# Validate actual semantic products against contracts.
Draft202012Validator(load(D/'contracts'/'chemistry-promoted-pck.schema.json')).validate(pck)
Draft202012Validator(load(D/'contracts'/'chemistry-core1-study-plan.schema.json')).validate(plan_a)
lesson_schema=Draft202012Validator(load(D/'contracts'/'chemistry-core1-lesson.schema.json'))
for l in plan_a['lessons']+plan_b['lessons']: lesson_schema.validate(l)
Draft202012Validator(load(D/'contracts'/'chemistry-core-appendix-contract.schema.json')).validate(plan_a['appendices'])
Draft202012Validator(load(D/'contracts'/'chemistry-core-appendix-contract.schema.json')).validate(plan_b['appendices'])

# 1 CORE1_IS_ONLY_A_REPAIR_MEMO
bad=copy.deepcopy(plan_a); bad['lessons']=bad['lessons'][1:]; redigest_plan(bad)
expect('CORE1_IS_ONLY_A_REPAIR_MEMO',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 2 CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-READ-FORMULA')['worked_example']['external_candidate_refs']=['EXT01']; redigest_plan(bad)
expect('CORE1_REUSES_ORIGINAL_TRANSFER_AS_WORKED_EXAMPLE',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 3 PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY
badp=copy.deepcopy(pck); badp['assets'][0]['promotion_authority']={}; redigest_pck(badp)
expect('PCK_ASSET_WITHOUT_PROMOTION_AUTHORITY',lambda:validate_plan(plan_a,model_a,study_scope,badp,profile,completeness,problems))
# 4 PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-READ-FORMULA')['worked_example']['problem_family_ref']=''; redigest_plan(bad)
expect('PROBLEM_INSTANCE_WITHOUT_PROBLEM_FAMILY',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 5 FULL_LEARNING_TREATMENT_WITHOUT_REPRESENTATION_TRANSLATION
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-TRANSLATE-PARTICLE-SYMBOL')['representation_path']=[]; redigest_plan(bad)
expect('FULL_LEARNING_TREATMENT_WITHOUT_REPRESENTATION_TRANSLATION',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 6 NAKED_RULE_COUNTS_AS_CONCEPT_TEACHING
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-CHECK-RULE-EXCEPTION')['ordinary_language_explanation']=''; redigest_plan(bad)
expect('NAKED_RULE_COUNTS_AS_CONCEPT_TEACHING',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 7 CONDITION_EXCEPTION_DROPPED
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-CHECK-RULE-EXCEPTION')['condition_exception_obligations']=[]; redigest_plan(bad)
expect('CONDITION_EXCEPTION_DROPPED',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 8 MISCONCEPTION_WARNING_WITHOUT_REPAIR
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-PARSE-ION-CHARGE')['misconception_repair']['repair_steps']=[]; redigest_plan(bad)
expect('MISCONCEPTION_WARNING_WITHOUT_REPAIR',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 9 READY_CONTENT_PADDED_INTO_FULL_RETEACH
bad=copy.deepcopy(plan_b); x=lesson(bad,'CAP-PARSE-ION-CHARGE'); x['guided_attempt']=copy.deepcopy(lesson(plan_a,'CAP-PARSE-ION-CHARGE')['guided_attempt']); redigest_plan(bad)
expect('READY_CONTENT_PADDED_INTO_FULL_RETEACH',lambda:validate_plan(bad,model_b,study_scope,pck,profile,completeness,problems))
# 10 CHEMICAL_CHECK_REDUCED_TO_ANSWER_ONLY
bad=copy.deepcopy(plan_a); lesson(bad,'CAP-CHECK-ATOM-CONSERVATION')['worked_example']['verification_steps']=[]; redigest_plan(bad)
expect('CHEMICAL_CHECK_REDUCED_TO_ANSWER_ONLY',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 11 APPENDIX_A_MISSING
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_a']['present']=False; redigest_plan(bad)
expect('APPENDIX_A_MISSING',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 12 APPENDIX_B_MISSING
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_b']['present']=False; redigest_plan(bad)
expect('APPENDIX_B_MISSING',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 13 APPENDIX_C_MISSING
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_c']['present']=False; redigest_plan(bad)
expect('APPENDIX_C_MISSING',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 14 APPENDIX_A_USES_EXACT_EXAMSIDE_TRANSFER
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_a']['items'][0]['external_candidate_refs']=['EXT01']; redigest_plan(bad)
expect('APPENDIX_A_USES_EXACT_EXAMSIDE_TRANSFER',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 15 APPENDIX_B_INCOMPLETE
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_b']['solutions']=bad['appendices']['appendix_b']['solutions'][:-1]; redigest_plan(bad)
expect('APPENDIX_B_INCOMPLETE',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 16 HANDOUT_CONTAINS_ANSWERS
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_c']['answer_free']=False; redigest_plan(bad)
expect('HANDOUT_CONTAINS_ANSWERS',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))
# 17 HANDOUT_INTRODUCES_NEW_CHEMISTRY
bad=copy.deepcopy(plan_a); bad['appendices']['appendix_c']['introduced_capability_refs']=['CAP-READ-STRUCTURE-SITE']; redigest_plan(bad)
expect('HANDOUT_INTRODUCES_NEW_CHEMISTRY',lambda:validate_plan(bad,model_a,study_scope,pck,profile,completeness,problems))

# Treatment-relative sufficiency and authority boundaries.
assert lesson(plan_b,'CAP-PARSE-ION-CHARGE')['content_roles']==profile['content_roles_by_mode']['CONCISE_VERIFY_ONLY']
assert all(a['promotion_authority']['subject_expert_release_state']=='NOT_GRANTED' for a in pck['assets'])
assert all(a['raw_mature_reference_used'] is False for a in pck['assets'])
# Deterministic replay.
again=build_plan(copy.deepcopy(model_a),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(profile),copy.deepcopy(completeness),copy.deepcopy(problems),'CHEM-C-G-PLAN-NO-ATTEMPT')
assert json.dumps(plan_a,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-G required falsifiers = 17 PASS')
print('CHEMISTRY C-G promoted PCK pilot authority = PASS')
print('CHEMISTRY C-G treatment-relative Core1 authoring = PASS')
print('CHEMISTRY C-G Appendix A/B/C semantic closure = PASS')
print('CHEMISTRY C-G external transfer unspoiled = PASS')
print('CHEMISTRY C-G deterministic replay = PASS')
