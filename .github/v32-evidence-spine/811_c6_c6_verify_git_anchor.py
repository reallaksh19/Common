#!/usr/bin/env python3
"""Offline V3.2 handover archive verifier backed by an EXACT Git commit object.

Reads only the anchor blob from the immutable anchor commit. No GitHub token,
network, live status or owner permission needed for --archive verification.
The ZIP bytes must be separately retained after the 7-day Actions expiry.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
ANCHOR_SHA = "de3cac5d2c19b4301500fede250f4c56c226fda1"
# Git object ID of the exact verified 1,912-byte manifest. Unlike commit ancestry,
# this blob ID is preserved if the manifest is merged through a squash commit.
ANCHOR_BLOB_SHA = "c78fa3bf496feb21c76dac64874204252bc4c09b"
ANCHOR_PATH = ".github/v32-evidence-spine/811-c6-c6-git-custody-anchor-v1.json"
EXPECTED_REPO = "reallaksh19/Common"
EXPECTED_ARTIFACT = 11571023434
MEMBERS = {"EVENTS.jsonl", "HANDOVER_CONTEXT.yaml"}
MAX_ZIP = 5_000_000
MAX_FILE = 2_000_000


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def committed_anchor(root: Path = ROOT) -> dict:
    """Do not load a branch-local file or caller-provided manifest."""
    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args],
                              check=True, capture_output=True, timeout=20).stdout
    # Source selection is content-addressed, never a mutable branch-local YAML.
    # Preserve strict original-commit provenance when that commit is in HEAD
    # ancestry. For Owner-approved squash merges (no original parent lineage),
    # use the *committed HEAD blob* ONLY if its exact Git object ID equals the
    # independently precommitted/verified original blob. Never read worktree.
    try:
        ancestor = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor",
             ANCHOR_SHA, "HEAD"],
            capture_output=True, timeout=20,
        )
        anchor_ref = (
            ANCHOR_SHA + ":" + ANCHOR_PATH if ancestor.returncode == 0
            else "HEAD:" + ANCHOR_PATH
        )
        observed_blob = git("rev-parse", "--verify", anchor_ref).decode().strip()
        require(observed_blob == ANCHOR_BLOB_SHA, "GIT_ANCHOR_BLOB_IDENTITY_MISMATCH")
        raw = git("show", anchor_ref)
    except RuntimeError:
        raise
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise RuntimeError("GIT_ANCHOR_PINNED_BLOB_UNAVAILABLE") from exc
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError("GIT_ANCHOR_OBJECT_INVALID_JSON") from exc
    require(isinstance(result, dict) and
            result.get("schema") == "common-v32-c6-c6-git-content-anchor-v1"
            and result.get("authority") == "AGENT_RECORDED_PROVIDER_EVIDENCE_NOT_OWNER_SIGNATURE",
            "GIT_ANCHOR_AUTHORITY_INVALID")
    source = result.get("source")
    require(isinstance(source, dict)
            and source.get("repository") == EXPECTED_REPO
            and source.get("repository_id") == 1207996454
            and source.get("artifact_id") == EXPECTED_ARTIFACT
            and source.get("workflow_run_id") == 37826161172
            and source.get("workflow_head_sha") == "c14f41abbd0f5a0ee4d738a8c4927c2faf5149ac"
            and source.get("artifact_name") == "c6-c5-provider-anchored-handover"
            and source.get("workflow_run_conclusion") == "success",
            "GIT_ANCHOR_PROVIDER_IDENTITY_INVALID")
    require(result.get("privacy", "").startswith("COMMIT_ONLY_HASHES"),
            "GIT_ANCHOR_PRIVACY_POLICY_INVALID")
    require(result.get("owner_original_message_permalink") == "UNKNOWN",
            "GIT_ANCHOR_OWNER_ORIGIN_CLAIM_UNVERIFIED")
    need = result.get("files")
    require(isinstance(need, list) and len(need) == 2
            and {f.get("name") for f in need} == MEMBERS,
            "GIT_ANCHOR_FILE_INVENTORY_INVALID")
    for f in need:
        require(isinstance(f.get("bytes"), int) and 0 < f["bytes"] <= MAX_FILE
                and isinstance(f.get("sha256"), str)
                and re.fullmatch(r"[0-9a-f]{64}", f["sha256"]),
                "GIT_ANCHOR_FILE_HASH_INVALID")
    require(isinstance(source.get("artifact_zip_sha256"), str)
            and re.fullmatch(r"[0-9a-f]{64}", source["artifact_zip_sha256"])
            and isinstance(source.get("artifact_zip_bytes"), int)
            and 0 < source["artifact_zip_bytes"] <= MAX_ZIP,
            "GIT_ANCHOR_ARCHIVE_HASH_INVALID")
    return result


def verify_archive_bytes(archive: bytes, manifest: dict) -> dict[str, bytes]:
    source = manifest["source"]
    require(0 < len(archive) <= MAX_ZIP, "GIT_ANCHOR_ARCHIVE_OVERSIZED")
    require(len(archive) == source["artifact_zip_bytes"]
            and sha256(archive) == source["artifact_zip_sha256"],
            "GIT_ANCHOR_ARCHIVE_BYTES_MISMATCH")
    file_index = {x["name"]: x for x in manifest["files"]}
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            members = z.infolist()
            require(len(members) == 2 and
                    {x.filename for x in members} == MEMBERS
                    and all(not x.is_dir() for x in members),
                    "GIT_ANCHOR_ARCHIVE_FILE_INVENTORY_MISMATCH")
            result = {}
            for item in members:
                mode = (item.external_attr >> 16) & 0xFFFF
                require(not stat.S_ISLNK(mode)
                        and item.file_size == file_index[item.filename]["bytes"]
                        and item.file_size <= MAX_FILE
                        and item.compress_size <= MAX_ZIP,
                        "GIT_ANCHOR_ARCHIVE_FILE_METADATA_INVALID")
                raw = z.read(item)
                require(len(raw) == item.file_size
                        and sha256(raw) == file_index[item.filename]["sha256"],
                        "GIT_ANCHOR_FILE_HASH_MISMATCH:" + item.filename)
                result[item.filename] = raw
    except (zipfile.BadZipFile, OSError, KeyError, ValueError) as exc:
        raise RuntimeError("GIT_ANCHOR_BAD_ARCHIVE") from exc
    return result


def run_offline(path: Path) -> dict[str, bytes]:
    manifest = committed_anchor()
    require(path.is_file() and not path.is_symlink(), "GIT_ANCHOR_LOCAL_ARCHIVE_NOT_REGULAR")
    archive = path.read_bytes()
    result = verify_archive_bytes(archive, manifest)
    # Complete a second-process cold reconstruction of both verified source
    # artifacts, not merely two hash comparisons. No token, network or
    # execution permission crosses this boundary.
    with tempfile.TemporaryDirectory() as directory:
        from pathlib import Path
        folder = Path(directory)
        for name, raw in result.items():
            (folder / name).write_bytes(raw)
        env = dict(os.environ)
        env.pop("GH_TOKEN", None)
        env.pop("GITHUB_TOKEN", None)
        verifier = Path(__file__).with_name("811_c6_c4_cold_successor.py")
        proc = subprocess.run(
            [sys.executable, str(verifier), "--bundle", str(folder), "--local-only"],
            capture_output=True, text=True, timeout=40, env=env,
        )
        require(proc.returncode == 0 and
                "COLD_OFFLINE_AUTHORITY=NO_SOURCE_CURRENTNESS_NO_EXECUTION" in proc.stdout,
                "GIT_ANCHOR_OFFLINE_CONTEXT_REPLAY_INVALID")
    print("C6_C6_OFFLINE_COLD_CONTEXT_REPLAY=PASS_NO_TOKEN")
    print("C6_C6_GIT_ANCHOR_COMMIT=" + ANCHOR_SHA)
    print("C6_C6_OFFLINE_RETAINED_ARCHIVE=VERIFIED_TWO_FILES")
    print("C6_C6_OWNER_SIGNATURE_OR_INDEPENDENT_REVIEW=NOT_CLAIMED")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    run_offline(args.archive)


if __name__ == "__main__":
    main()
