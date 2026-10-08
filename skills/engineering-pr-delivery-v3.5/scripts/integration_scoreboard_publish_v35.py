#!/usr/bin/env python3
"""R4: guarded, rerunnable GitHub issue/PR smart scoreboard publisher.

Uses DELP.sync_projection/GitHubStore as the sole issue LIVE_STATUS writer,
and writes one owned section in the linked PR. GitHub has NO atomic conditional
PATCH for issue title/comment/PR title/body: detect/retry/readback is best-effort,
not a distributed transaction or a guarantee against last-millisecond races.
There is deliberately no default approved graph or background event automation.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Mapping

import delp_projection_v35 as DELP
import integration_read_model_v35 as R2
import integration_scoreboard_v35 as R3
import integration_scoreboard_events_v35 as EVENTS


class PublishError(ValueError):
    """A source/currentness/managed-text conflict prevents unsafe publication."""


class ScoreboardTransport(DELP.GhTransport):
    """Thin GitHub API extension; DELP remains the issue status authority."""

    def get_check_runs(self, head_sha: str) -> dict[str, Any]:
        # Explicit count+full retrieval prevents false CI PASS on paginated results.
        payload = self._gh(
            "--method", "GET",
            f"repos/{self.repository}/commits/{head_sha}/check-runs",
            "-f", "per_page=100",
        )
        if not isinstance(payload, dict):
            raise PublishError("unexpected GitHub check-runs API response")
        return payload

    def get_issue_comment(self, comment_id: int) -> dict[str, Any]:
        return self._gh(f"repos/{self.repository}/issues/comments/{comment_id}")

    def patch_pull(self, number: int, *, title: str, body: str) -> dict[str, Any]:
        return self._gh(
            "--method", "PATCH", f"repos/{self.repository}/pulls/{number}",
            "-f", f"title={title}", "-f", f"body={body}",
        )


def _check_binding(indexed: Mapping[str, Any], ref: str, expected_pr: int) -> None:
    node = indexed["nodes"].get(ref)
    if node is None or node.get("kind") != "LEAF":
        raise PublishError("responsibility is not an approved graph LEAF")
    declared = node.get("primary_pr")
    if not declared or DELP.ref_number(declared) != expected_pr:
        raise PublishError("requested PR is not the responsibility's declared primary PR")


_APPROVAL_START = "<!-- V35_SCOREBOARD_APPROVAL_V1_BEGIN -->"
_APPROVAL_END = "<!-- V35_SCOREBOARD_APPROVAL_V1_END -->"


def _approved_for_write(
    transport: Any,
    indexed: Mapping[str, Any],
    responsibility_ref: str,
    expected_pr: int,
    expected_graph_digest: str | None,
    approval_ref: str | None,
) -> dict[str, Any]:
    """Fetch a provider-authored, scoped approval—not a caller-asserted permalink.

    The approved *graph itself* remains an upstream Owner/Coordinator selection.
    This verifies an external GitHub principal and graph binding; it does not
    authenticate original chat text or grant Local roles/custody/merge authority.
    """
    repo = str(indexed["programme"].get("repository") or "")
    if not expected_graph_digest or expected_graph_digest != indexed["digest"]:
        raise PublishError("write denied: expected approved graph digest absent or mismatched")
    trusted = indexed["programme"].get("scoreboard_approvers") or []
    if not isinstance(trusted, list) or not trusted or any(
        not isinstance(name, str) or not name.strip() for name in trusted
    ):
        raise PublishError("write denied: approved graph must list scoreboard_approvers")
    if not isinstance(approval_ref, str):
        raise PublishError("write denied: real scoped source-approval permalink required")
    url_re = re.compile(
        "^https://github\\.com/" + re.escape(repo) +
        "/issues/[0-9]+#issuecomment-([1-9][0-9]*)$"
    )
    match = url_re.fullmatch(approval_ref)
    if match is None:
        raise PublishError("write denied: scoped source-approval issue comment ref required")
    comment = transport.get_issue_comment(int(match.group(1)))
    if not isinstance(comment, Mapping) or comment.get("html_url") != approval_ref:
        raise PublishError("write denied: approval comment provider readback mismatch")
    author = str((comment.get("user") or {}).get("login") or "")
    if author not in trusted:
        raise PublishError("write denied: approval comment authored by unauthorized principal")
    body = str(comment.get("body") or "")
    if body.count(_APPROVAL_START) != 1 or body.count(_APPROVAL_END) != 1:
        raise PublishError("write denied: unique typed approval block missing")
    interior = body.split(_APPROVAL_START, 1)[1].split(_APPROVAL_END, 1)[0].strip()
    try:
        approved = json.loads(interior)
    except json.JSONDecodeError as exc:
        raise PublishError("write denied: approval block is not exact JSON") from exc
    required = {
        "schema": "V35_SCOREBOARD_APPROVAL_V1",
        "scope": "ISSUE_PR_SCOREBOARD_TITLE_AND_MANAGED_BODY_ONLY",
        "repository": repo,
        "root": indexed["root"],
        "responsibility_ref": responsibility_ref,
        "pr_number": expected_pr,
        "graph_digest": indexed["digest"],
        "revoked": False,
    }
    if not isinstance(approved, dict) or any(
        approved.get(key) != value for key, value in required.items()
    ):
        raise PublishError("write denied: approval scope/identity/graph mismatch or revoked")
    return {
        "approval_ref": approval_ref, "approval_author": author,
        "approved_graph_digest": indexed["digest"],
        "scope": required["scope"],
    }


def _read(
    transport: Any,
    graph: Mapping[str, Any],
    responsibility_ref: str,
    pr_number: int,
    owner_origin: Mapping[str, Any] | None,
    *,
    human_titles: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    model = R2.from_provider(
        graph, responsibility_ref, transport,
        human_titles=human_titles, owner_origin=owner_origin,
    )
    pull = transport.get_pull(pr_number)
    sha = (pull.get("head") or {}).get("sha")
    checks = transport.get_check_runs(sha) if sha else None
    rendered = R3.render(model, pull, checks)
    return model, pull, rendered


def plan(
    transport: Any,
    graph: Mapping[str, Any],
    responsibility_ref: str,
    pr_number: int,
    *,
    owner_origin: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """One provider-backed read, no mutation, no asserted review/IC authority."""
    DELP.require_repository_match(graph, transport.repository, live=True)
    indexed = DELP.validate_graph(graph)
    _check_binding(indexed, responsibility_ref, pr_number)
    titles = {
        ref: str(transport.get_issue(DELP.ref_number(ref)).get("title") or "")
        for ref in indexed["nodes"]
    }
    model, pull, rendered = _read(
        transport, graph, responsibility_ref, pr_number, owner_origin,
        human_titles=titles,
    )
    expected_body = R3.managed_body(str(pull.get("body") or ""), rendered["pr_managed_body"])
    issue_title_map = rendered["issue_titles"]
    return {
        "status": "DRY_RUN_NO_MUTATION",
        "basis_sha256": rendered["basis_sha256"],
        "graph_digest": model["source_identity"]["graph_digest"],
        "candidate_sha": rendered["candidate_sha"],
        "issue_titles": issue_title_map,
        "pr_title": rendered["pr_title"],
        "pr_body_would_change": expected_body != str(pull.get("body") or ""),
        "pr_title_would_change": rendered["pr_title"] != str(pull.get("title") or ""),
        "checks": rendered["checks"],
        "approval": "OPERATOR_SOURCE_RECEIPT_REQUIRED_FOR_APPLY",
        "integration_acceptance": "NOT_DERIVED",
    }


def _patch_pr(
    transport: Any,
    number: int,
    expected_candidate: str,
    renderer_input: Mapping[str, Any],
    *,
    max_attempts: int,
) -> dict[str, Any]:
    """Preserves latest human prose and verifies exact bytes after the patch."""
    for attempt in range(1, max_attempts + 1):
        before = transport.get_pull(number)
        if (before.get("head") or {}).get("sha") != expected_candidate:
            raise PublishError("PR head moved before write: reproject; no stale title publication")
        # Re-render against latest human title, safely stripping only our prefix.
        rendering = R3.render(renderer_input, before, transport.get_check_runs(expected_candidate))
        new_title = rendering["pr_title"]
        new_body = R3.managed_body(str(before.get("body") or ""), rendering["pr_managed_body"])
        if (before.get("title"), before.get("body") or "") == (new_title, new_body):
            return {"status": "UNCHANGED", "attempts": attempt}
        # Best-effort pre-write re-read; GitHub lacks an If-Match update API
        # for these fields, so any continuing race must be caught by readback.
        guard = transport.get_pull(number)
        if ((guard.get("head") or {}).get("sha") != expected_candidate):
            raise PublishError("PR candidate moved during publication")
        if (guard.get("title") or "", guard.get("body") or "") != (
            before.get("title") or "", before.get("body") or ""
        ):
            continue
        transport.patch_pull(number, title=new_title, body=new_body)
        after = transport.get_pull(number)
        if ((after.get("head") or {}).get("sha") != expected_candidate):
            raise PublishError("PR candidate moved during readback; abort and reproject")
        if (after.get("title"), after.get("body") or "") == (new_title, new_body):
            return {"status": "WRITTEN_READBACK_VERIFIED", "attempts": attempt}
    raise PublishError("concurrent PR edit prevented stable managed publication")


def publish(
    transport: Any,
    graph: Mapping[str, Any],
    responsibility_ref: str,
    pr_number: int,
    *,
    owner_origin: Mapping[str, Any] | None = None,
    expected_graph_digest: str | None = None,
    approval_ref: str | None = None,
    max_attempts: int = 3,
) -> dict[str, Any]:
    """Guarded live one-time apply; fail closed; no cross-surface atomicity claim."""
    DELP.require_repository_match(graph, transport.repository, live=True)
    indexed = DELP.validate_graph(graph)
    _check_binding(indexed, responsibility_ref, pr_number)
    approval = _approved_for_write(
        transport, indexed, responsibility_ref, pr_number,
        expected_graph_digest, approval_ref,
    )
    if not 1 <= max_attempts <= 5:
        raise PublishError("bounded attempts must be 1..5")
    base_titles = {
        ref: str(transport.get_issue(DELP.ref_number(ref)).get("title") or "")
        for ref in indexed["nodes"]
    }
    model, _, rendered = _read(
        transport, graph, responsibility_ref, pr_number, owner_origin,
        human_titles=base_titles,
    )
    # One existing DELP issue LIVE_STATUS writer (leaves-first, CAS-like retry).
    issue_result = DELP.sync_projection(
        DELP.GitHubStore(transport), graph,
        lambda: DELP.ledger_from_github(transport, graph),
        lambda: DELP.observe_github(transport, graph),
        base_titles,
    )
    # Revalidate source head/facts/graph before touching the PR.
    following, _, _ = _read(
        transport, graph, responsibility_ref, pr_number, owner_origin,
        human_titles=base_titles,
    )
    if (model["source_identity"]["input_digest"] != following["source_identity"]["input_digest"]
        or model["basis_sha256"] != following["basis_sha256"]):
        raise PublishError(
            "provider/graph/facts changed during issue sync: PR withheld, retry entire cycle"
        )
    pr_result = _patch_pr(
        transport, pr_number, rendered["candidate_sha"], following,
        max_attempts=max_attempts,
    )
    return {
        "status": "APPLIED_NONATOMIC_READBACK_CHECKED",
        "basis_sha256": following["basis_sha256"],
        "candidate_sha": rendered["candidate_sha"],
        "issues": issue_result,
        "pr": pr_result,
        "provider_approval": approval,
        "warning": "GitHub has no atomic CAS across issue comments/titles and PR fields",
        "integration_acceptance": "NOT_DERIVED",
        "custody_and_merge_authority": "NOT_DERIVED",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Guarded DELP-backed GitHub issue/PR title sync")
    ap.add_argument("--graph", type=Path, required=True, help="Approved DELP execution graph JSON/YAML")
    ap.add_argument("--repository", required=True)
    ap.add_argument("--responsibility", required=True)
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--owner-origin", type=Path)
    ap.add_argument("--apply", action="store_true", help="MUTATES: requires graph digest + source approval receipt")
    ap.add_argument("--expected-graph-digest", help="Graph digest independently approved by Owner/Coordinator")
    ap.add_argument("--approval-ref", help="Scoped approved source comment permalink; operator must verify it")
    ap.add_argument("--event-name", help="GitHub event name; optional explicit event selection")
    ap.add_argument("--event-payload", type=Path, help="GitHub event JSON; never accepted as authority")
    ap.add_argument("--event-actor", help="GitHub actor for comment-loop suppression")
    args = ap.parse_args(argv)
    try:
        import yaml
        graph = yaml.safe_load(args.graph.read_text(encoding="utf-8"))
        origin = yaml.safe_load(args.owner_origin.read_text(encoding="utf-8")) if args.owner_origin else None
        transport = ScoreboardTransport(args.repository)
        if args.event_name or args.event_payload:
            if not (args.event_name and args.event_payload):
                raise PublishError("--event-name and --event-payload must be supplied together")
            selection = EVENTS.event_scope(
                graph, args.responsibility, args.pr, args.event_name,
                json.loads(args.event_payload.read_text(encoding="utf-8")),
                args.event_actor or os.environ.get("GITHUB_ACTOR"),
            )
            if selection["decision"] != "SELECT":
                print(json.dumps({"status": "EVENT_SKIPPED_NO_MUTATION", "selection": selection}))
                return 0
        if args.apply:
            result = publish(
                transport, graph, args.responsibility, args.pr,
                owner_origin=origin, expected_graph_digest=args.expected_graph_digest,
                approval_ref=args.approval_ref,
            )
        else:
            result = plan(transport, graph, args.responsibility, args.pr, owner_origin=origin)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except (DELP.DelpError, R2.ReadModelError, R3.ScoreboardError, EVENTS.EventError, PublishError, OSError, ValueError) as exc:
        print(f"V3.5 scoreboard sync rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
