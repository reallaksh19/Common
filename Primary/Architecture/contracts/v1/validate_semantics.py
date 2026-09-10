#!/usr/bin/env python3
"""Fail-closed checks for the Primary Grades 4-5 semantic contract example.

This validator intentionally uses only the Python standard library. It does not
attempt to replace a full JSON-Schema implementation; it checks the invariants
that are most important to the Primary architecture cold-start contract.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "primary-learning-semantics.schema.json"
EXAMPLE = ROOT / "examples" / "fractions-learning-episode.example.json"

EVIDENCE_STATES = {
    "NOT_OBSERVED",
    "NOT_YET_TESTED",
    "EMERGING",
    "DEVELOPING",
    "SECURE",
    "REASSESS_LATER",
    "NOT_APPLICABLE",
}
EVIDENCE_DIMENSIONS = {
    "acquisition",
    "independentUse",
    "delayedRetention",
    "transfer",
    "stretch",
}


def fail(message: str) -> None:
    raise SystemExit(f"Primary semantic validation failed: {message}")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - fail closed for malformed source
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    schema = load(SCHEMA)
    example = load(EXAMPLE)

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("schema must declare JSON Schema draft 2020-12")
    if example.get("schemaVersion") != "1.0":
        fail("example schemaVersion must be 1.0")

    target = example.get("teachingTarget") or {}
    state = example.get("skillState") or {}
    session = example.get("currentLearningState") or {}
    episode = example.get("learningEpisode") or {}

    target_objects = target.get("learningObjectIds") or []
    if not target_objects:
        fail("TeachingTarget requires at least one learningObjectId")
    if state.get("learningObjectId") not in target_objects:
        fail("SkillState learningObjectId must be one of the TeachingTarget learningObjectIds")
    if set(episode.get("learningObjectIds") or []) != set(target_objects):
        fail("LearningEpisode learningObjectIds must preserve TeachingTarget identity in the reference fixture")
    if not set(session.get("learningObjectIds") or []).issubset(set(target_objects)):
        fail("CurrentLearningState may not introduce unrelated learning objects")

    evidence = state.get("learningEvidence") or {}
    if set(evidence) != EVIDENCE_DIMENSIONS:
        fail("SkillState must keep acquisition, independentUse, delayedRetention, transfer and stretch as separate dimensions")
    invalid_states = {value for value in evidence.values() if value not in EVIDENCE_STATES}
    if invalid_states:
        fail(f"invalid evidence states: {sorted(invalid_states)}")

    if episode.get("independentCheckRequired") is not True:
        fail("LearningEpisode must require an independent check")
    steps = episode.get("steps") or []
    step_ids = [step.get("stepId") for step in steps]
    if len(step_ids) != len(set(step_ids)):
        fail("LearningEpisode stepId values must be unique")
    if not any(step.get("role") == "INDEPENDENT_CHECK" for step in steps):
        fail("LearningEpisode must contain an INDEPENDENT_CHECK step")

    delayed = episode.get("delayedRetrieval") or {}
    if delayed.get("required"):
        if not any(step.get("role") == "RETRIEVAL" for step in steps):
            fail("required delayed retrieval must have a RETRIEVAL step")
        earliest = delayed.get("earliestDays")
        latest = delayed.get("latestDays")
        if earliest is not None and latest is not None and latest < earliest:
            fail("delayed retrieval latestDays must be >= earliestDays")

    conceptual = session.get("conceptualSupport") or {}
    if not conceptual.get("level") or not conceptual.get("type"):
        fail("CurrentLearningState must represent conceptual support explicitly")
    if "accessAdjustments" not in session:
        fail("CurrentLearningState must represent access adjustments separately from conceptual support")

    for event in example.get("runtimeTrace") or []:
        if event.get("type") == "DIAGNOSIS":
            diagnosis = event.get("diagnosis") or {}
            if not diagnosis.get("evidenceRefs"):
                fail("diagnosis must cite observation evidence")
            if diagnosis.get("confidence") not in {"LOW", "MEDIUM", "HIGH"}:
                fail("diagnosis must carry bounded confidence")
        if event.get("type") == "MOVE":
            move = event.get("move") or {}
            if not move.get("expectedChildAction"):
                fail("TeacherMove must leave an observable child action")

    forbidden_single_mastery = {"mastery", "masteryScore", "masteryState"}
    if forbidden_single_mastery.intersection(example.keys()):
        fail("top-level single mastery field is forbidden")

    print("Primary learning semantics v1 fixture passed canonical invariants.")


if __name__ == "__main__":
    main()
