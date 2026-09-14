#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import fail, load, validate_schema

POLICY_PATH = HERE.parent / "policies" / "math-technical-composition-policy.json"


def _content_blocks(page: dict):
    for block in page.get("technical_blocks", []):
        yield block
    for block in page.get("prose_blocks", []):
        yield block


def validate_page_blueprint(doc: dict) -> None:
    validate_schema(doc, "math-learner-page-blueprint.schema.json")
    policy = load(POLICY_PATH)

    if policy.get("subject") != "MATHEMATICS":
        fail("MATH_TECHNICAL_COMPOSITION_POLICY_SUBJECT_DRIFT")
    if not all(policy.get("principles", {}).values()):
        fail("MATH_TECHNICAL_COMPOSITION_POLICY_WEAKENED")

    seen_page_ids = set()
    signatures = defaultdict(list)

    for page in doc["pages"]:
        page_id = page["page_id"]
        if page_id in seen_page_ids:
            fail("MATH_PAGE_ID_DUPLICATE", page_id)
        seen_page_ids.add(page_id)

        pagination = page["pagination"]
        if pagination["manual_spacers_used"]:
            fail("MATH_MANUAL_SPACER_PADDING_FORBIDDEN", page_id)
        if pagination["mode"] == "FLOW" and pagination["break_reason"] is not None:
            fail("MATH_FLOW_PAGE_CANNOT_CARRY_BREAK_REASON", page_id)
        if pagination["mode"] == "PEDAGOGIC_BREAK" and not pagination["break_reason"]:
            fail("MATH_PEDAGOGIC_BREAK_REASON_REQUIRED", page_id)

        if page["page_kind"] == "COVER":
            continue

        stage = page["stage"]
        stage_policy = policy["page_requirements"][stage]
        if page["page_kind"] not in stage_policy["allowed_page_kinds"]:
            fail("MATH_PAGE_KIND_STAGE_MISMATCH", f"{page_id}:{stage}:{page['page_kind']}")

        technical = page["technical_blocks"]
        if not technical:
            fail("MATH_PROSE_ONLY_PAGE_FORBIDDEN", page_id)
        kinds = {block["kind"] for block in technical}
        missing_all = set(stage_policy["required_all"]) - kinds
        if missing_all:
            fail("MATH_PAGE_REQUIRED_TECHNICAL_BLOCK_MISSING", f"{page_id}:{','.join(sorted(missing_all))}")
        required_any = set(stage_policy["required_any"])
        if required_any and not (required_any & kinds):
            fail("MATH_PAGE_TECHNICAL_PAYLOAD_MISSING", page_id)

        if stage in {"CORE1B", "CORE2B"} and not page["workspace_blocks"]:
            fail("MATH_OPEN_TUTOR_WORKSPACE_REQUIRED", page_id)

        for rep in page["representations"]:
            if rep["clip_to_viewport"] is not True:
                fail("MATH_REPRESENTATION_VIEWPORT_CLIP_REQUIRED", rep["representation_id"])
            vp = rep["viewport"]
            if vp["x"] + vp["width"] > 1 or vp["y"] + vp["height"] > 1:
                fail("MATH_REPRESENTATION_VIEWPORT_OUT_OF_PAGE", rep["representation_id"])
            if not rep["semantic_geometry_refs"]:
                fail("MATH_REPRESENTATION_SEMANTIC_GEOMETRY_REQUIRED", rep["representation_id"])

        for block in _content_blocks(page):
            if not block["math_refs"]:
                fail("MATH_CONTENT_MUST_BIND_MATHEMATICS", block["block_id"])
            upstream = block["upstream_ref"]
            transform = block["transformation"]
            if upstream is not None and transform == "NONE":
                fail("MATH_DOWNSTREAM_CONTENT_TRANSFORMATION_REQUIRED", block["block_id"])
            signatures[block["content_signature"]].append(
                {
                    "stage": stage,
                    "block_id": block["block_id"],
                    "role": block["content_role"],
                    "upstream_ref": upstream,
                    "transformation": transform,
                }
            )

    allowed_repeat = set(policy["allowed_cross_core_repeat_roles"])
    for signature, rows in signatures.items():
        stages = {row["stage"] for row in rows}
        if len(stages) < 2:
            continue
        if any(row["role"] not in allowed_repeat for row in rows):
            fail("MATH_CROSS_CORE_NARRATIVE_DUPLICATION_FORBIDDEN", signature)
        first = rows[0]
        for row in rows[1:]:
            if row["transformation"] != "IMMUTABLE_CARRY":
                fail("MATH_ALLOWED_REPEAT_MUST_DECLARE_IMMUTABLE_CARRY", row["block_id"])
            if row["upstream_ref"] is None:
                fail("MATH_ALLOWED_REPEAT_MUST_REFERENCE_UPSTREAM", row["block_id"])

    badge = doc["difficulty_badge"]
    rows_by_key = {}
    for row in doc["depth_obligations"]:
        key = (row["stage"], row["badge"], row["obligation_id"])
        if key in rows_by_key:
            fail("MATH_DEPTH_OBLIGATION_DUPLICATE", ":".join(key))
        rows_by_key[key] = row
        if row["badge"] != badge:
            fail("MATH_DEPTH_OBLIGATION_BADGE_DRIFT", ":".join(key))
        if row["disposition"] == "SATISFIED":
            if not row["evidence_refs"]:
                fail("MATH_DEPTH_OBLIGATION_EVIDENCE_REQUIRED", row["obligation_id"])
            if row["not_applicable_reason"] is not None:
                fail("MATH_SATISFIED_OBLIGATION_CANNOT_HAVE_NA_REASON", row["obligation_id"])
        else:
            if row["evidence_refs"]:
                fail("MATH_NA_OBLIGATION_CANNOT_CARRY_EVIDENCE", row["obligation_id"])
            if not row["not_applicable_reason"]:
                fail("MATH_NA_OBLIGATION_REASON_REQUIRED", row["obligation_id"])

    for stage in ("CORE1A", "CORE1B"):
        expected = policy["depth_obligations"][stage][badge]
        for obligation in expected:
            key = (stage, badge, obligation["id"])
            row = rows_by_key.get(key)
            if row is None:
                fail("MATH_DEPTH_OBLIGATION_MISSING", ":".join(key))
            if obligation["required"] and row["disposition"] != "SATISFIED":
                fail("MATH_REQUIRED_DEPTH_OBLIGATION_MUST_BE_SATISFIED", ":".join(key))

        expected_ids = {x["id"] for x in expected}
        supplied_ids = {
            row["obligation_id"]
            for row in doc["depth_obligations"]
            if row["stage"] == stage and row["badge"] == badge
        }
        extras = supplied_ids - expected_ids
        if extras:
            fail("MATH_UNKNOWN_DEPTH_OBLIGATION", f"{stage}:{','.join(sorted(extras))}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate Mathematics technical depth and learner-page composition blueprint.")
    ap.add_argument("--input", required=True)
    args = ap.parse_args()
    doc = load(args.input)
    validate_page_blueprint(doc)
    print(json.dumps({
        "status": "PASS",
        "blueprint_id": doc["blueprint_id"],
        "pages": len(doc["pages"]),
        "difficulty_badge": doc["difficulty_badge"],
    }, indent=2))


if __name__ == "__main__":
    main()
