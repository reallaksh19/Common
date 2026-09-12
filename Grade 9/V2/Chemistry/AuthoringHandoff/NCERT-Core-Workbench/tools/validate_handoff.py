#!/usr/bin/env python3
"""Lightweight integrity checks for the NCERT Core Workbench.

This is a handoff validator, not a substitute for PR #322's exact-product
validators or human review. It checks the concrete invariants discovered in the
stress test: files exist, the fixed retained-question counts are still visible
in Core (2), and each Core (2) has enough immediate answer-check blocks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

TOPICS = {
    "some-basic-concepts": 68,
    "behaviour-of-gases": 27,
    "chemical-bonding": 38,
    "redox-reactions": 11,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    root = args.root.resolve()
    failures: list[str] = []
    report: dict[str, object] = {"root": str(root), "topics": {}}

    for topic, expected in TOPICS.items():
        d = root / "final" / topic
        needed = [d / "core1.html", d / "core2.html", d / "coverage-ledger.csv"]
        for p in needed:
            if not p.exists() or p.stat().st_size == 0:
                failures.append(f"missing/empty: {p}")
        if any(str(d) in x for x in failures):
            continue

        text = (d / "core2.html").read_text(encoding="utf-8")
        q_count = len(re.findall(r"Question\s+\d+\s+-", text))
        answer_checks = len(re.findall(r"Answer check", text, flags=re.I))
        if q_count != expected:
            failures.append(f"{topic}: expected {expected} canonical question pages, found {q_count}")
        if answer_checks < expected:
            failures.append(f"{topic}: expected at least {expected} immediate answer checks, found {answer_checks}")
        if "worked" not in text.lower() or "solution" not in text.lower():
            failures.append(f"{topic}: Core (2) does not visibly declare a worked-solution path")

        report["topics"][topic] = {
            "expected_questions": expected,
            "question_pages_found": q_count,
            "answer_check_mentions": answer_checks,
            "sha256": {
                "core1_html": sha256(d / "core1.html"),
                "core2_html": sha256(d / "core2.html"),
                "coverage_ledger": sha256(d / "coverage-ledger.csv"),
            },
        }

    print(json.dumps(report, indent=2))
    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("\nPASS: handoff structural checks closed")


if __name__ == "__main__":
    main()
