#!/usr/bin/env python3
"""Internal-semantics -> learner-copy boundary (M-UPGRADE-2 item 9).

PR #323's RCA, RC-4: reasoning roles, evidence ids, route-state labels and pipeline
vocabulary are correct machine objects, but they were rendered too directly because no
contract separated internal semantics from learner copy.

**This module does not own a ban-list.** #351 established
``LearnerProduct/policies/math-learner-language-policy.json`` as the central learner-language
authority — approved public labels plus forbidden internal terms — and
``run_learner_product.py`` binds it by policy id. What was missing was an engine that scans
actual text against it, and one gap in its coverage: an internal *role* label
(``RECONSTRUCT``, ``CONTRAST``, ``VERIFY``) printed as a learner heading is the same defect
class as pipeline jargon but is not matched by a substring ban-list.

So:

* the policy file is the authority and was extended in place (same ``policy_id``) with
  ``forbidden_learner_role_labels``, ``internal_role_label_public_titles`` and
  ``internal_identifier_patterns``;
* this module is the detector all three consumer stages share;
* Core1A's original hardcoded list is unioned in rather than replaced, so adopting the
  policy can only widen what Core1A already caught.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
DEFAULT_CONSUMERS = PHASE / "registry" / "math-learner-copy-registry.json"
DEFAULT_POLICY = MATH / "LearnerProduct" / "policies" / "math-learner-language-policy.json"


def load_policy(path: Path | str | None = None) -> dict:
    """The central learner-language policy — the authority for what may be printed."""
    return json.loads(Path(path or DEFAULT_POLICY).read_text(encoding="utf-8"))


def load_registry(path: Path | str | None = None) -> dict:
    """Consumer bindings plus Core1A's legacy tokens. Holds no ban-list of its own."""
    return json.loads(Path(path or DEFAULT_CONSUMERS).read_text(encoding="utf-8"))


def banned_tokens(registry: dict | None = None, policy: dict | None = None) -> tuple[str, ...]:
    """The policy's forbidden terms unioned with Core1A's legacy tokens."""
    registry = registry if registry is not None else load_registry()
    policy = policy if policy is not None else load_policy()
    return tuple(sorted(set(policy["forbidden_learner_terms"])
                        | set(registry["legacy_core1a_tokens"])))


def role_labels(policy: dict | None = None) -> dict[str, str]:
    policy = policy if policy is not None else load_policy()
    return dict(policy["internal_role_label_public_titles"])


def approved_labels(policy: dict | None = None) -> dict[str, str]:
    """The approved public labels (TRY IT FIRST, SMALL CLUE, FULL WORKING, ...)."""
    policy = policy if policy is not None else load_policy()
    return dict(policy["labels"])


def warm_title(role: str, policy: dict | None = None) -> str:
    """Public heading for an internal role label.

    Falls back to a sentence-cased form rather than printing the label, so an unmapped role
    degrades into readable English instead of machine vocabulary.
    """
    titles = role_labels(policy)
    if role in titles:
        return titles[role]
    return str(role).replace("_", " ").strip().capitalize()


def _identifier_patterns(policy: dict) -> list[re.Pattern[str]]:
    return [re.compile(p) for p in policy["internal_identifier_patterns"]]


def find_leaks(texts: Iterable[str], registry: dict | None = None,
               policy: dict | None = None) -> dict[str, list[str]]:
    """Return the leaks found in learner-facing text, grouped by class.

    ``jargon``      banned pipeline/authoring vocabulary
    ``role_label``  an internal role label printed as learner copy
    ``identifier``  an internal id or snake_case machine key
    """
    registry = registry if registry is not None else load_registry()
    policy = policy if policy is not None else load_policy()
    tokens = banned_tokens(registry, policy)
    labels = policy["forbidden_learner_role_labels"]
    exemptions = policy["role_label_detection"].get("approved_label_exemptions", [])
    patterns = _identifier_patterns(policy)

    jargon: set[str] = set()
    role_leaks: set[str] = set()
    identifiers: set[str] = set()

    for raw in texts:
        text = str(raw or "")
        if not text:
            continue
        lowered = text.lower()
        for token in tokens:
            if token in lowered:
                jargon.add(token.strip())
        # ALL_CAPS_TOKEN_OR_EXACT_HEADING: the lowercase English words 'verify',
        # 'represent' and 'compare' are good learner copy; the machine label is not.
        # An approved public label that happens to share a word (QUICK CHECK for VERIFY)
        # is exempt, because the policy itself prescribes it.
        scan = text
        for approved in exemptions:
            scan = scan.replace(approved, " ")
        for label in labels:
            if re.search(rf"\b{re.escape(label)}\b", scan):
                role_leaks.add(label)
            elif scan.strip() == label.replace("_", " "):
                role_leaks.add(label)
        for pattern in patterns:
            for match in pattern.findall(text):
                identifiers.add(match if isinstance(match, str) else match[0])

    return {
        "jargon": sorted(jargon),
        "role_label": sorted(role_leaks),
        "identifier": sorted(identifiers),
    }


def audit_learner_copy(texts: Iterable[str], *, stage: str,
                       registry: dict | None = None,
                       policy: dict | None = None) -> dict:
    """Fail-closed learner-copy audit for a named consumer stage.

    ``stage`` selects the falsifier vocabulary from the registry's ``consumers`` list, so
    Core1A keeps raising ``CORE1A_INTERNAL_JARGON_LEAK`` and Core2A raises
    ``CORE2A_INTERNAL_JARGON_LEAK`` from the same detector.
    """
    registry = registry if registry is not None else load_registry()
    policy = policy if policy is not None else load_policy()
    consumer = next((c for c in registry["consumers"] if c["stage"] == stage), None)
    if consumer is None:
        raise ValueError(f"LEARNER_COPY_CONSUMER_UNKNOWN:{stage}")

    texts = list(texts)
    leaks = find_leaks(texts, registry, policy)
    failures: list[str] = []
    for token in leaks["jargon"]:
        failures.append(f"{consumer['falsifier']}:{token}")
    for label in leaks["role_label"]:
        failures.append(f"{consumer['falsifier']}:ROLE_LABEL:{label}")
    for identifier in leaks["identifier"]:
        failures.append(f"{consumer['identifier_falsifier']}:{identifier}")

    if failures:
        raise ValueError("|".join(sorted(set(failures))))

    return {
        "status": "PASS",
        "stage": stage,
        "policy_id": policy["policy_id"],
        "texts_checked": len(texts),
        "banned_token_count": len(banned_tokens(registry, policy)),
        "role_labels_governed": len(policy["forbidden_learner_role_labels"]),
        "checks": [
            "NO_BANNED_PIPELINE_VOCABULARY",
            "NO_INTERNAL_ROLE_LABEL_AS_LEARNER_COPY",
            "NO_INTERNAL_IDENTIFIER_AS_LEARNER_COPY",
        ],
    }
