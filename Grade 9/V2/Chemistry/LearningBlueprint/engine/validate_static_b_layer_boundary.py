#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_blueprint_v4 import BlueprintV4Error, validate_core2_conditioning, validate_instruction_bucket

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "policies" / "static-b-layer-boundary.v1.json"
V4_POLICY_PATH = ROOT / "policies" / "v4-bucket-and-conditioning-policy.json"


class StaticBLayerBoundaryError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise StaticBLayerBoundaryError(code, message)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def _base_checks(payload: dict[str, Any], policy: dict[str, Any]) -> None:
    if payload.get("subject") != policy["subject"] or payload.get("delivery_mode") != policy["delivery_mode"]:
        fail("CHEM_B_STATIC_BOUNDARY_INVALID")
    leaked = sorted(set(policy["forbidden_runtime_fields"]) & set(walk_keys(payload)))
    if leaked:
        fail("CHEM_B_LIVE_RUNTIME_FIELD_PRESENT", ",".join(leaked))
    if payload.get("new_chemistry_refs"):
        fail("CHEM_B_NEW_CHEMISTRY_INTRODUCED")


def validate_core1b(payload: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load(POLICY_PATH)
    _base_checks(payload, policy)
    cfg = policy["core1b"]

    leaked = sorted(set(cfg["forbidden_knowledge_fields"]) & set(walk_keys(payload)))
    if leaked:
        fail("CHEM_CORE1B_KNOWLEDGE_CONTAMINATION", ",".join(leaked))

    bucket = payload.get("instruction_bucket")
    if not isinstance(bucket, dict):
        fail("CHEM_CORE1B_BLUEPRINT_V4_BUCKET_REQUIRED")
    try:
        bucket_authority = validate_instruction_bucket(bucket)
    except BlueprintV4Error as exc:
        fail(str(exc).split(":", 1)[0], str(exc))

    capability = payload.get("capability_ref")
    family = payload.get("problem_family_ref")
    if capability not in set(payload.get("approved_capability_refs", [])):
        fail("CHEM_CORE1B_AUTHORITY_SCOPE_VIOLATION", "capability_ref")
    if family not in set(payload.get("approved_problem_family_refs", [])):
        fail("CHEM_CORE1B_AUTHORITY_SCOPE_VIOLATION", "problem_family_ref")

    for field in cfg["answer_closure_required"]:
        if not str(payload.get(field, "")).strip():
            fail("CHEM_CORE1B_ANSWER_CLOSURE_MISSING", field)

    if payload.get("help_mode") != cfg["help_mode"]:
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")
    rows = payload.get("help")
    if not isinstance(rows, list) or not rows:
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")
    allowed = cfg["help_order"]
    levels = [row.get("level") for row in rows if isinstance(row, dict)]
    if len(levels) != len(rows) or any(level not in allowed for level in levels):
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")
    ranks = [allowed.index(level) for level in levels]
    if ranks != sorted(ranks) or len(set(ranks)) != len(ranks):
        fail("CHEM_CORE1B_HELP_ORDER_INVALID")

    return {
        "status": "PASS",
        "product_mode": "CORE1B",
        "delivery_mode": "STATIC",
        "control_axis": cfg["control_axis"],
        "difficulty_badge": bucket_authority["difficulty_badge"],
        "page_envelope_max": bucket_authority["max_pages"],
        "research_mode": bucket_authority["research_mode"],
        "learner_knowledge_used_for_depth": False,
        "new_chemistry_refs": [],
        "answer_closure": "PASS",
    }


def validate_core2b(payload: dict[str, Any], policy: dict[str, Any] | None = None, v4_policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load(POLICY_PATH)
    v4_policy = v4_policy or load(V4_POLICY_PATH)
    _base_checks(payload, policy)
    cfg = policy["core2b"]

    conditioning = payload.get("learner_conditioning")
    if not isinstance(conditioning, dict):
        fail("CHEM_CORE2_LEARNER_CONDITION_UNRESOLVED")
    try:
        resolved = validate_core2_conditioning(conditioning, v4_policy)
    except BlueprintV4Error as exc:
        fail(str(exc).split(":", 1)[0], str(exc))

    support = resolved.get("resolved_support_profile", {})
    allowed_help = cfg["help_order"]
    entry = support.get("hint_entry_level")
    max_entry = allowed_help.index(cfg["support_hint_entry_may_not_start_after"])
    if entry not in allowed_help or allowed_help.index(entry) > max_entry:
        fail("CHEM_CORE2B_SUPPORT_PROFILE_INVALID", "hint_entry_level")
    if support.get("solution_delay") not in set(cfg["allowed_solution_delay"]):
        fail("CHEM_CORE2B_SUPPORT_PROFILE_INVALID", "solution_delay")

    selected = payload.get("selected_item_id")
    if selected not in set(payload.get("legal_core2a_item_ids", [])):
        fail("CHEM_CORE2B_ITEM_NOT_CORE2A_LEGAL")
    source = payload.get("source_item")
    if not isinstance(source, dict) or source.get("item_id") != selected:
        fail("CHEM_CORE2B_SOURCE_IDENTITY_DRIFT", "item_id")
    for field in cfg["required_source_identity_fields"]:
        if not str(source.get(field, "")).strip():
            fail("CHEM_CORE2B_SOURCE_IDENTITY_DRIFT", field)
    if payload.get("question_mode") != cfg["question_mode"]:
        fail("CHEM_CORE2B_SOURCE_IDENTITY_DRIFT", "question_mode")

    if payload.get("help_mode") != cfg["help_mode"]:
        fail("CHEM_CORE2B_HELP_ORDER_INVALID")
    rows = payload.get("help")
    if not isinstance(rows, list) or [row.get("level") for row in rows if isinstance(row, dict)] != allowed_help:
        fail("CHEM_CORE2B_HELP_ORDER_INVALID")

    for field in cfg["answer_closure_required"]:
        if not str(payload.get(field, "")).strip():
            fail("CHEM_CORE2B_ANSWER_CLOSURE_MISSING", field)

    result = {
        "status": "PASS",
        "product_mode": "CORE2B",
        "delivery_mode": "STATIC",
        "control_axis": cfg["control_axis"],
        "selected_item_id": selected,
        "conditioning_mode": resolved["mode"],
        "resolved_support_profile": support,
        "new_chemistry_refs": [],
        "answer_closure": "PASS",
        "question_identity_mutable_by_conditioning": False,
    }
    if resolved["mode"] == "KNOWLEDGE_PERCENT":
        result["knowledge_percent"] = resolved["knowledge_percent"]
        result["knowledge_interpretation"] = resolved["knowledge_interpretation"]
    else:
        result["owner_override_auditable"] = True
        result["fabricated_knowledge_percent"] = False
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["CORE1B", "CORE2B"])
    parser.add_argument("payload")
    args = parser.parse_args()
    payload = load(Path(args.payload))
    try:
        result = validate_core1b(payload) if args.mode == "CORE1B" else validate_core2b(payload)
    except StaticBLayerBoundaryError as exc:
        print(json.dumps({"status": "FAIL", "code": exc.code, "message": exc.message}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
