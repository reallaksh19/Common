#!/usr/bin/env python3
"""Validate core Grade 9 master-data invariants using only the Python stdlib.

Usage:
  python validate_bank.py master.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_bank.py master.json", file=sys.stderr)
        return 2

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors: list[str] = []

    project = data.get("project", {})
    if project.get("grade") != 9:
        fail(errors, "project.grade must be 9")

    concepts = data.get("concepts", [])
    concept_ids = [c.get("concept_id") for c in concepts]
    if len(concept_ids) != len(set(concept_ids)):
        fail(errors, "duplicate concept_id values found")
    valid_concepts = {x for x in concept_ids if x}

    qroot = data.get("questions", {})
    anchors = qroot.get("anchors", [])
    calibrated = qroot.get("core_calibrated", [])
    challenges = qroot.get("challenges", [])
    all_questions = anchors + calibrated + challenges

    ids = [q.get("id") for q in all_questions]
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate question IDs found")

    for q in all_questions:
        qid = q.get("id", "<missing>")
        pc = q.get("primary_concept_id")
        if not pc:
            fail(errors, f"{qid}: missing primary_concept_id")
        elif pc not in valid_concepts:
            fail(errors, f"{qid}: unknown primary_concept_id {pc}")
        if not q.get("provenance_class"):
            fail(errors, f"{qid}: missing provenance_class")
        if not q.get("question"):
            fail(errors, f"{qid}: missing question text")
        if q.get("transcription_status") == "SOURCE_UNRESOLVED" and q in anchors:
            fail(errors, f"{qid}: unresolved source anchor must not remain a scored anchor")

    requested_core = project.get("core_question_count")
    if requested_core is not None:
        actual_core = len(anchors) + len(calibrated)
        if actual_core != requested_core:
            fail(errors, f"Core count mismatch: requested {requested_core}, found {actual_core}")

    requested_challenges = project.get("challenge_question_count")
    if requested_challenges is not None and len(challenges) != requested_challenges:
        fail(errors, f"Challenge count mismatch: requested {requested_challenges}, found {len(challenges)}")

    for c in concepts:
        cid = c.get("concept_id", "<missing>")
        for dep in c.get("prerequisites", []):
            if dep not in valid_concepts:
                fail(errors, f"{cid}: unknown prerequisite {dep}")

    qa = data.get("qa", {})
    for field in ("source_qc_complete", "answers_verified", "concept_links_verified"):
        if field not in qa:
            fail(errors, f"qa.{field} missing")

    if errors:
        print("GRADE 9 BANK VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GRADE 9 BANK VALIDATION: PASS")
    print(f"concepts={len(concepts)} core={len(anchors)+len(calibrated)} challenges={len(challenges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
