#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
for name in ["bxx-projection-policy.schema.json", "core2-learner-input.schema.json"]:
    Draft202012Validator.check_schema(json.loads((ROOT / name).read_text(encoding="utf-8")))

print("LEARNER_INTELLIGENCE_PHASE4_INTEGRATION_SCHEMA_VALIDITY = PASS")
