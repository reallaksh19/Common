#!/usr/bin/env python3
import copy, json, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PHYS=ROOT.parent; REPO=ROOT.parents[3]; SHARED=REPO/'Grade 9'/'V2'/'Shared'/'HumanReview'
sys.path[:0]=[str(ROOT/'engine'),str(PHYS/'ColdStart'/'engine'),str(SHARED/'engine')]
from physics_cold_start_runner import run_cold_start
from evaluate_physics_exact_product import build_candidate, BLOCKED
from audit_physics_exact_candidate import build_review
from build_physics_human_review_binding import build_binding
from evaluate_physics_governed_release import evaluate_governed, sha
from check_physics_reference_eligibility import check as check_reference
from ingest_human_reviews import load_rubrics, project, load_submissions

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
policy=load(ROOT/'registry'/'physics-exact-product-quality-policy.json'); primitives=load(PHYS/'Representation'/'registry'/'physics-teaching-primitive-registry.json'); manifest=load(PHYS/'GENERATION_AUTHORITY_MANIFEST.json'); R=ROOT/'review-intake'; hp=load(R/'review_policy.json'); dims=tuple(hp['required_pass_submissions']); rubrics=load_rubrics(R,dims); realreg=load(R/'reviewer_authorization.real.json'); testreg=load(R/'reviewer_authorization.test-only.json')
with tempfile.TemporaryDirectory() as td:
    run=Path(td)/'with-attempts'; report,_=run_cold_start(manifest,run,True,REPO); candidate=build_candidate(run,report,load(run/'coverage_closure.json'),load(run/'core1_page_map.json'),load(run/'core2_page_map.json'),load(run/'core2.json'),primitives,policy); ai=build_review(run,policy); binding=build_binding(candidate,ai)
    real=project(binding,realreg,hp,rubrics,load_submissions(R/'submissions'/'real'),'REAL_RELEASE'); decision,_=evaluate_governed(candidate,policy,ai,binding,real,'REAL_RELEASE'); assert decision['exit_code']==BLOCKED and decision['release_evidence_eligible'] is False and decision['reference_read_authorized'] is False
    should_not=Path(td)/'SHOULD_NOT_BE_READ.json'; elig=check_reference(binding,real,'REAL_RELEASE',should_not); assert elig['status']=='BLOCKED_HUMAN_QUALITY_GATES' and elig['reference_read_attempted'] is False and not should_not.exists()
    classes={'SUBJECT':('HUMAN_SUBJECT','physics-test-subject-001'),'PEDAGOGY':('HUMAN_PEDAGOGY','physics-test-pedagogy-001'),'ASSESSMENT':('HUMAN_ASSESSMENT','physics-test-assessment-001'),'VISUAL':('HUMAN_VISUAL','physics-test-visual-001')}; subs=[]
    for dim,(cls,rid) in classes.items():
        rubric=rubrics[dim]; subs.append({'submission_id':'PHY-TEST-'+dim,'schema_version':'1.0.0','candidate_artifact_sha256':binding['artifact_sha256'],'candidate_artifact_sha256_refs':binding['artifact_sha256_refs'],'review_dimension':dim,'reviewer_class':cls,'reviewer_id':rid,'reviewer_authorization_version':testreg['version'],'review_status':'PASS','rubric_id':rubric['rubric_id'],'rubric_results':[{'criterion_id':c['criterion_id'],'disposition':'PASS','evidence':'synthetic'} for c in rubric['criteria']],'findings':[],'evidence_refs':['SYNTHETIC'],'attestation':{'affirmed':True,'statement':'synthetic'},'submitted_at':'2026-09-15T00:00:00Z','source':'HUMAN_SUBMISSION','test_only':True})
    test=project(binding,testreg,hp,rubrics,subs,'TEST_ONLY'); td0,_=evaluate_governed(candidate,policy,ai,binding,test,'TEST_ONLY'); assert td0['reference_read_authorized'] is True and td0['release_evidence_eligible'] is False
    comp={'comparison_id':'PHY-TEST-COMPARISON','schema_version':'1.0.0','subject':'PHYSICS','comparator_id':'FROZEN_PR156_MATURE_DESIGN_COMPARATOR','candidate_ref':candidate['candidate_id'],'candidate_digest':candidate['candidate_digest'],'artifact_sha256_refs':sorted(binding['artifact_sha256_refs']),'mode':'TEST_ONLY','fixture_class':'TEST_ONLY_SYNTHETIC','reference_access_phase':'FINAL_COMPARATIVE_VALIDATION','raw_reference_used_as_runtime_template':False,'reference_ref':'SYNTHETIC_REFERENCE','reference_digest':'1'*64,'status':'PASS','release_evidence_eligible':False,'comparison_digest':''}; comp['comparison_digest']=sha({k:v for k,v in comp.items() if k!='comparison_digest'})
    td1,_=evaluate_governed(candidate,policy,ai,binding,test,'TEST_ONLY',comp); assert td1['quality_states']['MATURE_DESIGN_QUALITY']=='PASS' and td1['classification']=='TEST_ONLY_FULL_PASS_NOT_RELEASEABLE' and td1['exit_code']==BLOCKED and td1['release_evidence_eligible'] is False
    try: evaluate_governed(candidate,policy,ai,binding,real,'REAL_RELEASE',dict(comp,mode='REAL_RELEASE',fixture_class='REAL',release_evidence_eligible=True)); raise AssertionError('early comparison accepted')
    except ValueError as e: assert str(e).startswith('REFERENCE_COMPARISON_RUN_BEFORE_HUMAN_GATES') or str(e).startswith('REFERENCE_COMPARISON_DIGEST_MISMATCH')
    try: evaluate_governed(candidate,policy,ai,binding,test,'REAL_RELEASE'); raise AssertionError('test intake accepted as real')
    except ValueError as e: assert str(e).startswith('REAL_HUMAN_REVIEW_CUSTODY_INVALID')
print('PHY P-L governed release + reference guard = PASS')
