#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())
def val(data,schema): Draft202012Validator(load(ROOT/'contracts'/schema)).validate(data)
val(load(ROOT/'fixtures/review_policy.synthetic.json'),'review-policy.schema.json')
for f in load(ROOT/'fixtures/ai_pre_review_findings.synthetic.json')['findings']: val(f,'review-finding.schema.json')
for d in load(ROOT/'fixtures/revision_plan.synthetic.json')['decisions']: val(d,'revision-decision.schema.json')
print('MATH-V2-06 review contracts = PASS')
