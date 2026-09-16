#!/usr/bin/env python3
"""Contract checks for Core (1A) <-> revised Core (2) v2 learner linkages."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINKS = ROOT / "registry" / "physics-core1a-core2-linkage.json"
LANG = ROOT / "registry" / "physics-core1a-learner-language.json"


def main():
    links = json.loads(LINKS.read_text())
    lang = json.loads(LANG.read_text())

    assert links["core2_question_count"] == 59
    rows = links["challenge_links"]
    assert len(rows) == 59

    nums = [r["challenge_number"] for r in rows]
    assert nums == list(range(1, 60)), f"Expected Q01-Q59 exactly once; got {nums}"

    ids = [r["challenge_id"] for r in rows]
    assert len(ids) == len(set(ids)) == 59

    concepts = links["concepts"]
    for row in rows:
        cid = row["core1a_concept_id"]
        assert cid in concepts, f"Missing concept {cid}"
        assert row["challenge_id"] in concepts[cid]["challenge_ids"]
        assert row["learner_link_label"] == concepts[cid]["learner_title"]
        assert row["core2_prompt_page"] == row["challenge_number"] + 2
        assert row["core2_solution_page"] == row["challenge_number"] + 63

    for cid, concept in concepts.items():
        expected = [r["challenge_id"] for r in rows if r["core1a_concept_id"] == cid]
        assert concept["challenge_ids"] == expected, (cid, concept["challenge_ids"], expected)

    banned = [w.lower() for w in lang["banned_learner_words"]]
    learner_strings = []
    learner_strings.extend(v for v in links["learner_navigation"].values() if isinstance(v, str))
    for concept in concepts.values():
        learner_strings.append(concept["learner_title"])
    learner_strings.extend(lang["module_labels"].values())
    learner_strings.extend(lang["core2_navigation"].values())
    blob = "\n".join(str(s).lower() for s in learner_strings)
    for word in banned:
        assert word not in blob, f"Banned learner-facing word present: {word}"

    required_labels = {
        "Ready to practise?",
        "Need a quick refresher?",
        "Go back to this idea",
        "Try Core (2)",
    }
    present = set(str(v) for v in links["learner_navigation"].values()) | set(lang["core2_navigation"].values())
    assert required_labels <= present

    print("PASS: Core1A<->Core2 linkage registry covers Q01-Q59 exactly once.")
    print("PASS: learner-facing wording avoids internal production jargon.")


if __name__ == "__main__":
    main()
