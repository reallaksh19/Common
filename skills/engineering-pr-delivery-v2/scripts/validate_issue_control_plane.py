#!/usr/bin/env python3
from pathlib import Path
import re
import sys

REQUIRED_BASIS_SECTIONS = [
    "Original task / acceptance ledger",
    "Input ledger",
    "Benchmark / oracle ledger",
    "Roadmap ledger",
    "Owner qualification baseline",
]
REQUIRED_STATE_SECTIONS = REQUIRED_BASIS_SECTIONS
ROW_PATTERNS = {
    "TASK": r"(?m)^\s*(TASK-[A-Za-z0-9_.-]+)\b",
    "INPUT": r"(?m)^\s*(INPUT-[A-Za-z0-9_.-]+)\b",
    "BM": r"(?m)^\s*(BM-[A-Za-z0-9_.-]+)\b",
    "RM": r"(?m)^\s*(RM-[A-Za-z0-9_.-]+)\b",
}
PROGRAM_CHILD_FIELDS = [
    "PROGRAM_ID", "PROGRAM_WORK_ITEM_KEY", "ISSUE_ROLE", "WORK_PACKAGE_ID", "PARTITION_KEY",
    "PREDECESSOR_WORK_ITEM_KEY", "REVISION_SEQUENCE", "INHERITED_PROGRAM_BASIS_REVISION",
    "INHERITED_INPUT_SET_ID", "INHERITED_BENCHMARK_SET_ID", "INHERITED_VALIDATION_SET_ID",
    "INHERITED_ROADMAP_SET_ID", "PARENT_TASK_ROWS", "USES_INPUT_ROWS", "USES_BENCHMARK_ROWS",
    "USES_VALIDATION_ROWS", "PROGRAM_OVERLAP_CLASSIFICATION",
]
OVERLAP = {"SAFE_DISJOINT", "SAFE_SERIALIZED", "COORDINATION_REQUIRED", "BLOCKED_ACTIVE_SIBLING", "UNKNOWN"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip() if m else None


def has_section(text, title):
    return bool(re.search(rf"(?mi)^###\s+{re.escape(title)}\s*$", text or ""))


def comment_id_ok(value):
    return bool(value and re.fullmatch(r"[1-9][0-9]*", value))


def row_ids(text, kind):
    return set(re.findall(ROW_PATTERNS[kind], text or ""))


def validate_program_child(chain, at, basis_text, errors):
    role = field(at, "ISSUE_ROLE") or field(basis_text, "ISSUE_ROLE")
    if role not in {"WORK_PACKAGE", "REVISION"}:
        return
    for name in PROGRAM_CHILD_FIELDS:
        av = field(at, name)
        bv = field(basis_text, name)
        if not av:
            errors.append(f"{chain}: program child ACTIVE missing {name}")
        if not bv:
            errors.append(f"{chain}: program child Issue Basis missing {name}")
        if av and bv and av != bv:
            errors.append(f"{chain}: program child {name} mismatch ACTIVE={av} basis={bv}")

    parent = field(at, "PROGRAM_WORK_ITEM_KEY")
    if parent and not re.fullmatch(r"github:[^/\s]+/[^#\s]+#[1-9][0-9]*", parent):
        errors.append(f"{chain}: invalid PROGRAM_WORK_ITEM_KEY {parent}")

    overlap = field(at, "PROGRAM_OVERLAP_CLASSIFICATION")
    if overlap not in OVERLAP:
        errors.append(f"{chain}: invalid PROGRAM_OVERLAP_CLASSIFICATION={overlap}")
    write = field(at, "WRITE_AUTHORITY")
    auto = field(at, "AUTO_STATE")
    if overlap in {"COORDINATION_REQUIRED", "BLOCKED_ACTIVE_SIBLING", "UNKNOWN"}:
        if write == "WRITE_ALLOWED":
            errors.append(f"{chain}: overlap={overlap} cannot retain WRITE_ALLOWED")
        if auto == "RUNNING":
            errors.append(f"{chain}: overlap={overlap} cannot retain AUTO RUNNING")
    if overlap == "SAFE_SERIALIZED":
        evidence = field(at, "PROGRAM_SERIALIZATION_EVIDENCE")
        if write == "WRITE_ALLOWED" and (not evidence or evidence.upper() in {"NONE", "NOT_RUN", "UNKNOWN"}):
            errors.append(f"{chain}: SAFE_SERIALIZED WRITE_ALLOWED requires PROGRAM_SERIALIZATION_EVIDENCE")

    if role == "REVISION":
        pred = field(at, "PREDECESSOR_WORK_ITEM_KEY")
        seq = field(at, "REVISION_SEQUENCE")
        if not pred or pred == "NONE":
            errors.append(f"{chain}: REVISION requires PREDECESSOR_WORK_ITEM_KEY")
        if not seq or not seq.isdigit() or int(seq) <= 0:
            errors.append(f"{chain}: REVISION_SEQUENCE must be >0")


def validate_issue_chain(root: Path, chain_dir: Path):
    errors = []
    ap = chain_dir / "ACTIVE.md"
    if not ap.is_file():
        return errors
    at = ap.read_text(encoding="utf-8")
    if field(at, "CHAIN_STATE_VERSION") != "3" or field(at, "WORK_ITEM_SOURCE") != "GITHUB_ISSUE":
        return errors

    chain = field(at, "CHAIN_ID") or chain_dir.name
    key = field(at, "WORK_ITEM_KEY")
    if not key or not re.fullmatch(r"github:[^/\s]+/[^#\s]+#[1-9][0-9]*", key):
        errors.append(f"{chain}: invalid GitHub-Issue WORK_ITEM_KEY {key}")

    required = [
        "ISSUE_BASIS_ID", "ISSUE_BASIS_FILE", "ISSUE_BASIS_STATUS",
        "ISSUE_CURRENT_STATE_FILE", "ISSUE_CURRENT_STATE_BASIS",
        "ISSUE_CURRENT_STATE_ENDPOINT", "ISSUE_CHAIN_ROOT_COMMENT_ID",
        "ISSUE_ACTIVE_HANDOVER_COMMENT_ID", "ISSUE_LATEST_ENDPOINT_COMMENT_ID",
        "ISSUE_HANDOVER_SYNC_STATUS",
    ]
    for name in required:
        if not field(at, name):
            errors.append(f"{chain}: ACTIVE missing {name}")

    basis_id = field(at, "ISSUE_BASIS_ID")
    basis_rel = field(at, "ISSUE_BASIS_FILE")
    state_rel = field(at, "ISSUE_CURRENT_STATE_FILE")
    active_ep = field(at, "ACTIVE_ENDPOINT")
    sync = field(at, "ISSUE_HANDOVER_SYNC_STATUS")

    if field(at, "ISSUE_BASIS_STATUS") != "CURRENT":
        errors.append(f"{chain}: active Issue Basis must be CURRENT")
    if sync not in {"IN_SYNC", "STALE", "NOT_RUN", "FAILED"}:
        errors.append(f"{chain}: invalid ISSUE_HANDOVER_SYNC_STATUS={sync}")
    if field(at, "ISSUE_CURRENT_STATE_BASIS") != basis_id:
        errors.append(f"{chain}: ISSUE_CURRENT_STATE_BASIS must equal ISSUE_BASIS_ID")
    if active_ep and field(at, "ISSUE_CURRENT_STATE_ENDPOINT") != active_ep:
        errors.append(f"{chain}: ISSUE_CURRENT_STATE_ENDPOINT must equal ACTIVE_ENDPOINT")

    basis_path = root / basis_rel if basis_rel else None
    state_path = root / state_rel if state_rel else None
    if not basis_path or not basis_path.is_file():
        errors.append(f"{chain}: Issue Basis file missing: {basis_rel}")
        basis_text = ""
    else:
        basis_text = basis_path.read_text(encoding="utf-8")
        if field(basis_text, "ISSUE_BASIS_ID") != basis_id:
            errors.append(f"{chain}: Issue Basis ID mismatch")
        if field(basis_text, "WORK_ITEM_KEY") != key:
            errors.append(f"{chain}: Issue Basis WORK_ITEM_KEY mismatch")
        if field(basis_text, "ISSUE_BASIS_STATUS") != "CURRENT":
            errors.append(f"{chain}: referenced Issue Basis file must be CURRENT")
        for title in REQUIRED_BASIS_SECTIONS:
            if not has_section(basis_text, title):
                errors.append(f"{chain}: Issue Basis missing section {title}")

    if not state_path or not state_path.is_file():
        errors.append(f"{chain}: Issue Current State file missing: {state_rel}")
        state_text = ""
    else:
        state_text = state_path.read_text(encoding="utf-8")
        if field(state_text, "ISSUE_BASIS_ID") != basis_id:
            errors.append(f"{chain}: Issue Current State basis mismatch")
        if active_ep and field(state_text, "CURRENT_ENDPOINT") != active_ep:
            errors.append(f"{chain}: Issue Current State CURRENT_ENDPOINT must equal ACTIVE_ENDPOINT")
        for title in REQUIRED_STATE_SECTIONS:
            if not has_section(state_text, title):
                errors.append(f"{chain}: Issue Current State missing section {title}")

    if basis_text and state_text:
        for kind in ROW_PATTERNS:
            missing = sorted(row_ids(basis_text, kind) - row_ids(state_text, kind))
            if missing:
                errors.append(f"{chain}: {kind} rows diluted/missing from CURRENT.md: {missing}")

    validate_program_child(chain, at, basis_text, errors)

    ep_rel = field(at, "ACTIVE_ENDPOINT_FILE")
    ep_path = root / ep_rel if ep_rel else None
    ep_text = ep_path.read_text(encoding="utf-8") if ep_path and ep_path.is_file() else ""
    if not ep_text:
        errors.append(f"{chain}: active endpoint unavailable for Issue comment linkage")
    elif sync == "IN_SYNC":
        for name in ("ISSUE_CHAIN_ROOT_COMMENT_ID", "ISSUE_ACTIVE_HANDOVER_COMMENT_ID", "ISSUE_LATEST_ENDPOINT_COMMENT_ID"):
            if not comment_id_ok(field(at, name)):
                errors.append(f"{chain}: {name} must be a positive GitHub comment ID when IN_SYNC")
        ep_comment = field(ep_text, "ISSUE_ENDPOINT_COMMENT_ID")
        if not comment_id_ok(ep_comment):
            errors.append(f"{chain}: active endpoint missing positive ISSUE_ENDPOINT_COMMENT_ID when IN_SYNC")
        if ep_comment and field(at, "ISSUE_LATEST_ENDPOINT_COMMENT_ID") != ep_comment:
            errors.append(f"{chain}: latest Issue endpoint comment ID must match active endpoint")

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_issue_control_plane.py <repo-root-or-agents/chains>", file=sys.stderr)
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
        ap = d / "ACTIVE.md"
        if ap.is_file() and field(ap.read_text(encoding="utf-8"), "WORK_ITEM_SOURCE") == "GITHUB_ISSUE":
            checked += 1
            errors.extend(validate_issue_chain(root, d))
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: GitHub-Issue control-plane custody ({checked} issue chain(s))")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
