"""R7-U2: read-only operational GitHub release readiness. NO WRITES.

A passed preflight does not activate Actions or authorize Local/merge/review.
Graph+digest must originate from governing-root GitHub OWNER native comment;
issue/PR writer permission is a *distinct* independently read comment.
Workflow presence/active state is re-observed on a verified default-branch SHA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from typing import Any

import delp_projection_v35 as DELP
import integration_cold_entry_v35 as COLD
import integration_graph_authority_v35 as GRAPH
import integration_scoreboard_publish_v35 as PUBLISH

DEFAULT_WORKFLOW = ".github/workflows/v35-smart-scoreboard.yml"
# Explicitly audited in R7-U3 at main c8eb92a (inert V3.5 workflow).
# This is Git's SHA-1 of "blob <length>\\0<utf8-bytes>", NOT a substring
# marker match. Any workflow change requires independent review and pin update.
_AUDITED_WORKFLOW_BLOB_SHA = "95716cf41a58832fa0d813ab968ea0466474b99a"
_AUDITED_TEMPLATE_PATH = (
    "skills/engineering-pr-delivery-v3.5/"
    "examples/integration/v35-scoreboard-workflow.template.yml"
)
_SHA = re.compile(r"^[a-f0-9]{40}$")


class ReleasePreflightError(ValueError):
    """Invalid input or source origin. Never interprets absence as authority."""


def _checked_workflow(transport: Any, path: str) -> dict[str, Any]:
    """Prove guarded workflow at exact DEFAULT BRANCH commit, or return UNKNOWN."""
    if not isinstance(path, str) or not path.startswith(".github/workflows/") or not (
        path.endswith(".yml") or path.endswith(".yaml")
    ) or ".." in path.split("/"):
        raise ReleasePreflightError("workflow path must be a trusted .github/workflows YAML")
    if not hasattr(transport, "_gh"):
        return {"status": "WORKFLOW_PROVIDER_UNOBSERVED", "reason": "NATIVE_WORKFLOW_API_UNAVAILABLE"}
    try:
        repo = transport._gh(f"repos/{transport.repository}")
        if not isinstance(repo, Mapping) or not isinstance(repo.get("default_branch"), str):
            raise ReleasePreflightError("default branch cannot be verified from native repository metadata")
        branch = repo["default_branch"]
        head = transport.get_commit_sha(branch)
        if not isinstance(head, str) or not _SHA.fullmatch(head):
            raise ReleasePreflightError("native default branch commit SHA is unknown")
        file = transport.get_file_at(head, path)
        if not isinstance(file, Mapping) or not isinstance(file.get("content"), str):
            raise ReleasePreflightError("default branch workflow bytes unavailable")
        code = file["content"]
        workflow = transport._gh(
            f"repos/{transport.repository}/actions/workflows/{path.split('/')[-1]}"
        )
    except (DELP.DelpError, OSError, LookupError, ValueError) as exc:
        return {"status": "WORKFLOW_PROVIDER_UNVERIFIED",
                "reason": "CANNOT_VERIFY_DEFAULT_BRANCH_AND_WORKFLOW",
                "detail": str(exc)[:180]}
    if not isinstance(workflow, Mapping) or workflow.get("path") != path:
        return {"status": "WORKFLOW_IDENTITY_MISMATCH", "default_head": head}
    if workflow.get("state") != "active":
        return {"status": "WORKFLOW_NOT_ACTIVE", "default_head": head,
                "native_state": str(workflow.get("state") or "UNKNOWN")}
    # Require exact reviewed bytes, not strings that could be in comments,
    # harmless steps or an unrelated unsafe workflow. Check both the native
    # GitHub reported blob id and an independent Git-blob hash of the bytes.
    encoded = code.encode("utf-8")
    blob_sha = hashlib.sha1(
        b"blob " + str(len(encoded)).encode("ascii") + b"\\x00" + encoded
    ).hexdigest()
    reported_blob = file.get("blob_sha")
    if (blob_sha != _AUDITED_WORKFLOW_BLOB_SHA or
            reported_blob != _AUDITED_WORKFLOW_BLOB_SHA):
        return {
            "status": "WORKFLOW_NOT_AUDITED_TEMPLATE",
            "default_head": head,
            "source_audit": "EXACT_GIT_BLOB_ID_MISMATCH",
            "native_blob_id": str(reported_blob or "UNKNOWN"),
            "calculated_blob_id": blob_sha,
        }
    # A successful blob check proves audited workflow content only. An external
    # security review, two Owner approvals and actual event readback remain
    # separate release obligations.
    return {"status": "TRUSTED_DEFAULT_BRANCH_WORKFLOW_OBSERVED",
            "default_branch": branch, "default_head": head,
            "path": path, "native_state": "active",
            "workflow_source_integrity": "AUDITED_TEMPLATE_BYTES_VERIFIED",
            "audited_template_path": _AUDITED_TEMPLATE_PATH,
            "audited_blob_sha": _AUDITED_WORKFLOW_BLOB_SHA,
            "independent_security_review": "NOT_PERFORMED"}


def assess(
    transport: Any, root_url: str, *,
    scoreboard_approval_ref: str | None = None,
    workflow_path: str = DEFAULT_WORKFLOW,
) -> dict[str, Any]:
    """Read current provider graph + writer source and optional deployment state.

    No acceptance or IC grants are computed; if root lacks an approval, later
    surfaces are intentionally UNOBSERVED rather than guessed from a template.
    """
    route = COLD._input_route(transport, root_url)
    if route["entry_kind"] != "PARENT":
        raise ReleasePreflightError("release gate must begin from governing parent issue")
    cold = COLD.reconstruct(transport, root_url)
    if cold.get("schema") != "V35_COLD_ENTRY_READINESS_V1":
        raise ReleasePreflightError("native cold-source schema not verified")
    common = {
        "schema": "V35_R7_RELEASE_PREFLIGHT_V1",
        "repository": transport.repository,
        "root": cold["root"],
        "candidate_source": cold["status"],
        "live_status_writer_invoked": False,
        "issue_pr_body_changes": "NONE",
        "owner_original_chat": "UNPROVEN",
        "native_custody": "SOURCE_NOT_PROVEN",
        "programme_ic_credit": "NONE",
        "independent_reviewer": "NOT_OBSERVED",
        "separate_owner_activation": "NOT_INFERRED",
    }
    if cold["status"] == "HOLD_NO_PROVIDER_APPROVED_GRAPH":
        return dict(common,
            status="HOLD_GRAPH_SOURCE_NOT_APPROVED",
            graph_selection="MISSING_ON_GOVERNING_ROOT",
            scoreboard_permission="NOT_EVALUATED_NO_APPROVED_GRAPH",
            workflow_deployment="NOT_EVALUATED_NO_APPROVED_GRAPH",
            actual_next="OWNER_ISSUE_ROOT_SCOPED_IMMUTABLE_GRAPH_SELECTION",
        )
    if cold["status"] != "GOVERNED_GRAPH_PROVIDER_OBSERVED_READ_ONLY":
        raise ReleasePreflightError("unrecognised current provider source")
    selected_ref = cold["approved_source_ref"]
    selected = GRAPH.load_approved_source(
        transport, selected_ref,
        selected_responsibility=cold["selected_leaf"],
        selected_pr=cold["approved_pr"],
        expected_programme_root=cold["root"],
    )
    if selected["graph_digest"] != cold["graph_digest"]:
        raise ReleasePreflightError("source graph digest drifted across native reads")
    if not scoreboard_approval_ref:
        return dict(common,
            status="HOLD_SCOREBOARD_PERMISSION_MISSING",
            graph_selection="PROVIDER_OWNER_ROOT_GRAPH_VERIFIED",
            graph_digest=selected["graph_digest"],
            graph_source_ref=selected_ref,
            scoreboard_permission="MISSING_SCOPED_COMMENT_REF",
            workflow_deployment="NOT_EVALUATED_WITHOUT_WRITER_PERMISSION",
            actual_next="OWNER_ISSUE_SEPARATE_SCOPED_SCOREBOARD_PERMISSION",
        )
    indexed = DELP.validate_graph(selected["graph"])
    try:
        approval = PUBLISH._approved_for_write(
            transport, indexed, cold["selected_leaf"], cold["approved_pr"],
            selected["graph_digest"], scoreboard_approval_ref,
        )
    except (PUBLISH.PublishError, DELP.DelpError) as exc:
        return dict(common,
            status="HOLD_SCOREBOARD_PERMISSION_UNVERIFIED",
            graph_selection="PROVIDER_OWNER_ROOT_GRAPH_VERIFIED",
            graph_digest=selected["graph_digest"],
            graph_source_ref=selected_ref,
            scoreboard_permission="DENIED_BY_NATIVE_SCOPE_OR_PRINCIPAL",
            workflow_deployment="NOT_EVALUATED_WITHOUT_WRITER_PERMISSION",
            permission_denial=str(exc)[:180],
            actual_next="RECONCILE_OWNER_APPROVED_SCOPED_SCOREBOARD_COMMENT",
        )
    observed = _checked_workflow(transport, workflow_path)
    if observed["status"] != "TRUSTED_DEFAULT_BRANCH_WORKFLOW_OBSERVED":
        return dict(common,
            status="HOLD_DEFAULT_BRANCH_WORKFLOW_NOT_VERIFIED",
            graph_selection="PROVIDER_OWNER_ROOT_GRAPH_VERIFIED",
            graph_digest=selected["graph_digest"],
            graph_source_ref=selected_ref,
            scoreboard_permission="PROVIDER_SCOPED_WRITER_VERIFIED",
            scoreboard_approval_ref=approval["approval_ref"],
            workflow=observed,
            actual_next="REVIEW_AND_INSTALL_TRUSTED_WORKFLOW_SEPARATELY",
        )
    return dict(common,
        status="PREFLIGHT_GATES_OBSERVED_NOT_OPERATIONALLY_ACCEPTED",
        graph_selection="PROVIDER_OWNER_ROOT_GRAPH_VERIFIED",
        graph_digest=selected["graph_digest"],
        graph_source_ref=selected_ref,
        scoreboard_permission="PROVIDER_SCOPED_WRITER_VERIFIED",
        scoreboard_approval_ref=approval["approval_ref"],
        workflow=observed,
        actual_next="OWNER_AUTHORIZE_CONTROLLED_LIVE_REPLAY_AND_INDEPENDENT_REVIEW",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R7 read-only GitHub operational release preflight")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--root-url", required=True)
    parser.add_argument("--scoreboard-approval-ref")
    parser.add_argument("--workflow-path", default=DEFAULT_WORKFLOW)
    args = parser.parse_args(argv)
    try:
        result = assess(
            PUBLISH.ScoreboardTransport(args.repository), args.root_url,
            scoreboard_approval_ref=args.scoreboard_approval_ref,
            workflow_path=args.workflow_path,
        )
        print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
        return 0 if result["status"] == "PREFLIGHT_GATES_OBSERVED_NOT_OPERATIONALLY_ACCEPTED" else 3
    except (ReleasePreflightError, COLD.ColdEntryError, GRAPH.GraphSelectionError,
            DELP.DelpError, OSError, ValueError) as exc:
        print(f"V3.5 R7 release preflight REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
