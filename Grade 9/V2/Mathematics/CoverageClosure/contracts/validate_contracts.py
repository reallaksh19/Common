#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parent
for p in sorted(D.glob('*.schema.json')):
    try:
        schema = json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"INVALID_SCHEMA_JSON:{p.name}:{exc}") from exc
    Draft202012Validator.check_schema(schema)
    print(f"validated {p.name}")
print('MATH M-J contracts valid')
