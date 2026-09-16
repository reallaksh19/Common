#!/usr/bin/env python3
"""Governed example admission for Mathematics Core1A.

Legacy capability/family banks are treated only as candidate material. In a bound
run they are compiled into immutable governed-example assets first; learner
manuscript authoring consumes those admitted assets, not raw bank objects.

This is an incremental migration boundary. The next migration can relocate the
candidate source out of Python without changing the learner-product contract.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

import build_math_core1a_textbook as base
import core1a_capability_authoring as capability

_ACTIVE_REGISTRY: dict | None = None
_CATALOG: dict[str, dict] = {}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _capability_registry_refs(capability_ref: str) -> list[str]:
    if _ACTIVE_REGISTRY is None:
        return []
    refs = []
    for asset in _ACTIVE_REGISTRY.get("assets", []):
        if asset.get("asset_type") != "CAPABILITY":
            continue
        if capability_ref in asset.get("core1_refs", []):
            refs.append(asset["asset_id"])
    if not refs:
        base.fail("CORE1A_GOVERNED_EXAMPLE_CAPABILITY_NOT_IN_REGISTRY", capability_ref)
    return sorted(set(refs))


def _admit(capability_ref: str, family_ref: str, ordinal: int, item: Any) -> dict:
    payload = {
        "capability_ref": capability_ref,
        "family_ref": family_ref,
        "ordinal": ordinal,
        "prompt": str(item.prompt).strip(),
        "solution_steps": [str(x).strip() for x in item.steps],
        "answer": str(item.answer).strip(),
        "hints": [str(x).strip() for x in item.hints],
    }
    if not payload["prompt"] or not payload["answer"] or not payload["solution_steps"]:
        base.fail("CORE1A_GOVERNED_EXAMPLE_INCOMPLETE", f"{capability_ref}:{ordinal}")
    if len(payload["hints"]) != 3 or any(not x for x in payload["hints"]):
        base.fail("CORE1A_GOVERNED_EXAMPLE_HINT_CONTRACT", f"{capability_ref}:{ordinal}")
    content_digest = digest(payload)
    asset_id = "GEX-MATH-" + content_digest[:20].upper()
    row = {
        "example_asset_id": asset_id,
        "asset_type": "GOVERNED_EXAMPLE",
        "admission_status": "ADMITTED",
        "content_digest": content_digest,
        "capability_registry_refs": _capability_registry_refs(capability_ref),
        **payload,
    }
    existing = _CATALOG.get(asset_id)
    if existing is not None and existing != row:
        base.fail("CORE1A_GOVERNED_EXAMPLE_ID_COLLISION", asset_id)
    _CATALOG[asset_id] = row
    return row


def governed_bank(capability_ref: str, family_ref: str | None) -> list[dict]:
    if not family_ref:
        return []
    raw = capability.capability_bank(capability_ref, family_ref)
    rows = [_admit(capability_ref, family_ref, i + 1, item) for i, item in enumerate(raw)]
    if len(rows) < 6:
        base.fail("CORE1A_GOVERNED_EXAMPLE_DEPTH_INCOMPLETE", capability_ref)
    digests = [x["content_digest"] for x in rows]
    if len(digests) != len(set(digests)):
        base.fail("CORE1A_GOVERNED_EXAMPLE_DUPLICATE", capability_ref)
    return rows


def _practice(rows: list[dict], lesson: dict) -> dict[str, dict]:
    index_for = {"WORKED": 0, "GUIDED": 2, "FADED": 3, "INDEPENDENT": 4, "TRANSFER": 5, "VERIFY": 4}
    out: dict[str, dict] = {}
    for plan in lesson.get("problem_authoring_plans", []):
        role = plan["instance_role"]
        if role not in index_for:
            base.fail("CORE1A_UNKNOWN_INSTANCE_ROLE", role)
        item = rows[index_for[role]]
        out[role] = {
            "prompt": item["prompt"],
            "solution_steps": list(item["solution_steps"]),
            "answer": item["answer"],
            "hints": list(item["hints"]),
            "source_class": "GOVERNED_CORE1A_EXAMPLE",
            "governed_example_asset_ref": item["example_asset_id"],
            "content_digest": item["content_digest"],
        }
    return out


def authored_lesson(lesson: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    family_id = base.choose_family(lesson)
    cap = lesson["capability_ref"]
    asset = capability.choose_asset_for_capability(lesson, assets)
    family = families.get(family_id) if family_id else None
    full = lesson["treatment"] in base.FULL_TREATMENTS

    if full and not family_id:
        base.fail("CORE1A_PROBLEM_FAMILY_REQUIRED", lesson["lesson_id"])
    if full and family_id not in base.FAMILY_BANKS:
        base.fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id or lesson["lesson_id"])

    rows = governed_bank(cap, family_id) if family_id else []
    practice = _practice(rows, lesson) if rows else {}
    title = capability.CAPABILITY_TITLES.get(cap, lesson.get("learner_title") or base.humanize_code(cap))

    recognition = []
    if family:
        recognition = [base.sentence(x) for x in family.get("problem_signature", {}).get("recognition_cues", [])]
    ordinary = base.sentence(asset.get("ordinary_language_bridge", "")) if asset else ""
    anchor = base.sentence(asset.get("anchor", "")) if asset else ""
    route = base.public_route(asset, family)

    mistake = ""
    repair = []
    if asset:
        wrong = asset.get("misconception_discriminator", {}).get("candidate_wrong_model", "")
        probe = asset.get("misconception_discriminator", {}).get("probe", "")
        if wrong:
            mistake = base.sentence(wrong) + ((" " + base.sentence(probe)) if probe else "")
        repair = [base.sentence(x) for x in asset.get("repair_route", [])]
    elif family and family.get("common_invalid_mechanisms"):
        wrong_row = family["common_invalid_mechanisms"][0]
        mistake = base.sentence(wrong_row.get("invalid_move", "")) + " " + base.sentence(wrong_row.get("why_invalid", ""))

    verification = []
    if asset:
        verification.extend(base.sentence(x) for x in asset.get("verification_method", []))
    verification.extend(base.public_phrase(x) for x in lesson.get("verification_requirements", []))
    verification = list(dict.fromkeys(x for x in verification if x))

    worked = []
    if full:
        for item in rows[:2]:
            worked.append({
                "prompt": item["prompt"],
                "steps": list(item["solution_steps"]),
                "answer": item["answer"],
                "governed_example_asset_ref": item["example_asset_id"],
                "content_digest": item["content_digest"],
            })

    governed_refs = [x["example_asset_id"] for x in rows]
    return {
        "lesson_id": lesson["lesson_id"],
        "title": title,
        "treatment": lesson["treatment"],
        "family_ref": family_id,
        "opening": ordinary or "Begin by identifying the mathematical roles before calculating.",
        "concept_explanation": anchor or (base.sentence(family.get("problem_signature", {}).get("target_job", "")) if family else ""),
        "what_to_notice": recognition,
        "why_it_works": route,
        "common_mistake": mistake,
        "repair": repair,
        "worked_examples": worked,
        "practice": practice,
        "verification": verification,
        "source_trace": {
            "core1_lesson_ref": lesson["lesson_id"],
            "assessment_question_refs": list(lesson.get("assessment_question_refs", [])),
            "pck_asset_refs": list(lesson.get("pck_asset_refs", [])),
            "governed_example_asset_refs": governed_refs,
        },
    }


def install(registry: dict) -> None:
    global _ACTIVE_REGISTRY, _CATALOG
    _ACTIVE_REGISTRY = copy.deepcopy(registry)
    _CATALOG = {}
    base.authored_lesson = authored_lesson


def catalog_document() -> dict:
    rows = sorted(_CATALOG.values(), key=lambda x: (x["capability_ref"], x["ordinal"], x["example_asset_id"]))
    doc = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "catalog_role": "GOVERNED_CORE1A_EXAMPLE_ADMISSION",
        "examples": rows,
    }
    doc["catalog_digest"] = digest(doc)
    return doc
