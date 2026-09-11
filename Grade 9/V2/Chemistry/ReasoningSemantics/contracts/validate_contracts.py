#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parent; R=D.parent/'registry'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
family_schema=load(D/'chemistry-problem-family.schema.json')
registry=load(R/'chemistry-problem-family-registry.json')
for family in registry['families']: Draft202012Validator(family_schema).validate(family)
Draft202012Validator(load(D/'chemistry-reasoning-role-registry.schema.json')).validate(load(R/'chemistry-reasoning-role-registry.json'))
Draft202012Validator(load(D/'chemistry-guide-demand-badge-policy.schema.json')).validate(load(R/'chemistry-guide-demand-badge-policy.json'))
assert len(registry['families'])>=12
print('CHEMISTRY C-D contract registries = PASS')
