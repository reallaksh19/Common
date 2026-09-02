#!/usr/bin/env python3
"""Fail-closed recovery scanner for the exact IOQM G9 GEO-05 package.

This tool never reconstructs or rewrites package bytes. It searches a faithful/full
Git checkout for the frozen GEO-05 names and expected PDF blobs, including refs,
reflogs, and unreachable commits/trees/blobs that GitHub's API cannot enumerate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

TARGET_TOPIC = "GEO-05_Coordinate_Vector_Mensuration_Representations"
TARGET_FILENAMES = {
    "GEO05_Student_Pack_v1.pdf": {
        "git_blob": "60ee54edc7a0f74c51723c7754f138170db43772",
        "sha256": "45468a443e8e150110299117d2f033e0ae8be111e747492b6ce490e80f8c5247",
        "bytes": 14257,
    },
    "GEO05_Teacher_Key_v1.pdf": {
        "git_blob": "aac1f03e31112adce627f871d033d2b06ff2ef87",
        "sha256": "54ba2add1bbdbdc4e18df11fac55dab3e739ba60f5cb8459e825bcbbeca94115",
        "bytes": 4686,
    },
}
TARGET_TOKENS = (
    TARGET_TOPIC,
    "GEO05_Student_Pack_v1.pdf",
    "GEO05_Teacher_Key_v1.pdf",
    "GEO05_Stable_Alternate_Representation_Interface_v1.md",
    "IOQM-G9-GEO-05",
)


def run_git(repo: Path, *args: str, check: bool = True, text: bool = True):
    cp = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        check=False,
    )
    if check and cp.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return cp


def is_git_repo(repo: Path) -> bool:
    cp = run_git(repo, "rev-parse", "--git-dir", check=False)
    return cp.returncode == 0


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_object_exists(repo: Path, oid: str, expected_type: str | None = None) -> bool:
    cp = run_git(repo, "cat-file", "-e", f"{oid}^{{{expected_type}}}" if expected_type else oid, check=False)
    return cp.returncode == 0


def read_blob(repo: Path, oid: str) -> bytes:
    cp = run_git(repo, "cat-file", "blob", oid, text=False)
    return cp.stdout


def list_named_objects(repo: Path) -> list[tuple[str, str]]:
    cp = run_git(repo, "rev-list", "--objects", "--all", "--reflog", check=False)
    rows: list[tuple[str, str]] = []
    if cp.returncode != 0:
        cp = run_git(repo, "rev-list", "--objects", "--all")
    for line in cp.stdout.splitlines():
        oid, sep, name = line.partition(" ")
        if sep:
            rows.append((oid, name))
    return rows


def matching_named_objects(repo: Path) -> list[dict]:
    out = []
    seen = set()
    for oid, name in list_named_objects(repo):
        if any(tok.lower() in name.lower() for tok in TARGET_TOKENS):
            key = (oid, name)
            if key not in seen:
                seen.add(key)
                out.append({"oid": oid, "path": name})
    return sorted(out, key=lambda x: (x["path"], x["oid"]))


def unreachable_objects(repo: Path) -> dict[str, list[str]]:
    cp = run_git(repo, "fsck", "--full", "--no-reflogs", "--unreachable", check=False)
    found: dict[str, list[str]] = {"commit": [], "tree": [], "blob": [], "tag": [], "other": []}
    for line in (cp.stdout + "\n" + cp.stderr).splitlines():
        parts = line.strip().split()
        if len(parts) >= 3 and parts[0] in {"unreachable", "dangling"}:
            typ, oid = parts[1], parts[2]
            found.setdefault(typ if typ in found else "other", []).append(oid)
    for k in found:
        found[k] = sorted(set(found[k]))
    return found


def scan_unreachable_commits(repo: Path, commit_oids: Iterable[str]) -> list[dict]:
    hits: list[dict] = []
    for oid in commit_oids:
        cp = run_git(repo, "ls-tree", "-r", "--name-only", oid, check=False)
        if cp.returncode != 0:
            continue
        matched = [p for p in cp.stdout.splitlines() if any(tok.lower() in p.lower() for tok in TARGET_TOKENS)]
        if matched:
            hits.append({"commit": oid, "paths": sorted(matched)})
    return hits


def scan_worktree(repo: Path) -> list[dict]:
    hits = []
    ignored = {".git", "node_modules", ".venv", "venv", "__pycache__"}
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in ignored]
        rootp = Path(root)
        for fn in files:
            p = rootp / fn
            rel = p.relative_to(repo).as_posix()
            if any(tok.lower() in rel.lower() for tok in TARGET_TOKENS):
                hits.append({"path": rel, "bytes": p.stat().st_size})
    return sorted(hits, key=lambda x: x["path"])


def verify_expected_pdf_blobs(repo: Path, dump_dir: Path | None) -> dict:
    result = {}
    if dump_dir:
        dump_dir.mkdir(parents=True, exist_ok=True)
    for filename, exp in TARGET_FILENAMES.items():
        oid = exp["git_blob"]
        rec = {
            "expected_git_blob": oid,
            "expected_sha256": exp["sha256"],
            "expected_bytes": exp["bytes"],
            "object_present": False,
            "object_type": None,
            "actual_sha256": None,
            "actual_bytes": None,
            "exact_match": False,
            "dumped_to": None,
        }
        if git_object_exists(repo, oid):
            typ = run_git(repo, "cat-file", "-t", oid).stdout.strip()
            rec["object_type"] = typ
            if typ == "blob":
                data = read_blob(repo, oid)
                rec["object_present"] = True
                rec["actual_sha256"] = sha256(data)
                rec["actual_bytes"] = len(data)
                rec["exact_match"] = rec["actual_sha256"] == exp["sha256"] and rec["actual_bytes"] == exp["bytes"]
                if dump_dir and rec["exact_match"]:
                    out = dump_dir / filename
                    out.write_bytes(data)
                    rec["dumped_to"] = str(out)
        result[filename] = rec
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo", type=Path, help="Path to a faithful/full Common Git checkout")
    ap.add_argument("--dump-exact-pdfs", type=Path, default=None,
                    help="Write only exact verified PDF blobs to this directory")
    ap.add_argument("--json-out", type=Path, default=None, help="Optional JSON report path")
    args = ap.parse_args()

    repo = args.repo.resolve()
    if not is_git_repo(repo):
        print(json.dumps({"status": "FAIL_NOT_GIT_REPO", "repo": str(repo)}, indent=2))
        return 2

    unreachable = unreachable_objects(repo)
    pdf_blobs = verify_expected_pdf_blobs(repo, args.dump_exact_pdfs)
    report = {
        "status": "RECOVERY_SCAN_COMPLETE",
        "repo": str(repo),
        "head": run_git(repo, "rev-parse", "HEAD").stdout.strip(),
        "target_topic": TARGET_TOPIC,
        "named_object_hits": matching_named_objects(repo),
        "worktree_hits": scan_worktree(repo),
        "unreachable_counts": {k: len(v) for k, v in unreachable.items()},
        "unreachable_commit_path_hits": scan_unreachable_commits(repo, unreachable.get("commit", [])),
        "expected_pdf_blobs": pdf_blobs,
        "exact_pdf_blob_count": sum(1 for v in pdf_blobs.values() if v["exact_match"]),
        "package_reconstruction_performed": False,
    }
    if report["exact_pdf_blob_count"] == 2:
        report["recovery_classification"] = "EXACT_FROZEN_PDF_BLOBS_RECOVERED"
    elif report["named_object_hits"] or report["unreachable_commit_path_hits"] or report["worktree_hits"]:
        report["recovery_classification"] = "PARTIAL_GEO05_EVIDENCE_FOUND"
    else:
        report["recovery_classification"] = "NO_GEO05_BYTES_FOUND"

    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded, encoding="utf-8")
    sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
