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
LEGACY_LOCATOR = re.compile(r"^git-blob:([0-9a-fA-F]{40})#(EP-[A-Za-z0-9_.-]+)$")


def field_value(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)
    return m.group(1).strip() if m else None


def has_section(text: str, title: str) -> bool:
    return bool(re.search(rf"(?mi)^###\s+{re.escape(title)}\s*$", text))


def section_body(text: str, title: str):
    m = re.search(
        rf"(?mis)^###\s+{re.escape(title)}\s*$\n(.*?)(?=^###\s+|\Z)",
        text,
    )
    return m.group(1).strip() if m else None


def table_rows(text: str, heading: str):
    m = re.search(
        rf"(?mis)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
    )
    if not m:
        return None

    rows = []
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    return rows


def normal_locator(locator: str) -> bool:
    return not bool(LEGACY_LOCATOR.fullmatch(locator or ""))


def validate_endpoint_content(text: str, expected: dict, prior_endpoint: str | None):
    errors = []
    eid = expected["endpoint"]
    prefix = f"{eid}:"

    for name in REQUIRED_FIELDS:
        if not field_value(text, name):
            errors.append(f"{prefix} missing field {name}")

    comparisons = {
        "CHAIN_ID": expected["chain"],
        "LEG_ID": expected["leg"],
        "ENDPOINT_ID": eid,
        "CHECKPOINT_HEAD": expected["head"],
        "STATE": expected["state"],
    }
    for name, wanted in comparisons.items():
        actual = field_value(text, name)
        if actual and actual != wanted:
            errors.append(f"{prefix} {name} mismatch: index={wanted} endpoint={actual}")

    previous = field_value(text, "PREVIOUS_ENDPOINT")
    if prior_endpoint is None:
        if previous and not previous.upper().startswith("NONE"):
            errors.append(
                f"{prefix} first endpoint for chain {expected['chain']} must use PREVIOUS_ENDPOINT NONE, found {previous}"
            )
    else:
        previous_id = previous.split()[0] if previous else None
        if previous_id != prior_endpoint:
            errors.append(
                f"{prefix} PREVIOUS_ENDPOINT must be chain-local prior endpoint {prior_endpoint}, found {previous}"
            )

    for title in REQUIRED_SECTIONS:
        if not has_section(text, title):
            errors.append(f"{prefix} missing section: {title}")

    for title in REQUIRED_INVENTORIES:
        body = section_body(text, title)
        if body is not None and not body.strip():
            errors.append(
                f"{prefix} empty inventory {title}; use explicit NONE/UNRESOLVED with reason"
            )

    state = expected["state"]
    if state == "COMPLETE":
        if "NEXT_AGENT_QUALIFICATION: NOT_REQUIRED" not in text:
            errors.append(
                f"{prefix} COMPLETE requires NEXT_AGENT_QUALIFICATION: NOT_REQUIRED"
            )
        if not field_value(text, "COMPLETION_BASIS"):
            errors.append(f"{prefix} COMPLETE requires COMPLETION_BASIS")
    elif state == "SUPERSEDED":
        # A superseded chain endpoint may still retain its historical question set.
        pass
    else:
        if not field_value(text, "QUALIFICATION_BASIS_HEAD"):
            errors.append(f"{prefix} missing QUALIFICATION_BASIS_HEAD")
        if not field_value(text, "QUESTION_SET_ID"):
            errors.append(f"{prefix} missing QUESTION_SET_ID")
        qstatus = field_value(text, "QUESTION_SET_STATUS")
        if qstatus not in {"CURRENT", "STALE"}:
            errors.append(
                f"{prefix} QUESTION_SET_STATUS must be CURRENT or STALE for non-terminal endpoint"
            )

        qmatches = re.findall(r"(?mi)^####\s+Q([1-5])\s+—\s+(.+?)\s*$", text)
        if len(qmatches) != 5:
            errors.append(
                f"{prefix} expected exactly five Q1-Q5 headings, found {len(qmatches)}"
            )
        else:
            nums = [int(n) for n, _ in qmatches]
            if nums != [1, 2, 3, 4, 5]:
                errors.append(f"{prefix} question order/numbering must be Q1..Q5")
            for n, title in qmatches:
                expected_title = QUESTION_TITLES[int(n)]
                if title.strip().lower() != expected_title.lower():
                    errors.append(
                        f"{prefix} Q{n} title must be '{expected_title}', found '{title.strip()}'"
                    )

    return errors


def resolve_endpoint_path(repo_root: Path, locator: str):
    rel = Path(locator)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    if not locator.startswith("agents/agentchain/") or not locator.endswith(".md"):
        return None
    return repo_root / rel


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agentchain.py <agents/agentchain.md>", file=sys.stderr)
        return 2

    index_path = Path(sys.argv[1]).resolve()
    text = index_path.read_text(encoding="utf-8")
    repo_root = index_path.parent.parent
    errors = []

    if not re.search(r"(?mi)^AGENTCHAIN_VERSION\s*:\s*\S+", text):
        errors.append("missing AGENTCHAIN_VERSION")

    active_rows = table_rows(text, "ACTIVE CHAINS")
    log_rows = table_rows(text, "ENDPOINT LOG")
    if active_rows is None:
        errors.append("missing ACTIVE CHAINS table")
        active_rows = []
    if log_rows is None:
        errors.append("missing ENDPOINT LOG table")
        log_rows = []

    # Drop table header rows.
    active_rows = [r for r in active_rows if r and r[0].lower() != "chain"]
    log_rows = [r for r in log_rows if r and r[0].lower() != "endpoint"]

    endpoints = []
    endpoint_by_id = {}
    latest_by_chain = {}
    prior_by_endpoint = {}

    for cells in log_rows:
        if len(cells) != 6:
            errors.append(f"ENDPOINT LOG row must have 6 columns: {' | '.join(cells)}")
            continue
        eid, chain, leg, head, state, locator = cells
        if eid in endpoint_by_id:
            errors.append(f"duplicate endpoint id in ENDPOINT LOG: {eid}")
            continue
        if not re.fullmatch(r"EP-[A-Za-z0-9_.-]+", eid):
            errors.append(f"invalid endpoint id in ENDPOINT LOG: {eid}")
        if state not in VALID_STATES:
            errors.append(f"{eid}: invalid STATE {state}")

        prior = latest_by_chain.get(chain)
        prior_by_endpoint[eid] = prior
        meta = {
            "endpoint": eid,
            "chain": chain,
            "leg": leg,
            "head": head,
            "state": state,
            "locator": locator,
        }
        endpoints.append(meta)
        endpoint_by_id[eid] = meta
        latest_by_chain[chain] = eid

        legacy = LEGACY_LOCATOR.fullmatch(locator)
        if legacy:
            if legacy.group(2) != eid:
                errors.append(
                    f"{eid}: legacy locator fragment {legacy.group(2)} does not match endpoint id"
                )
            continue

        endpoint_path = resolve_endpoint_path(repo_root, locator)
        if endpoint_path is None:
            errors.append(
                f"{eid}: locator must be agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md or controlled git-blob legacy locator: {locator}"
            )
            continue
        expected_suffix = Path("agents") / "agentchain" / chain / f"{eid}.md"
        if Path(locator) != expected_suffix:
            errors.append(
                f"{eid}: endpoint locator must be {expected_suffix.as_posix()}, found {locator}"
            )
        if not endpoint_path.is_file():
            errors.append(f"{eid}: endpoint file missing: {locator}")
            continue

        endpoint_text = endpoint_path.read_text(encoding="utf-8")
        errors.extend(
            validate_endpoint_content(endpoint_text, meta, prior_by_endpoint[eid])
        )

    active_by_chain = {}
    for cells in active_rows:
        if len(cells) != 8:
            errors.append(f"ACTIVE CHAINS row must have 8 columns: {' | '.join(cells)}")
            continue
        chain, _mission, latest_endpoint, endpoint_file, _pr, state, _domain, _next = cells
        if chain in active_by_chain:
            errors.append(f"duplicate ACTIVE CHAINS row for {chain}")
            continue
        active_by_chain[chain] = latest_endpoint

        meta = endpoint_by_id.get(latest_endpoint)
        if not meta:
            errors.append(
                f"ACTIVE CHAINS {chain} points to missing ENDPOINT LOG id {latest_endpoint}"
            )
            continue
        if meta["chain"] != chain:
            errors.append(
                f"ACTIVE CHAINS {chain} points to {latest_endpoint}, which belongs to {meta['chain']}"
            )
        expected_latest = latest_by_chain.get(chain)
        if expected_latest != latest_endpoint:
            errors.append(
                f"ACTIVE CHAINS {chain} is stale: points to {latest_endpoint}, latest logged endpoint is {expected_latest}"
            )
        if state != meta["state"]:
            errors.append(
                f"ACTIVE CHAINS {chain} state {state} disagrees with {latest_endpoint} state {meta['state']}"
            )
        if meta["state"] in TERMINAL_STATES:
            errors.append(
                f"ACTIVE CHAINS {chain} points to terminal endpoint {latest_endpoint} ({meta['state']})"
            )
        if LEGACY_LOCATOR.fullmatch(meta["locator"]):
            errors.append(
                f"ACTIVE CHAINS {chain} may not use historical legacy locator {meta['locator']}"
            )
        if endpoint_file != meta["locator"]:
            errors.append(
                f"ACTIVE CHAINS {chain} endpoint file {endpoint_file} disagrees with ENDPOINT LOG locator {meta['locator']}"
            )

    for chain, latest_endpoint in latest_by_chain.items():
        state = endpoint_by_id[latest_endpoint]["state"]
        if state not in TERMINAL_STATES and chain not in active_by_chain:
            errors.append(
                f"non-terminal chain {chain} latest endpoint {latest_endpoint} is missing from ACTIVE CHAINS"
            )
        if state in TERMINAL_STATES and chain in active_by_chain:
            errors.append(
                f"terminal chain {chain} must not remain in ACTIVE CHAINS"
            )

    # Detect durable endpoint files that were created but never indexed. This is
    # the crash-between-endpoint-and-index-update condition and must not be silent.
    logged_normal = {
        meta["locator"] for meta in endpoints if normal_locator(meta["locator"])
    }
    endpoint_root = repo_root / "agents" / "agentchain"
    if endpoint_root.is_dir():
        for endpoint_file in endpoint_root.rglob("*.md"):
            rel = endpoint_file.relative_to(repo_root).as_posix()
            if rel not in logged_normal:
                errors.append(
                    f"orphan endpoint file is not present in ENDPOINT LOG: {rel}"
                )

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print(
        f"PASS: split agentchain relay ({len(endpoints)} logged endpoints, {len(active_by_chain)} active chains)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
