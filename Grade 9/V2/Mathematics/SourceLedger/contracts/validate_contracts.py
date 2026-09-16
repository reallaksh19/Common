#!/usr/bin/env python3
import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parent
store = {}
for p in sorted(D.glob("*.schema.json")):
    doc = json.loads(p.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(doc)
    store[doc["$id"]] = doc

for schema_id in sorted(store):
    root = store[schema_id]
    Draft202012Validator(root, resolver=RefResolver.from_schema(root, store=store))

print(f"MATH M-UPGRADE-2 source-ledger contracts valid ({len(store)} schemas)")
