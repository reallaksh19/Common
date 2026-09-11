#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

REQUIRED_QUALITY={
    'PUBLICATION_ENGINEERING':'PASS',
    'SUBJECT_CORRECTNESS':'PASS',
    'PEDAGOGY_USABILITY':'PASS',
    'VISUAL_USABILITY':'PASS',
    'BENCHMARK_COMPARATIVE_VALIDATION':'NOT_RUN'
}

def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def load(p): return json.loads(Path(p).read_text())

def unwrap_summary(obj):
    test_only=obj.get('fixture_class')=='TEST_ONLY_SYNTHETIC'
    return obj.get('quality_review_summary',obj),test_only

def check_eligibility(binding,summary_obj):
    summary,test_only=unwrap_summary(summary_obj)
    reasons=[]
    candidate_sha=binding['artifact_sha256']
    if binding.get('publication_engineering')!='PASS': reasons.append('CANDIDATE_ENGINEERING_NOT_PASS')
    if summary.get('revised_artifact_sha256')!=candidate_sha: reasons.append('CANDIDATE_SHA_MISMATCH')
    q=summary.get('quality_states',{})
    for key,expected in REQUIRED_QUALITY.items():
        if q.get(key)!=expected: reasons.append(f'{key}_NOT_{expected}')
    evidence=summary.get('human_review_evidence',{})
    for key in ('SUBJECT','PEDAGOGY','VISUAL'):
        if evidence.get(key,0)<1: reasons.append(f'HUMAN_{key}_EVIDENCE_MISSING')
    if summary.get('unresolved_major_count',0)>0: reasons.append('BLOCKING_REVIEW_FINDINGS_REMAIN')
    binding_test=binding.get('binding_class')=='TEST_ONLY_SYNTHETIC_BINDING'
    test_only=test_only or binding_test
    if test_only and binding.get('release_evidence_eligible',True): reasons.append('TEST_ONLY_BINDING_MARKED_RELEASE_ELIGIBLE')
    status='READY_FOR_REFERENCE_SELECTION' if not reasons else 'BLOCKED_HUMAN_QUALITY_GATES'
    payload={'binding':binding,'summary':summary_obj}
    return {
      'schema_version':'1.0.0',
      'eligibility_id':'MATH-V2-07-ELIGIBILITY-TEST' if test_only else 'MATH-V2-07-ELIGIBILITY-CURRENT',
      'candidate_sha256':candidate_sha,
      'status':status,
      'blocking_reasons':sorted(set(reasons)),
      'reference_read_attempted':False,
      'test_only':test_only,
      'release_evidence_eligible':(status=='READY_FOR_REFERENCE_SELECTION' and not test_only and binding.get('release_evidence_eligible') is True),
      'input_digest':sha_obj(payload)
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binding',required=True); ap.add_argument('--quality-summary',required=True); ap.add_argument('--reference-registry'); ap.add_argument('--out'); a=ap.parse_args()
    result=check_eligibility(load(a.binding),load(a.quality_summary))
    # Critical ordering proof: a blocked gate returns before touching reference-registry.
    if result['status']=='READY_FOR_REFERENCE_SELECTION' and a.reference_registry:
        Path(a.reference_registry).read_bytes()
        result['reference_read_attempted']=True
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.out: Path(a.out).write_text(text)
    else: print(text,end='')
if __name__=='__main__': main()
