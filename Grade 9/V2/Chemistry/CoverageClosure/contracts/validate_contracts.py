#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(D/'engine'))
from freeze_chemistry_source_denominator import validate_profile
from validate_chemistry_answer_custody import load_profile as load_answer_custody_profile, reconcile_authored_baselines
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

schemas=[
 'chemistry-source-coverage-matrix.schema.json',
 'chemistry-external-corpus-coverage-matrix.schema.json',
 'chemistry-transfer-evidence-event.schema.json',
 'chemistry-learner-state-update.schema.json',
 'chemistry-longitudinal-update.schema.json',
 'chemistry-publication-coverage-closure.schema.json',
 'chemistry-source-ingestion-profile.schema.json',
]
for name in schemas:
    s=load(D/'contracts'/name); Draft202012Validator.check_schema(s)

event_schema=Draft202012Validator(load(D/'contracts'/'chemistry-transfer-evidence-event.schema.json'))
fixture=load(D/'fixtures'/'chemistry-transfer-evidence.fixture.json')
assert fixture['subject']=='CHEMISTRY'
for e in fixture['events']: event_schema.validate(e)
policy=load(D/'registry'/'chemistry-transfer-evidence-policy.json')
assert policy['subject']=='CHEMISTRY'
assert policy['support_states']['H3_SUCCESS']['independent'] is False
assert policy['support_states']['SOLUTION_EXPOSED']['mastery_eligible'] is False
assert policy['current_success_may_close_future_obligations'] is False
assert {'POSITIVE_EVIDENCE_ONLY','EXCLUDE_FROM_NEGATIVE_INFERENCE'}<=set(policy['negative_inference_blocked_for'])
ingestion=load(D/'registry'/'chemistry-source-ingestion-profile.json')
Draft202012Validator(load(D/'contracts'/'chemistry-source-ingestion-profile.schema.json')).validate(ingestion)
validate_profile(ingestion,D.parents[3])
assert ingestion['unresolved_counter_policy']=='RECORD_AS_UNRESOLVED_NEVER_INFER'
assert ingestion['authoring_requires_freeze_state']==['FROZEN_ITEM_LEDGER']
print('CHEMISTRY C-J schemas = 7 PASS')
print('CHEMISTRY C-J transfer evidence fixture = PASS')
print('CHEMISTRY C-J longitudinal policy = PASS')
print('CHEMISTRY C-J source-ingestion denominator profile = %d frozen instances PASS'%len(ingestion['frozen_instances']))
custody=load_answer_custody_profile()
assert custody['hint_is_not_an_answer_path'] is True
assert custody['closed_invariant']=='questions_total == immediate_answer_checks_total == full_solutions_total'
assert {'QUESTION_WITHOUT_ANSWER_PATH','QUESTION_WITHOUT_IMMEDIATE_CHECK','QUESTION_WITHOUT_FULL_SOLUTION','OPEN_RESPONSE_WITHOUT_RUBRIC','ANSWER_COUNT_RECONCILIATION_FAILURE'}<=set(custody['falsifiers'])
baselines=reconcile_authored_baselines(custody,D.parents[3])
print('CHEMISTRY C-J answer-custody profile = PR #346 baselines %s reconciled PASS'%'/'.join(str(baselines[k]['questions_total']) for k in ['some-basic-concepts','behaviour-of-gases','chemical-bonding','redox-reactions']))
