#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
REPO = CHEM.parents[2]
sys.path.insert(0, str(D / 'engine'))
from validate_chemistry_generation_contract import (
    validate_contract, validate_execution, cold_start_gate, load_contract, digest)


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e)); return
    raise AssertionError('expected ' + code)


contract = load_contract(CHEM / 'GENERATION_CONTRACT.json')
Draft202012Validator(load(D / 'contracts' / 'chemistry-generation-contract.schema.json')).validate(contract)
validate_contract(contract, REPO)
assert cold_start_gate(REPO)['contract_id'] == contract['contract_id']

REQUIRED = list(contract['required_phase_order'])
assert REQUIRED == [
    'SOURCE_INGESTION', 'SOURCE_SCOPE_CLASSIFICATION', 'CAPABILITY_DERIVATION', 'CORE1_STUDY_MODEL',
    'INSTRUCTIONAL_AUTHORING', 'PROBLEM_AUTHORING', 'PCK_BINDING', 'VISUAL_OBLIGATION_BINDING',
    'CORE2_PRIMARY_OWNERSHIP', 'REALIZATION', 'VISUAL_AND_LEGIBILITY_PREFLIGHT', 'COVERAGE_CLOSURE',
    'CUSTODY_FREEZE']

full_log = [{'phase_id': p, 'executed': True} for p in REQUIRED]
assert validate_execution(contract, full_log, REPO)

# ---- structural falsifiers -------------------------------------------------
bad = copy.deepcopy(contract); bad['phases'] = bad['phases'][:-1]; bad['contract_digest'] = ''
expect('REQUIRED_PHASE_MISSING', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract)
bad['phases'][4], bad['phases'][5] = bad['phases'][5], bad['phases'][4]
bad['contract_digest'] = ''
expect('PHASE_ORDER_VIOLATION', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract)
bad['phases'][3]['depends_on'] = ['REALIZATION']; bad['contract_digest'] = ''
expect('PHASE_ORDER_VIOLATION', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract)
bad['phases'][7]['required_registry_paths'].append('Grade 9/V2/Chemistry/Representation/registry/does-not-exist.json')
bad['contract_digest'] = ''
expect('REQUIRED_REGISTRY_MISSING', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract)
bad['phases'][9]['required_engine_paths'].append('Grade 9/V2/Chemistry/ExactProduct/engine/does-not-exist.py')
bad['contract_digest'] = ''
expect('REQUIRED_ENGINE_MISSING', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract); bad['contract_digest'] = '0' * 64
expect('GENERATION_CONTRACT_DIGEST_DRIFT', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract); bad['human_gate_states']['PEDAGOGICAL_DESIGN'] = 'MACHINE_MOVABLE'
bad['contract_digest'] = ''
expect('PHASE_ORDER_VIOLATION', lambda: validate_contract(bad, REPO))

bad = copy.deepcopy(contract); bad['renderer_selection_forbidden'] = False; bad['contract_digest'] = ''
expect('PHASE_ORDER_VIOLATION', lambda: validate_contract(bad, REPO))

# ---- execution falsifiers --------------------------------------------------
expect('PHASE_NOT_EXECUTED', lambda: validate_execution(contract, full_log[:-1], REPO))

log = copy.deepcopy(full_log); log[6]['executed'] = False
expect('PHASE_NOT_EXECUTED', lambda: validate_execution(contract, log, REPO))

# A cold start that jumps straight to realization must be refused, not warned.
log = [{'phase_id': 'SOURCE_INGESTION', 'executed': True}, {'phase_id': 'REALIZATION', 'executed': True}]
expect('UPSTREAM_PHASE_UNEXECUTED', lambda: validate_execution(contract, log, REPO))

log = copy.deepcopy(full_log); log[3], log[4] = log[4], log[3]
expect('UPSTREAM_PHASE_UNEXECUTED', lambda: validate_execution(contract, log, REPO))

log = copy.deepcopy(full_log) + [{'phase_id': 'FREESTYLE_EXTRA_PHASE', 'executed': True}]
expect('UNDECLARED_PHASE_EXECUTED', lambda: validate_execution(contract, log, REPO))

log = copy.deepcopy(full_log) + [{'phase_id': 'REALIZATION', 'executed': True}]
expect('PHASE_EXECUTED_OUT_OF_ORDER', lambda: validate_execution(contract, log, REPO))

# ---- the contract really does gate a missing upstream contract -------------
expect('REQUIRED_REGISTRY_MISSING', lambda: cold_start_gate(REPO / 'no-such-checkout'))

# Determinism: the sealed digest is reproducible from the contract body.
assert contract['contract_digest'] == digest(contract, 'contract_digest')

print('CHEMISTRY GENERATION CONTRACT required falsifiers = 9 PASS')
print('CHEMISTRY GENERATION CONTRACT declared phases = %d PASS' % len(REQUIRED))
print('CHEMISTRY GENERATION CONTRACT cold-start refusal on missing upstream contract = PASS')
print('CHEMISTRY GENERATION CONTRACT execution-order gate = PASS')
