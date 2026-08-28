#!/usr/bin/env python3
from pathlib import Path
import re
import sys

from validate_agentchain import (
    TERMINAL_STATES,
    VALID_STATES,
    field_value,
    validate_endpoint_content,
)

ACTIVE_REQUIRED_FIELDS = [
    "CHAIN_STATE_VERSION",
    "CHAIN_ID",
    "MISSION",
    "ACTIVE_ENDPOINT",
    "ACTIVE_ENDPOINT_FILE",
    "PR",
    "BRANCH",
    "HEAD",
    "STATE",
    "AUTHORITY_DOMAIN",
    "ACTIVE_CUSTODIAN",
    "CUSTODY_EPOCH",
    "COORDINATION_STATE",
    "DEPENDENCIES",
]

VALID_COORDINATION_STATES = {
    "SAFE",
    "COORDINATION_REQUIRED",
    "BLOCKED_BY_ACTIVE_CHAIN",
    "UNKNOWN",
    "NOT_APPLICABLE",
}


def endpoint_key(chain_id: str, endpoint_id: str):
    return (chain_id, endpoint_id)


def positive_int(value: str | None):
    if value is None or not re.fullmatch(r"[1-9][0-9]*", value):
        return None
    return int(value)


def load_endpoint(path: Path):
    text = path.read_text(encoding="utf-8")
    return {
        "path": path,
        "text": text,
        "chain": field_value(text, "CHAIN_ID"),
        "leg": field_value(text, "LEG_ID"),
        "endpoint": field_value(text, "ENDPOINT_ID"),
        "previous": field_value(text, "PREVIOUS_ENDPOINT"),
        "head": field_value(text, "CHECKPOINT_HEAD"),
        "state": field_value(text, "STATE"),
        "epoch": positive_int(field_value(text, "CUSTODY_EPOCH")),
    }


def validate_chain_dir(chain_dir: Path):
    errors = []
    active_path = chain_dir / "ACTIVE.md"
    endpoints_dir = chain_dir / "endpoints"

    if not active_path.is_file():
        return [f"{chain_dir.name}: missing ACTIVE.md"]
    if not endpoints_dir.is_dir():
        return [f"{chain_dir.name}: missing endpoints/ directory"]

    active_text = active_path.read_text(encoding="utf-8")
    for name in ACTIVE_REQUIRED_FIELDS:
        if not field_value(active_text, name):
            errors.append(f"{chain_dir.name}: ACTIVE.md missing field {name}")

    chain_id = field_value(active_text, "CHAIN_ID")
    if chain_id and chain_id != chain_dir.name:
        errors.append(
            f"{chain_dir.name}: ACTIVE.md CHAIN_ID must match directory name, found {chain_id}"
        )

    active_endpoint = field_value(active_text, "ACTIVE_ENDPOINT")
    active_locator = field_value(active_text, "ACTIVE_ENDPOINT_FILE")
    active_state = field_value(active_text, "STATE")
    active_head = field_value(active_text, "HEAD")
    active_epoch = positive_int(field_value(active_text, "CUSTODY_EPOCH"))
    coordination = field_value(active_text, "COORDINATION_STATE")

    if active_state and active_state not in VALID_STATES:
        errors.append(f"{chain_dir.name}: ACTIVE.md invalid STATE {active_state}")
    if coordination and coordination not in VALID_COORDINATION_STATES:
        errors.append(
            f"{chain_dir.name}: ACTIVE.md invalid COORDINATION_STATE {coordination}"
        )
    if field_value(active_text, "CUSTODY_EPOCH") and active_epoch is None:
        errors.append(f"{chain_dir.name}: CUSTODY_EPOCH must be a positive integer")

    endpoint_paths = sorted(endpoints_dir.glob("*.md"))
    if not endpoint_paths:
        errors.append(f"{chain_dir.name}: endpoints/ contains no endpoint files")
        return errors

    endpoints = {}
    for path in endpoint_paths:
        data = load_endpoint(path)
        eid = data["endpoint"]
        if not eid:
            errors.append(f"{path}: missing ENDPOINT_ID")
            continue
        if path.stem != eid:
            errors.append(
                f"{path}: filename must equal ENDPOINT_ID ({eid}.md), found {path.name}"
            )
        if data["chain"] != chain_id:
            errors.append(
                f"{path}: CHAIN_ID mismatch: ACTIVE={chain_id}, endpoint={data['chain']}"
            )
        key = endpoint_key(chain_id or chain_dir.name, eid)
        if key in endpoints:
            errors.append(f"{chain_dir.name}: duplicate chain-local endpoint id {eid}")
            continue
        endpoints[key] = data

    by_id = {data["endpoint"]: data for data in endpoints.values() if data["endpoint"]}
    successors = {eid: [] for eid in by_id}
    roots = []

    for eid, data in by_id.items():
        prev = data["previous"]
        prev_id = prev.split()[0] if prev else None
        if prev and prev.upper().startswith("NONE"):
            roots.append(eid)
            prior = None
        else:
            prior = prev_id
            if not prior or prior not in by_id:
                errors.append(
                    f"{chain_dir.name}/{eid}: PREVIOUS_ENDPOINT must resolve within the same chain, found {prev}"
                )
            else:
                successors[prior].append(eid)

        expected = {
            "endpoint": eid,
            "chain": chain_id,
            "leg": data["leg"],
            "head": data["head"],
            "state": data["state"],
        }
        errors.extend(validate_endpoint_content(data["text"], expected, prior))

        if field_value(data["text"], "CUSTODY_EPOCH") and data["epoch"] is None:
            errors.append(f"{chain_dir.name}/{eid}: CUSTODY_EPOCH must be a positive integer")

    if len(roots) != 1:
        errors.append(
            f"{chain_dir.name}: expected exactly one chain root endpoint, found {len(roots)} ({roots})"
        )

    for eid, children in successors.items():
        if len(children) > 1:
            errors.append(
                f"{chain_dir.name}/{eid}: divergent successors {children}; reconcile custody instead of accepting parallel same-chain advancement"
            )

    # Detect cycles and validate custody epoch increments along the unique chain.
    if len(roots) == 1:
        seen = set()
        current = roots[0]
        expected_epoch = 1
        while current:
            if current in seen:
                errors.append(f"{chain_dir.name}: endpoint lineage cycle at {current}")
                break
            seen.add(current)
            data = by_id[current]
            if data["epoch"] != expected_epoch:
                errors.append(
                    f"{chain_dir.name}/{current}: CUSTODY_EPOCH expected {expected_epoch}, found {data['epoch']}"
                )
            children = successors.get(current, [])
            current = children[0] if len(children) == 1 else None
            expected_epoch += 1
        if len(seen) != len(by_id):
            unreachable = sorted(set(by_id) - seen)
            errors.append(f"{chain_dir.name}: unreachable/orphan endpoint lineage {unreachable}")

    if active_endpoint not in by_id:
        errors.append(
            f"{chain_dir.name}: ACTIVE_ENDPOINT {active_endpoint} does not resolve in endpoints/"
        )
    else:
        data = by_id[active_endpoint]
        expected_locator = f"agents/chains/{chain_id}/endpoints/{active_endpoint}.md"
        if active_locator != expected_locator:
            errors.append(
                f"{chain_dir.name}: ACTIVE_ENDPOINT_FILE must be {expected_locator}, found {active_locator}"
            )
        if active_state != data["state"]:
            errors.append(
                f"{chain_dir.name}: ACTIVE state {active_state} != endpoint state {data['state']}"
            )
        if active_head != data["head"]:
            errors.append(
                f"{chain_dir.name}: ACTIVE HEAD {active_head} != endpoint CHECKPOINT_HEAD {data['head']}"
            )
        if active_epoch != data["epoch"]:
            errors.append(
                f"{chain_dir.name}: ACTIVE CUSTODY_EPOCH {active_epoch} != endpoint epoch {data['epoch']}"
            )
        if successors.get(active_endpoint):
            errors.append(
                f"{chain_dir.name}: ACTIVE_ENDPOINT {active_endpoint} is stale; successor(s) exist: {successors[active_endpoint]}"
            )

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_chain_store.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2

    supplied = Path(sys.argv[1]).resolve()
    chains_dir = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
    if not chains_dir.is_dir():
        print(f"FAIL: canonical chain store not found: {chains_dir}", file=sys.stderr)
        return 1

    chain_dirs = sorted(p for p in chains_dir.iterdir() if p.is_dir())
    if not chain_dirs:
        print("PASS: canonical chain store exists; no chains present")
        return 0

    errors = []
    for chain_dir in chain_dirs:
        errors.extend(validate_chain_dir(chain_dir))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: canonical chain-local relay store ({len(chain_dirs)} chain(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
