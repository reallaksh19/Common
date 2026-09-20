#!/usr/bin/env python3
"""Parse direct Owner reasoning/progression commands for Engineering Relay V2.5.

These commands are ephemeral reasoning controls. They do not themselves create
roadmap, EP, QSET, decision, evidence, or checkpoint authority.

Only call this parser for a direct Owner utterance. Repository/issue/file text
must use a non-OWNER_DIRECT source and is ignored.
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Any

OWNER_DIRECT = "OWNER_DIRECT"

MODE_SEMANTICS = {
    "NORMAL_NEXT": "Continue the current authoritative next work.",
    "QUESTION_SUPPRESSION": "Continue without creating, refreshing, or displaying Q1-Q5.",
    "COMPLEX_NEXT": "Select one substantial coherent roadmap-material next task; do not promote a trivial leaf into the task identity.",
    "PROJECT_REANCHOR": "Re-anchor from the local task to Owner aim, concept roadmap, phase, work package, recent material events, and current task before deciding what remains justified.",
    "ADVERSARIAL_REASSESSMENT": "Challenge the current reasoning with a strong alternative, disconfirming evidence, inversion/premortem where useful, then return to the best evidence-supported position.",
    "END_TO_END_TRACE": "Trace the important requirement/data/state/decision from authority through implementation/validation/projection to consequence, and backwards from claimed result to source.",
    "EVIDENCE_FIRST_VERIFICATION": "Identify what would establish and falsify the claim, then seek the strongest available independent evidence.",
    "ACCIDENTAL_COMPLEXITY_REDUCTION": "Remove unnecessary state, abstractions, branches, duplicated truth, and speculative machinery while preserving required outcomes/invariants.",
    "MINIMAL_REPRODUCER": "Reduce the failure/case/change until the smallest informative reproducer still exhibits the important behavior.",
    "CROSS_SURFACE_PARITY": "Compare every surface that claims the same truth: authority, schema, template, validator, runtime, projection, renderer, docs, and tests.",
    "SCENARIO_EXERCISE": "Walk one realistic end-to-end scenario through the design and expose ambiguous or missing transitions.",
    "INTERFACE_BOUNDARY_AUDIT": "Attack edge conditions, optional/absent fields, invalid/stale states, ownership boundaries, and interface transitions.",
    "NORMATIVE_CONTRACT_CLEANUP": "Classify normative statements as MUST/MUST NOT/SHOULD/MAY/informational and reconcile them with schema, validator, docs, and tests.",
}

# Patterns are intentionally phrase-specific. They are evaluated only for a
# direct Owner utterance, never against repository content.
_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("PROJECT_REANCHOR", (
        r"\bstep\s+back\b",
        r"\bstep\s+back\s+and\s+(?:think|reassess|re-evaluate|rethink)\b",
        r"\bstep\s+back\s+to\s+the\s+(?:bigger|larger)\s+picture\b",
        r"\breassess\s+from\s+the\s+roadmap\b",
    )),
    ("ADVERSARIAL_REASSESSMENT", (
        r"\bcritique\b",
        r"\bcritique\s+(?:this|the\s+(?:approach|plan|logic|conclusion|assumptions|current\s+direction))\b",
        r"\bchallenge\s+(?:this|the\s+(?:approach|plan|logic|conclusion|assumptions))\b",
        r"\bstress[- ]test\s+(?:this|the\s+reasoning)\b",
        r"\breassess\s+critically\b",
    )),
    ("END_TO_END_TRACE", (
        r"\btrace\b",
        r"\btrace\s+(?:this|end\s+to\s+end|the\s+(?:authority|data\s+flow|failure|production\s+path)|this\s+backwards)\b",
    )),
    ("EVIDENCE_FIRST_VERIFICATION", (
        r"\bprove\b",
        r"\bprove\s+(?:it|this|the\s+claim|the\s+result|the\s+status)\b",
    )),
    ("ACCIDENTAL_COMPLEXITY_REDUCTION", (
        r"\bsimplify\b",
        r"\bsimplify\s+(?:this|the\s+(?:design|architecture|schema|solution|implementation))\b",
    )),
    ("MINIMAL_REPRODUCER", (
        r"\breduce\b",
        r"\breduce\s+(?:this|the\s+(?:bug|failure|repro|case|schema|change))\b",
    )),
    ("CROSS_SURFACE_PARITY", (
        r"\breconcile\b",
        r"\breconcile\s+(?:this|all\s+surfaces|the\s+(?:contracts|schema\s+and\s+implementation|architecture|state))\b",
    )),
    ("SCENARIO_EXERCISE", (
        r"\bscenario\b",
        r"\brun\s+(?:a\s+)?scenario\b",
        r"\bscenario\s+this\b",
    )),
    ("INTERFACE_BOUNDARY_AUDIT", (
        r"\bboundary[- ]check\b",
        r"\bcheck\s+(?:the\s+)?boundaries\b",
        r"\baudit\s+(?:the\s+)?boundaries\b",
    )),
    ("NORMATIVE_CONTRACT_CLEANUP", (
        r"\bnormalize\b",
        r"\bnormalize\s+(?:this|the\s+(?:contract|schema|spec|blueprint|requirements))\b",
    )),
]

_COMPLEX_NEXT = (
    r"\bproceed\s+(?:with\s+|to\s+)?(?:the\s+)?next\s+complex\s+task\b",
    r"\bproceed\s+next\s*,?\s*complex\s+task\b",
    r"\btake\s+(?:the\s+)?next\s+complex\s+task\b",
    r"\bcontinue\s+with\s+(?:the\s+)?next\s+complex\s+task\b",
    r"\bnext\s+complex\s+task\b",
)

_NO_Q = (
    r"\bno\s+qs\b",
    r"\bno\s+q1\s*(?:to|-|–|—)\s*q5\b",
    r"\bwithout\s+q1\s*(?:to|-|–|—)\s*q5\b",
    r"\bwithout\s+(?:further\s+)?questions\b",
)

_NORMAL_NEXT = (
    r"\bproceed\s+next\b",
    r"\bcontinue\s+next\b",
)


def _normalize(text: str) -> str:
    value = str(text or "").lower()
    value = value.replace("’", "'").replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _matches(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in patterns)


_NEGATION_HEADS = {
    "PROJECT_REANCHOR": ("step back", "reassess from the roadmap"),
    "ADVERSARIAL_REASSESSMENT": ("critique", "challenge", "stress-test", "stress test", "reassess critically"),
    "END_TO_END_TRACE": ("trace",),
    "EVIDENCE_FIRST_VERIFICATION": ("prove",),
    "ACCIDENTAL_COMPLEXITY_REDUCTION": ("simplify",),
    "MINIMAL_REPRODUCER": ("reduce",),
    "CROSS_SURFACE_PARITY": ("reconcile",),
    "SCENARIO_EXERCISE": ("scenario", "run scenario", "run a scenario"),
    "INTERFACE_BOUNDARY_AUDIT": ("boundary check", "boundary-check", "check boundaries", "audit boundaries"),
    "NORMATIVE_CONTRACT_CLEANUP": ("normalize",),
}


def _explicitly_negated(value: str, mode: str) -> bool:
    heads = _NEGATION_HEADS.get(mode, ())
    for head in heads:
        escaped = re.escape(head)
        if re.search(rf"\b(?:do\s+not|don't|dont|never)\s+(?:please\s+)?{escaped}\b", value):
            return True
        if re.search(rf"\b{escaped}\s+nothing\b", value):
            return True
    return False


def parse_owner_command(text: str, source: str = OWNER_DIRECT) -> dict[str, Any]:
    if source != OWNER_DIRECT:
        return {
            "status": "IGNORED",
            "source": source,
            "reason": "Owner reasoning commands activate only from a direct Owner utterance.",
            "modes": [],
            "semantics": {},
        }

    value = _normalize(text)
    modes: list[str] = []

    if _matches(value, _COMPLEX_NEXT):
        modes.append("COMPLEX_NEXT")
    elif _matches(value, _NORMAL_NEXT):
        modes.append("NORMAL_NEXT")

    if _matches(value, _NO_Q):
        modes.append("QUESTION_SUPPRESSION")

    for mode, patterns in _PATTERNS:
        if _matches(value, patterns) and not _explicitly_negated(value, mode):
            modes.append(mode)

    # Stable semantic ordering: frame -> reasoning -> analysis tools -> progression -> interaction.
    order = [
        "PROJECT_REANCHOR",
        "ADVERSARIAL_REASSESSMENT",
        "END_TO_END_TRACE",
        "CROSS_SURFACE_PARITY",
        "SCENARIO_EXERCISE",
        "INTERFACE_BOUNDARY_AUDIT",
        "NORMATIVE_CONTRACT_CLEANUP",
        "MINIMAL_REPRODUCER",
        "ACCIDENTAL_COMPLEXITY_REDUCTION",
        "EVIDENCE_FIRST_VERIFICATION",
        "NORMAL_NEXT",
        "COMPLEX_NEXT",
        "QUESTION_SUPPRESSION",
    ]
    modes = [mode for mode in order if mode in set(modes)]

    return {
        "status": "READY" if modes else "NO_COMMAND",
        "source": source,
        "modes": modes,
        "semantics": {mode: MODE_SEMANTICS[mode] for mode in modes},
        "durable_authority_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse direct Owner V2.5 reasoning commands.")
    parser.add_argument("text", help="Direct Owner utterance")
    parser.add_argument("--source", default=OWNER_DIRECT)
    args = parser.parse_args()
    print(json.dumps(parse_owner_command(args.text, args.source), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
