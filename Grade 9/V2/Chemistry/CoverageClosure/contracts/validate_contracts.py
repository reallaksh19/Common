#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

schemas=[
 'chemistry-source-coverage-matrix.schema.json',
 'chemistry-external-corpus-coverage-matrix.schema.json',
 'chemistry-transfer-evidence-event.schema.json',
 'chemistry-learner-state-update.schema.json',
 'chemistry-longitudinal-update.schema.json',
 'chemistry-publication-coverage-closure.schema.json',
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
print('CHEMISTRY C-J schemas = 6 PASS')
print('CHEMISTRY C-J transfer evidence fixture = PASS')
print('CHEMISTRY C-J longitudinal policy = PASS')
