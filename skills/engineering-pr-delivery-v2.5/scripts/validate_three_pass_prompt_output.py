#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")

LEGACY_ACTIVE_PATTERNS = (
    "TARGET SCOPE:",
    "TASK_ARTIFACT",
    "TARGET NATIVE DELIVERABLE",
    "FINAL OUTPUT CONTRACT",
    "PROMPT-3 OUTPUT GATE",
    "The register is the thing you are imagining",
    "imagine an excellent live register",
    "Produce the reconciled register",
    "Your deliverable is a better current register",
)

PROMPT1_METHOD_META_PATTERNS = (
    "this answer will be used",
    "fixed independent reference",
    "independent reference in a later pass",
    "later pass",
    "next pass",
    "third pass",
    "do not inspect the current repository",
    "do not inspect the repository",
    "do not open any repository",
    "do not open the repository",
    "do not open the issue tracker",
    "you will be held to this picture",
    "before seeing the current answer",
    "before seeing the current implementation",
    "before looking at how this repository",
    "before looking at how the current repository",
    "before looking at the repository",
    "prompt 2 will",
    "prompt 3 will",
)

REQUIRED_BASIS_FIELDS = (
    "SCHEMA SOURCE:",
    "SCHEMA REF:",
    "SCHEMA CONTENT SHA:",
    "SCHEMA FETCH STATUS:",
    "SCHEMA COMPATIBILITY:",
    "LEGACY-SIGNATURE GATE:",
)

REQUIRED_PREFLIGHT_FIELDS = (
    "LOT:",
    "USER-REQUESTED LEVEL:",
    "USER-REQUESTED TARGET:",
    "LEVEL INTERPRETATION:",
    "TARGET TITLE / SURFACE:",
    "REQUEST MODE:",
    "COMPLEX MODE:",
    "CURRENT ARTIFACT FORM:",
    "CURRENT STATED ANSWER / IMPLEMENTATION:",
    "CURRENT-STATE FACTS:",
    "CURRENT ANSWER QUARANTINE:",
    "TARGET ANCHORS:",
    "PROBLEM KERNEL:",
    "UNDERLYING HUMAN PROBLEM:",
    "HUMAN OUTCOME:",
    "GENUINE CONSTRAINTS:",
    "EXPERTISE:",
    "IMAGINATION OBJECT:",
    "REALITY OBJECT:",
    "COMPARISON QUESTION:",
    "HANDOVER DESTINATION:",
    "LOT/LEVEL BOUNDARY GATE:",
    "SPECIFICITY-FLOOR GATE:",
    "KERNEL-COVERAGE GATE:",
    "SAME-ISSUE IDENTITY GATE:",
    "ANSWER-EXCLUSION GATE:",
    "ARTIFACT-ERASURE GATE:",
    "CURRENT-VOCABULARY GATE:",
    "PROMPT-1 OBJECT GATE:",
    "HUMAN-IMMERSION GATE:",
    "PROMPT-3 FREEDOM GATE:",
    "COMPLEX Q1–Q5 COVERAGE:",
)

PROMPT_HEADINGS = (
    "## PROMPT 1 — IMAGINE",
    "## PROMPT 2 — UNDERSTAND",
    "## PROMPT 3 — REVALIDATE AND MOVE FORWARD",
)


def _field_value(block: str, field: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(field)}\s*(.*)$")
    match = pattern.search(block)
    if not match:
        return ""
    inline = match.group(1).strip()
    if inline:
        return inline

    tail = block[match.end():]
    for raw in tail.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("PASS —") or line.startswith("N/A"):
            return line
        if re.match(r"^[A-Z][A-Z0-9 /()–—-]+:$", line):
            return ""
        return line
    return ""


def _basis_block(text: str) -> str:
    start = text.find("# SCHEMA BASIS")
    lot = text.find("# LOT ")
    if start < 0:
        return ""
    return text[start:lot if lot > start else len(text)]


def _lot_blocks(text: str) -> list[str]:
    starts = [m.start() for m in re.finditer(r"(?m)^# LOT\s+", text)]
    blocks = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(text)
        blocks.append(text[start:end])
    return blocks


def validate_text(text: str, expected_schema_sha: str | None = None) -> list[str]:
    errors: list[str] = []

    if not text.lstrip().startswith("# SCHEMA BASIS"):
        errors.append("output must begin with '# SCHEMA BASIS'")

    basis = _basis_block(text)
    if not basis:
        errors.append("missing SCHEMA BASIS block")
    else:
        for field in REQUIRED_BASIS_FIELDS:
            if field not in basis:
                errors.append(f"SCHEMA BASIS missing {field}")

        status = _field_value(basis, "SCHEMA FETCH STATUS:")
        sha = _field_value(basis, "SCHEMA CONTENT SHA:")
        compatibility = _field_value(basis, "SCHEMA COMPATIBILITY:")

        if status not in {"LIVE_THIS_RUN", "USER_SUPPLIED_TEXT"}:
            errors.append("SCHEMA FETCH STATUS must be LIVE_THIS_RUN or USER_SUPPLIED_TEXT")
        if status == "LIVE_THIS_RUN" and not HEX40.fullmatch(sha):
            errors.append("LIVE_THIS_RUN requires a 40-character lowercase hex SCHEMA CONTENT SHA")
        if expected_schema_sha and sha != expected_schema_sha:
            errors.append(
                f"SCHEMA CONTENT SHA {sha!r} does not match expected current SHA {expected_schema_sha!r}"
            )
        if compatibility != "PASS":
            errors.append("SCHEMA COMPATIBILITY must be PASS")
        if "LEGACY-SIGNATURE GATE:" in basis and "PASS" not in basis.split("LEGACY-SIGNATURE GATE:", 1)[1][:160]:
            errors.append("LEGACY-SIGNATURE GATE must PASS")

    for pattern in LEGACY_ACTIVE_PATTERNS:
        if pattern in text:
            errors.append(f"legacy active signature present: {pattern!r}")

    lots = _lot_blocks(text)
    if not lots:
        errors.append("at least one '# LOT ...' section is required")
        return errors

    for i, lot in enumerate(lots, 1):
        label = f"LOT {i}"
        if "## PREFLIGHT RECORD" not in lot:
            errors.append(f"{label}: missing visible PREFLIGHT RECORD")
            continue

        for heading in PROMPT_HEADINGS:
            if lot.count(heading) != 1:
                errors.append(f"{label}: must contain exactly one {heading!r}")

        p1 = lot.find(PROMPT_HEADINGS[0])
        preflight = lot[:p1 if p1 >= 0 else len(lot)]

        for field in REQUIRED_PREFLIGHT_FIELDS:
            if field not in preflight:
                errors.append(f"{label}: preflight missing {field}")

        level = _field_value(preflight, "USER-REQUESTED LEVEL:")
        if level == "ISSUE_TASK":
            for field in (
                "PROBLEM KERNEL:",
                "CURRENT ANSWER QUARANTINE:",
                "KERNEL-COVERAGE GATE:",
                "SAME-ISSUE IDENTITY GATE:",
                "ANSWER-EXCLUSION GATE:",
            ):
                if field not in preflight:
                    errors.append(f"{label}: ISSUE_TASK missing {field}")
            for gate in (
                "KERNEL-COVERAGE GATE:",
                "SAME-ISSUE IDENTITY GATE:",
                "ANSWER-EXCLUSION GATE:",
            ):
                tail = preflight.split(gate, 1)[1][:220] if gate in preflight else ""
                if "PASS" not in tail:
                    errors.append(f"{label}: {gate} must PASS for ISSUE_TASK")

        complex_mode = _field_value(preflight, "COMPLEX MODE:")
        if complex_mode not in {"ON", "OFF"}:
            errors.append(f"{label}: COMPLEX MODE must be ON or OFF")
        if complex_mode == "ON":
            tail = preflight.split("COMPLEX Q1–Q5 COVERAGE:", 1)[1][:220] if "COMPLEX Q1–Q5 COVERAGE:" in preflight else ""
            if "PASS" not in tail:
                errors.append(f"{label}: COMPLEX Q1–Q5 COVERAGE must PASS when complex mode is ON")

        if p1 >= 0:
            p2 = lot.find(PROMPT_HEADINGS[1], p1 + 1)
            prompt1 = lot[p1:p2 if p2 >= 0 else len(lot)]
            prompt1_lower = prompt1.lower()
            if "register is the thing" in prompt1_lower:
                errors.append(f"{label}: Prompt 1 is artifact-form anchored to a register")
            for phrase in PROMPT1_METHOD_META_PATTERNS:
                if phrase in prompt1_lower:
                    errors.append(f"{label}: Prompt 1 leaks generator/method language: {phrase!r}")

        p3 = lot.find(PROMPT_HEADINGS[2])
        if p3 >= 0:
            prompt3 = lot[p3:]
            for phrase in (
                "produce the reconciled register",
                "your deliverable is a better current register",
            ):
                if phrase in prompt3.lower():
                    errors.append(f"{label}: Prompt 3 predetermines artifact survival: {phrase!r}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate structural conformance of generated three-pass prompt Markdown."
    )
    parser.add_argument("path", help="Generated Markdown file")
    parser.add_argument("--expected-schema-sha", default=None)
    args = parser.parse_args()

    text = Path(args.path).read_text(encoding="utf-8")
    errors = validate_text(text, args.expected_schema_sha)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("PASS")


if __name__ == "__main__":
    main()
