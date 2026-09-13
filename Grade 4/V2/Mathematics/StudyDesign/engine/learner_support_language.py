"""Learner-facing support-copy gate for Grade 4 Math V2.

Source ambiguity/defect evidence must remain in source custody, but raw forensic
metadata is not learner instruction. This module keeps that separation explicit
without hiding the source issue from teachers or the audit trail.
"""
from __future__ import annotations

import re
from typing import Any, Mapping


class LearnerSupportLanguageError(ValueError):
    pass


MAX_CUE_CHARS = 150
MAX_ACTION_CHARS = 110
MAX_EXTRA_HINT_CHARS = 180
FORBIDDEN_LEARNER_PHRASES = (
    "why this is flagged",
    "source issue",
    "source metadata",
    "literal nearest",
    "worksheet instruction is ambiguous",
)
INTERNAL_SOURCE_CODE_RE = re.compile(r"\b(?:DEFECTIVE_PRINTED_ITEM|SEMANTICALLY_INVALID_STORY|PHOTO_MAPPING_UNCERTAIN|SOURCE_NOT_PROVIDED|MAPPING_PENDING)\b")


def _require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise LearnerSupportLanguageError(f"{code}: {detail}")


def _norm(value: Any) -> str:
    return " ".join(str(value or "").lower().split())


def _learner_strings(question: Mapping[str, Any]) -> list[tuple[str, str]]:
    hint = question.get("hint_contract") or {}
    values: list[tuple[str, str]] = []
    if str(hint.get("hint_text") or "").strip():
        values.append(("hint_text", str(hint["hint_text"])))
    for stage in hint.get("stages") or []:
        level = str(stage.get("level") or "stage")
        values.append((f"{level}.verbal_cue", str(stage.get("verbal_cue") or "")))
        values.append((f"{level}.learner_action", str(stage.get("learner_action") or "")))
    return values


def assert_child_support_copy(question: Mapping[str, Any]) -> None:
    """Fail if support copy is forensic/internal, raw-copied, or too dense."""
    qid = str(question.get("question_id") or question.get("display_ref") or "question")
    hint = question.get("hint_contract") or {}
    extra = str(hint.get("hint_text") or "")
    _require(len(extra) <= MAX_EXTRA_HINT_CHARS, "LEARNER_HINT_COPY_TOO_LONG", f"{qid}/hint_text={len(extra)}")

    for stage in hint.get("stages") or []:
        level = str(stage.get("level") or "stage")
        cue = str(stage.get("verbal_cue") or "")
        action = str(stage.get("learner_action") or "")
        _require(len(cue) <= MAX_CUE_CHARS, "LEARNER_HINT_COPY_TOO_LONG", f"{qid}/{level}.cue={len(cue)}")
        _require(len(action) <= MAX_ACTION_CHARS, "LEARNER_HINT_COPY_TOO_LONG", f"{qid}/{level}.action={len(action)}")

    source_issue = str((question.get("source_identity") or {}).get("source_issue") or "").strip()
    source_issue_norm = _norm(source_issue)
    source_code = source_issue.split(":", 1)[0].strip() if source_issue else ""
    for field, text in _learner_strings(question):
        lowered = _norm(text)
        _require(not INTERNAL_SOURCE_CODE_RE.search(text), "SOURCE_FORENSIC_LANGUAGE_ON_LEARNER_SURFACE", f"{qid}/{field}")
        _require(not any(phrase in lowered for phrase in FORBIDDEN_LEARNER_PHRASES), "SOURCE_FORENSIC_LANGUAGE_ON_LEARNER_SURFACE", f"{qid}/{field}")
        if source_code:
            _require(source_code.lower() not in lowered, "SOURCE_ISSUE_RAW_COPY_ON_LEARNER_SURFACE", f"{qid}/{field}")
        if source_issue_norm and len(source_issue_norm) >= 20:
            _require(source_issue_norm not in lowered, "SOURCE_ISSUE_RAW_COPY_ON_LEARNER_SURFACE", f"{qid}/{field}")
