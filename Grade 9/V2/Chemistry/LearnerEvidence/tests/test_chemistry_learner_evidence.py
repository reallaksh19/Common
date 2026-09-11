#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[str(D/'engine'),str(CHEM/'AssessmentReview'/'engine'),str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine')]
from infer_chemistry_learner_evidence import build_snapshot,digest
from review_chemistry_assessment import build_review,load_registry as load_review_registry
from build_chemistry_scope import build_scope
from build_chemistry_reasoning_semantics import build_semantics

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def cap(snapshot,ref): return next(x for x in snapshot['capability_states'] if x['capability_ref']==ref)
def case(snapshot,code): return next(x for x in snapshot['diagnostic_cases'] if x['hypothesis_code']==code)
def disposition(bundle,ref): return next(x for x in bundle['processed_evidence'] if x['observation_ref']==ref)['disposition']
A=CHEM/'AssessmentIntake'/'fixtures'; R=CHEM/'AssessmentReview'; S=CHEM/'AssessmentScope'; RS=CHEM/'ReasoningSemantics'; E=D
sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
review_reg,manifest_digest=load_review_registry(R/'registry'/'chemistry-item-validity-registry.json')
review=build_review(copy.deepcopy(sources),copy.deepcopy(questions),review_reg,load(R/'policies'/'chemistry-diagnostic-use-policy.json'),load(R/'registry'/'chemistry-qc-events.json'),registry_manifest_digest=manifest_digest)
source_ledger=load(S/'registry'/'chemistry-source-obligation-ledger.json'); qbindings=load(S/'registry'/'chemistry-question-capability-bindings.json'); external=load(S/'registry'/'chemistry-external-corpus-classification.json'); authority=load(S/'authority'/'chemistry-canonical-authority.json')
scope_bundle=build_scope(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(authority))
semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),load(RS/'registry'/'chemistry-problem-family-registry.json'),load(RS/'registry'/'chemistry-reasoning-role-registry.json'),load(RS/'registry'/'chemistry-guide-demand-badge-policy.json'))
registry=load(E/'registry'/'chemistry-observation-code-registry.json'); policy=load(E/'registry'/'chemistry-diagnostic-policy.json'); attempts=load(E/'fixtures'/'chemistry-diagnostic-attempt-set.fixture.json'); ledger=load(E/'fixtures'/'chemistry-learner-evidence-ledger.fixture.json')

# Branch A: no AttemptSet
no_attempt_bundle=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy))
no_attempt=no_attempt_bundle['snapshot']
assert no_attempt['attempt_mode']=='ABSENT'
assert no_attempt['support_policy']=='NEUTRAL_CONSERVATIVE'
assert not no_attempt['diagnostic_cases']
assert all(x['state']=='UNKNOWN' for x in no_attempt['capability_states'])
assert all(not x['negative_evidence_refs'] for x in no_attempt['capability_states'])

# Branch B: AttemptSet present
with_attempt=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy),copy.deepcopy(attempts),copy.deepcopy(ledger))
snap=with_attempt['snapshot']
assert snap['attempt_mode']=='PRESENT' and snap['support_policy']=='EVIDENCE_CONDITIONED'
assert no_attempt['assessment_scope_ref']==snap['assessment_scope_ref']
assert no_attempt['assessment_scope_digest']==snap['assessment_scope_digest']
assert no_attempt['scope_unchanged'] is True and snap['scope_unchanged'] is True

# Required Chemistry falsifiers
# 1 CORRECT_FORMULA_PARSE + BAD_ARITHMETIC != FORMULA_FAILURE
assert cap(snap,'CAP-PARSE-ION-CHARGE')['state']=='DEMONSTRATED'
assert disposition(with_attempt,'O02')=='SHARED_EXECUTION_ERROR_LOCALIZED'
# 2 CORRECT_OXIDATION_STATES + AGENT_INVERSION != OXIDATION_NUMBER_FAILURE
sem2=copy.deepcopy(semantics); rec=next(x for x in sem2['question_semantics'] if x['target_ref']=='CQ12')
for step in rec['reasoning_route']['steps']:
    if 'CAP-TRACK-OXIDATION-STATE' not in step['capability_refs']: step['capability_refs'].append('CAP-TRACK-OXIDATION-STATE')
led2=copy.deepcopy(ledger); led2['observations']=[
 {'observation_id':'OX1','attempt_ref':'DA02','item_ref':'CQ12','route_step_index':3,'route_role':'TRACK_SPECIES_OR_STATE_CHANGE','representation_level':'SYMBOLIC','observation_code':'CORRECT_OXIDATION_STATE_TRACKING','polarity':'POSITIVE','capability_refs':['CAP-TRACK-OXIDATION-STATE'],'evidence_fragment':'Oxidation states are tracked correctly.','observation_confidence':0.99,'extraction_confidence':0.99,'transcription_confidence':0.99},
 {'observation_id':'OX2','attempt_ref':'DA02','item_ref':'CQ12','route_step_index':4,'route_role':'CLASSIFY','representation_level':'SYMBOLIC','observation_code':'AGENT_ROLE_INVERSION','polarity':'NEGATIVE','capability_refs':['CAP-ATTACH-SPECIES-ROLE'],'evidence_fragment':'Agent role is inverted after correct oxidation-state tracking.','observation_confidence':0.99,'extraction_confidence':0.99,'transcription_confidence':0.99}]
led2['ledger_digest']=''; led2['ledger_digest']=digest(led2,'ledger_digest','observations','observation_id')
s2=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),sem2,copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy),copy.deepcopy(attempts),led2)['snapshot']
assert cap(s2,'CAP-TRACK-OXIDATION-STATE')['state']=='DEMONSTRATED'
assert cap(s2,'CAP-ATTACH-SPECIES-ROLE')['state']=='EVIDENCE_OF_DIFFICULTY'
# 3 CORRECT_PARTICLE_MODEL + SYMBOLIC_TRANSCRIPTION_ERROR != PARTICLE_MODEL_FAILURE
assert cap(snap,'CAP-TRANSLATE-PARTICLE-SYMBOL')['state']=='MIXED'
assert 'O05' in cap(snap,'CAP-TRANSLATE-PARTICLE-SYMBOL')['positive_evidence_refs']
# 4 CORRECT_OBSERVATION + OVERCLAIM != OBSERVATION_FAILURE
assert cap(snap,'CAP-SEPARATE-OBSERVATION-INFERENCE')['state']=='MIXED'
assert 'O07' in cap(snap,'CAP-SEPARATE-OBSERVATION-INFERENCE')['positive_evidence_refs']
# 5 CORRECT_BASE_RULE + MISSED_EXCEPTION != WHOLE_TOPIC_FAILURE
assert cap(snap,'CAP-CHECK-RULE-EXCEPTION')['state']=='MIXED'
assert 'O09' in cap(snap,'CAP-CHECK-RULE-EXCEPTION')['positive_evidence_refs']
# 6 NO_ATTEMPT != CHEMISTRY_WEAK
assert all(x['state']!='EVIDENCE_OF_DIFFICULTY' for x in no_attempt['capability_states'])
# 7 ONE_ERROR != CONFIRMED_MISCONCEPTION
assert case(snap,'AGENT_ROLE_INVERSION')['status']=='PROBE_REQUIRED'
assert not any(x['status']=='CONFIRMED' for x in snap['diagnostic_cases'])
# 8 INVALID_ITEM_PUNISHES_LEARNER
assert disposition(with_attempt,'O11')=='IGNORED_INVALID_ITEM'
assert cap(snap,'CAP-PARSE-ION-CHARGE')['state']!='EVIDENCE_OF_DIFFICULTY'
# 9 LOW_CONFIDENCE_OBSERVATION_BECOMES_CONFIDENT_STATE
assert disposition(with_attempt,'O12')=='LOW_CONFIDENCE_PROBE_REQUIRED'
assert cap(snap,'CAP-VERIFY-CHEMICAL-REPRESENTATION')['state']!='EVIDENCE_OF_DIFFICULTY'
# 10 SHARED_ARITHMETIC_FAILURE_ERASES_CHEMISTRY_REASONING
assert cap(snap,'CAP-PARSE-ION-CHARGE')['state']=='DEMONSTRATED'

# Two independent high-confidence negatives are required before CONFIRMED.
led3=copy.deepcopy(ledger); a2={'attempt_id':'DA08','question_ref':'CQ12','part_ref':None,'binding_method':'EXPLICIT_ID','response':'Agent role inverted again.'}; at3=copy.deepcopy(attempts); at3['attempts'].append(a2); at3['attempt_set_digest']=''; at3['attempt_set_digest']=digest(at3,'attempt_set_digest','attempts','attempt_id')
extra=copy.deepcopy(next(x for x in led3['observations'] if x['observation_id']=='O04')); extra.update({'observation_id':'O13','attempt_ref':'DA08'}); led3['attempt_set_ref']=at3['attempt_set_id']; led3['observations'].append(extra); led3['ledger_digest']=''; led3['ledger_digest']=digest(led3,'ledger_digest','observations','observation_id')
s3=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy),at3,led3)['snapshot']
assert case(s3,'AGENT_ROLE_INVERSION')['status']=='CONFIRMED'

again=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy),copy.deepcopy(attempts),copy.deepcopy(ledger))
assert json.dumps(with_attempt,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-E required falsifiers = 10 PASS')
print('CHEMISTRY C-E no-attempt branch = UNKNOWN / no negative diagnosis PASS')
print('CHEMISTRY C-E attempt branch = localized evidence PASS')
print('CHEMISTRY C-E assessment scope invariant = PASS')
print('CHEMISTRY C-E deterministic replay = PASS')
