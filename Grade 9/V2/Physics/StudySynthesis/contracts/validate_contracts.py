#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
PHYS=ROOT.parent
CONTRACTS=ROOT/'contracts'
sys.path[:0]=[
    str(ROOT/'engine'),
    str(PHYS/'LearnerEvidence'/'engine'),
    str(PHYS/'ProblemSemantics'/'engine'),
]
from build_physics_learner_study_model import derive_study_scope, build_model, load, digest
from infer_physics_learner_evidence import build_snapshot
from build_physics_problem_semantics import build_package

for p in sorted(CONTRACTS.glob('*.schema.json')):
    Draft202012Validator.check_schema(load(p))

Q=load(PHYS/'AssessmentIntake/fixtures/motion-question-set.fixture.json')
TOPIC=load(PHYS/'AssessmentIntake/fixtures/motion-topic-scope.fixture.json')
REVIEW=load(PHYS/'AssessmentReview/registry/physics-item-validity-registry.json')
REVIEW_POLICY=load(PHYS/'AssessmentReview/policies/diagnostic-use-policy.json')
CANON=load(PHYS/'Canonical/registry/capabilities.json')
AUTH=load(PHYS/'AssessmentScope/authority/physics-assessment-scope-authority.json')
BIND=load(PHYS/'AssessmentScope/registry/motion-question-scope-bindings.json')
PD=PHYS/'ProblemSemantics'
PKG=build_package(
    Q,TOPIC,REVIEW,REVIEW_POLICY,CANON,AUTH,BIND,
    load(PD/'registry/physics-reasoning-role-registry.json'),
    load(PD/'registry/physics-problem-family-registry.json'),
    load(PD/'registry/physics-verification-route-registry.json'),
    load(PD/'registry/motion-item-semantics.json'),
    load(PD/'registry/guide-demand-badge-policy.json'),
)
PE=PHYS/'LearnerEvidence'
PE_REG=load(PE/'registry/physics-observation-code-registry.json')
PE_POLICY=load(PE/'registry/physics-diagnostic-policy.json')
ATT=load(PHYS/'AssessmentIntake/fixtures/motion-attempt-set.fixture.json')
LED=load(PE/'fixtures/physics-learner-evidence-ledger.fixture.json')
POLICY=load(ROOT/'policies/physics-treatment-policy.json')

Draft202012Validator(load(CONTRACTS/'physics-treatment-policy.schema.json')).validate(POLICY)
assert POLICY['policy_digest']==digest(POLICY,'policy_digest')

scope=derive_study_scope(copy.deepcopy(BIND),copy.deepcopy(AUTH),copy.deepcopy(PKG))
no_bundle=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(PE_REG),copy.deepcopy(PE_POLICY))
attempt_bundle=build_snapshot(copy.deepcopy(PKG),copy.deepcopy(Q),copy.deepcopy(PE_REG),copy.deepcopy(PE_POLICY),copy.deepcopy(ATT),copy.deepcopy(LED))
no_model=build_model(copy.deepcopy(scope),copy.deepcopy(no_bundle),copy.deepcopy(POLICY))
attempt_model=build_model(copy.deepcopy(scope),copy.deepcopy(attempt_bundle),copy.deepcopy(POLICY))

Draft202012Validator(load(CONTRACTS/'physics-learner-study-scope.schema.json')).validate(scope)
model_validator=Draft202012Validator(load(CONTRACTS/'physics-learner-study-model.schema.json'))
model_validator.validate(no_model)
model_validator.validate(attempt_model)
assert no_model['study_scope_digest']==attempt_model['study_scope_digest']==scope['study_scope_digest']
assert no_model['learner_attempt_mode']=='ABSENT' and attempt_model['learner_attempt_mode']=='PRESENT'

example=load(ROOT/'examples/physics-longitudinal-binding.example.json')
assert example['subject']=='PHYSICS' and example['fixture_class']=='PUBLIC_SYNTHETIC'
assert example['invariant']=='CURRENT_SUCCESS_DOES_NOT_CLOSE_DELAYED_OR_TRANSFER_OBLIGATIONS'
assert example['dimensions']['delayed_retention']=='OPEN' and example['dimensions']['far_transfer']=='OPEN'

print('PHYSICS P-F contracts + no-attempt/attempt reference synthesis = PASS')
