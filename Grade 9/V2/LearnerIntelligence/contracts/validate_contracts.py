#!/usr/bin/env python3
from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parent
for path in sorted(ROOT.glob('*.schema.json')):
    Draft202012Validator.check_schema(json.loads(path.read_text(encoding='utf-8')))
print('V2_LEARNER_INTELLIGENCE_SCHEMA_VALIDITY = PASS')
