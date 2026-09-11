#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parent
for p in D.glob('*.schema.json'):
    Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')))
print('MATH M-J contracts valid')
