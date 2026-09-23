#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from handover_context import build_context, build_request, render_request
from intelligence_projection import build_improvement, build_task
from lease_liveness import active_lease_renewal
from programme_reconciliation import assess_boundary, require_boundary_ready
from relay_can import evaluate as can_action
from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v3lib import canonical_digest, load_events, load_yaml, validate_schema
from relay_tx import _event, _assert_event_ids_available


def plan_handover(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    target_path: Path,
    base_ref: str,
    complex_mode: bool,
    parent_issue_observation: dict | None = None,
    programme_issue_observations: list[dict] | None = None,
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
    try:
        programme_assessment = require_boundary_ready(
            assess_boundary(
                task_parent,
                programme_issue_observations,
                boundary="HANDOVER",
                current_observation=parent_issue_observation,
            )
        )
    except (RuntimeError, ValueError) as exc:
        raise TransactionError(str(exc)) from exc

    effective_parent_observation = programme_assessment.get("selected_observation")
    programme_reconciliation = programme_assessment["reconciliation"]
    if effective_parent_observation is not None:
        task_snapshot = build_task(root, base_ref, effective_parent_observation)

    context, snapshot = build_context(
        root,
        base_ref=base_ref,
        target=target,
        complex_mode=complex_mode,
        parent_issue_observation=effective_parent_observation,
        programme_reconciliation=programme_reconciliation,
    )
    improvement_view = build_improvement(root)
    task_meta = (context.get("accumulated_learning") or {}).get("task_snapshot") or {}
    improvement_meta = (context.get("accumulated_learning") or {}).get("improvement_view") or {}
    if canonical_digest(task_snapshot) != task_meta.get("digest"):
        raise TransactionError("task snapshot changed while freezing handover context")
    if canonical_digest(improvement_view) != improvement_meta.get("digest"):
        raise TransactionError("improvement view changed while freezing handover context")
    request = build_request(context)
    request_md = render_request(request).encode("utf-8")

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
            request["handover_context"]["digest"],
            task_meta["digest"],
            improvement_meta["digest"],
            canonical_digest(programme_reconciliation),
        ],
        {
            "complex_mode": bool(complex_mode),
            "prompt_count": len(request["generator"]["prompt_sequence"]),
            "generator_mode": request["generator"]["mode"],
            "programme_parent_count": len(programme_reconciliation.get("parents") or []),
            "programme_frontier": list(programme_reconciliation.get("programme_frontier") or []),
            "programme_continuation": programme_assessment.get("continuation"),
            "next_programme_frontier": programme_assessment.get("next_frontier"),
        },
    ))

    replacements = {
        snapshot_path: yaml_bytes(snapshot),
        "relay/GENERATED/HANDOVER_CONTEXT.yaml": yaml_bytes(context),
        str(task_meta["path"]): yaml_bytes(task_snapshot),
        str(improvement_meta["path"]): yaml_bytes(improvement_view),
        "relay/GENERATED/THREE_PASS_REQUEST.yaml": yaml_bytes(request),
        "relay/GENERATED/THREE_PASS_REQUEST.md": request_md,
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
        description="Freeze V3 relay truth and create a verified request for the standalone current three-pass generator."
    )
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--tx-id", required=True)
    parser.add_argument("--event-id", required=True)
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
    parser.add_argument("--complex", action="store_true")
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
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
