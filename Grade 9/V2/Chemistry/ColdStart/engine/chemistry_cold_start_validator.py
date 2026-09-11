#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve(); COLD=HERE.parents[1]; CHEM=HERE.parents[2]; REPO=HERE.parents[5]
sys.path.insert(0,str(HERE.parent))
from chemistry_cold_start_runner import digest,fail,verify_manifest,compare_runs

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def validate_report(report,manifest,internal=None):
    verify_manifest(manifest)
    if report['report_digest']!=digest(report,'report_digest'): fail('FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE','report digest')
    audit=report['runtime_dependency_audit']; reads=audit['runtime_reads']; manual=audit['manual_precomputed_inputs_used']
    if audit['chat_or_issue_history_used'] or any('issue' in x.lower() or 'chat' in x.lower() or 'conversation' in x.lower() for x in reads): fail('COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY')
    if audit['raw_pr157_used'] or any('pull/157' in x.lower() or 'pr157' in x.lower() for x in reads): fail('RAW_PR157_READ_DURING_PRODUCTION')
    if 'ChemistrySourceObligationLedger' in manual: fail('GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED')
    if 'PrefilteredEligibleExternalSet' in manual: fail('GENERATION_STARTS_FROM_PREFILTERED_ELIGIBLE_PYQS')
    if 'LearnerStudyModel' in manual: fail('MANUAL_STUDYMODEL_REQUIRED')
    if 'ProblemFamilyMap' in manual: fail('MANUAL_PROBLEM_FAMILY_MAP_REQUIRED')
    req=set(manifest['required_authority_trace_decisions']); traces=report['authority_trace']; got={x['decision_class'] for x in traces}
    if not req<=got or any(not x['authority_refs'] or not x['resolution'].strip() or x['resolution'].strip().lower()=='agent decided' for x in traces): fail('FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE')
    pkg=report['two_product_package']
    if pkg['product_count']!=2 or len(pkg['products'])!=2 or pkg['third_product_created']: fail('THIRD_HANDOUT_PDF_CREATED')
    core=next((x for x in pkg['products'] if x['product_id']=='CORE_STUDY_GUIDE'),None)
    if not core or 'APPENDIX_C_PRINTABLE_HANDOUT' not in core['required_sections'] or not report['summary']['appendix_c_present']: fail('APPENDIX_C_MISSING_FROM_CORE1')
    if report['run_mode']=='NO_ATTEMPT' and report['input_custody']['attempt_set_digest'] is not None: fail('NO_ATTEMPT_RUN_INVENTS_CHEMISTRY_WEAKNESS','attempt digest present')
    if internal is not None and report['run_mode']=='NO_ATTEMPT':
        states=[x['learner_state'] for x in internal['study_model']['capability_records']]
        if any(x!='UNKNOWN' for x in states): fail('NO_ATTEMPT_RUN_INVENTS_CHEMISTRY_WEAKNESS')
        if any(x['lesson_mode']!='FULL_LEARNING' for x in internal['core1']['lessons']): fail('NO_ATTEMPT_RUN_INVENTS_CHEMISTRY_WEAKNESS','scope shortened without evidence')
    Draft202012Validator(load(COLD/'contracts'/'chemistry-cold-start-run-report.schema.json')).validate(report)
    Draft202012Validator(load(COLD/'contracts'/'chemistry-two-product-package.schema.json')).validate(pkg)
    return True

def validate_comparison(comp,a,b):
    if comp['comparison_digest']!=digest(comp,'comparison_digest'): fail('ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE','comparison digest')
    inv=comp['invariants']
    if not inv['source_set_digest_identical'] or not inv['question_set_digest_identical'] or not inv['corpus_digest_identical'] or not inv['declared_topic_scope_digest_identical'] or not inv['source_obligation_denominator_identical']: fail('ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE')
    if not inv['external_candidate_denominator_identical'] or not inv['scope_classification_identical']: fail('ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY')
    if not inv['primary_question_ownership_identical']: fail('ATTEMPT_RUN_CHANGES_PRIMARY_QUESTION_OWNERSHIP')
    if not inv['canonical_chemistry_truth_identical'] or not inv['canonical_bindings_identical'] or not inv['problem_family_truth_identical']: fail('ATTEMPT_RUN_CHANGES_CANONICAL_CHEMISTRY_TRUTH')
    if a['input_custody']['attempt_set_digest'] is not None or b['input_custody']['attempt_set_digest'] is None: fail('ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE','run modes')
    Draft202012Validator(load(COLD/'contracts'/'chemistry-cold-start-comparison.schema.json')).validate(comp)
    return True

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--report',required=True); ap.add_argument('--manifest',default=str(CHEM/'CHEMISTRY_GENERATION_AUTHORITY_MANIFEST.json')); a=ap.parse_args()
    validate_report(load(a.report),load(a.manifest)); print('CHEMISTRY C-K cold-start report = PASS')
if __name__=='__main__': main()
