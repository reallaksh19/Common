#!/usr/bin/env python3
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'engine'))
from core1b_runtime import Core1BRuntimeError,build_release_receipt,derive_state,validate_registry,validate_unit
load=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
G=ROOT/'golden'/'moving-launcher'; REG=load(ROOT/'registry'/'moving-launcher-atoms-v1.json'); AUTH=load(G/'core1a-authority.json'); UNIT=load(G/'core1b-unit.json'); EVENTS=load(G/'observed-events.json')
def validator(name):
    s=load(ROOT/'contracts'/name); Draft202012Validator.check_schema(s); return Draft202012Validator(s)
validator('physics-core1b-authority-release.schema.json').validate(AUTH)
validator('physics-core1b-unit.schema.json').validate(UNIT)
validate_registry(REG); validate_unit(UNIT,REG,AUTH,EVENTS)
assert AUTH['provenance_class']=='PROCESS_GOLDEN' and AUTH['bucket_id']=='M2D-SBA-23'
assert derive_state(UNIT,AUTH,EVENTS)=='NOT_EXPOSED'
try:
    build_release_receipt(UNIT,REG,AUTH,EVENTS)
except Core1BRuntimeError as e:
    assert str(e)=='CORE1B_OBSERVED_INDEPENDENT_EVIDENCE_REQUIRED'
else:
    raise AssertionError('process golden with no observed learner evidence must not issue a Core1B release receipt')
print('Core1B moving-launcher process golden: PASS (authority digest bound; learner state remains NOT_EXPOSED)')
