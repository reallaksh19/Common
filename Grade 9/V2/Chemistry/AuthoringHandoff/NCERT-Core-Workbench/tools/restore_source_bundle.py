#!/usr/bin/env python3
"""Restore the full editable source workspace from text-safe bundle parts.

The GitHub connector used to create this handoff only exposes UTF-8 content
writes. To preserve the complete editable HTML/CSV workbench without dropping
large files, the source workspace is stored as ordered base64 chunks of a
`tar.gz` archive under `bundles/source-workspace/`.

Run from the NCERT-Core-Workbench directory:

    python tools/restore_source_bundle.py --output restored-workspace

The restored tree contains `final/` and `history/` source HTML/CSVs plus the
handoff documentation/tools used to make them.
"""
from __future__ import annotations

import argparse
import base64
import io
import tarfile
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--output", type=Path, default=Path("restored-workspace"))
    args = ap.parse_args()
    parts_dir = args.root / "bundles" / "source-workspace"
    parts = sorted(parts_dir.glob("source-workspace.tar.gz.b64.part*"))
    if not parts:
        raise SystemExit(f"No source bundle parts found under {parts_dir}")
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    payload = base64.b64decode(encoded)
    args.output.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
        tf.extractall(args.output)
    print(f"restored {len(parts)} parts into {args.output.resolve()}")


if __name__ == "__main__":
    main()
