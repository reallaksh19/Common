#!/usr/bin/env python3
from pathlib import Path
import re
import sys


def parse_active_rows(text: str):
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


def section_paths(endpoint_text: str):
    found = set()
    for heading in ("Expected next-leg files / domains", "Production paths", "Validation / test paths"):
        m = re.search(rf"(?mis)^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|\Z)", endpoint_text)
        if not m:
            continue
        for token in re.findall(r"`([^`]+)`", m.group(1)):
            token = token.strip()
            if token and not token.startswith(("PASS", "FAIL", "NOT_")):
                found.add(token.rstrip("/"))
    return found


def overlaps(a: str, b: str):
    aa = a.rstrip("/*"); bb = b.rstrip("/*")
    return aa == bb or aa.startswith(bb + "/") or bb.startswith(aa + "/")


def main():
    if len(sys.argv) != 2:
        print("Usage: detect_chain_overlap.py <agents/agentchain.md>", file=sys.stderr)
        return 2
    index = Path(sys.argv[1]).resolve()
    rows = parse_active_rows(index.read_text(encoding="utf-8"))
    details = []
    for row in rows:
        p = (index.parent.parent / row["endpoint_file"]).resolve()
        paths = section_paths(p.read_text(encoding="utf-8")) if p.exists() else set()
        details.append((row, paths))

    conflicts = []
    for i in range(len(details)):
        for j in range(i + 1, len(details)):
            a, ap = details[i]; b, bp = details[j]
            authority_overlap = a["authority"] == b["authority"] and a["authority"] not in {"", "NONE", "N/A"}
            path_hits = sorted((x, y) for x in ap for y in bp if overlaps(x, y))
            if authority_overlap or path_hits:
                conflicts.append((a["chain"], b["chain"], authority_overlap, path_hits))
    if conflicts:
        for a, b, auth, hits in conflicts:
            print(f"COORDINATION_REQUIRED: {a} <-> {b}; authority_overlap={auth}; path_overlap={hits}")
        return 1
    print("PASS: no active-chain authority/path overlap detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
