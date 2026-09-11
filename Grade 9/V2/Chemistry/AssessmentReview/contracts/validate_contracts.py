#!/usr/bin/env python3
import copy, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
C = D / 'contracts'

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def digest_without(value, field):
    x=copy.deepcopy(value); x.pop(field,None); return hashlib.sha256(canonical(x)).hexdigest()

def validate(name, value):
    schema = load(C / name)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            print(f'{name}: {list(err.path)}: {err.message}')
        raise SystemExit(1)

policy = load(D / 'policies' / 'chemistry-diagnostic-use-policy.json')
manifest = load(D / 'registry' / 'chemistry-item-validity-registry.json')
qc = load(D / 'registry' / 'chemistry-qc-events.json')
cases = load(D / 'fixtures' / 'chemistry-review-cases.fixture.json')

validate('chemistry-diagnostic-use-policy.schema.json', policy)
validate('chemistry-item-validity-registry.schema.json', manifest)
if manifest['registry_digest'] != digest_without(manifest,'registry_digest'):
    raise SystemExit('registry manifest digest mismatch')

source_reviews=[]; question_reviews=[]
for field,target,review_schema in [
    ('source_review_shards',source_reviews,'chemistry-source-integrity-review.schema.json'),
    ('question_review_shards',question_reviews,'chemistry-assessment-item-review.schema.json'),
]:
    for ref in manifest[field]:
        shard=load(D/'registry'/ref['path'])
        validate('chemistry-review-shard.schema.json',shard)
        if shard['shard_digest'] != digest_without(shard,'shard_digest') or shard['shard_digest'] != ref['shard_digest']:
            raise SystemExit(f"review shard digest mismatch: {ref['path']}")
        if len(shard['reviews']) != ref['record_count']:
            raise SystemExit(f"review shard count mismatch: {ref['path']}")
        for record in shard['reviews']:
            validate(review_schema, record)
        target.extend(shard['reviews'])

expanded={k:manifest[k] for k in ['registry_id','schema_version','subject','source_set_ref','question_set_ref','review_policy_version','qc_registry_ref']}
expanded['source_reviews']=source_reviews; expanded['question_reviews']=question_reviews; expanded['registry_digest']=manifest['expanded_registry_digest']
if expanded['registry_digest'] != digest_without(expanded,'registry_digest'):
    raise SystemExit('expanded registry digest mismatch')

for event in qc['events']:
    validate('chemistry-qc-event.schema.json', event)

required_case_types = {'CLEAN','SOURCE_INTERNAL_TYPO','FORMULA_OR_CHARGE_OCR_AMBIGUITY','UNDERDETERMINED','CONDITION_SENSITIVE','MISSING_STRUCTURE_OR_FIGURE','EXTERNAL_CLEAN'}
actual = {x['case_type'] for x in cases['cases']}
if actual != required_case_types:
    raise SystemExit(f'pilot case coverage mismatch: {sorted(actual)}')

print('CHEMISTRY C-B contract/schema validation = PASS')
print(f'source review records = {len(source_reviews)}')
print(f'question/subpart review records = {len(question_reviews)}')
print(f'pilot case classes = {len(cases["cases"])}')
