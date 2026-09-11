#!/usr/bin/env python3
import json, sys
from pathlib import Path

D=Path(__file__).resolve().parents[1]
MATH=D.parent
sys.path.insert(0,str(MATH/"StudySynthesis"/"engine"))
sys.path.insert(0,str(D/"engine"))
from synthesize_math_study_model import build_study_scope, load
from author_math_core1 import load_candidate_bundle

bindings=load(MATH/"AssessmentScope"/"registry"/"mixed-grade9-question-scope-bindings.json")
authority=load(MATH/"AssessmentScope"/"authority"/"math-assessment-scope-authority.json")
scope=build_study_scope(bindings,authority)
registry,assets=load_candidate_bundle(MATH/"InstructionalKnowledge"/"registry"/"math-pck-candidates.json")

required=set(scope["direct_assessed_capability_refs"]+scope["prerequisite_support_capability_refs"])
covered={cap for asset in assets for cap in asset["capability_refs"]}
missing=sorted(required-covered)
extra=sorted(covered-required)
print("MATH M-G assessment-scope capability count =",len(required))
print("MATH M-G PCK candidate covered capability count =",len(required & covered))
print("MATH M-G PCK candidate coverage gaps =",json.dumps(missing))
print("MATH M-G PCK candidate extra/support capabilities =",json.dumps(extra))
assert not missing,"PCK_SCOPE_COVERAGE_GAP:"+",".join(missing)

# Candidate coverage does not imply producer legality. Promotion stays a separate human-authority gate.
production=load(MATH/"InstructionalKnowledge"/"registry"/"math-pck-promotion-registry.json")
assert production["registry_class"]=="PRODUCTION"
assert all(a["lifecycle_status"]=="CANDIDATE" for a in assets)
assert all(a["review"]["status"]=="PENDING_HUMAN_REVIEW" for a in assets)
assert all(a["review"]["human_review_evidence_refs"]==[] for a in assets)
print("MATH M-G assessment-scope PCK candidate coverage PASS")
print("MATH M-G human promotion remains a separate fail-closed authority")
