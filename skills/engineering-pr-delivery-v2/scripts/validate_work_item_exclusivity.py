#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import uuid

TERMINAL = {"COMPLETE", "SUPERSEDED", "ABANDONED", "CLOSED"}


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip() if m else None


def valid_instance(value):
    if not value or ":" not in value:
        return False
    agent_class, raw = value.split(":", 1)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9._-]*", agent_class):
        return False
    try:
        parsed = uuid.UUID(raw)
    except (ValueError, AttributeError):
        return False
    return str(parsed) == raw.lower()


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_work_item_exclusivity.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2
    supplied = Path(sys.argv[1]).resolve()
    chains = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
    if not chains.is_dir():
        print(f"FAIL: canonical chain store not found: {chains}")
        return 1

    rows = []
    errors = []
    grandfathered = 0
    for chain_dir in sorted(p for p in chains.iterdir() if p.is_dir()):
        active = chain_dir / "ACTIVE.md"
        if not active.is_file():
            continue
        text = active.read_text(encoding="utf-8")
        if field(text, "CHAIN_STATE_VERSION") != "3":
            continue
        state = field(text, "STATE") or "UNKNOWN"
        if state in TERMINAL:
            continue
        chain = field(text, "CHAIN_ID") or chain_dir.name
        key = field(text, "WORK_ITEM_KEY")
        mode = field(text, "WORK_ITEM_MODE")
        instance = field(text, "AGENT_INSTANCE_ID")
        partition = field(text, "WORK_ITEM_PARTITION")
        authority = field(text, "WORK_ITEM_PARTITION_AUTHORITY")

        if not any((key, mode, instance, partition, authority)):
            grandfathered += 1
            continue
        if not key:
            errors.append(f"{chain}: WORK_ITEM_KEY missing")
        if mode not in {"EXCLUSIVE", "PARTITIONED"}:
            errors.append(f"{chain}: WORK_ITEM_MODE must be EXCLUSIVE or PARTITIONED; found {mode}")
        if not valid_instance(instance):
            errors.append(f"{chain}: AGENT_INSTANCE_ID must be <agent-class>:<UUID>; model/family labels are not unique instances")
        if mode == "PARTITIONED":
            if not partition or partition.upper() in {"NONE", "N/A"}:
                errors.append(f"{chain}: PARTITIONED work item requires WORK_ITEM_PARTITION")
            if not authority or not authority.startswith("OWNER:"):
                errors.append(f"{chain}: PARTITIONED work item requires WORK_ITEM_PARTITION_AUTHORITY: OWNER:<locator>")
        rows.append({"chain": chain, "key": key, "mode": mode, "partition": partition})

    by_key = {}
    for row in rows:
        if not row["key"]:
            continue
        by_key.setdefault(row["key"], []).append(row)

    for key, group in sorted(by_key.items()):
        if len(group) < 2:
            continue
        if any(row["mode"] == "EXCLUSIVE" for row in group):
            errors.append(
                f"work item {key}: multiple non-terminal claims include EXCLUSIVE custody: "
                + ", ".join(row["chain"] for row in group)
            )
            continue
        seen = {}
        for row in group:
            part = row["partition"]
            if part in seen:
                errors.append(f"work item {key}: duplicate PARTITIONED scope {part}: {seen[part]} and {row['chain']}")
            else:
                seen[part] = row["chain"]

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print(f"PASS: exact work-item custody ({len(rows)} adopted active chain(s); {grandfathered} historical active chain(s) grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
