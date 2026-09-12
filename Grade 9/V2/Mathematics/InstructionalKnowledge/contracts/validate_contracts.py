#!/usr/bin/env python3
"""Fail-closed contract validation for the Mathematics PCK authority (M-G).

Exit codes: 0 = PASS, 1 = FAIL, 2 = BLOCKED (a contract or registry could not be read).
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(MATH / "Core1Authoring" / "engine"))

SCHEMAS = [
    "math-pck-asset.schema.json",
    "math-pck-candidate-registry.schema.json",
    "math-pck-promotion-registry.schema.json",
    "math-pck-promotion-review-record.schema.json",
]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}:{detail}" if detail else code)


def main():
    try:
        schemas = {name: load(ROOT / "contracts" / name) for name in SCHEMAS}
        import promote_math_pck as pm
        from author_math_core1 import load_candidate_bundle

        candidate_registry, candidate_assets = load_candidate_bundle(ROOT / "registry" / "math-pck-candidates.json")
        promotion_registry = load(ROOT / "registry" / "math-pck-promotion-registry.json")
    except Exception as exc:  # noqa: BLE001 - blocked, not failed
        print(f"BLOCKED: {exc}")
        return 2

    try:
        for name, schema in schemas.items():
            Draft202012Validator.check_schema(schema)
        asset_validator = Draft202012Validator(schemas["math-pck-asset.schema.json"])
        for asset in candidate_assets:
            asset_validator.validate(asset)
            if asset["lifecycle_status"] != "CANDIDATE":
                fail("PCK_CANDIDATE_LIFECYCLE_DRIFT", asset["asset_id"])
            if asset["review"]["status"] != "PENDING_HUMAN_REVIEW" or asset["review"]["human_review_evidence_refs"]:
                fail("FAKE_HUMAN_REVIEW_STATE", asset["asset_id"])
        Draft202012Validator(schemas["math-pck-candidate-registry.schema.json"]).validate(candidate_registry)
        Draft202012Validator(schemas["math-pck-promotion-registry.schema.json"]).validate(promotion_registry)

        for record in promotion_registry["promotions"]:
            pm.assert_promotion_honesty(record)
        if not promotion_registry["promotions"]:
            fail("PCK_PROMOTION_MECHANISM_NOT_EXERCISED")

        # The committed registry must be exactly what the pipeline produces.
        rebuilt, refusals = pm.build_registry(candidate_registry, candidate_assets)
        if refusals:
            fail("PCK_PROMOTION_REFUSED", refusals[0]["asset_id"])
        if rebuilt != promotion_registry:
            fail("PCK_PROMOTION_REGISTRY_NOT_REPRODUCIBLE")

        # Any producer-legal entry must name real authorized human review.
        for record in promotion_registry["promotions"]:
            if record["producer_legal"] and record["review_source"] != "HUMAN_REVIEW_INTAKE_RESULT":
                fail("FAKE_HUMAN_REVIEW_STATE", record["asset_id"])
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}")
        return 1

    provisional = sum(1 for r in promotion_registry["promotions"] if r["promotion_status"] == "PROVISIONAL_PROMOTED")
    producer_legal = sum(1 for r in promotion_registry["promotions"] if r["producer_legal"])
    print(
        "MATH M-G PCK contracts PASS "
        f"(candidates={len(candidate_assets)} promotions={len(promotion_registry['promotions'])} "
        f"provisional={provisional} producer_legal={producer_legal})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
