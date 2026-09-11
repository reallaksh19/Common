#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

primitive_schema = load(HERE / "math-teaching-primitive.schema.json")
registry_schema = load(HERE / "math-teaching-primitive-registry.schema.json")
spec_schema = load(HERE / "math-representation-spec.schema.json")
plan_schema = load(HERE / "math-representation-plan.schema.json")
profile_schema = load(HERE / "math-page-intent-profile.schema.json")
registry = load(BASE / "registry/math-teaching-primitive-registry.json")
profile = load(BASE / "policies/math-page-intent-profile.json")

for schema in [primitive_schema, registry_schema, spec_schema, plan_schema, profile_schema]:
    Draft202012Validator.check_schema(schema)

# Inline local refs for standalone validation in CI.
registry_runtime_schema = copy.deepcopy(registry_schema)
registry_runtime_schema["properties"]["primitives"]["items"] = primitive_schema
plan_runtime_schema = copy.deepcopy(plan_schema)
plan_runtime_schema["properties"]["representations"]["items"] = spec_schema

def assert_valid(schema, value, label):
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        raise SystemExit(label + ": " + "; ".join(e.message for e in errors))

assert_valid(registry_runtime_schema, registry, "teaching primitive registry schema failure")
assert_valid(profile_schema, profile, "page intent profile schema failure")

for fixture in sorted((BASE / "fixtures").glob("*.fixture.json")):
    data = load(fixture)
    for spec in data["representations"]:
        assert_valid(spec_schema, spec, "representation spec schema failure " + fixture.name)

required_names = {
    "ALIGNED_TRANSFORMATION_STACK","TERM_HIGHLIGHT_VIEW","EQUIVALENCE_BALANCE_VIEW","COORDINATE_PLANE",
    "SLOPE_TRIANGLE_VIEW","CORRECT_WRONG_TRANSFORMATION_CONTRAST","SIDE_BY_SIDE_METHOD_VIEW",
    "ANNOTATED_DERIVATION","INVARIANT_HIGHLIGHT","SUBSTITUTION_CHECK_VIEW","PARALLEL_MEET_CONTRAST",
    "MIRROR_SOLUTION_VIEW"
}
actual_names = {p["canonical_name"] for p in registry["primitives"]}
if actual_names != required_names:
    raise SystemExit("teaching primitive coverage mismatch")

current_math_requirements = {
    "NATURAL_LANGUAGE_STATEMENT","ORDERED_PAIR","GEOMETRIC_DISTANCE_RELATION","SYMBOLIC_LINEAR_EQUATION",
    "UNORDERED_PAIR_MODEL","SLOPE_RATIO","ANGLE_RELATION","PARAMETER_CONDITION","SYSTEM_OF_LINEAR_EQUATIONS",
    "CARTESIAN_AXIS_CONSTRAINT","UNIT_RATE","RATE_CONTEXT_MODEL"
}
profile_requirements = {b["representation_requirement_ref"] for b in profile["requirement_bindings"]}
if profile_requirements != current_math_requirements:
    raise SystemExit("page-intent profile does not close current M-D representation vocabulary")

# Build every reference fixture and validate the output contract.
engine_spec = importlib.util.spec_from_file_location("mh_engine", BASE / "engine/build_math_representation_plan.py")
mh = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(mh)
for fixture in sorted((BASE / "fixtures").glob("*.fixture.json")):
    data = load(fixture)
    out = mh.build(data["context"], data["representations"], registry, profile)
    assert_valid(plan_runtime_schema, out, "representation plan schema failure " + fixture.name)

print("MATH M-H contract validation PASS")
