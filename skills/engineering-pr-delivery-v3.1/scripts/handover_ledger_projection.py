#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from intelligence_projection import ProjectionError, build_task
from snapshot_projection import build as build_snapshot
from v3lib import canonical_digest, load_events, load_yaml, validate_schema


RECORD_TYPES = {
    "EP_CREATED",
    "LEASE_GRANTED",
    "LEASE_RENEWED",
    "LEASE_RELEASED",
    "LEASE_REVOKED",
    "CHECKPOINT_ACCEPTED",
    "HANDOVER_PLANNED",
    "HANDOVER_PUBLISHED",
    "HANDOVER_ACCEPTED",
    "RECOVERY_STARTED",
    "RECOVERY_RECONSTRUCTED",
    "CHANGE_HYPOTHESIS_RECORDED",
    "CHANGE_VERIFIED",
    "CHANGE_REJECTED",
    "CHANGE_DELTA_PROPOSED",
    "CHANGE_AUTHORIZED",
    "LOCAL_EXECUTION_EXPORTED",
    "LOCAL_EXECUTION_RETURNED",
    "ROADMAP_RECONCILED",
    "TASK_CLOSED",
    "PR_OPENED",
    "PR_MERGED",
}


def _load_yaml_files(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    if not directory.exists():
        return rows
    for path in sorted(directory.glob("*.yaml")):
        value = load_yaml(path)
        if isinstance(value, dict):
            rows.append((path, value))
    return rows


def _matches_parent(ep: dict[str, Any], repository: str, number: int) -> bool:
    parent = ep.get("parent_issue") or {}
    return parent.get("repository") == repository and parent.get("number") == number


def _checkpoint_complete(checkpoint: dict[str, Any] | None) -> bool:
    if not isinstance(checkpoint, dict):
        return False
    acceptance = checkpoint.get("acceptance") or []
    return bool(acceptance) and all(
        isinstance(item, dict) and item.get("result") == "PASS"
        for item in acceptance
    )


def _checkpoint_by_ep(root: Path, events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for event in events:
        if event.get("type") != "CHECKPOINT_ACCEPTED":
            continue
        checkpoint_id = str(event.get("subject") or "")
        path = root / "relay/CHECKPOINTS" / f"{checkpoint_id}.yaml"
        if not path.exists():
            continue
        checkpoint = load_yaml(path)
        if isinstance(checkpoint, dict) and checkpoint.get("ep"):
            result[str(checkpoint["ep"])] = checkpoint
    for _, checkpoint in _load_yaml_files(root / "relay/CHECKPOINTS"):
        ep_id = checkpoint.get("ep")
        if ep_id and ep_id not in result and _checkpoint_complete(checkpoint):
            result[str(ep_id)] = checkpoint
    return result


def _leases_by_ep(root: Path) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for _, lease in _load_yaml_files(root / "relay/LEASES"):
        ep_id = ((lease.get("basis") or {}).get("ep_id"))
        if ep_id:
            result.setdefault(str(ep_id), []).append(lease)
    return result


def _selected_lease(leases: list[dict[str, Any]]) -> dict[str, Any] | None:
    active = [lease for lease in leases if lease.get("state") == "ACTIVE"]
    if active:
        return active[-1]
    return leases[-1] if leases else None


def _lease_continuation(
    lease: dict[str, Any] | None,
    events: list[dict[str, Any]],
    *,
    ep_id: str | None = None,
    fallback_recovery: bool = False,
) -> str:
    if fallback_recovery:
        return "RECOVERY"
    lease_id = str((lease or {}).get("id") or "")
    if not lease_id:
        return "UNKNOWN"
    grant_index = None
    continuation = "NEW"
    for index, event in enumerate(events):
        if event.get("type") != "LEASE_GRANTED" or str(event.get("subject")) != lease_id:
            continue
        grant_index = index
        value = str((event.get("details") or {}).get("continuation") or "")
        continuation = value if value in {"NEW", "HANDOFF", "RECOVERY"} else "NEW"
    if continuation == "NEW" and ep_id and grant_index is not None:
        for event in events[grant_index + 1:]:
            if event.get("type") == "HANDOVER_PUBLISHED" and str(event.get("subject")) == str(ep_id):
                return "HANDOFF_PENDING"
    return continuation


def _ep_status(
    ep_id: str,
    *,
    current_ep: str | None,
    current_lease: str | None,
    checkpoint: dict[str, Any] | None,
    lease: dict[str, Any] | None,
    events: list[dict[str, Any]],
) -> tuple[str, str]:
    if ep_id == current_ep and lease and lease.get("id") == current_lease and lease.get("state") == "ACTIVE":
        return "ACTIVE", _lease_continuation(lease, events, ep_id=ep_id)
    if _checkpoint_complete(checkpoint):
        return "COMPLETE", _lease_continuation(lease, events, ep_id=ep_id)
    if lease and lease.get("state") in {"RELEASED", "REVOKED", "INVALIDATED"}:
        return "RECOVERY_REQUIRED", "RECOVERY"
    return "UNKNOWN", _lease_continuation(lease, events, ep_id=ep_id)


def build(
    root: Path,
    parent_issue_observation: dict[str, Any],
    *,
    base_ref: str,
) -> dict[str, Any]:
    task = build_task(root, base_ref, parent_issue_observation)
    parent = task.get("parent_issue") or {}
    ledger_ref = parent.get("handover_ledger")
    if not isinstance(ledger_ref, dict):
        provider_status_path = root / "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml"
        if provider_status_path.exists():
            provider_status = load_yaml(provider_status_path)
            observed_parent = provider_status.get("parent") or {}
            if (
                observed_parent.get("repository") == parent.get("repository")
                and observed_parent.get("issue_number") == parent.get("number")
            ):
                ledger_ref = provider_status.get("handover")

    repository = str(parent.get("repository") or "")
    number = parent.get("number")
    if not repository or not isinstance(number, int):
        raise ProjectionError("handover ledger requires a concrete parent issue identity")

    state = load_yaml(root / "relay/STATE.yaml")
    snapshot = build_snapshot(root, base_ref)
    events, errors = load_events(root / "relay/EVENTS.jsonl")
    if errors:
        raise ProjectionError("; ".join(errors))

    current_execution = state.get("execution") or {}
    current_ep = current_execution.get("ep")
    current_lease = current_execution.get("lease")

    eps: dict[str, dict[str, Any]] = {}
    ep_paths: dict[str, str] = {}
    for path, ep in _load_yaml_files(root / "relay/WORK"):
        ep_id = str(ep.get("id") or "")
        if not ep_id:
            continue
        if _matches_parent(ep, repository, number) or ep_id == current_ep:
            eps[ep_id] = ep
            ep_paths[ep_id] = str(path.relative_to(root))

    if current_ep and current_ep not in eps:
        current_path = root / "relay/WORK" / f"{current_ep}.yaml"
        if current_path.exists():
            ep = load_yaml(current_path)
            if isinstance(ep, dict):
                eps[str(current_ep)] = ep
                ep_paths[str(current_ep)] = str(current_path.relative_to(root))

    checkpoints = _checkpoint_by_ep(root, events)
    leases_by_ep = _leases_by_ep(root)

    created_order: list[str] = []
    for event in events:
        if event.get("type") == "EP_CREATED" and str(event.get("subject")) in eps:
            created_order.append(str(event.get("subject")))
    for ep_id in sorted(eps):
        if ep_id not in created_order:
            created_order.append(ep_id)

    ep_index: list[dict[str, Any]] = []
    relevant_refs: set[str] = set()
    for ep_id in created_order:
        ep = eps[ep_id]
        checkpoint = checkpoints.get(ep_id)
        lease = _selected_lease(leases_by_ep.get(ep_id, []))
        status, continuation = _ep_status(
            ep_id,
            current_ep=str(current_ep) if current_ep else None,
            current_lease=str(current_lease) if current_lease else None,
            checkpoint=checkpoint,
            lease=lease,
            events=events,
        )
        checkpoint_id = (checkpoint or {}).get("id")
        lease_id = (lease or {}).get("id")
        executor = ((lease or {}).get("executor") or {}).get("id")
        custody_epoch = ((lease or {}).get("custody") or {}).get("epoch")
        basis = [ep_paths[ep_id]]
        if checkpoint_id:
            basis.append(f"relay/CHECKPOINTS/{checkpoint_id}.yaml")
        if lease_id:
            basis.append(f"relay/LEASES/{lease_id}.yaml")
        relevant_refs.update([ep_id, *(str(x) for x in (checkpoint_id, lease_id) if x)])
        ep_index.append({
            "ep": ep_id,
            "work_package": str(ep.get("work_package")),
            "status": status,
            "continuation": continuation,
            "checkpoint": checkpoint_id,
            "lease": lease_id,
            "executor": executor,
            "custody_epoch": custody_epoch,
            "basis": basis,
        })

    frontier = next((row for row in ep_index if row["ep"] == current_ep), None)
    if frontier is None:
        frontier = {
            "ep": current_ep,
            "work_package": (task.get("identity") or {}).get("work_package"),
            "status": "UNKNOWN",
            "continuation": "UNKNOWN",
            "checkpoint": None,
            "lease": current_lease,
            "executor": (task.get("execution") or {}).get("executor"),
            "custody_epoch": current_execution.get("custody_epoch"),
        }

    offloads: list[dict[str, Any]] = []
    for ep_id in created_order:
        for offload in eps[ep_id].get("offloads") or []:
            if isinstance(offload, dict):
                row = {"origin_ep": ep_id, **offload}
                offloads.append(row)

    records = []
    for event in events:
        if event.get("type") not in RECORD_TYPES:
            continue
        event_refs = {
            str(event.get("subject") or ""),
            *(str(x) for x in event.get("basis") or []),
        }
        if relevant_refs and not (event_refs & relevant_refs):
            continue
        records.append({
            "event_id": str(event.get("event_id")),
            "type": str(event.get("type")),
            "timestamp": str(event.get("timestamp")),
            "actor": str(event.get("actor")),
            "subject": str(event.get("subject")),
            "basis": [str(x) for x in event.get("basis") or []],
        })

    change_rows = []
    for path, delta in _load_yaml_files(root / "relay/CHANGES"):
        if delta.get("schema_version") != "relay-v3.1-change-delta":
            continue
        source_issue = ((delta.get("application") or {}).get("source_issue"))
        if source_issue in {None, number}:
            change_rows.append((path, delta))
    active_change = None
    for path, delta in change_rows:
        if (delta.get("application") or {}).get("status") != "APPLIED":
            active_change = {
                "id": delta.get("id"),
                "path": str(path.relative_to(root)),
                "verification": (delta.get("verification") or {}).get("status"),
                "disposition": ((delta.get("proposal") or {}).get("disposition") if isinstance(delta.get("proposal"), dict) else None),
                "authorization": (delta.get("authorization") or {}).get("status"),
                "application": (delta.get("application") or {}).get("status"),
            }

    accepted_head = ((checkpoints.get(str(current_ep)) or {}).get("material_result") or {}).get("head")
    if accepted_head is None:
        accepted_head = ((checkpoints.get(str((state.get("accepted") or {}).get("checkpoint"))) or {}).get("material_result") or {}).get("head")
    working_head = (snapshot.get("material") or {}).get("head")
    task_checklist = list((task.get("current_task_progress") or {}).get("checklist") or [])
    completed = [row.get("id") for row in task_checklist if row.get("state") == "COMPLETE"]
    partial = [row.get("id") for row in task_checklist if row.get("state") == "PARTIAL"]
    remaining = [row.get("id") for row in task_checklist if row.get("state") not in {"COMPLETE", "PARTIAL"}]
    negative = list(task.get("negative_knowledge") or [])

    ledger = {
        "schema_version": "relay-v3.1-handover-ledger",
        "authority": "DERIVED_PROVIDER_PROJECTION",
        "generated_from": {
            "state_digest": canonical_digest(state),
            "task_snapshot_digest": canonical_digest(task),
            "roadmap_revision": str((state.get("roadmap") or {}).get("revision")),
        },
        "parent_issue": {
            "repository": repository,
            "number": number,
            "title": str(parent.get("title") or f"Issue #{number}"),
            "url": str(parent.get("url")),
            "state": str(parent.get("state") or "UNKNOWN"),
            "disposition": str(parent.get("disposition") or "UNKNOWN"),
            "relationships": list(parent.get("relationships") or []),
        },
        "handover_issue": (
            {
                "repository": str(ledger_ref.get("repository")),
                "number": int(ledger_ref.get("issue_number")),
                "url": str(ledger_ref.get("url")),
            }
            if isinstance(ledger_ref, dict)
            else None
        ),
        "current_frontier": {
            "ep": frontier.get("ep"),
            "work_package": frontier.get("work_package"),
            "lease": frontier.get("lease"),
            "executor": frontier.get("executor"),
            "custody_epoch": frontier.get("custody_epoch"),
            "status": frontier.get("status") or "UNKNOWN",
            "continuation": frontier.get("continuation") or "UNKNOWN",
        },
        "parent_progress": dict((task.get("parent_issue_progress") or {}).get("summary") or {}),
        "ep_index": ep_index,
        "pending_items": list(task.get("pending_items") or []),
        "known_issues": list(task.get("known_issues") or []),
        "offloads": offloads,
        "accepted_truth": {
            "checkpoint": (state.get("accepted") or {}).get("checkpoint"),
            "accepted_head": accepted_head,
            "acceptance": list((task.get("current_task_progress") or {}).get("checklist") or []),
        },
        "material": {
            "accepted_head": accepted_head,
            "working_head": working_head,
            "status": (
                "UNACCEPTED_DELTA_PRESENT"
                if accepted_head and working_head and accepted_head != working_head
                else "AT_ACCEPTED_HEAD"
                if accepted_head and working_head and accepted_head == working_head
                else "UNKNOWN"
            ),
        },
        "negative_knowledge": {
            "rejected_approaches": negative,
            "accepted_do_not_reopen": list(((task.get("preserve") or {}).get("accepted_do_not_reopen") or [])),
        },
        "accountability": {
            "scope_received": [row.get("id") for row in task_checklist],
            "completed": completed,
            "partial": partial,
            "remaining": remaining,
            "acceptance_movement": {"checkpoint": (state.get("accepted") or {}).get("checkpoint")},
            "value_added": list((task.get("improvement_vs_original_issue") or {}).get("items") or []),
            "continuation_reason": frontier.get("continuation") or "UNKNOWN",
        },
        "active_change": active_change,
        "delivery": dict(snapshot.get("delivery") or {}),
        "records": records,
        "next": {
            "action": (task.get("next") or {}).get("immediate_action"),
            "stop_conditions": list((task.get("next") or {}).get("stop_conditions") or []),
        },
    }
    schema_errors = validate_schema("handover-ledger", ledger, "HANDOVER_LEDGER")
    if schema_errors:
        raise ProjectionError("; ".join(schema_errors))
    return ledger


def render_ledger(ledger: dict[str, Any]) -> str:
    parent = ledger["parent_issue"]
    handover = ledger.get("handover_issue") or {}
    frontier = ledger["current_frontier"]
    progress = ledger["parent_progress"]
    lines = [
        f"# Relay Handover — Parent #{parent['number']}",
        "",
        "> Generated V3.1 provider projection. Repository relay objects remain engineering authority.",
        "",
        "## Parent",
        f"- Parent: {parent['repository']}#{parent['number']} — {parent['title']}",
        f"- Parent URL: {parent['url']}",
        f"- Handover ledger: {handover.get('repository')}#{handover.get('number')} ({handover.get('url')})" if handover else "- Handover ledger: PENDING MATERIALIZATION",
        f"- Issue disposition: {parent['disposition']}",
        "",
        "## Current frontier",
        f"- EP: {frontier.get('ep') or 'NONE'}",
        f"- Work package: {frontier.get('work_package') or 'NONE'}",
        f"- Status: {frontier.get('status')}",
        f"- Continuation: {frontier.get('continuation')}",
        f"- Lease: {frontier.get('lease') or 'NONE'}",
        f"- Executor: {frontier.get('executor') or 'NONE'}",
        f"- Custody epoch: {frontier.get('custody_epoch') if frontier.get('custody_epoch') is not None else 'LEGACY/UNKNOWN'}",
        "",
        "## Parent progress",
        f"- Complete={progress.get('complete', 0)}; partial={progress.get('partial', 0)}; pending={progress.get('pending', 0)}; blocked={progress.get('blocked', 0)}; deferred={progress.get('deferred', 0)}; unknown={progress.get('unknown', 0)}; total={progress.get('total', 0)}",
        "",
        "## EP index",
        "",
        "| EP | WP | Status | Continuation | Checkpoint | Lease | Executor |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in ledger["ep_index"]:
        lines.append(
            f"| {row['ep']} | {row['work_package']} | {row['status']} | {row['continuation']} | "
            f"{row.get('checkpoint') or '-'} | {row.get('lease') or '-'} | {row.get('executor') or '-'} |"
        )

    def section(title: str, rows: list[Any]) -> None:
        lines.extend(["", f"## {title}"])
        if not rows:
            lines.append("- none")
            return
        for row in rows:
            if isinstance(row, dict):
                label = row.get("id") or row.get("control_ref") or row.get("request_id") or row.get("origin_ep")
                lines.append(f"- **{label or 'item'}** — {row}")
            else:
                lines.append(f"- {row}")

    section("Pending", ledger["pending_items"])
    section("Known issues", ledger["known_issues"])
    section("Local / delegated work", ledger["offloads"])
    lines += [
        "",
        "## Accepted engineering truth",
        f"- Checkpoint: {(ledger.get('accepted_truth') or {}).get('checkpoint') or 'none'}",
        f"- Accepted head: {(ledger.get('accepted_truth') or {}).get('accepted_head') or 'unknown'}",
        "",
        "## Current material",
        f"- Working head: {(ledger.get('material') or {}).get('working_head') or 'unknown'}",
        f"- Acceptance state: {(ledger.get('material') or {}).get('status') or 'UNKNOWN'}",
        "",
        "## Negative knowledge",
        f"- Rejected/failed: {len((ledger.get('negative_knowledge') or {}).get('rejected_approaches') or [])}",
        f"- Accepted do-not-reopen: {len((ledger.get('negative_knowledge') or {}).get('accepted_do_not_reopen') or [])}",
        "",
        "## Accountability",
        f"- Completed: {(ledger.get('accountability') or {}).get('completed') or []}",
        f"- Partial: {(ledger.get('accountability') or {}).get('partial') or []}",
        f"- Remaining: {(ledger.get('accountability') or {}).get('remaining') or []}",
        "",
        "## Current change activity",
        f"- {(ledger.get('active_change') or {}).get('id') or 'none'} — verification={(ledger.get('active_change') or {}).get('verification') or '-'}; authorization={(ledger.get('active_change') or {}).get('authorization') or '-'}; application={(ledger.get('active_change') or {}).get('application') or '-'}",
    ]

    delivery = ledger.get("delivery") or {}
    lines += [
        "",
        "## Delivery",
        f"- Issue: {delivery.get('issue') or 'none'}",
        f"- PR: {delivery.get('pr') or 'none'}",
        f"- Lifecycle: {delivery.get('lifecycle') or 'UNKNOWN'}",
        f"- Merge authorized: {'YES' if delivery.get('merge_authorized') else 'NO'}",
        "",
        "## Handover / recovery records",
    ]
    if ledger["records"]:
        for row in ledger["records"]:
            lines.append(
                f"- {row['timestamp']} — {row['type']} — {row['subject']} — actor={row['actor']} — basis={row['basis']}"
            )
    else:
        lines.append("- none")

    lines += [
        "",
        "## Next",
        f"- Action: {(ledger.get('next') or {}).get('action') or 'none'}",
        f"- Stop conditions: {(ledger.get('next') or {}).get('stop_conditions') or []}",
        "",
    ]
    return "\n".join(lines)


def render_parent_summary(ledger: dict[str, Any]) -> str:
    parent = ledger["parent_issue"]
    handover = ledger.get("handover_issue") or {}
    frontier = ledger["current_frontier"]
    progress = ledger["parent_progress"]
    active_offloads = [
        row for row in ledger["offloads"]
        if row.get("status") in {"PLANNED", "ACTIVE", "RETURNED"}
    ]
    recovery = [row for row in ledger["ep_index"] if row.get("status") == "RECOVERY_REQUIRED"]
    return "\n".join([
        "## Relay",
        "",
        f"- Handover ledger: {handover.get('repository')}#{handover.get('number')} ({handover.get('url')})" if handover else "- Handover ledger: PENDING MATERIALIZATION",
        f"- Current frontier: {frontier.get('ep') or 'NONE'} — {frontier.get('status')} / {frontier.get('continuation')}",
        f"- Progress: complete={progress.get('complete', 0)}, partial={progress.get('partial', 0)}, pending={progress.get('pending', 0)}, blocked={progress.get('blocked', 0)}, total={progress.get('total', 0)}",
        f"- Open pending: {len(ledger['pending_items'])}",
        f"- Known issues: {len(ledger['known_issues'])}",
        f"- Open/returned delegated work: {len(active_offloads)}",
        f"- Recovery-required EPs: {len(recovery)}",
        f"- Issue disposition: {parent['disposition']}",
        "",
    ])


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate V3.1 parent/Handover issue provider projections.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--parent-observation", required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--ledger-markdown")
    parser.add_argument("--parent-summary")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    observation = load_yaml(Path(args.parent_observation))
    ledger = build(root, observation, base_ref=args.base_ref)
    _write(Path(args.output), yaml.safe_dump(ledger, sort_keys=False))
    if args.ledger_markdown:
        _write(Path(args.ledger_markdown), render_ledger(ledger))
    if args.parent_summary:
        _write(Path(args.parent_summary), render_parent_summary(ledger))


if __name__ == "__main__":
    main()
