#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = Path(__file__).resolve()
CORE1 = HERE.parents[1]
MATH = HERE.parents[2]
PCK = MATH / "InstructionalKnowledge"
sys.path.insert(0, str(CORE1 / "engine"))

import author_math_core1 as mg


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


CANDIDATES, CANDIDATE_ASSETS = mg.load_candidate_bundle(PCK / "registry" / "math-pck-candidates.json")
PROD = load(PCK / "registry" / "math-pck-promotion-registry.json")
TEST_PROMO = load(CORE1 / "fixtures" / "test-only-pck-promotion-registry.fixture.json")
STUDY = load(CORE1 / "fixtures" / "study-model-two-capabilities.fixture.json")
PROFILE = load(CORE1 / "policies" / "math-instructional-authoring-profile.json")
SCOPE_POLICY = load(CORE1 / "policies" / "math-core1-scope-completeness-policy.json")

SCHEMAS = {}
for schema_name in ["math-problem-authoring-plan.schema.json", "math-core1-lesson.schema.json", "math-core1-study-plan.schema.json"]:
    schema = load(CORE1 / "contracts" / schema_name)
    SCHEMAS[schema["$id"]] = schema


def expect_error(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        return
    raise AssertionError(f"expected {code}")


required_asset_ids = {
    "MATH-PCK-EQUALITY-PRESERVATION-v1",
    "MATH-PCK-EXPRESSION-IDENTITY-v1",
    "MATH-PCK-BINOMIAL-SQUARE-RECONSTRUCTION-v1",
    "MATH-PCK-ORDERED-PAIR-SEMANTICS-v1",
    "MATH-PCK-SLOPE-AS-RATE-OF-CHANGE-v1",
    "MATH-PCK-COLLINEARITY-COMMON-DIRECTION-v1",
    "MATH-PCK-SIMULTANEOUS-EQUATION-ELIMINATION-v1",
    "MATH-PCK-GEOMETRY-TO-ALGEBRA-BRIDGE-v1",
    "MATH-PCK-SOLUTION-VERIFICATION-v1",
    "MATH-PCK-WORD-TO-EQUATION-MODELLING-v1",
}
assert required_asset_ids.issubset({x["asset_id"] for x in CANDIDATE_ASSETS})
for asset in CANDIDATE_ASSETS:
    assert asset["lifecycle_status"] == "CANDIDATE"
    assert asset["review"]["status"] == "PENDING_HUMAN_REVIEW"
    assert not asset["review"]["human_review_evidence_refs"]

# The production promotion registry now carries real pipeline output. Every
# entry is provisional: authoring-legal, never producer-legal, expert review
# still PENDING. No fabricated human PASS may appear.
assert PROD["registry_class"] == "PRODUCTION"
assert PROD["promotions"], "production promotion registry must be exercised, not empty"
for rec in PROD["promotions"]:
    assert rec["promotion_status"] == "PROVISIONAL_PROMOTED", rec["asset_id"]
    assert rec["promotion_class"] == "AI_ASSISTED_PROVISIONAL"
    assert rec["review_source"] == "AI_ASSISTED_REFERENCE_REVIEW"
    assert rec["review_registry_class"] == "AI_ASSISTED"
    assert rec["authoring_legal"] is True
    assert rec["producer_legal"] is False
    assert rec["release_legal"] is False
    assert rec["expert_review_state"] == {"SUBJECT_EXPERT_PASS": "PENDING", "PEDAGOGY_EXPERT_PASS": "PENDING"}
    assert [s["stage"] for s in rec["review_pipeline"]] == [
        "EVIDENCE_PROVENANCE_REVIEW",
        "PEDAGOGICAL_REVIEW",
        "SUBJECT_REVIEW",
        "SCOPE_REVIEW",
    ]

# A provisional promotion produces an authoring-legal plan that is explicitly
# not release-legal.
prod_plan = mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, PROD, PROFILE, SCOPE_POLICY, test_mode=False)
assert prod_plan["release_class"] == "PROVISIONAL_PENDING_EXPERT_REVIEW"
assert prod_plan["pck_authority"]["expert_review_state"] == "PENDING"
assert prod_plan["pck_authority"]["release_legal"] is False
assert prod_plan["pck_authority"]["producer_legal_asset_refs"] == []
assert prod_plan["pck_authority"]["provisional_asset_refs"]

# A provisional record that claims producer legality is rejected by name.
lying = copy.deepcopy(PROD)
lying["promotions"][0]["producer_legal"] = True
lying["promotions"][0]["promotion_digest"] = mg.digest(lying["promotions"][0], "promotion_digest")
lying["registry_digest"] = mg.digest(lying, "registry_digest")
expect_error(
    "PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL",
    lambda: mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, lying, PROFILE, SCOPE_POLICY, test_mode=False),
)

# A provisional record that relabels itself as human-reviewed is rejected.
fake_human = copy.deepcopy(PROD)
fake_human["promotions"][0]["promotion_status"] = "PROMOTED"
fake_human["promotions"][0]["promotion_digest"] = mg.digest(fake_human["promotions"][0], "promotion_digest")
fake_human["registry_digest"] = mg.digest(fake_human, "registry_digest")
expect_error(
    "PCK_REVIEW_AUTHORITY_INVALID",
    lambda: mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, fake_human, PROFILE, SCOPE_POLICY, test_mode=False),
)

# An empty production registry still fails closed for full-teaching treatments.
empty_prod = copy.deepcopy(PROD)
empty_prod["promotions"] = []
empty_prod["registry_digest"] = mg.digest(empty_prod, "registry_digest")
expect_error(
    "PCK_PROMOTION_REQUIRED:MATH-EQUALITY-PRESERVATION",
    lambda: mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, empty_prod, PROFILE, SCOPE_POLICY, test_mode=False),
)

expect_error(
    "TEST_ONLY_PCK_REGISTRY_FORBIDDEN",
    lambda: mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, TEST_PROMO, PROFILE, SCOPE_POLICY, test_mode=False),
)

plan_a = mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, TEST_PROMO, PROFILE, SCOPE_POLICY, test_mode=True)
plan_b = mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, TEST_PROMO, PROFILE, SCOPE_POLICY, test_mode=True)
assert plan_a == plan_b
assert plan_a["release_class"] == "TEST_ONLY"
assert plan_a["scope_completeness"]["status"] == "PASS"
assert set(plan_a["scope_completeness"]["required_capability_refs"]) == {"MATH-EQUALITY-PRESERVATION", "MATH-RIVER-CURRENT-MODEL"}
assert plan_a["scope_completeness"]["omitted_capability_refs"] == []

plan_schema = SCHEMAS["math-core1-study-plan.schema.json"]
schema_registry = Registry().with_resources([(k, Resource.from_contents(v)) for k, v in SCHEMAS.items()])
Draft202012Validator(plan_schema, registry=schema_registry).validate(plan_a)

by_cap = {x["capability_ref"]: x for x in plan_a["lessons"]}
eq = by_cap["MATH-EQUALITY-PRESERVATION"]
ready = by_cap["MATH-RIVER-CURRENT-MODEL"]

assert eq["instructional_sequence"] == ["ANCHOR", "REPRESENT", "EXPLAIN", "RECONSTRUCT", "CONTRAST", "WORKED", "GUIDED", "FADED", "INDEPENDENT", "VERIFY", "TRANSFER"]
assert "MATH-PCK-EQUALITY-PRESERVATION-v1" in eq["pck_asset_refs"]
assert {p["instance_role"] for p in eq["problem_authoring_plans"]} == {"WORKED", "GUIDED", "FADED", "INDEPENDENT", "TRANSFER"}
for pap in eq["problem_authoring_plans"]:
    assert pap["must_be_new_instance"] is True
    assert pap["source_question_reuse"] is False
    assert pap["source_question_refs"] == []
    assert pap["problem_family_ref"].startswith("MATH-PF-")

assert ready["instructional_sequence"] == ["ACTIVATE", "VERIFY"]
assert all(step not in ready["instructional_sequence"] for step in ["WORKED", "GUIDED", "FADED", "TRANSFER"])

# A full-teaching capability with no PCK candidate at all still fails closed.
gap_study = copy.deepcopy(STUDY)
cp = gap_study["learner_study_model"]["capability_plans"][0]
cp["capability_ref"] = "MATH-TRIGONOMETRIC-RATIO"
cp["problem_family_refs"] = ["MATH-PF-LINE-SLOPE-POINT"]
assert not any("MATH-TRIGONOMETRIC-RATIO" in a["capability_refs"] for a in CANDIDATE_ASSETS)
expect_error(
    "PCK_COVERAGE_GAP:MATH-TRIGONOMETRIC-RATIO",
    lambda: mg.author(gap_study, CANDIDATES, CANDIDATE_ASSETS, TEST_PROMO, PROFILE, SCOPE_POLICY, test_mode=True),
)

# A capability that has a candidate but no promotion of any class still fails closed.
unpromoted_study = copy.deepcopy(STUDY)
up = unpromoted_study["learner_study_model"]["capability_plans"][0]
up["capability_ref"] = "MATH-FRACTION-ARITHMETIC"
up["problem_family_refs"] = ["MATH-PF-LINE-SLOPE-POINT"]
expect_error(
    "PCK_PROMOTION_REQUIRED:MATH-FRACTION-ARITHMETIC",
    lambda: mg.author(unpromoted_study, CANDIDATES, CANDIDATE_ASSETS, TEST_PROMO, PROFILE, SCOPE_POLICY, test_mode=True),
)

fake_prod = copy.deepcopy(TEST_PROMO)
fake_prod["registry_class"] = "PRODUCTION"
for rec in fake_prod["promotions"]:
    rec["promotion_status"] = "PROMOTED"
    rec["producer_legal"] = True
    rec["promotion_digest"] = mg.digest(rec, "promotion_digest")
fake_prod["registry_digest"] = mg.digest(fake_prod, "registry_digest")
expect_error(
    "PCK_REVIEW_AUTHORITY_INVALID",
    lambda: mg.author(STUDY, CANDIDATES, CANDIDATE_ASSETS, fake_prod, PROFILE, SCOPE_POLICY, test_mode=False),
)

reuse = copy.deepcopy(plan_a)
reuse["lessons"][0]["problem_authoring_plans"][0]["source_question_reuse"] = True
reuse["lessons"][0]["problem_authoring_plans"][0]["source_question_refs"] = ["Q10"]
expect_error(
    "SOURCE_QUESTION_REUSE_FORBIDDEN",
    lambda: mg.assert_plan_invariants(reuse, STUDY["learner_study_model"], PROFILE),
)

missing = copy.deepcopy(plan_a)
missing["lessons"] = missing["lessons"][:-1]
expect_error(
    "CORE1_SCOPE_GAP",
    lambda: mg.assert_plan_invariants(missing, STUDY["learner_study_model"], PROFILE),
)

bad_assets = copy.deepcopy(CANDIDATE_ASSETS)
bad_assets[0]["anchor"] += " tampered"
expect_error(
    "PCK_DIGEST_MISMATCH",
    lambda: mg.author(STUDY, CANDIDATES, bad_assets, TEST_PROMO, PROFILE, SCOPE_POLICY, test_mode=True),
)

print("MATH M-G PCK promotion + Core1 authoring falsifiers PASS")
