#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

COMPAT="schemas/three-pass-prompt-generator.schema.md"
HANDOVER="scripts/handover_planning.py"
SKILL="SKILL.md"
LAUNCHER_REL="skills/three-pass-prompt-generator/SKILL.md"
SCHEMA_REL="skills/three-pass-prompt-generator/schema.md"
VALIDATOR_REL="skills/three-pass-prompt-generator/validate.py"


def _text(path:Path)->str:
    return path.read_text(encoding="utf-8")


def _revision_from_schema(text:str)->str|None:
    match=re.search(r"(?m)^PROTOCOL REVISION:\s*\n?\s*(TPG-[A-Za-z0-9-]+)",text)
    return match.group(1) if match else None


def _revision_from_validator(text:str)->str|None:
    match=re.search(r'EXPECTED_PROTOCOL_REVISION\s*=\s*"([^"]+)"',text)
    return match.group(1) if match else None


def validate(skill_root:Path,repo_root:Path|None=None):
    e=[];w=[]
    skill_root=skill_root.resolve()
    repo_root=(repo_root or skill_root.parents[1]).resolve()

    compat_path=skill_root/COMPAT;handover_path=skill_root/HANDOVER;skill_path=skill_root/SKILL
    launcher=repo_root/LAUNCHER_REL;schema=repo_root/SCHEMA_REL;validator=repo_root/VALIDATOR_REL
    for label,path in (
        ("compatibility redirect",compat_path),
        ("handover planner",handover_path),
        ("engineering skill",skill_path),
        ("standalone launcher",launcher),
        ("standalone schema",schema),
        ("standalone validator",validator),
    ):
        if not path.exists():e.append(f"missing {label}: {path}")
    if e:return e,w

    compat=_text(compat_path);handover=_text(handover_path);engineering=_text(skill_path)
    launcher_text=_text(launcher);schema_text=_text(schema);validator_text=_text(validator)

    for token in (
        "skills/three-pass-prompt-generator/SKILL.md",
        "skills/three-pass-prompt-generator/schema.md",
        "skills/three-pass-prompt-generator/validate.py",
        "current `main`",
        "actual schema SHA",
        "THREE_PASS_ONLY",
    ):
        if token not in compat:e.append(f"compatibility redirect missing live-generator requirement: {token}")

    for token in (
        "skills/engineering-pr-delivery-v2.5/schemas/three-pass-prompt-generator.schema.md",
        "skills/three-pass-prompt-generator/SKILL.md",
        "skills/three-pass-prompt-generator/schema.md",
        '"mode":"THREE_PASS_ONLY"',
        '"complex_mode":bool(complex_project)',
        '"visible_q1_q5":bool(complex_project)',
    ):
        if token not in handover:e.append(f"handover planner missing generator binding: {token}")

    for token in (
        "PLAN_FOR_HANDOVER — COMBINED CONTROL TRANSACTION",
        "fetch current `main`",
        "live schema revision/SHA",
        "exactly three prompts",
        "Q1–Q5",
    ):
        if token not in engineering:e.append(f"engineering skill missing handover-generator control: {token}")

    for token in (
        "Fetch `skills/three-pass-prompt-generator/schema.md` from current `main`",
        "# SCHEMA EXECUTION HANDSHAKE",
        "GENERATOR MODE = THREE_PASS_ONLY",
        "Validate the artifact with `skills/three-pass-prompt-generator/validate.py`",
    ):
        if token not in launcher_text:e.append(f"standalone launcher missing required live behavior: {token}")

    for token in (
        "# SCHEMA EXECUTION HANDSHAKE",
        "THREE_PASS_ONLY",
        "## PROMPT 1 — IMAGINE",
        "## PROMPT 2 — UNDERSTAND",
        "## PROMPT 3 — REVALIDATE AND MOVE FORWARD",
        "COMPLEX Q1–Q5 COVERAGE:",
    ):
        if token not in schema_text:e.append(f"standalone schema missing required three-pass surface: {token}")

    schema_revision=_revision_from_schema(schema_text)
    validator_revision=_revision_from_validator(validator_text)
    if not schema_revision:e.append("cannot read live standalone schema protocol revision")
    if not validator_revision:e.append("cannot read standalone validator expected protocol revision")
    if schema_revision and validator_revision and schema_revision!=validator_revision:
        e.append(f"standalone schema/validator revision mismatch: {schema_revision} != {validator_revision}")

    if "PROMPT_HEADINGS" not in validator_text or "validate_text" not in validator_text:
        e.append("standalone validator no longer validates the three prompt artifact")

    return e,w


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("skill_root",nargs="?",default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--repo-root")
    a=ap.parse_args()
    e,w=validate(Path(a.skill_root),Path(a.repo_root) if a.repo_root else None)
    for item in w:print(f"WARNING: {item}")
    for item in e:print(f"ERROR: {item}")
    if e:
        print(f"FAIL: {len(e)} error(s), {len(w)} warning(s)")
        raise SystemExit(1)
    print(f"PASS: handover live-generator contract; {len(w)} warning(s)")


if __name__=="__main__":
    main()
