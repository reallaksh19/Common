#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[
 str(D/'engine'),str(CHEM/'Core2Transfer'/'engine'),str(CHEM/'Representation'/'engine'),
 str(CHEM/'CoreAuthoring'/'engine'),str(CHEM/'AssessmentReview'/'engine'),
 str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine'),
 str(CHEM/'LearnerEvidence'/'engine'),str(CHEM/'LearnerStudy'/'engine')]
from build_chemistry_coverage_closure import build_closure,validate_closure,digest
from build_chemistry_core2_transfer import build_plan as build_core2
from build_chemistry_representations import build_bundle as build_representations
from build_chemistry_core1 import build_plan as build_core1,load_pck_registry
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
def redigest(o,field): o[field]=''; o[field]=digest(o,field)
def smrow(cl,ref): return next(x for x in cl['source_matrix']['records'] if x['obligation_ref']==ref)
def emrow(cl,ref): return next(x for x in cl['external_matrix']['records'] if x['candidate_ref']==ref)
def update(cl,eid): return next(x for x in cl['learner_state_updates'] if x['event_ref']==eid)
def longrow(cl,cap): return next(x for x in cl['longitudinal_update']['records'] if x['capability_ref']==cap)

A=CHEM/'AssessmentIntake'/'fixtures'; R=CHEM/'AssessmentReview'; S=CHEM/'AssessmentScope'; RS=CHEM/'ReasoningSemantics'; E=CHEM/'LearnerEvidence'; LS=CHEM/'LearnerStudy'; CA=CHEM/'CoreAuthoring'; REP=CHEM/'Representation'; C2=CHEM/'Core2Transfer'
sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
review_reg,manifest_digest=load_review_registry(R/'registry'/'chemistry-item-validity-registry.json')
review=build_review(copy.deepcopy(sources),copy.deepcopy(questions),review_reg,load(R/'policies'/'chemistry-diagnostic-use-policy.json'),load(R/'registry'/'chemistry-qc-events.json'),registry_manifest_digest=manifest_digest)
source_ledger=load(S/'registry'/'chemistry-source-obligation-ledger.json'); qbindings=load(S/'registry'/'chemistry-question-capability-bindings.json'); external=load(S/'registry'/'chemistry-external-corpus-classification.json'); authority=load(S/'authority'/'chemistry-canonical-authority.json')
scope=build_scope(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(authority))
families=load(RS/'registry'/'chemistry-problem-family-registry.json'); guide=load(RS/'registry'/'chemistry-guide-demand-badge-policy.json')
semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(families),load(RS/'registry'/'chemistry-reasoning-role-registry.json'),copy.deepcopy(guide))
no_attempt=build_snapshot(copy.deepcopy(scope),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),load(E/'registry'/'chemistry-observation-code-registry.json'),load(E/'registry'/'chemistry-diagnostic-policy.json'))
study_scope=derive_study_scope(copy.deepcopy(scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
model=build_model(copy.deepcopy(study_scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(no_attempt),load(LS/'registry'/'chemistry-treatment-policy.json'),'CHEM-C-J-UPSTREAM')
pck=load_pck_registry(); core_profile=load(CA/'registry'/'chemistry-instructional-authoring-profile.json'); completeness=load(CA/'registry'/'chemistry-core1-scope-completeness-policy.json'); problems=load(CA/'registry'/'chemistry-problem-authoring-profile.json')
core1=build_core1(copy.deepcopy(model),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(core_profile),copy.deepcopy(completeness),copy.deepcopy(problems),'CHEM-C-J-CORE1')
primitives=load(REP/'registry'/'chemistry-teaching-primitive-registry.json'); rep_profile=load(REP/'registry'/'chemistry-page-intent-profile.json'); notation=load(REP/'registry'/'chemistry-notation-render-contract.json')
representations=build_representations(copy.deepcopy(core1),copy.deepcopy(model),copy.deepcopy(primitives),copy.deepcopy(rep_profile),copy.deepcopy(notation),'CHEM-C-J-REPRESENTATIONS')
bodies=load(C2/'fixtures'/'chemistry-external-transfer-source.fixture.json'); transfer=load(C2/'registry'/'chemistry-transfer-badge-policy.json'); concepts=load(C2/'registry'/'chemistry-concept-segregation.json'); c2profile=load(C2/'registry'/'chemistry-core2-authoring-profile.json')
core2=build_core2(copy.deepcopy(corpus),copy.deepcopy(external),copy.deepcopy(bodies),copy.deepcopy(core1),copy.deepcopy(model),copy.deepcopy(families),copy.deepcopy(guide),copy.deepcopy(transfer),copy.deepcopy(concepts),copy.deepcopy(c2profile),copy.deepcopy(primitives),copy.deepcopy(notation),'CHEM-C-J-CORE2')
fixture=load(D/'fixtures'/'chemistry-transfer-evidence.fixture.json'); events=fixture['events']; policy=load(D/'registry'/'chemistry-transfer-evidence-policy.json')
args=(source_ledger,corpus,external,model,core1,representations,core2,families,events,policy)
closure=build_closure(*copy.deepcopy(args))

assert closure['summary']['source_obligations_required']==10
assert closure['summary']['source_obligations_closed']==10
assert closure['summary']['external_candidates_total']==6
assert closure['summary']['eligible_external_total']==5
assert closure['summary']['eligible_external_placed_unique']==5
assert closure['external_matrix']['summary']['missing_total']==0
assert closure['external_matrix']['summary']['duplicate_primary_total']==0
assert update(closure,'TE-EXT02-01')['independent_success'] is False
assert update(closure,'TE-EXT03-01')['mastery_claim'] is False
assert 'RULE_SELECTION' in update(closure,'TE-EXT01-01')['positive_dimensions']
assert update(closure,'TE-EXT04-01')['negative_inference_applied'] is False
assert update(closure,'TE-EXT05-01')['current_episode_state']=='PARTIAL_OR_INVALID_REASONING'

Draft202012Validator(load(D/'contracts'/'chemistry-source-coverage-matrix.schema.json')).validate(closure['source_matrix'])
Draft202012Validator(load(D/'contracts'/'chemistry-external-corpus-coverage-matrix.schema.json')).validate(closure['external_matrix'])
Draft202012Validator(load(D/'contracts'/'chemistry-publication-coverage-closure.schema.json')).validate(closure)
us=Draft202012Validator(load(D/'contracts'/'chemistry-learner-state-update.schema.json'))
for u in closure['learner_state_updates']: us.validate(u)
Draft202012Validator(load(D/'contracts'/'chemistry-longitudinal-update.schema.json')).validate(closure['longitudinal_update'])

bad=copy.deepcopy(closure); smrow(bad,'CO-CS01')['core1_lesson_refs']=[]; redigest(bad['source_matrix'],'matrix_digest'); redigest(bad,'closure_digest')
expect('SOURCE_OBLIGATION_WITHOUT_CORE1_COVERAGE',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); smrow(bad,'CO-CS02')['appendix_b_solution_refs']=[]; redigest(bad['source_matrix'],'matrix_digest'); redigest(bad,'closure_digest')
expect('APPENDIX_A_WITHOUT_APPENDIX_B_SOLUTION',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); smrow(bad,'CO-CS03')['appendix_c_capability_refs']=[]; redigest(bad['source_matrix'],'matrix_digest'); redigest(bad,'closure_digest')
expect('APPENDIX_C_REQUIRED_SUPPORT_MISSING',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); x=emrow(bad,'EXT01'); x['placement_status']='MISSING'; x['core2_page_refs']=[]; x['primary_concept_refs']=[]; redigest(bad['external_matrix'],'matrix_digest'); redigest(bad,'closure_digest')
expect('ELIGIBLE_EXTERNAL_QUESTION_WITHOUT_CORE2_TRANSFER',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); x=emrow(bad,'EXT02'); x['placement_status']='DUPLICATE'; x['core2_page_refs']=['EXT02','EXT02']; x['primary_concept_refs']=[x['primary_concept_refs'][0],x['primary_concept_refs'][0]]; redigest(bad['external_matrix'],'matrix_digest'); redigest(bad,'closure_digest')
expect('DUPLICATE_PRIMARY_PLACEMENT',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); bad['summary']['eligible_external_placed_unique']=99; redigest(bad,'closure_digest')
expect('SUMMARY_COUNTERS_NOT_DERIVED_FROM_RECORDS',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); u=update(bad,'TE-EXT02-01'); u['independent_success']=True; u['current_episode_state']='CURRENT_DEMONSTRATED_INDEPENDENT'; redigest(u,'update_digest'); redigest(bad,'closure_digest')
expect('H3_SUCCESS_RECORDED_AS_INDEPENDENT_SUCCESS',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); u=update(bad,'TE-EXT03-01'); u['mastery_claim']=True; redigest(u,'update_digest'); redigest(bad,'closure_digest')
expect('SOLUTION_EXPOSED_RECORDED_AS_MASTERY',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); u=update(bad,'TE-EXT01-01'); u['positive_dimensions']=[]; redigest(u,'update_digest'); redigest(bad,'closure_digest')
expect('ARITHMETIC_FAILURE_ERASES_RULE_SELECTION_SUCCESS',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); u=update(bad,'TE-EXT05-01'); u['mastery_claim']=True; u['independent_success']=True; u['current_episode_state']='CURRENT_DEMONSTRATED_INDEPENDENT'; redigest(u,'update_digest'); redigest(bad,'closure_digest')
expect('CORRECT_ANSWER_WITH_INVALID_CHEMISTRY_RECORDED_AS_FULL_SUCCESS',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); lr=longrow(bad,'CAP-PARSE-ION-CHARGE'); lr['remaining_future_evidence_obligations']=lr['remaining_future_evidence_obligations'][1:]; redigest(bad['longitudinal_update'],'update_digest'); redigest(bad,'closure_digest')
expect('CURRENT_SUCCESS_ERASES_FUTURE_RETRIEVAL',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); u=update(bad,'TE-EXT04-01'); u['negative_inference_applied']=True; u['current_episode_state']='DIFFICULTY_EVIDENCE'; redigest(u,'update_digest'); redigest(bad,'closure_digest')
expect('NEGATIVE_EVIDENCE_FROM_EXCLUDED_ITEM',lambda:validate_closure(bad,*args))
bad=copy.deepcopy(closure); lr=longrow(bad,'CAP-CHECK-ATOM-CONSERVATION'); lr['obligation_owners']=lr['obligation_owners'][1:]; redigest(bad['longitudinal_update'],'update_digest'); redigest(bad,'closure_digest')
expect('LONGITUDINAL_OBLIGATION_DISAPPEARS',lambda:validate_closure(bad,*args))

again=build_closure(*copy.deepcopy(args))
assert json.dumps(closure,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-J required falsifiers = 13 PASS')
print('CHEMISTRY C-J source coverage = 10/10 PASS')
print('CHEMISTRY C-J external placement = 5/5 of 6-candidate denominator PASS')
print('CHEMISTRY C-J support-state evidence semantics = PASS')
print('CHEMISTRY C-J longitudinal future obligations preserved = PASS')
print('CHEMISTRY C-J deterministic replay = PASS')
