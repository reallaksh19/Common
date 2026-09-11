#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads(Path(p).read_text())
def schema(name): return load(ROOT/'contracts'/name)
def validate(obj,name): Draft202012Validator(schema(name)).validate(obj)

validate(load(ROOT/'fixtures'/'publication_policy.synthetic.json'),'math-publication-policy.schema.json')
print('MATH-V2-05 contract schemas = PASS')
