#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(MATH / "LearnerIntelligence/engine"))
from synthesize_math_study_model import build_study_scope, synthesize
from derive_math_learner_state import derive as derive_learner_state


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


scope_schema = load(Path(__file__).parent / "math-learner-study-scope.schema.json")
model_schema = load(Path(__file__).parent / "math-learner-study-model.schema.json")
Draft202012Validator.check_schema(scope_schema)
Draft202012Validator.check_schema(model_schema)

questions = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json")
attempts = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-attempt-set.fixture.json")
reviews = load(MATH / "AssessmentReview/registry/assessment-item-validity-registry.json")
authority = load(MATH / "AssessmentScope/authority/math-assessment-scope-authority.json")
bindings = load(MATH / "AssessmentScope/registry/mixed-grade9-question-scope-bindings.json")
item_semantics = load(MATH / "ProblemSemantics/registry/mixed-grade9-item-semantics.json")
obs_registry = load(MATH / "LearnerIntelligence/registry/math-observation-type-registry.json")
reviewed = load(MATH / "LearnerIntelligence/fixtures/reviewed-observations.fixture.json")
policy = load(ROOT / "policies/math-treatment-policy.json")

present = derive_learner_state(questions, reviews, authority, item_semantics, obs_registry, attempts, reviewed)["learner_state_snapshot"]
absent = derive_learner_state(questions, reviews, authority, item_semantics, obs_registry)["learner_state_snapshot"]
scope = build_study_scope(bindings, authority)
present_model = synthesize(scope, present, policy)
absent_model = synthesize(scope, absent, policy)

Draft202012Validator(scope_schema).validate(scope)
Draft202012Validator(model_schema).validate(present_model)
Draft202012Validator(model_schema).validate(absent_model)
print(f"MATH M-F contracts PASS ({len(scope['capability_scope_records'])} in-scope capability records; present+absent models)")
