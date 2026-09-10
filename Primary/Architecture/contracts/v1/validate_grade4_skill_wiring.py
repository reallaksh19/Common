#!/usr/bin/env python3
"""Validate that Grade 4 subject skills consume the canonical Primary runtime."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

REQUIRED_COMMON = [
    "../../Primary/Architecture/PRIMARY_INTEGRATED_ARCHITECTURE.md",
    "../../Primary/Architecture/SEMANTIC_OWNERSHIP.md",
    "../primary-teacher-runtime/SKILL.md",
    "../../Primary/Architecture/PRIMARY_TEACHER_RUNTIME.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"Grade 4 Primary skill wiring validation failed: {message}")


def require(path: Path, tokens: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            fail(f"{path.relative_to(ROOT)} is missing required token: {token}")
    return text


def main() -> None:
    english = ROOT / "skills" / "grade4-english" / "SKILL.md"
    math = ROOT / "skills" / "grade4-math" / "SKILL.md"

    english_text = require(english, REQUIRED_COMMON + [
        "SOURCE_BOUNDARY",
        "PRIMARY_RUNTIME_ALIGNMENT",
        "do **not** invent a new source category",
        "ACQUISITION",
        "DELAYED_RETENTION",
    ])
    math_text = require(math, REQUIRED_COMMON + [
        "CHILD_SELECTED",
        "CHILD_PRODUCED",
        "PRIMARY_RUNTIME_ALIGNMENT",
        "PERFORMANCE_LAPSE",
        "DELAYED_RETENTION",
    ])

    forbidden_english = "heavy -> quality"
    if forbidden_english.lower() in english_text.lower():
        fail("English skill reintroduced a force-fit adjective category")

    if "same-game correctness cannot establish delayed retention" not in math_text:
        fail("Math skill must explicitly separate same-session performance from delayed retention")

    print("Grade 4 Math/English skills are wired to the canonical Primary Teacher Runtime.")


if __name__ == "__main__":
    main()
