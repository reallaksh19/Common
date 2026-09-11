#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())
for p in sorted(Path(__file__).parent.glob('*.schema.json')):
    Draft202012Validator.check_schema(load(p))
for name,schema in [('publication_target.synthetic.json','physics-publication-target.schema.json'),('publication_policy.synthetic.json','physics-publication-policy.schema.json')]:
    Draft202012Validator(load(Path(__file__).parent/schema)).validate(load(ROOT/'fixtures'/name))
print('PHY-V2-05 contract/fixture validation = PASS')
