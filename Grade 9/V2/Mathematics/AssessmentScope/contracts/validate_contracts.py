#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parent
ROOT = D.parent

SCHEMAS = [
    "math-question-capability-binding.schema.json",
    "scope-reconciliation.schema.json",
    "math-assessment-scope-model.schema.json",
    "math-assessment-coverage-matrix.schema.json",
    "math-prerequisite-closure.schema.json",
]

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

for name in SCHEMAS:
    schema = load(D / name)
    Draft202012Validator.check_schema(schema)

pairs = [
    ("math-question-capability-binding.schema.json", ROOT / "registry" / "mixed-grade9-question-scope-bindings.json"),
]
for schema_name, instance_path in pairs:
    Draft202012Validator(load(D / schema_name)).validate(load(instance_path))

print(f"MATH M-C contract validation PASS ({len(SCHEMAS)} schemas, {len(pairs)} static artifacts)")
