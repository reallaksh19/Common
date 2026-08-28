#!/usr/bin/env python3
from pathlib import Path
import re
import sys

from validate_agentchain import field_value, TERMINAL_STATES


def section_paths(endpoint_text: str):
    found = set()
    for heading in (
        "Expected next-leg files / domains",
        "Production paths",
        "Validation / test paths",
        "Benchmarks",
        "Authoritative sources",
    ):
        m = re.search(
            rf"(?mis)^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|\Z)",
            endpoint_text,
        )
        if not m:
            continue
        for token in re.findall(r"`([^`]+)`", m.group(1)):
            token = token.strip()
            if token and not token.startswith(("PASS", "FAIL", "NOT_")):
                found.add(token.rstrip("/"))
    return found


def overlaps(a: str, b: str):
    aa = a.rstrip("/*")
    bb = b.rstrip("/*")
    return aa == bb or aa.startswith(bb + "/") or bb.startswith(aa + "/")


def load_canonical_rows(chains_dir: Path):
    rows = []
    for chain_dir in sorted(p for p in chains_dir.iterdir() if p.is_dir()):
        active = chain_dir / "ACTIVE.md"
        if not active.is_file():
            continue
        text = active.read_text(encoding="utf-8")
        state = field_value(text, "STATE") or "UNKNOWN"
        if state in TERMINAL_STATES:
            continue
        locator = field_value(text, "ACTIVE_ENDPOINT_FILE")
        endpoint = chains_dir.parent.parent / locator if locator else None
        endpoint_text = endpoint.read_text(encoding="utf-8") if endpoint and endpoint.is_file() else ""
        rows.append(
            {
                "chain": field_value(text, "CHAIN_ID") or chain_dir.name,
                "authority": field_value(text, "AUTHORITY_DOMAIN") or "",
                "dependencies": field_value(text, "DEPENDENCIES") or "",
                "coordination": field_value(text, "COORDINATION_STATE") or "UNKNOWN",
                "paths": section_paths(endpoint_text),
            }
        )
    return rows


def parse_legacy_active_rows(text: str):
    m = re.search(r"(?mis)^## ACTIVE CHAINS\s*$\n(.*?)(?=^## ENDPOINT LOG\s*$|\Z)", text)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        if not line.startswith("|") or "---" in line or "Chain" in line:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) >= 8:
            rows.append({"chain": cols[0], "endpoint_file": cols[3], "authority": cols[6]})
    return rows


def load_legacy_rows(index: Path):
    rows = []
    for row in parse_legacy_active_rows(index.read_text(encoding="utf-8")):
        p = (index.parent.parent / row["endpoint_file"]).resolve()
        text = p.read_text(encoding="utf-8") if p.exists() else ""
        rows.append(
            {
                "chain": row["chain"],
                "authority": row["authority"],
                "dependencies": "",
                "coordination": "UNKNOWN",
                "paths": section_paths(text),
            }
        )
    return rows


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: detect_chain_overlap.py <repo-root-or-agents/chains-or-legacy-agentchain.md>",
            file=sys.stderr,
        )
        return 2

    supplied = Path(sys.argv[1]).resolve()
    if supplied.is_file():
        rows = load_legacy_rows(supplied)
        mode = "legacy-index"
    else:
        chains_dir = supplied if supplied.name == "chains" else supplied / "agents" / "chains"
        if not chains_dir.is_dir():
            print(f"FAIL: canonical chain store not found: {chains_dir}", file=sys.stderr)
            return 1
        rows = load_canonical_rows(chains_dir)
        mode = "chain-local"

    conflicts = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a = rows[i]
            b = rows[j]
            authority_overlap = (
                a["authority"] == b["authority"]
                and a["authority"] not in {"", "NONE", "N/A"}
            )
            path_hits = sorted(
                (x, y) for x in a["paths"] for y in b["paths"] if overlaps(x, y)
            )
            dependency_overlap = b["chain"] in a["dependencies"] or a["chain"] in b["dependencies"]
            if authority_overlap or path_hits or dependency_overlap:
                conflicts.append(
                    (a["chain"], b["chain"], authority_overlap, dependency_overlap, path_hits)
                )

    if conflicts:
        for a, b, auth, dep, hits in conflicts:
            print(
                f"COORDINATION_REQUIRED: {a} <-> {b}; "
                f"authority_overlap={auth}; dependency={dep}; path_overlap={hits}"
            )
        return 1

    print(f"PASS: no active-chain authority/path/dependency overlap detected ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
