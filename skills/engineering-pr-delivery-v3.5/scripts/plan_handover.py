#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from handover_context import build_context
from intelligence_projection import build_improvement, build_task
from lease_liveness import active_lease_renewal
from programme_reconciliation import assess_boundary
from relay_can import evaluate as can_action
from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v3lib import canonical_digest, load_events, load_yaml, validate_schema
from relay_tx import _assert_event_ids_available, _event, _issue_scoped_id, _transition_event_ids


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
    )
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
    args = parser.parse_args()
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
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
