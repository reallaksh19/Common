#!/usr/bin/env python3
"""Atomic restoration contract for the exact IOQM G9 GEO-05 package.

This tool is for custody restoration only. It never regenerates, normalizes, edits,
or repairs package files. A candidate package is admitted only when the existing
GEO-05 exact-byte intake + static verifier pass. The admitted bytes are copied to a
temporary directory, byte identity is rechecked, and the directory is atomically
renamed into place. No material Git mutation is performed by this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_PACKAGE_NAME = "GEO-05_Coordinate_Vector_Mensuration_Representations"
EXPECTED_FILE_COUNT = 24
SCHEMA = "geo05-restoration-contract-v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def inventory(root: Path) -> list[dict]:
    rows: list[dict] = []
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        data = p.read_bytes()
        rows.append({
            "path": p.relative_to(root).as_posix(),
            "bytes": len(data),
            "sha256": sha256_bytes(data),
            "git_blob": git_blob_sha(data),
        })
    return rows


def reject_symlinks(root: Path) -> list[str]:
    bad: list[str] = []
    for p in root.rglob("*"):
        if p.is_symlink():
            bad.append(p.relative_to(root).as_posix())
    return sorted(bad)


def run_intake(intake: Path, verifier: Path, root: Path, manifest_out: Path) -> tuple[int, dict | None, str]:
    cp = subprocess.run(
        [sys.executable, str(intake), str(root), "--verifier", str(verifier), "--manifest-out", str(manifest_out)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    manifest = None
    if manifest_out.is_file():
        try:
            manifest = json.loads(manifest_out.read_text(encoding="utf-8"))
        except Exception:
            manifest = None
    return cp.returncode, manifest, cp.stdout


def compare_inventories(a: list[dict], b: list[dict]) -> tuple[bool, dict]:
    ma = {r["path"]: r for r in a}
    mb = {r["path"]: r for r in b}
    missing = sorted(set(ma) - set(mb))
    extra = sorted(set(mb) - set(ma))
    mismatched: list[dict] = []
    for path in sorted(set(ma) & set(mb)):
        if ma[path] != mb[path]:
            mismatched.append({"path": path, "source": ma[path], "staged": mb[path]})
    ok = not missing and not extra and not mismatched
    return ok, {"missing": missing, "extra": extra, "mismatched": mismatched}


def ensure_empty_destination(dest: Path) -> None:
    if dest.exists():
        if not dest.is_dir():
            raise RuntimeError(f"destination exists and is not a directory: {dest}")
        if any(dest.iterdir()):
            raise RuntimeError(f"destination exists and is not empty: {dest}")
        dest.rmdir()


def atomic_stage(source: Path, dest: Path) -> tuple[list[dict], list[dict], dict]:
    ensure_empty_destination(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    source_inv = inventory(source)
    tmp = Path(tempfile.mkdtemp(prefix=f".{dest.name}.restore-", dir=str(dest.parent)))
    try:
        stage_root = tmp / dest.name
        shutil.copytree(source, stage_root, copy_function=shutil.copy2, symlinks=False)
        staged_inv = inventory(stage_root)
        identity_ok, diff = compare_inventories(source_inv, staged_inv)
        if not identity_ok:
            raise RuntimeError(f"staged byte identity mismatch: {json.dumps(diff, sort_keys=True)}")
        os.replace(stage_root, dest)
        return source_inv, staged_inv, diff
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("candidate", type=Path, help="candidate exact GEO-05 package root")
    ap.add_argument("--intake", type=Path, required=True, help="geo05_intake.py")
    ap.add_argument("--verifier", type=Path, required=True, help="geo05_verify.py")
    ap.add_argument("--stage-to", type=Path, help="destination package directory; omitted for admission-only mode")
    ap.add_argument("--receipt-out", type=Path, required=True, help="JSON restoration receipt")
    args = ap.parse_args()

    candidate = args.candidate.resolve()
    intake = args.intake.resolve()
    verifier = args.verifier.resolve()
    receipt_out = args.receipt_out.resolve()
    receipt: dict = {
        "schema": SCHEMA,
        "candidate": str(candidate),
        "expected_package_name": EXPECTED_PACKAGE_NAME,
        "expected_file_count": EXPECTED_FILE_COUNT,
        "admission_pass": False,
        "staged": False,
        "source_staged_identity_pass": False,
        "material_git_mutation_performed": False,
        "content_regeneration_performed": False,
    }

    try:
        if not candidate.is_dir():
            raise RuntimeError(f"candidate package directory missing: {candidate}")
        if candidate.name != EXPECTED_PACKAGE_NAME:
            raise RuntimeError(f"candidate root name {candidate.name!r}; expected {EXPECTED_PACKAGE_NAME!r}")
        if not intake.is_file():
            raise RuntimeError(f"intake helper missing: {intake}")
        if not verifier.is_file():
            raise RuntimeError(f"verifier missing: {verifier}")
        symlinks = reject_symlinks(candidate)
        receipt["symlinks"] = symlinks
        if symlinks:
            raise RuntimeError(f"candidate contains symlinks: {symlinks}")

        receipt_out.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="geo05-admission-") as td:
            manifest_path = Path(td) / "intake.json"
            rc, manifest, intake_output = run_intake(intake, verifier, candidate, manifest_path)
        receipt["intake_returncode"] = rc
        receipt["intake_output"] = intake_output
        receipt["intake_manifest"] = manifest
        if rc != 0 or not manifest or manifest.get("admission_pass") is not True:
            raise RuntimeError("candidate failed exact-byte intake/static verifier")
        if manifest.get("file_count") != EXPECTED_FILE_COUNT:
            raise RuntimeError("intake manifest file count is not exactly 24")
        receipt["admission_pass"] = True
        receipt["source_inventory"] = inventory(candidate)

        if args.stage_to is not None:
            dest = args.stage_to.resolve()
            if dest.name != EXPECTED_PACKAGE_NAME:
                raise RuntimeError(f"stage destination root name {dest.name!r}; expected {EXPECTED_PACKAGE_NAME!r}")
            src_inv, staged_inv, _ = atomic_stage(candidate, dest)
            receipt["stage_to"] = str(dest)
            receipt["staged"] = True
            receipt["staged_inventory"] = staged_inv
            identity_ok, identity_diff = compare_inventories(src_inv, staged_inv)
            receipt["source_staged_identity_pass"] = identity_ok
            receipt["identity_diff"] = identity_diff
            if not identity_ok:
                raise RuntimeError("post-stage source/staged identity check failed")
        else:
            receipt["source_staged_identity_pass"] = None

        receipt["status"] = "PASS_ADMITTED_AND_STAGED" if receipt["staged"] else "PASS_ADMISSION_ONLY"
        receipt_out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(receipt_out)
        return 0
    except Exception as exc:
        receipt["status"] = "FAIL"
        receipt["error"] = str(exc)
        receipt_out.parent.mkdir(parents=True, exist_ok=True)
        receipt_out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"FAIL: {exc}", file=sys.stderr)
        print(receipt_out)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
