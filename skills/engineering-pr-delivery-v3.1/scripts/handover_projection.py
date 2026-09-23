from __future__ import annotations

from typing import Any


def render(snapshot: dict[str, Any], checkpoint: dict[str, Any] | None, task_snapshot: dict[str, Any] | None = None, improvement_view: dict[str, Any] | None = None) -> str:
    owner = snapshot.get("owner") or {}
    programme = snapshot.get("programme") or {}
    execution = snapshot.get("execution") or {}
    scope = snapshot.get("scope") or {}
    material = snapshot.get("material") or {}
    controls = snapshot.get("controls") or {}
    nxt = snapshot.get("next") or {}
    handoff = (checkpoint or {}).get("handoff") or {}

    lines = [
        "# Engineering Relay V3.1 Handover",
        "",
        "## Programme",
        f"- Outcome: {owner.get('outcome') or 'unknown'}",
        f"- Current goal: {owner.get('current_goal') or 'unknown'}",
        f"- Roadmap revision: {(snapshot.get('generated_from') or {}).get('roadmap_revision')}",
        f"- Programme progress: {programme.get('programme_progress')}%",
        f"- Accepted evidence coverage: {programme.get('accepted_progress')}%",
        "",
        "## Current execution",
        f"- Lifecycle: {execution.get('lifecycle')}",
        f"- Work package: {execution.get('work_package')}",
        f"- EP: {execution.get('ep')}",
        f"- Lease: {execution.get('lease')}",
        f"- Executor: {execution.get('executor')}",
        "",
        "## Material basis",
        f"- Base: {material.get('base')}",
        f"- Material head: {material.get('head')}",
        f"- Relevant paths digest: {material.get('relevant_paths_digest')}",
        f"- Dependency digest: {material.get('dependency_digest')}",
        "",
        "## Boundaries",
        f"- Allowed writes: {scope.get('allowed_writes') or []}",
        f"- Protected: {scope.get('protected') or []}",
        f"- Prohibited: {scope.get('prohibited') or []}",
        "",
        "## Controls by action plane",
        f"- Execution blockers: {controls.get('execution_blockers') or []}",
        f"- Handover blockers: {controls.get('handover_blockers') or []}",
        f"- Delivery blockers: {controls.get('delivery_blockers') or []}",
        "",
        "## Accepted checkpoint handoff",
    ]
    if checkpoint:
        lines.append(f"- Checkpoint: {checkpoint.get('id')}")
        for key, label in (
            ("what_changed", "What changed"),
            ("what_is_true_now", "What is true now"),
            ("what_remains_uncertain", "What remains uncertain"),
            ("do_not_break", "Do not break"),
            ("attempted_and_rejected", "Attempted and rejected"),
            ("resume_from", "Resume from"),
        ):
            lines.append(f"- {label}: {handoff.get(key) or []}")
        lines.append(f"- First successor action: {handoff.get('first_successor_action') or 'unknown'}")
    else:
        lines.append("- No accepted checkpoint handoff is available.")

    if task_snapshot:
        current = (task_snapshot.get("current_task_progress") or {}).get("summary") or {}
        parent = (task_snapshot.get("parent_issue_progress") or {}).get("summary") or {}
        parent_issue = task_snapshot.get("parent_issue") or {}
        lines += [
            "",
            "## Parent issue lineage",
            f"- Issue: {parent_issue.get('repository') or 'unknown'}#{parent_issue.get('number') or 'NONE'}",
            f"- Disposition: {parent_issue.get('disposition') or 'UNKNOWN'}",
            f"- Relationships: {parent_issue.get('relationships') or []}",
        ]
        lines += [
            "",
            "## Quantitative status",
            f"- Current task: complete={current.get('complete', 0)}, partial={current.get('partial', 0)}, pending={current.get('pending', 0)}, blocked={current.get('blocked', 0)}, total={current.get('total', 0)}",
            f"- Parent issue: complete={parent.get('complete', 0)}, partial={parent.get('partial', 0)}, pending={parent.get('pending', 0)}, blocked={parent.get('blocked', 0)}, deferred={parent.get('deferred', 0)}, total={parent.get('total', 0)}",
        ]

    if improvement_view:
        improvement = improvement_view.get("improvement") or {}
        lines += [
            "",
            "## Value added by this runner",
            f"- Capability added: {improvement.get('capability_added') or []}",
            f"- Capability strengthened: {improvement.get('capability_strengthened') or []}",
            f"- Evidence added: {improvement.get('evidence_added') or []}",
            f"- Understanding improved: {improvement.get('understanding_improved') or []}",
            f"- Downstream unlocked: {improvement.get('downstream_unlocked') or []}",
            f"- Not improved: {improvement_view.get('not_improved') or []}",
            f"- Still not proved: {improvement_view.get('still_not_proved') or []}",
            f"- New questions: {improvement_view.get('new_questions') or []}",
        ]

    lines += [
        "",
        "## Immediate next action",
        f"- {nxt.get('immediate_material_action') or 'none'}",
        f"- Stop conditions: {nxt.get('stop_conditions') or []}",
        "",
        "## Reconstruction sources",
    ]
    for source in (snapshot.get("handoff") or {}).get("reconstruction_sources") or []:
        lines.append(f"- {source}")
    return "\n".join(lines) + "\n"
