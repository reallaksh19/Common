#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote

from handover_context import build_context, build_delp_source_bound_successor, UNKNOWN_OWNER_SOURCE
from intelligence_projection import build_improvement, build_task
from lease_liveness import active_lease_renewal
from programme_reconciliation import assess_boundary
from relay_can import evaluate as can_action
from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v3lib import canonical_digest, load_events, load_yaml, validate_schema
from relay_tx import _assert_event_ids_available, _event, _issue_scoped_id, _transition_event_ids



def _assert_native_graph_current_release(repository: str, graph_path: str, pinned_raw: bytes) -> None:
    """Bind native handover to current default-branch graph, not just a caller SHA.

    The same canonical graph must feed decomposition/scoreboards and a CURRENT
    successor. An immutable agent-selected commit is insufficient release proof.
    This is provider-currentness only, not Owner approval or a merge grant.
    """
    try:
        repo_response = subprocess.run(
            ["gh", "api", "--method", "GET", "repos/" + repository],
            capture_output=True, text=True, check=True, timeout=45,
        )
        repo_meta = json.loads(repo_response.stdout)
        if (not isinstance(repo_meta, dict)
                or str(repo_meta.get("full_name") or "").lower() != repository.lower()):
            raise ValueError("repository identity mismatch")
        branch = repo_meta.get("default_branch")
        if not isinstance(branch, str) or not re.fullmatch(r"[A-Za-z0-9_./-]{1,200}", branch):
            raise ValueError("missing safe default branch")
        endpoint = ("repos/" + repository + "/contents/"
                    + quote(graph_path, safe="/") + "?ref=" + quote(branch, safe=""))
        released_response = subprocess.run(
            ["gh", "api", "--method", "GET", endpoint],
            capture_output=True, text=True, check=True, timeout=45,
        )
        item = json.loads(released_response.stdout)
        if not isinstance(item, dict) or item.get("type") != "file" or item.get("encoding") != "base64":
            raise ValueError("default branch graph not a canonical content file")
        released_raw = base64.b64decode(item["content"], validate=False)
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as exc:
        raise TransactionError("SOURCE_RELEASED_GRAPH_GET_FAILED") from exc
    if released_raw != pinned_raw:
        raise TransactionError("SOURCE_GRAPH_NOT_CURRENT_RELEASED")


def _native_delp_source(
    *, repository: str, graph_revision: str, graph_path: str,
    leaf_ref: str, frozen_basis_path: Path | None = None,
) -> dict:
    """Authenticated GitHub GET-only source for CLI opt-in.

    Never execute the fetched graph, accept ambient repository inference, or
    export the writer methods from the general DELP transport.
    """
    if not os.environ.get("GH_TOKEN") and not os.environ.get("GITHUB_TOKEN"):
        raise TransactionError("SOURCE_GITHUB_TOKEN_REQUIRED")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise TransactionError("SOURCE_REPOSITORY_INVALID")
    if repository.lower() != os.environ.get("GITHUB_REPOSITORY", "").lower():
        raise TransactionError("SOURCE_REPOSITORY_NOT_AUTHENTICATED")
    if not re.fullmatch(r"[0-9a-f]{40}", graph_revision):
        raise TransactionError("SOURCE_GRAPH_REVISION_MUST_BE_EXACT_SHA")
    path = PurePosixPath(graph_path)
    if (path.is_absolute() or not graph_path.endswith(".json")
            or any(part in ("", ".", "..") for part in graph_path.split("/"))
            or len(graph_path) > 256):
        raise TransactionError("SOURCE_GRAPH_PATH_NOT_REPOSITORY_RELATIVE")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+#[1-9][0-9]*", leaf_ref):
        raise TransactionError("SOURCE_LEAF_REF_INVALID")

    endpoint = ("repos/" + repository + "/contents/" + quote(graph_path, safe="/")
                + "?ref=" + graph_revision)
    try:
        response = subprocess.run(
            ["gh", "api", "--method", "GET", endpoint],
            capture_output=True, text=True, check=True, timeout=45,
        )
        item = json.loads(response.stdout)
        if item.get("type") != "file" or item.get("encoding") != "base64":
            raise ValueError("not a canonical GitHub content blob")
        raw = base64.b64decode(item["content"], validate=False)
        if len(raw) > 5_000_000:
            raise ValueError("source graph exceeds bounded input")
        graph = json.loads(raw)
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as exc:
        raise TransactionError("SOURCE_GRAPH_AUTHENTICATED_GET_FAILED") from exc
    if not isinstance(graph, dict) or (
        str((graph.get("programme") or {}).get("repository") or "").lower()
        != repository.lower()
    ):
        raise TransactionError("SOURCE_GRAPH_REPOSITORY_MISMATCH")

    # Mandatory release custody: a pin can identify a candidate PR graph that is
    # not yet the graph used by the live DELP scoreboard. Do not call that CURRENT.
    def release_check() -> None:
        _assert_native_graph_current_release(repository, graph_path, raw)

    release_check()

    import delp_projection_v32 as delp

    class ReadOnlyGithub:
        """Expose only the five GitHub GET methods required by the DELP reader."""
        def __init__(self):
            self.__transport = delp.GhTransport(repository)

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

    frozen_basis = None
    if frozen_basis_path is not None:
        frozen_basis = load_yaml(frozen_basis_path)
        if isinstance(frozen_basis, dict) and set(frozen_basis) == {"digests"}:
            frozen_basis = frozen_basis["digests"]
    return {
        "graph": graph,
        "leaf_ref": leaf_ref,
        "provider": ReadOnlyGithub(),
        "frozen_basis": frozen_basis,
        "__native_release_check": release_check,
        "__native_graph_source": {
            "repository": repository,
            "revision": graph_revision,
            "path": graph_path,
            "permalink": "https://github.com/" + repository
                         + "/blob/" + graph_revision + "/" + graph_path,
        },
    }


def _owner_intent_handover_options(owner_intent: dict | None) -> tuple[int | None, list[str], bool]:
    if owner_intent is None:
        return None, [], False
    if not isinstance(owner_intent, dict):
        raise TransactionError("owner_intent must be a mapping")
    payload = owner_intent.get("owner_intent") if isinstance(owner_intent.get("owner_intent"), dict) else owner_intent
    deliverables = payload.get("requested_deliverables") or []
    constraints = payload.get("boundary_constraints") or []
    if not isinstance(deliverables, list) or not isinstance(constraints, list):
        raise TransactionError("owner_intent deliverables/constraints must be lists")
    counts: list[int] = []
    requested = False
    for row in deliverables:
        if not isinstance(row, dict) or row.get("type") != "SUCCESSOR_RECONSTRUCTION_CHALLENGE":
            continue
        requested = True
        if row.get("count") is not None:
            count = row["count"]
            if isinstance(count, bool) or not isinstance(count, int) or not (0 <= count <= 10):
                raise TransactionError("Owner-intent successor challenge count must be an integer from 0 to 10")
            counts.append(count)
    if len(set(counts)) > 1:
        raise TransactionError("Owner intent contains conflicting successor challenge counts")
    clean_constraints = [str(x) for x in constraints if isinstance(x, str) and x.strip()]
    return (counts[0] if counts else None), list(dict.fromkeys(clean_constraints)), requested


def _resolve_successor_options(
    owner_intent: dict | None,
    explicit_count: int | None,
) -> tuple[int | None, list[str]]:
    owner_count, constraints, requested = _owner_intent_handover_options(owner_intent)
    if owner_count is not None and explicit_count is not None and owner_count != explicit_count:
        raise TransactionError(
            f"successor challenge count conflicts with Owner intent: explicit {explicit_count}, Owner {owner_count}"
        )
    resolved = explicit_count if explicit_count is not None else owner_count
    if requested and resolved is None:
        raise TransactionError(
            "Owner intent requests a successor reconstruction challenge without a concrete count; "
            "resolve the count before freezing the handover"
        )
    return resolved, constraints


def plan_handover(
    root: Path,
    *,
    tx_id: str | None,
    event_id: str | None,
    actor: str,
    target_path: Path,
    base_ref: str,
    complex_mode: bool,
    parent_issue_observation: dict | None = None,
    programme_issue_observations: list[dict] | None = None,
    selected_programme_ref: str | None = None,
    successor_challenge_count: int | None = None,
    owner_intent: dict | None = None,
    delp_source: dict | None = None,
    fail_after: int | None = None,
):
    allowed = can_action(root, "HANDOVER")
    if not allowed["allowed"]:
        raise TransactionError(f"HANDOVER denied: {', '.join(allowed['reason_codes'])}")

    target = load_yaml(target_path)
    errors = validate_schema("handover-target", target, "HANDOVER_TARGET")
    if errors:
        raise TransactionError("; ".join(errors))

    # Resolve all programme-boundary semantics through the canonical assessment.
    # A single live parent observation is sufficient for cheap continuation;
    # an explicit ordered parent set may switch the programme frontier.
    task_snapshot = build_task(root, base_ref, None)
    task_parent = task_snapshot.get("parent_issue") or {}
    governing_issue = task_parent.get("number")
    governing_issue = int(governing_issue) if governing_issue is not None else None
    tx_id = _issue_scoped_id(
        root,
        kind="TX",
        value=tx_id,
        issue_number=governing_issue,
        label="transaction id",
    )
    event_id = _transition_event_ids(
        root,
        event_id=event_id,
        issue_number=governing_issue,
        legacy_suffixes=[""],
    )[0]
    # Recorder-first V3.1 records programme reconciliation as context only.
    # A BLOCK/UNKNOWN assessment is carried into the handover package instead of
    # preventing the handover record from being created.
    try:
        programme_assessment = assess_boundary(
            task_parent,
            programme_issue_observations,
            boundary="HANDOVER",
            current_observation=parent_issue_observation,
            selected_frontier_ref=selected_programme_ref,
        )
    except ValueError:
        programme_assessment = assess_boundary(None, None, boundary="HANDOVER")

    effective_parent_observation = programme_assessment.get("selected_observation")
    programme_reconciliation = programme_assessment["reconciliation"]
    if effective_parent_observation is not None:
        task_snapshot = build_task(root, base_ref, effective_parent_observation)

    resolved_challenge_count, owner_boundary_constraints = _resolve_successor_options(
        owner_intent,
        successor_challenge_count,
    )
    improvement_view = build_improvement(root)
    # Source locations are custody metadata for the EVENT; keep the existing
    # C4 handover-context schema strictly unchanged and pass only its
    # authoritative source input keys to the source-bound DELP builder.
    native_graph_source = (
        delp_source.get("__native_graph_source")
        if isinstance(delp_source, dict) else None
    )
    native_release_check = (
        delp_source.get("__native_release_check")
        if isinstance(delp_source, dict) else None
    )
    if native_release_check is not None and not callable(native_release_check):
        raise TransactionError("SOURCE_RELEASE_CHECK_INVALID")
    context_source = (
        {k: v for k, v in delp_source.items()
         if k not in {"__native_graph_source", "__native_release_check"}}
        if isinstance(delp_source, dict) else delp_source
    )
    context, snapshot = build_context(
        root,
        base_ref=base_ref,
        target=target,
        complex_mode=complex_mode,
        parent_issue_observation=effective_parent_observation,
        programme_reconciliation=programme_reconciliation,
        task_snapshot_override=task_snapshot,
        improvement_view_override=improvement_view,
        successor_challenge_count=resolved_challenge_count,
        successor_boundary_constraints=owner_boundary_constraints,
        delp_source=context_source,
    )
    source_bound = context.get("source_bound_successor")
    if delp_source is not None:
        if not isinstance(source_bound, dict) or source_bound.get("currentness") != "CURRENT_READ_ONLY":
            raise TransactionError("SOURCE_BOUND_RECONCILIATION_REQUIRED")
    task_meta = (context.get("accumulated_learning") or {}).get("task_snapshot") or {}
    improvement_meta = (context.get("accumulated_learning") or {}).get("improvement_view") or {}
    if canonical_digest(task_snapshot) != task_meta.get("digest"):
        raise TransactionError("task snapshot changed while freezing handover context")
    if canonical_digest(improvement_view) != improvement_meta.get("digest"):
        raise TransactionError("improvement view changed while freezing handover context")
    state = load_yaml(root / "relay/STATE.yaml")
    snapshot_path = str((state.get("generated") or {}).get("snapshot"))
    events, event_errors = load_events(root / "relay/EVENTS.jsonl")
    if event_errors:
        raise TransactionError("; ".join(event_errors[:8]))
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "HANDOVER_PLANNED",
        actor,
        target["url"],
        [
            tx_id,
            target["provider_ref"],
            canonical_digest(context),
            task_meta["digest"],
            improvement_meta["digest"],
            canonical_digest(programme_reconciliation),
        ],
        {
            "reasoning_request_generated": False,
            "successor_entry_mode": (context.get("successor_entry") or {}).get("mode"),
            "successor_challenge_count": len((context.get("successor_entry") or {}).get("successor_reconstruction_challenge") or []),
            "owner_intent_bound": owner_intent is not None,
            "owner_boundary_constraint_count": len(owner_boundary_constraints),
            "programme_parent_count": len(programme_reconciliation.get("parents") or []),
            "programme_frontier": list(programme_reconciliation.get("programme_frontier") or []),
            "selected_programme_frontier": programme_assessment.get("selected_programme_frontier"),
            "programme_continuation": programme_assessment.get("continuation"),
            "next_programme_frontier": programme_assessment.get("next_frontier"),
            **({
                "source_bound_currentness": source_bound["currentness"],
                "source_bound_input_digest": source_bound["digests"]["input"],
                "source_bound_plan_digest": source_bound["digests"]["plan"],
                "source_bound_graph_digest": source_bound["digests"]["graph"],
                "source_bound_provider_digest": source_bound["digests"]["provider"],
                "source_delp_responsibility_basis_digest":
                    source_bound["delp_responsibility_core"]["basis_digest"],
            } if source_bound is not None else {}),
            **({"source_graph_pinned_location": native_graph_source}
               if native_graph_source is not None else {}),
        },
    ))

    replacements = {
        snapshot_path: yaml_bytes(snapshot),
        "relay/GENERATED/HANDOVER_CONTEXT.yaml": yaml_bytes(context),
        "relay/EVENTS.jsonl": jsonl_bytes(events),
    }
    renewal = active_lease_renewal(root, state, actor, base_ref=base_ref)
    if renewal is not None:
        lease_path, renewed_lease = renewal
        replacements[lease_path] = yaml_bytes(renewed_lease)

    # A provider can move after context was first constructed. Freeze the
    # transaction against the *same* graph/plan/input/provider digests again
    # immediately before entering the transactional staging/commit boundary.
    # This is a read-only freshness fence, not an external GitHub CAS.
    if source_bound is not None:
        if native_release_check is not None:
            native_release_check()
        last_read = build_delp_source_bound_successor(
            context_source["graph"],
            leaf_ref=context_source["leaf_ref"],
            provider=context_source["provider"],
            frozen_basis=source_bound["digests"],
            owner_source_status=context_source.get("owner_source_status", UNKNOWN_OWNER_SOURCE),
        )
        if last_read["currentness"] != "CURRENT_READ_ONLY":
            raise TransactionError("SOURCE_BOUND_RECONCILIATION_REQUIRED")
        if (last_read["delp_responsibility_core"]["basis_digest"] !=
                source_bound["delp_responsibility_core"]["basis_digest"]):
            raise TransactionError("SOURCE_DELP_RESPONSIBILITY_BASIS_CHANGED")

    return execute(
        root,
        tx_id=tx_id,
        command="PLAN_HANDOVER",
        actor=actor,
        replacements=replacements,
        fail_after=fail_after,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze V3 relay custody truth without implicitly generating a reasoning request."
    )
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument(
        "--tx-id",
        help="Explicit transaction ID. Omit to allocate TX.<issue>.<serial> from the current task parent issue.",
    )
    parser.add_argument(
        "--event-id",
        help="Explicit event ID. Omit to allocate EVT.<issue>.<serial> from the current task parent issue.",
    )
    parser.add_argument("--actor", required=True)
    parser.add_argument("--target-observation", required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--parent-issue-observation")
    parser.add_argument(
        "--programme-issue-observation",
        action="append",
        default=[],
        help="Provider observation for one reconciled programme parent; repeat in intended programme order.",
    )
    parser.add_argument(
        "--selected-programme-ref",
        help="Explicit Owner/ROADMAP selected programme parent ref.",
    )
    parser.add_argument("--complex", action="store_true")
    parser.add_argument(
        "--successor-challenge-count",
        type=int,
        help="Compatibility override for successor challenge count; must agree with Owner intent when both are supplied.",
    )
    parser.add_argument(
        "--owner-intent",
        help="YAML file containing either OWNER_INTENT itself or a parse_owner_command result with an owner_intent field.",
    )
    parser.add_argument(
        "--source-repository",
        help="GitHub owner/name for an explicitly opted-in, GET-only DELP source.",
    )
    parser.add_argument("--source-graph-revision",
                        help="Immutable 40-hex GitHub commit holding the released graph.")
    parser.add_argument("--source-graph-path",
                        help="Repository-relative JSON graph path within that commit.")
    parser.add_argument("--source-leaf-ref",
                        help="Exact DELP leaf ref, e.g. Common#793.")
    parser.add_argument("--source-frozen-basis",
                        help="Optional YAML containing the previous graph/plan/input/provider digests.")
    args = parser.parse_args()
    selectors = [args.source_repository, args.source_graph_revision,
                 args.source_graph_path, args.source_leaf_ref]
    if any(selectors) and not all(selectors):
        parser.error("source-bound handover requires all four source selectors")
    if args.source_frozen_basis and not all(selectors):
        parser.error("--source-frozen-basis requires complete source selectors")
    delp_source = (
        _native_delp_source(
            repository=args.source_repository,
            graph_revision=args.source_graph_revision,
            graph_path=args.source_graph_path,
            leaf_ref=args.source_leaf_ref,
            frozen_basis_path=Path(args.source_frozen_basis) if args.source_frozen_basis else None,
        )
        if all(selectors) else None
    )
    result = plan_handover(
        Path(args.repo_root).resolve(),
        tx_id=args.tx_id,
        event_id=args.event_id,
        actor=args.actor,
        target_path=Path(args.target_observation),
        base_ref=args.base_ref,
        complex_mode=args.complex,
        parent_issue_observation=(load_yaml(Path(args.parent_issue_observation)) if args.parent_issue_observation else None),
        programme_issue_observations=[load_yaml(Path(path)) for path in args.programme_issue_observation],
        selected_programme_ref=args.selected_programme_ref,
        successor_challenge_count=args.successor_challenge_count,
        owner_intent=(load_yaml(Path(args.owner_intent)) if args.owner_intent else None),
        delp_source=delp_source,
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
