#!/usr/bin/env python3
"""P-G contract validation: PCK registry, authoring profiles and a generated Core1 plan."""
import json, sys, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
C = ROOT / "contracts"
sys.path[:0] = [str(ROOT / "engine"), str(ROOT / "tests")]

from build_physics_core1 import build_plan, load_pck_registry, validate_pck_registry, load  # noqa: E402
from upstream import build_upstream  # noqa: E402


def schema(name):
    return json.loads((C / name).read_text(encoding="utf-8"))


def validator(name):
    s = schema(name)
    store = {
        "physics-core1-lesson.schema.json": schema("physics-core1-lesson.schema.json"),
        "physics-promoted-pck.schema.json": schema("physics-promoted-pck.schema.json"),
        "physics-core1-study-plan.schema.json": schema("physics-core1-study-plan.schema.json"),
    }
    return Draft202012Validator(s, resolver=RefResolver(base_uri="", referrer=s, store=store))


registry = load_pck_registry()
validate_pck_registry(registry)
validator("physics-promoted-pck.schema.json").validate(registry)

profile = load(ROOT / "registry" / "physics-instructional-authoring-profile.json")
problems = load(ROOT / "registry" / "physics-problem-authoring-profile.json")
completeness = load(ROOT / "registry" / "physics-core1-scope-completeness-policy.json")

scope, model = build_upstream(attempts=True)
plan = build_plan(model, scope, registry, profile, completeness, problems)

lesson_validator = validator("physics-core1-lesson.schema.json")
for lesson in plan["lessons"]:
    lesson_validator.validate(lesson)
validator("physics-core1-study-plan.schema.json").validate(plan)

for asset in registry["assets"]:
    auth = asset["promotion_authority"]
    assert auth["promotion_state"] == "PROMOTED_PILOT", asset["asset_id"]
    assert auth["subject_expert_release_state"] == "NOT_GRANTED", asset["asset_id"]
    assert auth["pedagogy_expert_release_state"] == "NOT_GRANTED", asset["asset_id"]
    assert auth["final_product_release_blocked"] is True, asset["asset_id"]

assert set(plan["human_expert_review_states"].values()) == {"PENDING"}
print(
    "PHY P-G contract validation: PASS "
    f"({len(registry['assets'])} promoted-pilot PCK assets, {len(plan['lessons'])} Core1 lessons, "
    f"{plan['summary']['appendix_a_item_count']} Appendix A items)"
)
