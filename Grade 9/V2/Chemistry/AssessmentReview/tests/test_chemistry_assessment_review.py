#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
sys.path.insert(0, str(D / 'engine'))
sys.path.insert(0, str(CHEM / 'AssessmentIntake' / 'engine'))

from review_chemistry_assessment import build_review, digest_without_field, load_registry  # noqa: E402
from build_chemistry_assessment_intake import digest as intake_digest, q_payload  # noqa: E402

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def expect_error(code, fn):
    try: fn()
    except ValueError as exc:
        assert str(exc).startswith(code), (code, str(exc)); return
    raise AssertionError(f'expected {code}')
def redigest_registry(r): r['registry_digest']=digest_without_field(r,'registry_digest'); return r
def redigest_qc(qc):
    for event in qc['events']: event['event_digest']=digest_without_field(event,'event_digest')
    qc['registry_digest']=digest_without_field(qc,'registry_digest'); return qc
def review_q(reg, ref): return next(x for x in reg['question_reviews'] if x['item_ref']==ref)
def review_s(reg, ref): return next(x for x in reg['source_reviews'] if x['source_unit_ref']==ref)

sources=load(CHEM/'AssessmentIntake'/'fixtures'/'mixed-chemistry-source.fixture.json')
questions=load(CHEM/'AssessmentIntake'/'fixtures'/'mixed-chemistry-question-set.fixture.json')
registry,registry_manifest_digest=load_registry(D/'registry'/'chemistry-item-validity-registry.json')
policy=load(D/'policies'/'chemistry-diagnostic-use-policy.json')
qc=load(D/'registry'/'chemistry-qc-events.json')
cases=load(D/'fixtures'/'chemistry-review-cases.fixture.json')

bundle=build_review(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy),copy.deepcopy(qc),registry_manifest_digest=registry_manifest_digest)
assert bundle['review_precedes_attempt_interpretation'] is True
assert bundle['attempt_data_consumed'] is False
assert bundle['summary']['source_unit_count']==12
assert bundle['summary']['question_item_count']==17
assert bundle['bundle_digest']==digest_without_field(bundle,'bundle_digest')
assert bundle['review_registry_manifest_digest']==registry_manifest_digest
by_q={x['item_ref']:x for x in bundle['question_reviews']}
assert set(by_q)=={f'CQ{i:02d}' for i in range(1,15)}|{'CQ14.a','CQ14.b','CQ14.c'}
assert by_q['CQ07']['validity_state']=='VALID_CONDITION_SENSITIVE'
assert by_q['CQ07']['required_conditions']==['heat']
assert by_q['CQ13']['source_integrity_state']=='FORMULA_OR_CHARGE_AMBIGUITY'
assert by_q['CQ13']['validity_state']=='REVIEW_REQUIRED'
assert by_q['CQ13']['diagnostic_use']=='EXCLUDE_FROM_NEGATIVE_INFERENCE'
assert by_q['CQ13']['diagnostic_constraints']['negative_inference_allowed'] is False
assert 'QUESTION:CQ13' in bundle['summary']['blocking_review_refs']
required_cases={'CLEAN','SOURCE_INTERNAL_TYPO','FORMULA_OR_CHARGE_OCR_AMBIGUITY','UNDERDETERMINED','CONDITION_SENSITIVE','MISSING_STRUCTURE_OR_FIGURE','EXTERNAL_CLEAN'}
assert {x['case_type'] for x in cases['cases']}==required_cases

# 1 SOURCE_TYPO_SILENTLY_CORRECTED
bad=copy.deepcopy(registry); r=review_s(bad,'CS01'); r['source_integrity_state']='SOURCE_INTERNAL_TYPO'; r['diagnostic_use']='PARTIAL'; r['learner_use_statement']='Corrected learner-use statement.'; redigest_registry(bad)
expect_error('SOURCE_TYPO_SILENTLY_CORRECTED',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# Explicit repair path is legal only with provenance-bound QC event.
good=copy.deepcopy(registry); good_qc=copy.deepcopy(qc); r=review_s(good,'CS01'); r['source_integrity_state']='SOURCE_INTERNAL_TYPO'; r['diagnostic_use']='PARTIAL'; r['learner_use_statement']='Corrected learner-use statement.'; r['qc_event_ref']='QC-CS01-001'
good_qc['events'].append({'event_id':'QC-CS01-001','target_ref':'CS01','event_type':'SOURCE_TYPO_REPAIR','source_before':r['source_asserted_text'],'learner_use_after':r['learner_use_statement'],'rationale':'Explicit synthetic correction used to prove QC-event custody.','evidence_locator':'fixture:review:P02','scope_changed':False,'review_class':'AI_ASSISTED_REFERENCE_REVIEW','human_chemistry_expert_review':False,'confidence':0.99,'event_digest':''})
redigest_registry(good); redigest_qc(good_qc)
repaired=build_review(copy.deepcopy(sources),copy.deepcopy(questions),good,copy.deepcopy(policy),good_qc)
assert next(x for x in repaired['source_reviews'] if x['source_unit_ref']=='CS01')['source_asserted_text']==sources['units'][0]['statement']

# 2 OCR_FORMULA_AMBIGUITY_SILENTLY_NORMALIZED
bad=copy.deepcopy(registry); r=review_s(bad,'CS06'); r['source_integrity_state']='TYPOGRAPHIC_OR_OCR_AMBIGUITY'; r['diagnostic_use']='EXCLUDE_FROM_NEGATIVE_INFERENCE'; r['rendered_source_inspection']='UNRESOLVED'; r['learner_use_statement']='Normalized charge text without inspection.'; redigest_registry(bad)
expect_error('OCR_FORMULA_AMBIGUITY_SILENTLY_NORMALIZED',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 3 IONIC_CHARGE_AMBIGUITY_USED_AS_CONFIDENT_EVIDENCE
bad=copy.deepcopy(registry); r=review_q(bad,'CQ06'); r['source_integrity_state']='FORMULA_OR_CHARGE_AMBIGUITY'; r['diagnostic_use']='FULL'; r['rendered_source_inspection']='CONFIRMED'; redigest_registry(bad)
expect_error('IONIC_CHARGE_AMBIGUITY_USED_AS_CONFIDENT_EVIDENCE',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 4 UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS
bad=copy.deepcopy(registry); r=review_q(bad,'CQ05'); r['validity_state']='UNDERDETERMINED'; r['diagnostic_use']='FULL'; r['canonical_answer']['uniqueness_status']='NON_UNIQUE'; r['canonical_answer']['answer_conditions']=['insufficient condition to choose one conclusion']; redigest_registry(bad)
expect_error('UNDERDETERMINED_ITEM_CAUSES_NEGATIVE_DIAGNOSIS',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 5 MISSING_STRUCTURE_SILENTLY_INVENTED
bad=copy.deepcopy(registry); r=review_q(bad,'CQ08'); r['source_integrity_state']='TRUNCATED_OR_MISSING_STRUCTURE_OR_FIGURE'; r['validity_state']='REVIEW_REQUIRED'; r['diagnostic_use']='EXCLUDE_FROM_NEGATIVE_INFERENCE'; r['missing_or_damaged_representation']=True; r['rendered_source_inspection']='UNRESOLVED'; r['replacement_representation_invented']=True; redigest_registry(bad)
expect_error('MISSING_STRUCTURE_SILENTLY_INVENTED',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 6 CONDITION_SENSITIVE_ITEM_LOSES_CONDITION
bad=copy.deepcopy(registry); r=review_q(bad,'CQ07'); r['required_conditions']=[]; redigest_registry(bad)
expect_error('CONDITION_SENSITIVE_ITEM_LOSES_CONDITION',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 7 SOURCE_KEY_OVERRIDES_CANONICAL_CHEMISTRY
qbad=copy.deepcopy(questions); q1=next(x for x in qbad['questions'] if x['question_id']=='CQ01'); q1['answer_key']='O1'; q1['source_provenance']['source_digest']=intake_digest(q_payload(q1)); qbad['question_set_digest']=intake_digest(qbad,'question_set_digest','questions','question_id')
rbad=copy.deepcopy(registry); r1=review_q(rbad,'CQ01'); r1['source_asserted_answer']='O1'; r1['source_question_digest']=q1['source_provenance']['source_digest']; redigest_registry(rbad)
expect_error('SOURCE_KEY_OVERRIDES_CANONICAL_CHEMISTRY',lambda:build_review(copy.deepcopy(sources),qbad,rbad,copy.deepcopy(policy),copy.deepcopy(qc)))
r1['validity_state']='KEY_ERROR'; r1['diagnostic_use']='PARTIAL'; redigest_registry(rbad)
key_bundle=build_review(copy.deepcopy(sources),qbad,rbad,copy.deepcopy(policy),copy.deepcopy(qc)); key_q1={x['item_ref']:x for x in key_bundle['question_reviews']}['CQ01']
assert key_q1['source_key_status']=='MISMATCH' and key_q1['canonical_answer']['accepted_option_ids']==['O2'] and key_q1['diagnostic_constraints']['negative_inference_allowed'] is False

# 8 DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR
bad=copy.deepcopy(registry); r=review_q(bad,'CQ05'); r['validity_state']='CHEMICAL_DOMAIN_ISSUE'; r['diagnostic_use']='PARTIAL'; redigest_registry(bad)
expect_error('DOMAIN_DEFECT_REWRITTEN_AS_LEARNER_ERROR',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 9 REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS
bad=copy.deepcopy(registry); r=review_q(bad,'CQ05'); r['validity_state']='REVIEW_REQUIRED'; r['diagnostic_use']='FULL'; redigest_registry(bad)
expect_error('REVIEW_REQUIRED_USED_AS_CONFIDENT_DIAGNOSIS',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 10 ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS
bad=copy.deepcopy(registry); bad['learner_diagnosis']={'invented':True}; redigest_registry(bad)
expect_error('ITEM_REVIEW_RUNS_AFTER_DIAGNOSIS',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

# 11 QC_REPAIR_SILENTLY_EXPANDS_SCOPE
bad=copy.deepcopy(good_qc); bad['events'][0]['scope_changed']=True; redigest_qc(bad)
expect_error('QC_REPAIR_SILENTLY_EXPANDS_SCOPE',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),good,copy.deepcopy(policy),bad))

# Extra coverage/provenance gates.
bad=copy.deepcopy(registry); bad['question_reviews']=[x for x in bad['question_reviews'] if x['item_ref']!='CQ14.b']; redigest_registry(bad)
expect_error('ITEM_REVIEW_COVERAGE_GAP',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))
bad=copy.deepcopy(registry); review_s(bad,'CS03')['source_digest']='0'*64; redigest_registry(bad)
expect_error('SOURCE_REVIEW_SOURCE_DRIFT',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))
bad=copy.deepcopy(registry); r=review_q(bad,'CQ05'); r['validity_state']='VALID_MULTIPLE_INTERPRETATIONS'; r['diagnostic_use']='PARTIAL'; r['canonical_interpretations']=['only one interpretation retained']; redigest_registry(bad)
expect_error('MULTIPLE_INTERPRETATIONS_FORCED_TO_ONE',lambda:build_review(copy.deepcopy(sources),copy.deepcopy(questions),bad,copy.deepcopy(policy),copy.deepcopy(qc)))

again=build_review(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(registry),copy.deepcopy(policy),copy.deepcopy(qc))
assert json.dumps(bundle,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-B required falsifiers = 11 PASS')
print('CHEMISTRY C-B extra coverage/provenance falsifiers = 3 PASS')
print('CHEMISTRY C-B explicit QC repair path = PASS')
print('CHEMISTRY C-B deterministic replay = PASS')
