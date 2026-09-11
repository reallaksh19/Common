#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

D=Path(__file__).resolve().parents[1]
V2=D.parent.parent
SHARED=V2/"Shared"/"LearnerIntelligence"/"contracts"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canonical(o): return json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest_without_field(o,field,sort_array=None,key=None):
    x=json.loads(json.dumps(o))
    x.pop(field,None)
    if sort_array and key: x[sort_array]=sorted(x[sort_array],key=lambda r:r[key])
    return hashlib.sha256(canonical(x)).hexdigest()

shared=[
    SHARED/"learner-evidence-ledger.schema.json",
    SHARED/"diagnostic-case.schema.json",
    SHARED/"learner-state-snapshot.schema.json",
]
for p in shared:
    Draft202012Validator.check_schema(load(p))
local=D/"contracts"/"physics-reasoning-observation.schema.json"
Draft202012Validator.check_schema(load(local))

registry=load(D/"registry"/"physics-observation-code-registry.json")
assert registry["registry_digest"]==digest_without_field(registry,"registry_digest")
required={
"CORRECT_SYSTEM_SELECTION","CORRECT_REFERENCE_FRAME","CORRECT_MODEL_SELECTION","CORRECT_RELATION_SELECTION",
"CORRECT_STATE_EXTRACTION","CORRECT_REPRESENTATION_TRANSLATION","INVALID_STATE_RESET","OMITTED_PHASE_HANDOFF",
"SIGN_DIRECTION_MISMATCH","DISTANCE_DISPLACEMENT_CONFUSION","GRAPH_HEIGHT_SLOPE_AREA_CONFUSION",
"APEX_COMPONENT_AMBIGUITY","ARITHMETIC_EXECUTION_ERROR","MODEL_VALIDITY_IGNORED",
"VERIFICATION_NOT_PERFORMED","VERIFICATION_FAILED"}
assert {x["code"] for x in registry["codes"]}==required

policy=load(D/"registry"/"physics-diagnostic-policy.json")
assert policy["policy_digest"]==digest_without_field(policy,"policy_digest")
assert policy["benchmark_inputs"]==[]
assert policy["confirmed_misconception_min_independent_negative_evidence"]>=2

ledger=load(D/"fixtures"/"physics-learner-evidence-ledger.fixture.json")
Draft202012Validator(load(SHARED/"learner-evidence-ledger.schema.json")).validate(ledger)
assert ledger["ledger_digest"]==digest_without_field(ledger,"ledger_digest","observations","observation_id")
obs_validator=Draft202012Validator(load(local))
for obs in ledger["observations"]: obs_validator.validate(obs)

print("PHYSICS P-E shared/local contract validation = PASS")
