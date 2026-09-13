#!/usr/bin/env python3
"""Validate the Grade 4 English golden child-page lesson plan."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_PAGE_ROLES = {"NOTICE", "UNDERSTAND", "WATCH_ONE", "TRY_ONE", "BOUNDARY", "FRESH_RETRY", "TRANSFER", "REVIEW"}
ALLOWED_MOVES = {"NOTICE", "EXPLAIN", "MODEL", "CLASSIFY", "ORDER", "REPAIR", "APPLY", "REVIEW"}
ALLOWED_RESPONSE_SPACE = {"NONE", "SMALL", "MEDIUM", "LARGE", "FULL_WIDTH", "HALF_PAGE"}
TEACHING_ROLES = {"NOTICE", "UNDERSTAND", "WATCH_ONE", "BOUNDARY"}
INTERNAL_LABELS = {
    "SOURCE_MODEL_BOUNDARY",
    "SOURCE_UNRESOLVED",
    "OUTSIDE_CANONICAL_KNOWLEDGE",
    "DERIVED_STUDY_MATERIAL_ASSERTION",
    "OWNER_OR_TEACHER_SUPPLIED_RULE",
    "OWNER_CONFIRMED_PENDING_PRIMARY_SOURCE",
}


class ContractError(Exception):
    pass


def fail(code: str, detail: str) -> None:
    raise ContractError(f"{code}: {detail}")


def words(text: str) -> int:
    return len([part for part in text.replace("->", " ").split() if part])


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            # authority/internal metadata inside data records is allowed; only child-visible fields are checked separately
            if key in {"placement_authority", "authority", "verification_status", "model_id"}:
                continue
            yield from walk_strings(item)


def validate(payload: dict) -> None:
    profile = payload["output_profile"]
    load = payload["child_load"]
    model = payload["school_model"]
    pages = payload["pages"]

    if profile.get("body_pt", 0) < 10.5 or profile.get("question_pt", 0) < 11:
        fail("TEXT_BELOW_SHARED_MINIMUM", "body/question type is below Grade 4 publishing minimum")

    if model.get("immutable_for_episode") is not True:
        fail("MODEL_NOT_FROZEN", "school model must be immutable for the lesson")
    if model.get("categories") != model.get("order"):
        fail("MODEL_ORDER_MISMATCH", "golden fixture requires categories and order to match exactly")

    category_ids = [card["id"] for card in payload.get("category_cards", [])]
    if category_ids != model["categories"]:
        fail("CATEGORY_CARD_DRIFT", "category cards must exactly match the frozen school model")

    if not pages:
        fail("NO_PAGES", "golden lesson has no pages")

    page_ids = set()
    has_boundary = False
    has_fresh_retry = False
    has_review = False

    for page in pages:
        page_id = page.get("page_id", "<missing-page-id>")
        if page_id in page_ids:
            fail("DUPLICATE_PAGE_ID", page_id)
        page_ids.add(page_id)

        if page.get("page_role") not in ALLOWED_PAGE_ROLES:
            fail("INVALID_PAGE_ROLE", f"{page_id}: {page.get('page_role')}")
        if page.get("dominant_move") not in ALLOWED_MOVES:
            fail("MULTIPLE_DOMINANT_MOVES", f"{page_id}: missing or invalid dominant_move")
        if not isinstance(page.get("dominant_move"), str):
            fail("MULTIPLE_DOMINANT_MOVES", page_id)

        if page.get("new_rules", 0) > load["max_new_rules"]:
            fail("TOO_MANY_NEW_RULES", page_id)

        chunks = page.get("explanation_chunks") or []
        if len(chunks) > load["max_explanation_chunks"]:
            fail("TOO_MANY_EXPLANATION_CHUNKS", page_id)

        action = page.get("action")
        if load.get("require_learner_action") and not action:
            fail("MISSING_LEARNER_ACTION", page_id)
        if action:
            instruction = action.get("instruction", "")
            if words(instruction) > load["max_instruction_words"]:
                fail("INSTRUCTION_TOO_LONG", f"{page_id}: {words(instruction)} words")
            if action.get("response_space") not in ALLOWED_RESPONSE_SPACE:
                fail("MISSING_RESPONSE_SPACE", page_id)

        if page.get("page_role") in TEACHING_ROLES and load.get("require_instructional_visual_on_teaching_pages"):
            if not page.get("instructional_visual"):
                fail("MISSING_INSTRUCTIONAL_VISUAL", page_id)

        child_visible = {
            "title": page.get("title", ""),
            "goal": page.get("goal", ""),
            "explanation_chunks": chunks,
            "action": action or {},
            "instructional_visual": page.get("instructional_visual") or {},
        }
        for text in walk_strings(child_visible):
            for label in INTERNAL_LABELS:
                if label in text:
                    fail("INTERNAL_LABEL_LEAKED_TO_CHILD_SURFACE", f"{page_id}: {label}")

        visual = page.get("instructional_visual") or {}
        if visual.get("type") == "BOUNDARY_PHRASE":
            has_boundary = True
            for item in visual.get("items", []):
                if item.get("boundary"):
                    if item.get("category") is not None:
                        fail("BOUNDARY_RENDERED_AS_CATEGORY", f"{page_id}/{item.get('word')}")
                    authority = item.get("placement_authority")
                    if not authority or authority == "SOURCE_UNRESOLVED":
                        fail("BOUNDARY_PLACEMENT_UNRESOLVED", f"{page_id}/{item.get('word')}")

        if page.get("page_role") == "FRESH_RETRY":
            has_fresh_retry = True
        if page.get("page_role") == "REVIEW":
            has_review = True
            if not any("3-7 days" in chunk for chunk in chunks):
                fail("MISSING_DELAYED_RETRIEVAL", page_id)

    if not has_boundary:
        fail("MISSING_BOUNDARY_PAGE", "golden lesson must render at least one star-word boundary")
    if not has_fresh_retry:
        fail("MISSING_FRESH_RETRY", "golden lesson must include a fresh retry page")
    if not has_review:
        fail("MISSING_REVIEW", "golden lesson must include review/delayed retrieval")


def main() -> int:
    fixture = Path(__file__).parents[1] / "Golden" / "adjective-golden-lesson.v1.draft.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    validate(payload)
    print(f"PASS: child page contract ({len(payload['pages'])} golden pages)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
