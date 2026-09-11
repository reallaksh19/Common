#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parents[1]
C = D / "contracts"
F = D / "fixtures"

schema_names = [
    "assessment-source-provenance.schema.json",
    "assessment-question.schema.json",
    "question-set.schema.json",
    "attempt-set.schema.json",
    "declared-topic-scope.schema.json",
    "assessment-intake-envelope.schema.json",
]
schemas = {name: json.loads((C/name).read_text(encoding="utf-8")) for name in schema_names}
store = {schema["$id"]: schema for schema in schemas.values()}

def validate(instance_name, schema_name):
    instance = json.loads((F/instance_name).read_text(encoding="utf-8"))
    schema = schemas[schema_name]
    resolver = RefResolver.from_schema(schema, store=store)
    Draft202012Validator(schema, resolver=resolver).validate(instance)

validate("mixed-grade9-question-set.fixture.json", "question-set.schema.json")
validate("mixed-grade9-topic-scope.fixture.json", "declared-topic-scope.schema.json")
validate("mixed-grade9-attempt-set.fixture.json", "attempt-set.schema.json")
validate("math-assessment-intake.example.json", "assessment-intake-envelope.schema.json")

print("MATH M-A contract validation = 4 fixtures PASS")
