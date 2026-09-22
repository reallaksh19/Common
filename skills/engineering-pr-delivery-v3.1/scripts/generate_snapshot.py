#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from snapshot_projection import build
from v3lib import load_yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Engineering Relay V3.1 CURRENT_SNAPSHOT from canonical authority.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--base-ref", help="Current base ref for active material-basis inspection.")
    parser.add_argument("--apply", action="store_true", help="Write STATE.generated.snapshot atomically after successful generation.")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    snapshot = build(root, args.base_ref)
    if args.apply:
        state = load_yaml(root / "relay/STATE.yaml")
        output = root / str((state.get("generated") or {}).get("snapshot"))
        output.parent.mkdir(parents=True, exist_ok=True)
        temp = output.with_suffix(output.suffix + ".tmp")
        temp.write_text(yaml.safe_dump(snapshot, sort_keys=False), encoding="utf-8")
        temp.replace(output)
        print(json.dumps({"status": "PASS", "output": str(output.relative_to(root))}, indent=2))
    else:
        print(yaml.safe_dump(snapshot, sort_keys=False), end="")


if __name__ == "__main__":
    main()
