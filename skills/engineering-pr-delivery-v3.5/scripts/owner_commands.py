#!/usr/bin/env python3
"""Parse direct Owner intent without destroying the Owner's original request.

The parser is intentionally side-effect free. For a direct Owner utterance it
preserves a lossless OWNER_INTENT envelope, then derives the legacy scalar
intent/workflow compatibility view. The caller must execute governed Relay
operations and provider reads/writes separately.

Repository, issue, file, fixture, and quoted text MUST NOT activate Owner intent.
The envelope is capture/normalization evidence only and creates no durable
permission, lifecycle, merge, review, or production authority.
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Any

OWNER_DIRECT = "OWNER_DIRECT"

INTENT_SEMANTICS = {
    "WHAT_NEXT": (
        "Reconcile live programme reality before recommending any continuation. "
        "Read the governing parent/child issue set, provider state, ROADMAP, accepted "
        "evidence, Owner decisions and open obligations; report the real next frontier "
        "without admitting or executing it."
    ),
    "PROCEED_NEXT": (
        "Proceed to the next task justified by the reconciled programme and current "
        "roadmap. Do not mechanically continue the last EP and do not invent a new task "
        "when the existing plan already determines the next obligation."
    ),
    "PROCEED_NEXT_COMPLEX": (
        "Step back to the whole programme/task before progressing. Reconcile parents, "
        "children, roadmap, evidence, blockers, stale plans and Owner decisions; choose "
        "one substantial coherent task rather than a convenient patch or leaf file."
    ),
    "PLAN_HANDOVER": (
        "Prepare a governed custody handover: reconcile live programme/roadmap truth, "
        "freeze the predecessor-observed handover context, update/synchronize the provider "
        "handover issue, and publish the handover package. Custody transfer does not itself "
        "authorize replanning or an independent reconstruction request."
    ),
    "STATS": (
        "Report current detailed programme/task statistics against the governing parent "
        "issue and relevant sub-issues in point-wise checklist form. Separate completed, "
        "partial, pending, blocked, deferred, acceptance debt, delivery/governance debt "
        "and delegated/local work. Do not progress execution."
    ),
    "TAKEOVER_RECONCILE": (
        "An explicit new-agent/takeover/lateral-entry command is stronger than ordinary continuation. "
        "Cold-reconstruct parent/roadmap/provider truth, refresh the phase-wise plan and parent status, create "
        "the next bounded child issue/comment block, publish recovery TASK_EVIDENCE first when the predecessor "
        "ended abnormally, then run ordinary DELP admission before coding only that bounded child. Publish "
        "TASK_EVIDENCE at execution end before selecting another child. Never continue from chat memory."
    ),
    "CONTINUE_RECONCILE": (
        "A bare same-agent continuation command (continue, proceed, next, resume, reconcile, keep going) "
        "means reconstruct and reconcile BEFORE continuing; it never means continue from conversational "
        "memory. Resolve the owned leaf responsibility and its lineage, observe the live PR/candidate, compare "
        "the latest evidence frontier with it, repair any evidence gap first, reproject titles and status "
        "from facts, read the provider back, surface the compact CONTINUE CHECKPOINT, then execute exactly "
        "the next bounded unit. It never changes the parent, denominator, scope, priority or merge authority."
    ),
    "PREPARE_LOCAL_AGENT": (
        "Prepare a recipient-ready local-agent work packet with repository/clone basis, "
        "branch and exact HEAD, task purpose, technical context, bounded steps, scope, "
        "acceptance, commands, stop/prohibition rules, and a required return/update target "
        "for the governed sub-issue. The helper does not inherit Relay custody."
    ),
}

WORKFLOWS = {
    "WHAT_NEXT": {
        "boundary": "NEXT_WORK",
        "progress_execution": False,
        "steps": [
            "Read live governing parent and relevant child/sub-issue observations.",
            "Run canonical ordered programme reconciliation.",
            "Determine the explicit Owner/ROADMAP selected execution frontier separately from all still-real programme obligations.",
            "Compare provider reality with ROADMAP, accepted checkpoints, Owner decisions, pending/KI controls, delivery state and stale/open work.",
            "Separate selected frontier, alternate live obligations, execution blockers, acceptance debt, delivery/governance debt and deferred/future work.",
            "If the selected frontier is blocked, report that it remains selected and execution-blocked; do not laterally jump to another live branch without a new Owner/programme selection.",
            "Treat an execution blocker as an execution restriction only: it does not grant programme reselection authority and is not proof that one external/provider action is the only legitimate action.",
            "Report the selected still-real frontier and why; do not admit or execute it.",
        ],
        "requires": ["programme_parent_observations"],
    },
    "PROCEED_NEXT": {
        "boundary": "NEXT_WORK",
        "progress_execution": True,
        "steps": [
            "Reconcile live parent/child programme reality before selecting execution.",
            "Resolve the explicit Owner/ROADMAP selected execution frontier separately from other unfinished work.",
            "If the selected frontier is execution-blocked, stop on that blocker while keeping the same selected frontier; do not switch to another live branch merely to stay busy or without Owner/programme reselection.",
            "Do not present an execution blocker as programme authority or as proof that one external/provider action is the only legitimate action.",
            "If the current EP is still the selected frontier, continue it; if Owner/programme selection moved, do not revive the stale EP.",
            "If IDLE and a different selected task is next, admit exactly that governed task before execution.",
            "Preserve normal lease, scope, material-drift and checkpoint gates.",
            "Before executing the selected unit, run the DELP continuation admission (reconstruct lineage, observe the live candidate, repair any evidence gap, reproject from facts, read back) and surface the compact CONTINUE CHECKPOINT.",
        ],
        "requires": ["programme_parent_observations"],
    },
    "PROCEED_NEXT_COMPLEX": {
        "boundary": "NEXT_WORK",
        "progress_execution": True,
        "steps": [
            "Step back from the current patch/file/EP and re-anchor on Owner outcome and governing parent set.",
            "Reconcile parent/child provider reality, ROADMAP, accepted evidence, open controls, delivery obligations, stale PRs/work and Owner decisions.",
            "Distinguish unfinished obligations from the one Owner/ROADMAP selected execution frontier.",
            "Challenge whether the apparent next patch or currently ACTIVE work package is actually the selected programme obligation.",
            "Choose one substantial coherent task with an explicit outcome/acceptance boundary.",
            "Only then continue/admit execution under ordinary Relay custody and safety gates.",
            "Before executing, run the DELP continuation admission (reconstruct lineage, observe the live candidate, repair any evidence gap, reproject from facts, read back) and surface the compact CONTINUE CHECKPOINT.",
        ],
        "requires": ["programme_parent_observations", "whole_task_reassessment"],
    },
    "PLAN_HANDOVER": {
        "boundary": "HANDOVER",
        "progress_execution": False,
        "steps": [
            "Reconcile live parent/child programme reality and ROADMAP before freezing continuation.",
            "Refresh task/improvement/project read models from durable truth.",
            "Create HANDOVER_PLANNED with the canonical programme reconciliation bound into the context.",
            "Generate full handover documentation and provider Relay/Handover ledger projection.",
            "Create/update and verify the governed GitHub handover sub-issue using provider readback.",
            "Publish the matching handover artifact (HANDOVER_PUBLISHED).",
            "Materialize any explicitly requested Successor Reconstruction Challenge inside the handover package; questions must protect the next engineering decision and require live repository/provider evidence.",
            "Successor entry is RECONSTRUCT_PLAN_ONLY until explicit Owner execution admission: no qualification, retained validation, production mutation, PR creation or task execution merely because custody moved.",
            "Do not generate a new Two-Pass/replanning request merely because custody is being prepared; reasoning is separate and must be explicitly requested or independently required by the governing responsibility.",
            "Do not claim HANDOVER_ACCEPTED until a successor actually accepts custody.",
        ],
        "requires": ["handover_target_observation", "programme_parent_observations", "provider_handover_issue_readback"],
    },
    "STATS": {
        "boundary": "READ_ONLY",
        "progress_execution": False,
        "steps": [
            "Read live governing parent and relevant child/sub-issue observations.",
            "Build the current task snapshot, programme reconciliation and handover ledger.",
            "Render every parent acceptance item as a checklist row with state and evidence.",
            "Render relevant sub-issues with ownership/disposition and acceptance summary.",
            "Render current EP acceptance, pending items, known issues, delegated/local work, accepted checkpoint/head and unaccepted delta.",
            "Show programme frontier, blockers, acceptance debt, delivery/governance debt and deferred/future work separately.",
        ],
        "requires": ["programme_parent_observations"],
    },
    "TAKEOVER_RECONCILE": {
        "boundary": "RECONCILE_PLAN_DECOMPOSE_THEN_EXECUTE",
        "progress_execution": True,
        "steps": [
            "Cold-reconstruct the governing parent, relevant children, ROADMAP, accepted evidence and live provider state; never use chat memory as authority.",
            "Refresh and publish the phase-wise implementation plan and parent status against current roadmap/provider reality before selecting code.",
            "Create or update the next bounded child issue/comment block with outcome, scope/write surface, acceptance and stop condition before any coding.",
            "Inspect predecessor termination and the evidence frontier. If the prior epoch ended because of stream, memory, GitHub/provider/tool failure, or material exists without end evidence, publish TASK_EVIDENCE — RECOVERY before any new coding.",
            "Run the ordinary DELP continuation admission: resolve lineage, observe the live candidate, materialize missing facts, fix an unreleasable plan, recover stale evidence, reproject and read back before execution.",
            "Execute exactly the bounded child block; do not broaden parent, denominator, scope, priority, review or merge authority.",
            "At execution end publish TASK_EVIDENCE for the exact candidate and child outcome before selecting or decomposing another child.",
            "For the next agent or next child, repeat this sequence from durable GitHub truth; never continue from conversational memory.",
        ],
        "requires": [
            "programme_parent_observations",
            "roadmap_state",
            "leaf_responsibility",
            "live_candidate_observation",
            "bounded_child_block",
            "delp_projection",
        ],
    },
    "CONTINUE_RECONCILE": {
        "boundary": "RECONSTRUCT_THEN_CONTINUE",
        "progress_execution": True,
        "steps": [
            "Resolve the owned leaf responsibility from durable truth (issue/PR/execution graph), never from chat history.",
            "Resolve the full lineage: root programme, intermediate responsibility, leaf, current PR and current candidate SHA.",
            "Observe the live PR head/candidate and read the latest valid CHECKPOINT_FACTS_V1 evidence for the leaf.",
            "Compare the evidence frontier with the live candidate; if units are complete without current evidence, publish recovery evidence before any new coding.",
            "Recompute the projection (leaf P/E, ancestor D/E, frontier, titles) from facts with the DELP projector; never hand-edit a title or percentage.",
            "Write the projection with compare-and-swap and read it back from the provider.",
            "Surface the compact CONTINUE CHECKPOINT: PATH, CHILD, EVIDENCE, PARENT, ROOT, BLOCKER, OWNER_ACTION, NEXT.",
            "Execute exactly the next bounded unit; do not change parent, denominator, scope, priority or merge authority.",
        ],
        "requires": ["leaf_responsibility", "live_candidate_observation", "delp_projection"],
    },
    "PREPARE_LOCAL_AGENT": {
        "boundary": "LOCAL_EXECUTION_EXPORT",
        "progress_execution": False,
        "steps": [
            "Resolve the bounded offload/task and governed return sub-issue before dispatch.",
            "Export a LOCAL_EXECUTION package from current durable Relay truth and exact material HEAD.",
            "Include canonical repository clone/fetch basis, branch, exact HEAD and working-directory preflight.",
            "Include full task purpose, EP/WP context, allowed/protected scope, acceptance/evidence requirements, exact commands when known, stop conditions and prohibited actions.",
            "Require the helper to return the typed result contract and update the specified sub-issue with outcome/evidence/artifacts.",
            "Keep Relay custody with the originating owner; returned helper evidence is immutable input to later acceptance.",
        ],
        "requires": ["base_ref", "return_sub_issue"],
    },
}

_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("PROCEED_NEXT_COMPLEX", (
        r"\bproceed\s+(?:with\s+|to\s+)?(?:the\s+)?next\s+complex\s+task\b",
        r"\bproceed\s+next\s*,?\s*complex\s+task\b",
        r"\bcontinue\s+(?:with\s+)?(?:the\s+)?next\s+complex\s+task\b",
        r"\btake\s+(?:the\s+)?next\s+complex\s+task\b",
        r"\bnext\s+complex\s+task\b",
        r"\bproceed\s+(?:with\s+)?(?:the\s+)?next\s+substantial\s+task\b",
    )),
    ("PLAN_HANDOVER", (
        r"\bplan\s+(?:for\s+)?(?:the\s+)?handover\b",
        r"\bprepare\s+(?:for\s+)?(?:the\s+)?handover\b",
        r"\bprepare\s+(?:a\s+)?handover\s+plan\b",
        r"\bmake\s+(?:the\s+)?handover\s+plan\b",
        r"\bhandover\s+plan\b",
        r"\bhand\s*over\s+ready\b",
    )),
    ("PREPARE_LOCAL_AGENT", (
        r"\bprepare\s+(?:for\s+)?(?:the\s+|a\s+)?local\s+agent\b",
        r"\bprepare\s+(?:the\s+)?local\s+agent\b",
        r"\bprepare\s+(?:a\s+)?local\s+agent\s+(?:packet|request|instructions?)\b",
        r"\bcreate\s+(?:the\s+|a\s+)?local\s+agent\s+(?:packet|request|instructions?)\b",
        r"\blocal\s+agent\s+(?:packet|request|instructions?)\b",
        r"\bprepare\s+(?:for\s+)?local\s+execution\b",
    )),
    ("STATS", (
        r"^\s*stats?\s*[?!.,]*\s*$",
        r"\bshow\s+(?:me\s+)?(?:the\s+)?(?:current\s+)?(?:detailed\s+)?stats?\b",
        r"\bcurrent\s+(?:detailed\s+)?statistics\b",
        r"\bshow\s+(?:me\s+)?(?:the\s+)?(?:parent\s+issue|issue|task)\s+(?:status|checklist|statistics)\b",
        r"\bstatus\s+against\s+(?:the\s+)?parent\s+issue\b",
        r"\bparent\s+issue\s+stats?\b",
    )),
    ("WHAT_NEXT", (
        r"^\s*what\s+next\s*[?!.,]*\s*$",
        r"\bwhat\s+should\s+(?:we|i)\s+do\s+next\b",
        r"\bwhat(?:'s|\s+is)\s+next\b",
        r"\bwhat\s+is\s+(?:the\s+)?next\s+(?:real\s+)?(?:task|work|step|frontier)\b",
        r"\bfigure\s+out\s+what\s+next\b",
    )),
    ("PROCEED_NEXT", (
        r"\bproceed\s+(?:with\s+|to\s+)?(?:the\s+)?next(?:\s+task)?\b",
        r"\bproceed\s+next\b",
        r"\bcontinue\s+(?:with\s+|to\s+)?(?:the\s+)?next(?:\s+task)?\b",
        r"\bmove\s+(?:on\s+)?to\s+(?:the\s+)?next\s+task\b",
        r"\btake\s+(?:the\s+)?next\s+task\b",
    )),
    # Explicit executor transfer/lateral entry. Kept separate from same-agent continuation because it must
    # refresh the phase plan and bounded child block before any coding.
    ("TAKEOVER_RECONCILE", (
        r"^\s*(?:take\s+over|takeover|lateral\s+entry|enter\s+laterally|new\s+agent\s+takeover|walk\s+through\s+as\s+(?:a\s+)?new\s+agent)"
        r"(?:\s+(?:please|now))?\s*[?!.,]*\s*$",
    )),
    # Bare same-agent continuation commands. Anchored so ordinary sentences never activate it.
    ("CONTINUE_RECONCILE", (
        r"^\s*(?:continue|proceed|next|resume|reconcile|keep\s+going|carry\s+on)"
        r"(?:\s+(?:please|now))?\s*[?!.,]*\s*$",
    )),
]

# Lower-level reasoning modes retained from V2.5 compatibility. They compose with
# the high-level intent rather than changing its workflow identity.
_REASONING_PATTERNS = {
    "PROJECT_REANCHOR": (r"\bstep\s+back\b", r"\breassess\s+from\s+the\s+roadmap\b"),
    "ADVERSARIAL_REASSESSMENT": (
        r"\bcritique\b",
        r"\bchallenge\s+(?:this|the\s+plan|the\s+approach|the\s+direction)\b",
        r"\bstress[- ]test\b",
        r"\badversarial\b",
    ),
    "CROSS_SURFACE_PARITY": (r"\breconcile\s+all\s+surfaces\b",),
    "EVIDENCE_FIRST_VERIFICATION": (r"\bprove\s+(?:it|this)\b",),
    "ACCIDENTAL_COMPLEXITY_REDUCTION": (r"\bsimplify\b",),
}
_NO_Q = (
    r"\bno\s+qs\b",
    r"\bno\s+q1\s*(?:to|-|–|—)\s*q5\b",
    r"\bwithout\s+(?:further\s+)?questions\b",
)


_PRIMARY_PURPOSE_BY_INTENT = {
    "WHAT_NEXT": "STATUS_ONLY",
    "PROCEED_NEXT": "EXECUTE_TASK",
    "PROCEED_NEXT_COMPLEX": "RECONCILE_AND_PLAN",
    "PLAN_HANDOVER": "TRANSFER_CUSTODY",
    "STATS": "STATUS_ONLY",
    "TAKEOVER_RECONCILE": "EXECUTE_TASK",
    "CONTINUE_RECONCILE": "EXECUTE_TASK",
    "PREPARE_LOCAL_AGENT": "PREPARE_DELEGATION",
}

_NO_QUALIFICATION = (
    r"\bno\s+qualification\b",
    r"\bdo\s+not\s+(?:run|perform)\s+qualification\b",
)
_NO_RETAINED_VALIDATION = (
    r"\bno\s+retained\s+validation\b",
    r"\bdo\s+not\s+(?:run|perform)\s+retained\s+validation\b",
)
_NO_PRODUCTION_MUTATION = (
    r"\bdo\s+not\s+(?:modify|change|edit|touch)\s+production(?:\s+code)?\b",
    r"\bno\s+production\s+(?:mutation|code\s+changes?)\b",
)
_NO_PR_CREATION = (
    r"\bdo\s+not\s+(?:create|open)\s+(?:a\s+)?(?:product\s+)?pr\b",
    r"\bno\s+(?:product\s+)?pr\s+creation\b",
)
_NO_TASK_EXECUTION = (
    r"\bdo\s+not\s+(?:start|execute|run)\s+(?:the\s+)?(?:next\s+)?(?:task|unit|c\d+(?:[- ]execution)?)\b",
    r"\bno\s+(?:task|unit)\s+execution\b",
)

_NO_REPLAN = (
    r"\bdo\s+not\s+replan\b",
    r"\bdon't\s+replan\b",
    r"\bno\s+replan(?:ning)?\b",
    r"\bwithout\s+replanning\b",
    r"\bdo\s+not\s+(?:create|make)\s+(?:a\s+)?new\s+plan\b",
)

_PRESERVE_TARGET = (
    r"\bpreserve\s+(?P<ref>#\d+)\s+as\s+(?:the\s+)?(?:active\s+)?responsibility\b",
    r"\bkeep\s+(?P<ref>#\d+)\s+as\s+(?:the\s+)?(?:active\s+)?responsibility\b",
)

_EXACT_QUESTION_COUNT = re.compile(
    r"\bexactly\s+(?P<count>\d+)\s+(?:successor\s+|repo(?:sitory)?[- ]grounded\s+)?questions?\b",
    flags=re.IGNORECASE,
)


def _extract_target(value: str, explicit_target: Any) -> Any:
    if explicit_target is not None:
        return explicit_target
    for pattern in _PRESERVE_TARGET:
        match = re.search(pattern, value, flags=re.IGNORECASE)
        if match:
            return {"ref": match.group("ref")}
    return None


def _primary_purpose(intent: str | None, reasoning_modes: list[str]) -> str:
    if intent in _PRIMARY_PURPOSE_BY_INTENT:
        return _PRIMARY_PURPOSE_BY_INTENT[intent]
    if "ADVERSARIAL_REASSESSMENT" in reasoning_modes:
        return "ASSURE_DIRECTION"
    if "PROJECT_REANCHOR" in reasoning_modes:
        return "RECONCILE_AND_PLAN"
    return "OTHER"


def _requested_deliverables(
    value: str,
    intent: str | None,
) -> list[dict[str, Any]]:
    deliverables: list[dict[str, Any]] = []
    if intent == "PLAN_HANDOVER":
        deliverables.append({"type": "HANDOVER_PACKAGE"})
    elif intent == "STATS":
        deliverables.append({"type": "STATUS_REPORT"})
    elif intent == "WHAT_NEXT":
        deliverables.append({"type": "NEXT_FRONTIER_REPORT"})
    elif intent == "PREPARE_LOCAL_AGENT":
        deliverables.append({"type": "LOCAL_AGENT_PACKET"})
    elif intent == "TAKEOVER_RECONCILE":
        deliverables.extend(
            [
                {"type": "ENTRY_RECONCILIATION"},
                {"type": "PHASE_PLAN_REFRESH"},
                {"type": "BOUNDED_CHILD_BLOCK"},
                {"type": "TASK_EVIDENCE_AT_EXECUTION_END"},
            ]
        )

    count_match = _EXACT_QUESTION_COUNT.search(value)
    has_questions = bool(re.search(r"\bquestions?\b", value))
    successor_context = bool(
        intent == "PLAN_HANDOVER"
        or re.search(
            r"\b(?:successor|next\s+agent|understand\s+the\s+repo)\b",
            value,
        )
    )
    asks_successor_questions = has_questions and successor_context
    if asks_successor_questions:
        challenge: dict[str, Any] = {"type": "SUCCESSOR_RECONSTRUCTION_CHALLENGE"}
        if count_match:
            challenge["count"] = int(count_match.group("count"))
        deliverables.append(challenge)
    return deliverables


def _custody_intent(value: str, intent: str | None) -> str:
    if intent == "PLAN_HANDOVER":
        return "PREPARE_TRANSFER"
    if intent == "TAKEOVER_RECONCILE":
        return "RECOVERY"
    if intent in {"CONTINUE_RECONCILE", "PROCEED_NEXT", "PROCEED_NEXT_COMPLEX"}:
        return "CONTINUE"
    return "CONTINUE"


def _boundary_constraints(value: str, target: Any, intent: str | None) -> list[str]:
    constraints: list[str] = []
    if intent == "TAKEOVER_RECONCILE":
        constraints.extend(
            [
                "PHASE_PLAN_REFRESH_BEFORE_CODING",
                "BOUNDED_CHILD_BLOCK_BEFORE_CODING",
                "RECOVERY_TASK_EVIDENCE_BEFORE_NEW_CODING_IF_ABNORMAL_PREDECESSOR",
                "TASK_EVIDENCE_AT_EXECUTION_END",
            ]
        )
    if _matches(value, _NO_REPLAN):
        constraints.append("NO_REPLAN")
    for patterns, label in (
        (_NO_QUALIFICATION, "NO_QUALIFICATION"),
        (_NO_RETAINED_VALIDATION, "NO_RETAINED_VALIDATION"),
        (_NO_PRODUCTION_MUTATION, "NO_PRODUCTION_MUTATION"),
        (_NO_PR_CREATION, "NO_PR_CREATION"),
        (_NO_TASK_EXECUTION, "NO_TASK_EXECUTION"),
    ):
        if _matches(value, patterns):
            constraints.append(label)
    if target is not None and any(
        re.search(pattern, value, flags=re.IGNORECASE)
        for pattern in _PRESERVE_TARGET
    ):
        constraints.append("PRESERVE_TARGET")
    count_match = _EXACT_QUESTION_COUNT.search(value)
    successor_context = bool(
        re.search(
            r"\b(?:handover|hand\s*over|successor|next\s+agent|understand\s+the\s+repo)\b",
            value,
        )
    )
    if count_match and successor_context:
        constraints.append(
            f"EXACT_SUCCESSOR_CHALLENGE_COUNT:{int(count_match.group('count'))}"
        )
    return constraints


def _owner_intent_envelope(
    text: str,
    value: str,
    intent: str | None,
    reasoning_modes: list[str],
    suppress_questions: bool,
    *,
    source_ref: str | None,
    authority_ref: str | None,
    target: Any,
) -> dict[str, Any]:
    resolved_target = _extract_target(value, target)
    modifiers = list(reasoning_modes)
    if suppress_questions:
        modifiers.append("NO_FURTHER_QUESTIONS")
    return {
        "verbatim_request": text,
        "source_ref": source_ref,
        "primary_purpose": _primary_purpose(intent, reasoning_modes),
        "requested_deliverables": _requested_deliverables(value, intent),
        "target": resolved_target,
        "custody_intent": _custody_intent(value, intent),
        "assurance_request": (
            "ADVERSARIAL"
            if "ADVERSARIAL_REASSESSMENT" in reasoning_modes
            else "STANDARD"
        ),
        "modifiers": modifiers,
        "boundary_constraints": _boundary_constraints(value, resolved_target, intent),
        "authority_ref": authority_ref,
    }


def _normalize(text: str) -> str:
    value = str(text or "").lower()
    value = value.replace("’", "'").replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _matches(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in patterns)


def parse_owner_command(
    text: str,
    source: str = OWNER_DIRECT,
    *,
    source_ref: str | None = None,
    authority_ref: str | None = None,
    target: Any = None,
) -> dict[str, Any]:
    if source != OWNER_DIRECT:
        return {
            "status": "IGNORED",
            "source": source,
            "owner_intent": None,
            "intent": None,
            "reasoning_modes": [],
            "workflow": None,
            "reason": "Owner command intents activate only from a direct Owner utterance.",
        }

    verbatim = str(text or "")
    value = _normalize(verbatim)
    intent = None
    for candidate, patterns in _PATTERNS:
        if _matches(value, patterns):
            intent = candidate
            break

    reasoning_modes = [
        mode for mode, patterns in _REASONING_PATTERNS.items()
        if _matches(value, patterns)
    ]
    if intent == "PROCEED_NEXT_COMPLEX" and "PROJECT_REANCHOR" not in reasoning_modes:
        reasoning_modes.insert(0, "PROJECT_REANCHOR")

    suppress_questions = _matches(value, _NO_Q)
    owner_intent = _owner_intent_envelope(
        verbatim,
        value,
        intent,
        reasoning_modes,
        suppress_questions,
        source_ref=source_ref,
        authority_ref=authority_ref,
        target=target,
    )

    if not intent and not reasoning_modes:
        return {
            "status": "NO_COMMAND",
            "source": source,
            "owner_intent": owner_intent,
            "intent": None,
            "reasoning_modes": [],
            "workflow": None,
            "question_suppression": suppress_questions,
            "durable_authority_created": False,
        }

    workflow = dict(WORKFLOWS[intent]) if intent else None
    return {
        "status": "READY",
        "source": source,
        "owner_intent": owner_intent,
        "intent": intent,
        "semantics": INTENT_SEMANTICS.get(intent),
        "reasoning_modes": reasoning_modes,
        "question_suppression": suppress_questions,
        "workflow": workflow,
        "durable_authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preserve lossless Owner intent and derive Relay workflow compatibility."
    )
    parser.add_argument("text", help="Direct Owner utterance")
    parser.add_argument("--source", default=OWNER_DIRECT)
    parser.add_argument("--source-ref")
    parser.add_argument("--authority-ref")
    parser.add_argument("--target")
    args = parser.parse_args()
    print(
        json.dumps(
            parse_owner_command(
                args.text,
                args.source,
                source_ref=args.source_ref,
                authority_ref=args.authority_ref,
                target=args.target,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
