from __future__ import annotations

from typing import Any


def render(snapshot: dict[str, Any], checkpoint: dict[str, Any] | None) -> str:
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
        f"- Accepted progress: {programme.get('accepted_progress')}%",
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
