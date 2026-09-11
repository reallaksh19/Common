#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads(Path(p).read_text())
sch=load(R/'contracts/review-finding.schema.json')
for f in load(R/'fixtures/ai_pre_review_findings.synthetic.json'):
    Draft202012Validator(sch).validate(f)
print('PHY-V2-06 review contracts/fixtures = PASS')
