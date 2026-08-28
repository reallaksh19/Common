#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import sys

V3_ACTIVE_FIELDS = [
    "CHAIN_STATE_VERSION", "CHAIN_ID", "MISSION", "ACTIVE_ENDPOINT",
    "ACTIVE_ENDPOINT_FILE", "PR", "BRANCH", "HEAD", "STATE",
    "ENGINEERING_STATE", "CUSTODY_STATE", "QUALIFICATION_STATE",
    "WRITE_AUTHORITY", "AUTO_STATE", "MERGE_AUTHORITY", "AUTHORITY_DOMAIN",
    "ACTIVE_CUSTODIAN", "CUSTODY_EPOCH", "COORDINATION_STATE",
    "DEPENDENCIES", "ROADMAPS", "ROADMAP_REVIEW_STATUS", "HANDOVER_READY",
]
SNAPSHOT_LABELS = [
    "Repo:", "Task:", "Chain:", "Endpoint:", "PR:", "PR status:",
    "Merge authority:", "Roadmap:", "Inputs:", "Benchmarks:",
    "Governing docs / authoritative sources:", "Exact next action:",
]
VALID_ENGINEERING = {"READY", "IN_PROGRESS", "BLOCKED", "COMPLETE"}
VALID_CUSTODY = {"HELD", "VACANT", "TAKEOVER_REQUIRED", "QUALIFIED_PENDING_RECONCILIATION", "RECONCILING"}
VALID_QUAL = {"NOT_REQUIRED", "PENDING", "PASS", "FAIL", "DEFERRED", "REQUALIFICATION_REQUIRED"}
VALID_WRITE = {"READ_ONLY", "WRITE_ALLOWED", "BLOCKED"}
VALID_AUTO = {"RUNNING", "PAUSED", "BLOCKED", "NOT_APPLICABLE"}
VALID_MERGE = {"OWNER_ONLY", "AUTHORIZED"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip() if m else None


def section(text, title):
    m = re.search(rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|\Z)", text)
    return m.group(1).strip() if m else None


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def roadmap_errors(root, chain, active):
    errors = []
    value = field(active, "ROADMAPS")
    status = field(active, "ROADMAP_REVIEW_STATUS")
    if not value:
        return [f"{chain}: missing ROADMAPS"]
    if value.upper().startswith("NONE"):
        if status != "NOT_APPLICABLE":
            errors.append(f"{chain}: ROADMAPS NONE requires NOT_APPLICABLE")
        return errors
    if status not in {"COMPLETE", "BLOCKED"}:
        errors.append(f"{chain}: bound roadmap requires COMPLETE or BLOCKED")
        return errors
    for item in value.split(";"):
        item = item.strip()
        if "@" not in item:
            errors.append(f"{chain}: roadmap binding lacks @blob: {item}")
            continue
        rel, expected = item.rsplit("@", 1)
        expected = expected.strip().lower()
        if not re.fullmatch(r"[0-9a-f]{40}", expected):
            errors.append(f"{chain}: invalid roadmap blob in {item}")
            continue
        p = root / rel.strip()
        if not p.is_file():
            errors.append(f"{chain}: roadmap missing {rel.strip()}")
        elif git_blob_sha(p) != expected:
            errors.append(f"{chain}: stale roadmap binding {rel.strip()}")
    return errors


def validate_chain(root, chain_dir):
    errors = []
    active_path = chain_dir / "ACTIVE.md"
    if not active_path.is_file():
        return errors
    active = active_path.read_text(encoding="utf-8")
    if field(active, "CHAIN_STATE_VERSION") != "3":
        return errors
    chain = field(active, "CHAIN_ID") or chain_dir.name
    for name in V3_ACTIVE_FIELDS:
        if not field(active, name):
            errors.append(f"{chain}: ACTIVE.md missing {name}")
    if errors:
        return errors
    enums = [
        ("ENGINEERING_STATE", VALID_ENGINEERING), ("CUSTODY_STATE", VALID_CUSTODY),
        ("QUALIFICATION_STATE", VALID_QUAL), ("WRITE_AUTHORITY", VALID_WRITE),
        ("AUTO_STATE", VALID_AUTO), ("MERGE_AUTHORITY", VALID_MERGE),
    ]
    for name, allowed in enums:
        if field(active, name) not in allowed:
            errors.append(f"{chain}: invalid {name}={field(active, name)}")
    custody = field(active, "CUSTODY_STATE")
    qual = field(active, "QUALIFICATION_STATE")
    write = field(active, "WRITE_AUTHORITY")
    auto = field(active, "AUTO_STATE")
    if custody in {"VACANT", "TAKEOVER_REQUIRED", "QUALIFIED_PENDING_RECONCILIATION", "RECONCILING"} and write == "WRITE_ALLOWED":
        errors.append(f"{chain}: {custody} cannot have WRITE_ALLOWED")
    if qual in {"PENDING", "FAIL", "DEFERRED", "REQUALIFICATION_REQUIRED"} and write == "WRITE_ALLOWED":
        errors.append(f"{chain}: {qual} qualification cannot have WRITE_ALLOWED")
    if write == "WRITE_ALLOWED" and custody != "HELD":
        errors.append(f"{chain}: WRITE_ALLOWED requires CUSTODY_STATE HELD")
    if custody in {"VACANT", "TAKEOVER_REQUIRED"} and auto == "RUNNING":
        errors.append(f"{chain}: agent-loss/takeover state cannot leave AUTO RUNNING")
    if field(active, "HANDOVER_READY") != "TRUE":
        errors.append(f"{chain}: HANDOVER_READY must be TRUE")
    endpoint_rel = field(active, "ACTIVE_ENDPOINT_FILE")
    ep = root / endpoint_rel
    if not ep.is_file():
        errors.append(f"{chain}: active endpoint missing {endpoint_rel}")
        return errors
    text = ep.read_text(encoding="utf-8")
    snap = section(text, "Handover snapshot")
    if snap is None:
        errors.append(f"{chain}: active endpoint missing Handover snapshot")
    else:
        words = len(re.findall(r"\S+", snap))
        if words >= 300:
            errors.append(f"{chain}: Handover snapshot must be <300 words, found {words}")
        for label in SNAPSHOT_LABELS:
            if label.lower() not in snap.lower():
                errors.append(f"{chain}: Handover snapshot missing {label}")
        for q in range(1, 6):
            if not re.search(rf"(?mi)^Q{q}\s*:", snap):
                errors.append(f"{chain}: Handover snapshot missing Q{q}")
    if field(text, "HANDOVER_READY") != "TRUE":
        errors.append(f"{chain}: endpoint HANDOVER_READY must be TRUE")
    errors.extend(roadmap_errors(root, chain, active))
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_handover_snapshot.py <repo-root-or-agents/chains>", file=sys.stderr)
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
    checked = 0
    for d in sorted(p for p in chains.iterdir() if p.is_dir()):
        active = d / "ACTIVE.md"
        if active.is_file() and field(active.read_text(encoding="utf-8"), "CHAIN_STATE_VERSION") == "3":
            checked += 1
            errors.extend(validate_chain(root, d))
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: version-3 handover snapshots/state ({checked} chain(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
