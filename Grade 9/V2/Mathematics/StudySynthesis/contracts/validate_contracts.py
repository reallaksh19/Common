#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from synthesize_math_study_model import synthesize

def load(p): return json.loads(p.read_text(encoding="utf-8"))
policy=load(ROOT/"fixtures/policy.synthetic.json")
Draft202012Validator(load(Path(__file__).with_name("math-study-synthesis-policy.schema.json"))).validate(policy)
model=synthesize(ROOT/"fixtures")
if model.get("status")=="BLOCKED": raise SystemExit(model)
Draft202012Validator(load(Path(__file__).with_name("math-learner-study-model.schema.json"))).validate(model)
expected=load(ROOT/"fixtures/expected_study_model.synthetic.json")
assert model==expected, "generated StudyModel drift"
print("MATH-V2-03 contract validation: PASS")
