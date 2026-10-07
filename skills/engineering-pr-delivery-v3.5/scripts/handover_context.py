from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from snapshot_projection import build as build_snapshot
from intelligence_projection import build_improvement, build_task
from programme_reconciliation import build as build_programme_reconciliation
from v3lib import canonical_digest, load_yaml, validate_schema


PROMPT_SEQUENCE = ["PASS_1_SYSTEM_BASELINE", "PASS_2_IMPROVE_RECONCILE_PLAN"]
LAUNCHER = "skills/two-pass-prompt-generator/SKILL.md"
SCHEMA = "skills/two-pass-prompt-generator/schema.md"
VALIDATOR = "skills/two-pass-prompt-generator/validate.py"

SUCCESSOR_ENTRY_MODE = "RECONSTRUCT_PLAN_ONLY"
SUCCESSOR_ALLOWED_ACTIONS = [
    "READ_RECONSTRUCT",
    "RECONCILE_LIVE_TRUTH",
    "DRAFT_OR_UPDATE_PLAN",
    "ANSWER_SUCCESSOR_CHALLENGE",
]
SUCCESSOR_FORBIDDEN_ACTIONS = [
    "QUALIFICATION",
    "RETAINED_VALIDATION",
    "PRODUCTION_MUTATION",
    "PR_CREATION",
    "TASK_EXECUTION",
]
SUCCESSOR_EXECUTION_ADMISSION = "OWNER_EXPLICIT_EXECUTION_ADMISSION"


class HandoverContextError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _protocol_checkout_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _standalone_contract(protocol_root: Path | None = None) -> str:
    root = protocol_root or _protocol_checkout_root()
    schema_path = root / SCHEMA
    validator_path = root / VALIDATOR
    launcher_path = root / LAUNCHER
    for path in (launcher_path, schema_path, validator_path):
        if not path.exists():
            raise HandoverContextError(f"standalone two-pass component missing: {path}")
    schema_text = schema_path.read_text(encoding="utf-8")
    validator_text = validator_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^PROTOCOL REVISION:\s*\n?\s*(TPG-[A-Za-z0-9-]+)", schema_text)
    validator_match = re.search(r'EXPECTED_PROTOCOL_REVISION\s*=\s*"([^"]+)"', validator_text)
    if not match or not validator_match:
        raise HandoverContextError("cannot establish standalone two-pass protocol revision")
    revision = match.group(1)
    if revision != validator_match.group(1):
        raise HandoverContextError("standalone two-pass schema/validator revision mismatch")
    for token in (
        "TWO_PASS_ONLY",
        "## PASS 1 — INDEPENDENT SYSTEM BASELINE",
        "## PASS 2 — IMPROVE, RECONCILE, PLAN",
        "STEP-BACK RECONCILIATION",
        "Original Intent",
        "LOCAL_AGENT_FINDING",
        "RLL_TRANSPORT_ONLY",
        "IMPROVEMENT PROPOSAL",
        "APPROVAL REQUIRED",
    ):
        if token not in schema_text:
            raise HandoverContextError(f"standalone two-pass schema missing required surface: {token}")
    if "fetch `skills/two-pass-prompt-generator/schema.md` from current `main`" not in launcher_path.read_text(encoding="utf-8"):
        raise HandoverContextError("standalone launcher no longer requires a current-main schema fetch")
    return revision


def _wp_row(roadmap: dict[str, Any], wp_id: str | None) -> dict[str, Any] | None:
    for row in roadmap.get("work_packages") or []:
        if isinstance(row, dict) and str(row.get("id")) == str(wp_id):
            return row
    return None


def _validate_target(target: dict[str, Any]) -> None:
    errors = validate_schema("handover-target", target, "HANDOVER_TARGET")
    if errors:
        raise HandoverContextError("; ".join(errors))


def validate_visibility(context: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    blind = context.get("blind_context") or {}
    reality = context.get("reality_context") or {}
    blind_text = json.dumps(blind, sort_keys=True, ensure_ascii=False).lower()

    for token in (
        "lease-",
        "lease.",
        "pull_request",
        "pull request",
        "pr #",
        "coordination_head",
        "material_head",
        "execution_blockers",
        "delivery_blockers",
        "handover_blockers",
        "current_snapshot",
        "work_package",
        "acceptance_statements",
        "selected_frontier",
        "current_parent",
        "original_intent",
        "offload",
        "rll_",
    ):
        if token in blind_text:
            errors.append(f"blind_context contains reality-only token: {token}")

    execution = reality.get("execution") or {}
    material = reality.get("material") or {}
    dynamic_values = {
        "lease": execution.get("lease"),
        "executor": execution.get("executor"),
        "branch": execution.get("branch"),
        "material_head": material.get("head"),
        "coordination_head": material.get("coordination_head"),
    }
    for label, value in dynamic_values.items():
        text = str(value or "").strip()
        if text and len(text) >= 5 and text.lower() in blind_text:
            errors.append(f"blind_context leaks current {label}: {text}")

    return errors




def _successor_entry(context: dict[str, Any], challenge_count: int | None) -> dict[str, Any]:
    if challenge_count is None:
        count = 0
    elif isinstance(challenge_count, bool) or not isinstance(challenge_count, int) or not (0 <= challenge_count <= 10):
        raise HandoverContextError("successor_challenge_count must be an integer from 0 to 10")
    else:
        count = challenge_count

    learning = context.get("accumulated_learning") or {}
    reality = context.get("reality_context") or {}
    material = reality.get("material") or {}
    execution = reality.get("execution") or {}
    reconstruction = learning.get("reconstruction_context") or {}
    task_snapshot = (learning.get("task_snapshot") or {}).get("value") or {}
    target_state = str((context.get("target") or {}).get("state") or "UNKNOWN")
    latest_reconciliation = reconstruction.get("latest_reconciliation") or {}
    latest_reconciliation_ref = str(latest_reconciliation.get("ref") or "").strip() or None
    latest_reconciliation_summary = str(latest_reconciliation.get("summary") or "").strip() or None
    inherited_first_action = str(learning.get("first_successor_action") or "").strip() or None
    current_task_next = str(((task_snapshot.get("next") or {}).get("immediate_action")) or "").strip() or None
    terminal_target = target_state in {"CLOSED", "MERGED"}
    advanced_frontier = bool(latest_reconciliation_ref or latest_reconciliation_summary or terminal_target)
    if latest_reconciliation_ref or latest_reconciliation_summary:
        freshness = "CURRENT_RECONCILIATION_SUPERSEDES_HANDOFF"
    elif terminal_target:
        freshness = "TERMINAL_TARGET_REQUIRES_RECONCILIATION"
    else:
        freshness = "HANDOFF_FRONTIER_ACTIVE"
    if advanced_frontier:
        decision = current_task_next or "VERIFY_CURRENT_DISPOSITION_AND_NEXT_CONSUMER"
    else:
        decision = inherited_first_action or current_task_next or "the next bounded engineering decision"

    anchors: list[str] = []
    for value in (
        (context.get("target") or {}).get("provider_ref"),
        f"material_head:{material.get('head')}" if material.get("head") else None,
        f"branch:{execution.get('branch')}" if execution.get("branch") else None,
        ((reconstruction.get("original_intent") or {}).get("source_ref")),
        ((reconstruction.get("original_intent") or {}).get("url")),
        ((reconstruction.get("latest_reconciliation") or {}).get("ref")),
    ):
        text = str(value or "").strip()
        if text and text not in anchors:
            anchors.append(text)
    for value in list(reconstruction.get("roadmap_refs") or []) + list(reconstruction.get("primary_conversation_refs") or []):
        text = str(value or "").strip()
        if text and text not in anchors:
            anchors.append(text)
        if len(anchors) >= 8:
            break

    unresolved = [str(x).strip() for x in learning.get("what_remains_uncertain") or [] if str(x).strip()]
    rejected = [str(x).strip() for x in learning.get("attempted_and_rejected") or [] if str(x).strip()]
    invariants = [str(x).strip() for x in learning.get("do_not_break") or [] if str(x).strip()]
    invariants.extend(str(x).strip() for x in reality.get("task_constraints") or [] if str(x).strip())

    uncertainty = unresolved[0] if unresolved else "the earliest owning layer / root classification is not yet proven"
    negative = rejected[0] if rejected else "do not repeat an unproven predecessor repair direction"
    invariant = invariants[0] if invariants else "preserve currently accepted behavior and authority boundaries"
    anchor_text = ", ".join(anchors[:3]) or "current repository/provider truth"
    current_frontier = (
        latest_reconciliation_summary
        or (f"provider target state {target_state}" if terminal_target else None)
        or "the predecessor-observed handover frontier"
    )
    if advanced_frontier:
        q1 = (
            f"The predecessor handover may be stale: current frontier is {current_frontier}. Before {decision}, reconstruct the exact "
            f"current implementation path in the live repository and verify which owning layer(s) actually remain active or landed. "
            f"Use {anchor_text}; cite current files/functions and exact material/provider evidence. Do not reopen the inherited task "
            "unless live evidence contradicts the current reconciliation, and state one observation that would falsify your disposition."
        )
        q2 = (
            f"For {decision}, classify the live evidence and authority boundaries against the current frontier: {current_frontier}. "
            f"The historical handover uncertainty was: {uncertainty}. Verify whether that inherited uncertainty is still active rather "
            "than asserting it as current. Distinguish production authority, candidate-generation evidence, review-only evidence, "
            "validation/benchmark evidence and historical evidence, and state which source must not be promoted into production authority."
        )
        q3 = (
            f"Before {decision}, reconstruct the current upstream/downstream responsibility and consumer boundaries from live provider "
            f"truth. Current frontier: {current_frontier}. Treat inherited action {inherited_first_action or 'NONE'} as history only; "
            f"preserve this invariant: {invariant}, and retain negative knowledge: {negative}. State whether this responsibility is still "
            "open for coding or already complete/landed, and identify the exact current evidence needed before any further material work."
        )
    else:
        q1 = (
            f"Before {decision}, reconstruct the exact current implementation path in the live repository from the relevant "
            f"entry point to the owned mutation boundary. Use {anchor_text}; cite current files/functions and exact material/provider "
            "evidence, identify the earliest owning layer, and state one observation that would falsify that ownership."
        )
        q2 = (
            f"For {decision}, classify the live evidence and authority boundaries that govern the decision. Resolve this current "
            f"uncertainty: {uncertainty}. Use repository/provider evidence, distinguish production authority, candidate-generation "
            "evidence, review-only evidence, validation/benchmark evidence and historical evidence, and state which source must not "
            "be promoted into production authority."
        )
        q3 = (
            f"Before {decision}, reconstruct the upstream and downstream responsibility boundaries and the exact material/evidence "
            f"frontier. Explain why adjacent layers do not own the next change, preserve this invariant: {invariant}, and account for "
            f"negative knowledge: {negative}. State the exact evidence/root classification required before coding."
        )

    base_questions = [
        {
            "question": q1,
            "required_evidence": [
                "current repository file/function call path",
                "exact material head and live provider readback",
                "evidence that locates the earliest owning layer",
            ],
            "authority_distinctions": [
                "production semantics vs candidate generation",
                "current exact evidence vs predecessor assertion",
            ],
            "falsifier": "A live repository/provider observation shows the proposed owning layer is downstream of an earlier proven loss.",
            "pass_condition": "Names current files/functions and exact live refs, locates an owning layer, and gives a falsifier.",
            "fail_condition": "Can be answered from issue prose, generic architecture knowledge, or predecessor conclusions alone.",
            "forbidden_shortcuts": [
                "do not answer from handover prose alone",
                "do not assume the predecessor diagnosis is current truth",
                "do not start implementation while ownership is unproved",
            ],
            "downstream_consequence": "Determines which bounded child may legitimately own the next material change.",
        },
        {
            "question": q2,
            "required_evidence": [
                "current authority-defining code/schema or governing contract",
                "live evidence/source classification",
                "contradictory or limiting evidence where present",
            ],
            "authority_distinctions": [
                "production authority",
                "candidate-generation-only",
                "review-only",
                "validation/benchmark-only",
                "historical/not-current",
            ],
            "falsifier": "A governing current contract gives a supposedly non-authoritative source direct production authority.",
            "pass_condition": "Classifies each load-bearing source by current authority and resolves the uncertainty with live evidence.",
            "fail_condition": "Treats READY/PASS/benchmark coincidence or predecessor prose as identity/production authority without contract evidence.",
            "forbidden_shortcuts": [
                "do not promote benchmark expected output into matching authority",
                "do not equate status readiness with semantic correctness",
                "do not collapse historical evidence into exact-head evidence",
            ],
            "downstream_consequence": "Prevents a repair from being justified by the wrong evidence class.",
        },
        {
            "question": q3,
            "required_evidence": [
                "current parent/child/dependency graph or issue/PR relationships",
                "exact material and semantic/evidence frontier",
                "negative knowledge / rejected approach evidence",
                "explicit pre-coding proof or root classification",
            ],
            "authority_distinctions": [
                "upstream cause vs downstream compensation",
                "plan/decomposition authority vs execution evidence",
            ],
            "falsifier": "An upstream or adjacent responsibility is shown by current evidence to own the first causal loss.",
            "pass_condition": "Names upstream/downstream boundaries, exact frontier, protected invariant, negative knowledge and the pre-coding proof.",
            "fail_condition": "Proposes a PR/fix before current ownership/root classification is established.",
            "forbidden_shortcuts": [
                "do not compensate downstream for an unlocated upstream defect",
                "do not repeat an already-rejected approach without new evidence",
                "do not create a PR merely because a plausible patch is visible",
            ],
            "downstream_consequence": "Controls whether the successor may propose the next bounded implementation child.",
        },
    ]

    questions: list[dict[str, Any]] = []
    for index in range(count):
        if index < len(base_questions):
            row = dict(base_questions[index])
        else:
            subject = unresolved[(index - 3) % len(unresolved)] if unresolved else invariant
            subject_label = (
                f"historical inherited uncertainty {subject!r}; verify whether it remains active against {current_frontier}"
                if advanced_frontier
                else f"successor uncertainty {subject!r}"
            )
            row = {
                "question": (
                    f"Resolve {subject_label} before {decision}. Reconstruct the answer from current repository/provider evidence, "
                    "explain its effect on the decision at risk, and state a falsifier."
                ),
                "required_evidence": ["current repository/provider evidence tied to the stated uncertainty"],
                "authority_distinctions": ["current exact evidence vs inherited assertion"],
                "falsifier": "Current repository/provider evidence contradicts the proposed resolution.",
                "pass_condition": "Resolves the uncertainty with current refs and a falsifier.",
                "fail_condition": "Answers generically or only from inherited prose.",
                "forbidden_shortcuts": ["do not execute the task to discover the answer", "do not treat inherited prose as current truth"],
                "downstream_consequence": "Decides whether the next engineering step remains safe.",
            }
        row.update(
            {
                "id": f"Q{index + 1}",
                "decision_at_risk": str(decision),
                "repository_anchors": list(anchors),
            }
        )
        questions.append(row)

    return {
        "mode": SUCCESSOR_ENTRY_MODE,
        "allowed_actions": list(SUCCESSOR_ALLOWED_ACTIONS),
        "forbidden_actions": list(SUCCESSOR_FORBIDDEN_ACTIONS),
        "execution_admission": SUCCESSOR_EXECUTION_ADMISSION,
        "challenge_basis": {
            "freshness": freshness,
            "target_state": target_state,
            "latest_reconciliation_ref": latest_reconciliation_ref,
            "latest_reconciliation_summary": latest_reconciliation_summary,
            "current_task_next": current_task_next,
            "inherited_first_successor_action": inherited_first_action,
            "inherited_uncertainties": unresolved,
            "inherited_negative_knowledge": rejected,
            "protected_invariants": invariants,
        },
        "successor_reconstruction_challenge": questions,
    }


def build_context(
    root: Path,
    *,
    base_ref: str,
    target: dict[str, Any],
    complex_mode: bool,
    parent_issue_observation: dict[str, Any] | None = None,
    programme_reconciliation: dict[str, Any] | None = None,
    task_snapshot_override: dict[str, Any] | None = None,
    improvement_view_override: dict[str, Any] | None = None,
    protocol_root: Path | None = None,
    successor_challenge_count: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _validate_target(target)
    # Custody preparation is independent of the optional standalone reasoning
    # generator. Keep protocol_root/complex_mode in the call signature for
    # compatibility with historical callers, but do not resolve Two-Pass assets
    # while constructing a handover context.
    snapshot = build_snapshot(root, base_ref)
    state = load_yaml(root / "relay/STATE.yaml")
    roadmap = load_yaml(root / str((state.get("roadmap") or {}).get("path")))

    execution = snapshot.get("execution") or {}
    ep_id = execution.get("ep")
    lease_id = execution.get("lease")
    checkpoint_id = (snapshot.get("evidence") or {}).get("latest_checkpoint")
    checkpoint = load_yaml(root / "relay/CHECKPOINTS" / f"{checkpoint_id}.yaml") if checkpoint_id else None

    context_ep_id = ep_id or ((checkpoint or {}).get("ep"))
    context_ep = load_yaml(root / "relay/WORK" / f"{context_ep_id}.yaml") if context_ep_id else None
    context_wp_id = execution.get("work_package") or ((context_ep or {}).get("work_package"))
    wp = _wp_row(roadmap, context_wp_id)
    handoff = (checkpoint or {}).get("handoff") or {}
    task_snapshot = task_snapshot_override or build_task(root, base_ref, parent_issue_observation)
    improvement_view = improvement_view_override or build_improvement(root)
    task_identity = task_snapshot.get("identity") or {}
    task_reconstruction = task_snapshot.get("reconstruction_context")
    if not isinstance(task_reconstruction, dict):
        task_reconstruction = {
            "original_intent": None,
            "latest_reconciliation": None,
            "primary_conversation_refs": [],
            "roadmap_refs": [],
            "local_agent_refs": [],
            "rll_refs": [],
        }
    task_continuity = task_snapshot.get("continuity")
    if not isinstance(task_continuity, dict):
        task_continuity = {
            "current": None,
            "further_tasks": [],
            "predecessor_ref": None,
        }
    improvement = improvement_view.get("improvement") or {}
    capability_change = bool(
        improvement.get("capability_added")
        or improvement.get("capability_strengthened")
    )
    evidence_count = len(improvement.get("evidence_added") or [])
    reconciliation = programme_reconciliation or build_programme_reconciliation(
        [],
        current_parent_ref=None,
    )

    context = {
        "schema_version": "relay-v3.1-handover-context",
        "authority": "DERIVED_HANDOVER_INPUT",
        "frozen_at": _now(),
        "frozen_basis": {
            "roadmap_revision": (snapshot.get("generated_from") or {}).get("roadmap_revision"),
            "state_digest": (snapshot.get("generated_from") or {}).get("state_digest"),
            "target_digest": canonical_digest(target),
            "material_head": (snapshot.get("material") or {}).get("head"),
            "relevant_paths_digest": (snapshot.get("material") or {}).get("relevant_paths_digest"),
            "dependency_digest": (snapshot.get("material") or {}).get("dependency_digest"),
            "coordination_head": (snapshot.get("generated_from") or {}).get("coordination_head"),
            "checkpoint": checkpoint_id,
            "ep": ep_id,
            "lease": lease_id,
        },
        "target": target,
        "blind_context": {
            "programme": {
                "outcome": (snapshot.get("owner") or {}).get("outcome"),
                "roadmap_title": roadmap.get("title"),
            },
            # Task/EP constraints are intentionally excluded here. If a consumer has
            # genuinely repository-wide constraints, it may add them explicitly.
            "stable_constraints": [],
        },
        "reality_context": {
            "programme_reconciliation": reconciliation,
            "local_responsibility": {
                "work_package": context_wp_id,
                "title": (wp or {}).get("title"),
                "outcome": ((context_ep or {}).get("outcome") or {}).get("statement") or (wp or {}).get("title"),
                "acceptance_statements": [
                    str(item.get("statement"))
                    for item in ((context_ep or {}).get("acceptance") or [])
                    if isinstance(item, dict) and str(item.get("statement") or "").strip()
                ],
            },
            "task_constraints": list(((context_ep or {}).get("scope") or {}).get("prohibit") or []),
            "execution": {
                "lifecycle": execution.get("lifecycle"),
                "ep": ep_id,
                "lease": lease_id,
                "executor": execution.get("executor"),
                "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
            },
            "material": {
                "base": (snapshot.get("material") or {}).get("base"),
                "head": (snapshot.get("material") or {}).get("head"),
                "relevant_paths_digest": (snapshot.get("material") or {}).get("relevant_paths_digest"),
                "dependency_digest": (snapshot.get("material") or {}).get("dependency_digest"),
                "coordination_head": (snapshot.get("generated_from") or {}).get("coordination_head"),
            },
            "evidence": snapshot.get("evidence") or {},
            "controls": snapshot.get("controls") or {},
            "delivery": snapshot.get("delivery") or {},
        },
        "accumulated_learning": {
            "checkpoint": checkpoint_id,
            "discoveries": list((checkpoint or {}).get("discoveries") or []),
            "known_limitations": list((checkpoint or {}).get("known_limitations") or []),
            "what_changed": list(handoff.get("what_changed") or []),
            "what_is_true_now": list(handoff.get("what_is_true_now") or []),
            "what_remains_uncertain": list(handoff.get("what_remains_uncertain") or []),
            "do_not_break": list(handoff.get("do_not_break") or []),
            "attempted_and_rejected": list(handoff.get("attempted_and_rejected") or []),
            "resume_from": list(handoff.get("resume_from") or []),
            "first_successor_action": handoff.get("first_successor_action"),
            "reconstruction_context": task_reconstruction,
            "continuity": task_continuity,
            "task_snapshot": {
                "digest": canonical_digest(task_snapshot),
                "source_protocol": task_snapshot.get("source_protocol"),
                "ep": task_identity.get("ep"),
                "work_package": task_identity.get("work_package"),
                "next_action": (task_snapshot.get("next") or {}).get("immediate_action"),
                "value": task_snapshot,
            },
            "improvement_view": {
                "digest": canonical_digest(improvement_view),
                "source_protocol": improvement_view.get("source_protocol"),
                "checkpoint": improvement_view.get("checkpoint"),
                "capability_change": capability_change,
                "evidence_count": evidence_count,
                "value": improvement_view,
            },
            "parent_issue": {
                "repository": (task_snapshot.get("parent_issue") or {}).get("repository"),
                "number": (task_snapshot.get("parent_issue") or {}).get("number"),
                "disposition": (task_snapshot.get("parent_issue") or {}).get("disposition") or "UNKNOWN",
                "relationships": list((task_snapshot.get("parent_issue") or {}).get("relationships") or []),
            },
        },
    }
    context["successor_entry"] = _successor_entry(context, successor_challenge_count)
    errors = validate_schema("handover-context", context, "HANDOVER_CONTEXT")
    errors.extend(validate_visibility(context))
    if errors:
        raise HandoverContextError("; ".join(errors))
    return context, snapshot


def build_request(
    context: dict[str, Any],
    *,
    complex_mode: bool | None = None,
    protocol_root: Path | None = None,
) -> dict[str, Any]:
    """Explicitly derive a Two-Pass reasoning request from custody context.

    PLAN_HANDOVER never calls this helper. The standalone protocol handshake
    therefore belongs to the explicit reasoning-request operation, not to
    custody preparation.
    """
    visibility_errors = validate_visibility(context)
    if visibility_errors:
        raise HandoverContextError("; ".join(visibility_errors))
    blind = context["blind_context"]
    target = context["target"]

    legacy_generator = context.get("generator_contract") or {}
    selected_complex_mode = (
        bool(legacy_generator.get("complex_mode", False))
        if complex_mode is None
        else bool(complex_mode)
    )
    revision = _standalone_contract(protocol_root)
    generator = {
        "canonical_launcher": LAUNCHER,
        "canonical_schema": SCHEMA,
        "canonical_validator": VALIDATOR,
        "protocol_revision_at_freeze": revision,
        "generator_mode": "TWO_PASS_ONLY",
        "live_main_fetch_required": True,
        "prompt_sequence": list(PROMPT_SEQUENCE),
        "complex_mode": selected_complex_mode,
        "approval_boundary_required": True,
    }
    request = {
        "schema_version": "relay-v3.1-two-pass-request",
        "authority": "DERIVED_GENERATOR_REQUEST",
        "target": target,
        "handover_context": {
            "path": "relay/GENERATED/HANDOVER_CONTEXT.yaml",
            "digest": canonical_digest(context),
        },
        "generator": {
            "launcher": generator["canonical_launcher"],
            "schema": generator["canonical_schema"],
            "validator": generator["canonical_validator"],
            "mode": generator["generator_mode"],
            "live_main_fetch_required": True,
            "prompt_sequence": list(generator["prompt_sequence"]),
            "complex_mode": generator["complex_mode"],
            "approval_boundary_required": generator["approval_boundary_required"],
        },
        "user_input": {
            "target": target["url"],
            "repository": target["repository"],
            "human_goal": blind["programme"]["outcome"],
            "user_intent": "Generate the current standalone two-pass handover. Pass 1 independently reconstructs the live repository/application without exposing the actual issue/task, provenance history or execution continuity or asking for a next action. Pass 2 uses that baseline plus the actual task, accumulated reconstruction refs and latest AGENT_STATUS_V1/Further task continuity to reconcile Original Intent, current Owner/Roadmap authority, EP responsibility, relevant primary-agent reasoning, execution continuity, Local Agent/OFFLOAD evidence, RLL transport and live material truth before proposing high-ROI improvements and a draft engineering plan; it stops for Owner approval before durable plan/EP/implementation actions.",
            "authorized_actions": "The generated prompts grant no production authority. Pass 2 may publish the approved implementation plan, bind/create EPs and refresh Task Snapshot/Handover only after explicit Owner approval; material execution occurs only when the Owner-approved action boundary and real provider/tool permissions allow it.",
            "intent_boundary": "Pass 1 may inspect the live repository/application but must not receive or reveal the actual issue/task, Original Intent source, prior agent conversation/reconciliation, AGENT_STATUS_V1/Further task, Local Agent/OFFLOAD or RLL task history, current PR, requested change, Improvement Proposal or further action. Pass 2 must distinguish historical intent, current Owner/Roadmap authority, agent reasoning, mutable execution continuity, delegated evidence, RLL transport and material truth; stale AGENT_STATUS never outranks live material truth; prefer no improvement over speculation; reject rewrites/scope expansion; keep adjacent proposals in separate responsibilities; and pause before durable publication or implementation until Owner approval.",
            "intent_completion_test": "The standalone generator fetches its canonical schema from current main, emits exactly Pass 1 and Pass 2, validates the artifact, and Pass 2 contains an explicit Owner approval boundary plus the post-approval issue/EP/Task-Snapshot/Handover continuation.",
            "context_rule": "Read relay/GENERATED/HANDOVER_CONTEXT.yaml only after the schema handshake. For Pass 1 use only blind_context: repository/system identity comes from this request, while blind_context supplies broad programme outcome/title and any genuinely global stable constraints. Do not use reality_context or accumulated_learning when generating Pass 1. Pass 1 asks for live system understanding and ends without recommendations. Pass 2 consumes the Pass-1 result, then reads reality_context plus accumulated_learning.reconstruction_context and accumulated_learning.continuity and refreshes target/provider/material reality; reconcile in order Original Intent -> current Owner/Roadmap amendments -> EP/owned issue + current plan -> relevant primary-agent reasoning -> latest AGENT_STATUS_V1/Further task -> Local Agent/OFFLOAD evidence -> RLL transport -> PR/tests/runtime -> latest TASK_EVIDENCE/TASK_RESULT -> Task Snapshot/Handover. Revalidate every unresolved FT-* item against live material truth before carrying it forward. Emit STEP-BACK RECONCILIATION before any high-ROI Improvement Proposal, then draft IMPLEMENTATION_PLAN in chat, stop for Owner approval, and after approval publish on the original issue and update EP/Task Snapshot/Handover.",
        },
    }
    errors = validate_schema("two-pass-request", request, "TWO_PASS_REQUEST")
    if errors:
        raise HandoverContextError("; ".join(errors))
    return request


def render_request(request: dict[str, Any]) -> str:
    user = request["user_input"]
    gen = request["generator"]
    qline = (
        "DEEP MODE: ON — increase evidence depth and quantitative analysis inside the same two passes; do not add stages."
        if gen["complex_mode"]
        else "DEEP MODE: OFF."
    )
    return f"""TARGET:
{user['target']}

REPOSITORY / SYSTEM:
{user['repository']}

HUMAN GOAL:
{user['human_goal']}

USER INTENT:
{user['user_intent']}

AUTHORIZED ACTIONS:
{user['authorized_actions']}

INTENT BOUNDARY:
{user['intent_boundary']}

INTENT COMPLETION TEST:
{user['intent_completion_test']}

OTHER CONTEXT:
{user['context_rule']}

GENERATOR BINDING:
Fetch {gen['schema']} from current main during generation. Use {gen['launcher']} as launcher and {gen['validator']} as validator. GENERATOR MODE = {gen['mode']}. Do not treat the frozen protocol revision or this request as a substitute for the required live schema fetch.

{qline}
"""
