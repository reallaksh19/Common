#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())
def validate(data,name): Draft202012Validator(load(ROOT/'contracts'/name)).validate(data)
validate(load(ROOT/'fixtures/current_candidate_binding.json'),'candidate-validation-binding.schema.json')
validate(load(ROOT/'fixtures/candidate_binding.test-only.json'),'candidate-validation-binding.schema.json')
validate(load(ROOT/'fixtures/synthetic_reference.test-only.json'),'mature-math-reference.schema.json')
rubric=load(ROOT/'fixtures/validation_rubric.json')
assert rubric['authority']=='COMPARATIVE_VALIDATION_ONLY' and rubric['producer_template'] is False and len(rubric['dimensions'])==11
sys.path.insert(0,str(ROOT/'engine'))
from check_eligibility import check_eligibility
from compare_synthetic import build_result
current=check_eligibility(load(ROOT/'fixtures/current_candidate_binding.json'),load(ROOT/'fixtures/quality_review_summary.pending.json'))
validate(current,'comparative-validation-eligibility.schema.json')
assert current['status']=='BLOCKED_HUMAN_QUALITY_GATES'
test=build_result(load(ROOT/'fixtures/candidate_binding.test-only.json'),load(ROOT/'fixtures/quality_review_summary.test-only-pass.json'),load(ROOT/'fixtures/synthetic_reference.test-only.json'),rubric)
gap_schema=load(ROOT/'contracts/validation-gap.schema.json')
registry=Registry().with_resource('validation-gap.schema.json',Resource.from_contents(gap_schema))
Draft202012Validator(load(ROOT/'contracts/comparative-validation-result.schema.json'),registry=registry).validate(test)
print('MATH-V2-07 validation contracts = PASS')
