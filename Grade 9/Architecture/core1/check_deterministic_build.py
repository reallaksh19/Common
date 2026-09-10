#!/usr/bin/env python3
"""Fail closed if identical Core (1) input does not rebuild byte-for-byte."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def files(root: Path) -> dict[str, Path]:
    return {
        str(path.relative_to(root)): path
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def manifest(root: Path) -> dict:
    matches = sorted(root.glob("*_Research_Bundle_Manifest.json"))
    if len(matches) != 1:
        raise SystemExit(f"expected one ResearchBundleManifest in {root}, found {len(matches)}")
    return json.loads(matches[0].read_text(encoding="utf-8"))


def run(builder: Path, input_path: Path, out: Path) -> None:
    subprocess.run(
        [sys.executable, str(builder), "--input", str(input_path), "--out", str(out)],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument(
        "--builder",
        type=Path,
        default=Path(__file__).with_name("build_research_package.py"),
    )
    args = ap.parse_args()

    input_path = args.input.resolve()
    builder = args.builder.resolve()
    with tempfile.TemporaryDirectory(prefix="core1-determinism-") as tmp:
        root = Path(tmp)
        first = root / "first"
        second = root / "second"
        run(builder, input_path, first)
        run(builder, input_path, second)

        first_files = files(first)
        second_files = files(second)
        if first_files.keys() != second_files.keys():
            missing_first = sorted(second_files.keys() - first_files.keys())
            missing_second = sorted(first_files.keys() - second_files.keys())
            raise SystemExit(
                "Core1 deterministic rebuild changed file set: "
                f"only_second={missing_first} only_first={missing_second}"
            )

        mismatches = []
        for rel in first_files:
            left = first_files[rel]
            right = second_files[rel]
            left_hash = sha256(left)
            right_hash = sha256(right)
            if left_hash != right_hash:
                mismatches.append((rel, left_hash, right_hash))
        if mismatches:
            detail = "\n".join(
                f"  {rel}: first={left_hash} second={right_hash}"
                for rel, left_hash, right_hash in mismatches
            )
            raise SystemExit(f"Core1 deterministic rebuild failed:\n{detail}")

        first_manifest = manifest(first)
        second_manifest = manifest(second)
        if first_manifest["package_digest"] != second_manifest["package_digest"]:
            raise SystemExit("byte-identical outputs reported different package_digest values")

        print("CORE1_DETERMINISTIC_REBUILD = PASS")
        print(f"package_digest = {first_manifest['package_digest']}")
        print(f"artifacts_compared = {len(first_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
