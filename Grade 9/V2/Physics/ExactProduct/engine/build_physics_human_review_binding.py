#!/usr/bin/env python3
"""Build the Shared HumanReview candidate binding from exact Physics P-L evidence only."""
import argparse, hashlib, json
from pathlib import Path


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()

def build_binding(candidate, ai_review):
    if candidate.get('subject')!='PHYSICS': raise ValueError('PHYSICS_CANDIDATE_REQUIRED')
    refs=sorted(p['artifact_sha256'] for p in candidate.get('products',[]))
    if len(refs)!=2 or len(set(refs))!=2: raise ValueError('EXACT_TWO_ARTIFACT_SET_REQUIRED')
    if sorted(ai_review.get('artifact_sha256_refs') or [])!=refs: raise ValueError('AI_PRE_REVIEW_ARTIFACT_SET_MISMATCH')
    if ai_review.get('authority')!='ADVISORY_ONLY' or ai_review.get('sets_quality_states') is not False:
        raise ValueError('AI_PRE_REVIEW_AUTHORITY_INVALID')
    artifact_set_digest=sha_obj(refs)
    return {
      'schema_version':'1.0.0',
      'candidate_id':candidate['candidate_id']+'-HUMAN-REVIEW',
      'subject':'PHYSICS',
      'artifact_sha256':artifact_set_digest,
      'artifact_sha256_refs':refs,
      'baseline_artifact_sha256':artifact_set_digest,
      'publication_engineering':candidate['machine_gate'],
      'unresolved_major_count':0 if candidate['machine_gate']=='PASS' else len(candidate.get('machine_findings') or []),
      'ai_pre_review_status':'ADVISORY_COMPLETE',
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',required=True); ap.add_argument('--ai-pre-review',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    result=build_binding(load(a.candidate),load(a.ai_pre_review)); Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PHY P-L human-review binding: exact artifact set bound, human authority not implied')
if __name__=='__main__': main()
