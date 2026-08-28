#!/usr/bin/env python3
from pathlib import Path
import re
import sys

TITLES = {
    1: "Production Trace",
    2: "Current Unresolved Problem / Failure Isolation",
    3: "Authority / Invariant",
    4: "Independent Validation",
    5: "Next Contribution / Minimal Patch",
}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip() if m else None


def section(text, title):
    m = re.search(rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|\Z)", text)
    return m.group(1).strip() if m else None


def qbody(pack, n):
    title = TITLES[n]
    m = re.search(rf"(?mis)^####\s+Q{n}\s+—\s+{re.escape(title)}\s*$\n(.*?)(?=^####\s+Q[1-5]\s+—|\Z)", pack)
    return m.group(1).strip() if m else None


def nonempty_marker(body, marker):
    m = re.search(rf"(?mi)^\s*{re.escape(marker)}\s*:\s*(.+)$", body or "")
    if not m:
        return False
    value = m.group(1).strip()
    return bool(value and not value.upper().startswith(("NONE", "N/A", "NOT APPLICABLE")))


def validate_endpoint(path):
    text = path.read_text(encoding="utf-8")
    pack = section(text, "Takeover qualification pack")
    if pack is None:
        return [f"{path}: missing Takeover qualification pack"]
    errors = []
    required_headers = {
        "PURPOSE": "QUALIFICATION_ONLY",
        "NOT_AN_IMPLEMENTATION_TASK": "TRUE",
        "QUALIFICATION_PROTOCOL_VERSION": "3",
        "QUESTION_SET_ADMISSION_REQUIREMENT": "REQUIRED_ON_TAKEOVER",
    }
    for name, expected in required_headers.items():
        if field(pack, name) != expected:
            errors.append(f"{path}: {name} must be {expected}")
    for name in ("QUALIFICATION_BASIS_HEAD", "QUESTION_SET_ID", "QUESTION_SET_AUTHOR"):
        if not field(pack, name):
            errors.append(f"{path}: missing {name}")

    bodies = {}
    for n in range(1, 6):
        body = qbody(pack, n)
        if body is None:
            errors.append(f"{path}: missing Q{n} — {TITLES[n]}")
            continue
        bodies[n] = body
        if not nonempty_marker(body, "Repository anchors"):
            errors.append(f"{path}: Q{n} requires concrete Repository anchors")
        if not nonempty_marker(body, "Fail if"):
            errors.append(f"{path}: Q{n} requires explicit Fail if")
        if len(re.findall(r"\S+", body)) < 25:
            errors.append(f"{path}: Q{n} is too shallow (<25 words of rubric/evidence)")

    requirements = {
        1: ("Production object/case", "Required technical work"),
        2: ("Calculation/reconstruction", "Required numerical/technical evidence", "Predicted intermediate values", "First wrong boundary", "Falsifier"),
        3: ("Authority/source trace", "Protected invariant", "Falsifier", "Invalid shortcut"),
        4: ("Independent oracle", "Required numerical/technical evidence", "Units/sign/tolerance", "Falsifier"),
        5: ("Safe patch boundary", "Expected before/after evidence", "Validation required", "Negative test", "Rollback/falsifier boundary", "No-patch condition"),
    }
    for n, markers in requirements.items():
        if n not in bodies:
            continue
        for marker in markers:
            if not nonempty_marker(bodies[n], marker):
                errors.append(f"{path}: Q{n} missing {marker}")

    if 5 in bodies and re.search(r"(?mi)^\s*(Implement|Fix|Modify|Patch|Change|Create)\b", bodies[5]):
        errors.append(f"{path}: Q5 is written as an implementation task, not qualification")

    technical = sum(nonempty_marker(bodies.get(n, ""), "Required numerical/technical evidence") for n in range(1, 6))
    technical += int(nonempty_marker(bodies.get(2, ""), "Calculation/reconstruction"))
    if technical < 2:
        errors.append(f"{path}: set requires at least two numerical/technical reconstructions")
    if not nonempty_marker(bodies.get(4, ""), "Independent oracle"):
        errors.append(f"{path}: set requires an independent oracle")
    if not any(nonempty_marker(bodies.get(n, ""), "Falsifier") for n in range(1, 6)):
        errors.append(f"{path}: set requires an explicit falsifier")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_qualification_questions.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2
    supplied = Path(sys.argv[1]).resolve()
    chains = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
    if not chains.is_dir():
        print(f"FAIL: canonical chain store not found: {chains}")
        return 1
    errors = []
    checked = 0
    for d in sorted(p for p in chains.iterdir() if p.is_dir()):
        active = d / "ACTIVE.md"
        if not active.is_file():
            continue
        at = active.read_text(encoding="utf-8")
        if field(at, "CHAIN_STATE_VERSION") != "3":
            continue
        ep = field(at, "ACTIVE_ENDPOINT_FILE")
        if not ep:
            continue
        root = chains.parent.parent
        p = root / ep
        if p.is_file() and field(p.read_text(encoding="utf-8"), "STATE") not in {"COMPLETE", "SUPERSEDED"}:
            checked += 1
            errors.extend(validate_endpoint(p))
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: expert qualification question packs ({checked} endpoint(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
