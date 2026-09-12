"""Instructional-completeness acceptance for English Worksheet 09.

This gate exists because source mapping alone is not a study guide. Coverage passes
only when each source obligation resolves to real teaching/model/practice/hint/
independent-verification/answer-or-rubric TeachingBlocks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
ENGLISH_ROOT = HERE.parents[1]
SOURCE_SET = ENGLISH_ROOT / "Benchmarks" / "source_sets" / "english_worksheet_09"
STUDY_ENGINE = ENGLISH_ROOT / "StudyDesign" / "engine"
SCHEMA = ENGLISH_ROOT / "StudyDesign" / "contracts" / "study-journey.schema.json"
for path in (SOURCE_SET, STUDY_ENGINE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build_fixture import build_handoff  # type: ignore  # noqa: E402
from study_journey_fixture import ALL_REFS, build_study_journey  # type: ignore  # noqa: E402
from study_journey import block_index, validate_study_journey  # type: ignore  # noqa: E402


def main() -> None:
    journey = build_study_journey()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(journey)
    result = validate_study_journey(journey)

    # QuestionEvidence and StudyJourney must agree on the source obligations.
    handoff = build_handoff()
    source_refs = {str(p["source_ref"]) for p in handoff["learning_representation_plans"]}
    assert source_refs == set(ALL_REFS), (source_refs, set(ALL_REFS))
    assert set(journey["required_source_refs"]) == source_refs

    # Coverage is evidence-backed; booleans are not an accepted substitute.
    forbidden_boolean_fields = {"teach", "model", "practice", "hints", "verify", "answer_or_rubric"}
    for row in journey["source_coverage"]:
        assert not forbidden_boolean_fields.intersection(row), row
        for field in (
            "teach_block_refs", "model_block_refs", "practice_block_refs",
            "hint_block_refs", "verify_block_refs", "answer_or_rubric_block_refs",
        ):
            assert row[field], f"{row['source_ref']} has no {field}"

    blocks = block_index(journey)

    # The first real benchmark must carry the pedagogical obligations that made
    # the reference self-teaching edition useful, rather than collapsing to one
    # worksheet page per source question.
    required_blocks = {
        "ADJ-CONCEPT", "ADJ-SOURCE-RULE", "ADJ-MODEL", "ADJ-CONTRAST", "ADJ-HINTS", "ADJ-VERIFY",
        "ORDER-RULE", "ORDER-MODEL-TEMPLE", "ORDER-MODEL-DOOR", "ORDER-BOUNDARY", "ORDER-VERIFY",
        "MYSTERY-CONCEPT", "MYSTERY-MODEL", "MYSTERY-PLANNER", "MYSTERY-VERIFY",
        "TRAVEL-CONCEPT", "TRAVEL-SOURCE-RULE", "TRAVEL-MODEL", "TRAVEL-CONTRAST", "TRAVEL-VERIFY",
        "POEM-ROUTINE", "POEM-VOCAB", "POEM-MODEL", "POEM-SOURCE", "POEM-VERIFY",
        "Q1-CONCEPT", "Q1-MODEL", "Q1-CONTRAST", "Q1-HINTS", "Q1-VERIFY",
        "Q2-CONCEPT", "Q2-MODEL", "Q2-DIAG", "Q2-VERIFY",
        "Q34-CONCEPT", "Q3-MODEL", "Q4-MODEL", "Q3-VERIFY", "Q4-VERIFY",
    }
    assert required_blocks.issubset(blocks), sorted(required_blocks - set(blocks))

    boundary = blocks["ORDER-BOUNDARY"]
    assert boundary["block_type"] == "SOURCE_BOUNDARY"
    assert boundary["provenance"] == "SOURCE_DERIVED"
    assert "traditional" in boundary["body"]
    assert "invent" in boundary["body"].lower()

    # Open English responses are judged by evidence/rubric, never exact-string truth.
    for ref in ("Q1-RUBRIC", "Q2-RUBRIC", "Q3-RUBRIC", "Q4-RUBRIC", "TRAVEL-RUBRIC", "MYSTERY-RUBRIC"):
        block = blocks[ref]
        assert block["block_type"] == "RUBRIC"
        assert block["answer_visibility"] == "ANSWER_KEY_ONLY"
    assert "exact-string" in blocks["Q1-RUBRIC"]["body"]

    # Supported work is not independent evidence.
    for obj in journey["learning_objects"]:
        for ref in obj["independent_evidence_refs"]:
            block = blocks[ref]
            assert block["block_type"] in {"INDEPENDENT_RETRY", "TRANSFER", "RETRIEVAL"}
            assert block["support_level"] == "H0"
            assert block["answer_visibility"] == "HIDDEN"

    # Depth is asserted semantically by learning objects/blocks, not by PDF page count.
    assert result["learning_object_count"] >= 8
    assert result["teaching_block_count"] >= 55
    assert result["source_coverage_count"] == 8
    print(json.dumps(result, indent=2))
    print("English Worksheet 09 StudyJourney instructional-completeness acceptance PASS")


if __name__ == "__main__":
    main()
