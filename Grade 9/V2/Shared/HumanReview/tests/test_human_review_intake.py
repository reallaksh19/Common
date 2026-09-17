#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'engine'))
from ingest_human_reviews import load, load_rubrics, load_submissions, project
V2=ROOT.parents[1]
MATH=V2/'Mathematics'/'Review'/'intake'
candidate=load(MATH/'candidate_binding.json'); policy=load(MATH/'review_policy.json'); rubrics=load_rubrics(MATH)
realreg=load(MATH/'reviewer_authorization.real.json'); testreg=load(MATH/'reviewer_authorization.test-only.json')
real=project(candidate,realreg,policy,rubrics,load_submissions(MATH/'submissions'/'real'),'REAL_RELEASE')
q=real['quality_review_summary']['quality_states']
assert real['intake_status']=='READY' and real['accepted_submission_ids']==[] and real['release_evidence_eligible'] is False
assert (q['SUBJECT_CORRECTNESS'],q['PEDAGOGY_USABILITY'],q['VISUAL_USABILITY'])==('PENDING','PENDING','PENDING')
passsubs=load_submissions(MATH/'submissions'/'test-only'/'pass')
passed=project(candidate,testreg,policy,rubrics,passsubs,'TEST_ONLY')
q=passed['quality_review_summary']['quality_states']
assert (q['SUBJECT_CORRECTNESS'],q['PEDAGOGY_USABILITY'],q['VISUAL_USABILITY'])==('PASS','PASS','PASS')
assert passed['release_evidence_eligible'] is False and passed['fixture_class']=='TEST_ONLY_SYNTHETIC'
failed=project(candidate,testreg,policy,rubrics,load_submissions(MATH/'submissions'/'test-only'/'fail'),'TEST_ONLY')
assert failed['quality_review_summary']['quality_states']['VISUAL_USABILITY']=='FAIL'
def rejected(mutator):
    subs=copy.deepcopy(passsubs); mutator(subs)
    r=project(copy.deepcopy(candidate),copy.deepcopy(testreg),copy.deepcopy(policy),copy.deepcopy(rubrics),subs,'TEST_ONLY')
    assert r['intake_status']=='EVIDENCE_REJECTED' and r['rejected_submissions'] and r['release_evidence_eligible'] is False
    return {x for rr in r['rejected_submissions'] for x in rr['reasons']}
reasons=rejected(lambda s:s[0].__setitem__('source','AI_PRE_REVIEW')); assert 'SCHEMA_INVALID' in reasons
reasons=rejected(lambda s:s[0].__setitem__('reviewer_id','not-authorized')); assert 'REVIEWER_NOT_AUTHORIZED_FOR_CLASS' in reasons
reasons=rejected(lambda s:s[0].update(review_dimension='VISUAL')); assert 'REVIEWER_CLASS_DIMENSION_MISMATCH' in reasons
reasons=rejected(lambda s:s[0].__setitem__('candidate_artifact_sha256','0'*64)); assert 'CANDIDATE_SHA_MISMATCH' in reasons
reasons=rejected(lambda s:s[0]['rubric_results'].pop()); assert 'REQUIRED_RUBRIC_INCOMPLETE' in reasons
reasons=rejected(lambda s:s[0]['rubric_results'][0].__setitem__('disposition','FAIL')); assert 'PASS_WITH_REQUIRED_CRITERION_FAILURE' in reasons
reasons=rejected(lambda s:s[0]['findings'].append({'finding_id':'X','severity':'BLOCKING','status':'OPEN','statement':'blocking'})); assert 'PASS_WITH_OPEN_BLOCKING_FINDING' in reasons
reasons=rejected(lambda s:s[0].__setitem__('reviewer_authorization_version','OLD')); assert 'AUTHORIZATION_VERSION_MISMATCH' in reasons
try: project(candidate,testreg,policy,rubrics,passsubs,'REAL_RELEASE'); raise AssertionError('test registry accepted for real release')
except ValueError: pass
x=copy.deepcopy(passsubs[0]); x['review_dimension']='VISUAL'; x['reviewer_class']='HUMAN_VISUAL'; x['rubric_id']='MATH-VISUAL-RUBRIC-1'; x['rubric_results']=[{'criterion_id':c['criterion_id'],'disposition':'PASS','evidence':'x'} for c in rubrics['VISUAL']['criteria']]; x['reviewer_id']='test-subject-001'
r=project(candidate,testreg,policy,rubrics,[x],'TEST_ONLY'); assert 'REVIEWER_NOT_AUTHORIZED_FOR_CLASS' in r['rejected_submissions'][0]['reasons']
p2=project(candidate,testreg,policy,rubrics,passsubs,'TEST_ONLY'); assert json.dumps(passed,sort_keys=True)==json.dumps(p2,sort_keys=True)

# Four-dimension, exact-artifact-set support is opt-in and leaves legacy Math behavior unchanged.
c4=copy.deepcopy(candidate); c4['candidate_id']='SYNTHETIC-FOUR-DIM'; c4['artifact_sha256_refs']=[candidate['artifact_sha256'],'1'*64]
p4=copy.deepcopy(policy); p4['required_pass_submissions']['ASSESSMENT']=1; p4['require_exact_artifact_set_binding']=True; p4['quality_state_by_dimension']={'SUBJECT':'SUBJECT_CORRECTNESS','PEDAGOGY':'PEDAGOGICAL_DESIGN','ASSESSMENT':'ASSESSMENT_DESIGN','VISUAL':'VISUAL_USABILITY'}
r4=copy.deepcopy(testreg); r4['authorized_reviewers']['HUMAN_ASSESSMENT']=['test-assessment-001']
rubs4=copy.deepcopy(rubrics); rubs4['ASSESSMENT']={'schema_version':'1.0.0','rubric_id':'SYNTH-ASSESSMENT-RUBRIC','review_dimension':'ASSESSMENT','criteria':[{'criterion_id':'A1','required':True,'description':'assessment criterion'}]}
subs4=copy.deepcopy(passsubs)
for s in subs4: s['candidate_artifact_sha256_refs']=list(c4['artifact_sha256_refs'])
subs4.append({'submission_id':'SYNTH-ASSESSMENT-PASS','schema_version':'1.0.0','candidate_artifact_sha256':c4['artifact_sha256'],'candidate_artifact_sha256_refs':list(c4['artifact_sha256_refs']),'review_dimension':'ASSESSMENT','reviewer_class':'HUMAN_ASSESSMENT','reviewer_id':'test-assessment-001','reviewer_authorization_version':r4['version'],'review_status':'PASS','rubric_id':'SYNTH-ASSESSMENT-RUBRIC','rubric_results':[{'criterion_id':'A1','disposition':'PASS','evidence':'synthetic'}],'findings':[],'evidence_refs':['SYNTHETIC'],'attestation':{'affirmed':True,'statement':'synthetic assessment review'},'submitted_at':'2026-09-15T00:00:00Z','source':'HUMAN_SUBMISSION','test_only':True})
four=project(c4,r4,p4,rubs4,subs4,'TEST_ONLY'); q4=four['quality_review_summary']['quality_states']
assert [q4[p4['quality_state_by_dimension'][d]] for d in ('SUBJECT','PEDAGOGY','ASSESSMENT','VISUAL')]==['PASS','PASS','PASS','PASS']
assert four['candidate_artifact_sha256_refs']==sorted(c4['artifact_sha256_refs']) and four['release_evidence_eligible'] is False
broken=copy.deepcopy(subs4); broken[0].pop('candidate_artifact_sha256_refs',None)
br=project(c4,r4,p4,rubs4,broken,'TEST_ONLY'); assert 'CANDIDATE_ARTIFACT_SET_MISMATCH' in {x for rr in br['rejected_submissions'] for x in rr['reasons']}
print('V2 shared human-review intake falsifiers = 16 PASS')
