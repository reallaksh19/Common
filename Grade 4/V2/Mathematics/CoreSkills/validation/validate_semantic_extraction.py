#!/usr/bin/env python3
"""Validate semantic extraction normalization and anti-drift gates."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Primary.V2.Mathematics.CoreSkills.engine.author import AuthoringError, author
from Primary.V2.Mathematics.CoreSkills.engine.semantic_extraction import normalize_extraction

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "authoring" / "semantic_extraction_cases.json"


def fail(message: str) -> None:
    raise SystemExit(f"Primary Math V2 semantic extraction validation failed: {message}")


def expect_error(primary_input, extraction, code: str) -> None:
    try:
        normalize_extraction(primary_input, extraction)
    except AuthoringError as exc:
        if exc.code != code:
            fail(f"expected {code}, got {exc.code}: {exc.message}")
        return
    fail(f"expected {code}, but normalization succeeded")


def main() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))["valid"]
    primary_input = payload["primary_input"]
    extraction = payload["extraction"]

    normalized = normalize_extraction(primary_input, extraction)
    question = normalized["question_set"]["questions"][0]
    evidence = question.get("evidence") or {}
    if evidence.get("question_ref") != "Q-MUL-23X6":
        fail("normalized QuestionEvidence lost question_ref")
    if "extraction://EXT-MUL-23X6-001#Q-MUL-23X6" not in evidence.get("source_refs", []):
        fail("extraction provenance ref missing")
    if normalized["question_set"].get("extraction_provenance", {}).get("policy") != "CLAIMS_VERIFIED_NOT_INFERRED_BY_NORMALIZER":
        fail("normalizer provenance policy missing")

    authored = author(normalized)
    caps = set(authored["skill_model"]["concepts"][0]["capability_refs"])
    if "MULT_WRITTEN_ALGORITHM" not in caps:
        fail("normalized evidence did not flow into authoring engine")
    if authored["skill_model"].get("work_evidence_refs"):
        fail("semantic extraction fabricated learner work")

    mismatch = copy.deepcopy(extraction)
    mismatch["questions"][0]["source_text"] = "Calculate 32 × 6."
    expect_error(primary_input, mismatch, "SEMANTIC_EXTRACTION_SOURCE_TEXT_MISMATCH")

    unknown = copy.deepcopy(extraction)
    unknown["questions"][0]["claims"]["capability_refs"].append("CAPABILITY_NOT_IN_REGISTRY")
    expect_error(primary_input, unknown, "UNKNOWN_CAPABILITY_REF")

    low_conf = copy.deepcopy(extraction)
    low_conf["questions"][0]["claims"]["confidence"] = 0.40
    low_conf["questions"][0]["claims"]["ambiguity"] = []
    expect_error(primary_input, low_conf, "LOW_CONFIDENCE_EXTRACTION_SILENTLY_FORCED")

    no_conf = copy.deepcopy(extraction)
    no_conf["questions"][0]["claims"].pop("confidence", None)
    expect_error(primary_input, no_conf, "MODEL_ASSISTED_EXTRACTION_CONFIDENCE_MISSING")

    coverage = copy.deepcopy(extraction)
    coverage["questions"] = []
    expect_error(primary_input, coverage, "SEMANTIC_EXTRACTION_QUESTION_COVERAGE_MISMATCH")

    curriculum = copy.deepcopy(extraction)
    curriculum["questions"][0]["claims"]["scope_basis"] = "CURRICULUM_CONFIRMED"
    curriculum["questions"][0]["claims"]["authority_ref"] = None
    expect_error(primary_input, curriculum, "CURRICULUM_CONFIRMED_WITHOUT_AUTHORITY_REF")

    print("Primary Math V2 semantic extraction: normalization and falsifiers PASS")


if __name__ == "__main__":
    main()
