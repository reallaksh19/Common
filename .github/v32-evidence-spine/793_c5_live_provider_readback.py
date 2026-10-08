#!/usr/bin/env python3
"""C5 native GitHub read-only ESC-4 cold successor challenge.

This is an *implementation* source check, not an independent reviewer verdict.
It must fail closed when real GitHub cannot be re-read and never submits writes.
"""
from __future__ import annotations

import base64
import copy
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import delp_projection_v32 as delp  # noqa: E402
from handover_context import (  # noqa: E402
    HandoverContextError,
    build_delp_source_bound_successor,
)

ORACLE_PATH = Path(__file__).with_name("793-c5-live-provider-golden.json")
REPO = "reallaksh19/Common"


class ReadOnlyGh:
    """Permit the small GET-only DELP provider contract, not GhTransport writers."""

    def __init__(self) -> None:
        self._transport = delp.GhTransport(REPO)

    def get_commit_sha(self, ref):
        return self._transport.get_commit_sha(ref)

    def get_issue(self, number):
        return self._transport.get_issue(number)

    def get_pull(self, number):
        return self._transport.get_pull(number)

    def list_comments(self, number):
        return self._transport.list_comments(number)

    def compare(self, base, head):
        return self._transport.compare(base, head)


def read_pinned_graph(sha: str) -> dict:
    if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha):
        raise RuntimeError("C5_INVALID_RELEASED_GRAPH_HEAD")
    endpoint = (
        f"repos/{REPO}/contents/.github/v32-evidence-spine/"
        f"718-proposal-v2.json?ref={sha}"
    )
    result = subprocess.run(
        ["gh", "api", "--method", "GET", endpoint],
        capture_output=True, text=True, check=True, timeout=45,
    )
    response = json.loads(result.stdout)
    if response.get("type") != "file" or response.get("encoding") != "base64":
        raise RuntimeError("C5_GRAPH_NOT_CANONICAL_GITHUB_BLOB")
    data = base64.b64decode(response["content"])
    return json.loads(data)


def require(actual, wanted, case: str):
    if actual != wanted:
        raise AssertionError(f"{case}: expected {wanted!r}, observed {actual!r}")


def main() -> None:
    if not os.environ.get("GH_TOKEN") and not os.environ.get("GITHUB_TOKEN"):
        raise RuntimeError("C5_AUTHENTICATED_GITHUB_TOKEN_REQUIRED")
    require(os.environ.get("GITHUB_REPOSITORY"), REPO, "C5_REPOSITORY_SCOPE")
    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    require(oracle["schema"], "v32-793-c5-real-provider-cold-replay-v1", "C5_ORACLE_SCHEMA")
    require([c["id"] for c in oracle["cases"]],
            [f"LIVE-{i:02d}" for i in range(1, 7)], "C5_ORACLE_CASE_INVENTORY")
    graph = read_pinned_graph(oracle["exact_released_graph_sha"])
    leaf = next(n for n in graph["nodes"] if n.get("ref") == oracle["leaf"])
    require(leaf.get("primary_pr"), oracle["expected_graph_material"], "LIVE-01_MATERIAL_ID")
    require(leaf.get("owns_claims"), [oracle["expected_claim"]], "LIVE-01_CLAIM")
    provider = ReadOnlyGh()
    actual_pull = provider.get_pull(oracle["product_pr"])
    sha = actual_pull["head"]["sha"]
    # The previous C5 passed on whatever live #800 head happened to be
    # returned, even when the fixture named a different reviewed source.
    # A true exact-head replay must bind both the golden and the provider.
    require(sha, oracle["exact_product_code_base"], "LIVE-00_EXACT_C4_PRODUCT_HEAD")

    basis = build_delp_source_bound_successor(graph, leaf_ref=oracle["leaf"], provider=provider)
    actual_observation = delp.observe_github(provider, graph)[oracle["leaf"]]
    require(actual_observation["candidate_sha"], sha, "LIVE-01_PROVIDER_SHA")
    require(basis["leaf"], oracle["leaf"], "LIVE-01_LEAF")
    require(basis["currentness"], "CURRENT_READ_ONLY", "LIVE-01_FRESH_BASIS")
    require(basis["claim_ids"], [oracle["expected_claim"]], "LIVE-01_CLAIM_BASIS")
    require(basis["owner_merge_authority"], "NOT_GRANTED", "LIVE-01_MERGE_AUTHORITY")
    require(basis["authority_effects"], [], "LIVE-01_AUTHORITY")
    print("LIVE-01=PASS SOURCE_PR_HEAD_RECONCILED NO_ACCEPTANCE")

    replay = build_delp_source_bound_successor(
        graph, leaf_ref=oracle["leaf"], provider=provider, frozen_basis=basis["digests"]
    )
    require(replay["currentness"], "CURRENT_READ_ONLY", "LIVE-02_SAME_FROZEN_BASIS")
    require(replay["moved_axes"], [], "LIVE-02_NO_DRIFT")
    print("LIVE-02=PASS REAL_PROVIDER_REPLAY")

    stale = dict(basis["digests"])
    stale["input"] = "sha256:" + "0" * 64
    changed = build_delp_source_bound_successor(
        graph, leaf_ref=oracle["leaf"], provider=provider, frozen_basis=stale
    )
    require(changed["currentness"], "RECONCILE_REQUIRED", "LIVE-03_STALE_FROZEN")
    if "input" not in changed["moved_axes"]:
        raise AssertionError("LIVE-03_INPUT_DRIFT_NOT_RECORDED")
    print("LIVE-03=PASS STALE_INPUT_RECONCILE")

    wrong = copy.deepcopy(graph)
    wrong_leaf = next(n for n in wrong["nodes"] if n["ref"] == oracle["leaf"])
    wrong_leaf["owns_claims"] = ["ESC-5"]
    try:
        build_delp_source_bound_successor(wrong, leaf_ref=oracle["leaf"], provider=provider)
    except HandoverContextError:
        pass
    else:
        raise AssertionError("LIVE-04_CHANGED_CLAIM_ACCEPTED")
    print("LIVE-04=PASS CHANGED_PLAN_REJECTED")

    class SpoofedProduct(ReadOnlyGh):
        def get_pull(self, number):
            data = copy.deepcopy(super().get_pull(number))
            if number == oracle["product_pr"]:
                data["head"]["sha"] = "0" * 40 if sha != "0" * 40 else "f" * 40
            return data

    spoofed = build_delp_source_bound_successor(
        graph, leaf_ref=oracle["leaf"], provider=SpoofedProduct(),
        frozen_basis=basis["digests"],
    )
    require(spoofed["currentness"], "RECONCILE_REQUIRED", "LIVE-05_CANDIDATE_DRIFT")
    if "input" not in spoofed["moved_axes"]:
        raise AssertionError("LIVE-05_INPUT_DIGEST_DID_NOT_MOVE")
    print("LIVE-05=PASS PROVIDER_HEAD_SPOOF_DETECTED_AGAINST_FROZEN_BASIS")

    require(replay["owner_source_status"], "UNRESOLVED_CHAT_MESSAGE_LINK",
            "LIVE-06_ORIGINAL_OWNER_MESSAGE_UNKNOWN")
    require(replay["execution_admission"], "NEVER_FROM_RECONSTRUCTION", "LIVE-06_EXECUTION")
    require(replay["owner_merge_authority"], "NOT_GRANTED", "LIVE-06_MERGE")
    if replay["authority_effects"]:
        raise AssertionError("LIVE-06_ILLEGAL_AUTHORITY_EFFECT")
    print("LIVE-06=PASS NO_OWNER_OR_CUSTODY_AUTHORITY")
    print("C5_NATIVE_GITHUB_SOURCE_READBACK=PASS_SIX_CASES_NOT_INDEPENDENT_ACCEPTANCE")
    print("C5_PRODUCT_HEAD_OBSERVED=" + sha)
    print("C5_RECONSTRUCTION_CURRENTNESS=CURRENT_READ_ONLY_NOT_APPROVED")


if __name__ == "__main__":
    main()
