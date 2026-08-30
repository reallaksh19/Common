#!/usr/bin/env python3
from pathlib import Path
import re
import sys

TERMINAL = {"COMPLETE", "SUPERSEDED", "ABANDONED", "CLOSED"}
BOOL = {"TRUE", "FALSE"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip() if m else None


def adopted(text):
    return field(text, "HANDOVER_PROTOCOL_VERSION") == "2"


def evidence_ready(text):
    content = field(text, "HANDOVER_CONTENT_READY") == "TRUE"
    status = field(text, "HANDOVER_VALIDATION_STATUS")
    evidence = field(text, "HANDOVER_VALIDATION_EVIDENCE")
    valid_evidence = bool(evidence and evidence.upper() not in {"NONE", "N/A", "NOT_RUN"})
    return content and status == "PASS" and valid_evidence


def modern_planes(text):
    return field(text, "CHAIN_HANDOVER_READY") is not None or field(text, "TAKEOVER_QUALIFICATION_READY") is not None


def expected_ready(text):
    base = evidence_ready(text)
    if not modern_planes(text):
        return base
    chain_ready = field(text, "CHAIN_HANDOVER_READY") == "TRUE"
    takeover_ready = field(text, "TAKEOVER_QUALIFICATION_READY") == "TRUE"
    issue_ok = True
    if field(text, "WORK_ITEM_SOURCE") == "GITHUB_ISSUE":
        issue_ok = field(text, "ISSUE_HANDOVER_SYNC_STATUS") == "IN_SYNC"
    return base and chain_ready and takeover_ready and issue_ok


def validate_fields(label, text):
    errors = []
    expected = {
        "HANDOVER_PROTOCOL_VERSION": "2",
        "REPORTING_CONTRACT": "ACTIVE_HANDOVER_FIRST",
        "HANDOVER_RESPONSE_REQUIRED": "ALWAYS",
        "RESPONSE_DELTA_MODE": "DELTA_ONLY",
    }
    for name, wanted in expected.items():
        got = field(text, name)
        if got != wanted:
            errors.append(f"{label}: {name} expected {wanted}, found {got}")

    content = field(text, "HANDOVER_CONTENT_READY")
    status = field(text, "HANDOVER_VALIDATION_STATUS")
    ready = field(text, "HANDOVER_READY")
    if content not in BOOL:
        errors.append(f"{label}: HANDOVER_CONTENT_READY must be TRUE or FALSE")
    if status not in {"PASS", "FAIL", "NOT_RUN"}:
        errors.append(f"{label}: HANDOVER_VALIDATION_STATUS must be PASS, FAIL or NOT_RUN")
    if ready not in BOOL:
        errors.append(f"{label}: HANDOVER_READY must be TRUE or FALSE")

    if modern_planes(text):
        for name in ("CHAIN_HANDOVER_READY", "TAKEOVER_QUALIFICATION_READY"):
            if field(text, name) not in BOOL:
                errors.append(f"{label}: {name} must be TRUE or FALSE")
        qstatus = field(text, "QUESTION_SET_STATUS")
        takeover = field(text, "TAKEOVER_QUALIFICATION_READY")
        if qstatus == "STALE" and takeover == "TRUE":
            errors.append(f"{label}: STALE question set cannot be takeover-qualification ready")
        if field(text, "WORK_ITEM_SOURCE") == "GITHUB_ISSUE":
            sync = field(text, "ISSUE_HANDOVER_SYNC_STATUS")
            if sync not in {"IN_SYNC", "STALE", "NOT_RUN", "FAILED"}:
                errors.append(f"{label}: invalid ISSUE_HANDOVER_SYNC_STATUS={sync}")
            if ready == "TRUE" and sync != "IN_SYNC":
                errors.append(f"{label}: issue-based HANDOVER_READY TRUE requires Issue sync IN_SYNC")

    derived = "TRUE" if expected_ready(text) else "FALSE"
    if ready in BOOL and ready != derived:
        errors.append(f"{label}: HANDOVER_READY={ready} contradicts evidence/readiness-derived value {derived}")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_handover_readiness.py <repo-root-or-agents/chains>", file=sys.stderr)
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
        if not adopted(at):
            grandfathered += 1
            continue
        chain = field(at, "CHAIN_ID") or d.name
        checked += 1
        errors.extend(validate_fields(f"{chain} ACTIVE", at))
        rel = field(at, "ACTIVE_ENDPOINT_FILE")
        ep = root / rel if rel else None
        if not ep or not ep.is_file():
            errors.append(f"{chain}: active endpoint missing for readiness validation")
            continue
        et = ep.read_text(encoding="utf-8")
        if not adopted(et):
            errors.append(f"{chain}: ACTIVE adopted handover protocol 2 but endpoint did not")
            continue
        errors.extend(validate_fields(f"{chain} endpoint", et))
        for name in ("CHAIN_HANDOVER_READY", "TAKEOVER_QUALIFICATION_READY", "HANDOVER_READY"):
            if field(at, name) is not None or field(et, name) is not None:
                if field(at, name) != field(et, name):
                    errors.append(f"{chain}: ACTIVE/endpoint {name} mismatch")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: handover readiness evidence semantics ({checked} adopted chain(s); {grandfathered} historical chain(s) grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
