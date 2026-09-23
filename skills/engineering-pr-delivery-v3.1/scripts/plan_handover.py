#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from handover_context import build_context, build_request, render_request
from intelligence_projection import build_improvement, build_task
from programme_currentness import assess as assess_currentness
from programme_reconciliation import build as build_programme_reconciliation, require_ready as require_programme_reconciliation
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

    # Build once to establish the EP-bound parent identity. If the caller supplied
    # an explicit programme parent set, use its matching live observation for the
    # current task rather than requiring a duplicate single-parent argument.
    task_snapshot = build_task(root, base_ref, parent_issue_observation)
    task_parent = task_snapshot.get("parent_issue") or {}
    current_parent_ref = (
        f"{task_parent.get('repository')}#{task_parent.get('number')}"
        if task_parent.get("repository") and task_parent.get("number")
        else None
    )
    explicit_programme_set = list(programme_issue_observations or [])
    effective_parent_observation = parent_issue_observation
    if effective_parent_observation is None and current_parent_ref:
        for observation in explicit_programme_set:
            ref = f"{observation.get('repository')}#{observation.get('issue_number')}"
            if ref == current_parent_ref:
                effective_parent_observation = observation
                task_snapshot = build_task(root, base_ref, effective_parent_observation)
                break

    currentness = assess_currentness(task_snapshot)
    reconciliation_inputs = explicit_programme_set or (
        [effective_parent_observation] if effective_parent_observation is not None else []
    )
    programme_reconciliation = build_programme_reconciliation(
        reconciliation_inputs,
        current_parent_ref=current_parent_ref,
    )
    try:
        require_programme_reconciliation(programme_reconciliation)
    except (RuntimeError, ValueError) as exc:
        raise TransactionError(str(exc)) from exc

    if currentness.get("status") != "CURRENT" and not explicit_programme_set:
        reasons = ",".join(currentness.get("reason_codes") or [])
        raise TransactionError(
            f"{currentness.get('status')}: parent issue {current_parent_ref} cannot be "
            f"carried forward as the current programme frontier ({reasons})"
        )

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
        },
    ))

    return execute(
        root,
        tx_id=tx_id,
        command="PLAN_HANDOVER",
        actor=actor,
        replacements={
            snapshot_path: yaml_bytes(snapshot),
            "relay/GENERATED/HANDOVER_CONTEXT.yaml": yaml_bytes(context),
            str(task_meta["path"]): yaml_bytes(task_snapshot),
            str(improvement_meta["path"]): yaml_bytes(improvement_view),
            "relay/GENERATED/THREE_PASS_REQUEST.yaml": yaml_bytes(request),
            "relay/GENERATED/THREE_PASS_REQUEST.md": request_md,
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
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
