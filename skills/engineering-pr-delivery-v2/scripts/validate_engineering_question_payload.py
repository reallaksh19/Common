#!/usr/bin/env python3
from pathlib import Path
import re
import sys

NUMERIC_PROFILES = {"FEA", "WRC_LOCAL_STRESS", "LOAD_CALC", "FIXED_FORMAT_WRITER"}
TERMINAL = {"COMPLETE", "SUPERSEDED", "ABANDONED", "CLOSED"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip() if m else None


def section(text, title):
    m = re.search(rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|\Z)", text)
    return m.group(1).strip() if m else None


def qbody(pack, n):
    m = re.search(rf"(?mis)^####\s+Q{n}\s+—[^\n]*$\n(.*?)(?=^####\s+Q[1-5]\s+—|\Z)", pack or "")
    return m.group(1).strip() if m else None


def nonempty(value):
    return bool(value and not value.upper().startswith(("NONE", "N/A", "NOT APPLICABLE", "TBD")))


def numeric_count(value):
    return len(re.findall(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", value or ""))


def validate_endpoint(chain, text):
    if field(text, "QUALIFICATION_PROFILE_VERSION") != "2":
        return [], True
    errors = []
    pack = section(text, "Takeover qualification pack")
    if not pack:
        return [f"{chain}: profile-v2 endpoint missing Takeover qualification pack"], False
    profile = field(pack, "QUALIFICATION_PROFILE") or field(text, "QUALIFICATION_PROFILE")
    if field(pack, "QUALIFICATION_PROFILE_VERSION") != "2":
        errors.append(f"{chain}: qualification pack must declare QUALIFICATION_PROFILE_VERSION: 2")
    bodies = {}
    concrete_numeric = 0
    for n in range(1, 6):
        body = qbody(pack, n)
        if body is None:
            errors.append(f"{chain}: missing detailed Q{n}")
            continue
        bodies[n] = body
        payload = field(body, "Concrete payload")
        derivation = field(body, "Required derivation")
        if not nonempty(payload):
            errors.append(f"{chain}: Q{n} missing non-empty Concrete payload")
        if not nonempty(derivation):
            errors.append(f"{chain}: Q{n} missing non-empty Required derivation")
        if nonempty(payload) and numeric_count(payload) >= 3:
            concrete_numeric += 1
    if profile in NUMERIC_PROFILES:
        for n in (2, 4):
            body = bodies.get(n, "")
            payload = field(body, "Concrete payload")
            derivation = field(body, "Required derivation")
            if not nonempty(payload) or numeric_count(payload) < 3:
                errors.append(f"{chain}: {profile} Q{n} must carry at least three concrete numeric literals")
            if not nonempty(derivation):
                errors.append(f"{chain}: {profile} Q{n} requires an explicit derivation/calculation")
        if concrete_numeric < 2:
            errors.append(f"{chain}: {profile} pack requires >=2 questions with hand-computable concrete numeric payload; found {concrete_numeric}")
    return errors, False


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_engineering_question_payload.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2
    supplied = Path(sys.argv[1]).resolve()
    chains = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
    root = chains.parent.parent if supplied.name == "chains" else supplied
    if not chains.is_dir():
        print(f"FAIL: canonical chain store not found: {chains}")
        return 1
    errors = []
    checked = grandfathered = 0
    for d in sorted(p for p in chains.iterdir() if p.is_dir()):
        a = d / "ACTIVE.md"
        if not a.is_file():
            continue
        at = a.read_text(encoding="utf-8")
        if field(at, "CHAIN_STATE_VERSION") != "3" or (field(at, "STATE") or "") in TERMINAL:
            continue
        rel = field(at, "ACTIVE_ENDPOINT_FILE")
        ep = root / rel if rel else None
        if not ep or not ep.is_file():
            continue
        e, old = validate_endpoint(field(at, "CHAIN_ID") or d.name, ep.read_text(encoding="utf-8"))
        errors.extend(e)
        grandfathered += int(old)
        checked += int(not old)
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: concrete engineering qualification payload ({checked} profile-v2 chain(s); {grandfathered} historical chain(s) grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
