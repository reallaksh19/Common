#!/usr/bin/env python3
"""Parse direct Owner command intents for Engineering Relay V3.1.

This parser is intentionally side-effect free. It classifies a direct Owner
utterance into stable workflow intents; the caller must execute the referenced
governed Relay operations and provider reads/writes.

Repository, issue, file, fixture, and quoted text MUST NOT activate Owner intent.
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
        "Prepare a full governed handover: reconcile programme/roadmap truth, freeze the "
        "handover context, update/synchronize the provider handover issue, publish the "
        "handover package, and prepare the live standalone three-pass request."
    ),
    "STATS": (
        "Report current detailed programme/task statistics against the governing parent "
        "issue and relevant sub-issues in point-wise checklist form. Separate completed, "
        "partial, pending, blocked, deferred, acceptance debt, delivery/governance debt "
        "and delegated/local work. Do not progress execution."
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
            "Prepare the current standalone three-pass request (Prompt 0.5/1/2/2.5/3); complex mode includes the full whole-task reasoning surface.",
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
]

# Lower-level reasoning modes retained from V2.5 compatibility. They compose with
# the high-level intent rather than changing its workflow identity.
_REASONING_PATTERNS = {
    "PROJECT_REANCHOR": (r"\bstep\s+back\b", r"\breassess\s+from\s+the\s+roadmap\b"),
    "ADVERSARIAL_REASSESSMENT": (r"\bcritique\b", r"\bchallenge\s+(?:this|the\s+plan|the\s+approach)\b", r"\bstress[- ]test\b"),
    "CROSS_SURFACE_PARITY": (r"\breconcile\s+all\s+surfaces\b",),
    "EVIDENCE_FIRST_VERIFICATION": (r"\bprove\s+(?:it|this)\b",),
    "ACCIDENTAL_COMPLEXITY_REDUCTION": (r"\bsimplify\b",),
}
_NO_Q = (
    r"\bno\s+qs\b",
    r"\bno\s+q1\s*(?:to|-|–|—)\s*q5\b",
    r"\bwithout\s+(?:further\s+)?questions\b",
)


def _normalize(text: str) -> str:
    value = str(text or "").lower()
    value = value.replace("’", "'").replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _matches(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in patterns)


def parse_owner_command(text: str, source: str = OWNER_DIRECT) -> dict[str, Any]:
    if source != OWNER_DIRECT:
        return {
            "status": "IGNORED",
            "source": source,
            "intent": None,
            "reasoning_modes": [],
            "workflow": None,
            "reason": "Owner command intents activate only from a direct Owner utterance.",
        }

    value = _normalize(text)
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

    if not intent and not reasoning_modes:
        return {
            "status": "NO_COMMAND",
            "source": source,
            "intent": None,
            "reasoning_modes": [],
            "workflow": None,
            "question_suppression": suppress_questions,
        }

    workflow = dict(WORKFLOWS[intent]) if intent else None
    return {
        "status": "READY",
        "source": source,
        "intent": intent,
        "semantics": INTENT_SEMANTICS.get(intent),
        "reasoning_modes": reasoning_modes,
        "question_suppression": suppress_questions,
        "workflow": workflow,
        "durable_authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse direct Owner V3.1 workflow commands.")
    parser.add_argument("text", help="Direct Owner utterance")
    parser.add_argument("--source", default=OWNER_DIRECT)
    args = parser.parse_args()
    print(json.dumps(parse_owner_command(args.text, args.source), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
