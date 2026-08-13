#!/usr/bin/env python3
"""Check concept/question navigation references before PDF publication.

Usage:
  python check_master_links.py master.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_master_links.py master.json", file=sys.stderr)
        return 2

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors: list[str] = []

    concepts = data.get("concepts", [])
    concept_ids = {c.get("concept_id") for c in concepts if c.get("concept_id")}

    qroot = data.get("questions", {})
    questions = qroot.get("anchors", []) + qroot.get("core_calibrated", []) + qroot.get("challenges", [])
    question_ids = {q.get("id") for q in questions if q.get("id")}

    for q in questions:
        qid = q.get("id", "<missing>")
        pc = q.get("primary_concept_id")
        if pc not in concept_ids:
            errors.append(f"{qid}: primary concept {pc!r} not found")
        for sc in q.get("secondary_concept_ids", []):
            if sc not in concept_ids:
                errors.append(f"{qid}: secondary concept {sc!r} not found")

    for c in concepts:
        cid = c.get("concept_id", "<missing>")
        fields = (
            "primary_anchor_ids",
            "same_level_question_ids",
            "challenge_question_ids",
        )
        for field in fields:
            for qid in c.get(field, []):
                if qid not in question_ids:
                    errors.append(f"{cid}: {field} references missing question {qid}")
        for dep in c.get("prerequisites", []):
            if dep not in concept_ids:
                errors.append(f"{cid}: missing prerequisite concept {dep}")

    if errors:
        print("GRADE 9 MASTER LINK CHECK: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GRADE 9 MASTER LINK CHECK: PASS")
    print(f"concepts={len(concept_ids)} questions={len(question_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
