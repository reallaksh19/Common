"""R2-C: approved graph selection from provider-authenticated GitHub source.

A caller cannot assert both the plan and its own "approved" digest. A typed,
OWNER-authored issue comment must select an immutable Git commit/path/graph
digest, root, responsibility, generation, PR and Owner intent receipt.
This is a read gate for a scoreboard, NEVER a native Local/custody/merge grant.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any

import delp_projection_v35 as DELP
import integration_source_authority_v35 as SOURCE

APPROVAL_START = "<!-- V35_GRAPH_SELECTION_APPROVAL_V1_BEGIN -->"
APPROVAL_END = "<!-- V35_GRAPH_SELECTION_APPROVAL_V1_END -->"
SCOPE = "READ_MODEL_AND_ISSUE_PR_SCOREBOARD_ONLY"
URL = re.compile(
    r"^https://github\.com/([^/#]+)/([^/#]+)/issues/([1-9][0-9]*)#issuecomment-([1-9][0-9]*)$"
)
SHA = re.compile(r"^[a-f0-9]{40}$")


class GraphSelectionError(ValueError):
    """Graph cannot be authenticated against a stable Owner-selected source."""


def _approval_object(comment: Mapping[str, Any]) -> Mapping[str, Any]:
    body = str(comment.get("body") or "")
    if body.count(APPROVAL_START) != 1 or body.count(APPROVAL_END) != 1:
        raise GraphSelectionError("one complete typed graph selection block required")
    if body.index(APPROVAL_START) >= body.index(APPROVAL_END):
        raise GraphSelectionError("approval delimiters in wrong order")
    raw = body.split(APPROVAL_START, 1)[1].split(APPROVAL_END, 1)[0].strip()
    try:
        obj = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise GraphSelectionError("approval block is not JSON") from exc
    if not isinstance(obj, Mapping):
        raise GraphSelectionError("approval body must be a typed mapping")
    return obj


def _graph_path(path: Any) -> str:
    if not isinstance(path, str) or not path.strip() or path.startswith("/"):
        raise GraphSelectionError("approved graph file path missing")
    if any(part in ("", ".", "..", ".git") for part in path.split("/")):
        raise GraphSelectionError("approved graph file path traversal or invalid component")
    if not path.endswith(".json"):
        raise GraphSelectionError("approved graph must be canonical JSON")
    return path


def load_approved_source(
    transport: Any,
    approval_ref: str,
    *,
    selected_responsibility: str,
    selected_pr: int,
    expected_programme_root: str | None = None,
) -> dict[str, Any]:
    """Use ONLY graph bytes returned by provider at immutable approved git ref.

    Operator supplies desired leaf/PR, but not which graph or digest to trust.
    Approval lives in a GitHub native issue comment from repository OWNER;
    original Owner chat remains unverifiable when its first mirror is GitHub.
    """
    repo = getattr(transport, "repository", None)
    if not isinstance(repo, str) or not repo.strip():
        raise GraphSelectionError("GitHub provider repository identity missing")
    match = URL.fullmatch(str(approval_ref or ""))
    if not match or f"{match.group(1)}/{match.group(2)}".casefold() != repo.casefold():
        raise GraphSelectionError("graph approval permalink not in current repository")
    approval_issue = int(match.group(3))
    comment = transport.get_issue_comment(int(match.group(4)))
    if not isinstance(comment, Mapping):
        raise GraphSelectionError("graph approval provider record unavailable")
    if comment.get("html_url") != approval_ref or comment.get("issue_url") != (
        f"https://api.github.com/repos/{repo}/issues/{approval_issue}"
    ):
        raise GraphSelectionError("graph approval URL or issue identity mismatch")
    if comment.get("author_association") != "OWNER" or not str(
        (comment.get("user") or {}).get("login") or ""
    ):
        raise GraphSelectionError("graph approval not authored by repository OWNER")
    issue = transport.get_issue(approval_issue)
    if not isinstance(issue, Mapping) or issue.get("number") != approval_issue:
        raise GraphSelectionError("governing graph issue provider mismatch")
    data = _approval_object(comment)
    required = {
        "schema": "V35_GRAPH_SELECTION_APPROVAL_V1",
        "scope": SCOPE,
        "repository": repo,
        "root": expected_programme_root or data.get("root"),
        "responsibility_ref": selected_responsibility,
        "pr_number": selected_pr,
        "approval_issue": approval_issue,
        "revoked": False,
        "native_custody_granted": False,
        "local_merge_authorized": False,
        "original_chat_authenticated": False,
    }
    if any(data.get(key) != value for key, value in required.items()):
        raise GraphSelectionError("approved graph scope/identity/revocation/authority mismatch")
    commit = data.get("graph_commit_sha")
    if not isinstance(commit, str) or not SHA.fullmatch(commit):
        raise GraphSelectionError("graph source requires immutable 40-char commit SHA")
    graph_file = _graph_path(data.get("graph_path"))
    payload = transport.get_file_at(commit, graph_file)
    if not isinstance(payload, Mapping) or not isinstance(payload.get("content"), str):
        raise GraphSelectionError("immutable graph source file unavailable")
    raw = payload["content"]
    observed_digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if data.get("graph_file_sha256") != observed_digest:
        raise GraphSelectionError("approved immutable graph byte digest mismatch")
    try:
        graph = json.loads(raw)
    except ValueError as exc:
        raise GraphSelectionError("immutable graph file is invalid JSON") from exc
    DELP.require_repository_match(graph, repo, live=True)
    index = DELP.validate_graph(graph)
    if data.get("root") != index["root"]:
        raise GraphSelectionError("approved graph root differs from actual graph")
    if data.get("graph_digest") != index["digest"]:
        raise GraphSelectionError("approved DELP canonical graph digest mismatch")
    if data.get("graph_generation") != index["programme"]["graph_generation"]:
        raise GraphSelectionError("approved graph generation is stale/foreign")
    leaf = index["nodes"].get(selected_responsibility)
    if not leaf or leaf["kind"] != "LEAF":
        raise GraphSelectionError("approved graph excludes selected leaf")
    if not leaf.get("primary_pr") or DELP.ref_number(leaf["primary_pr"]) != selected_pr:
        raise GraphSelectionError("approved graph excludes declared selected PR")
    if data.get("spec_generation") != leaf.get("spec_generation"):
        raise GraphSelectionError("approved source spec generation mismatch")
    owner = data.get("owner_origin")
    claim_issue = data.get("owner_claim_issue")
    if type(claim_issue) is not int or claim_issue < 1:
        raise GraphSelectionError("owner claim issue source binding absent")
    verified_mirror = SOURCE.verify_owner_mirror(
        transport, repo, owner, claim_issue=claim_issue
    )
    # A published mutable comment can be edited/revoked. Its latest provider
    # version MUST be observed again immediately before an actual write.
    return {
        "schema": "V35_GRAPH_SELECTED_SOURCE_V1",
        "graph": graph,
        "graph_digest": index["digest"],
        "graph_commit_sha": commit,
        "graph_path": graph_file,
        "graph_file_sha256": observed_digest,
        "root": index["root"],
        "responsibility_ref": selected_responsibility,
        "pr_number": selected_pr,
        "owner_origin": dict(owner),
        "owner_mirror": verified_mirror,
        "approval_ref": approval_ref,
        "approval_comment_updated_at": comment.get("updated_at"),
        "approval_author": str((comment.get("user") or {}).get("login") or ""),
        "scope": SCOPE,
        "live_workflow_permission": "NOT_GRANTED_BY_SOURCE_APPROVAL",
        "custody": "NOT_GRANTED",
        "merge_authority": "NOT_GRANTED",
        "original_chat_source": "UNPROVEN",
    }
