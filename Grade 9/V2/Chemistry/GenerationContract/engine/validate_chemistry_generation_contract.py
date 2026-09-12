#!/usr/bin/env python3
"""Chemistry V2 generation-contract orchestration gate.

`GENERATION_CONTRACT.json` is the single machine-readable entry point for a
cold-start Chemistry producer. Before this existed, an agent had to *discover*
its upstream obligations by repository archaeology, which is exactly how a
compliant renderer ends up producing a semantically correct but instructionally
thin page: the page-level contracts were checkable, the orchestration was not.

Two independent gates live here.

``validate_contract``
    Structural: the declared phases are exactly the required order, dependencies
    only ever point backwards, and every declared registry/engine path really
    exists in the repository. This is what makes a *cold start* refuse to
    proceed — a missing upstream contract is a hard failure, not a warning.

``validate_execution``
    Runtime: an execution log must cover every declared phase, in declared
    order, with no phase running before one of its dependencies and no
    undeclared phase appearing at all.

Both are fail-closed and raise the falsifier code named in the contract's own
``contract_falsifiers`` list.
"""
import argparse, copy, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve()
CHEM = HERE.parents[2]
REPO = HERE.parents[5]
CONTRACT_PATH = CHEM / 'GENERATION_CONTRACT.json'


def canonical(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field: x.pop(field, None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))


def fail(code, detail=''): raise ValueError(f'{code}: {detail}' if detail else code)


def load_contract(path=CONTRACT_PATH): return load(path)


def validate_contract(contract, repo_root=REPO, check_paths=True):
    """Structural gate. Returns the phase index keyed by phase_id."""
    if contract.get('subject') != 'CHEMISTRY': fail('REQUIRED_PHASE_MISSING', 'subject')
    stored = contract.get('contract_digest', '')
    if stored and stored != digest(contract, 'contract_digest'):
        fail('GENERATION_CONTRACT_DIGEST_DRIFT', contract.get('contract_id', 'contract'))
    required = list(contract['required_phase_order'])
    phases = contract['phases']
    by = {p['phase_id']: p for p in phases}
    if len(by) != len(phases): fail('REQUIRED_PHASE_MISSING', 'duplicate phase id')
    if [p['phase_id'] for p in phases] != required:
        missing = [x for x in required if x not in by]
        if missing: fail('REQUIRED_PHASE_MISSING', ', '.join(missing))
        fail('PHASE_ORDER_VIOLATION', 'declared phases are not in required_phase_order')
    seen = []
    for index, phase in enumerate(phases, 1):
        pid = phase['phase_id']
        if phase['ordinal'] != index: fail('PHASE_ORDER_VIOLATION', pid + ':ordinal')
        for dep in phase['depends_on']:
            if dep not in by: fail('REQUIRED_PHASE_MISSING', pid + ' depends on ' + dep)
            if dep not in seen: fail('PHASE_ORDER_VIOLATION', pid + ' depends on later phase ' + dep)
        if index > 1 and not phase['depends_on']:
            fail('PHASE_ORDER_VIOLATION', pid + ':no declared dependency')
        if not phase.get('obligation'): fail('REQUIRED_PHASE_MISSING', pid + ':obligation')
        if not phase.get('produces'): fail('REQUIRED_PHASE_MISSING', pid + ':produces')
        if not phase.get('falsifiers'): fail('REQUIRED_PHASE_MISSING', pid + ':falsifiers')
        if check_paths:
            root = Path(repo_root)
            for rel in phase.get('required_registry_paths', []):
                if not (root / rel).exists(): fail('REQUIRED_REGISTRY_MISSING', pid + ':' + rel)
            for rel in phase.get('required_engine_paths', []):
                if not (root / rel).exists(): fail('REQUIRED_ENGINE_MISSING', pid + ':' + rel)
        seen.append(pid)
    if check_paths:
        root = Path(repo_root)
        for key in ('entrypoint_md', 'authority_manifest', 'legacy_entrypoint'):
            rel = contract.get(key)
            if rel and not (root / rel).exists(): fail('REQUIRED_REGISTRY_MISSING', key + ':' + rel)
    if contract.get('renderer_invention_allowed') is not False: fail('PHASE_ORDER_VIOLATION', 'renderer_invention_allowed')
    if contract.get('renderer_selection_forbidden') is not True: fail('PHASE_ORDER_VIOLATION', 'renderer_selection_forbidden')
    for state, rule in contract['human_gate_states'].items():
        if state != 'PUBLICATION_ENGINEERING' and rule != 'PENDING_AUTHORIZED_HUMAN_ONLY':
            fail('PHASE_ORDER_VIOLATION', 'human gate ' + state)
    return by


def validate_execution(contract, execution_log, repo_root=REPO, check_paths=True):
    """Runtime gate over an ordered execution log.

    ``execution_log`` is a list of ``{'phase_id': ..., 'executed': bool, ...}``
    records in the order the producer actually ran them.
    """
    by = validate_contract(contract, repo_root, check_paths)
    required = list(contract['required_phase_order'])
    records = list(execution_log or [])
    ran = {}
    for position, record in enumerate(records):
        pid = record.get('phase_id')
        if pid not in by: fail('UNDECLARED_PHASE_EXECUTED', str(pid))
        if pid in ran: fail('PHASE_EXECUTED_OUT_OF_ORDER', pid + ':executed twice')
        if not record.get('executed'): fail('PHASE_NOT_EXECUTED', pid)
        for dep in by[pid]['depends_on']:
            if dep not in ran: fail('UPSTREAM_PHASE_UNEXECUTED', pid + ' before ' + dep)
        ran[pid] = position
    missing = [x for x in required if x not in ran]
    if missing: fail('PHASE_NOT_EXECUTED', ', '.join(missing))
    order = [x for x in records if x['phase_id'] in set(required)]
    if [x['phase_id'] for x in order] != required: fail('PHASE_EXECUTED_OUT_OF_ORDER', 'execution order')
    return True


def cold_start_gate(repo_root=REPO, contract_path=CONTRACT_PATH):
    """Refuse a cold start when any required upstream contract is missing.

    Returns the contract when the repository satisfies it; raises the specific
    falsifier otherwise. A producer calls this *first*, before reading any
    source PDF.
    """
    contract = load_contract(contract_path)
    validate_contract(contract, repo_root, check_paths=True)
    return contract


def seal(contract_path=CONTRACT_PATH):
    contract = load(contract_path)
    contract['contract_digest'] = ''
    contract['contract_digest'] = digest(contract, 'contract_digest')
    Path(contract_path).write_text(json.dumps(contract, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return contract['contract_digest']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--contract', default=str(CONTRACT_PATH))
    ap.add_argument('--repo-root', default=str(REPO))
    ap.add_argument('--execution-log')
    ap.add_argument('--seal', action='store_true')
    a = ap.parse_args()
    if a.seal:
        print(json.dumps({'contract_digest': seal(a.contract)}, sort_keys=True)); return
    contract = load(a.contract)
    validate_contract(contract, a.repo_root)
    if a.execution_log:
        log = load(a.execution_log)
        validate_execution(contract, log.get('phases', log), a.repo_root)
    print(json.dumps({'contract_id': contract['contract_id'],
                      'contract_digest': contract['contract_digest'],
                      'phases': len(contract['phases']),
                      'status': 'PASS'}, sort_keys=True))


if __name__ == '__main__': main()
