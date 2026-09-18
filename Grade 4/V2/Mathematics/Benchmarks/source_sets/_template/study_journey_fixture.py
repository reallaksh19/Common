"""Document-level StudyJourney template for a copied scanned source set.

Do not turn source order into lesson order mechanically. Group source evidence
into teaching concepts, then choose teach/worked/guided/independent/transfer
blocks deliberately. Any learner-facing question must carry a source/generation
identity, answer contract and explicit hint policy.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source.json"


def B(
    block_id: str,
    block_type: str,
    title: str,
    body: str,
    *,
    visibility: str = "HIDDEN",
    refs: Iterable[str] = (),
    questions: Iterable[Dict[str, Any]] = (),
    solution_text: str = "",
    representation: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "block_id": block_id,
        "block_type": block_type,
        "title": title,
        "body": body,
        "answer_visibility": visibility,
        "source_refs": list(refs),
    }
    qs = list(questions)
    if qs:
        out["questions"] = qs
    if solution_text:
        out["solution_text"] = solution_text
    if representation is not None:
        out["representation"] = representation
    return out


# A SOURCE learner question must retain the complete visible worksheet identity.
# Example shape (replace all values):
# {
#   "question_id": "M1-Q1",
#   "origin": "SOURCE",
#   "display_ref": "I(a)",
#   "prompt": "40 ÷ 5 + 12 = ____",
#   "source_identity": {
#       "source_ref": "Q1",
#       "source_display_ref": "I(a)",
#       "source_text": "40 ÷ 5 + 12 = ____",
#       "source_numeric_tokens": ["40", "5", "12"],
#       "source_asset_ref": "SCAN-001",
#       "source_page_or_image_index": 1,
#       "source_section_label": "I",
#       "source_item_label": "a",
#       "source_issue": null
#   },
#   "task_support_policy": "NUMERIC_FIRST",
#   "answer_contract": {
#       "answer_kind": "EXACT",
#       "answer_text": "20",
#       "check_route": "CHECK_AFTER_TRY",
#       "answer_ref": "ANS-Q1"
#   },
#   "hint_contract": {
#       "modality": "NUMERIC",
#       "hint_text": "40 ÷ 5 = 8. Now use 8 + 12.",
#       "visual_ref": null,
#       "may_reveal_final_answer": false
#   }
# }
#
# Generated questions must use labels such as Practice A / Fresh Try A / Check A
# and must set source_identity=null. They must never reuse source numbering.
#
# Hint policy:
# - NUMERIC_FIRST for arithmetic/procedure: give a small numeric next step.
# - VISUAL_FIRST for structure/geometry: bind to a real representation.
# - MIXED when both are necessary.
# - NO_HINT for a true independent attempt.
#
# Every learner question must have an answer contract even when the answer is
# delayed to an answer map or teacher key.
MODULES: list[Dict[str, Any]] = []


def _source_refs() -> list[str]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if payload.get("template_only") is True:
        raise ValueError("TEMPLATE_NOT_FILLED: source.json")
    refs = [str(row.get("question_ref") or "") for row in payload.get("questions") or []]
    if not refs or any(not ref for ref in refs):
        raise ValueError("SOURCE_QUESTION_REFS_REQUIRED")
    if len(refs) != len(set(refs)):
        raise ValueError("DUPLICATE_SOURCE_QUESTION_REF")
    return refs


def build_study_journey() -> Dict[str, Any]:
    required = _source_refs()
    if not MODULES:
        raise ValueError("TEMPLATE_REQUIRES_STUDY_JOURNEY: synthesize source questions into explicit teaching modules")

    covered = sorted({str(ref) for module in MODULES for ref in (module.get("source_refs") or [])})
    plan = {
        "schema_version": "1.0.0",
        "journey_id": "REPLACE_WITH_STUDY_JOURNEY_ID",
        "grade_level": 4,
        "title": "REPLACE_WITH_LEARNER_FACING_STUDY_GUIDE_TITLE",
        "modules": MODULES,
        "source_coverage": {"required_source_refs": required, "covered_source_refs": covered},
    }
    if "REPLACE_" in plan["journey_id"] or "REPLACE_" in plan["title"]:
        raise ValueError("TEMPLATE_NOT_FILLED: StudyJourney identity/title")
    return plan


if __name__ == "__main__":
    print(json.dumps(build_study_journey(), indent=2))
