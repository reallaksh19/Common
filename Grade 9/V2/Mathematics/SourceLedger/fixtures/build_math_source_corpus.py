#!/usr/bin/env python3
"""Build the frozen source-corpus fixture and the matching authored-plan fixture.

The corpus deliberately contains the exact shapes that lost content during the stress test:

* a four-option MCQ (Linear Equations) — the option set that got covered by the next panel;
* a compound "prove ... and hence deduce ..." item (Euclid) — two proof obligations where
  the top-level count only ever showed one question;
* a multipart item with a parameter condition (Polynomials) — the subpart whose loss leaves
  the top-level count unchanged;
* a modelling item with a unit requirement (Surface Areas & Volumes).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PHASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHASE / "engine"))

from build_math_source_ledger import freeze_manifest, shape_of  # noqa: E402

CORPUS_OUT = PHASE / "fixtures" / "math-source-corpus.fixture.json"
AUTHORED_OUT = PHASE / "fixtures" / "math-authored-plan.fixture.json"


def ask(ref, kind, label, text, visible=True) -> dict:
    return {"atomic_ask_ref": ref, "kind": kind, "label": label, "text": text,
            "learner_visible": visible}


def question(ref, order, stem, mode, asks) -> dict:
    return {
        "question_ref": ref,
        "source_order": order,
        "stem": stem,
        "response_mode": mode,
        "subpart_shape": shape_of(asks),
        "atomic_asks": asks,
    }


QUESTIONS = [
    question(
        "Q1", 1,
        "Which of the following points does NOT lie on the line 2x + 4y = 8?",
        "MCQ_SELECTION",
        [
            ask("Q1#OPT-A", "OPTION", "(A)", "(0, 2)"),
            ask("Q1#OPT-B", "OPTION", "(B)", "(2, 1)"),
            ask("Q1#OPT-C", "OPTION", "(C)", "(4, 0)"),
            ask("Q1#OPT-D", "OPTION", "(D)", "(1, 2)"),
            ask("Q1#JUST", "JUSTIFICATION", "Reason:",
                "Give a reason for the option you chose."),
        ],
    ),
    question(
        "Q2", 2,
        "Two distinct lines cannot have more than one point in common.",
        "PROOF",
        [
            ask("Q2#PROOF-1", "PROOF_OBLIGATION", "(i)",
                "Prove the statement using Euclid's axioms."),
            ask("Q2#PROOF-2", "PROOF_OBLIGATION", "(ii)",
                "Hence deduce that two distinct lines cannot both pass through two "
                "distinct given points."),
        ],
    ),
    question(
        "Q3", 3,
        "For the polynomial p(x) = x cubed + a x squared minus 5x + 6:",
        "MULTIPART",
        [
            ask("Q3#SUB-a", "SUBPART", "(a)",
                "Find the value of a for which (x minus 1) is a factor of p(x)."),
            ask("Q3#SUB-b", "SUBPART", "(b)",
                "Using that value of a, factorise p(x) completely."),
            ask("Q3#COND", "PARAMETER_CONDITION", "Condition:",
                "State the values of a for which p(x) has no linear factor with integer "
                "root."),
        ],
    ),
    question(
        "Q4", 4,
        "A solid metal cylinder is melted and recast as a sphere of the same volume.",
        "MODEL_UNIT_CALCULATION",
        [
            ask("Q4#SUB-a", "SUBPART", "(a)", "Find the radius of the sphere."),
            ask("Q4#UNITS", "UNIT_REQUIREMENT", "Units:",
                "Give the radius in centimetres correct to one decimal place."),
        ],
    ),
]


def build_corpus() -> dict:
    manifest = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "topic_ref": "MIXED_GRADE9_SOURCE_PROBE",
        "corpus_authority": {
            "name": "Stress-test source-shape probe",
            "reference": "Derived from the shapes named in PR #323 comments 5644501927, "
                         "5645333463 and 5645525718",
            "vendored": False,
            "note": "Deliberately not a vendored NCERT extract. The purpose of this fixture "
                    "is to exercise the completeness dimensions, not to restate source "
                    "content. The official units remain the authority named in the #345 "
                    "handoff.",
        },
        "frozen_at_stage": "BEFORE_AUTHORING",
        "required_question_refs": [],
        "required_atomic_ask_refs": [],
        "questions": QUESTIONS,
    }
    return freeze_manifest(manifest)


def build_authored(manifest: dict) -> dict:
    """A complete authored plan: every row, every atomic ask, matching shapes."""
    pages = []
    for q in manifest["questions"]:
        pages.append({
            "question_ref": q["question_ref"],
            "atomic_ask_refs": [a["atomic_ask_ref"] for a in q["atomic_asks"]],
            "subpart_shape": dict(q["subpart_shape"]),
            "concept_linked": True,
            "core1_evidence_linked": True,
            "solution_complete": True,
            "verification_complete": True,
        })
    return {"topic_ref": manifest["topic_ref"], "pages": pages}


def main() -> None:
    manifest = build_corpus()
    authored = build_authored(manifest)
    CORPUS_OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    AUTHORED_OUT.write_text(json.dumps(authored, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(f"wrote {CORPUS_OUT.name}: {len(manifest['required_question_refs'])} rows, "
          f"{len(manifest['required_atomic_ask_refs'])} atomic asks")
    print(f"wrote {AUTHORED_OUT.name}: {len(authored['pages'])} pages")


if __name__ == "__main__":
    main()
