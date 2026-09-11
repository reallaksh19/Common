#!/usr/bin/env python3
import copy, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
CONTRACTS=ROOT/"contracts"
POL=ROOT/"policies"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def dig(v,field):
    x=copy.deepcopy(v); x.pop(field,None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

for p in sorted(CONTRACTS.glob("*.schema.json")):
    Draft202012Validator.check_schema(load(p))

profile=load(POL/"physics-instructional-authoring-profile.json")
scope=load(POL/"physics-core1-scope-completeness-policy.json")
problem=load(POL/"physics-problem-authoring-profile.json")
assert profile["profile_digest"]==dig(profile,"profile_digest")
assert scope["policy_digest"]==dig(scope,"policy_digest")
assert problem["profile_digest"]==dig(problem,"profile_digest")
assert profile["full_learning_stages"]==[
"PHENOMENON","DEFINE_SYSTEM","CHOOSE_FRAME_SIGN","REPRESENT","NOTICE_DECISIVE_FEATURE",
"ORDINARY_LANGUAGE","CHECK_MODEL_VALIDITY","RECONSTRUCT","MINIMAL_CONTRAST","WORKED_REASONING",
"GUIDED_ATTEMPT","FADED_ATTEMPT","INDEPENDENT_ATTEMPT","PHYSICAL_VERIFICATION","TRANSFER"]
assert profile["ready_stages"]==["ACTIVATE","VERIFY"]
assert profile["probe_first_stages"]==["DIAGNOSTIC_PROBE"]
assert problem["must_be_new_instance"] is True and problem["source_question_reuse"] is False
print("PHYSICS P-G Core1 contracts + policy digests = PASS")
