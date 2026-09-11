#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parent
data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
schemas={n:json.loads((D/n).read_text(encoding='utf-8')) for n in ['chemistry-reasoning-route.schema.json','chemistry-condition-validity-binding.schema.json','chemistry-verification-route.schema.json','chemistry-demand-vector.schema.json']}
for group in ('source_semantics','question_semantics'):
    for r in data[group]:
        Draft202012Validator(schemas['chemistry-reasoning-route.schema.json']).validate(r['reasoning_route'])
        Draft202012Validator(schemas['chemistry-condition-validity-binding.schema.json']).validate(r['condition_validity'])
        Draft202012Validator(schemas['chemistry-verification-route.schema.json']).validate(r['verification_route'])
        Draft202012Validator(schemas['chemistry-demand-vector.schema.json']).validate(r['demand_vector'])
assert data['summary']['reasoning_route_is_hint_independent'] is True
assert data['summary']['difficulty_scalar_is_not_authority'] is True
print('CHEMISTRY C-D generated semantics = PASS')
