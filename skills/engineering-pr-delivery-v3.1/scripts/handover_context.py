from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from snapshot_projection import build as build_snapshot
from intelligence_projection import build_improvement, build_task
from v3lib import canonical_digest, load_yaml, validate_schema


PROMPT_SEQUENCE = ["PROMPT_0_5", "PROMPT_1", "PROMPT_2", "PROMPT_2_5", "PROMPT_3"]
LAUNCHER = "skills/three-pass-prompt-generator/SKILL.md"
SCHEMA = "skills/three-pass-prompt-generator/schema.md"
VALIDATOR = "skills/three-pass-prompt-generator/validate.py"


class HandoverContextError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _standalone_contract(root: Path) -> str:
    schema_path = root / SCHEMA
    validator_path = root / VALIDATOR
    launcher_path = root / LAUNCHER
    for path in (launcher_path, schema_path, validator_path):
        if not path.exists():
            raise HandoverContextError(f"standalone three-pass component missing: {path}")
    schema_text = schema_path.read_text(encoding="utf-8")
    validator_text = validator_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^PROTOCOL REVISION:\s*\n?\s*(TPG-[A-Za-z0-9-]+)", schema_text)
    validator_match = re.search(r'EXPECTED_PROTOCOL_REVISION\s*=\s*"([^"]+)"', validator_text)
    if not match or not validator_match:
        raise HandoverContextError("cannot establish standalone three-pass protocol revision")
    revision = match.group(1)
    if revision != validator_match.group(1):
        raise HandoverContextError("standalone three-pass schema/validator revision mismatch")
    for token in (
        "THREE_PASS_ONLY",
        "## PROMPT 0.5 — IMAGINE FROM PROGRAMME",
        "## PROMPT 1 — IMAGINE",
        "## PROMPT 2 — UNDERSTAND",
        "## PROMPT 2.5 — RECONCILE REALITY AND DIRECTION",
        "## PROMPT 3 — REVALIDATE AND MOVE FORWARD",
        "COMPLEX Q1–Q5 COVERAGE:",
    ):
        if token not in schema_text:
            raise HandoverContextError(f"standalone three-pass schema missing required surface: {token}")
    if "Fetch `skills/three-pass-prompt-generator/schema.md` from current `main`" not in launcher_path.read_text(encoding="utf-8"):
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
        "pull_request",
        "pull request",
        "pr #",
        "coordination_head",
        "material_head",
        "execution_blockers",
        "delivery_blockers",
        "handover_blockers",
        "current_snapshot",
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


def build_context(
    root: Path,
    *,
    base_ref: str,
    target: dict[str, Any],
    complex_mode: bool,
    parent_issue_observation: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _validate_target(target)
    revision = _standalone_contract(root)
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
    task_snapshot = build_task(root, base_ref, parent_issue_observation)
    improvement_view = build_improvement(root)
    task_identity = task_snapshot.get("identity") or {}
    task_ep = task_identity.get("ep") or context_ep_id
    task_path = f"relay/GENERATED/tasks/{task_ep or 'current'}.snapshot.yaml"
    improvement_cp = improvement_view.get("checkpoint") or checkpoint_id
    improvement_path = f"relay/GENERATED/improvements/{improvement_cp or 'current'}.improvement.yaml"
    improvement = improvement_view.get("improvement") or {}
    capability_change = bool(
        improvement.get("capability_added")
        or improvement.get("capability_strengthened")
    )
    evidence_count = len(improvement.get("evidence_added") or [])

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
                "current_goal": (snapshot.get("owner") or {}).get("current_goal"),
                "roadmap_revision": (snapshot.get("generated_from") or {}).get("roadmap_revision"),
                "roadmap_title": roadmap.get("title"),
            },
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
            "stable_constraints": list(((context_ep or {}).get("scope") or {}).get("prohibit") or []),
        },
        "reality_context": {
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
            "task_snapshot": {
                "path": task_path,
                "digest": canonical_digest(task_snapshot),
                "source_protocol": task_snapshot.get("source_protocol"),
                "ep": task_identity.get("ep"),
                "work_package": task_identity.get("work_package"),
                "next_action": (task_snapshot.get("next") or {}).get("immediate_action"),
            },
            "improvement_view": {
                "path": improvement_path,
                "digest": canonical_digest(improvement_view),
                "source_protocol": improvement_view.get("source_protocol"),
                "checkpoint": improvement_view.get("checkpoint"),
                "capability_change": capability_change,
                "evidence_count": evidence_count,
            },
            "parent_issue": {
                "repository": (task_snapshot.get("parent_issue") or {}).get("repository"),
                "number": (task_snapshot.get("parent_issue") or {}).get("number"),
                "disposition": (task_snapshot.get("parent_issue") or {}).get("disposition") or "UNKNOWN",
                "relationships": list((task_snapshot.get("parent_issue") or {}).get("relationships") or []),
            },
        },
        "generator_contract": {
            "canonical_launcher": LAUNCHER,
            "canonical_schema": SCHEMA,
            "canonical_validator": VALIDATOR,
            "protocol_revision_at_freeze": revision,
            "generator_mode": "THREE_PASS_ONLY",
            "live_main_fetch_required": True,
            "prompt_sequence": list(PROMPT_SEQUENCE),
            "complex_mode": bool(complex_mode),
            "prompt1_q1_q5_required": bool(complex_mode),
        },
    }
    errors = validate_schema("handover-context", context, "HANDOVER_CONTEXT")
    errors.extend(validate_visibility(context))
    if errors:
        raise HandoverContextError("; ".join(errors))
    return context, snapshot


def build_request(context: dict[str, Any]) -> dict[str, Any]:
    visibility_errors = validate_visibility(context)
    if visibility_errors:
        raise HandoverContextError("; ".join(visibility_errors))
    blind = context["blind_context"]
    target = context["target"]
    generator = context["generator_contract"]
    request = {
        "schema_version": "relay-v3.1-three-pass-request",
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
            "prompt1_q1_q5_required": generator["prompt1_q1_q5_required"],
        },
        "user_input": {
            "target": target["url"],
            "human_goal": blind["programme"]["outcome"],
            "user_intent": "Generate the current standalone five-prompt handover for the provider-verified target using the frozen V3 handover context.",
            "authorized_actions": "This handover package grants no new action authority. Prompt 3 must revalidate live relay.can(action) and explicit Owner authority before acting.",
            "intent_boundary": "Use blind_context for Prompts 0.5/1; quarantine reality_context until Prompt 2; treat accumulated_learning as accepted/history context rather than present action authority.",
            "intent_completion_test": "The standalone generator fetches its canonical schema from current main, emits exactly Prompt 0.5 / 1 / 2 / 2.5 / 3, and validates the artifact against that live schema.",
            "context_rule": "Read relay/GENERATED/HANDOVER_CONTEXT.yaml after the standalone schema handshake. blind_context may shape Prompts 0.5/1; reality_context is reserved for Prompt 2 onward; accumulated_learning must not be silently contradicted without new evidence.",
        },
    }
    errors = validate_schema("three-pass-request", request, "THREE_PASS_REQUEST")
    if errors:
        raise HandoverContextError("; ".join(errors))
    return request


def render_request(request: dict[str, Any]) -> str:
    user = request["user_input"]
    gen = request["generator"]
    qline = (
        "COMPLEX MODE: ON — preserve visible target-specific Q1–Q5 inside Prompt 1 per the live standalone schema."
        if gen["complex_mode"]
        else "COMPLEX MODE: OFF."
    )
    return f"""TARGET:
{user['target']}

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
