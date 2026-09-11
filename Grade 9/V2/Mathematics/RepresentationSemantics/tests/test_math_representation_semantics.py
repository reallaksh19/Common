#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mh_engine", BASE / "engine/build_math_representation_plan.py")
mh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mh)

def load(rel):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))

registry = load("registry/math-teaching-primitive-registry.json")
profile = load("policies/math-page-intent-profile.json")
fixtures = {
    p.name: load("fixtures/" + p.name)
    for p in sorted((BASE / "fixtures").glob("*.fixture.json"))
}

def reseal_spec(s):
    s["spec_digest"] = mh.digest(s, "spec_digest")

def reseal_registry(r):
    for p in r["primitives"]:
        p["primitive_digest"] = mh.digest(p, "primitive_digest")
    r["registry_digest"] = mh.digest(r, "registry_digest")

def reseal_profile(p):
    p["profile_digest"] = mh.digest(p, "profile_digest")

def expect(code, fn):
    try:
        fn()
    except ValueError as exc:
        assert code in str(exc), (code, str(exc))
        return
    raise AssertionError("expected " + code)

# 1. Representative Core1 and Core2 semantic plans build.
plans = {}
for name, fixture in fixtures.items():
    plans[name] = mh.build(fixture["context"], fixture["representations"], registry, profile)
    assert plans[name]["coverage"]
    assert plans[name]["representations"]

# 2. Deterministic replay.
f = fixtures["core1-equality.fixture.json"]
a = mh.build(f["context"], f["representations"], registry, profile)
b = mh.build(copy.deepcopy(f["context"]), copy.deepcopy(f["representations"]), copy.deepcopy(registry), copy.deepcopy(profile))
assert mh.canon(a) == mh.canon(b)

# 3. DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS
bad = copy.deepcopy(f)
bad["representations"][0]["semantic_role"] = "DECORATIVE"
reseal_spec(bad["representations"][0])
expect("DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 4. VISUAL_WITHOUT_CAPABILITY_BINDING
bad = copy.deepcopy(f)
bad["representations"][0]["capability_ref"] = "MATH-OTHER-CAPABILITY"
reseal_spec(bad["representations"][0])
expect("VISUAL_WITHOUT_CAPABILITY_BINDING", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 5. RENDERER_INVENTS_UNDECLARED_MATH_MEANING
bad = copy.deepcopy(f)
bad["representations"][0]["renderer_constraints"]["must_not_infer_mathematical_content"] = False
reseal_spec(bad["representations"][0])
expect("RENDERER_INVENTS_UNDECLARED_MATH_MEANING", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 6. CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED
bad = copy.deepcopy(f)
s = bad["representations"][1]
s["primitive_id"] = "MATH-TP-ALIGNED_TRANSFORMATION_STACK-v1"
s["source_semantic_data"]["payload"] = {"states":["a=b","a+c=b+c"],"operations":["add c to both sides"],"invariant":"solution set preserved"}
reseal_spec(s)
# Make the non-contrast primitive job-compatible so the falsifier reaches the contrast-semantic gate.
r_contrast = copy.deepcopy(registry)
p_aligned = next(x for x in r_contrast["primitives"] if x["primitive_id"] == "MATH-TP-ALIGNED_TRANSFORMATION_STACK-v1")
p_aligned["supported_instructional_jobs"].append("DISCRIMINATE_CASES")
reseal_registry(r_contrast)
expect("CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED", lambda: mh.build(bad["context"], bad["representations"], r_contrast, profile))

# 7. Missing semantic source fields fail.
bad = copy.deepcopy(fixtures["core1-slope.fixture.json"])
bad["representations"][1]["source_semantic_data"]["payload"].pop("delta_y")
reseal_spec(bad["representations"][1])
expect("SOURCE_SEMANTIC_DATA_INCOMPLETE", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 8. A required semantic representation cannot be omitted.
bad = copy.deepcopy(fixtures["core2-euclid-transfer.fixture.json"])
bad["representations"] = [x for x in bad["representations"] if x["semantic_requirement_ref"] != "ANGLE_RELATION"]
expect("REPRESENTATION_REQUIREMENT_UNCOVERED:ANGLE_RELATION", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 9. Renderer cannot choose an undeclared primitive for a semantic requirement.
bad = copy.deepcopy(fixtures["core2-euclid-transfer.fixture.json"])
s = next(x for x in bad["representations"] if x["semantic_requirement_ref"] == "ANGLE_RELATION")
s["primitive_id"] = "MATH-TP-COORDINATE_PLANE-v1"
s["instructional_job"] = "SHOW_STRUCTURE"
s["source_semantic_data"]["payload"] = {"points":{},"axes":{},"relations":[]}
s["misconception_or_contrast_ref"] = None
reseal_spec(s)
expect("PRIMITIVE_NOT_ALLOWED_FOR_REQUIREMENT", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 10. ERROR_CONTRAST in the lesson/PCK obligations requires an explicit contrast representation.
bad = copy.deepcopy(f)
bad["representations"] = [x for x in bad["representations"] if x["instructional_job"] != "DISCRIMINATE_CASES"]
expect("ERROR_CONTRAST_REQUIRED_BUT_NOT_REPRESENTED", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 11. VERIFICATION_HABIT requires an explicit verification representation.
bad = copy.deepcopy(f)
bad["representations"] = [x for x in bad["representations"] if x["instructional_job"] != "VERIFY_REASONING"]
expect("VERIFICATION_REPRESENTATION_REQUIRED_BUT_MISSING", lambda: mh.build(bad["context"], bad["representations"], registry, profile))

# 12. Registry custody detects tampering.
r2 = copy.deepcopy(registry)
r2["primitives"][0]["required_source_fields"].append("invented_field")
expect("TEACHING_PRIMITIVE_REGISTRY_DIGEST_MISMATCH", lambda: mh.build(f["context"], f["representations"], r2, profile))

# 13. Every current M-D representation vocabulary item has a declared semantic primitive route.
expected = {"NATURAL_LANGUAGE_STATEMENT","ORDERED_PAIR","GEOMETRIC_DISTANCE_RELATION","SYMBOLIC_LINEAR_EQUATION","UNORDERED_PAIR_MODEL","SLOPE_RATIO","ANGLE_RELATION","PARAMETER_CONDITION","SYSTEM_OF_LINEAR_EQUATIONS","CARTESIAN_AXIS_CONSTRAINT","UNIT_RATE","RATE_CONTEXT_MODEL"}
assert {x["representation_requirement_ref"] for x in profile["requirement_bindings"]} == expected

# 14. Required issue primitives all exist.
required_primitives = {"ALIGNED_TRANSFORMATION_STACK","TERM_HIGHLIGHT_VIEW","EQUIVALENCE_BALANCE_VIEW","COORDINATE_PLANE","SLOPE_TRIANGLE_VIEW","CORRECT_WRONG_TRANSFORMATION_CONTRAST","SIDE_BY_SIDE_METHOD_VIEW","ANNOTATED_DERIVATION","INVARIANT_HIGHLIGHT","SUBSTITUTION_CHECK_VIEW","PARALLEL_MEET_CONTRAST","MIRROR_SOLUTION_VIEW"}
assert {x["canonical_name"] for x in registry["primitives"]} == required_primitives

print("MATH M-H representation falsifiers PASS")
