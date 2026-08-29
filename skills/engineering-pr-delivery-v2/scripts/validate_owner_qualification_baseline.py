#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

TERMINAL = {"COMPLETE", "SUPERSEDED", "ABANDONED", "CLOSED"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip() if m else None


def section(text, title):
    m = re.search(rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|\Z)", text)
    return m.group(1).strip() if m else None


def norm(value):
    return re.sub(r"\s+", "", str(value).lower())


def active_questions(text):
    sec = section(text, "Active qualification questions")
    if not sec:
        return {}
    matches = list(re.finditer(r"(?mi)^Q([1-5])\s*:\s*", sec))
    out = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(sec)
        out[f"Q{m.group(1)}"] = sec[m.end():end].strip()
    return out


def question_set_id(text):
    pack = section(text, "Takeover qualification pack") or ""
    return field(pack, "QUESTION_SET_ID") or field(text, "QUESTION_SET_ID")


def validate_endpoint(root, chain, text):
    errors = []
    discovery = field(text, "OWNER_QUALIFICATION_BASELINE_DISCOVERY")
    source = field(text, "OWNER_QUALIFICATION_BASELINE_SOURCE")
    manifest_rel = field(text, "OWNER_QUALIFICATION_BASELINE_MANIFEST")
    status = field(text, "OWNER_QUALIFICATION_BASELINE_STATUS")
    if not any((discovery, source, manifest_rel, status)):
        return [], True
    if discovery != "COMPLETE":
        errors.append(f"{chain}: OWNER_QUALIFICATION_BASELINE_DISCOVERY must be COMPLETE")
    if not source:
        errors.append(f"{chain}: OWNER_QUALIFICATION_BASELINE_SOURCE missing")
        return errors, False
    if source.upper().startswith("NONE"):
        if manifest_rel and not manifest_rel.upper().startswith("NONE"):
            errors.append(f"{chain}: source NONE cannot bind a baseline manifest")
        if status != "NOT_APPLICABLE":
            errors.append(f"{chain}: source NONE requires baseline status NOT_APPLICABLE")
        return errors, False
    if not manifest_rel or manifest_rel.upper().startswith("NONE"):
        errors.append(f"{chain}: Owner baseline source requires OWNER_QUALIFICATION_BASELINE_MANIFEST")
        return errors, False
    manifest_path = root / manifest_rel
    if not manifest_path.is_file():
        errors.append(f"{chain}: baseline manifest missing: {manifest_rel}")
        return errors, False
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{chain}: baseline manifest is invalid JSON: {exc}")
        return errors, False
    if data.get("version") != 1:
        errors.append(f"{chain}: baseline manifest version must be 1")
    if data.get("source") != source:
        errors.append(f"{chain}: manifest source {data.get('source')} != endpoint source {source}")
    if data.get("sourceAuthority") != "OWNER":
        errors.append(f"{chain}: manifest sourceAuthority must be OWNER")
    qsid = question_set_id(text)
    if data.get("activeQuestionSetId") != qsid:
        errors.append(f"{chain}: manifest activeQuestionSetId {data.get('activeQuestionSetId')} != endpoint {qsid}")
    active = active_questions(text)
    if set(active) != {"Q1", "Q2", "Q3", "Q4", "Q5"}:
        errors.append(f"{chain}: Active qualification questions must contain Q1-Q5 before baseline coverage can be proven")
        return errors, False
    for item in data.get("questions", []):
        label = item.get("baselineQuestion", "?")
        covered = item.get("coveredBy") or []
        missing = [q for q in covered if q not in active]
        if not covered or missing:
            errors.append(f"{chain}: baseline {label} has invalid coveredBy {covered}; missing {missing}")
            continue
        union = "\n".join(active[q] for q in covered)
        n = norm(union)
        for literal in item.get("requiredLiterals", []):
            if norm(literal) not in n:
                errors.append(f"{chain}: baseline {label} lost required literal {literal!r} in {covered}")
        for concept in item.get("requiredConcepts", []):
            if norm(concept) not in n:
                errors.append(f"{chain}: baseline {label} lost required concept {concept!r} in {covered}")
        lower = union.lower()
        for obligation in item.get("requiredObligations", []):
            if str(obligation).lower() not in lower:
                errors.append(f"{chain}: baseline {label} lost required obligation {obligation!r} in {covered}")
    if status != "SATISFIED":
        errors.append(f"{chain}: Owner baseline source requires OWNER_QUALIFICATION_BASELINE_STATUS: SATISFIED")
    return errors, False


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_owner_qualification_baseline.py <repo-root-or-agents/chains>", file=sys.stderr)
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
        active_path = d / "ACTIVE.md"
        if not active_path.is_file():
            continue
        at = active_path.read_text(encoding="utf-8")
        if field(at, "CHAIN_STATE_VERSION") != "3" or (field(at, "STATE") or "") in TERMINAL:
            continue
        ep_rel = field(at, "ACTIVE_ENDPOINT_FILE")
        ep = root / ep_rel if ep_rel else None
        if not ep or not ep.is_file():
            continue
        e, was_grandfathered = validate_endpoint(root, field(at, "CHAIN_ID") or d.name, ep.read_text(encoding="utf-8"))
        if was_grandfathered:
            grandfathered += 1
        else:
            checked += 1
        errors.extend(e)
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: Owner qualification baseline coverage ({checked} adopted chain(s); {grandfathered} historical chain(s) grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
