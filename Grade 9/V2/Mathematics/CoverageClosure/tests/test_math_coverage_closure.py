#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D=Path(__file__).resolve().parents[1]; MATH=D.parent
sys.path[:0]=[
 str(D/'engine'),str(MATH/'LearnerIntelligence'/'engine'),str(MATH/'StudySynthesis'/'engine'),
 str(MATH/'ProblemSemantics'/'engine'),str(MATH/'Core2Transfer'/'engine')]
from build_math_coverage_closure import build_package,validate_package,digest,FUTURE_DIMS
from derive_math_learner_state import derive
from synthesize_math_study_model import build_study_scope,synthesize
from build_math_problem_semantics import build_package as build_semantics,load_family_registry
from build_math_core2_transfer import build_plan as build_core2

def L(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError('expected '+code)
def event(pkg,q): return next(x for x in pkg['transfer_evidence_events'] if x['question_ref']==q)
def state_update(pkg,eid): return next(x for x in pkg['learner_state_updates'] if x['event_ref']==eid)
def long_update(pkg,eid): return next(x for x in pkg['longitudinal_updates'] if x['event_ref']==eid)
def reseal_state(u): u['update_digest']=digest(u,'update_digest')
def reseal_long(u): u['update_digest']=digest(u,'update_digest')
def reseal_pkg(p): p['package_digest']=digest(p,'package_digest')

Q=L(MATH/'AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json')
S=L(MATH/'AssessmentIntake/fixtures/mixed-grade9-topic-scope.fixture.json')
RR=L(MATH/'AssessmentReview/registry/assessment-item-validity-registry.json')
RP=L(MATH/'AssessmentReview/policies/diagnostic-use-policy.json')
A=L(MATH/'AssessmentScope/authority/math-assessment-scope-authority.json')
B=L(MATH/'AssessmentScope/registry/mixed-grade9-question-scope-bindings.json')
ROLE=L(MATH/'ProblemSemantics/registry/math-reasoning-role-registry.json')
FAM=load_family_registry(MATH/'ProblemSemantics/registry/math-problem-family-registry.json')
VER=L(MATH/'ProblemSemantics/registry/math-verification-route-registry.json')
ITEM=L(MATH/'ProblemSemantics/registry/mixed-grade9-item-semantics.json')
DPOL=L(MATH/'ProblemSemantics/registry/guide-demand-badge-policy.json')
PS=build_semantics(Q,S,RR,RP,A,B,ROLE,FAM,VER,ITEM,DPOL)
OBS=L(MATH/'LearnerIntelligence/registry/math-observation-type-registry.json')
prior=derive(Q,RR,A,ITEM,OBS)['learner_state_snapshot']
scope=build_study_scope(B,A)
MF=L(MATH/'StudySynthesis/policies/math-treatment-policy.json')
study=synthesize(scope,prior,MF)
PRIM=L(MATH/'RepresentationSemantics/registry/math-teaching-primitive-registry.json')
PINT=L(MATH/'RepresentationSemantics/policies/math-page-intent-profile.json')
MI=L(MATH/'Core2Transfer/registry/math-core2-authoring-profile.json')
core2=build_core2(Q,RR,RP,B,A,PS,VER,PRIM,PINT,MI,None)
OUT=L(D/'fixtures/math-transfer-outcomes.fixture.json')
POL=L(D/'registry/math-transfer-evidence-policy.json')
ARGS=(Q,B,study,prior,core2,OUT,POL)
pkg=build_package(*copy.deepcopy(ARGS))

# Core closure structure.
assert len(pkg['assessment_coverage_matrix']['rows'])==17
assert {r['item_ref'] for r in pkg['assessment_coverage_matrix']['rows']}=={b['item_ref'] for b in B['bindings']}
assert {r['question_ref'] for r in pkg['assessment_coverage_matrix']['rows']}=={f'Q{i}' for i in range(1,15)}
assert pkg['publication_coverage_closure']['semantic_closure_status']=='PASS'
assert pkg['publication_coverage_closure']['publication_closure_status']=='BLOCKED_UPSTREAM_PCK_PROMOTION'
assert pkg['publication_coverage_closure']['publication_blockers']
assert all(not xs for xs in pkg['publication_coverage_closure']['gap_report'].values())
assert all(r['core1_links'] and r['core1_problem_authoring_obligation_refs'] for r in pkg['assessment_coverage_matrix']['rows'])
assert all(r['core2_page_digest'] and r['reasoning_route_ref'] and r['verification_obligation_refs'] for r in pkg['assessment_coverage_matrix']['rows'])

# Evidence state distinctions.
assert event(pkg,'Q7')['evidence_state']=='INDEPENDENT_SUCCESS'
assert event(pkg,'Q10')['evidence_state']=='H1_SUCCESS'
assert event(pkg,'Q11')['evidence_state']=='H2_SUCCESS'
assert event(pkg,'Q12')['evidence_state']=='H3_SUCCESS'
assert event(pkg,'Q14')['evidence_state']=='SOLUTION_EXPOSED'
assert event(pkg,'Q5')['evidence_state']=='INCORRECT_AFTER_SUPPORT'
assert event(pkg,'Q4')['evidence_state']=='NO_ATTEMPT'
assert event(pkg,'Q8')['verification_state']=='VERIFICATION_FAILURE'
assert event(pkg,'Q9')['assessment_validity_state']=='UNDERDETERMINED' and event(pkg,'Q9')['negative_inference_allowed'] is False

q7u=state_update(pkg,event(pkg,'Q7')['event_id'])
assert all(x['independent_success_increment']==1 and x['resulting_readiness']=='READY' for x in q7u['capability_updates'])
q12u=state_update(pkg,event(pkg,'Q12')['event_id'])
assert all(x['independent_success_increment']==0 and x['assisted_success_increment']==1 for x in q12u['capability_updates'])
q14u=state_update(pkg,event(pkg,'Q14')['event_id'])
assert all(x['state_changed'] is False and x['evidence_class']=='NON_DIAGNOSTIC' for x in q14u['capability_updates'])
q9u=state_update(pkg,event(pkg,'Q9')['event_id'])
assert all(x['negative_evidence_increment']==0 for x in q9u['capability_updates'])

q7l=long_update(pkg,event(pkg,'Q7')['event_id'])
for cap in q7l['capability_obligations']:
    by={x['dimension']:x for x in cap['dimensions']}
    assert by['acquisition']['resulting_status']=='CURRENT_EVIDENCE'
    assert by['independent_reconstruction']['resulting_status']=='CURRENT_EVIDENCE'
    assert all(by[d]['resulting_status']=='OPEN_FUTURE_EVIDENCE' and not by[d]['closed_by_event'] for d in FUTURE_DIMS)

# Validate the product against first-class M-J contracts.
store={}
for sp in (D/'contracts').glob('*.schema.json'):
    doc=L(sp); store[doc['$id']]=doc
root=store['math-coverage-closure-package.schema.json']; resolver=RefResolver.from_schema(root,store=store)
Draft202012Validator(root,resolver=resolver).validate(pkg)
for e in pkg['transfer_evidence_events']: Draft202012Validator(store['math-transfer-evidence-event.schema.json'],resolver=resolver).validate(e)
for u in pkg['learner_state_updates']: Draft202012Validator(store['math-learner-state-update.schema.json'],resolver=resolver).validate(u)
for u in pkg['longitudinal_updates']: Draft202012Validator(store['math-longitudinal-update.schema.json'],resolver=resolver).validate(u)

# 1 QUESTION_WITHOUT_CORE1_COVERAGE
badcore=copy.deepcopy(core2); p=next(x for x in badcore['pages'] if x['question_ref']=='Q7'); p['core1_lesson_refs']=[]
expect('QUESTION_WITHOUT_CORE1_COVERAGE',lambda:build_package(Q,B,study,prior,badcore,OUT,POL))
# 2 QUESTION_WITHOUT_CORE2_TRANSFER
badcore=copy.deepcopy(core2); badcore['pages']=[x for x in badcore['pages'] if x['question_ref']!='Q3']
expect('QUESTION_WITHOUT_CORE2_TRANSFER',lambda:build_package(Q,B,study,prior,badcore,OUT,POL))
# 3 CAPABILITY_WITHOUT_INSTRUCTIONAL_TREATMENT
badstudy=copy.deepcopy(study); target=next(b for b in B['bindings'] if b['item_ref']=='Q5')['canonical_capability_refs'][0]; badstudy['capability_plans']=[x for x in badstudy['capability_plans'] if x['capability_ref']!=target]
expect('CAPABILITY_WITHOUT_INSTRUCTIONAL_TREATMENT',lambda:build_package(Q,B,badstudy,prior,core2,OUT,POL))
# 4 CORE2_PAGE_WITHOUT_SOURCE_QUESTION_CUSTODY
badcore=copy.deepcopy(core2); next(x for x in badcore['pages'] if x['question_ref']=='Q7')['source_ref']='0'*64
expect('CORE2_PAGE_WITHOUT_SOURCE_QUESTION_CUSTODY',lambda:build_package(Q,B,study,prior,badcore,OUT,POL))
# 5 REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY
badcore=copy.deepcopy(core2); next(x for x in badcore['pages'] if x['question_ref']=='Q8')['reasoning_route']['primary_family_ref']='MATH-PF-INVENTED'
expect('REASONING_ROUTE_WITHOUT_PROBLEM_FAMILY_AUTHORITY',lambda:build_package(Q,B,study,prior,badcore,OUT,POL))
# 6 EVIDENCE_EVENT_WITHOUT_SOURCE_QUESTION
badout=copy.deepcopy(OUT); badout['outcomes'][0]['question_ref']='Q99'
expect('EVIDENCE_EVENT_WITHOUT_SOURCE_QUESTION',lambda:build_package(Q,B,study,prior,core2,badout,POL))
# 7 H3_SUCCESS_RECORDED_AS_INDEPENDENT_SUCCESS
bad=copy.deepcopy(pkg); e=event(bad,'Q12'); u=state_update(bad,e['event_id']); u['capability_updates'][0]['independent_success_increment']=1; reseal_state(u); reseal_pkg(bad)
expect('H3_SUCCESS_RECORDED_AS_INDEPENDENT_SUCCESS',lambda:validate_package(bad,Q,B,study,prior,core2,POL))
# 8 SOLUTION_EXPOSED_RECORDED_AS_MASTERY
bad=copy.deepcopy(pkg); e=event(bad,'Q14'); u=state_update(bad,e['event_id']); u['capability_updates'][0]['resulting_readiness']='READY'; u['capability_updates'][0]['state_changed']=True; reseal_state(u); reseal_pkg(bad)
expect('SOLUTION_EXPOSED_RECORDED_AS_MASTERY',lambda:validate_package(bad,Q,B,study,prior,core2,POL))
# 9 CURRENT_SUCCESS_ERASES_FUTURE_RETRIEVAL
bad=copy.deepcopy(pkg); e=event(bad,'Q7'); u=long_update(bad,e['event_id']); d=next(x for x in u['capability_obligations'][0]['dimensions'] if x['dimension']=='delayed_retention'); d['resulting_status']='CURRENT_EVIDENCE'; d['closed_by_event']=True; reseal_long(u); reseal_pkg(bad)
expect('CURRENT_SUCCESS_ERASES_FUTURE_RETRIEVAL',lambda:validate_package(bad,Q,B,study,prior,core2,POL))
# 10 LONGITUDINAL_OBLIGATION_DISAPPEARS
bad=copy.deepcopy(pkg); e=event(bad,'Q10'); u=long_update(bad,e['event_id']); u['capability_obligations'][0]['dimensions']=u['capability_obligations'][0]['dimensions'][:-1]; reseal_long(u); reseal_pkg(bad)
expect('LONGITUDINAL_OBLIGATION_DISAPPEARS',lambda:validate_package(bad,Q,B,study,prior,core2,POL))
# 11 TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS
bad=copy.deepcopy(pkg); eid=bad['transfer_evidence_events'][0]['event_id']; bad['learner_state_updates']=[x for x in bad['learner_state_updates'] if x['event_ref']!=eid]; reseal_pkg(bad)
expect('TRANSFER_EVENT_WITHOUT_LEARNER_STATE_UPDATE_SEMANTICS',lambda:validate_package(bad,Q,B,study,prior,core2,POL))
# 12 ASSESSMENT_SAFETY_POLICY_LOST (Q9 negative evidence)
bad=copy.deepcopy(pkg); e=event(bad,'Q9'); u=state_update(bad,e['event_id']); u['capability_updates'][0]['negative_evidence_increment']=1; reseal_state(u); reseal_pkg(bad)
expect('ASSESSMENT_SAFETY_POLICY_LOST',lambda:validate_package(bad,Q,B,study,prior,core2,POL))
# 13 ASSESSMENT_COVERAGE_ROW_GAP
bad=copy.deepcopy(pkg); bad['assessment_coverage_matrix']['rows']=bad['assessment_coverage_matrix']['rows'][:-1]; bad['assessment_coverage_matrix']['matrix_digest']=digest(bad['assessment_coverage_matrix'],'matrix_digest'); reseal_pkg(bad)
expect('ASSESSMENT_COVERAGE_ROW_GAP',lambda:validate_package(bad,Q,B,study,prior,core2,POL))

again=build_package(*copy.deepcopy(ARGS))
assert json.dumps(pkg,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('MATH M-J assessment coverage = 17/17 item bindings PASS')
print('MATH M-J transfer evidence support-state separation = PASS')
print('MATH M-J assessment-safety feedback = PASS')
print('MATH M-J longitudinal future-obligation preservation = PASS')
print('MATH M-J publication closure fail-closed on M-G PCK gate = PASS')
print('MATH M-J required falsifiers = 13 PASS')
print('MATH M-J deterministic replay = PASS')
