#!/usr/bin/env python3
"""P-H contract validation: primitive registry, representation bundle, physical page map."""
import json, sys, tempfile, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
C = ROOT / "contracts"
sys.path[:0] = [str(ROOT / "engine"), str(PHYS / "CoreAuthoring" / "tests")]

from upstream import core1_plan, load  # noqa: E402
from build_physics_representations import build_bundle  # noqa: E402
from realize_physics_representations import realize, audit  # noqa: E402


def schema(name):
    return json.loads((C / name).read_text(encoding="utf-8"))


STORE = {n: schema(n) for n in (
    "physics-teaching-primitive-registry.schema.json",
    "physics-representation-spec.schema.json",
    "physics-representation-bundle.schema.json",
    "physics-physical-page-map.schema.json",
)}


def validator(name):
    s = STORE[name]
    return Draft202012Validator(s, resolver=RefResolver(base_uri="", referrer=s, store=STORE))


registry = load(ROOT / "registry" / "physics-teaching-primitive-registry.json")
profile = load(ROOT / "registry" / "physics-page-intent-profile.json")
contract = load(ROOT / "registry" / "physics-figure-render-contract.json")
validator("physics-teaching-primitive-registry.schema.json").validate(registry)

scope, model, plan = core1_plan(attempts=True)
questions = load(PHYS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
bundle = build_bundle(plan, model, questions, registry, profile, contract)

spec_validator = validator("physics-representation-spec.schema.json")
for spec in bundle["representations"]:
    spec_validator.validate(spec)
validator("physics-representation-bundle.schema.json").validate(bundle)

with tempfile.TemporaryDirectory() as td:
    page_map, pdf_path = realize(bundle, registry, contract, td)
    validator("physics-physical-page-map.schema.json").validate(page_map)
    audit(page_map, Path(pdf_path).read_bytes(), registry, contract)

    # every required primitive named in #256 / #234 Phase 7 must exist and be realizable
    required = set(registry["required_primitive_ids"])
    declared = {p["primitive_id"] for p in registry["primitives"]}
    assert required <= declared, sorted(required - declared)

    assert page_map["realization_summary"]["label_only_figure_count"] == 0
    assert page_map["realization_summary"]["total_vector_ops"] > 0
    for p in page_map["content_placements"]:
        floor = next(x["minimum_vector_ops"] for x in registry["primitives"]
                     if x["primitive_id"] == p["primitive"])
        assert p["vector_ops"] >= floor, (p["content_ref"], p["vector_ops"], floor)

print(
    "PHY P-H contract validation: PASS "
    f"({len(registry['primitives'])} primitives, {bundle['summary']['representation_count']} representations, "
    f"{page_map['realization_summary']['total_vector_ops']} real vector operations over "
    f"{page_map['physical_page_count']} pages)"
)
