#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
for name in ['chemistry-learner-study-scope.schema.json','chemistry-learner-study-model.schema.json']:
    schema=load(D/'contracts'/name); Draft202012Validator.check_schema(schema)
policy=load(D/'registry'/'chemistry-treatment-policy.json')
assert policy['subject']=='CHEMISTRY' and policy['schema_version']=='1.0.0'
required={'READY_VERIFY_ONLY','ACTIVE_STUDY','REPAIR_BEFORE','REPAIR_IN_UNIT','PROBE_FIRST'}
assert set(policy['required_pck_jobs_by_treatment'])==required
assert set(policy['priority_by_treatment'])==required
assert set(policy['state_to_treatment'])=={'UNKNOWN','DEMONSTRATED','EVIDENCE_OF_DIFFICULTY','MIXED'}
assert set(policy['no_attempt_forbidden_treatments'])=={'REPAIR_BEFORE','REPAIR_IN_UNIT'}
expected_dims={'acquisition','independent_reconstruction','delayed_retention','near_transfer','far_transfer','mixed_discrimination','representation_translation','condition_exception_discrimination','fluency','timed_performance'}
assert set(policy['longitudinal_dimensions'])==expected_dims
example=load(D/'registry'/'chemistry-longitudinal-binding.example.json')
assert example['subject']=='CHEMISTRY' and set(example['dimensions'])==expected_dims
assert example['dimensions']['delayed_retention']=='OPEN' and example['dimensions']['far_transfer']=='OPEN'
print('CHEMISTRY C-F contracts, treatment policy and longitudinal example = PASS')
