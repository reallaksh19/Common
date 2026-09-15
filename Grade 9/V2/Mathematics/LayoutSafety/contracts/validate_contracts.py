#!/usr/bin/env python3
"""Validate the layout-safety contracts.

The rendered object map this phase audits is owned by ``Mathematics/SourceLedger`` — one
object model, audited by both phases (completeness there, readability and collision here) —
so it is validated from its own directory and only referenced from here.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parent
MATH = D.parents[1]

for p in sorted(D.glob("*.schema.json")):
    Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))

shared = MATH / "SourceLedger" / "contracts" / "math-rendered-object-map.schema.json"
if not shared.exists():
    raise SystemExit("LAYOUT_SAFETY_SHARED_OBJECT_MAP_MISSING")
Draft202012Validator.check_schema(json.loads(shared.read_text(encoding="utf-8")))

print("MATH M-UPGRADE-2 layout-safety contracts valid")
