"""R6: three *independent* GitHub-entry readbacks, source-bound equality oracle.

"Independent reads" means separate provider invocations, NOT independent
human reviewers or distinct principals. Real Agent-6 acceptance remains a
different-principal review, and missing Owner source remains HOLD.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from typing import Any

import integration_cold_entry_v35 as COLD
import integration_relay_consumers_v35 as R5
import integration_scoreboard_publish_v35 as PUBLISH


class ColdReplayError(ValueError):
    """Root/leaf/PR provider sources differ; never promote partial agreement."""


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")).hexdigest()


def _unique_routes(transport: Any, urls: tuple[str, str, str]) -> dict[str, str]:
    if len(urls) != 3 or len(set(urls)) != 3:
        raise ColdReplayError("exactly three distinct native GitHub entry URLs required")
    routes: dict[str, str] = {}
    for url in urls:
        try:
            route = COLD._input_route(transport, url)
        except COLD.ColdEntryError as exc:
            raise ColdReplayError(f"invalid native provider entry route: {exc}") from exc
        kind = route["entry_kind"]
        if kind in routes:
            raise ColdReplayError("duplicate entry kind, need PARENT, CHILD, PR")
        routes[kind] = url
    if set(routes) != {"PARENT", "CHILD", "PR"}:
        raise ColdReplayError("a complete parent/child/PR native entry set is required")
    return routes


def replay(transport: Any, entries: tuple[str, str, str]) -> dict[str, Any]:
    """One native GitHub provider, three independent R2-D/R5 reads + final root.

    Does not accept a precomputed snapshot, cached approvals, injected graph,
    reviewer verdict, task evidence or caller-authored candidate SHA.
    """
    routes = _unique_routes(transport, entries)
    root, child, pr = routes["PARENT"], routes["CHILD"], routes["PR"]
    pr_match = re.search(r"/pull/([1-9][0-9]*)$", pr)
    if not pr_match:
        raise ColdReplayError("PR entry has no provider number")
    pr_number = int(pr_match.group(1))
    initial = transport.get_pull(pr_number)
    start_sha = (initial.get("head") or {}).get("sha")
    if not isinstance(start_sha, str) or not re.fullmatch(r"[a-f0-9]{40}", start_sha):
        raise ColdReplayError("first PR provider head unavailable")
    readbacks: list[tuple[str, dict[str, Any]]] = []
    try:
        for label, url in (("PARENT", root), ("CHILD", child), ("PR", pr)):
            view = R5.from_provider(transport, url)
            readbacks.append((label, view))
        fresh = R5.from_provider(transport, root)  # drift fence: not a cached read
    except (COLD.ColdEntryError, R5.RelayConsumerError) as exc:
        raise ColdReplayError(f"cold source readback failed closed: {exc}") from exc
    last = transport.get_pull(pr_number)
    last_sha = (last.get("head") or {}).get("sha")
    if last_sha != start_sha:
        raise ColdReplayError("PR head drifted during independent cold reads")
    first = readbacks[0][1]
    for label, view in readbacks[1:] + [("PARENT_REPEAT", fresh)]:
        if view != first:
            raise ColdReplayError(
                f"provider source/read model drift between cold entries: {label}"
            )
    if first["state"]["root"] != (
        f"{transport.repository.split('/')[-1]}#{COLD._input_route(transport, root)['root_number']}"
    ):
        raise ColdReplayError("root report identity disagrees with native route")
    surfaces = first["surfaces"]
    if set(surfaces) != set(R5.SURFACES):
        raise ColdReplayError("incomplete relay surface set")
    if first["approval_status"] == "HOLD_NO_APPROVED_GRAPH":
        decision = "REPLAY_HOLD_OBSERVED_NO_OWNER_APPROVAL"
        exit_status = 3
    elif first["approval_status"] == "SOURCE_READ_ONLY_ACCEPTANCE_NOT_DERIVED":
        if first["state"].get("exact_head") != start_sha:
            raise ColdReplayError("DELP candidate head differs from native PR")
        decision = "REPLAY_SOURCE_BOUND_NOT_PROGRAMME_ACCEPTED"
        exit_status = 0
    else:
        raise ColdReplayError("unsupported source readiness state")
    return {
        "schema": "V35_THREE_ENTRY_PROVIDER_REPLAY_V1",
        "decision": decision,
        "exit_status": exit_status,
        "repository": transport.repository,
        "root": first["state"]["root"],
        "provider_pr_head": start_sha,
        "readback_count": 4,
        "entry_kinds": ["PARENT", "CHILD", "PR", "PARENT_REPEAT"],
        "basis": first["source_basis"],
        "report_digest": first["relay_report_sha256"],
        "all_nine_surfaces_digest": _hash(surfaces),
        "outputs_compared": list(R5.SURFACES),
        "actual_next": first["state"]["actual_next"],
        "provider_approved_source": first["approval_status"],
        "task_evidence_published": "NOT_DERIVED",
        "independent_reviewer_principal": "NOT_OBSERVED",
        "native_custody": "SOURCE_NOT_PROVEN",
        "programme_ic_credit": "NONE",
        "live_writer_activation": "NOT_GRANTED",
        "qualification": "MECHANICAL_THREE_ENTRY_REPLAY_ONLY",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R6 3-entry native GitHub read-only stress")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--parent-url", required=True)
    parser.add_argument("--child-url", required=True)
    parser.add_argument("--pr-url", required=True)
    args = parser.parse_args(argv)
    try:
        result = replay(
            PUBLISH.ScoreboardTransport(args.repository),
            (args.parent_url, args.child_url, args.pr_url),
        )
        print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
        return result["exit_status"]
    except (ColdReplayError, OSError, ValueError) as exc:
        print(f"V3.5 3-entry replay REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
