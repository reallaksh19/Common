#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

LEGACY_PREFIXES = (
    "agents/agentchain.md",
    "agents/agentchain/",
)


def main():
    if len(sys.argv) not in {3, 4}:
        print("Usage: validate_legacy_relay_diff.py <repo-root> <base-ref> [head-ref]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    base = sys.argv[2]
    head = sys.argv[3] if len(sys.argv) == 4 else "HEAD"
    if not (root / ".git").exists():
        print("FAIL: git checkout required for legacy-relay diff validation")
        return 1
    cmd = ["git", "-C", str(root), "diff", "--name-status", f"{base}...{head}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL: cannot inspect changed paths:", r.stderr.strip())
        return 1
    violations = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        paths = parts[1:]
        for path in paths:
            if any(path == p or path.startswith(p) for p in LEGACY_PREFIXES):
                violations.append((status, path))
    if violations:
        for status, path in violations:
            print(f"FAIL: new material leg changes read-only legacy relay path: {status} {path}")
        print("Use agents/chains/<CHAIN_ID>/**; preserve legacy artifacts as historical provenance.")
        return 1
    print("PASS: no legacy relay writes in material-leg diff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
