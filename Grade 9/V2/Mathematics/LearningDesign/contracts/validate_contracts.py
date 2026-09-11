#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())

Draft202012Validator(load(D/"contracts/math-learning-design-policy.schema.json")).validate(load(D/"fixtures/policy.synthetic.json"))
Draft202012Validator(load(D/"contracts/interaction-support-state.schema.json")).validate(load(D/"fixtures/interaction_support_state.synthetic.json"))

sys.path.insert(0,str(D/"engine"))
from design_math_learning import build_design, digest_without_field
r=build_design(load(D/"fixtures/learner_study_model.synthetic.json"),
               load(D/"fixtures/publication_planning_view.synthetic.json"),
               load(D/"fixtures/publication_target.synthetic.json"),
               load(D/"fixtures/policy.synthetic.json"))
assert r["status"]=="READY"
plan=r["learning_design_plan"]
Draft202012Validator(load(D/"contracts/math-learning-design-plan.schema.json")).validate(plan)
assert plan["design_digest"]==digest_without_field(plan)

expected=load(D/"fixtures/expected_design.synthetic.json")
actual_modes={x["target_id"]:[x["engagement_mode"],x["readiness_mode"]] for x in plan["target_preservation"]}
assert actual_modes==expected["expected_target_modes"]
step_ids={x["step_id"] for x in plan["steps"]}
assert set(expected["required_step_ids"]) <= step_ids
p01=next(x for x in plan["steps"] if x["step_id"]=="P01")
assert p01["payload"]["probe_ref"]==expected["slope_probe_ref"]
assert any(x["rung_id"]==expected["route_change_rung"] and x["route"]=="ROUTE_CHANGE" for x in plan["support_ladder"])
print("MATH-V2-04 contract + expected-design validation = PASS")
