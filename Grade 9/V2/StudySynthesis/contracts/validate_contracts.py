from pathlib import Path
import importlib.util, json
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"contracts"; F=ROOT/"fixtures"

schemas={}
for schema_name in ["study-synthesis-policy.schema.json","learner-study-model.schema.json","study-synthesis-result.schema.json"]:
    schema=json.loads((C/schema_name).read_text())
    Draft202012Validator.check_schema(schema)
    schemas[schema_name]=schema

policy=json.loads((F/"study_synthesis_policy.synthetic.json").read_text())
Draft202012Validator(schemas["study-synthesis-policy.schema.json"]).validate(policy)

spec=importlib.util.spec_from_file_location("synth",ROOT/"engine"/"synthesize_study_model.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
d=m.load_inputs(F)
out=m.synthesize(d["goal"],d["scope"],d["cks"],d["view"],d["policy"])
assert out["status"]=="PASS"
Draft202012Validator(schemas["learner-study-model.schema.json"]).validate(out["learner_study_model"])
assert out["gaps"]==[]
assert set(out["input_identity"])=={"goal_ref","canonical_target_scope_ref","canonical_knowledge_set_ref","research_learner_view_ref","policy_version"}
print("V2-04 contract validation: PASS")
