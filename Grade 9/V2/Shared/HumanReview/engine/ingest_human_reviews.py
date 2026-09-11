#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
SCHEMA_DIR=ROOT/'contracts'
DIM_CLASS={'SUBJECT':'HUMAN_SUBJECT','PEDAGOGY':'HUMAN_PEDAGOGY','VISUAL':'HUMAN_VISUAL'}
DIM_GATE={'SUBJECT':'SUBJECT_CORRECTNESS','PEDAGOGY':'PEDAGOGY_USABILITY','VISUAL':'VISUAL_USABILITY'}

def load(p): return json.loads(Path(p).read_text())
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def schema(name): return load(SCHEMA_DIR/name)
def validate(o,name): Draft202012Validator(schema(name),format_checker=None).validate(o)

def load_rubrics(rubric_dir):
    rubrics={}
    for p in sorted(Path(rubric_dir).glob('*_rubric.json')):
        r=load(p); validate(r,'human-review-rubric.schema.json')
        if r['review_dimension'] in rubrics: raise ValueError('duplicate rubric dimension')
        ids=[c['criterion_id'] for c in r['criteria']]
        if len(ids)!=len(set(ids)): raise ValueError('duplicate rubric criterion')
        rubrics[r['review_dimension']]=r
    if set(rubrics)!=set(DIM_CLASS): raise ValueError('rubrics must cover SUBJECT/PEDAGOGY/VISUAL exactly once')
    return rubrics

def load_submissions(submissions_dir):
    d=Path(submissions_dir)
    if not d.exists(): return []
    return [load(p) for p in sorted(d.rglob('*.json'))]

def assess_submission(sub,candidate,registry,rubrics,mode):
    sid=sub.get('submission_id','') if isinstance(sub,dict) else ''
    reasons=[]
    try: validate(sub,'human-review-submission.schema.json')
    except Exception: return sid or '<UNKNOWN>', ['SCHEMA_INVALID']
    dim=sub['review_dimension']; expected_class=DIM_CLASS[dim]
    if sub['candidate_artifact_sha256']!=candidate['artifact_sha256']: reasons.append('CANDIDATE_SHA_MISMATCH')
    if sub['reviewer_class']!=expected_class: reasons.append('REVIEWER_CLASS_DIMENSION_MISMATCH')
    if sub['reviewer_authorization_version']!=registry['version']: reasons.append('AUTHORIZATION_VERSION_MISMATCH')
    if sub['reviewer_id'] not in registry['authorized_reviewers'][sub['reviewer_class']]: reasons.append('REVIEWER_NOT_AUTHORIZED_FOR_CLASS')
    if mode=='REAL_RELEASE' and sub['test_only']: reasons.append('TEST_ONLY_SUBMISSION_FOR_REAL_RELEASE')
    if mode=='TEST_ONLY' and not sub['test_only']: reasons.append('REAL_SUBMISSION_IN_TEST_ONLY_MODE')
    rubric=rubrics[dim]
    if sub['rubric_id']!=rubric['rubric_id']: reasons.append('RUBRIC_ID_MISMATCH')
    results=sub['rubric_results']; result_ids=[r['criterion_id'] for r in results]
    if len(result_ids)!=len(set(result_ids)): reasons.append('DUPLICATE_RUBRIC_RESULT')
    known={c['criterion_id'] for c in rubric['criteria']}; required={c['criterion_id'] for c in rubric['criteria'] if c['required']}
    if not set(result_ids)<=known: reasons.append('UNKNOWN_RUBRIC_CRITERION')
    if not required<=set(result_ids): reasons.append('REQUIRED_RUBRIC_INCOMPLETE')
    by={r['criterion_id']:r['disposition'] for r in results}
    if sub['review_status']=='PASS' and any(by.get(cid)!='PASS' for cid in required): reasons.append('PASS_WITH_REQUIRED_CRITERION_FAILURE')
    if sub['review_status']=='PASS' and any(f['severity']=='BLOCKING' and f['status']=='OPEN' for f in sub['findings']): reasons.append('PASS_WITH_OPEN_BLOCKING_FINDING')
    if not sub['attestation']['affirmed']: reasons.append('ATTESTATION_NOT_AFFIRMED')
    return sid,reasons

def project(candidate,registry,policy,rubrics,submissions,mode):
    validate(candidate,'candidate-review-binding.schema.json')
    validate(registry,'reviewer-authorization-registry.schema.json')
    validate(policy,'human-review-policy.schema.json')
    if mode=='REAL_RELEASE' and registry['registry_class']!='REAL': raise ValueError('REAL_RELEASE requires REAL authorization registry')
    if mode=='TEST_ONLY' and registry['registry_class']!='TEST_ONLY': raise ValueError('TEST_ONLY requires TEST_ONLY authorization registry')
    original=copy.deepcopy({'candidate':candidate,'registry':registry,'policy':policy,'rubrics':rubrics,'submissions':submissions})
    accepted=[]; rejected=[]; accepted_by={d:[] for d in DIM_CLASS}
    for sub in submissions:
        sid,reasons=assess_submission(sub,candidate,registry,rubrics,mode)
        if reasons: rejected.append({'submission_id':sid,'reasons':sorted(set(reasons))})
        else:
            accepted.append(sid); accepted_by[sub['review_dimension']].append(sub)
    gates={}; counts={}
    for dim in ('SUBJECT','PEDAGOGY','VISUAL'):
        rows=accepted_by[dim]; counts[dim]=len(rows)
        if any(x['review_status']=='FAIL' for x in rows): state='FAIL'
        elif sum(1 for x in rows if x['review_status']=='PASS')>=policy['required_pass_submissions'][dim]: state='PASS'
        else: state='PENDING'
        gates[DIM_GATE[dim]]=state
    quality={'schema_version':'1.0.0','baseline_artifact_sha256':candidate['baseline_artifact_sha256'],'revised_artifact_sha256':candidate['artifact_sha256'],'ai_pre_review_status':candidate['ai_pre_review_status'],'unresolved_major_count':candidate['unresolved_major_count'],'human_review_evidence':counts,'quality_states':{'PUBLICATION_ENGINEERING':candidate['publication_engineering'],**gates,'BENCHMARK_COMPARATIVE_VALIDATION':policy['benchmark_comparative_validation_state']}}
    fixture='REAL' if mode=='REAL_RELEASE' else 'TEST_ONLY_SYNTHETIC'
    release_ok=(mode=='REAL_RELEASE' and registry['registry_class']=='REAL' and not rejected and candidate['publication_engineering']=='PASS' and all(gates[k]=='PASS' for k in gates) and candidate['unresolved_major_count']==0)
    payload={'candidate':candidate,'registry':registry,'policy':policy,'rubrics':rubrics,'submissions':submissions,'mode':mode}
    result={'schema_version':'1.0.0','intake_id':'HUMAN-REVIEW-INTAKE-'+candidate['candidate_id']+'-'+mode,'fixture_class':fixture,'candidate_sha256':candidate['artifact_sha256'],'registry_id':registry['registry_id'],'registry_version':registry['version'],'policy_id':policy['policy_id'],'mode':mode,'intake_status':'EVIDENCE_REJECTED' if rejected else 'READY','accepted_submission_ids':sorted(accepted),'rejected_submissions':sorted(rejected,key=lambda x:x['submission_id']),'quality_review_summary':quality,'release_evidence_eligible':release_ok,'input_digest':sha_obj(payload)}
    validate(result,'human-review-intake-result.schema.json')
    if original!={'candidate':candidate,'registry':registry,'policy':policy,'rubrics':rubrics,'submissions':submissions}: raise AssertionError('input mutation detected')
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',required=True); ap.add_argument('--registry',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--rubric-dir',required=True); ap.add_argument('--submissions-dir',required=True); ap.add_argument('--mode',choices=['REAL_RELEASE','TEST_ONLY'],required=True); ap.add_argument('--out')
    a=ap.parse_args(); result=project(load(a.candidate),load(a.registry),load(a.policy),load_rubrics(a.rubric_dir),load_submissions(a.submissions_dir),a.mode); text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.out: Path(a.out).write_text(text)
    else: print(text,end='')
if __name__=='__main__': main()
