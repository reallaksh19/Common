#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'engine'))
from check_eligibility import check_eligibility
from compare_synthetic import build_result, validate_reference

def load(n): return json.loads((ROOT/'fixtures'/n).read_text())
current=load('current_candidate_binding.json'); pending=load('quality_review_summary.pending.json')
tb=load('candidate_binding.test-only.json'); ts=load('quality_review_summary.test-only-pass.json'); ref=load('synthetic_reference.test-only.json'); rubric=load('validation_rubric.json')
e=check_eligibility(current,pending)
assert e['status']=='BLOCKED_HUMAN_QUALITY_GATES' and e['reference_read_attempted'] is False and e['release_evidence_eligible'] is False
assert {'SUBJECT_CORRECTNESS_NOT_PASS','PEDAGOGY_USABILITY_NOT_PASS','VISUAL_USABILITY_NOT_PASS'} <= set(e['blocking_reasons'])
p=copy.deepcopy(pending); p['ai_pre_review_status']='LOTS_OF_AI_EVIDENCE'; assert check_eligibility(current,p)['status']=='BLOCKED_HUMAN_QUALITY_GATES'
p=copy.deepcopy(pending); p['revised_artifact_sha256']='f'*64; assert 'CANDIDATE_SHA_MISMATCH' in check_eligibility(current,p)['blocking_reasons']
s=copy.deepcopy(ts); s['quality_review_summary']['unresolved_major_count']=1; assert check_eligibility(tb,s)['status']=='BLOCKED_HUMAN_QUALITY_GATES'
e2=check_eligibility(tb,ts); assert e2['status']=='READY_FOR_REFERENCE_SELECTION' and e2['test_only'] and not e2['release_evidence_eligible']
r=build_result(tb,ts,ref,rubric); assert r['status']=='VALIDATION_GAP' and r['test_only'] and not r['release_evidence_eligible'] and r['real_benchmark_comparison']=='NOT_RUN'
assert r['validation_gaps'] and r['validation_gaps'][0]['required_action']=='REVISION_CYCLE' and r['upstream_mutation'] is False
def reject(mut):
    x=copy.deepcopy(ref); mut(x)
    try: validate_reference(x); raise AssertionError('invalid reference accepted')
    except ValueError: pass
reject(lambda x:x.__setitem__('producer_input',True))
reject(lambda x:x.__setitem__('allowed_use','PRODUCER_INPUT'))
reject(lambda x:x.__setitem__('source_pr',157))
a,b,c,d=copy.deepcopy(tb),copy.deepcopy(ts),copy.deepcopy(ref),copy.deepcopy(rubric); build_result(a,b,c,d); assert a==tb and b==ts and c==ref and d==rubric
r2=build_result(tb,ts,ref,rubric); assert json.dumps(r,sort_keys=True,separators=(',',':'))==json.dumps(r2,sort_keys=True,separators=(',',':'))
assert 'VISUAL_COMPOSITION' in r['validation_gaps'][0]['dimensions']
print('MATH-V2-07 validation-gate falsifiers = 12 PASS')
