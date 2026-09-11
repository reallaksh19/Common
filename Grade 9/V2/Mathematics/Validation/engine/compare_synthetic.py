#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path
from check_eligibility import check_eligibility

FORBIDDEN_UPSTREAM_KEYS={'canonical_registry','learner_state','learner_state_snapshot','learner_study_model','learning_design_plan','canonical_mutation','diagnosis_update'}

def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def walk_keys(o):
    if isinstance(o,dict):
        for k,v in o.items(): yield k; yield from walk_keys(v)
    elif isinstance(o,list):
        for v in o: yield from walk_keys(v)

def validate_reference(ref):
    if ref.get('subject')!='MATHEMATICS': raise ValueError('non-Math reference rejected')
    if ref.get('allowed_use')!='COMPARATIVE_VALIDATION_ONLY': raise ValueError('reference use boundary violation')
    if ref.get('producer_input') is not False: raise ValueError('producer-input reference rejected')
    if ref.get('source_pr')==157: raise ValueError('PR #157 is Chemistry and cannot be a Math reference')
    cls=ref.get('reference_class')
    if cls=='TEST_ONLY_SYNTHETIC_REFERENCE':
        if ref.get('freeze_review_status')!='TEST_ONLY' or ref.get('release_evidence_eligible') is not False: raise ValueError('invalid test-only reference')
    elif cls=='FROZEN_MATURE_MATH_REFERENCE':
        if ref.get('freeze_review_status')!='APPROVED_FOR_COMPARATIVE_VALIDATION' or ref.get('release_evidence_eligible') is not True: raise ValueError('mature reference not explicitly frozen')
    else: raise ValueError('unknown reference class')
    if FORBIDDEN_UPSTREAM_KEYS.intersection(set(walk_keys(ref))): raise ValueError('reference contains upstream mutation contract')

def build_result(binding,summary_obj,reference,rubric):
    binding_before=copy.deepcopy(binding); summary_before=copy.deepcopy(summary_obj); ref_before=copy.deepcopy(reference); rubric_before=copy.deepcopy(rubric)
    elig=check_eligibility(binding,summary_obj)
    if elig['status']!='READY_FOR_REFERENCE_SELECTION':
        base={
          'schema_version':'1.0.0','validation_id':'MATH-V2-07-CURRENT-BLOCKED','status':'BLOCKED','candidate_sha256':binding['artifact_sha256'],
          'reference_read_attempted':False,'reference_ids':[],'reference_sha256s':[],'dimension_results':[], 'validation_gaps':[],
          'test_only':elig['test_only'],'release_evidence_eligible':False,'upstream_mutation':False,'real_benchmark_comparison':'NOT_RUN'
        }
        base['result_digest']=sha_obj(base)
        return base
    validate_reference(reference)
    dimensions=rubric['dimensions']; outcomes=reference.get('synthetic_dimension_outcomes',{})
    results=[]; gap_dims=[]
    for d in dimensions:
        status=outcomes.get(d,'NOT_EVALUATED')
        if status=='GAP': gap_dims.append(d)
        results.append({'dimension':d,'status':status,'evidence':f"Test-only comparator outcome for {d}: {status}."})
    test_only=elig['test_only'] or reference['reference_class']=='TEST_ONLY_SYNTHETIC_REFERENCE'
    gaps=[]
    if gap_dims:
        gaps=[{'gap_id':'MATH-V2-07-TEST-GAP-001','candidate_sha256':binding['artifact_sha256'],'reference_sha256':reference['artifact_sha256'],'dimensions':gap_dims,'findings':[f'{d} below synthetic comparison expectation' for d in gap_dims],'required_action':'REVISION_CYCLE','upstream_mutation':False}]
    status='VALIDATION_GAP' if gaps else 'PASS'
    base={
      'schema_version':'1.0.0','validation_id':'MATH-V2-07-TEST-ONLY-COMPARISON','status':status,'candidate_sha256':binding['artifact_sha256'],
      'reference_read_attempted':True,'reference_ids':[reference['reference_id']],'reference_sha256s':[reference['artifact_sha256']],
      'dimension_results':results,'validation_gaps':gaps,'test_only':test_only,'release_evidence_eligible':(not test_only and status=='PASS'),
      'upstream_mutation':False,'real_benchmark_comparison':'NOT_RUN' if test_only else 'RUN'
    }
    base['result_digest']=sha_obj(base)
    if binding!=binding_before or summary_obj!=summary_before or reference!=ref_before or rubric!=rubric_before: raise ValueError('comparator mutated input/upstream state')
    return base

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binding',required=True); ap.add_argument('--quality-summary',required=True); ap.add_argument('--reference',required=True); ap.add_argument('--rubric',required=True); ap.add_argument('--out'); a=ap.parse_args()
    result=build_result(load(a.binding),load(a.quality_summary),load(a.reference),load(a.rubric))
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.out: Path(a.out).write_text(text)
    else: print(text,end='')
if __name__=='__main__': main()
