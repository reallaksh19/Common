#!/usr/bin/env python3
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from evaluate_math_mature_gate import load, validate_policy, validate_candidate, schema
from build_math_exact_candidate import build_fixture_binding

for name in [
    "math-exact-candidate-binding.schema.json",
    "math-exact-review-receipt.schema.json",
    "math-mature-gate-decision.schema.json",
]:
    Draft202012Validator.check_schema(schema(name))

policy=load(ROOT/"registry"/"math-mature-quality-policy.json")
validate_policy(policy)
candidate=build_fixture_binding("A")
validate_candidate(candidate)
assert candidate["candidate_class"]=="SEMANTIC_COLD_START_EXACT_PACKAGE"
assert candidate["materialization_state"]=="BLOCKED_UPSTREAM_PCK"
assert candidate["artifact_set_digest"] is None
assert candidate["upstream_blockers"]
print("MATH M-L contracts + quality policy + current exact semantic binding PASS")
