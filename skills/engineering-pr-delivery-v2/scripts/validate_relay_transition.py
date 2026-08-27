#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ALLOWED = {
    "ACTIVE": {"ACTIVE", "QUALIFICATION_REQUIRED", "BLOCKED", "READY_FOR_NEXT_LEG", "COMPLETE", "RECOVERY_REQUIRED"},
    "QUALIFICATION_REQUIRED": {"QUALIFICATION_REQUIRED", "READY_FOR_NEXT_LEG", "BLOCKED", "RECOVERY_REQUIRED", "COMPLETE"},
    "READY_FOR_NEXT_LEG": {"ACTIVE", "QUALIFICATION_REQUIRED", "BLOCKED", "RECOVERY_REQUIRED", "COMPLETE"},
    "RECOVERY_REQUIRED": {"QUALIFICATION_REQUIRED", "ACTIVE", "BLOCKED", "READY_FOR_NEXT_LEG", "COMPLETE"},
    "BLOCKED": {"BLOCKED", "RECOVERY_REQUIRED", "QUALIFICATION_REQUIRED", "ACTIVE", "READY_FOR_NEXT_LEG", "COMPLETE"},
    "SUPERSEDED": set(),
    "COMPLETE": set(),
}


def field(text: str, name: str):
    vals = [v.strip() for v in re.findall(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)]
    return vals[0] if len(vals) == 1 else None


def load(path):
    text = Path(path).read_text(encoding="utf-8")
    return {
        "chain": field(text, "CHAIN_ID"),
        "endpoint": field(text, "ENDPOINT_ID"),
        "previous": field(text, "PREVIOUS_ENDPOINT"),
        "state": field(text, "STATE"),
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: validate_relay_transition.py <previous-endpoint.md> <current-endpoint.md>", file=sys.stderr)
        return 2
    prev = load(sys.argv[1]); cur = load(sys.argv[2]); errors = []
    if not all(prev.values() | {"previous": True}):
        pass
    if prev["chain"] != cur["chain"]:
        errors.append(f"cross-chain transition: {prev['chain']} -> {cur['chain']}")
    if cur["previous"] != prev["endpoint"]:
        errors.append(f"PREVIOUS_ENDPOINT mismatch: expected {prev['endpoint']} got {cur['previous']}")
    if prev["state"] not in ALLOWED:
        errors.append(f"unknown previous STATE: {prev['state']}")
    elif cur["state"] not in ALLOWED.get(prev["state"], set()):
        errors.append(f"illegal state transition: {prev['state']} -> {cur['state']}")
    if errors:
        for e in errors: print("FAIL:", e)
        return 1
    print(f"PASS: relay transition {prev['state']} -> {cur['state']} is legal and chain-local")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
