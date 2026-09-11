#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

COLD=Path(__file__).resolve().parents[1]; CHEM=COLD.parent
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=dict(o)
    if field:x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()

for n in ['chemistry-cold-start-run-report.schema.json','chemistry-two-product-package.schema.json','chemistry-cold-start-comparison.schema.json']:
    Draft202012Validator.check_schema(load(COLD/'contracts'/n))
manifest=load(CHEM/'CHEMISTRY_GENERATION_AUTHORITY_MANIFEST.json')
assert manifest['manifest_digest']==digest(manifest,'manifest_digest')
assert manifest['subject']=='CHEMISTRY'
assert manifest['runtime_input_contract']['required']==['ChemistrySourceSet','QuestionSetOrCorpusSet','DeclaredTopicScope']
assert manifest['runtime_input_contract']['optional']==['AttemptSet']
assert len(manifest['two_product_topology'])==2
assert 'APPENDIX_C_PRINTABLE_HANDOUT' in next(x for x in manifest['two_product_topology'] if x['product_id']=='CORE_STUDY_GUIDE')['required_sections']
assert not any('AssessmentScope/registry/chemistry-source-obligation-ledger' in x for x in manifest['authorities'].values())
assert not any('AssessmentScope/registry/chemistry-question-capability-bindings' in x for x in manifest['authorities'].values())
assert not any('AssessmentScope/registry/chemistry-external-corpus-classification' in x for x in manifest['authorities'].values())
policy=load(COLD/'registry'/'chemistry-cold-start-derivation-policy.json')
for group in ['source_rules','question_rules','external_rules']:
    for r in policy[group]:
        assert not ({'source_unit_id','question_id','candidate_id'} & set(r)), (group,r['rule_id'])
        assert r['match_any'] and r['capability_refs'] and r['concept_refs'] and r['problem_family_ref']
print('CHEMISTRY C-K schemas = 3 PASS')
print('CHEMISTRY C-K authority manifest = PASS')
print('CHEMISTRY C-K raw-evidence derivation policy = PASS')
