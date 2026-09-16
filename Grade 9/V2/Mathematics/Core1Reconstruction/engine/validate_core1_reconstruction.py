#!/usr/bin/env python3
"""Core1 reconstruction-chain depth and the cross-core bridge (M-UPGRADE-2 item 6).

The strongest cross-topic finding of the seven-topic stress test was an asymmetry: Core2
became more mature than Core1. A question book exposed a six-state reasoning chain while
the study guide that supposedly prepared the learner contained a theorem statement, a short
explanation and one exercise.

So a full-teaching lesson must *realize* the chain

    ANCHOR -> REPRESENT -> EXPLAIN -> RECONSTRUCT -> WORKED -> GUIDED
           -> FADED -> INDEPENDENT -> VERIFY -> TRANSFER

rather than declare that the stage labels exist. `RECONSTRUCT` must carry a real derivation
built from item 2's route-state objects; the practice stages must reference materialized
learner realizations. The chain then publishes the reasoning evidence it genuinely teaches,
and the cross-core bridge requires

    Core2 required reasoning evidence - Core1 realized teaching evidence = {}
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path[:0] = [str(MATH / "MathTypesetting" / "engine"),
                str(MATH / "LearnerRealization" / "engine")]

from learner_realization import validate_realization  # noqa: E402

DEFAULT_POLICY = PHASE / "policies" / "math-core1-reconstruction-policy.json"
DEFAULT_ROLE_REGISTRY = MATH / "LearnerRealization" / "registry" \
    / "math-realization-role-registry.json"

FALSIFIERS = (
    "CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE",
    "CORE1_RECONSTRUCTION_WITHOUT_DERIVATION",
    "CORE1_WORKED_INSTANCE_NOT_MATERIALIZED",
    "CORE1_TRANSFER_INSTANCE_MISSING",
    "CORE1_CHAIN_ORDER_DRIFT",
    "CORE1_STAGE_UNDERREALIZED",
    "THEOREM_DIRECTION_NOT_DECLARED",
    "CONVERSE_RESTATES_FORWARD_STATEMENT",
    "CONVERSE_USED_WITHOUT_BEING_TAUGHT",
    "CORE1_CORE2_REASONING_COVERAGE_GAP",
    "CORE1_RECONSTRUCTION_GATE_FAILED",
)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _normalise(text: str) -> str:
    return " ".join(str(text or "").lower().split())


# --------------------------------------------------------------------------
# derived teaching evidence
# --------------------------------------------------------------------------
def derive_teaching_evidence(chain: dict, realizations: dict[str, dict],
                             roles: dict | None = None) -> list[str]:
    """One token per reasoning role this lesson actually realizes.

    Derived rather than declared, so a lesson cannot advertise teaching evidence it does not
    contain. Only substantive, non-trivial states count: a `CLASSIFY` step that restates the
    givens is not teaching evidence for a Core2 `TRANSFORM` state.
    """
    roles = roles if roles is not None else load(DEFAULT_ROLE_REGISTRY)
    lesson = chain["lesson_ref"]
    tokens: set[str] = set()

    def absorb(derivation: Iterable[dict]) -> None:
        for step in derivation:
            role = roles["roles"].get(step["role"])
            if role is None or step.get("trivial"):
                continue
            if role["substantive"]:
                tokens.add(f"{lesson}#{step['role']}")

    for stage in chain["stages"]:
        if stage["evidence_kind"] == "DERIVATION":
            absorb(stage.get("derivation") or [])
        elif stage["evidence_kind"] == "REALIZATION":
            realization = realizations.get(stage.get("realization_ref") or "")
            if realization is not None:
                absorb(realization["derivation"])
    return sorted(tokens)


def seal_chain(chain: dict, realizations: dict[str, dict],
               roles: dict | None = None) -> dict:
    out = copy.deepcopy(chain)
    out["realized_teaching_evidence"] = derive_teaching_evidence(out, realizations, roles)
    out.pop("chain_id", None)
    out.pop("chain_digest", None)
    out["chain_id"] = "MATH-C1RC-" + digest(out)[:16]
    out["chain_digest"] = digest(out, "chain_digest")
    return out


# --------------------------------------------------------------------------
# chain validation
# --------------------------------------------------------------------------
def validate_chain(chain: dict, realizations: dict[str, dict], *,
                   policy: dict | None = None, roles: dict | None = None,
                   theorem_based: bool = False) -> list[str]:
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    roles = roles if roles is not None else load(DEFAULT_ROLE_REGISTRY)
    failures: list[str] = []
    lesson = chain["lesson_ref"]
    full = chain["treatment"] in policy["full_treatments"]
    present = [s["stage"] for s in chain["stages"]]
    requirements = policy["stage_evidence_requirements"]

    if chain["chain_digest"] != digest(chain, "chain_digest"):
        failures.append(f"CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE:{lesson}:digest_drift")

    if full:
        required = policy["required_chain"]
        missing = [s for s in required if s not in present]
        if missing:
            failures.append(f"CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE:{lesson}:"
                            f"{','.join(missing)}")
        if policy["chain_order_is_significant"]:
            ordered = [s for s in present if s in required]
            expected = [s for s in required if s in ordered]
            if ordered != expected:
                failures.append(f"CORE1_CHAIN_ORDER_DRIFT:{lesson}:{','.join(ordered)}")

    for stage in chain["stages"]:
        name = stage["stage"]
        requirement = requirements.get(name)
        if requirement is None:
            continue
        if stage["evidence_kind"] not in requirement["evidence_kind"]:
            if name == "RECONSTRUCT":
                failures.append(f"CORE1_RECONSTRUCTION_WITHOUT_DERIVATION:{lesson}:"
                                f"{stage['evidence_kind']}")
            elif name == "WORKED":
                failures.append(f"CORE1_WORKED_INSTANCE_NOT_MATERIALIZED:{lesson}:"
                                f"{stage['evidence_kind']}")
            elif name == "TRANSFER":
                failures.append(f"CORE1_TRANSFER_INSTANCE_MISSING:{lesson}:"
                                f"{stage['evidence_kind']}")
            else:
                failures.append(f"CORE1_STAGE_UNDERREALIZED:{lesson}:{name}:"
                                f"{stage['evidence_kind']}")
            continue

        if stage["evidence_kind"] == "PROSE":
            minimum = int(requirement.get("min_prose_chars", 0))
            if len(_normalise(stage.get("prose") or "")) < minimum:
                failures.append(f"CORE1_STAGE_UNDERREALIZED:{lesson}:{name}:prose_too_short")
        elif stage["evidence_kind"] == "DERIVATION":
            derivation = stage.get("derivation") or []
            if len(derivation) < int(requirement.get("min_derivation_steps", 1)):
                code = ("CORE1_RECONSTRUCTION_WITHOUT_DERIVATION" if name == "RECONSTRUCT"
                        else "CORE1_STAGE_UNDERREALIZED")
                failures.append(f"{code}:{lesson}:{name}:too_few_steps")
            substantive = [s for s in derivation
                           if roles["roles"].get(s["role"], {}).get("substantive")
                           and not s.get("trivial")]
            if len(substantive) < int(requirement.get("min_substantive_steps", 1)):
                code = ("CORE1_RECONSTRUCTION_WITHOUT_DERIVATION" if name == "RECONSTRUCT"
                        else "CORE1_STAGE_UNDERREALIZED")
                failures.append(f"{code}:{lesson}:{name}:no_substantive_step")
        else:
            ref = stage.get("realization_ref")
            realization = realizations.get(ref or "")
            if realization is None:
                code = {
                    "WORKED": "CORE1_WORKED_INSTANCE_NOT_MATERIALIZED",
                    "TRANSFER": "CORE1_TRANSFER_INSTANCE_MISSING",
                }.get(name, "CORE1_STAGE_UNDERREALIZED")
                failures.append(f"{code}:{lesson}:{name}:{ref}")
                continue
            # the referenced instance must itself pass the item-2 realization gate
            for code in validate_realization(realization, roles=roles):
                failures.append(f"CORE1_STAGE_UNDERREALIZED:{lesson}:{name}:{code}")

    derived = derive_teaching_evidence(chain, realizations, roles)
    if sorted(chain["realized_teaching_evidence"]) != derived:
        failures.append(f"CORE1_RECONSTRUCTION_CHAIN_INCOMPLETE:{lesson}:"
                        "declared_evidence_is_not_what_the_chain_realizes")

    failures.extend(_theorem_direction_failures(chain, policy, theorem_based))
    return sorted(set(failures))


def _theorem_direction_failures(chain: dict, policy: dict, theorem_based: bool) -> list[str]:
    failures: list[str] = []
    direction = chain.get("theorem_direction")
    lesson = chain["lesson_ref"]
    tp = policy["theorem_direction_policy"]
    if theorem_based and tp["required_when_capability_is_theorem_based"] and direction is None:
        failures.append(f"THEOREM_DIRECTION_NOT_DECLARED:{lesson}")
        return failures
    if direction is None:
        return failures
    if tp["converse_must_not_restate_the_forward_statement"]:
        forward = (_normalise(direction["forward"]["condition"]),
                   _normalise(direction["forward"]["conclusion"]))
        converse = (_normalise(direction["converse"]["condition"]),
                    _normalise(direction["converse"]["conclusion"]))
        if forward == converse:
            failures.append(f"CONVERSE_RESTATES_FORWARD_STATEMENT:{lesson}")
        elif converse[0] != forward[1] and converse[1] != forward[0]:
            # a converse must genuinely swap the implication
            failures.append(f"CONVERSE_RESTATES_FORWARD_STATEMENT:{lesson}:not_swapped")
    if direction["converse"]["is_true"] is False and \
            not (direction.get("counterexample_when_converse_false") or "").strip():
        failures.append(f"THEOREM_DIRECTION_NOT_DECLARED:{lesson}:"
                        "false_converse_without_counterexample")
    return failures


# --------------------------------------------------------------------------
# the cross-core bridge
# --------------------------------------------------------------------------
def build_bridge(topic_ref: str, rows: list[dict], chains: list[dict]) -> dict:
    """Assemble the bridge manifest and compute the unresolved set."""
    taught: set[str] = set()
    direction_by_lesson: dict[str, dict | None] = {}
    for chain in chains:
        taught |= set(chain["realized_teaching_evidence"])
        direction_by_lesson[chain["lesson_ref"]] = chain.get("theorem_direction")

    unresolved: list[str] = []
    for row in rows:
        for state in row["reasoning_states"]:
            if state["trivial"]:
                continue
            ref = state.get("core1_evidence_ref")
            if not ref:
                unresolved.append(f"{row['core2_question_ref']}:{row['atomic_ask_ref']}:"
                                  f"{state['role']}:NO_EVIDENCE_REF")
            elif ref not in taught:
                unresolved.append(f"{row['core2_question_ref']}:{row['atomic_ask_ref']}:"
                                  f"{state['role']}:{ref}")
            if state.get("uses_converse"):
                lesson = str(ref or "").split("#", 1)[0]
                direction = direction_by_lesson.get(lesson)
                if direction is None or direction["direction_taught"] == "FORWARD":
                    unresolved.append(f"{row['core2_question_ref']}:{row['atomic_ask_ref']}:"
                                      f"{state['role']}:CONVERSE_NOT_TAUGHT:{lesson}")
        if row["first_recovery_evidence_ref"] not in taught:
            unresolved.append(f"{row['core2_question_ref']}:{row['atomic_ask_ref']}:"
                              f"FIRST_RECOVERY:{row['first_recovery_evidence_ref']}")
        for ref in row["core1_evidence_refs"]:
            if ref not in taught:
                unresolved.append(f"{row['core2_question_ref']}:{row['atomic_ask_ref']}:"
                                  f"ROW_EVIDENCE:{ref}")

    bridge = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "topic_ref": topic_ref,
        "rows": rows,
        "unresolved": sorted(set(unresolved)),
    }
    bridge["bridge_id"] = "MATH-CCB-" + digest(bridge)[:16]
    bridge["bridge_digest"] = digest(bridge, "bridge_digest")
    return bridge


def audit_reconstruction(chains: list[dict], realizations: dict[str, dict], *,
                         bridge_rows: list[dict] | None = None,
                         topic_ref: str = "MIXED_GRADE9",
                         theorem_based_lessons: Iterable[str] = (),
                         policy: dict | None = None,
                         roles: dict | None = None) -> dict:
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    roles = roles if roles is not None else load(DEFAULT_ROLE_REGISTRY)
    theorem_based = set(theorem_based_lessons)
    failures: list[str] = []

    for chain in chains:
        failures.extend(validate_chain(
            chain, realizations, policy=policy, roles=roles,
            theorem_based=chain["lesson_ref"] in theorem_based))

    bridge = None
    if bridge_rows is not None:
        bridge = build_bridge(topic_ref, bridge_rows, chains)
        for entry in bridge["unresolved"]:
            if "CONVERSE_NOT_TAUGHT" in entry:
                failures.append(f"CONVERSE_USED_WITHOUT_BEING_TAUGHT:{entry}")
            else:
                failures.append(f"CORE1_CORE2_REASONING_COVERAGE_GAP:{entry}")

    if failures:
        fail("CORE1_RECONSTRUCTION_GATE_FAILED", "|".join(sorted(set(failures))))

    taught = sorted({token for chain in chains
                     for token in chain["realized_teaching_evidence"]})
    return {
        "status": "PASS",
        "chain_count": len(chains),
        "full_teaching_chains": sum(1 for c in chains
                                    if c["treatment"] in policy["full_treatments"]),
        "stages_realized": sorted({s["stage"] for c in chains for s in c["stages"]}),
        "realized_teaching_evidence": taught,
        "theorem_directions_declared": sorted({
            c["theorem_direction"]["theorem_ref"] for c in chains
            if c.get("theorem_direction")
        }),
        "bridge": bridge,
        "cross_core_invariant": "Core2 required reasoning evidence - Core1 realized "
                                "teaching evidence = {}",
        "cross_core_unresolved": [] if bridge is None else bridge["unresolved"],
        "corpus_digest": digest(sorted(c["chain_digest"] for c in chains)),
        "checks": [
            "FULL_TEACHING_CHAIN_PRESENT_AND_IN_ORDER",
            "RECONSTRUCT_CARRIES_A_REAL_DERIVATION",
            "PRACTICE_STAGES_REFERENCE_MATERIALIZED_INSTANCES",
            "REFERENCED_INSTANCES_PASS_THE_REALIZATION_GATE",
            "TEACHING_EVIDENCE_IS_DERIVED_NOT_DECLARED",
            "THEOREM_DIRECTION_IS_FIRST_CLASS",
            "EVERY_NON_TRIVIAL_CORE2_STATE_RESOLVES_TO_CORE1_EVIDENCE",
        ],
        "release_meaning": "PUBLICATION_ENGINEERING only; pedagogy and expert review "
                           "PENDING, PCK stays PROVISIONAL_PROMOTED",
    }
