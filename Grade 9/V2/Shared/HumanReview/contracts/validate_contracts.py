#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parent
for p in sorted(ROOT.glob('*.schema.json')):
    obj=json.loads(p.read_text())
    Draft202012Validator.check_schema(obj)
print('V2 shared human-review contracts = PASS')
