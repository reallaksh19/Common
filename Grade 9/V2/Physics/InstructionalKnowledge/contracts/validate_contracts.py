#!/usr/bin/env python3
import copy, hashlib, importlib.util, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
PHYS=ROOT.parent
CONTRACTS=ROOT/"contracts"
REG=ROOT/"registry"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest_without(v,field):
    x=copy.deepcopy(v); x.pop(field,None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

for p in sorted(CONTRACTS.glob("*.schema.json")):
    Draft202012Validator.check_schema(load(p))

spec=importlib.util.spec_from_file_location("physics_pck_candidates",REG/"physics_pck_candidates.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
candidates=mod.get_registry()
promotions=load(REG/"physics-pck-promotion-registry.json")
asset_schema=load(CONTRACTS/"physics-pck-asset.schema.json")
Draft202012Validator(load(CONTRACTS/"physics-pck-candidate-registry.schema.json")).validate(candidates)
Draft202012Validator(load(CONTRACTS/"physics-pck-promotion-registry.schema.json")).validate(promotions)

assert candidates["registry_digest"]==digest_without(candidates,"registry_digest")
assert promotions["registry_digest"]==digest_without(promotions,"registry_digest")
ids=set(); covered=set()
for asset in candidates["asset_documents"]:
    Draft202012Validator(asset_schema).validate(asset)
    assert asset["asset_id"] not in ids; ids.add(asset["asset_id"])
    assert asset["asset_digest"]==digest_without(asset,"asset_digest")
    assert asset["review"]["status"]=="PENDING_HUMAN_REVIEW"
    assert asset["review"]["human_review_evidence_refs"]==[]
    covered.update(asset["capability_refs"])

required_topics={
"PHY-PCK-SYSTEM-REFERENCE-FRAME-v1","PHY-PCK-SIGN-DIRECTION-v1",
"PHY-PCK-DISTANCE-DISPLACEMENT-v1","PHY-PCK-AVERAGE-SPEED-WEIGHTING-v1",
"PHY-PCK-CONSTANT-ACCELERATION-MODEL-GATE-v1","PHY-PCK-EQUATION-SELECTION-FIRST-MOVE-v1",
"PHY-PCK-STATE-PROPAGATION-PHASES-v1","PHY-PCK-NTH-SECOND-INTERVAL-v1",
"PHY-PCK-STOPPING-DISTANCE-SPEED-SQUARED-v1","PHY-PCK-GRAVITY-CONSTANT-ACCELERATION-v1",
"PHY-PCK-HIGHEST-POINT-ZERO-V-NONZERO-A-v1","PHY-PCK-SAME-HEIGHT-TWO-TIMES-v1",
"PHY-PCK-RELATIVE-COMMON-G-CANCELLATION-v1","PHY-PCK-MOVING-RELEASE-v1",
"PHY-PCK-VT-SIGNED-AREA-v1","PHY-PCK-GRAPH-HEIGHT-SLOPE-AREA-v1",
"PHY-PCK-PHYSICAL-VERIFICATION-v1"
}
assert required_topics <= ids

authority=load(PHYS/"AssessmentScope/authority/physics-assessment-scope-authority.json")
authority_caps={x["capability_id"] for x in authority["capabilities"]}
assert covered <= authority_caps
missing=authority_caps-covered
assert not missing, f"PCK_COVERAGE_GAP: {sorted(missing)}"

# AI-authored candidate records must never self-promote.
assert promotions["promotions"]==[], "PCK promotion requires explicit human review evidence"
print(f"PHYSICS P-G PCK candidate assets = {len(ids)} PASS")
print("PHYSICS P-G authority capability coverage = PASS")
print("PHYSICS P-G human-promotion boundary = FAIL-CLOSED PASS")
