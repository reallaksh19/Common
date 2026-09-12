#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/"engine"))
sys.path.insert(0,str(ROOT/"runtime"))
from design_learning import build_design
from select_support import select_support, validate_selection

schemas={}
for p in HERE.glob("*.schema.json"):
    schemas[p.name]=json.loads(p.read_text())
store={s.get("$id",name):s for name,s in schemas.items()}
for s in schemas.values():
    Draft202012Validator.check_schema(s)

def validate(schema_name,obj):
    schema=schemas[schema_name]
    resolver=RefResolver.from_schema(schema,store=store)
    Draft202012Validator(schema,resolver=resolver,format_checker=Draft202012Validator.FORMAT_CHECKER).validate(obj)

def load(name):
    return json.loads((ROOT/"fixtures"/name).read_text())

policy=load("learning_design_policy.synthetic.json")
state=load("interaction_support_state.synthetic.json")
study=load("learner_study_model.synthetic.json")
view=load("publication_planning_view.synthetic.json")
target=load("publication_target.synthetic.json")

validate("learning-design-policy.schema.json",policy)
validate("interaction-support-state.schema.json",state)
result=build_design(study,view,target,policy)
validate("learning-design-result.schema.json",result)
assert result["status"]=="READY"
plan=result["learning_design_plan"]
validate("learning-design-plan.schema.json",plan)
selection=select_support(plan,state)
validate_selection(plan,selection)
validate("support-selection.schema.json",selection)
print("V2-05 contract + generated artifact validation: PASS")
