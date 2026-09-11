#!/usr/bin/env python3
import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = Path(__file__).resolve()
CORE1 = HERE.parents[1]
MATH = HERE.parents[2]
PCK = MATH / "InstructionalKnowledge"
SHARED_HUMAN = MATH.parent / "Shared" / "HumanReview"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value, omit=None):
    value = copy.deepcopy(value)
    if omit and isinstance(value, dict):
        value.pop(omit, None)
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


pck_contracts = PCK / "contracts"
core_contracts = CORE1 / "contracts"
schema_paths = [
    pck_contracts / "math-pck-asset.schema.json",
    pck_contracts / "math-pck-candidate-registry.schema.json",
    pck_contracts / "math-pck-promotion-registry.schema.json",
    core_contracts / "math-problem-authoring-plan.schema.json",
    core_contracts / "math-core1-lesson.schema.json",
    core_contracts / "math-core1-study-plan.schema.json",
]
schemas = {p.name: load(p) for p in schema_paths}
store = {s["$id"]: s for s in schemas.values()}
registry = Registry().with_resources([(k, Resource.from_contents(v)) for k, v in store.items()])
for schema in schemas.values():
    Draft202012Validator.check_schema(schema)

asset_schema = schemas["math-pck-asset.schema.json"]
candidate_schema = schemas["math-pck-candidate-registry.schema.json"]
promotion_schema = schemas["math-pck-promotion-registry.schema.json"]

candidate_registry_path = PCK / "registry" / "math-pck-candidates.json"
candidate_registry = load(candidate_registry_path)
Draft202012Validator(candidate_schema, registry=registry).validate(candidate_registry)
assert candidate_registry["registry_digest"] == digest(candidate_registry, "registry_digest")
candidate_assets = []
for doc in candidate_registry["asset_documents"]:
    asset = load(candidate_registry_path.parent / doc["path"])
    assert asset["asset_id"] == doc["asset_id"]
    assert asset["asset_digest"] == doc["asset_digest"]
    candidate_assets.append(asset)
for asset in candidate_assets:
    Draft202012Validator(asset_schema).validate(asset)
    assert asset["asset_digest"] == digest(asset, "asset_digest")
    assert asset["lifecycle_status"] == "CANDIDATE"
    assert asset["review"]["status"] == "PENDING_HUMAN_REVIEW"
    assert asset["review"]["human_review_evidence_refs"] == []

production_promotions = load(PCK / "registry" / "math-pck-promotion-registry.json")
Draft202012Validator(promotion_schema).validate(production_promotions)
assert production_promotions["registry_digest"] == digest(production_promotions, "registry_digest")
assert production_promotions["registry_class"] == "PRODUCTION"

test_promotions = load(CORE1 / "fixtures" / "test-only-pck-promotion-registry.fixture.json")
Draft202012Validator(promotion_schema).validate(test_promotions)
assert test_promotions["registry_digest"] == digest(test_promotions, "registry_digest")
assert test_promotions["registry_class"] == "TEST_ONLY"
for rec in test_promotions["promotions"]:
    assert rec["promotion_digest"] == digest(rec, "promotion_digest")
    assert rec["review_registry_class"] == "TEST_ONLY"
    assert rec["producer_legal"] is False

authority = load(MATH / "AssessmentScope" / "authority" / "math-assessment-scope-authority.json")
capability_ids = {x["capability_id"] for x in authority["capabilities"]}
family_ids = {x["problem_family_id"] for x in authority["problem_families"]}
for asset in candidate_assets:
    missing_caps = set(asset["capability_refs"]) - capability_ids
    assert not missing_caps, f"candidate capability refs unresolved: {sorted(missing_caps)}"
    assert asset["worked_example_family"] in family_ids
    assert asset["transfer_family"] in family_ids

mf_schema = load(MATH / "StudySynthesis" / "contracts" / "math-learner-study-model.schema.json")
mf_fixture = load(CORE1 / "fixtures" / "study-model-two-capabilities.fixture.json")["learner_study_model"]
Draft202012Validator(mf_schema).validate(mf_fixture)

human_submission = load(SHARED_HUMAN / "contracts" / "human-review-submission.schema.json")
assert human_submission["properties"]["source"]["const"] == "HUMAN_SUBMISSION"
assert set(human_submission["properties"]["review_dimension"]["enum"]) >= {"SUBJECT", "PEDAGOGY"}

print("MATH M-G contracts + PCK candidate custody + human promotion boundary PASS")
