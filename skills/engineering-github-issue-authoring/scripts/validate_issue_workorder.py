#!/usr/bin/env python3
"""Structural validator for durable engineering issue/programme drafts.

This validator checks reconstruction quality. It does not grant or deny engineering
permission and must not be used as an execution gate.
"""
from pathlib import Path
import re
import sys

ROLES = {
    "SINGLE",
    "PROGRAM_ROOT",
    "WORK_PACKAGE",
    "PARALLEL_FOCUSED",
    "REVISION",
    "INTEGRATION",
    "RELAY_HANDOVER",
}
QUESTION_PROFILES = {"NUMERICAL_ENGINEERING", "SOFTWARE_ENGINEERING", "SOURCE_GOVERNANCE"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip().strip(chr(96)) if m else None


def has_heading(text, pattern):
    return bool(re.search(rf"(?mi)^#+\s+.*(?:{pattern}).*$", text))


def require_field(text, name, errors):
    value = field(text, name)
    if not value:
        errors.append(f"missing required field: {name}")
    return value


def require_heading(text, pattern, errors, label=None):
    if not has_heading(text, pattern):
        errors.append(f"missing required heading: {label or pattern}")


def validate_optional_questions(text, errors):
    m = re.search(r"(?mis)^#\s+Appendix A\s+.*implementation.*?$\n(.*)\Z", text)
    if not m:
        return
    app = m.group(1)
    profile = field(app, "QUESTION_PROFILE")
    if profile and profile not in QUESTION_PROFILES:
        errors.append(f"QUESTION_PROFILE must be one of {sorted(QUESTION_PROFILES)}; found {profile}")
    heads = list(re.finditer(r"(?mi)^##\s+Q([1-5])\b.*$", app))
    if heads:
        order = [x.group(1) for x in heads]
        if order != ["1", "2", "3", "4", "5"]:
            errors.append(f"when Q1-Q5 are present they must be complete and ordered; found {order}")


def validate_common(text, errors):
    if not re.search(r"\b[0-9a-f]{40}\b", text, re.I):
        errors.append("record an observed 40-hex repository SHA for creation/current basis")
    if "V3.1" not in text and "V3_1" not in text:
        errors.append("current Relay protocol must be explicit as V3.1 when Relay context is present")
    if re.search(r"(?i)engineering-pr-delivery-v2(?:\.5)?\b", text):
        errors.append("do not use V3/V2.5 legacy protocol paths as current issue semantics")


def validate_program_root(text, errors):
    require_field(text, "PROGRAM_ID", errors)
    if not (field(text, "PROGRAMME_BASIS_REVISION") or field(text, "PROGRAM_BASIS_REVISION")):
        errors.append("missing programme basis revision")
    for pattern, label in (
        (r"owner outcome|mission", "Owner outcome"),
        (r"why now|governing witness", "Why now / governing witnesses"),
        (r"non-goal|global protected|exclusion", "Non-goals"),
        (r"effective amendment index|amendment index", "Effective amendment index"),
        (r"canonical input|common input", "Canonical input registry"),
        (r"workstream registry|work-package.*registry|partition.*registry", "Workstream registry"),
        (r"producer.*consumer|consumer contract", "Producer/consumer contracts"),
        (r"dependenc", "Dependency contracts"),
        (r"exit criteria|definition of done|programme success", "Programme exit criteria"),
        (r"relay handover|operational ledger", "Relay Handover reference"),
    ):
        require_heading(text, pattern, errors, label)


def validate_child(text, role, errors):
    for pattern, label in (
        (r"outcome|mission", "Outcome"),
        (r"why now|concrete witness|ground truth", "Why now / witness"),
        (r"owned responsibility|bounded scope|partition", "Owned responsibility"),
        (r"ownership boundary|conflict-avoidance|protected sibling", "Ownership boundary"),
        (r"canonical input|source truth|input/source", "Canonical inputs/source truth"),
        (r"preserve|invariant", "Preserve / invariants"),
        (r"falsifier|negative test", "Falsifier"),
        (r"success oracle|definition of done|pass.*fail", "Success oracle"),
        (r"implementation plan", "Implementation Plan"),
        (r"handoff", "Expected handoff"),
        (r"semantic escalation|escalat", "Semantic escalation"),
    ):
        require_heading(text, pattern, errors, label)

    if role in {"WORK_PACKAGE", "PARALLEL_FOCUSED", "REVISION", "INTEGRATION"}:
        if not (
            field(text, "PARENT_WORK_ITEM_KEY")
            or field(text, "PROGRAMME")
            or field(text, "PARENT_PROGRAMME")
        ):
            errors.append("child issue must reference the parent programme")

    if role == "REVISION":
        pred = require_field(text, "PREDECESSOR_WORK_ITEM_KEY", errors)
        if pred == "NONE":
            errors.append("REVISION requires a predecessor work item")

    validate_optional_questions(text, errors)


def validate_handover(text, errors):
    if not (field(text, "PARENT_PROGRAMME") or field(text, "PARENT_WORK_ITEM_KEY")):
        errors.append("RELAY_HANDOVER must reference its parent programme")
    for pattern, label in (
        (r"non-authority rule|not.*authority", "Non-authority rule"),
        (r"programme basis", "Programme basis"),
        (r"workstreams", "Workstreams"),
        (r"dependency ledger|dependencies", "Dependency ledger"),
        (r"nonterminal pr", "Nonterminal PRs"),
        (r"pending items", "Pending items"),
        (r"known issues", "Known issues"),
        (r"negative knowledge|do-not-reopen", "Negative knowledge"),
        (r"handoff", "Producer/consumer handoffs"),
        (r"owner decisions needed", "Owner decisions needed"),
        (r"next coordinator action", "Next coordinator action"),
        (r"next useful observation|next observation", "Next useful observation"),
    ):
        require_heading(text, pattern, errors, label)


def validate(path):
    text = path.read_text(encoding="utf-8")
    errors = []
    role = field(text, "ISSUE_ROLE") or "SINGLE"
    if role not in ROLES:
        return [f"ISSUE_ROLE must be one of {sorted(ROLES)}; found {role}"]

    validate_common(text, errors)

    if role == "PROGRAM_ROOT":
        validate_program_root(text, errors)
    elif role == "RELAY_HANDOVER":
        validate_handover(text, errors)
    else:
        validate_child(text, role, errors)

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_issue_workorder.py <issue-draft.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: draft file not found: {path}")
        return 1
    errors = validate(path)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("PASS: issue draft is reconstructible under the non-blocking programme/child/Handover structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
