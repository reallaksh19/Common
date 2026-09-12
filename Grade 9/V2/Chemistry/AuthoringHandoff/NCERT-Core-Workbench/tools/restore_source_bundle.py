#!/usr/bin/env python3
"""Restore the editable NCERT Chemistry workbench from text-safe bundle parts.

The handoff stores the final editable HTML/CSV sources as ordered base64 chunks
of a tar.gz archive under ``bundles/final-sources/``. This keeps the PR reviewable
through a UTF-8-only connector while still allowing another agent to reconstruct
the complete authoring tree exactly.

Run from the ``NCERT-Core-Workbench`` directory:

    python tools/restore_source_bundle.py --output restored-workspace

The restored tree contains:

    final/
      some-basic-concepts/
      behaviour-of-gases/
      chemical-bonding/
      redox-reactions/

Each topic contains ``core1.html``, ``core2.html`` and ``coverage-ledger.csv``.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import tarfile
from pathlib import Path

EXPECTED_SHA256 = "9be4cc8bc1d40c28ba5940b1d1048975cd20838b68145ad82f62918ae8b107af"
EXPECTED_BYTES = 117370


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--output", type=Path, default=Path("restored-workspace"))
    args = ap.parse_args()

    parts_dir = args.root / "bundles" / "final-sources"
    parts = sorted(parts_dir.glob("final-sources.tar.gz.b64.part*"))
    if not parts:
        raise SystemExit(f"No source bundle parts found under {parts_dir}")

    # Fail closed on missing/non-contiguous parts. Expected names are part000,
    # part001, ... in lexical order.
    expected_names = [f"final-sources.tar.gz.b64.part{i:03d}" for i in range(len(parts))]
    actual_names = [p.name for p in parts]
    if actual_names != expected_names:
        raise SystemExit(
            "Bundle part sequence is incomplete or out of order:\n"
            f"expected={expected_names}\nactual={actual_names}"
        )

    encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    try:
        payload = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f"Bundle base64 is invalid: {exc}") from exc

    digest = hashlib.sha256(payload).hexdigest()
    if len(payload) != EXPECTED_BYTES:
        raise SystemExit(f"Bundle size mismatch: expected {EXPECTED_BYTES}, got {len(payload)}")
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"Bundle SHA-256 mismatch: expected {EXPECTED_SHA256}, got {digest}")

    args.output.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tf:
        # Archive entries are generated locally and intentionally contain only
        # relative final/ paths. Still reject absolute paths / parent traversal.
        for member in tf.getmembers():
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise SystemExit(f"Unsafe archive member: {member.name}")
        tf.extractall(args.output)

    print(
        f"restored {len(parts)} parts ({len(payload)} bytes, sha256={digest}) "
        f"into {args.output.resolve()}"
    )


if __name__ == "__main__":
    main()
