"""R2-D: cold GitHub-only parent/leaf/PR entry to one governed read-only state.

Mutable issue/PR prose is only a route HINT, not approval. The sole graph
authority is a native GitHub OWNER selection comment on the root, verified
with integration_graph_authority_v35 against immutable source bytes.
No absent approval is ever replaced by a historical golden or caller digest.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import json
import re
from collections.abc import Mapping
from typing import Any

import delp_projection_v35 as DELP
import integration_graph_authority_v35 as GRAPH
import integration_read_model_v35 as MODEL

_URL = re.compile(r"^https://github\.com/([^/#]+)/([^/#]+)/(issues|pull)/([1-9][0-9]*)$")
_PARENT = re.compile(r"(?im)^\s*Parent programme:\s*(?:[a-zA-Z0-9_.-]+\s*)?#([1-9][0-9]*)")
_PR_PARENT = re.compile(r"(?i)\bprogramme\s*#([1-9][0-9]*)\b")
_PR_LEAF = re.compile(r"(?i)\bP[0-9]+(?:[.][0-9]+)?\s*#([1-9][0-9]*)\b")
_ROOT_MARKER = "<!-- V35_PARENT_OWNER_INTENT_BEGIN -->"


class ColdEntryError(ValueError):
    """Entry identity/provenance ambiguous or foreign, never implicitly accepted."""


def _single_int(text: str, regex: re.Pattern[str], label: str) -> int:
    ids = {int(x) for x in regex.findall(text)}
    if len(ids) != 1:
        raise ColdEntryError(f"{label}: no unique provider document route hint")
    return ids.pop()


def _input_route(transport: Any, entry_url: str) -> dict[str, Any]:
    match = _URL.fullmatch(str(entry_url or ""))
    repo = getattr(transport, "repository", None)
    if not match or not isinstance(repo, str) or repo.casefold() != (
        f"{match.group(1)}/{match.group(2)}".casefold()
    ):
        raise ColdEntryError("entry URL is foreign, unsupported or not repository bound")
    kind, n = match.group(3), int(match.group(4))
    if kind == "issues":
        observed = transport.get_issue(n)
        if not isinstance(observed, Mapping) or observed.get("number") != n:
            raise ColdEntryError("provider issue number changed or missing")
        text = str(observed.get("body") or "")
        if _ROOT_MARKER in text:
            if _PARENT.search(text):
                raise ColdEntryError("root and leaf identity markers contradict")
            return {"root_number": n, "entry_kind": "PARENT", "entry_number": n,
                    "leaf_number": None, "pr_number": None}
        root_number = _single_int(text, _PARENT, "child parent")
        if root_number == n:
            raise ColdEntryError("leaf points to itself as parent")
        return {"root_number": root_number, "entry_kind": "CHILD", "entry_number": n,
                "leaf_number": n, "pr_number": None}
    pull = transport.get_pull(n)
    if not isinstance(pull, Mapping) or pull.get("number") != n:
        raise ColdEntryError("provider PR number changed or missing")
    base = (pull.get("base") or {}).get("repo") or {}
    if str(base.get("full_name") or "").casefold() != repo.casefold():
        raise ColdEntryError("provider PR belongs to a foreign repository")
    text = str(pull.get("body") or "")
    root = _single_int(text, _PR_PARENT, "PR programme")
    leaf = _single_int(text, _PR_LEAF, "PR responsibility")
    if leaf == root:
        raise ColdEntryError("PR responsibility cannot be root")
    return {"root_number": root, "entry_kind": "PR", "entry_number": n,
            "leaf_number": leaf, "pr_number": n}


def _typed_approval_comments(transport: Any, root: int) -> list[Mapping[str, Any]]:
    values = transport.list_comments(root)
    if not isinstance(values, list):
        raise ColdEntryError("native GitHub comments unavailable or incomplete")
    matching = [c for c in values if isinstance(c, Mapping) and
                GRAPH.APPROVAL_START in str(c.get("body") or "")]
    if len(matching) > 1:
        raise ColdEntryError("multiple graph-selection comments: ambiguous, fail closed")
    return matching


def reconstruct(transport: Any, entry_url: str) -> dict[str, Any]:
    """Discover approved current graph from a cold entry, or explicit HOLD.

    Return value is a read-only advisory. It has *no* permission to execute
    a subsequent GitHub write, even if an OWNER graph comment exists.
    """
    route = _input_route(transport, entry_url)
    repo = transport.repository
    root_number = route["root_number"]
    parent = transport.get_issue(root_number)
    if not isinstance(parent, Mapping) or parent.get("number") != root_number:
        raise ColdEntryError("provider programme root unavailable or changed")
    if _ROOT_MARKER not in str(parent.get("body") or ""):
        raise ColdEntryError("candidate parent is not the governed programme root")
    approvals = _typed_approval_comments(transport, root_number)
    root_ref = f"{repo.split('/')[-1]}#{root_number}"
    common = {
        "schema": "V35_COLD_ENTRY_READINESS_V1",
        "repository": repo,
        "root": root_ref,
        "programme_root_issue": root_number,
        "provider_read_only": True,
        "local_merge_authority": "NOT_DERIVED",
        "native_custody": "SOURCE_NOT_PROVEN",
        "programme_ic_credit": "NOT_DERIVED",
        "event_workflow_activation": "NOT_AUTHORIZED",
    }
    if not approvals:
        return dict(common,
            status="HOLD_NO_PROVIDER_APPROVED_GRAPH",
            graph_source="NOT_PRESENT_IN_GOVERNING_ROOT_COMMENTS",
            selected_leaf="UNKNOWN_UNTIL_APPROVED_GRAPH",
            approved_pr="UNKNOWN_UNTIL_APPROVED_GRAPH",
            actual_next="OWNER_PUBLISH_APPROVED_GRAPH_SELECTION_THEN_REPLAY",
            owner_original_source="UNPROVEN",
            evidence_currentness="NOT_EVALUATED_WITHOUT_GRAPH",
            description="Identical root-level blocker from parent, child or PR entry; routes are hints only.",
        )
    comment = approvals[0]
    body = str(comment.get("body") or "")
    try:
        obj = GRAPH._approval_object(comment)
    except GRAPH.GraphSelectionError as exc:
        raise ColdEntryError(f"invalid or incomplete root graph comment: {exc}") from exc
    selected_leaf = str(obj.get("responsibility_ref") or "")
    pr_number = obj.get("pr_number")
    if not selected_leaf or type(pr_number) is not int or pr_number < 1:
        raise ColdEntryError("root graph approval has no unique selected responsibility/PR")
    if route["leaf_number"] is not None and selected_leaf != (
        f"{repo.split('/')[-1]}#{route['leaf_number']}"
    ):
        raise ColdEntryError("cold entry leaf disagrees with provider graph selection")
    if route["pr_number"] is not None and route["pr_number"] != pr_number:
        raise ColdEntryError("cold entry PR disagrees with provider graph selection")
    comment_url = comment.get("html_url")
    if not isinstance(comment_url, str) or not comment_url:
        raise ColdEntryError("root approval comment provider permalink missing")
    try:
        selected = GRAPH.load_approved_source(
            transport, comment_url,
            selected_responsibility=selected_leaf, selected_pr=pr_number,
            expected_programme_root=root_ref,
        )
    except (GRAPH.GraphSelectionError, DELP.DelpError) as exc:
        raise ColdEntryError(f"provider-approved graph failed source verification: {exc}") from exc
    model = MODEL.from_provider(
        selected["graph"], selected_leaf, transport,
        owner_origin=selected["owner_origin"]
    )
    if selected["graph_digest"] != model["source_identity"]["graph_digest"]:
        raise ColdEntryError("DELP read-model digest differs from provider selected graph")
    if model["candidate_sha"] != (
        transport.get_pull(pr_number).get("head") or {}
    ).get("sha"):
        raise ColdEntryError("selected PR candidate changed during cold projection")
    core = {
        "graph_digest": selected["graph_digest"],
        "approved_source_ref": selected["approval_ref"],
        "approved_graph_commit": selected["graph_commit_sha"],
        "selected_leaf": selected_leaf,
        "approved_pr": pr_number,
        "exact_head": model["candidate_sha"],
        "basis_sha256": model["basis_sha256"],
        "progress": model["progress"],
        "actual_next": model["actual_next"],
        "accepted_evidence_sources": model["accepted_evidence_sources"],
        "owner_original_source": selected["original_chat_source"],
    }
    core["snapshot_digest"] = hashlib.sha256(json.dumps(
        core, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    return dict(common,
        status="GOVERNED_GRAPH_PROVIDER_OBSERVED_READ_ONLY",
        graph_source="OWNER_APPROVED_IMMUTABLE_GITHUB_SOURCE",
        **core,
    )


def main(argv: list[str] | None = None) -> int:
    """Cold provider check; exit 3 for unapproved source, 2 for invalid source."""
    parser = argparse.ArgumentParser(description="Read-only V3.5 root/leaf/PR cold source replay")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--entry-url", required=True)
    args = parser.parse_args(argv)
    try:
        # Only transport, not the write function. The read-only path never
        # calls GitHubStore, patch_pull, patch_title or post_comment.
        import integration_scoreboard_publish_v35 as SCOREBOARD
        transport = SCOREBOARD.ScoreboardTransport(args.repository)
        result = reconstruct(transport, args.entry_url)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0 if result["status"] == "GOVERNED_GRAPH_PROVIDER_OBSERVED_READ_ONLY" else 3
    except (ColdEntryError, GRAPH.GraphSelectionError, DELP.DelpError,
            MODEL.ReadModelError, OSError, ValueError) as exc:
        print(f"V3.5 cold-source replay denied: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
