#!/usr/bin/env python3
"""Lightweight structural validator for the NCERT Chemistry authoring handoff.

This is deliberately narrower than PR #322's exact-product validators and is
not a substitute for subject/pedagogy/assessment/visual human review. It exists
to stop a future agent from silently losing the concrete invariants that were
discovered during the stress test.

Examples:

    python tools/validate_handoff.py --root restored-workspace
    python tools/validate_handoff.py restored-workspace

The root may be either the restored workspace (containing ``final/``) or the
``final/`` directory itself.
"""
from __future__ import annotations

import argparse
import csv
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


def retained_ledger_rows(path: Path) -> int:
    """Count retained/placed source rows across the slightly different ledgers."""
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return 0

    headers = {h.lower().strip(): h for h in rows[0].keys() if h}
    status_key = headers.get("status")
    if not status_key:
        # Some ledgers contain only retained rows.
        return len(rows)

    keep = {"retained", "placed", "included", "in_scope", "in scope"}
    return sum(1 for row in rows if str(row.get(status_key, "")).strip().lower() in keep)


def resolve_final_root(root: Path) -> Path:
    root = root.resolve()
    if root.name == "final":
        return root
    if (root / "final").is_dir():
        return root / "final"
    return root / "final"  # useful path in error output even when missing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root_positional", nargs="?", type=Path)
    ap.add_argument("--root", dest="root_option", type=Path)
    args = ap.parse_args()

    root = args.root_option or args.root_positional or Path(__file__).resolve().parents[1]
    final_root = resolve_final_root(root)

    failures: list[str] = []
    report: dict[str, object] = {
        "input_root": str(Path(root).resolve()),
        "final_root": str(final_root),
        "topics": {},
    }

    if not final_root.is_dir():
        raise SystemExit(
            f"No final/ source tree found at {final_root}. "
            "Run tools/restore_source_bundle.py first, then pass the restored workspace."
        )

    for topic, expected in TOPICS.items():
        d = final_root / topic
        core1 = d / "core1.html"
        core2 = d / "core2.html"
        ledger = d / "coverage-ledger.csv"
        needed = [core1, core2, ledger]

        missing = [str(p) for p in needed if not p.exists() or p.stat().st_size == 0]
        if missing:
            failures.extend(f"missing/empty: {p}" for p in missing)
            continue

        c1 = core1.read_text(encoding="utf-8")
        c2 = core2.read_text(encoding="utf-8")

        # Canonical Core (2) question pages use this heading form. Mixed revision
        # pages intentionally do not match this pattern.
        q_count = len(re.findall(r"Question\s+\d+\s+-", c2))
        answer_checks = len(re.findall(r"Answer check", c2, flags=re.I))
        worked_markers = len(re.findall(r"worked solution|full worked|worked answer", c2, flags=re.I))
        ledger_retained = retained_ledger_rows(ledger)

        if q_count != expected:
            failures.append(
                f"{topic}: expected {expected} canonical Core (2) question pages, found {q_count}"
            )
        if answer_checks < expected:
            failures.append(
                f"{topic}: expected at least {expected} immediate answer-check markers, found {answer_checks}"
            )
        if worked_markers < expected:
            failures.append(
                f"{topic}: expected at least {expected} worked-solution markers, found {worked_markers}"
            )
        if ledger_retained != expected:
            failures.append(
                f"{topic}: expected {expected} retained/placed ledger rows, found {ledger_retained}"
            )

        # Core (1) must retain the teaching/practice/solution/handout topology.
        c1_lower = c1.lower()
        for required_term in ("practice", "solution", "handout"):
            if required_term not in c1_lower:
                failures.append(f"{topic}: Core (1) missing visible {required_term!r} section marker")

        report["topics"][topic] = {
            "expected_questions": expected,
            "ledger_retained_rows": ledger_retained,
            "canonical_question_pages_found": q_count,
            "answer_check_mentions": answer_checks,
            "worked_solution_markers": worked_markers,
            "sha256": {
                "core1_html": sha256(core1),
                "core2_html": sha256(core2),
                "coverage_ledger": sha256(ledger),
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
