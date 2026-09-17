#!/usr/bin/env python3
"""Fail-closed guard: reference bytes are unreadable until all governed human gates pass."""
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]
HUMAN=('SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN','VISUAL_USABILITY')
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(o): return hashlib.sha256(canonical(o)).hexdigest()
def check_schema(name,obj): Draft202012Validator(load(ROOT/'contracts'/name)).validate(obj)

def check(binding,intake,mode,reference_record=None):
    reasons=[]; q=intake.get('quality_review_summary',{}).get('quality_states',{})
    if intake.get('candidate_sha256')!=binding.get('artifact_sha256'): reasons.append('CANDIDATE_SHA_MISMATCH')
    if sorted(intake.get('candidate_artifact_sha256_refs') or [])!=sorted(binding.get('artifact_sha256_refs') or []): reasons.append('ARTIFACT_SET_MISMATCH')
    if q.get('PUBLICATION_ENGINEERING')!='PASS': reasons.append('PUBLICATION_ENGINEERING_NOT_PASS')
    for state in HUMAN:
        if q.get(state)!='PASS': reasons.append(state+'_NOT_PASS')
    if intake.get('intake_status')!='READY' or intake.get('rejected_submissions'): reasons.append('HUMAN_REVIEW_INTAKE_NOT_CLEAN')
    if mode=='REAL_RELEASE':
        if intake.get('mode')!='REAL_RELEASE' or intake.get('fixture_class')!='REAL' or not intake.get('release_evidence_eligible'): reasons.append('REAL_HUMAN_REVIEW_EVIDENCE_NOT_ELIGIBLE')
    else:
        if intake.get('mode')!='TEST_ONLY' or intake.get('fixture_class')!='TEST_ONLY_SYNTHETIC': reasons.append('TEST_HUMAN_REVIEW_CUSTODY_INVALID')
    status='READY_FOR_REFERENCE_COMPARISON' if not reasons else 'BLOCKED_HUMAN_QUALITY_GATES'
    read=False
    if status=='READY_FOR_REFERENCE_COMPARISON' and reference_record:
        Path(reference_record).read_bytes(); read=True
    result={'eligibility_id':'PHY-P-L-REFERENCE-ELIGIBILITY-'+mode,'schema_version':'1.0.0','subject':'PHYSICS','candidate_sha256':binding['artifact_sha256'],'artifact_sha256_refs':sorted(binding['artifact_sha256_refs']),'mode':mode,'status':status,'blocking_reasons':sorted(set(reasons)),'reference_read_attempted':read,'release_evidence_eligible':bool(status=='READY_FOR_REFERENCE_COMPARISON' and mode=='REAL_RELEASE' and intake.get('release_evidence_eligible')),'input_digest':''}
    result['input_digest']=sha({'binding':binding,'intake':intake,'mode':mode})
    check_schema('physics-reference-eligibility.schema.json',result); return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--binding',required=True); ap.add_argument('--human-review-intake',required=True); ap.add_argument('--mode',choices=['REAL_RELEASE','TEST_ONLY'],required=True); ap.add_argument('--reference-record'); ap.add_argument('--out'); a=ap.parse_args()
    r=check(load(a.binding),load(a.human_review_intake),a.mode,a.reference_record); text=json.dumps(r,indent=2,sort_keys=True)+'\n'; Path(a.out).write_text(text) if a.out else print(text,end='')
if __name__=='__main__': main()
