#!/usr/bin/env python3
import json, sys, tempfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]; REPO=D.parents[3]
sys.path[:0]=[str(D/'engine')]
from realize_chemistry_exact_product import realization
from audit_chemistry_exact_candidate import audit
from evaluate_chemistry_exact_product import machine_validate,build_release_decision,validate_release_decision

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
policy=load(D/'registry'/'chemistry-exact-product-quality-policy.json')
with tempfile.TemporaryDirectory() as td:
    out=Path(td); candidate,cold=realization(REPO,out)
    candidate,review=audit(out/'exact-product-candidate.json',out/'core-study-guide.pdf',out/'examside-solution-transfer-book.pdf',out/'ai-pre-review.json')
    assert review['state']=='FAIL'
    assert not candidate['machine_evidence']['macro_particle_symbolic_realized']
    assert any('MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED' in x for x in review['findings'])
    assert any('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK' in x for x in review['findings'])
    gate=machine_validate(candidate,cold,policy,out,candidate['source_qc_event_refs'])
    assert gate['status']=='PASS',gate
    rc={'comparator_id':policy['reference_comparator_id'],'state':'NOT_RUN','run_after_human_gates':False,'raw_reference_used_as_runtime_input':False}
    decision=build_release_decision(candidate,gate,[review],rc,policy)
    assert decision['classification']==policy['blocked_classification'] and decision['exit_code']==2
    validate_release_decision(decision,candidate,[review],policy)
print('CHEMISTRY C-L AI pre-review = FAIL as expected for current exact candidate')
print('Machine publication engineering remains PASS; mature release remains BLOCKED/2')
