#!/usr/bin/env python3
from pathlib import Path
import re
import sys

COMMANDS = {
    "PROCEED_NEXT",
    "PROCEED_NEXT_NO_QS",
    "PROCEED_NEXT_HANDOVER_READY",
}
ACTIONS = {"REUSED", "REFRESHED", "SUPPRESSED_BY_OWNER", "NOT_APPLICABLE"}
QSTATUS = {"CURRENT", "STALE", "NOT_APPLICABLE"}
DISPLAY = {"SHOW", "HIDE"}
BOOL = {"TRUE", "FALSE"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip() if m else None


def validate(label, text):
    errors = []
    cmd = field(text, "OWNER_PROGRESSION_COMMAND")
    if not cmd:
        return errors, False
    if cmd not in COMMANDS:
        return [f"{label}: invalid OWNER_PROGRESSION_COMMAND={cmd}"], True

    scope = field(text, "QUALIFICATION_SCOPE_ID")
    qid = field(text, "QUESTION_SET_ID")
    status = field(text, "QUESTION_SET_STATUS")
    action = field(text, "QUESTION_PACK_ACTION")
    display = field(text, "QUESTION_DISPLAY")
    chain_ready = field(text, "CHAIN_HANDOVER_READY")
    takeover_ready = field(text, "TAKEOVER_QUALIFICATION_READY")

    for name, value, allowed in (
        ("QUESTION_SET_STATUS", status, QSTATUS),
        ("QUESTION_PACK_ACTION", action, ACTIONS),
        ("QUESTION_DISPLAY", display, DISPLAY),
        ("CHAIN_HANDOVER_READY", chain_ready, BOOL),
        ("TAKEOVER_QUALIFICATION_READY", takeover_ready, BOOL),
    ):
        if value not in allowed:
            errors.append(f"{label}: {name} invalid or missing: {value}")

    if status != "NOT_APPLICABLE":
        if not scope:
            errors.append(f"{label}: qualification scope required when questions apply")
        if not qid or qid.upper() in {"NONE", "N/A"}:
            errors.append(f"{label}: QUESTION_SET_ID required when questions apply")

    if cmd == "PROCEED_NEXT":
        if action not in {"REUSED", "REFRESHED", "NOT_APPLICABLE"}:
            errors.append(f"{label}: proceed next requires REUSED/REFRESHED/NOT_APPLICABLE action")
        if action == "REUSED":
            if display != "HIDE":
                errors.append(f"{label}: reused questions must be hidden")
            if status != "CURRENT" or takeover_ready != "TRUE":
                errors.append(f"{label}: reused Q-set must remain CURRENT and takeover-ready")
        elif action == "REFRESHED":
            if display != "SHOW" or status != "CURRENT" or takeover_ready != "TRUE":
                errors.append(f"{label}: refreshed Q-set must be SHOW/CURRENT/takeover-ready")
        elif action == "NOT_APPLICABLE":
            if status != "NOT_APPLICABLE" or display != "HIDE":
                errors.append(f"{label}: N/A qualification must remain hidden and NOT_APPLICABLE")

    elif cmd == "PROCEED_NEXT_NO_QS":
        if action != "SUPPRESSED_BY_OWNER":
            errors.append(f"{label}: no-Q mode requires SUPPRESSED_BY_OWNER")
        if display != "HIDE":
            errors.append(f"{label}: no-Q mode must hide questions")
        if status == "CURRENT" and takeover_ready != "TRUE":
            errors.append(f"{label}: CURRENT existing Q-set should remain takeover-ready")
        if status == "STALE" and takeover_ready != "FALSE":
            errors.append(f"{label}: STALE set in no-Q mode must make takeover readiness FALSE")
        if status == "NOT_APPLICABLE" and takeover_ready != "TRUE":
            errors.append(f"{label}: NOT_APPLICABLE qualification should not block takeover readiness")

    elif cmd == "PROCEED_NEXT_HANDOVER_READY":
        if action not in {"REUSED", "REFRESHED", "NOT_APPLICABLE"}:
            errors.append(f"{label}: hand-over-ready mode requires current/reused/refreshed qualification")
        if status == "STALE":
            errors.append(f"{label}: hand-over-ready mode cannot end with STALE questions")
        if status == "CURRENT" and display != "SHOW":
            errors.append(f"{label}: hand-over-ready mode must show full current Q1-Q5")
        if takeover_ready != "TRUE":
            errors.append(f"{label}: hand-over-ready mode requires TAKEOVER_QUALIFICATION_READY TRUE")
        # CHAIN_HANDOVER_READY may be FALSE only when an explicit blocker prevented the requested freeze.
        if chain_ready == "FALSE":
            blocker = field(text, "HANDOVER_VALIDATION_STATUS") in {"FAIL", "NOT_RUN"} or field(text, "ISSUE_HANDOVER_SYNC_STATUS") in {"STALE", "NOT_RUN", "FAILED"}
            if not blocker:
                errors.append(f"{label}: CHAIN_HANDOVER_READY FALSE requires an explicit validation/sync blocker")

    if field(text, "WORK_ITEM_SOURCE") == "GITHUB_ISSUE" and cmd == "PROCEED_NEXT_HANDOVER_READY" and chain_ready == "TRUE":
        if field(text, "ISSUE_HANDOVER_SYNC_STATUS") != "IN_SYNC":
            errors.append(f"{label}: issue hand-over-ready checkpoint requires ISSUE_HANDOVER_SYNC_STATUS IN_SYNC")

    return errors, True


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_progression_command.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2
    supplied = Path(sys.argv[1]).resolve()
    if supplied.name == "chains":
        chains = supplied
        root = supplied.parent.parent
    else:
        root = supplied
        chains = root / "agents" / "chains"
    if not chains.is_dir():
        print(f"FAIL: canonical chain store not found: {chains}")
        return 1

    errors = []
    checked = grandfathered = 0
    for d in sorted(p for p in chains.iterdir() if p.is_dir()):
        ap = d / "ACTIVE.md"
        if not ap.is_file():
            continue
        at = ap.read_text(encoding="utf-8")
        if field(at, "CHAIN_STATE_VERSION") != "3":
            continue
        chain = field(at, "CHAIN_ID") or d.name
        e, adopted = validate(f"{chain} ACTIVE", at)
        if not adopted:
            grandfathered += 1
            continue
        checked += 1
        errors.extend(e)
        ep_rel = field(at, "ACTIVE_ENDPOINT_FILE")
        ep = root / ep_rel if ep_rel else None
        if not ep or not ep.is_file():
            errors.append(f"{chain}: active endpoint missing for progression validation")
            continue
        et = ep.read_text(encoding="utf-8")
        ee, ep_adopted = validate(f"{chain} endpoint", et)
        if not ep_adopted:
            errors.append(f"{chain}: ACTIVE adopted progression command protocol but endpoint did not")
        else:
            errors.extend(ee)
            for name in (
                "OWNER_PROGRESSION_COMMAND", "QUALIFICATION_SCOPE_ID", "QUESTION_SET_ID",
                "QUESTION_SET_STATUS", "QUESTION_PACK_ACTION", "QUESTION_DISPLAY",
                "CHAIN_HANDOVER_READY", "TAKEOVER_QUALIFICATION_READY",
            ):
                if field(at, name) != field(et, name):
                    errors.append(f"{chain}: ACTIVE/endpoint {name} mismatch")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: three-command progression semantics ({checked} adopted chain(s); {grandfathered} historical chain(s) grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
