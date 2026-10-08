#!/usr/bin/env python3
"""C6 C5: external GitHub Actions artifact-digest custody for TWO handover files.

Trust anchor: GitHub's separately stored artifact metadata (run/repo/head, ZIP
SHA256), not content supplied inside the pair of handover files or a locally
provided expected digest. This is NOT a Sigstore/Owner signature or permanent
custody: GitHub may delete artifacts and retention is time-limited.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
sys.path.insert(0, str(V3))
from v3lib import canonical_digest  # noqa: E402

REPO = "reallaksh19/Common"
ARTIFACT = "c6-c5-provider-anchored-handover"
FILES = {"HANDOVER_CONTEXT.yaml", "EVENTS.jsonl"}
MAX_ZIP = 5_000_000
MAX_FILE = 2_000_000
VERIFY = Path(__file__).with_name("811_c6_c4_cold_successor.py")


def need(condition, marker):
    if not condition:
        raise RuntimeError(marker)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def gh_json(endpoint, token):
    request = Request("https://api.github.com" + endpoint, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urlopen(request, timeout=40) as res:
        raw = res.read(2_000_000)
        need(len(raw) < 2_000_000, "ANCHOR_OVERSIZED_GITHUB_METADATA")
        return json.loads(raw)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        return None


def get_archive(artifact_id, token):
    endpoint = f"https://api.github.com/repos/{REPO}/actions/artifacts/{artifact_id}/zip"
    request = Request(endpoint, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        build_opener(NoRedirect).open(request, timeout=40)
    except HTTPError as err:
        need(err.code == 302, "ANCHOR_EXPECTED_PROVIDER_REDIRECT")
        target = err.headers.get("Location")
    else:
        raise RuntimeError("ANCHOR_EXPECTED_PROVIDER_REDIRECT")
    parsed = urlparse(target or "")
    need(parsed.scheme == "https" and bool(parsed.netloc)
         and not parsed.username and not parsed.password,
         "ANCHOR_UNSAFE_SIGNED_ARCHIVE_LOCATION")
    # NEVER forward the GitHub bearer token to storage's signed URL.
    with urlopen(Request(target), timeout=65) as response:
        blob = response.read(MAX_ZIP + 1)
    need(0 < len(blob) <= MAX_ZIP, "ANCHOR_ARCHIVE_SIZE_OUT_OF_BOUNDS")
    return blob


def validate_metadata(item, run, repo_metadata, run_id, head, artifact_id):
    need(item.get("id") == artifact_id and item.get("name") == ARTIFACT,
         "ANCHOR_ARTIFACT_ID_OR_NAME_MISMATCH")
    need(item.get("expired") is False, "ANCHOR_ARTIFACT_EXPIRED")
    need(isinstance(item.get("size_in_bytes"), int)
         and 0 < item["size_in_bytes"] <= MAX_ZIP,
         "ANCHOR_METADATA_SIZE_INVALID")
    reference = item.get("workflow_run") or {}
    need(reference.get("id") == run_id and run.get("id") == run_id,
         "ANCHOR_RUN_ID_MISMATCH")
    need(reference.get("head_sha") == head and run.get("head_sha") == head,
         "ANCHOR_SOURCE_HEAD_SHA_MISMATCH")
    repository_id = repo_metadata.get("id")
    need(isinstance(repository_id, int)
         and reference.get("repository_id") == repository_id
         and reference.get("head_repository_id") == repository_id
         and (run.get("repository") or {}).get("id") == repository_id,
         "ANCHOR_REPOSITORY_IDENTITY_MISMATCH")
    need((run.get("repository") or {}).get("full_name") == REPO,
         "ANCHOR_REPOSITORY_NAME_MISMATCH")
    value = item.get("digest")
    need(isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", value),
         "ANCHOR_PROVIDER_DIGEST_UNAVAILABLE")
    return value.split(":", 1)[1]


def unpack_two(archive, folder):
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as zip_reader:
            members = zip_reader.infolist()
            need(len(members) == 2
                 and {z.filename for z in members} == FILES
                 and all(not z.is_dir() for z in members),
                 "ANCHOR_ZIP_UNEXPECTED_FILES")
            for member in members:
                mode = (member.external_attr >> 16) & 0xFFFF
                need(not stat.S_ISLNK(mode)
                     and 0 < member.file_size <= MAX_FILE
                     and member.compress_size <= MAX_ZIP,
                     "ANCHOR_ZIP_UNSAFE_FILE")
                content = zip_reader.read(member)
                need(len(content) == member.file_size, "ANCHOR_ZIP_TRUNCATED_FILE")
                (folder / member.filename).write_bytes(content)
    except (zipfile.BadZipFile, RuntimeError, OSError, ValueError) as exc:
        raise RuntimeError("ANCHOR_ZIP_INVALID") from exc
    return {name: digest((folder / name).read_bytes()) for name in FILES}


def self_consistent_joint_forgery(original_dir, expected_hashes):
    """Demonstrate local pair can be rewritten coherently but fails provider pin."""
    with tempfile.TemporaryDirectory() as tmp:
        copydir = Path(tmp)
        for name in FILES:
            shutil.copyfile(original_dir / name, copydir / name)
        ctx = yaml.safe_load((copydir / "HANDOVER_CONTEXT.yaml").read_bytes())
        events = [json.loads(x) for x in
                  (copydir / "EVENTS.jsonl").read_text(encoding="utf-8").splitlines()
                  if x.strip()]
        learning = ctx["accumulated_learning"]
        learning["what_changed"].append("COORDINATED_FORGERY_SIMULATION")
        linked = [e for e in events if e.get("type") == "HANDOVER_PLANNED"
                  and "source_graph_pinned_location" in (e.get("details") or {})]
        need(len(linked) == 1, "ANCHOR_FORGERY_NO_REAL_HANDOVER_EVENT")
        linked[0]["basis"][2] = canonical_digest(ctx)
        (copydir / "HANDOVER_CONTEXT.yaml").write_text(
            yaml.safe_dump(ctx, sort_keys=False), encoding="utf-8")
        (copydir / "EVENTS.jsonl").write_text(
            "".join(json.dumps(e, sort_keys=True) + "\n" for e in events),
            encoding="utf-8")
        env = os.environ.copy()
        env.pop("GH_TOKEN", None)
        env.pop("GITHUB_TOKEN", None)
        result = subprocess.run(
            [sys.executable, str(VERIFY), "--bundle", str(copydir), "--local-only"],
            capture_output=True, text=True, timeout=35, env=env,
        )
        need(result.returncode == 0 and
             "COLD_LOCAL_CONTEXT_EVENT_LINK=PASS_NOT_LIVE_CURRENT" in result.stdout,
             "ANCHOR_ADVERSARIAL_SELF_CONSISTENCY_NOT_REPRODUCED:" + result.stderr[-800:])
        print("ANCHOR_JOINT_FORGERY_PASSES_TWO_FILE_CHECK=PROVEN")
        changed = {name: digest((copydir / name).read_bytes()) for name in FILES}
        need(any(changed[name] != expected_hashes[name] for name in FILES),
             "ANCHOR_JOINT_FORGERY_ACCEPTED_BY_PROVIDER_PIN")
        print("ANCHOR_JOINT_FORGERY_REJECTED_AGAINST_GITHUB_BYTES=PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-id", required=True, type=int)
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--dest", required=True)
    args = parser.parse_args()
    need(args.artifact_id > 0 and args.run_id > 0
         and re.fullmatch(r"[0-9a-f]{40}", args.source_head),
         "ANCHOR_PROVIDER_SELECTORS_INVALID")
    need(os.getenv("GITHUB_REPOSITORY") == REPO, "ANCHOR_REPOSITORY_SCOPE_REQUIRED")
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    need(bool(token), "ANCHOR_ACTIONS_READ_TOKEN_REQUIRED")
    repo_metadata = gh_json("/repos/" + REPO, token)
    run = gh_json(f"/repos/{REPO}/actions/runs/{args.run_id}", token)
    artifact = gh_json(f"/repos/{REPO}/actions/artifacts/{args.artifact_id}", token)
    expected = validate_metadata(artifact, run, repo_metadata,
                                 args.run_id, args.source_head, args.artifact_id)
    print("ANCHOR_PROVIDER_RUN_REPO_HEAD_IDENTITY=PASS")
    archive = get_archive(args.artifact_id, token)
    need(digest(archive) == expected, "ANCHOR_PROVIDER_ARCHIVE_SHA256_MISMATCH")
    need(len(archive) == artifact["size_in_bytes"], "ANCHOR_PROVIDER_ARCHIVE_SIZE_MISMATCH")
    print("ANCHOR_GITHUB_ARCHIVE_DIGEST=PASS_PROVIDER_STORED_SHA256")
    dest = Path(args.dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    need(not list(dest.iterdir()), "ANCHOR_OUTPUT_MUST_START_EMPTY")
    original = unpack_two(archive, dest)
    print("ANCHOR_ZIP_EXACT_TWO_DURABLE_FILES=PASS")
    # Provider must detect altered ZIP bytes, not just disallow a bad event.
    tampered = bytearray(archive)
    tampered[len(tampered) // 2] ^= 0x01
    need(digest(tampered) != expected, "ANCHOR_BIT_FLIP_NOT_DETECTED")
    print("ANCHOR_ALTERED_ZIP_DIGEST_REJECTED=PASS")
    # Provider metadata MUST reject spoofed run/head even if the files match.
    for kwargs, code in [
        ({"run_id": args.run_id + 1}, "ANCHOR_RUN_ID_MISMATCH"),
        ({"head": "0" * 40}, "ANCHOR_SOURCE_HEAD_SHA_MISMATCH"),
    ]:
        params = {"run_id": args.run_id, "head": args.source_head}
        params.update(kwargs)
        try:
            validate_metadata(artifact, run, repo_metadata, params["run_id"],
                              params["head"], args.artifact_id)
        except RuntimeError as exc:
            need(str(exc) == code, "ANCHOR_NEGATIVE_WRONG_REFUSAL:" + str(exc))
        else:
            raise RuntimeError("ANCHOR_SPOOFED_IDENTITY_ACCEPTED:" + code)
    print("ANCHOR_WRONG_RUN_AND_HEAD_REJECTED=PASS")
    self_consistent_joint_forgery(dest, original)
    # No sourced trust material is written into the untrusted two-file handover.
    need(set(p.name for p in dest.iterdir()) == FILES,
         "ANCHOR_UNEXPECTED_OUTPUT_CUSTODY_FILE")
    print("C6_C5_PROVIDER_ANCHORED_CUSTODY=PASS_NOT_OWNER_SIGNED")


if __name__ == "__main__":
    main()
