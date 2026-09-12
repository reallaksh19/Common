#!/usr/bin/env python3
"""Fail-fast checks for the Core1A Motion in a Plane source inventory."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "registry" / "physics-core1a-motion-in-a-plane-source-inventory.json"
LINK = ROOT / "registry" / "physics-core1a-core2-linkage.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_unique(rows, key, label):
    vals = [r.get(key) for r in rows]
    assert all(vals), f"{label}: blank {key}"
    assert len(vals) == len(set(vals)), f"{label}: duplicate {key}"


def main():
    inv = load(INV)
    link = load(LINK)

    groups = inv["source_groups"]
    equations = inv["equations"]
    illustrations = inv["worked_illustrations"]
    extensions = inv.get("source_visible_extensions", [])

    assert inv["expected_source_question_count"] == 59
    assert len(groups) >= 20, "source hierarchy is suspiciously incomplete"
    assert len(equations) >= 30, "equation inventory is suspiciously incomplete"
    assert len(illustrations) >= 16, "worked-illustration inventory is suspiciously incomplete"

    for rows, label in [
        (groups, "source_groups"),
        (equations, "equations"),
        (illustrations, "worked_illustrations"),
        (extensions, "source_visible_extensions"),
    ]:
        check_unique(rows, "id", label)
        for row in rows:
            assert row.get("source_locator"), f"{row['id']}: source locator missing"
            assert row.get("core1a_home"), f"{row['id']}: Core1A learner home missing"
            assert row.get("status") in {"PLANNED", "BUILT", "VERIFIED"}, f"{row['id']}: invalid status"

    # Every taught equation must say when it is valid. This prevents formula-only coverage.
    for eq in equations:
        assert eq.get("canonical_expression"), f"{eq['id']}: equation missing"
        assert eq.get("learner_name"), f"{eq['id']}: learner name missing"
        assert eq.get("valid_when"), f"{eq['id']}: validity condition missing"
        assert eq.get("must_be_taught") is True, f"{eq['id']}: source equation must have a teaching home"

    # Source-visible advanced material must never masquerade as ordinary core theory.
    for ext in extensions:
        assert ext.get("coverage_mode") == "STRETCH", f"{ext['id']}: source-visible extension must be STRETCH"
        assert ext.get("note"), f"{ext['id']}: source limitation note missing"

    # Core2 is the assessment side. Its registry must still account for every retained challenge.
    expected = inv["expected_source_question_count"]
    challenge_ids = set()
    for concept in link.get("concepts", []):
        for qid in concept.get("core2_challenges", []):
            challenge_ids.add(qid)
    assert len(challenge_ids) == expected, (
        f"Core2 linkage covers {len(challenge_ids)} challenges; expected {expected}"
    )

    print(
        "PASS source completeness inventory: "
        f"{len(groups)} source groups, {len(equations)} equations, "
        f"{len(illustrations)} worked illustrations, {expected} Core2 challenges"
    )


if __name__ == "__main__":
    main()
