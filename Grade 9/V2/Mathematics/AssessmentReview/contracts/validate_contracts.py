#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parents[1]
C = D / "contracts"
MATH = D.parent
sys.path.insert(0, str(D / "engine"))
from review_math_assessment import build_review  # noqa: E402

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

schemas = {
    name: load(C / name)
    for name in [
        "assessment-item-review.schema.json",
        "assessment-item-validity-registry.schema.json",
        "diagnostic-use-policy.schema.json",
        "assessment-review-bundle.schema.json",
    ]
}
store = {schema["$id"]: schema for schema in schemas.values()}

def validate(name, value):
    schema = schemas[name]
    resolver = RefResolver.from_schema(schema, store=store)
    errors = sorted(Draft202012Validator(schema, resolver=resolver).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        for err in errors:
            print(f"{name}: {list(err.path)}: {err.message}")
        raise SystemExit(1)

registry = load(D / "registry" / "assessment-item-validity-registry.json")
policy = load(D / "policies" / "diagnostic-use-policy.json")
questions = load(MATH / "AssessmentIntake" / "fixtures" / "mixed-grade9-question-set.fixture.json")

validate("assessment-item-validity-registry.schema.json", registry)
validate("diagnostic-use-policy.schema.json", policy)
for review in registry["reviews"]:
    validate("assessment-item-review.schema.json", review)

bundle = build_review(questions, registry, policy)
validate("assessment-review-bundle.schema.json", bundle)

print("MATH M-B contract validation = registry, policy, 17 reviews, bundle PASS")
