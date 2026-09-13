#!/usr/bin/env python3
"""Bind published source-question identity to the authoritative source.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Grade4.V2.Mathematics.Benchmarks.source_sets.pupil_pages_97_99.study_journey_fixture import build_study_journey

SOURCE_PATH = REPO_ROOT / "Grade 4" / "V2" / "Mathematics" / "Benchmarks" / "source_sets" / "pupil_pages_97_99" / "source.json"


def _issue_kind(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text.split(":", 1)[0]


def _numeric_values(values: object) -> list[str]:
    return [str(value).replace(",", "").strip() for value in (values or [])]


def main() -> None:
    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    rows = {str(r["question_ref"]): r for r in source["questions"]}
    plan = build_study_journey()

    seen: dict[str, dict] = {}
    for module in plan["modules"]:
        for block in module["blocks"]:
            for q in block.get("questions") or []:
                if q.get("origin") != "SOURCE":
                    continue
                identity = q.get("source_identity") or {}
                ref = str(identity.get("source_ref") or "")
                if ref not in rows:
                    raise SystemExit(f"SOURCE_IDENTITY_WITHOUT_TRANSCRIPTION: {ref}")
                row = rows[ref]
                if identity.get("source_display_ref") != row.get("source_display_ref"):
                    raise SystemExit(f"SOURCE_DISPLAY_REF_DRIFT: {ref}")
                if identity.get("source_text") != row.get("raw_text"):
                    raise SystemExit(f"SOURCE_QUESTION_TEXT_DRIFT: {ref}")
                if _numeric_values(identity.get("source_numeric_tokens")) != _numeric_values(row.get("source_numeric_tokens")):
                    raise SystemExit(f"SOURCE_NUMERIC_TOKEN_DRIFT: {ref}")
                if _issue_kind(identity.get("source_issue")) != _issue_kind(row.get("source_issue")):
                    raise SystemExit(f"SOURCE_ISSUE_CATEGORY_DRIFT: {ref}")
                seen[ref] = identity

    missing = sorted(set(rows) - set(seen))
    if missing:
        raise SystemExit(f"SOURCE_QUESTION_COVERAGE_GAP: {missing}")

    print({"status": "PASS", "source_questions": len(seen), "source_set_id": source["source_set_id"]})


if __name__ == "__main__":
    main()
