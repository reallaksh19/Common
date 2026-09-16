#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import fail, load, validate_schema

POLICY_PATH = HERE.parent / "policies" / "math-self-teaching-policy.json"


def derived_difficulty(dimensions: dict) -> tuple[float, str]:
    score = round(sum(dimensions.values()) / (4 * len(dimensions)) * 100, 2)
    badge = "EASY" if score <= 32 else "MEDIUM" if score <= 65 else "HARD"
    return score, badge


def validate_generation_spec(doc: dict) -> None:
    validate_schema(doc, "math-self-teaching-generation-spec.schema.json")
    policy = load(POLICY_PATH)
    depth = policy["generation_governance"]["core1_series"]["difficulty_badges"]

    seen_buckets = set()
    for bucket in doc["core1_buckets"]:
        if bucket["bucket_id"] in seen_buckets:
            fail("MATH_CORE1_DUPLICATE_BUCKET_ID", bucket["bucket_id"])
        seen_buckets.add(bucket["bucket_id"])

        badge = bucket["difficulty_badge"]
        rules = depth[badge]
        _, derived_badge = derived_difficulty(bucket["difficulty_dimensions"])
        if bucket["difficulty_badge_basis"] == "CORE1_SEMANTIC_COMPLEXITY" and badge != derived_badge:
            fail("MATH_CORE1_DERIVED_DIFFICULTY_BADGE_MISMATCH", f"{bucket['bucket_id']}:{badge}!={derived_badge}")

        if bucket["target_page_budget"] > rules["max_pages"]:
            fail("MATH_CORE1_BUCKET_PAGE_BUDGET_EXCEEDED", bucket["bucket_id"])

        refs = bucket["pedagogy_web_research_refs"]
        brief = bucket["pedagogy_research_brief_ref"]
        research_mode = rules["pedagogy_web_research"]
        if research_mode == "REQUIRED":
            if not refs or not brief:
                fail("MATH_CORE1_RESEARCH_EVIDENCE_INSUFFICIENT", bucket["bucket_id"])
        elif research_mode == "OPTIONAL":
            if bool(refs) != (brief is not None):
                fail("MATH_CORE1_OPTIONAL_RESEARCH_BINDING_INCOMPLETE", bucket["bucket_id"])
        else:
            fail("MATH_CORE1_RESEARCH_POLICY_INVALID", f"{badge}:{research_mode}")

        if not rules["subsubtopic_decomposition_allowed"] and bucket["subsubtopic_plan"]:
            fail("MATH_CORE1_SUBSUBTOPIC_DECOMPOSITION_FORBIDDEN", bucket["bucket_id"])

    cal = doc["core2_calibration"]
    percent = cal["learner_knowledge_percent"]
    waiver = cal["owner_waiver"]
    has_percent = percent is not None
    has_waiver = waiver is not None

    if has_percent == has_waiver:
        fail("MATH_CORE2_CALIBRATION_EXACTLY_ONE_REQUIRED")

    cap_rows = cal["capability_knowledge"]
    cap_refs = [row["capability_ref"] for row in cap_rows]
    if len(cap_refs) != len(set(cap_refs)):
        fail("MATH_CORE2_CAPABILITY_KNOWLEDGE_DUPLICATE")

    if has_percent:
        if not cal["knowledge_percent_source_ref"] or not cal["knowledge_calibration_policy_ref"]:
            fail("MATH_CORE2_KNOWLEDGE_PERCENT_BINDING_INCOMPLETE")
        if not cap_rows:
            fail("MATH_CORE2_CAPABILITY_KNOWLEDGE_REQUIRED")
    else:
        if cal["knowledge_percent_source_ref"] is not None or cal["knowledge_calibration_policy_ref"] is not None:
            fail("MATH_CORE2_WAIVER_CANNOT_FAKE_KNOWLEDGE_BINDING")
        if cap_rows:
            fail("MATH_CORE2_WAIVER_CANNOT_FAKE_CAPABILITY_KNOWLEDGE")
        if cal["resolved_core2a_support_profile"] != waiver["selected_core2a_support_profile"]:
            fail("MATH_CORE2_OWNER_WAIVER_SUPPORT_DRIFT")
        if cal["resolved_core2a_max_demand_level"] != waiver["selected_core2a_max_demand_level"]:
            fail("MATH_CORE2_OWNER_WAIVER_CORE2A_CEILING_DRIFT")
        if cal["resolved_core2b_max_demand_level"] != waiver["selected_core2b_max_demand_level"]:
            fail("MATH_CORE2_OWNER_WAIVER_CORE2B_CEILING_DRIFT")


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate Mathematics self-teaching generation calibration.")
    ap.add_argument("--input", required=True)
    args = ap.parse_args()
    doc = load(args.input)
    validate_generation_spec(doc)
    print(json.dumps({
        "status": "PASS",
        "core1_buckets": len(doc["core1_buckets"]),
        "core2_calibration": "KNOWLEDGE_PERCENT" if doc["core2_calibration"]["learner_knowledge_percent"] is not None else "OWNER_WAIVER",
        "core2a_support_profile": doc["core2_calibration"]["resolved_core2a_support_profile"],
        "core2a_max_demand_level": doc["core2_calibration"]["resolved_core2a_max_demand_level"],
        "core2b_max_demand_level": doc["core2_calibration"]["resolved_core2b_max_demand_level"],
    }, indent=2))


if __name__ == "__main__":
    main()
