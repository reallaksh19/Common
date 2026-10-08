#!/usr/bin/env python3
"""C6 successor from two saved artifacts in a NEW process (no producer globals).

Modes: offline verifies custody linkage but NEVER currentness; live re-reads
immutable graph and current GitHub issue/PR facts through a GET-only facade.
This is an engineering replay, not an independent human/agent reviewer.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/engineering-pr-delivery-v3.2/scripts"))
from v3lib import load_yaml, load_events, canonical_digest  # noqa: E402
from handover_context import build_delp_source_bound_successor, HandoverContextError  # noqa: E402

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")
LEAF = re.compile(r"^[A-Za-z0-9_.-]+#[1-9][0-9]*$")
KEYS = {"graph", "plan", "input", "provider"}


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def read_bundle(directory):
    """The frozen event binds the context hash, four axes and graph locator."""
    context_path = directory / "HANDOVER_CONTEXT.yaml"
    events_path = directory / "EVENTS.jsonl"
    require(context_path.is_file() and not context_path.is_symlink(),
            "COLD_CONTEXT_NOT_DURABLE_REGULAR_FILE")
    require(events_path.is_file() and not events_path.is_symlink(),
            "COLD_EVENTS_NOT_DURABLE_REGULAR_FILE")
    ctx = load_yaml(context_path)
    events, errors = load_events(events_path)
    require(isinstance(ctx, dict) and not errors, "COLD_CONTEXT_OR_EVENT_INVALID")
    bound = ctx.get("source_bound_successor") or {}
    require(isinstance(bound, dict) and bound.get("schema") == "relay-v3.2-source-bound-successor-v1",
            "COLD_SOURCE_BASIS_MISSING")
    require(bound.get("authority") == "DERIVED_RECONSTRUCTION_READ_ONLY"
            and bound.get("execution_admission") == "NEVER_FROM_RECONSTRUCTION"
            and bound.get("owner_merge_authority") == "NOT_GRANTED"
            and bound.get("authority_effects") == []
            and bound.get("owner_source_status") == "UNRESOLVED_CHAT_MESSAGE_LINK",
            "COLD_SOURCE_AUTHORITY_NOT_QUARANTINED")
    chosen = [event for event in events
              if event.get("type") == "HANDOVER_PLANNED"
              and isinstance(event.get("details"), dict)
              and event["details"].get("source_graph_pinned_location") is not None]
    require(len(chosen) == 1, "COLD_EXACTLY_ONE_BOUND_HANDOVER_REQUIRED")
    event = chosen[0]
    basis = event.get("basis")
    require(isinstance(basis, list) and len(basis) >= 3
            and basis[2] == canonical_digest(ctx), "COLD_CONTEXT_DIGEST_MISMATCH")
    saved = bound.get("digests")
    require(isinstance(saved, dict) and set(saved) == KEYS
            and all(isinstance(v, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", v)
                    for v in saved.values()), "COLD_SOURCE_DIGESTS_INCOMPLETE")
    detail = event["details"]
    for axis in KEYS:
        require(detail.get("source_bound_" + axis + "_digest") == saved[axis],
                "COLD_EVENT_SOURCE_DIGEST_MISMATCH:" + axis)
    challenge = (ctx.get("successor_entry") or {}).get("challenge_basis") or {}
    require(challenge.get("source_input_digest") == saved["input"]
            and challenge.get("source_plan_digest") == saved["plan"],
            "COLD_CHALLENGE_BASIS_NOT_BOUND")
    origin = detail["source_graph_pinned_location"]
    require(isinstance(origin, dict) and set(origin) == {
        "repository", "revision", "path", "permalink"
    }, "COLD_SOURCE_LOCATION_SCHEMA")
    repository, revision, graph_path = (
        origin.get("repository"), origin.get("revision"), origin.get("path")
    )
    require(isinstance(repository, str) and REPO.fullmatch(repository)
            and repository.lower() == str(bound.get("repository") or "").lower(),
            "COLD_SOURCE_REPOSITORY_INVALID")
    require(isinstance(revision, str) and SHA.fullmatch(revision),
            "COLD_SOURCE_REVISION_NOT_IMMUTABLE")
    require(isinstance(graph_path, str) and len(graph_path) < 256
            and graph_path.endswith(".json")
            and not graph_path.startswith("/")
            and all(p not in ("", ".", "..") for p in graph_path.split("/")),
            "COLD_SOURCE_LOCATION_PATH_INVALID")
    permalink = "https://github.com/" + repository + "/blob/" + revision + "/" + graph_path
    require(origin.get("permalink") == permalink, "COLD_SOURCE_LOCATION_LINK_MISMATCH")
    require(isinstance(bound.get("leaf"), str) and LEAF.fullmatch(bound["leaf"]),
            "COLD_SOURCE_LEAF_INVALID")
    require(bound.get("currentness") == "CURRENT_READ_ONLY"
            and not bound.get("moved_axes"),
            "COLD_SAVED_BASIS_WAS_NOT_CURRENT")
    return ctx, event, origin, saved


def authenticated_read_only_graph(origin):
    repository = origin["repository"]
    require((os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN"))
            and os.getenv("GITHUB_REPOSITORY", "").lower() == repository.lower(),
            "COLD_GITHUB_TOKEN_OR_REPO_SCOPE_REQUIRED")
    endpoint = ("repos/" + repository + "/contents/"
                + quote(origin["path"], safe="/") + "?ref=" + origin["revision"])
    try:
        raw = subprocess.run(["gh", "api", "--method", "GET", endpoint],
                             capture_output=True, text=True, check=True, timeout=45)
        item = json.loads(raw.stdout)
        require(item.get("type") == "file" and item.get("encoding") == "base64",
                "COLD_GRAPH_BLOB_NOT_CANONICAL")
        packed = re.sub(r"\\s+", "", item["content"])
        graph_bytes = base64.b64decode(packed, validate=True)
        require(len(graph_bytes) <= 5_000_000, "COLD_GRAPH_TOO_LARGE")
        graph = json.loads(graph_bytes)
    except (subprocess.SubprocessError, OSError, KeyError, ValueError) as exc:
        raise RuntimeError("COLD_GITHUB_GRAPH_GET_FAILED") from exc
    require(isinstance(graph, dict)
            and str((graph.get("programme") or {}).get("repository") or "").lower()
                == repository.lower(),
            "COLD_GRAPH_REPOSITORY_MISMATCH")
    return graph


def replay(bundle, live, negative_stale):
    ctx, event, origin, digests = read_bundle(bundle)
    print("COLD_LOCAL_CONTEXT_EVENT_LINK=PASS_NOT_LIVE_CURRENT")
    if not live:
        require(not negative_stale, "COLD_NEGATIVE_STALE_REQUIRES_REAL_PROVIDER")
        print("COLD_OFFLINE_AUTHORITY=NO_SOURCE_CURRENTNESS_NO_EXECUTION")
        return
    graph = authenticated_read_only_graph(origin)
    import delp_projection_v32 as delp

    class ReadOnlyProvider:
        # No update_issue, update_pull or other writer in the exposed API.
        def __init__(self):
            self.__transport = delp.GhTransport(origin["repository"])

        def get_commit_sha(self, ref):
            return self.__transport.get_commit_sha(ref)

        def get_issue(self, number):
            return self.__transport.get_issue(number)

        def get_pull(self, number):
            return self.__transport.get_pull(number)

        def compare(self, base, head):
            return self.__transport.compare(base, head)

        def list_comments(self, number):
            return self.__transport.list_comments(number)

    frozen = dict(digests)
    if negative_stale:
        frozen["input"] = "sha256:" + "0" * 64
    observed = build_delp_source_bound_successor(
        graph, leaf_ref=ctx["source_bound_successor"]["leaf"],
        provider=ReadOnlyProvider(), frozen_basis=frozen,
    )
    if negative_stale:
        require(observed["currentness"] == "RECONCILE_REQUIRED"
                and "input" in observed["moved_axes"],
                "COLD_FROZEN_NEGATIVE_DID_NOT_RECONCILE")
        print("COLD_LIVE_NEGATIVE_STALE_INPUT_REJECTED=PASS")
        return
    require(observed["currentness"] == "CURRENT_READ_ONLY"
            and observed["digests"] == digests,
            "COLD_LIVE_SOURCE_MOVED_RECONCILE_REQUIRED")
    for key in ("leaf", "repository", "root", "responsibility", "claim_ids"):
        require(observed.get(key) == ctx["source_bound_successor"].get(key),
                "COLD_LIVE_GRAPH_BINDING_MISMATCH:" + key)
    require(observed["owner_source_status"] == "UNRESOLVED_CHAT_MESSAGE_LINK"
            and observed["execution_admission"] == "NEVER_FROM_RECONSTRUCTION"
            and observed["owner_merge_authority"] == "NOT_GRANTED",
            "COLD_LIVE_AUTHORITY_ESCALATION")
    print("COLD_LIVE_GITHUB_SOURCE_REPLAY=PASS_CURRENT_READ_ONLY")
    print("COLD_OWNER_CHAT_SOURCE=UNKNOWN")
    print("COLD_REVIEWER_OR_MERGE_AUTHORITY=NOT_GRANTED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--live", action="store_true")
    modes.add_argument("--local-only", action="store_true")
    parser.add_argument("--negative-stale", action="store_true")
    args = parser.parse_args()
    # Check two files remain unchanged even when replayed with live transport.
    folder = Path(args.bundle).resolve()
    before = {name: (folder / name).read_bytes() for name in
              ("HANDOVER_CONTEXT.yaml", "EVENTS.jsonl")}
    replay(folder, args.live, args.negative_stale)
    require(all((folder / name).read_bytes() == before[name] for name in before),
            "COLD_REPLAY_MUTATED_DURABLE_HANDOVER")


if __name__ == "__main__":
    main()
