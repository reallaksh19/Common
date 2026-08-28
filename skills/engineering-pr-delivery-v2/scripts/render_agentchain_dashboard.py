#!/usr/bin/env python3
from pathlib import Path
import sys

from validate_agentchain import field_value, TERMINAL_STATES


def main():
    if len(sys.argv) != 2:
        print("Usage: render_agentchain_dashboard.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2

    supplied = Path(sys.argv[1]).resolve()
    chains_dir = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
    if not chains_dir.is_dir():
        print(f"ERROR: canonical chain store not found: {chains_dir}", file=sys.stderr)
        return 1

    rows = []
    for chain_dir in sorted(p for p in chains_dir.iterdir() if p.is_dir()):
        active = chain_dir / "ACTIVE.md"
        if not active.is_file():
            continue
        text = active.read_text(encoding="utf-8")
        state = field_value(text, "STATE") or "UNKNOWN"
        if state in TERMINAL_STATES:
            continue
        rows.append([
            field_value(text, "CHAIN_ID") or chain_dir.name,
            field_value(text, "MISSION") or "",
            field_value(text, "ACTIVE_ENDPOINT") or "",
            field_value(text, "PR") or "",
            state,
            field_value(text, "AUTHORITY_DOMAIN") or "",
            field_value(text, "ACTIVE_CUSTODIAN") or "",
            field_value(text, "CUSTODY_EPOCH") or "",
            field_value(text, "COORDINATION_STATE") or "",
        ])

    print("# Engineering Agent Chain Dashboard")
    print()
    print("DERIVED_VIEW: true")
    print("AUTHORITATIVE_STATE: agents/chains/<CHAIN_ID>/ACTIVE.md")
    print()
    print("| Chain | Mission | Endpoint | PR | State | Authority | Custodian | Epoch | Coordination |")
    print("|---|---|---|---|---|---|---|---:|---|")
    for row in rows:
        safe = [value.replace("|", "\\|") for value in row]
        print("| " + " | ".join(safe) + " |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
