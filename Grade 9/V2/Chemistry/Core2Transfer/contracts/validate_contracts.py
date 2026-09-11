#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

schemas=[
 'chemistry-core2-transfer-plan.schema.json','chemistry-transfer-question-page.schema.json',
 'chemistry-hint-ladder.schema.json','chemistry-core1-core2-linkage.schema.json',
 'chemistry-solution-verification.schema.json','chemistry-concept-segregation.schema.json']
for name in schemas: Draft202012Validator.check_schema(load(D/'contracts'/name))
transfer=load(D/'registry'/'chemistry-transfer-badge-policy.json'); concept=load(D/'registry'/'chemistry-concept-segregation.json'); profile=load(D/'registry'/'chemistry-core2-authoring-profile.json')
assert transfer['subject']=='CHEMISTRY' and transfer['psychometric_claim_allowed'] is False
assert transfer['transfer_badges']==['CANONICAL_TRANSFER']
assert concept['subject']=='CHEMISTRY' and concept['mappings']
for qf,m in concept['mappings'].items():
    assert m['primary_concept_ref'] not in m['supporting_concept_refs'],qf
    assert m['primary_capability_ref'] not in m['supporting_capability_refs'],qf
    assert qf in profile['workspace_by_family'] and qf in profile['hints_by_family'] and qf in profile['solution_steps_by_family']
    h=profile['hints_by_family'][qf]
    assert len({h['H1_NOTICE'],h['H2_RULE_MODEL_REPRESENTATION'],h['H3_START']})==3,qf
print('CHEMISTRY C-I six contracts = PASS')
print('CHEMISTRY C-I badge policy = PASS')
print('CHEMISTRY C-I concept segregation = PASS')
print('CHEMISTRY C-I authoring profile = PASS')
