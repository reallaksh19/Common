#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]; CHEM=D.parent
sys.path[:0]=[str(D/'engine'),str(CHEM/'AssessmentReview'/'engine'),str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine'),str(CHEM/'LearnerEvidence'/'engine')]
from build_chemistry_learner_study_model import derive_study_scope,build_model,validate_model,digest
from review_chemistry_assessment import build_review,load_registry as load_review_registry
from build_chemistry_scope import build_scope
from build_chemistry_reasoning_semantics import build_semantics
from infer_chemistry_learner_evidence import build_snapshot

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError('expected '+code)
def redigest(m): m['study_model_digest']=''; m['study_model_digest']=digest(m,'study_model_digest'); return m
def rec(m,c): return next(x for x in m['capability_records'] if x['capability_ref']==c)
def lon(m,c): return next(x for x in m['longitudinal_initializations'] if x['capability_ref']==c)

def coverage_signature(m):
    return {r['capability_ref']:(tuple(r['source_obligation_refs']),tuple(r['assessment_question_refs']),tuple(r['external_candidate_refs']),tuple(r['prerequisite_refs']),tuple(r['representation_level_obligations']),tuple(r['condition_exception_obligations']),tuple(r['conservation_obligations'])) for r in m['capability_records']}

A=CHEM/'AssessmentIntake'/'fixtures'; R=CHEM/'AssessmentReview'; S=CHEM/'AssessmentScope'; RS=CHEM/'ReasoningSemantics'; E=CHEM/'LearnerEvidence'
sources=load(A/'mixed-chemistry-source.fixture.json'); questions=load(A/'mixed-chemistry-question-set.fixture.json'); corpus=load(A/'mixed-chemistry-external-corpus.fixture.json'); topic=load(A/'mixed-chemistry-topic-scope.fixture.json')
review_reg,manifest_digest=load_review_registry(R/'registry'/'chemistry-item-validity-registry.json')
review=build_review(copy.deepcopy(sources),copy.deepcopy(questions),review_reg,load(R/'policies'/'chemistry-diagnostic-use-policy.json'),load(R/'registry'/'chemistry-qc-events.json'),registry_manifest_digest=manifest_digest)
source_ledger=load(S/'registry'/'chemistry-source-obligation-ledger.json'); qbindings=load(S/'registry'/'chemistry-question-capability-bindings.json'); external=load(S/'registry'/'chemistry-external-corpus-classification.json'); authority=load(S/'authority'/'chemistry-canonical-authority.json')
scope_bundle=build_scope(copy.deepcopy(sources),copy.deepcopy(questions),copy.deepcopy(corpus),copy.deepcopy(topic),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(authority))
semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),load(RS/'registry'/'chemistry-problem-family-registry.json'),load(RS/'registry'/'chemistry-reasoning-role-registry.json'),load(RS/'registry'/'chemistry-guide-demand-badge-policy.json'))
obs=load(E/'registry'/'chemistry-observation-code-registry.json'); diag_policy=load(E/'registry'/'chemistry-diagnostic-policy.json'); attempts=load(E/'fixtures'/'chemistry-diagnostic-attempt-set.fixture.json'); evidence=load(E/'fixtures'/'chemistry-learner-evidence-ledger.fixture.json'); treatment=load(D/'registry'/'chemistry-treatment-policy.json')
no_attempt=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(obs),copy.deepcopy(diag_policy))
with_attempt=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(questions),copy.deepcopy(obs),copy.deepcopy(diag_policy),copy.deepcopy(attempts),copy.deepcopy(evidence))
study_scope_a=derive_study_scope(copy.deepcopy(scope_bundle),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
study_scope_b=derive_study_scope(copy.deepcopy(scope_bundle),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
assert study_scope_a==study_scope_b
assert study_scope_a['required_source_obligation_refs']==sorted([r['obligation_id'] for r in source_ledger['obligations'] if r['scope_status']=='ELIGIBLE_IN_SCOPE'])
assert study_scope_a['required_assessment_question_refs']==sorted([r['item_ref'] for r in qbindings['bindings'] if r['scope_status']=='ELIGIBLE_IN_SCOPE'])
assert study_scope_a['required_external_candidate_refs']==['EXT01','EXT02','EXT03','EXT04','EXT05'] and study_scope_a['excluded_external_candidate_refs']==['EXT06']
model_a=build_model(copy.deepcopy(study_scope_a),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(no_attempt),copy.deepcopy(treatment),'CHEM-C-F-MODEL-NO-ATTEMPT')
model_b=build_model(copy.deepcopy(study_scope_b),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(with_attempt),copy.deepcopy(treatment),'CHEM-C-F-MODEL-WITH-ATTEMPT')
assert model_a['study_scope_digest']==model_b['study_scope_digest']
assert coverage_signature(model_a)==coverage_signature(model_b)
assert not any(r['treatment'] in {'REPAIR_BEFORE','REPAIR_IN_UNIT'} for r in model_a['capability_records'])
assert rec(model_b,'CAP-PARSE-ION-CHARGE')['treatment']=='READY_VERIFY_ONLY'
assert any(r['treatment']=='PROBE_FIRST' for r in model_b['capability_records'])

# Contract validation of actual outputs.
Draft202012Validator(load(D/'contracts'/'chemistry-learner-study-scope.schema.json')).validate(study_scope_a)
Draft202012Validator(load(D/'contracts'/'chemistry-learner-study-model.schema.json')).validate(model_a)
Draft202012Validator(load(D/'contracts'/'chemistry-learner-study-model.schema.json')).validate(model_b)

# 1 LEARNER_WEAKNESS_SHRINKS_REQUIRED_SCOPE
bad=copy.deepcopy(model_b); bad['capability_records']=bad['capability_records'][1:]; redigest(bad)
expect('LEARNER_WEAKNESS_SHRINKS_REQUIRED_SCOPE',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 2 OUT_OF_SCOPE_PYQ_EXPANDS_CORE1
bad=copy.deepcopy(model_a); bad['capability_records'][0]['external_candidate_refs'].append('EXT06'); bad['capability_records'][0]['external_candidate_refs'].sort(); redigest(bad)
expect('OUT_OF_SCOPE_PYQ_EXPANDS_CORE1',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 3 READY_CAPABILITY_FULLY_RETAUGHT_FOR_PAGE_DENSITY
bad=copy.deepcopy(model_b); x=rec(bad,'CAP-PARSE-ION-CHARGE'); x['required_pck_jobs']=list(treatment['required_pck_jobs_by_treatment']['ACTIVE_STUDY']); redigest(bad)
expect('READY_CAPABILITY_FULLY_RETAUGHT_FOR_PAGE_DENSITY',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 4 NO_ATTEMPT_FORCES_REPAIR
bad=copy.deepcopy(model_a); x=rec(bad,'CAP-CLASSIFY-CHANGE-EVIDENCE'); x['treatment']='REPAIR_IN_UNIT'; x['required_pck_jobs']=list(treatment['required_pck_jobs_by_treatment']['REPAIR_IN_UNIT']); redigest(bad)
expect('NO_ATTEMPT_FORCES_REPAIR',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 5 ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL
bad=copy.deepcopy(model_b); lon(bad,'CAP-PARSE-ION-CHARGE')['dimensions']['delayed_retention']='CURRENT_EVIDENCE'; redigest(bad)
expect('ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 6 STUDYMODEL_WITHOUT_SOURCE_TRACE
bad=copy.deepcopy(model_a); rec(bad,'CAP-CHECK-RULE-EXCEPTION')['source_obligation_refs']=[]; redigest(bad)
expect('STUDYMODEL_WITHOUT_SOURCE_TRACE',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 7 SOURCE_EXCEPTION_DROPPED_FROM_STUDYMODEL
bad=copy.deepcopy(model_a); rec(bad,'CAP-CHECK-RULE-EXCEPTION')['condition_exception_obligations']=[]; redigest(bad)
expect('SOURCE_EXCEPTION_DROPPED_FROM_STUDYMODEL',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 8 REPRESENTATION_TRANSLATION_DROPPED_FROM_STUDYMODEL
bad=copy.deepcopy(model_a); rec(bad,'CAP-TRANSLATE-PARTICLE-SYMBOL')['representation_level_obligations']=['SYMBOLIC']; redigest(bad)
expect('REPRESENTATION_TRANSLATION_DROPPED_FROM_STUDYMODEL',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 9 CONSERVATION_REQUIREMENT_DROPPED_FROM_STUDYMODEL
bad=copy.deepcopy(model_a); rec(bad,'CAP-CHECK-ATOM-CONSERVATION')['conservation_obligations']=[]; redigest(bad)
expect('CONSERVATION_REQUIREMENT_DROPPED_FROM_STUDYMODEL',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))
# 10 UPSTREAM_CHEMISTRY_STRENGTH_RELABELLED_WEAK_TO_SUPPORT_REPAIR
synthetic=copy.deepcopy(with_attempt); snap=synthetic['snapshot']; snap['diagnostic_cases']=[c for c in snap['diagnostic_cases'] if c['hypothesis_code']!='AGENT_ROLE_INVERSION']
for s in snap['capability_states']:
    if s['capability_ref']=='CAP-TRACK-REACTING-SPECIES': s['state']='DEMONSTRATED'
    if s['capability_ref']=='CAP-ATTACH-SPECIES-ROLE': s['state']='EVIDENCE_OF_DIFFICULTY'
model_c=build_model(copy.deepcopy(study_scope_a),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),synthetic,copy.deepcopy(treatment),'CHEM-C-F-MODEL-SYNTHETIC')
assert rec(model_c,'CAP-TRACK-REACTING-SPECIES')['treatment']=='READY_VERIFY_ONLY'
assert rec(model_c,'CAP-ATTACH-SPECIES-ROLE')['treatment']=='REPAIR_IN_UNIT'
bad=copy.deepcopy(model_c); x=rec(bad,'CAP-TRACK-REACTING-SPECIES'); x['treatment']='REPAIR_BEFORE'; x['required_pck_jobs']=list(treatment['required_pck_jobs_by_treatment']['REPAIR_BEFORE']); redigest(bad)
expect('UPSTREAM_CHEMISTRY_STRENGTH_RELABELLED_WEAK_TO_SUPPORT_REPAIR',lambda:validate_model(bad,study_scope_a,source_ledger,qbindings,external,semantics,treatment))

# Longitudinal obligations remain open even when current evidence is positive.
assert lon(model_b,'CAP-PARSE-ION-CHARGE')['dimensions']['delayed_retention']=='OPEN'
assert lon(model_b,'CAP-PARSE-ION-CHARGE')['dimensions']['far_transfer']=='OPEN'
# Source-authorized Chemistry obligations survive synthesis.
assert 'explicit exception supplied by source' in rec(model_a,'CAP-CHECK-RULE-EXCEPTION')['condition_exception_obligations']
assert {'PARTICULATE','SYMBOLIC'}<=set(rec(model_a,'CAP-TRANSLATE-PARTICLE-SYMBOL')['representation_level_obligations'])
assert 'ATOM_COUNT' in rec(model_a,'CAP-CHECK-ATOM-CONSERVATION')['conservation_obligations']
# Deterministic replay.
again=build_model(copy.deepcopy(study_scope_a),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(with_attempt),copy.deepcopy(treatment),'CHEM-C-F-MODEL-WITH-ATTEMPT')
assert json.dumps(model_b,sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(again,sort_keys=True,separators=(',',':'),ensure_ascii=False)
print('CHEMISTRY C-F required falsifiers = 10 PASS')
print('CHEMISTRY C-F no-attempt / attempt scope invariance = PASS')
print('CHEMISTRY C-F source-condition-representation-conservation closure = PASS')
print('CHEMISTRY C-F longitudinal initialization = PASS')
print('CHEMISTRY C-F deterministic replay = PASS')
