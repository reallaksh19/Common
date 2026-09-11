#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parents[1]
PHYSICS = D.parent
C = D / "contracts"
sys.path.insert(0, str(D / "engine"))
from reconcile_physics_assessment_scope import reconcile  # noqa: E402

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

schema_names = [
    "scope-reconciliation.schema.json",
    "physics-assessment-scope-model.schema.json",
    "physics-assessment-coverage-matrix.schema.json",
    "physics-question-capability-binding.schema.json",
    "physics-prerequisite-model-closure.schema.json",
]
schemas = {name: load(C / name) for name in schema_names}
store = {schema["$id"]: schema for schema in schemas.values()}

def validate(name, value):
    schema = schemas[name]
    resolver = RefResolver.from_schema(schema, store=store)
    errors = sorted(Draft202012Validator(schema, resolver=resolver).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            print(f"{name}: {list(err.path)}: {err.message}")
        raise SystemExit(1)

questions = load(PHYSICS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
topic_scope = load(PHYSICS / "AssessmentIntake" / "fixtures" / "motion-topic-scope.fixture.json")
review_registry = load(PHYSICS / "AssessmentReview" / "registry" / "physics-item-validity-registry.json")
review_policy = load(PHYSICS / "AssessmentReview" / "policies" / "diagnostic-use-policy.json")
canonical_caps = load(PHYSICS / "Canonical" / "registry" / "capabilities.json")
authority = load(D / "authority" / "physics-assessment-scope-authority.json")
bindings = load(D / "registry" / "motion-question-scope-bindings.json")

for binding in bindings["bindings"]:
    validate("physics-question-capability-binding.schema.json", binding)
model, coverage, report, prereq = reconcile(
    questions, topic_scope, review_registry, review_policy, canonical_caps, authority, bindings
)
validate("physics-assessment-scope-model.schema.json", model)
validate("physics-assessment-coverage-matrix.schema.json", coverage)
validate("scope-reconciliation.schema.json", report)
validate("physics-prerequisite-model-closure.schema.json", prereq)
assert len(coverage["rows"]) == 17 and coverage["coverage_complete"] is True
assert model["attempt_data_consumed"] is False and report["attempt_data_consumed"] is False
print("PHYSICS P-C contract validation = bindings + 4 generated authorities PASS")
