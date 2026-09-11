#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SCHEMAS = [
    "learner-intelligence-common.schema.json",
    "learner-evidence-ledger.schema.json",
    "reasoning-observation.schema.json",
    "diagnostic-case.schema.json",
    "learner-state-snapshot.schema.json",
    "learner-state-view.schema.json",
]

for name in SCHEMAS:
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(data)

print("LEARNER_INTELLIGENCE_PHASE1_SCHEMA_VALIDITY = PASS")
