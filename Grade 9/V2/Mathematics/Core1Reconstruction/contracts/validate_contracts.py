#!/usr/bin/env python3
"""Validate the reconstruction contracts, including cross-phase $refs.

The reconstruction chain embeds item 2's route-state objects, which live in
``Mathematics/LearnerRealization/contracts`` and in turn reference the MathExpression AST in
``Mathematics/MathTypesetting/contracts``. The resolver store therefore spans three phases —
which is itself the point: the chain is built out of the same realization objects, not a
parallel vocabulary.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

D = Path(__file__).resolve().parent
MATH = D.parents[1]
SEARCH = [D,
          MATH / "LearnerRealization" / "contracts",
          MATH / "MathTypesetting" / "contracts"]

store = {}
for directory in SEARCH:
    for p in sorted(directory.glob("*.schema.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(doc)
        store[doc["$id"]] = doc

for schema_id in ("math-core1-reconstruction-chain.schema.json",
                  "math-theorem-direction.schema.json",
                  "math-cross-core-bridge-manifest.schema.json"):
    root = store[schema_id]
    Draft202012Validator(root, resolver=RefResolver.from_schema(root, store=store))

print(f"MATH M-UPGRADE-2 reconstruction contracts valid ({len(store)} schemas resolved)")
