#!/usr/bin/env python3
"""P-J contract validation: coverage matrices, longitudinal update, publication closure."""
import json, sys, tempfile, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
C = ROOT / "contracts"
sys.path[:0] = [
    str(ROOT / "engine"), str(PHYS / "Representation" / "engine"),
    str(PHYS / "Core2Transfer" / "engine"), str(PHYS / "CoreAuthoring" / "tests"),
]

from upstream import core1_plan, core2_plan, representation_bundle, question_set, load  # noqa: E402
from realize_physics_representations import realize  # noqa: E402
from build_physics_coverage_closure import build_closure  # noqa: E402

NAMES = [
    "physics-transfer-evidence-event.schema.json",
    "physics-source-coverage-matrix.schema.json",
    "physics-external-corpus-coverage-matrix.schema.json",
    "physics-longitudinal-update.schema.json",
    "physics-learner-state-update.schema.json",
    "physics-publication-coverage-closure.schema.json",
]
STORE = {n: json.loads((C / n).read_text(encoding="utf-8")) for n in NAMES}


def validator(name):
    s = STORE[name]
    return Draft202012Validator(s, resolver=RefResolver(base_uri="", referrer=s, store=STORE))


scope, model, core1 = core1_plan(attempts=True)
bundle = representation_bundle(core1, model)
core2 = core2_plan(core1, model, scope)
rep = PHYS / "Representation"
registry = load(rep / "registry" / "physics-teaching-primitive-registry.json")
contract = load(rep / "registry" / "physics-figure-render-contract.json")
policy = load(ROOT / "registry" / "physics-transfer-evidence-policy.json")
ledger = load(ROOT / "fixtures" / "physics-transfer-evidence.fixture.json")
classification = load(PHYS / "Core2Transfer" / "registry" / "physics-external-corpus-classification.json")
review = load(PHYS / "AssessmentReview" / "registry" / "physics-item-validity-registry.json")

event_v = validator("physics-transfer-evidence-event.schema.json")
for e in ledger["events"]:
    event_v.validate(e)

with tempfile.TemporaryDirectory() as td:
    page_map, _ = realize(bundle, registry, contract, td)
    closure = build_closure(question_set(), review, core1, bundle, core2, classification,
                            scope, model, policy, ledger, page_map)

validator("physics-source-coverage-matrix.schema.json").validate(closure["source_coverage_matrix"])
validator("physics-external-corpus-coverage-matrix.schema.json").validate(
    closure["external_corpus_coverage_matrix"])
validator("physics-longitudinal-update.schema.json").validate(closure["longitudinal_update"])
validator("physics-learner-state-update.schema.json").validate(closure["learner_state_update"])
validator("physics-publication-coverage-closure.schema.json").validate(closure)

assert set(closure["human_expert_review_states"].values()) == {"PENDING"}
assert closure["learner_state_update"]["assessment_scope_unchanged"] is True
for u in closure["longitudinal_update"]["capability_updates"]:
    assert u["dimensions_after"]["delayed_retention"] != "CLOSED", u["capability_ref"]

print(
    "PHY P-J contract validation: PASS "
    f"(closure={closure['closure_state']}, "
    f"{closure['summary']['source_denominator']} source items / "
    f"{closure['summary']['source_uncovered']} uncovered, "
    f"{closure['summary']['external_denominator']} external candidates / "
    f"{closure['summary']['external_uncovered']} uncovered, "
    f"{closure['summary']['dimensions_closed']} longitudinal dimensions closed, "
    f"{closure['summary']['dimensions_open']} still open)"
)
