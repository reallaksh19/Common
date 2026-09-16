#!/usr/bin/env python3
import copy, json, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHYS=ROOT.parent; REPO=ROOT.parents[3]; SHARED=REPO/'Grade 9'/'V2'/'Shared'/'HumanReview'
sys.path[:0]=[str(ROOT/'engine'),str(PHYS/'ColdStart'/'engine'),str(SHARED/'engine')]
from physics_cold_start_runner import run_cold_start
from evaluate_physics_exact_product import build_candidate
from audit_physics_exact_candidate import build_review
from build_physics_human_review_binding import build_binding
from ingest_human_reviews import load_rubrics, project, load_submissions

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
policy=load(ROOT/'registry'/'physics-exact-product-quality-policy.json'); primitives=load(PHYS/'Representation'/'registry'/'physics-teaching-primitive-registry.json'); manifest=load(PHYS/'GENERATION_AUTHORITY_MANIFEST.json')
R=ROOT/'review-intake'; review_policy=load(R/'review_policy.json'); dims=tuple(review_policy['required_pass_submissions']); rubrics=load_rubrics(R,dims); realreg=load(R/'reviewer_authorization.real.json'); testreg=load(R/'reviewer_authorization.test-only.json')
with tempfile.TemporaryDirectory() as td:
    run=Path(td)/'with-attempts'; report,_=run_cold_start(manifest,run,True,REPO)
    candidate=build_candidate(run,report,load(run/'coverage_closure.json'),load(run/'core1_page_map.json'),load(run/'core2_page_map.json'),load(run/'core2.json'),primitives,policy)
    ai=build_review(run,policy); binding=build_binding(candidate,ai)
    assert binding['publication_engineering']=='PASS' and len(binding['artifact_sha256_refs'])==2
    real=project(binding,realreg,review_policy,rubrics,load_submissions(R/'submissions'/'real'),'REAL_RELEASE')
    q=real['quality_review_summary']['quality_states']; assert [q[x] for x in ('SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN','VISUAL_USABILITY')]==['PENDING']*4
    assert real['accepted_submission_ids']==[] and real['release_evidence_eligible'] is False
    classes={'SUBJECT':('HUMAN_SUBJECT','physics-test-subject-001'),'PEDAGOGY':('HUMAN_PEDAGOGY','physics-test-pedagogy-001'),'ASSESSMENT':('HUMAN_ASSESSMENT','physics-test-assessment-001'),'VISUAL':('HUMAN_VISUAL','physics-test-visual-001')}
    subs=[]
    for dim,(cls,rid) in classes.items():
        rubric=rubrics[dim]; subs.append({'submission_id':'PHY-TEST-'+dim,'schema_version':'1.0.0','candidate_artifact_sha256':binding['artifact_sha256'],'candidate_artifact_sha256_refs':binding['artifact_sha256_refs'],'review_dimension':dim,'reviewer_class':cls,'reviewer_id':rid,'reviewer_authorization_version':testreg['version'],'review_status':'PASS','rubric_id':rubric['rubric_id'],'rubric_results':[{'criterion_id':c['criterion_id'],'disposition':'PASS','evidence':'synthetic test evidence'} for c in rubric['criteria']],'findings':[],'evidence_refs':['TEST_ONLY_SYNTHETIC'],'attestation':{'affirmed':True,'statement':'synthetic test-only review'},'submitted_at':'2026-09-15T00:00:00Z','source':'HUMAN_SUBMISSION','test_only':True})
    test=project(binding,testreg,review_policy,rubrics,subs,'TEST_ONLY'); tq=test['quality_review_summary']['quality_states']; assert [tq[x] for x in ('SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN','VISUAL_USABILITY')]==['PASS']*4
    assert test['release_evidence_eligible'] is False
    bad=copy.deepcopy(subs); bad[0]['candidate_artifact_sha256_refs']=bad[0]['candidate_artifact_sha256_refs'][:1]
    rejected=project(binding,testreg,review_policy,rubrics,bad,'TEST_ONLY'); assert 'CANDIDATE_ARTIFACT_SET_MISMATCH' in {x for r in rejected['rejected_submissions'] for x in r['reasons']}
    fake_real=copy.deepcopy(subs); [x.__setitem__('test_only',False) for x in fake_real]
    rr=project(binding,realreg,review_policy,rubrics,fake_real,'REAL_RELEASE'); assert rr['intake_status']=='EVIDENCE_REJECTED' and rr['release_evidence_eligible'] is False
print('PHY P-L shared human-review intake = PASS (real remains four PENDING gates)')
