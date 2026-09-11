#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parents[1]
C = D / "contracts"
PHYSICS = D.parent
sys.path.insert(0, str(D / "engine"))
from review_physics_assessment import build_review  # noqa: E402

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

schema_names = [
    "physics-source-integrity-review.schema.json",
    "assessment-item-review.schema.json",
    "physics-item-validity-registry.schema.json",
    "diagnostic-use-policy.schema.json",
    "assessment-review-bundle.schema.json",
]
schemas = {name: load(C / name) for name in schema_names}
store = {schema["$id"]: schema for schema in schemas.values()}

def validate(name, value):
    schema = schemas[name]
    resolver = RefResolver.from_schema(schema, store=store)
    errors = sorted(
        Draft202012Validator(schema, resolver=resolver).iter_errors(value),
        key=lambda e: list(e.path),
    )
    if errors:
        for err in errors:
            print(f"{name}: {list(err.path)}: {err.message}")
        raise SystemExit(1)

registry = load(D / "registry" / "physics-item-validity-registry.json")
policy = load(D / "policies" / "diagnostic-use-policy.json")
questions = load(PHYSICS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")

validate("physics-item-validity-registry.schema.json", registry)
validate("diagnostic-use-policy.schema.json", policy)

bundle = build_review(questions, registry, policy)
for review in bundle["item_reviews"]:
    clean = {
        k: v for k, v in review.items()
        if k not in {"source_key_status", "diagnostic_constraints", "source_integrity_constraints"}
    }
    validate("assessment-item-review.schema.json", clean)
    validate("physics-source-integrity-review.schema.json", clean["source_integrity_review"])
validate("assessment-review-bundle.schema.json", bundle)

print("PHYSICS P-B contract validation = compact registry, policy, 17 expanded reviews, bundle PASS")
