#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMAS = [
    "capability-definition.schema.json",
    "error-signature.schema.json",
    "diagnostic-probe.schema.json",
    "math-reasoning-contract.schema.json",
    "physics-reasoning-contract.schema.json",
    "chemistry-reasoning-contract.schema.json",
]

for name in SCHEMAS:
    Draft202012Validator.check_schema(json.loads((ROOT / name).read_text(encoding="utf-8")))

print("LEARNER_INTELLIGENCE_PHASE2_SUBJECT_SCHEMA_VALIDITY = PASS")
