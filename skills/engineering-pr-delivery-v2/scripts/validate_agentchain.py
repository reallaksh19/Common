#!/usr/bin/env python3
from pathlib import Path
import re
import sys

REQUIRED_FIELDS = [
    "CHAIN_ID",
    "LEG_ID",
    "ENDPOINT_ID",
    "PREVIOUS_ENDPOINT",
    "ENDPOINT_REASON",
    "CHECKPOINT_HEAD",
    "MAIN_HEAD_OBSERVED",
    "STATE",
]

REQUIRED_SECTIONS = [
    "Mission",
    "This leg completed",
    "Currently in progress",
    "Remaining work",
    "Exact next action",
    "Known / proven",
    "Not proven",
    "NOT_RUN",
    "Active hypothesis",
    "Falsifier",
    "Protected invariants",
    "Do not redo",
    "Do not change",
    "Expected next-leg files / domains",
    "Inputs",
    "Benchmarks",
    "Common / governing documents",
    "Authoritative sources",
    "Production paths",
    "Validation / test paths",
    "Changed during this leg",
    "Validation summary",
    "Open risks / questions",
    "Next-agent qualification",
]

REQUIRED_INVENTORIES = [
    "Inputs",
    "Benchmarks",
    "Common / governing documents",
    "Authoritative sources",
    "Production paths",
    "Validation / test paths",
]

QUESTION_TITLES = {
    1: "Production Trace",
    2: "Current Unresolved Problem / Failure Isolation",
    3: "Authority / Invariant",
    4: "Independent Validation",
    5: "Next Contribution / Minimal Patch",
}

VALID_STATES = {
    "ACTIVE",
    "QUALIFICATION_REQUIRED",
    "RECOVERY_REQUIRED",
    "BLOCKED",
    "READY_FOR_NEXT_LEG",
    "COMPLETE",
    "SUPERSEDED",
}

TERMINAL_STATES = {"COMPLETE", "SUPERSEDED"}


def field_value(block: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", block)
    return m.group(1).strip() if m else None


def has_section(block: str, title: str) -> bool:
    return bool(re.search(rf"(?mi)^###\s+{re.escape(title)}\s*$", block))


def section_body(block: str, title: str):
    m = re.search(
        rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|^##\s+EP-|\Z)",
        block,
    )
    return m.group(1).strip() if m else None


def parse_active_rows(text: str):
    m = re.search(
        r"(?mis)^##\s+ACTIVE CHAINS\s*$\n(.*?)(?=^#\s+ENDPOINTS\s*$|\Z)",
        text,
    )
    if not m:
        return []

    rows = []
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        if cells[0].lower() == "chain":
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    return rows


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agentchain.py <agents/agentchain.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors = []

    if not re.search(r"(?mi)^AGENTCHAIN_VERSION\s*:\s*\S+", text):
        errors.append("missing AGENTCHAIN_VERSION")
    if not re.search(r"(?mi)^##\s+ACTIVE CHAINS\s*$", text):
        errors.append("missing ACTIVE CHAINS index")

    matches = list(re.finditer(r"(?m)^##\s+(EP-[A-Za-z0-9_.-]+)\s*$", text))
    if not matches:
        errors.append("no endpoint records found")

    endpoints = []
    ids = set()
    for i, match in enumerate(matches):
        eid = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        endpoints.append((eid, block))
        if eid in ids:
            errors.append(f"duplicate endpoint id: {eid}")
        ids.add(eid)

    endpoint_meta = {}
    latest_by_chain = {}

    for eid, block in endpoints:
        prefix = f"{eid}:"
        for name in REQUIRED_FIELDS:
            value = field_value(block, name)
            if not value:
                errors.append(f"{prefix} missing field {name}")

        declared = field_value(block, "ENDPOINT_ID")
        if declared and declared != eid:
            errors.append(f"{prefix} ENDPOINT_ID field is {declared}")

        chain_id = field_value(block, "CHAIN_ID")
        state = field_value(block, "STATE")
        if state and state not in VALID_STATES:
            errors.append(f"{prefix} invalid STATE {state}")

        previous = field_value(block, "PREVIOUS_ENDPOINT")
        prior_for_chain = latest_by_chain.get(chain_id) if chain_id else None
        if previous:
            if previous.upper().startswith("NONE"):
                if prior_for_chain:
                    errors.append(
                        f"{prefix} PREVIOUS_ENDPOINT cannot be NONE; prior endpoint for {chain_id} is {prior_for_chain}"
                    )
            else:
                previous_id = previous.split()[0]
                if not prior_for_chain:
                    errors.append(
                        f"{prefix} PREVIOUS_ENDPOINT {previous_id} supplied but this is the first ledger endpoint for chain {chain_id}"
                    )
                elif previous_id != prior_for_chain:
                    errors.append(
                        f"{prefix} PREVIOUS_ENDPOINT must be latest prior endpoint {prior_for_chain} for chain {chain_id}, found {previous_id}"
                    )

        for title in REQUIRED_SECTIONS:
            if not has_section(block, title):
                errors.append(f"{prefix} missing section: {title}")

        for title in REQUIRED_INVENTORIES:
            body = section_body(block, title)
            if body is not None and not body.strip():
                errors.append(
                    f"{prefix} empty inventory {title}; use explicit NONE/UNRESOLVED with reason"
                )

        if state == "COMPLETE":
            if "NEXT_AGENT_QUALIFICATION: NOT_REQUIRED" not in block:
                errors.append(
                    f"{prefix} COMPLETE requires NEXT_AGENT_QUALIFICATION: NOT_REQUIRED"
                )
            if not field_value(block, "COMPLETION_BASIS"):
                errors.append(f"{prefix} COMPLETE requires COMPLETION_BASIS")
        else:
            basis = field_value(block, "QUALIFICATION_BASIS_HEAD")
            qsid = field_value(block, "QUESTION_SET_ID")
            qstatus = field_value(block, "QUESTION_SET_STATUS")
            if not basis:
                errors.append(f"{prefix} missing QUALIFICATION_BASIS_HEAD")
            if not qsid:
                errors.append(f"{prefix} missing QUESTION_SET_ID")
            if qstatus not in {"CURRENT", "STALE"}:
                errors.append(
                    f"{prefix} QUESTION_SET_STATUS must be CURRENT or STALE for non-terminal endpoint"
                )

            qmatches = re.findall(r"(?mi)^####\s+Q([1-5])\s+—\s+(.+?)\s*$", block)
            if len(qmatches) != 5:
                errors.append(f"{prefix} expected exactly five Q1-Q5 headings, found {len(qmatches)}")
            else:
                nums = [int(n) for n, _ in qmatches]
                if nums != [1, 2, 3, 4, 5]:
                    errors.append(f"{prefix} question order/numbering must be Q1..Q5")
                for n, title in qmatches:
                    expected = QUESTION_TITLES[int(n)]
                    if title.strip().lower() != expected.lower():
                        errors.append(
                            f"{prefix} Q{n} title must be '{expected}', found '{title.strip()}'"
                        )

        if chain_id:
            latest_by_chain[chain_id] = eid
        endpoint_meta[eid] = {"chain": chain_id, "state": state}

    active_rows = parse_active_rows(text)
    active_by_chain = {}
    for cells in active_rows:
        if len(cells) < 5:
            errors.append(f"ACTIVE CHAINS row has too few columns: {' | '.join(cells)}")
            continue
        chain_id, latest_endpoint, row_state = cells[0], cells[2], cells[4]
        if chain_id in active_by_chain:
            errors.append(f"duplicate ACTIVE CHAINS row for {chain_id}")
            continue
        active_by_chain[chain_id] = latest_endpoint

        meta = endpoint_meta.get(latest_endpoint)
        if not meta:
            errors.append(
                f"ACTIVE CHAINS {chain_id} points to missing endpoint {latest_endpoint}"
            )
            continue
        if meta["chain"] != chain_id:
            errors.append(
                f"ACTIVE CHAINS {chain_id} points to {latest_endpoint}, which belongs to {meta['chain']}"
            )
        expected_latest = latest_by_chain.get(chain_id)
        if expected_latest and latest_endpoint != expected_latest:
            errors.append(
                f"ACTIVE CHAINS {chain_id} is stale: points to {latest_endpoint}, latest ledger endpoint is {expected_latest}"
            )
        if row_state != meta["state"]:
            errors.append(
                f"ACTIVE CHAINS {chain_id} state {row_state} disagrees with {latest_endpoint} state {meta['state']}"
            )
        if meta["state"] in TERMINAL_STATES:
            errors.append(
                f"ACTIVE CHAINS {chain_id} points to terminal endpoint {latest_endpoint} ({meta['state']})"
            )

    for chain_id, latest_endpoint in latest_by_chain.items():
        state = endpoint_meta[latest_endpoint]["state"]
        if state not in TERMINAL_STATES and chain_id not in active_by_chain:
            errors.append(
                f"non-terminal chain {chain_id} latest endpoint {latest_endpoint} is missing from ACTIVE CHAINS"
            )

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print(
        f"PASS: agentchain relay structure ({len(endpoints)} endpoints, {len(active_by_chain)} active chains)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
