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
    candidate,review=audit(out/'exact-product-candidate.json',out/'core-study-guide.pdf',out/'examside-solution-transfer-book.pdf',out/'ai-pre-review.json',out/'physical-page-map-core1.json',out/'physical-page-map-core2.json',policy)
    assert review['state']=='PASS',review
    assert candidate['machine_evidence']['macro_particle_symbolic_realized']
    assert review['findings']==[]
    # An AI pre-review may never stand in for a human gate.
    assert review['reviewer_role']=='AI_PRE_REVIEW' and review['production_claim'] is False
    assert set(review['not_established_by_this_review'])>={'SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN','VISUAL_USABILITY','MATURE_DESIGN_QUALITY'}
    assert len(review['evidence']['realized_primitive_kinds'])>=policy['minimum_realized_primitive_kinds'],review['evidence']
    gate=machine_validate(candidate,cold,policy,out,candidate['source_qc_event_refs'])
    assert gate['status']=='PASS',gate
    rc={'comparator_id':policy['reference_comparator_id'],'state':'NOT_RUN','run_after_human_gates':False,'raw_reference_used_as_runtime_input':False}
    decision=build_release_decision(candidate,gate,[review],rc,policy)
    assert decision['classification']==policy['blocked_classification'] and decision['exit_code']==2
    validate_release_decision(decision,candidate,[review],policy)
print('CHEMISTRY C-L AI pre-review = PASS for remediated exact candidate')
print('Realized teaching-primitive kinds =',len(review['evidence']['realized_primitive_kinds']))
print('Machine publication engineering remains PASS; mature release remains BLOCKED/2 pending authorized reviews')
