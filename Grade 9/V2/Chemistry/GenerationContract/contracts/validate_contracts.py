#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
sys.path.insert(0, str(D / 'engine'))
from validate_chemistry_generation_contract import validate_contract, load_contract

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

schema = load(D / 'contracts' / 'chemistry-generation-contract.schema.json')
Draft202012Validator.check_schema(schema)
contract = load_contract(CHEM / 'GENERATION_CONTRACT.json')
Draft202012Validator(schema).validate(contract)
validate_contract(contract, CHEM.parents[2])

md = (CHEM / 'GENERATION_CONTRACT.md').read_text(encoding='utf-8')
for phase in contract['required_phase_order']:
    assert phase in md, phase

print('CHEMISTRY GENERATION CONTRACT schema = PASS')
print('CHEMISTRY GENERATION CONTRACT phase order = PASS (%d phases)' % len(contract['phases']))
print('CHEMISTRY GENERATION CONTRACT required upstream paths present = PASS')
print('CHEMISTRY GENERATION CONTRACT human gates remain PENDING-only = PASS')
