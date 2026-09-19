#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_PROTOCOL_REVISION = "TPG-3P-2026-09-19-R4"

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

INVALID_THREE_PASS_PROTOCOL_PATTERNS = (
    "# QUALIFICATION GATE",
    "## QUALIFICATION GATE",
    "QUALIFICATION GATE — ANSWER QSET",
    "schema_version: relay-v2.5-question-set",
    "route_key: \"SERIAL:TO_BE_BOUND\"",
    "ep_contract_digest: TO_BE_BOUND",
    "QUESTION_SET_ADMISSION_STATUS",
    "Do not proceed to Pass 3 until that evaluation returns PASS",
    "ADMISSION GATE — check before anything else",
    "QUESTION_SET_ADMISSION_STATUS",
    "Submit your Q1–Q5 answers with your reality reconstruction to an independent evaluator",
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


PROMPT1_MACHINE_SURFACE_PATTERNS = (
    "q1 — production_path",
    "q2 — engineering_problem",
    "q3 — boundaries_invariants",
    "q4 — verification",
    "q5 — first_safe_slice",
    "required_output_keys:",
    "reconstruction_mode:",
    "payload.source:",
    "payload.values:",
    "evidence_required:",
    "oracle_refs:",
    "independence_requirement:",
    "step_refs:",
    "mutation.protected_invariant:",
    "mutation.falsifier:",
)

REQUIRED_BASIS_FIELDS = (
    "PROTOCOL REVISION:",
    "GENERATOR MODE:",
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
    "PROBLEM WITNESS TYPE:",
    "PROBLEM WITNESS SOURCE:",
    "PROBLEM WITNESS PAYLOAD:",
    "WITNESS CLAIM(S) TO REPRODUCE:",
    "WHY THIS WITNESS EXPOSES THE ISSUE:",
    "WITNESS INTERPRETATION QUARANTINE:",
    "INDEPENDENT WORK PRODUCT:",
    "WHY NOW:",
    "STARTING PREMISE:",
    "RESPONSIBLE ACTOR / JOB:",
    "OWNED QUESTION:",
    "NON-GOALS / OWNERSHIP BOUNDARY:",
    "ISSUE DIFFERENTIATOR:",
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
    "TASK-CONTRACT FIDELITY GATE:",
    "NEIGHBOUR-SEPARATION GATE:",
    "PROBLEM-WITNESS SELECTION GATE:",
    "WITNESS-INDEPENDENCE GATE:",
    "KERNEL-COVERAGE GATE:",
    "SAME-ISSUE IDENTITY GATE:",
    "ANSWER-EXCLUSION GATE:",
    "ARTIFACT-ERASURE GATE:",
    "CURRENT-VOCABULARY GATE:",
    "PROMPT-1 OBJECT GATE:",
    "HUMAN-Q-LABEL GATE:",
    "HUMAN-IMMERSION GATE:",
    "PROMPT-3 FREEDOM GATE:",
    "COMPLEX Q1–Q5 COVERAGE:",
    "MODE-ISOLATION GATE:",
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


def _handshake_block(text: str) -> str:
    start = text.find("# SCHEMA EXECUTION HANDSHAKE")
    basis = text.find("# SCHEMA BASIS")
    if start < 0:
        return ""
    return text[start:basis if basis > start else len(text)]


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

    if not text.lstrip().startswith("# SCHEMA EXECUTION HANDSHAKE"):
        errors.append("output must begin with '# SCHEMA EXECUTION HANDSHAKE'")

    handshake = _handshake_block(text)
    if not handshake:
        errors.append("missing SCHEMA EXECUTION HANDSHAKE block")
    else:
        revision = _field_value(handshake, "PROTOCOL REVISION:")
        handshake_mode = _field_value(handshake, "GENERATOR MODE:")
        handshake_status = _field_value(handshake, "SCHEMA FETCH STATUS:")
        handshake_sha = _field_value(handshake, "SCHEMA CONTENT SHA:")
        handshake_result = _field_value(handshake, "HANDSHAKE STATUS:")
        if revision != EXPECTED_PROTOCOL_REVISION:
            errors.append(
                f"PROTOCOL REVISION must be {EXPECTED_PROTOCOL_REVISION}"
            )
        if handshake_mode != "THREE_PASS_ONLY":
            errors.append("handshake GENERATOR MODE must be THREE_PASS_ONLY")
        if handshake_status != "LIVE_THIS_RUN":
            errors.append("handshake SCHEMA FETCH STATUS must be LIVE_THIS_RUN")
        if not HEX40.fullmatch(handshake_sha):
            errors.append("handshake requires a 40-character lowercase hex SCHEMA CONTENT SHA")
        if handshake_result != "PASS":
            errors.append("HANDSHAKE STATUS must be PASS")

    basis = _basis_block(text)
    if not basis:
        errors.append("missing SCHEMA BASIS block")
    else:
        for field in REQUIRED_BASIS_FIELDS:
            if field not in basis:
                errors.append(f"SCHEMA BASIS missing {field}")

        basis_revision = _field_value(basis, "PROTOCOL REVISION:")
        status = _field_value(basis, "SCHEMA FETCH STATUS:")
        sha = _field_value(basis, "SCHEMA CONTENT SHA:")
        mode = _field_value(basis, "GENERATOR MODE:")
        compatibility = _field_value(basis, "SCHEMA COMPATIBILITY:")

        if basis_revision != EXPECTED_PROTOCOL_REVISION:
            errors.append(
                f"SCHEMA BASIS PROTOCOL REVISION must be {EXPECTED_PROTOCOL_REVISION}"
            )
        if mode != "THREE_PASS_ONLY":
            errors.append("GENERATOR MODE must be THREE_PASS_ONLY")
        if handshake:
            handshake_sha = _field_value(handshake, "SCHEMA CONTENT SHA:")
            if sha and handshake_sha and sha != handshake_sha:
                errors.append("handshake SHA and SCHEMA BASIS SHA must match")
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

    for pattern in INVALID_THREE_PASS_PROTOCOL_PATTERNS:
        if pattern in text:
            errors.append(f"formal relay QSET/admission protocol is invalid in three-pass output: {pattern!r}")

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
        user_intent = _field_value(preflight, "USER INTENT:")
        intent_type = _field_value(preflight, "INTENT TYPE:")
        authorized_actions = _field_value(preflight, "AUTHORIZED ACTIONS:")
        intent_completion = _field_value(preflight, "INTENT COMPLETION TEST:")
        if not user_intent:
            errors.append(f"{label}: USER INTENT must be substantive")
        if intent_type not in {"ANALYZE_ONLY", "ANALYZE_THEN_ACT", "EXECUTE_DEFINED_ACTION", "DECIDE", "HANDOVER"}:
            errors.append(f"{label}: INTENT TYPE is invalid: {intent_type!r}")
        if not authorized_actions:
            errors.append(f"{label}: AUTHORIZED ACTIONS must be explicit; use NONE for analysis-only")
        if not intent_completion:
            errors.append(f"{label}: INTENT COMPLETION TEST must be substantive")
        intent_gate_value = _field_value(preflight, "INTENT-FIDELITY GATE:")
        if not intent_gate_value.startswith("PASS"):
            errors.append(f"{label}: INTENT-FIDELITY GATE must PASS")

        if level == "ISSUE_TASK":
            for field in (
                "WHY NOW:",
                "STARTING PREMISE:",
                "RESPONSIBLE ACTOR / JOB:",
                "OWNED QUESTION:",
                "NON-GOALS / OWNERSHIP BOUNDARY:",
                "ISSUE DIFFERENTIATOR:",
                "PROBLEM KERNEL:",
                "CURRENT ANSWER QUARANTINE:",
                "TASK-CONTRACT FIDELITY GATE:",
                "NEIGHBOUR-SEPARATION GATE:",
                "PROBLEM-WITNESS SELECTION GATE:",
                "WITNESS-INDEPENDENCE GATE:",
                "KERNEL-COVERAGE GATE:",
                "SAME-ISSUE IDENTITY GATE:",
                "ANSWER-EXCLUSION GATE:",
            ):
                if field not in preflight:
                    errors.append(f"{label}: ISSUE_TASK missing {field}")
            for gate in (
                "TASK-CONTRACT FIDELITY GATE:",
                "NEIGHBOUR-SEPARATION GATE:",
                "PROBLEM-WITNESS SELECTION GATE:",
                "WITNESS-INDEPENDENCE GATE:",
                "KERNEL-COVERAGE GATE:",
                "SAME-ISSUE IDENTITY GATE:",
                "ANSWER-EXCLUSION GATE:",
            ):
                tail = preflight.split(gate, 1)[1][:220] if gate in preflight else ""
                if "PASS" not in tail:
                    errors.append(f"{label}: {gate} must PASS for ISSUE_TASK")

        witness_type = _field_value(preflight, "PROBLEM WITNESS TYPE:")
        if level == "ISSUE_TASK":
            if not witness_type:
                errors.append(f"{label}: ISSUE_TASK requires PROBLEM WITNESS TYPE")
            if witness_type != "NONE":
                witness_required = (
                    "PROBLEM WITNESS SOURCE:",
                    "PROBLEM WITNESS PAYLOAD:",
                    "WHY THIS WITNESS EXPOSES THE ISSUE:",
                    "INDEPENDENT WORK PRODUCT:",
                )
                for field in witness_required:
                    if field not in preflight:
                        errors.append(f"{label}: selected witness missing {field}")
                    elif not _field_value(preflight, field):
                        errors.append(f"{label}: selected witness requires a substantive value for {field}")
        complex_mode = _field_value(preflight, "COMPLEX MODE:")
        if complex_mode not in {"ON", "OFF"}:
            errors.append(f"{label}: COMPLEX MODE must be ON or OFF")
        if complex_mode == "ON":
            tail = preflight.split("COMPLEX Q1–Q5 COVERAGE:", 1)[1][:220] if "COMPLEX Q1–Q5 COVERAGE:" in preflight else ""
            if "PASS" not in tail:
                errors.append(f"{label}: COMPLEX Q1–Q5 COVERAGE must PASS when complex mode is ON")
            qset_tail = preflight.split("MODE-ISOLATION GATE:", 1)[1][:220] if "MODE-ISOLATION GATE:" in preflight else ""
            if "PASS" not in qset_tail:
                errors.append(f"{label}: MODE-ISOLATION GATE must PASS when complex mode is ON")

        if p1 >= 0:
            p2 = lot.find(PROMPT_HEADINGS[1], p1 + 1)
            prompt1 = lot[p1:p2 if p2 >= 0 else len(lot)]
            prompt1_lower = prompt1.lower()
            if "register is the thing" in prompt1_lower:
                errors.append(f"{label}: Prompt 1 is artifact-form anchored to a register")
            for phrase in PROMPT1_METHOD_META_PATTERNS:
                if phrase in prompt1_lower:
                    errors.append(f"{label}: Prompt 1 leaks generator/method language: {phrase!r}")
            for phrase in PROMPT1_MACHINE_SURFACE_PATTERNS:
                if phrase in prompt1_lower:
                    errors.append(f"{label}: Prompt 1 exposes machine/taxonomy surface language: {phrase!r}")

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
