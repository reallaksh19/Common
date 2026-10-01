#!/usr/bin/env python3
"""Fail-closed validators for Chemistry LearningBlueprint v4 control contracts.

v4 deliberately separates two control systems:
- Core1A/Core1B depth is controlled by intrinsic subtopic difficulty.
- Core2A/Core2B support is controlled by a learner knowledge prior or explicit owner override.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class BlueprintV4Error(ValueError):
    pass


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def validate_instruction_bucket(bucket: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version", "bucket_id", "subject", "subtopic_id", "title",
        "difficulty_badge", "page_envelope", "research", "visual_plan",
        "decomposition", "realization_modes",
    }
    missing = sorted(required - set(bucket))
    if missing:
        raise BlueprintV4Error(f"CHEM_V4_BUCKET_REQUIRED_FIELD_MISSING:{','.join(missing)}")
    if bucket["schema_version"] != "4.0.0" or bucket["subject"] != "CHEMISTRY":
        raise BlueprintV4Error("CHEM_V4_BUCKET_IDENTITY_INVALID")

    forbidden = {"student_knowledge_percent", "knowledge_percent", "learner_readiness_percent"}
    leaked = sorted(forbidden & set(_walk_keys(bucket)))
    if leaked:
        raise BlueprintV4Error(f"CHEM_V4_CORE1_KNOWLEDGE_CONTAMINATION:{','.join(leaked)}")

    badge = bucket["difficulty_badge"]
    rules = {
        "EASY": (10, "OPTIONAL", 1),
        "MEDIUM": (20, "REQUIRED", 1),
        "HARD": (30, "DEEP_REQUIRED", 2),
    }
    if badge not in rules:
        raise BlueprintV4Error("CHEM_V4_BUCKET_DIFFICULTY_INVALID")
    max_allowed, research_mode, min_visual_jobs = rules[badge]

    envelope = bucket["page_envelope"]
    pages = envelope.get("max_pages")
    if not isinstance(pages, int) or pages < 1 or pages > max_allowed:
        raise BlueprintV4Error("CHEM_V4_BUCKET_PAGE_ENVELOPE_INVALID")
    if envelope.get("is_ceiling_not_quota") is not True:
        raise BlueprintV4Error("CHEM_V4_BUCKET_PAGE_QUOTA_FORBIDDEN")

    research = bucket["research"]
    if research.get("mode") != research_mode:
        raise BlueprintV4Error("CHEM_V4_BUCKET_RESEARCH_MODE_INVALID")
    refs = research.get("research_refs", [])
    if badge == "MEDIUM" and len(refs) < 1:
        raise BlueprintV4Error("CHEM_V4_MEDIUM_RESEARCH_MISSING")
    if badge == "HARD":
        if len(refs) < 2 or len(research.get("research_questions", [])) < 2:
            raise BlueprintV4Error("CHEM_V4_HARD_DEEP_RESEARCH_MISSING")

    visual_jobs = bucket["visual_plan"].get("visual_jobs", [])
    if len(set(visual_jobs)) < min_visual_jobs:
        raise BlueprintV4Error("CHEM_V4_BUCKET_VISUAL_JOB_CLOSURE_MISSING")

    decomp = bucket["decomposition"]
    decision = decomp.get("decision")
    ids = decomp.get("sub_subtopic_ids", [])
    if decision == "SPLIT" and len(ids) < 2:
        raise BlueprintV4Error("CHEM_V4_BUCKET_SPLIT_INCOMPLETE")
    if decision == "NOT_NEEDED" and ids:
        raise BlueprintV4Error("CHEM_V4_BUCKET_UNDECLARED_SPLIT")
    if decision not in {"SPLIT", "NOT_NEEDED"}:
        raise BlueprintV4Error("CHEM_V4_BUCKET_DECOMPOSITION_INVALID")

    if bucket["realization_modes"] != ["CORE1A", "CORE1B"]:
        raise BlueprintV4Error("CHEM_V4_BUCKET_REALIZATION_PAIR_INVALID")

    return {
        "status": "PASS",
        "control_axis": "INTRINSIC_SUBTOPIC_DIFFICULTY",
        "difficulty_badge": badge,
        "max_pages": pages,
        "research_mode": research_mode,
        "learner_knowledge_used": False,
    }


def _resolve_band(percent: float, policy: dict[str, Any]) -> dict[str, Any]:
    bands = policy["core2_policy"]["default_support_bands"]
    for band in bands:
        if band["min_inclusive"] <= percent <= band["max_inclusive"]:
            return {
                key: value
                for key, value in band.items()
                if key not in {"min_inclusive", "max_inclusive"}
            }
    raise BlueprintV4Error("CHEM_V4_KNOWLEDGE_BAND_UNRESOLVED")


def validate_core2_conditioning(conditioning: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    if conditioning.get("schema_version") != "4.0.0":
        raise BlueprintV4Error("CHEM_V4_CONDITIONING_SCHEMA_INVALID")
    mode = conditioning.get("mode")
    if mode == "KNOWLEDGE_PERCENT":
        if "owner_override" in conditioning:
            raise BlueprintV4Error("CHEM_V4_CONDITIONING_DUAL_AUTHORITY")
        percent = conditioning.get("knowledge_percent")
        if not isinstance(percent, (int, float)) or isinstance(percent, bool) or percent < 0 or percent > 100:
            raise BlueprintV4Error("CHEM_V4_KNOWLEDGE_PERCENT_INVALID")
        return {
            "status": "PASS",
            "mode": mode,
            "knowledge_percent": percent,
            "knowledge_interpretation": "SUPPORT_PRIOR_NOT_MASTERY_MEASUREMENT",
            "resolved_support_profile": _resolve_band(float(percent), policy),
        }

    if mode == "OWNER_OVERRIDE":
        if "knowledge_percent" in conditioning:
            raise BlueprintV4Error("CHEM_V4_CONDITIONING_DUAL_AUTHORITY")
        override = conditioning.get("owner_override")
        if not isinstance(override, dict):
            raise BlueprintV4Error("CHEM_V4_OWNER_OVERRIDE_MISSING")
        if not str(override.get("reason", "")).strip():
            raise BlueprintV4Error("CHEM_V4_OWNER_OVERRIDE_REASON_MISSING")
        if not isinstance(override.get("support_profile"), dict) or not isinstance(override.get("demand_profile"), dict):
            raise BlueprintV4Error("CHEM_V4_OWNER_OVERRIDE_PROFILE_MISSING")
        return {
            "status": "PASS",
            "mode": mode,
            "owner_override_auditable": True,
            "resolved_support_profile": override["support_profile"],
            "resolved_demand_profile": override["demand_profile"],
        }

    raise BlueprintV4Error("CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--bucket")
    parser.add_argument("--conditioning")
    args = parser.parse_args()

    if bool(args.bucket) == bool(args.conditioning):
        raise SystemExit("supply exactly one of --bucket or --conditioning")

    policy = json.loads(Path(args.policy).read_text(encoding="utf-8"))
    if args.bucket:
        payload = json.loads(Path(args.bucket).read_text(encoding="utf-8"))
        result = validate_instruction_bucket(payload)
    else:
        payload = json.loads(Path(args.conditioning).read_text(encoding="utf-8"))
        result = validate_core2_conditioning(payload, policy)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
