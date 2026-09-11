#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]; CHEM=D.parent; REPO=CHEM.parents[2]
sys.path.insert(0,str(D/'engine'))
from chemistry_cold_start_runner import run_cold_start,compare_runs,digest,validate_source_correction_custody
from chemistry_cold_start_validator import validate_report,validate_comparison

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError('expected '+code)
def redigest_report(r): r['report_digest']=''; r['report_digest']=digest(r,'report_digest'); return r
def redigest_comp(c): c['comparison_digest']=''; c['comparison_digest']=digest(c,'comparison_digest'); return c

A=CHEM/'AssessmentIntake'/'fixtures'; E=CHEM/'LearnerEvidence'/'fixtures'; COLD=D
sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
attempts=load(E/'chemistry-diagnostic-attempt-set.fixture.json'); evidence=load(E/'chemistry-learner-evidence-ledger.fixture.json')
manifest=load(CHEM/'CHEMISTRY_GENERATION_AUTHORITY_MANIFEST.json')

run_a,ia=run_cold_start(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),repo_root=REPO,run_id='CHEM-C-K-RUN-A')
run_b,ib=run_cold_start(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(attempts),copy.deepcopy(evidence),repo_root=REPO,run_id='CHEM-C-K-RUN-B')
validate_report(run_a,manifest,ia); validate_report(run_b,manifest,ib)
comparison=compare_runs(run_a,run_b); validate_comparison(comparison,run_a,run_b)

assert run_a['summary']['source_unit_count']==12
assert run_a['summary']['question_count']==14
assert run_a['summary']['external_candidate_count']==6
assert run_a['summary']['eligible_external_count']==5
assert run_a['summary']['core2_page_count']==5
assert run_a['summary']['product_count']==2
assert run_a['summary']['appendix_a_present'] and run_a['summary']['appendix_b_present'] and run_a['summary']['appendix_c_present']
assert all(x['learner_state']=='UNKNOWN' for x in ia['study_model']['capability_records'])
assert all(x['lesson_mode']=='FULL_LEARNING' for x in ia['core1']['lessons'])
assert run_a['stage_outputs']['source_obligation_refs']==run_b['stage_outputs']['source_obligation_refs']
assert run_a['stage_outputs']['external_candidate_refs']==run_b['stage_outputs']['external_candidate_refs']
assert run_a['stage_outputs']['scope_classification_signature']==run_b['stage_outputs']['scope_classification_signature']
assert run_a['stage_outputs']['canonical_binding_signature']==run_b['stage_outputs']['canonical_binding_signature']
assert run_a['stage_outputs']['problem_family_truth_signature']==run_b['stage_outputs']['problem_family_truth_signature']
assert run_a['stage_outputs']['primary_external_ownership_signature']==run_b['stage_outputs']['primary_external_ownership_signature']
assert run_a['stage_outputs']['canonical_chemistry_truth_signature']==run_b['stage_outputs']['canonical_chemistry_truth_signature']
assert run_a['stage_outputs']['learner_state_signature']!=run_b['stage_outputs']['learner_state_signature']
assert run_a['stage_outputs']['treatment_signature']!=run_b['stage_outputs']['treatment_signature']
assert not run_a['runtime_dependency_audit']['manual_precomputed_inputs_used']
assert not run_b['runtime_dependency_audit']['manual_precomputed_inputs_used']
assert not run_a['runtime_dependency_audit']['forbidden_reads']

Draft202012Validator(load(D/'contracts'/'chemistry-cold-start-run-report.schema.json')).validate(run_a)
Draft202012Validator(load(D/'contracts'/'chemistry-cold-start-run-report.schema.json')).validate(run_b)
Draft202012Validator(load(D/'contracts'/'chemistry-two-product-package.schema.json')).validate(run_a['two_product_package'])
Draft202012Validator(load(D/'contracts'/'chemistry-cold-start-comparison.schema.json')).validate(comparison)

# 1 COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY
bad=copy.deepcopy(run_a); bad['runtime_dependency_audit']['chat_or_issue_history_used']=True; redigest_report(bad)
expect('COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY',lambda:validate_report(bad,manifest))
# 2 GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED
bad=copy.deepcopy(run_a); bad['runtime_dependency_audit']['manual_precomputed_inputs_used']=['ChemistrySourceObligationLedger']; redigest_report(bad)
expect('GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED',lambda:validate_report(bad,manifest))
# 3 GENERATION_STARTS_FROM_PREFILTERED_ELIGIBLE_PYQS
bad=copy.deepcopy(run_a); bad['runtime_dependency_audit']['manual_precomputed_inputs_used']=['PrefilteredEligibleExternalSet']; redigest_report(bad)
expect('GENERATION_STARTS_FROM_PREFILTERED_ELIGIBLE_PYQS',lambda:validate_report(bad,manifest))
# 4 RAW_PR157_READ_DURING_PRODUCTION
bad=copy.deepcopy(run_a); bad['runtime_dependency_audit']['raw_pr157_used']=True; redigest_report(bad)
expect('RAW_PR157_READ_DURING_PRODUCTION',lambda:validate_report(bad,manifest))
# 5 MANUAL_STUDYMODEL_REQUIRED
bad=copy.deepcopy(run_a); bad['runtime_dependency_audit']['manual_precomputed_inputs_used']=['LearnerStudyModel']; redigest_report(bad)
expect('MANUAL_STUDYMODEL_REQUIRED',lambda:validate_report(bad,manifest))
# 6 MANUAL_PROBLEM_FAMILY_MAP_REQUIRED
bad=copy.deepcopy(run_a); bad['runtime_dependency_audit']['manual_precomputed_inputs_used']=['ProblemFamilyMap']; redigest_report(bad)
expect('MANUAL_PROBLEM_FAMILY_MAP_REQUIRED',lambda:validate_report(bad,manifest))
# 7 NO_ATTEMPT_RUN_INVENTS_CHEMISTRY_WEAKNESS
bad_internal=copy.deepcopy(ia); bad_internal['study_model']['capability_records'][0]['learner_state']='EVIDENCE_OF_DIFFICULTY'
expect('NO_ATTEMPT_RUN_INVENTS_CHEMISTRY_WEAKNESS',lambda:validate_report(run_a,manifest,bad_internal))
# 8 ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE
bad=copy.deepcopy(comparison); bad['invariants']['source_obligation_denominator_identical']=False; redigest_comp(bad)
expect('ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE',lambda:validate_comparison(bad,run_a,run_b))
# 9 ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY
bad=copy.deepcopy(comparison); bad['invariants']['scope_classification_identical']=False; redigest_comp(bad)
expect('ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY',lambda:validate_comparison(bad,run_a,run_b))
# 10 ATTEMPT_RUN_CHANGES_PRIMARY_QUESTION_OWNERSHIP
bad=copy.deepcopy(comparison); bad['invariants']['primary_question_ownership_identical']=False; redigest_comp(bad)
expect('ATTEMPT_RUN_CHANGES_PRIMARY_QUESTION_OWNERSHIP',lambda:validate_comparison(bad,run_a,run_b))
# 11 ATTEMPT_RUN_CHANGES_CANONICAL_CHEMISTRY_TRUTH
bad=copy.deepcopy(comparison); bad['invariants']['canonical_chemistry_truth_identical']=False; redigest_comp(bad)
expect('ATTEMPT_RUN_CHANGES_CANONICAL_CHEMISTRY_TRUTH',lambda:validate_comparison(bad,run_a,run_b))
# 12 FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE
bad=copy.deepcopy(run_a); bad['authority_trace']=[x for x in bad['authority_trace'] if x['decision_class']!='BADGE']; redigest_report(bad)
expect('FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE',lambda:validate_report(bad,manifest))
# 13 SOURCE_DAMAGE_FIXED_WITHOUT_REVIEW_EVENT
bad_source=copy.deepcopy(sources); bad_source['units'][0]['source_provenance']['human_correction_events']=['UNREGISTERED-QC-EVENT']
expect('SOURCE_DAMAGE_FIXED_WITHOUT_REVIEW_EVENT',lambda:validate_source_correction_custody(bad_source,load(CHEM/'AssessmentReview'/'registry'/'chemistry-qc-events.json')))
# 14 THIRD_HANDOUT_PDF_CREATED
bad=copy.deepcopy(run_a); bad['two_product_package']['product_count']=3; bad['two_product_package']['third_product_created']=True; bad['two_product_package']['products'].append(copy.deepcopy(bad['two_product_package']['products'][0])); redigest_report(bad)
expect('THIRD_HANDOUT_PDF_CREATED',lambda:validate_report(bad,manifest))
# 15 APPENDIX_C_MISSING_FROM_CORE1
bad=copy.deepcopy(run_a); bad['summary']['appendix_c_present']=False; core=next(x for x in bad['two_product_package']['products'] if x['product_id']=='CORE_STUDY_GUIDE'); core['required_sections']=[x for x in core['required_sections'] if x!='APPENDIX_C_PRINTABLE_HANDOUT']; redigest_report(bad)
expect('APPENDIX_C_MISSING_FROM_CORE1',lambda:validate_report(bad,manifest))

# Deterministic replay for all authority-selection and custody records.
run_a2,_=run_cold_start(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),repo_root=REPO,run_id='CHEM-C-K-RUN-A')
assert json.dumps(run_a,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(run_a2,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-K required falsifiers = 15 PASS')
print('CHEMISTRY C-K Run A no-attempt cold start = PASS')
print('CHEMISTRY C-K Run B attempt-present cold start = PASS')
print('CHEMISTRY C-K Run A/B invariant comparison = PASS')
print('CHEMISTRY C-K exactly two semantic learner candidates = PASS')
print('CHEMISTRY C-K repository-only authority trace = PASS')
print('CHEMISTRY C-K deterministic replay = PASS')
