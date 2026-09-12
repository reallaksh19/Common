#!/usr/bin/env python3
import json, sys, tempfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]; REPO=D.parents[3]
sys.path[:0]=[str(D/'engine')]
from realize_chemistry_exact_product import realization
from evaluate_chemistry_exact_product import machine_validate,build_release_decision,validate_release_decision

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
policy=load(D/'registry'/'chemistry-exact-product-quality-policy.json')
with tempfile.TemporaryDirectory() as td:
    out=Path(td); candidate,cold=realization(REPO,out)
    assert (out/'core-study-guide.pdf').exists() and (out/'examside-solution-transfer-book.pdf').exists()
    assert (out/'core-study-guide.pdf').read_bytes().startswith(b'%PDF')
    assert (out/'examside-solution-transfer-book.pdf').read_bytes().startswith(b'%PDF')
    gate=machine_validate(candidate,cold,policy,out,candidate['source_qc_event_refs'])
    assert gate['status']=='PASS',gate
    rc={'comparator_id':policy['reference_comparator_id'],'state':'NOT_RUN','run_after_human_gates':False,'raw_reference_used_as_runtime_input':False}
    decision=build_release_decision(candidate,gate,[],rc,policy)
    assert decision['classification']==policy['blocked_classification']
    assert decision['exit_code']==2
    validate_release_decision(decision,candidate,[],policy)
    e=candidate['machine_evidence']
    assert e['formula_typography_pass']
    assert e['macro_particle_symbolic_realized']
    assert e['learner_internal_identifier_leaks']==0
    assert e['actual_placement_evidence'] and e['placement_bounds_violations']==0 and e['orphan_continuations']==0
    assert len(e['teaching_primitive_kinds_realized'])>=policy['minimum_realized_primitive_kinds'],e
    print('Realized teaching primitives =',e['teaching_primitives_drawn'],'across',len(e['teaching_primitive_kinds_realized']),'kinds')
    print('CHEMISTRY C-L exact PDF realization = PASS')
    print('Core1 pages =',candidate['artifacts'][0]['page_count'])
    print('Core2 pages =',candidate['artifacts'][1]['page_count'])
    print('Production mature release = BLOCKED/2 pending authorized reviews')
