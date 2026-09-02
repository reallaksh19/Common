#!/usr/bin/env python3
"""Exact-byte intake helper for IOQM G9 GEO-05.

This tool never regenerates package content. It inventories the exact bytes supplied,
computes SHA-256 and Git blob IDs, and requires the custody verifier to pass before
marking intake admitted.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

EXPECTED_PACKAGE_NAME = "GEO-05_Coordinate_Vector_Mensuration_Representations"
EXPECTED_COUNT = 24
TARGET_PREFIX = "Grade 9/Mathematics/IOQM/03_Main_Topics/GEO-05_Coordinate_Vector_Mensuration_Representations"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()

def inventory(root: Path) -> dict:
    files = []
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        data = p.read_bytes(); rel = p.relative_to(root).as_posix()
        files.append({"relative_path": rel, "repository_path": f"{TARGET_PREFIX}/{rel}", "bytes": len(data), "sha256": sha256_bytes(data), "git_blob": git_blob_sha(data)})
    return {"schema":"geo05-exact-byte-intake-v1","package_root_name":root.name,"target_prefix":TARGET_PREFIX,"file_count":len(files),"files":files}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("root", type=Path); ap.add_argument("--verifier", type=Path, required=True); ap.add_argument("--manifest-out", type=Path, required=True); ap.add_argument("--allow-root-name-drift", action="store_true"); args = ap.parse_args()
    root = args.root.resolve()
    if not root.is_dir(): print(f"FAIL package root missing: {root}", file=sys.stderr); return 2
    if not args.allow_root_name_drift and root.name != EXPECTED_PACKAGE_NAME: print(f"FAIL package root name {root.name!r}; expected {EXPECTED_PACKAGE_NAME!r}", file=sys.stderr); return 2
    manifest = inventory(root); manifest["root_name_ok"] = root.name == EXPECTED_PACKAGE_NAME; manifest["file_count_ok"] = manifest["file_count"] == EXPECTED_COUNT
    verifier = args.verifier.resolve()
    if not verifier.is_file(): print(f"FAIL verifier missing: {verifier}", file=sys.stderr); return 2
    rc = subprocess.run([sys.executable, str(verifier), str(root)], check=False).returncode
    manifest["verifier_returncode"] = rc; manifest["verifier_pass"] = rc == 0
    manifest["admission_pass"] = bool(manifest["root_name_ok"] and manifest["file_count_ok"] and manifest["verifier_pass"] is True)
    out = args.manifest_out.resolve(); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n", encoding="utf-8"); print(out)
    if not manifest["root_name_ok"]: print("FAIL root name mismatch")
    if not manifest["file_count_ok"]: print(f"FAIL file count {manifest['file_count']} != {EXPECTED_COUNT}")
    if rc != 0: print(f"FAIL verifier returned {rc}")
    return 0 if manifest["admission_pass"] else 1

if __name__ == "__main__": raise SystemExit(main())
