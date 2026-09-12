"""Validate the scanned-source cold-start template fails closed until authored."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "Benchmarks" / "source_sets" / "_template"
START = ROOT / "START_HERE.md"


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _must_fail(fn, expected: str) -> None:
    try:
        fn()
    except ValueError as exc:
        message = str(exc)
        if expected not in message:
            raise AssertionError(f"expected {expected!r}, got {message!r}") from exc
        return
    raise AssertionError(f"template unexpectedly passed; expected {expected}")


def main() -> None:
    required_files = {
        "README.md",
        "source.json",
        "build_fixture.py",
        "production_fixture.py",
        "study_journey_fixture.py",
    }
    present = {p.name for p in TEMPLATE.iterdir() if p.is_file()}
    missing = sorted(required_files - present)
    assert not missing, f"SCAN_SOURCE_TEMPLATE_FILES_MISSING: {missing}"

    source = json.loads((TEMPLATE / "source.json").read_text(encoding="utf-8"))
    assert source.get("template_only") is True, "SCAN_SOURCE_TEMPLATE_MUST_START_LOCKED"
    assert source.get("scope_basis") == "QUESTION_SET_OBSERVED"
    assert any(row.get("source_issue") == "TEMPLATE_NOT_FILLED" for row in source.get("questions", []))

    build = _load(TEMPLATE / "build_fixture.py", "grade4_scan_template_build")
    _must_fail(build.build_primary_input, "TEMPLATE_NOT_FILLED")

    journey = _load(TEMPLATE / "study_journey_fixture.py", "grade4_scan_template_journey")
    _must_fail(journey.build_study_journey, "TEMPLATE_NOT_FILLED")

    start_text = START.read_text(encoding="utf-8")
    for required in (
        "faithful visual source extraction",
        "QuestionEvidence",
        "LearningRepresentationPlan",
        "StudyJourneyPlan",
        "Publication",
        "Acceptance",
        "PEDAGOGICAL_BRIDGE",
    ):
        assert required in start_text, f"START_HERE_COLD_START_STAGE_MISSING: {required}"

    assert "do not start in publication" in start_text.lower(), "START_HERE_PUBLISHER_BOUNDARY_MISSING"
    print("Grade 4 scan-source cold-start template: PASS")


if __name__ == "__main__":
    main()
