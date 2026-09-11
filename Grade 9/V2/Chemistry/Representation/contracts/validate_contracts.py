#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
ENG=D/'engine'
sys.path.insert(0,str(ENG))
from build_chemistry_representations import validate_registry, validate_notation

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

schema=load(D/'contracts'/'chemistry-representation-spec.schema.json')
Draft202012Validator.check_schema(schema)
registry=load(D/'registry'/'chemistry-teaching-primitive-registry.json')
profile=load(D/'registry'/'chemistry-page-intent-profile.json')
notation=load(D/'registry'/'chemistry-notation-render-contract.json')
by=validate_registry(registry); validate_notation(notation)
required=set(registry['required_primitive_ids'])
assert required<=set(by)
assert profile['subject']=='CHEMISTRY' and notation['subject']=='CHEMISTRY'
assert set(profile['conditional_primitives'].values())<=set(by)
for cap,pids in profile['primary_primitives_by_capability'].items():
    assert pids, cap
    for pid in pids:
        assert pid in by,(cap,pid)
        assert cap in by[pid]['capability_refs'],(cap,pid)
print('CHEMISTRY C-H representation schema = PASS')
print('CHEMISTRY C-H primitive registry = PASS')
print('CHEMISTRY C-H page-intent profile = PASS')
print('CHEMISTRY C-H notation contract = PASS')
