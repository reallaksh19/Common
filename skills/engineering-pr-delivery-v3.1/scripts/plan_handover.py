#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from handover_context import build_context, build_request, render_request
from intelligence_projection import build_improvement, build_task
from programme_currentness import require_handover_currentness
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
    fail_after: int | None = None,
):
    allowed = can_action(root, "HANDOVER")
    if not allowed["allowed"]:
        raise TransactionError(f"HANDOVER denied: {', '.join(allowed['reason_codes'])}")

    target = load_yaml(target_path)
    errors = validate_schema("handover-target", target, "HANDOVER_TARGET")
    if errors:
        raise TransactionError("; ".join(errors))

    task_snapshot = build_task(root, base_ref, parent_issue_observation)
    try:
        require_handover_currentness(task_snapshot)
    except RuntimeError as exc:
        raise TransactionError(str(exc)) from exc

    context, snapshot = build_context(
        root,
        base_ref=base_ref,
        target=target,
        complex_mode=complex_mode,
        parent_issue_observation=parent_issue_observation,
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
        ],
        {
            "complex_mode": bool(complex_mode),
            "prompt_count": len(request["generator"]["prompt_sequence"]),
            "generator_mode": request["generator"]["mode"],
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
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
