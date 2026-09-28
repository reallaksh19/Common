#!/usr/bin/env python3
"""P-I contract validation: transfer plan, pages, hint ladder, linkage, solution."""
import json, sys, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
C = ROOT / "contracts"
sys.path[:0] = [str(ROOT / "engine"), str(PHYS / "CoreAuthoring" / "tests")]

from upstream import core1_plan, load  # noqa: E402
from build_physics_core2_transfer import build_plan  # noqa: E402

NAMES = [
    "physics-hint-ladder.schema.json",
    "physics-core1-core2-linkage.schema.json",
    "physics-solution-verification.schema.json",
    "physics-transfer-question-page.schema.json",
    "physics-core2-transfer-plan.schema.json",
]
STORE = {n: json.loads((C / n).read_text(encoding="utf-8")) for n in NAMES}


def validator(name):
    s = STORE[name]
    return Draft202012Validator(s, resolver=RefResolver(base_uri="", referrer=s, store=STORE))


scope, model, plan = core1_plan(attempts=True)
core2 = build_plan(
    load(ROOT / "fixtures" / "physics-external-transfer-source.fixture.json"),
    load(ROOT / "registry" / "physics-external-corpus-classification.json"),
    plan, model, scope,
    load(ROOT / "registry" / "physics-core2-authoring-profile.json"),
    load(ROOT / "registry" / "physics-transfer-badge-policy.json"),
    load(ROOT / "registry" / "physics-concept-segregation.json"),
)

page_v = validator("physics-transfer-question-page.schema.json")
hint_v = validator("physics-hint-ladder.schema.json")
link_v = validator("physics-core1-core2-linkage.schema.json")
sol_v = validator("physics-solution-verification.schema.json")
for p in core2["transfer_pages"]:
    page_v.validate(p)
    hint_v.validate(p["hint_ladder"])
    link_v.validate(p["core1_linkage"])
    sol_v.validate(p["solution"])
validator("physics-core2-transfer-plan.schema.json").validate(core2)

assert set(core2["human_expert_review_states"].values()) == {"PENDING"}
assert core2["release_authority_state"] == "PILOT_ONLY_HUMAN_EXPERT_RELEASE_NOT_GRANTED"

print(
    "PHY P-I contract validation: PASS "
    f"({core2['summary']['page_count']} transfer pages over "
    f"{core2['summary']['eligible_candidate_count']} eligible candidates, "
    f"{core2['summary']['first_step_reference_count']} first-step references, "
    f"{len(core2['out_of_scope_candidate_refs'])} out-of-scope candidate(s) correctly excluded)"
)
