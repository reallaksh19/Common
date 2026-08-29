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

PROFILE_TOKENS = {
    "FEA": {"element", "node", "mesh", "dof", "stiffness", "jacobian", "det(j)", "equilibrium", "reaction", "recovery", "transform"},
    "WRC_LOCAL_STRESS": {"shell", "attachment", "axis", "geometry", "force", "moment", "load", "stress", "coefficient", "gamma", "beta"},
    "LOAD_CALC": {"support", "force", "moment", "load", "equilibrium", "reaction", "allocation", "unallocated", "gravity", "cog"},
    "FIXED_FORMAT_WRITER": {"byte", "field", "column", "pointer", "cardinality", "record", "row", "offset", "width", "fortran", "i13"},
    "PARSER_TOPOLOGY": {"parser", "topology", "node", "edge", "pointer", "cardinality", "hash", "schema", "record"},
    "SOURCE_GOVERNANCE": {"source", "page", "section", "equation", "table", "figure", "authority", "applicability", "claim", "ledger", "locator"},
    "GENERAL_ENGINEERING": set(),
}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip() if m else None


def section(text, title):
    m = re.search(rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|\Z)", text)
    return m.group(1).strip() if m else None


def qbody(pack, n):
    m = re.search(rf"(?mis)^####\s+Q{n}\s+—\s+{re.escape(TITLES[n])}\s*$\n(.*?)(?=^####\s+Q[1-5]\s+—|\Z)", pack or "")
    return m.group(1).strip() if m else None


def nonempty(body, marker):
    value = field(body or "", marker)
    return bool(value and not value.upper().startswith(("NONE", "N/A", "NOT APPLICABLE")))


def validate_endpoint(path: Path):
    text = path.read_text(encoding="utf-8")
    pack = section(text, "Takeover qualification pack")
    if not pack:
        return [f"{path}: missing Takeover qualification pack"]
    errors = []
    profile = field(pack, "QUALIFICATION_PROFILE") or field(text, "QUALIFICATION_PROFILE")
    if profile not in PROFILE_TOKENS:
        return [f"{path}: QUALIFICATION_PROFILE must be one of {', '.join(PROFILE_TOKENS)}; found {profile}"]

    bodies = {}
    for n in range(1, 6):
        body = qbody(pack, n)
        if body is None:
            continue
        bodies[n] = body
        for marker in ("Domain challenge", "Exact repository data required"):
            if not nonempty(body, marker):
                errors.append(f"{path}: {profile} Q{n} missing {marker}")

    for n in (2, 4):
        if n in bodies and not nonempty(bodies[n], "Calculation/reconstruction"):
            errors.append(f"{path}: {profile} Q{n} requires Calculation/reconstruction")

    combined = "\n".join(bodies.values()).lower()
    tokens = PROFILE_TOKENS[profile]
    if tokens:
        hits = sorted(token for token in tokens if token in combined)
        if len(hits) < 3:
            errors.append(f"{path}: {profile} pack lacks profile-specific technical anchors (need >=3 token families; found {hits})")

    weak_only = 0
    for n, body in bodies.items():
        challenge = (field(body, "Domain challenge") or "").lower()
        strong = re.search(r"\b(calculate|compute|reconstruct|derive|assemble|trace|predict|falsif|compare|prove|map|transport)\w*\b", challenge)
        weak = re.search(r"\b(explain|describe|list|re-read|summarize)\w*\b", challenge)
        if weak and not strong:
            weak_only += 1
    if weak_only >= 2:
        errors.append(f"{path}: {profile} pack has {weak_only} weak descriptive Domain challenge fields without technical reconstruction verbs")

    if profile == "SOURCE_GOVERNANCE":
        q1 = bodies.get(1, "")
        q2q4 = (bodies.get(2, "") + "\n" + bodies.get(4, "")).lower()
        if not re.search(r"(ledger|claim|consumer|implementation|adapter|route|checker|runtime)", q1, re.I):
            errors.append(f"{path}: SOURCE_GOVERNANCE Q1 must reconstruct source custody into an implementation/checker/consumer boundary")
        if not re.search(r"(page|section|equation|table|figure|locator|input inventory|applicability)", q2q4, re.I):
            errors.append(f"{path}: SOURCE_GOVERNANCE Q2/Q4 must require exact source-locator/applicability reconstruction")

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_qualification_profile.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2
    supplied = Path(sys.argv[1]).resolve()
    chains = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
    if not chains.is_dir():
        print(f"FAIL: canonical chain store not found: {chains}")
        return 1
    root = chains.parent.parent
    errors = []
    checked = 0
    for d in sorted(p for p in chains.iterdir() if p.is_dir()):
        active = d / "ACTIVE.md"
        if not active.is_file():
            continue
        at = active.read_text(encoding="utf-8")
        if field(at, "CHAIN_STATE_VERSION") != "3":
            continue
        ep_rel = field(at, "ACTIVE_ENDPOINT_FILE")
        if not ep_rel:
            continue
        ep = root / ep_rel
        if ep.is_file() and field(ep.read_text(encoding="utf-8"), "STATE") not in {"COMPLETE", "SUPERSEDED"}:
            checked += 1
            errors.extend(validate_endpoint(ep))
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: domain qualification profiles ({checked} endpoint(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
