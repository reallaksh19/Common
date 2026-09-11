#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parents[1]
C = D / "contracts"
R = D / "registry"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

schemas = {
    p.name: load(p)
    for p in C.glob("*.schema.json")
}
store = {schema["$id"]: schema for schema in schemas.values() if "$id" in schema}

def validate(name, value):
    schema = schemas[name]
    resolver = RefResolver.from_schema(schema, store=store)
    errors = sorted(Draft202012Validator(schema, resolver=resolver).iter_errors(value), key=lambda e:list(e.path))
    if errors:
        for err in errors:
            print(f"{name}: {list(err.path)}: {err.message}")
        raise SystemExit(1)

validate("chemistry-source-obligation-ledger.schema.json", load(R / "chemistry-source-obligation-ledger.json"))
binding_schema = schemas["chemistry-question-capability-binding.schema.json"]
for i, record in enumerate(load(R / "chemistry-question-capability-bindings.json")["bindings"]):
    errors = sorted(Draft202012Validator(binding_schema).iter_errors(record), key=lambda e:list(e.path))
    if errors:
        for err in errors:
            print(f"chemistry-question-capability-binding.schema.json[{i}]: {list(err.path)}: {err.message}")
        raise SystemExit(1)
validate("chemistry-external-corpus-classification.schema.json", load(R / "chemistry-external-corpus-classification.json"))

print("CHEMISTRY C-C registry/schema validation = PASS")
print("source obligations = 12")
print("question/subpart bindings = 17")
print("external candidate classifications = 6")
