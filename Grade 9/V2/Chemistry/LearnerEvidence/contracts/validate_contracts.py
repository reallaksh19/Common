#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parent; E=D.parent; CHEM=E.parent; SHARED=CHEM.parent/'Shared'/'LearnerIntelligence'/'contracts'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
for p in [SHARED/'learner-evidence-ledger.schema.json',SHARED/'diagnostic-case.schema.json',SHARED/'learner-state-snapshot.schema.json',D/'chemistry-reasoning-observation.schema.json']:
    Draft202012Validator.check_schema(load(p))
ledger=load(E/'fixtures'/'chemistry-learner-evidence-ledger.fixture.json'); Draft202012Validator(load(SHARED/'learner-evidence-ledger.schema.json')).validate(ledger)
obs_schema=load(D/'chemistry-reasoning-observation.schema.json')
for o in ledger['observations']: Draft202012Validator(obs_schema).validate(o)
attempts=load(E/'fixtures'/'chemistry-diagnostic-attempt-set.fixture.json'); Draft202012Validator(load(CHEM/'AssessmentIntake'/'contracts'/'attempt-set.schema.json')).validate(attempts)
registry=load(E/'registry'/'chemistry-observation-code-registry.json'); codes={x['code'] for x in registry['codes']}
required={'CORRECT_FORMULA_PARSE','CORRECT_CHARGE_PARSE','CORRECT_REPRESENTATION_LEVEL','CORRECT_RULE_SELECTION','CORRECT_CONDITION_SELECTION','CORRECT_EXCEPTION_RECOGNITION','CORRECT_CONSERVATION_SETUP','CORRECT_SPECIES_TRACKING','CORRECT_REACTION_CLASSIFICATION','CORRECT_PARTICLE_MODEL','CORRECT_EXPERIMENTAL_OBSERVATION','CORRECT_EVIDENCE_TO_CLAIM_LINK','SYMBOLIC_TRANSCRIPTION_ERROR','CHARGE_SUBSCRIPT_CONFUSION','RULE_EXCEPTION_MISSED','AGENT_ROLE_INVERSION','SPECTATOR_ROLE_CONFUSION','PARTICLE_SYMBOLIC_TRANSLATION_ERROR','OVERCLAIM_FROM_OBSERVATION','ARITHMETIC_EXECUTION_ERROR','VERIFICATION_NOT_PERFORMED','VERIFICATION_FAILED'}
assert required<=codes
policy=load(E/'registry'/'chemistry-diagnostic-policy.json')
assert policy['one_error_confirms_misconception'] is False
assert policy['shared_execution_errors_do_not_erase_chemistry_state'] is True
assert policy['no_attempt_state']=='UNKNOWN'
print('CHEMISTRY C-E shared + Chemistry contracts = PASS')
