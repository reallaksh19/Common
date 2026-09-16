#!/usr/bin/env python3
"""Validate the learner-realization contracts, including the cross-phase $refs.

``math-expression.schema.json`` lives in ``Mathematics/MathTypesetting/contracts`` because
the AST is owned by the typesetting phase; the realization contracts reference it by $id,
so the resolver store spans both directories.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parent
MATH = D.parents[1]
SEARCH = [D, MATH / "MathTypesetting" / "contracts"]

store = {}
for directory in SEARCH:
    for p in sorted(directory.glob("*.schema.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(doc)
        store[doc["$id"]] = doc

for schema_id in ("math-learner-realization.schema.json", "math-route-state.schema.json",
                  "math-answer-custody.schema.json",
                  "math-equivalence-transformation.schema.json"):
    root = store[schema_id]
    resolver = RefResolver.from_schema(root, store=store)
    Draft202012Validator(root, resolver=resolver)

print(f"MATH M-UPGRADE-2 learner-realization contracts valid ({len(store)} schemas resolved)")
