#!/usr/bin/env python3
"""Canonical P-L release authority: Shared HumanReview + final comparator custody."""
import argparse, copy, hashlib, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]; sys.path.insert(0,str(ROOT/'engine'))
from evaluate_physics_exact_product import evaluate as base_evaluate, validate_release, digest, PASS, FAIL, BLOCKED
HUMAN=('SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN','VISUAL_USABILITY')
CLASS={'SUBJECT_CORRECTNESS':('SUBJECT_EXPERT_PASS','AUTHORIZED_PHYSICS_SUBJECT'),'PEDAGOGICAL_DESIGN':('PEDAGOGY_EXPERT_PASS','AUTHORIZED_PEDAGOGY'),'ASSESSMENT_DESIGN':('ASSESSMENT_EXPERT_PASS','AUTHORIZED_ASSESSMENT'),'VISUAL_USABILITY':('VISUAL_USABILITY_EXPERT_PASS','AUTHORIZED_VISUAL_USABILITY')}
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(o): return hashlib.sha256(canonical(o)).hexdigest()
def check_schema(name,obj): Draft202012Validator(load(ROOT/'contracts'/name)).validate(obj)
def candidate_refs(candidate): return sorted(p['artifact_sha256'] for p in candidate['products'])

def validate_governed_intake(binding,intake,candidate,mode):
    refs=candidate_refs(candidate); artifact_set_digest=sha(refs)
    if binding.get('candidate_id')!=candidate['candidate_id']+'-HUMAN-REVIEW': raise ValueError('HUMAN_REVIEW_BINDING_CANDIDATE_MISMATCH')
    if sorted(binding.get('artifact_sha256_refs') or [])!=refs: raise ValueError('HUMAN_REVIEW_BINDING_ARTIFACT_SET_MISMATCH')
    if binding.get('artifact_sha256')!=artifact_set_digest or binding.get('baseline_artifact_sha256')!=artifact_set_digest: raise ValueError('HUMAN_REVIEW_BINDING_DIGEST_MISMATCH')
    if intake.get('candidate_sha256')!=artifact_set_digest or sorted(intake.get('candidate_artifact_sha256_refs') or [])!=refs: raise ValueError('HUMAN_REVIEW_INTAKE_ARTIFACT_SET_MISMATCH')
    summary=intake.get('quality_review_summary') or {}
    if summary.get('revised_artifact_sha256')!=artifact_set_digest or sorted(summary.get('artifact_sha256_refs') or [])!=refs: raise ValueError('HUMAN_REVIEW_SUMMARY_ARTIFACT_SET_MISMATCH')
    if intake.get('policy_id')!='PHY-P-L-HUMAN-REVIEW-v1': raise ValueError('HUMAN_REVIEW_POLICY_MISMATCH')
    if intake.get('intake_status')!='READY' or intake.get('rejected_submissions'): raise ValueError('HUMAN_REVIEW_EVIDENCE_REJECTED')
    if mode=='REAL_RELEASE':
        if intake.get('mode')!='REAL_RELEASE' or intake.get('fixture_class')!='REAL' or intake.get('registry_id')!='PHY-P-L-REVIEWERS-REAL-v1': raise ValueError('REAL_HUMAN_REVIEW_CUSTODY_INVALID')
    else:
        if intake.get('mode')!='TEST_ONLY' or intake.get('fixture_class')!='TEST_ONLY_SYNTHETIC' or intake.get('registry_id')!='PHY-P-L-REVIEWERS-TEST-v1': raise ValueError('TEST_HUMAN_REVIEW_CUSTODY_INVALID')
    return refs

def project_attestations(intake,refs):
    q=intake['quality_review_summary']['quality_states']; out=[]
    for state in HUMAN:
        value=q.get(state,'PENDING')
        if value in {'PASS','FAIL'}:
            review_class,role=CLASS[state]; out.append({'quality_state':state,'review_class':review_class,'reviewer_role':role,'attestation_ref':intake['intake_id']+':'+state,'artifact_sha256_refs':refs,'outcome':value})
    return out

def validate_comparison(comp,candidate,refs,mode,human_pass,human_release_eligible):
    check_schema('physics-reference-comparison.schema.json',comp)
    x=copy.deepcopy(comp); got=x.pop('comparison_digest'); expected=sha(x)
    if got!=expected: raise ValueError('REFERENCE_COMPARISON_DIGEST_MISMATCH')
    if not human_pass: raise ValueError('REFERENCE_COMPARISON_RUN_BEFORE_HUMAN_GATES')
    if mode=='REAL_RELEASE' and not human_release_eligible: raise ValueError('REAL_HUMAN_REVIEW_EVIDENCE_NOT_ELIGIBLE_FOR_REFERENCE')
    if comp['candidate_ref']!=candidate['candidate_id'] or comp['candidate_digest']!=candidate['candidate_digest'] or sorted(comp['artifact_sha256_refs'])!=refs: raise ValueError('REFERENCE_COMPARISON_NOT_BOUND_TO_EXACT_CANDIDATE')
    if mode=='REAL_RELEASE':
        if comp['mode']!='REAL_RELEASE' or comp['fixture_class']!='REAL' or not comp['release_evidence_eligible']: raise ValueError('REAL_REFERENCE_COMPARISON_CUSTODY_INVALID')
    else:
        if comp['mode']!='TEST_ONLY' or comp['fixture_class']!='TEST_ONLY_SYNTHETIC' or comp['release_evidence_eligible']: raise ValueError('TEST_REFERENCE_COMPARISON_CUSTODY_INVALID')

def evaluate_governed(candidate,policy,ai,binding,intake,mode='REAL_RELEASE',comparison=None):
    refs=validate_governed_intake(binding,intake,candidate,mode); attestations=project_attestations(intake,refs)
    release=base_evaluate(candidate,policy,attestations,ai); q=release['quality_states']; human_pass=all(q[s]=='PASS' for s in HUMAN); human_release_eligible=bool(intake.get('release_evidence_eligible'))
    reference_authorized=bool(human_pass and (mode=='TEST_ONLY' or human_release_eligible))
    if comparison is not None:
        validate_comparison(comparison,candidate,refs,mode,human_pass,human_release_eligible)
        q['REFERENCE_COMPARABILITY']=comparison['status']; q['MATURE_DESIGN_QUALITY']='PASS' if comparison['status']=='PASS' else 'FAIL'
        if comparison['status']=='FAIL': release['classification']=policy['failed_classification']; release['exit_code']=FAIL
        else: release['classification']=policy['mature_classification']; release['exit_code']=PASS
        release['blocking_states']=sorted(s for s in policy['required_quality_states'] if q[s] in {'PENDING','NOT_RUN','READY_TO_RUN'})
        release['blocking_reason']='Every required governed gate resolved PASS.' if release['exit_code']==PASS else 'Final reference comparison failed.'
        release['release_digest']=''; release['release_digest']=digest(release,'release_digest'); validate_release(release,candidate,policy)
    real_ok=bool(mode=='REAL_RELEASE' and release['exit_code']==PASS and human_release_eligible and comparison and comparison.get('release_evidence_eligible'))
    if mode=='REAL_RELEASE' and release['exit_code']==PASS and not real_ok: raise ValueError('REAL_GOVERNED_RELEASE_EVIDENCE_INCOMPLETE')
    if mode=='TEST_ONLY' and release['exit_code']==PASS:
        classification='TEST_ONLY_FULL_PASS_NOT_RELEASEABLE'; exit_code=BLOCKED
    else:
        classification=release['classification']; exit_code=release['exit_code']
    blocking=release['blocking_states'] if exit_code!=BLOCKED or mode=='REAL_RELEASE' else sorted(set(release['blocking_states']+['TEST_ONLY_EVIDENCE_NOT_RELEASEABLE']))
    decision={'decision_id':'PHY-P-L-GOVERNED-RELEASE-'+mode,'schema_version':'1.0.0','subject':'PHYSICS','candidate_ref':candidate['candidate_id'],'candidate_digest':candidate['candidate_digest'],'artifact_sha256_refs':refs,'gate_mode':mode,'human_review_intake_ref':intake['intake_id'],'human_review_input_digest':intake['input_digest'],'human_review_release_evidence_eligible':human_release_eligible,'quality_states':q,'reference_comparison_ref':comparison['comparison_id'] if comparison else None,'reference_comparison_digest':comparison['comparison_digest'] if comparison else None,'reference_read_authorized':reference_authorized,'classification':classification,'release_evidence_eligible':real_ok,'exit_code':exit_code,'blocking_states':blocking,'decision_digest':''}
    decision['decision_digest']=sha({k:v for k,v in decision.items() if k!='decision_digest'}); check_schema('physics-governed-release.schema.json',decision)
    if decision['release_evidence_eligible'] and (mode!='REAL_RELEASE' or decision['classification']!=policy['mature_classification'] or decision['exit_code']!=PASS): raise ValueError('GOVERNED_RELEASE_ELIGIBILITY_INVALID')
    return decision,release

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--ai-pre-review',required=True); ap.add_argument('--human-review-binding',required=True); ap.add_argument('--human-review-intake',required=True); ap.add_argument('--reference-comparison'); ap.add_argument('--mode',choices=['REAL_RELEASE','TEST_ONLY'],default='REAL_RELEASE'); ap.add_argument('--out',required=True); a=ap.parse_args()
    d,_=evaluate_governed(load(a.candidate),load(a.policy),load(a.ai_pre_review),load(a.human_review_binding),load(a.human_review_intake),a.mode,load(a.reference_comparison) if a.reference_comparison else None); Path(a.out).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(f"PHY P-L governed release: {d['classification']} (exit {d['exit_code']})"); return d['exit_code']
if __name__=='__main__': raise SystemExit(main())
