"""R2-B: provider-read Owner mirror and governed DELP source preflight.

No scoring, GitHub mutation, native custody grant, review decision or original
chat source authentication. Integrity is distinct from authority: a digest
proves what was read, not who approved the source or the Local execution.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any

import delp_projection_v35 as DELP
import integration_read_model_v35 as R2


class SourceAuthorityError(ValueError):
    """Invalid source or scoped identifier. Never silently accept a substitute."""


_MIRROR = re.compile(
    r"^https://github\.com/([^/#]+)/([^/#]+)/issues/([1-9][0-9]*)#issuecomment-([1-9][0-9]*)$"
)


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=False,
        separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def _full_mirror_quote(body: str) -> str:
    """Keep the exact quoted words and internal blank lines from GitHub Markdown."""
    quoted = []
    for line in str(body or "").splitlines():
        if line.startswith("> "):
            quoted.append(line[2:])
        elif line == ">":
            quoted.append("")
        elif quoted and line.strip():
            # Later distinct blockquote is not a trusted continuation.
            break
    return "\n".join(quoted)


def verify_owner_mirror(
    transport: Any,
    repository: str,
    origin: Mapping[str, Any] | None,
    *,
    claim_issue: int,
) -> dict[str, Any]:
    """Read actual GitHub comment, ensure FULL quote, issue link and OWNER principal.

    GitHub OWNER is evidence of a repository-authored durable mirror, NEVER
    a proof of the original ChatGPT message or a native Local grant.
    """
    if not isinstance(origin, Mapping):
        raise SourceAuthorityError("owner source envelope unavailable")
    if origin.get("original_source_ref") is not None or origin.get("original_source_status") != "UNRESOLVED_CHAT_LINK":
        raise SourceAuthorityError("unverified original chat source must remain unresolved")
    text = origin.get("verbatim")
    if not isinstance(text, str) or not text.strip():
        raise SourceAuthorityError("verbatim Owner words required")
    url = origin.get("first_durable_mirror")
    match = _MIRROR.fullmatch(url) if isinstance(url, str) else None
    if not match or f"{match.group(1)}/{match.group(2)}".casefold() != repository.casefold():
        raise SourceAuthorityError("Owner mirror URL is not in the selected repository")
    if int(match.group(3)) != claim_issue:
        raise SourceAuthorityError("Owner mirror targets the wrong claim issue")
    expected_origin = f"https://github.com/{repository}/issues/{claim_issue}"
    if origin.get("claim_origin") != expected_origin:
        raise SourceAuthorityError("claim origin does not bind the source receipt issue")
    comment_id = int(match.group(4))
    try:
        comment = transport.get_issue_comment(comment_id)
    except (DELP.DelpError, KeyError, LookupError) as exc:
        raise SourceAuthorityError("Owner mirror provider lookup unavailable or missing") from exc
    if not isinstance(comment, Mapping) or comment.get("html_url") != url:
        raise SourceAuthorityError("provider comment permalink/readback mismatch")
    expected_api_issue = f"https://api.github.com/repos/{repository}/issues/{claim_issue}"
    if comment.get("issue_url") != expected_api_issue:
        raise SourceAuthorityError("provider receipt belongs to an unrelated issue")
    user = comment.get("user") or {}
    if not isinstance(user, Mapping) or not user.get("login") or comment.get("author_association") != "OWNER":
        raise SourceAuthorityError("provider receipt is not authenticated as repository OWNER")
    quoted = _full_mirror_quote(str(comment.get("body") or ""))
    if quoted != text:
        raise SourceAuthorityError("full Owner quotation differs from provider mirror")
    # Confirm the source issue exists with native provider, not merely a URL.
    issue = transport.get_issue(claim_issue)
    if not isinstance(issue, Mapping) or issue.get("number") != claim_issue:
        raise SourceAuthorityError("source issue provider identity mismatch")
    return {
        "status": "GITHUB_OWNER_MIRROR_VERIFIED_ORIGINAL_UNPROVEN",
        "first_durable_mirror": url,
        "original_source_status": "UNRESOLVED_CHAT_LINK",
        "source_comment_id": comment_id,
        "source_issue": claim_issue,
        "mirror_author": str(user["login"]),
        "verbatim_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "provider_comment_updated_at": comment.get("updated_at") or None,
    }


def assess(
    transport: Any,
    graph: Mapping[str, Any],
    responsibility_ref: str,
    pr_number: int,
    *,
    owner_origin: Mapping[str, Any] | None,
    claim_issue: int,
    independently_pinned_graph_digest: str | None,
) -> dict[str, Any]:
    """Source-level preflight on provider/graph/facts. READ ONLY.

    A submitted graph+digest from the same caller is NOT by itself proof that
    this is the approved programme. Caller must establish the digest against
    a separately trusted source before the later R2-C/R4 production gate.
    """
    repo = getattr(transport, "repository", None)
    if not isinstance(repo, str) or not repo.strip():
        raise SourceAuthorityError("authenticated provider repository identity unavailable")
    DELP.require_repository_match(graph, repo, live=True)
    indexed = DELP.validate_graph(graph)
    node = indexed["nodes"].get(responsibility_ref)
    if not node or node["kind"] != "LEAF":
        raise SourceAuthorityError("foreign or non-leaf responsibility")
    if not node.get("primary_pr") or DELP.ref_number(node["primary_pr"]) != pr_number:
        raise SourceAuthorityError("requested PR is not declared for selected leaf")
    if not isinstance(independently_pinned_graph_digest, str) or independently_pinned_graph_digest != indexed["digest"]:
        raise SourceAuthorityError("graph digest does not match independently expected value")
    owner = verify_owner_mirror(transport, repo, owner_origin, claim_issue=claim_issue)
    before = transport.get_pull(pr_number)
    if not isinstance(before, Mapping) or before.get("number") != pr_number:
        raise SourceAuthorityError("provider PR identity mismatch")
    if str((before.get("base") or {}).get("repo", {}).get("full_name") or "").casefold() != repo.casefold():
        raise SourceAuthorityError("candidate PR belongs to a different repository")
    initial_head = (before.get("head") or {}).get("sha")
    if not isinstance(initial_head, str) or not re.fullmatch(r"[0-9a-f]{40}", initial_head):
        raise SourceAuthorityError("provider PR candidate head unavailable")
    # Reuse actual DELP accepted evidence and observed provider material.
    model = R2.from_provider(graph, responsibility_ref, transport, owner_origin=owner_origin)
    after = transport.get_pull(pr_number)
    if (after.get("head") or {}).get("sha") != initial_head or model.get("candidate_sha") != initial_head:
        raise SourceAuthorityError("provider PR head changed during source reconciliation")
    identity = model["source_identity"]
    if identity["graph_digest"] != indexed["digest"]:
        raise SourceAuthorityError("DELP graph identity changed during read")
    return {
        "schema": "V35_R2_B_SOURCE_RECONCILIATION_V1",
        "result": "PARTIAL_PROVIDER_PROVENANCE_NOT_RELEASED",
        "repository": repo,
        "root": indexed["root"],
        "responsibility_ref": responsibility_ref,
        "responsibility_id": node.get("responsibility_id") or "UNKNOWN",
        "graph_generation": indexed["programme"]["graph_generation"],
        "spec_generation": identity.get("spec_generation") or "UNKNOWN",
        "graph_digest": indexed["digest"],
        "source_basis_sha256": model["basis_sha256"],
        "provider_candidate_head": initial_head,
        "owner_mirror": owner,
        "original_owner_source": "UNPROVEN",
        "approved_graph_authority": "PIN_MATCH_OBSERVED_SEPARATE_APPROVAL_NOT_YET_ESTABLISHED",
        "native_custody": "NOT_PROVEN",
        "acceptance_credit": "NONE",
        "delivery_permission": "NONE",
        "accepted_evidence_sources": model["accepted_evidence_sources"],
        "rejected_facts": model["rejected_facts"],
        "progress": model["progress"],
        "actual_next": model["actual_next"],
        "basis_digest": canonical_hash([
            model["basis_sha256"], indexed["digest"], initial_head,
            owner["verbatim_sha256"], owner["source_comment_id"]
        ]),
    }
