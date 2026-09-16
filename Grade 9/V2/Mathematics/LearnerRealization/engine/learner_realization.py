#!/usr/bin/env python3
"""Learner mathematical realization — the governed layer the PR #323 RCA asked for.

RC-1: the pipeline jumped from semantic intent straight to representation/rendering, so
a route could keep its semantic label without ever proving the mathematical state
transition happened. The Theory-of-Equations reproducer is exactly this:

    v1  INTERPRET / REPRESENT / EXECUTE / VERIFY        (route metadata)
    v2  "Compute S1, compute S2, compute S3 ..."        (operation named, not demonstrated)
    v3  S2 + a1S1 + 2a2 = 0 -> S2 + 0(0) + 2(-7) = 0 -> S2 = 14   (realized mathematics)

This module makes v3 the only publishable shape. It validates:

* item 2 — real substitution and transformation in every substantive step;
* item 5 — an equivalence-transformation witness and a sufficiency check;
* item 8 — answer custody for every learner-facing question;
* item 9 — the internal-semantics/learner-copy boundary (via ``learner_copy``).
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path.insert(0, str(MATH / "MathTypesetting" / "engine"))

from math_expression import (  # noqa: E402
    GlyphRegistry,
    audit_expressions,
    detect_flattening,
    typeset_unicode,
)
from learner_copy import audit_learner_copy, load_registry as load_copy_registry  # noqa: E402

DEFAULT_ROLE_REGISTRY = PHASE / "registry" / "math-realization-role-registry.json"
DEFAULT_POLICY = PHASE / "policies" / "math-learner-realization-policy.json"

ANSWER_CUSTODY_FALSIFIERS = (
    "LEARNER_QUESTION_WITHOUT_ANSWER",
    "SELF_CHECK_SUBSTITUTED_FOR_ANSWER",
    "PROOF_PROMPT_WITHOUT_MODEL_PROOF",
    "CONSTRUCTION_WITHOUT_VERIFICATION_CONDITIONS",
    "MULTIPLE_VALID_ANSWERS_WITHOUT_ADMISSIBILITY_RULE",
    "OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA",
    "COUNTEREXAMPLE_WITHOUT_WITNESS",
    "ANSWER_WITHOUT_VERIFICATION",
    "ATTEMPT_PAGE_ANSWER_LEAKAGE",
    "ANSWER_CUSTODY_GATE_FAILED",
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


# --------------------------------------------------------------------------
# prose helpers
# --------------------------------------------------------------------------
def prose_text(prose: list[dict], reg: GlyphRegistry | None = None) -> str:
    reg = reg or GlyphRegistry()
    out: list[str] = []
    for segment in prose:
        if segment["segment"] == "TEXT":
            out.append(segment["text"])
        else:
            out.append(typeset_unicode(segment["expression"], reg))
    return " ".join(out)


def prose_expressions(prose: list[dict]) -> list[dict]:
    return [s["expression"] for s in prose if s["segment"] == "MATH"]


def realization_texts(realization: dict, reg: GlyphRegistry | None = None) -> list[str]:
    """Every learner-visible string this realization will put on a page."""
    reg = reg or GlyphRegistry()
    texts = [prose_text(realization["statement"], reg)]
    for step in realization["derivation"]:
        texts.append(step["learner_explanation"])
        texts.append(step["operation"]["rule_or_justification"])
        texts.append(step["why_valid"])
    for hint in realization["scaffold"].values():
        texts.append(hint["text"])
    custody = realization["answer_custody"]
    if custody.get("final_answer_prose"):
        texts.append(custody["final_answer_prose"])
    if custody.get("acceptance_rule"):
        texts.append(custody["acceptance_rule"])
    if custody.get("quick_check"):
        texts.append(custody["quick_check"])
    texts.append(custody["independent_verification"]["statement"])
    for step in custody.get("model_proof_steps", []):
        texts.append(step["statement"])
        texts.append(step["licensed_by"])
    texts.extend(custody.get("construction_verification_conditions", []))
    return [t for t in texts if t]


def realization_expressions(realization: dict) -> dict[str, dict]:
    """Every MathExpression this realization will typeset, keyed by page location."""
    item = realization["item_ref"]
    out: dict[str, dict] = {}
    for i, expression in enumerate(prose_expressions(realization["statement"])):
        out[f"{item}/statement/{i}"] = expression
    for step in realization["derivation"]:
        if step.get("input_state") is not None:
            out[f"{item}/{step['step_id']}/input"] = step["input_state"]
        if step.get("substitution") is not None:
            out[f"{item}/{step['step_id']}/substitution"] = step["substitution"]
        out[f"{item}/{step['step_id']}/output"] = step["output_state"]
        witness = step.get("equivalence_witness")
        if witness:
            out[f"{item}/{step['step_id']}/before"] = witness["before_relation"]
            out[f"{item}/{step['step_id']}/after"] = witness["after_relation"]
    custody = realization["answer_custody"]
    if custody.get("final_answer") is not None:
        out[f"{item}/answer"] = custody["final_answer"]
    for i, admissible in enumerate(custody.get("admissible_answers", [])):
        out[f"{item}/answer/admissible/{i}"] = admissible
    if custody.get("counterexample_witness") is not None:
        out[f"{item}/answer/witness"] = custody["counterexample_witness"]
    expected = custody["independent_verification"].get("expected")
    if expected is not None:
        out[f"{item}/verification/expected"] = expected
    return out


# --------------------------------------------------------------------------
# item 8 — answer custody
# --------------------------------------------------------------------------
def validate_answer_custody(custody: dict, *, attempt_surface_texts: Iterable[str] = (),
                            reg: GlyphRegistry | None = None) -> list[str]:
    """Return the answer-custody failures for one learner-facing question."""
    reg = reg or GlyphRegistry()
    kind = custody["answer_kind"]
    ref = custody["question_ref"]
    failures: list[str] = []

    has_expression_answer = custody.get("final_answer") is not None
    has_prose_answer = bool(custody.get("final_answer_prose"))
    has_proof = bool(custody.get("model_proof_steps"))
    has_admissible = bool(custody.get("admissible_answers"))
    has_conditions = bool(custody.get("construction_verification_conditions"))
    has_witness = custody.get("counterexample_witness") is not None
    has_rule = bool(custody.get("acceptance_rule"))

    resolved = any((has_expression_answer, has_prose_answer, has_proof,
                    has_admissible, has_conditions, has_witness))
    if not resolved:
        failures.append(f"LEARNER_QUESTION_WITHOUT_ANSWER:{ref}")

    # a quick check is never the answer artifact
    if not resolved and custody.get("quick_check"):
        failures.append(f"SELF_CHECK_SUBSTITUTED_FOR_ANSWER:{ref}")
    if custody.get("quick_check") and not resolved:
        failures.append(f"SELF_CHECK_SUBSTITUTED_FOR_ANSWER:{ref}")

    if kind in ("NUMERIC", "EXPRESSION", "ORDERED_PAIR", "SET", "MCQ_CHOICE"):
        if not (has_expression_answer or has_prose_answer):
            failures.append(f"LEARNER_QUESTION_WITHOUT_ANSWER:{ref}:{kind}")
    if kind == "PROOF" and not has_proof:
        failures.append(f"PROOF_PROMPT_WITHOUT_MODEL_PROOF:{ref}")
    if kind == "CONSTRUCTION" and not has_conditions:
        failures.append(f"CONSTRUCTION_WITHOUT_VERIFICATION_CONDITIONS:{ref}")
    if kind == "MULTIPLE_VALID":
        if not has_rule:
            failures.append(f"MULTIPLE_VALID_ANSWERS_WITHOUT_ADMISSIBILITY_RULE:{ref}")
        if not has_admissible:
            failures.append(f"LEARNER_QUESTION_WITHOUT_ANSWER:{ref}:MULTIPLE_VALID")
    if kind == "OPEN_RESPONSE" and not has_rule:
        failures.append(f"OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA:{ref}")
    if kind == "COUNTEREXAMPLE" and not has_witness:
        failures.append(f"COUNTEREXAMPLE_WITHOUT_WITNESS:{ref}")

    verification = custody["independent_verification"]
    if not verification["executable"]:
        failures.append(f"ANSWER_WITHOUT_VERIFICATION:{ref}")
    for pattern in ("check your answer", "verify the answer", "state one independent check",
                    "answers may vary"):
        if pattern in verification["statement"].lower():
            failures.append(f"ANSWER_WITHOUT_VERIFICATION:{ref}:generic")

    # the attempt surface must stay answer-neutral
    if custody["attempt_surface_answer_neutral"] is not True:
        failures.append(f"ATTEMPT_PAGE_ANSWER_LEAKAGE:{ref}")
    answer_strings = []
    if has_expression_answer:
        answer_strings.append(typeset_unicode(custody["final_answer"], reg))
    for admissible in custody.get("admissible_answers", []):
        answer_strings.append(typeset_unicode(admissible, reg))
    for text in attempt_surface_texts:
        for answer in answer_strings:
            if answer and len(answer) >= 2 and answer in str(text):
                failures.append(f"ATTEMPT_PAGE_ANSWER_LEAKAGE:{ref}:{answer}")
    return sorted(set(failures))


def seal_custody(custody: dict) -> dict:
    out = copy.deepcopy(custody)
    out.pop("custody_id", None)
    out.pop("custody_digest", None)
    custody_id = "MATH-AC-" + digest(out)[:16]
    result = copy.deepcopy(custody)
    result["custody_id"] = custody_id
    result["custody_digest"] = digest(result, "custody_digest")
    return result


# --------------------------------------------------------------------------
# item 5 — equivalence witness + sufficiency
# --------------------------------------------------------------------------
def validate_equivalence_witness(step: dict, roles: dict) -> list[str]:
    witness = step.get("equivalence_witness")
    failures: list[str] = []
    operation = step["operation"]["name"].upper()
    algebraic = operation in {
        "TRANSFORM", "REARRANGE", "RATIONALISE", "EXPAND", "FACTOR", "FACTORISE",
        "MULTIPLY", "DIVIDE", "SQUARE", "TAKE_ROOT", "SUBSTITUTE", "CLEAR_DENOMINATOR",
        "MULTIPLY_BY_ONE_IN_DISGUISE", "SOLVE",
    }
    if step["role"] == "TRANSFORM" or (algebraic and step["role"] in ("SETUP", "EXECUTE", "TRANSFORM")):
        if witness is None:
            failures.append(
                f"EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS:{step['step_id']}")
            return failures
    if witness is None:
        return failures
    if not witness.get("precondition", "").strip():
        failures.append(f"EQUIVALENCE_TRANSFORMATION_PRECONDITION_MISSING:{step['step_id']}")
    if witness["operation"] in roles["non_reversible_operations"]:
        if witness["reversible"] is True:
            failures.append(f"SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK:{step['step_id']}")
        elif witness["preserved_invariant"] == "SOLUTION_SET" and \
                not (witness.get("extraneous_root_check") or "").strip():
            failures.append(f"SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK:{step['step_id']}")
    if digest(witness["before_relation"]) == digest(witness["after_relation"]):
        failures.append(
            f"EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS:{step['step_id']}:no_change")
    return failures


# --------------------------------------------------------------------------
# item 2 — the realization gate
# --------------------------------------------------------------------------
def _anchored(text: str, anchors: Iterable[str]) -> bool:
    return any(a and a in text for a in anchors)


def validate_realization(realization: dict, *, roles: dict | None = None,
                         policy: dict | None = None, reg: GlyphRegistry | None = None,
                         parameterized: bool = False) -> list[str]:
    """Return the realization failures for one worked/guided/faded/independent instance."""
    roles = roles if roles is not None else load(DEFAULT_ROLE_REGISTRY)
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    reg = reg or GlyphRegistry()

    failures: list[str] = []
    item = realization["item_ref"]
    anchors = realization["item_anchors"]
    statement = prose_text(realization["statement"], reg)
    grounding = policy["item_grounding_policy"]

    # -- uninstantiated / template leakage -------------------------------
    texts = realization_texts(realization, reg)
    blob = "\n".join(texts)
    lowered = blob.lower()
    for pattern in roles["uninstantiated_patterns"]:
        if pattern in lowered:
            failures.append(f"WORKED_EXAMPLE_UNINSTANTIATED:{item}:{pattern}")
    for pattern in roles["unresolved_template_token_patterns"]:
        if re.search(pattern, blob):
            failures.append(f"WORKED_EXAMPLE_UNINSTANTIATED:{item}:template_token")
    if not realization["derivation"]:
        failures.append(f"WORKED_EXAMPLE_UNINSTANTIATED:{item}:no_derivation")

    # -- item grounding --------------------------------------------------
    if len(anchors) < int(grounding["min_anchors"]):
        failures.append(f"LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM:{item}:anchor_count")
    if grounding["anchors_must_appear_in_statement"]:
        for anchor in anchors:
            if anchor not in statement:
                failures.append(
                    f"LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM:{item}:anchor_absent:{anchor}")

    # -- per-step realization -------------------------------------------
    substantive = 0
    anchored_substantive = 0
    demonstration_required = set(roles["demonstration_required_operations"])
    generic_patterns = roles["generic_learner_copy_patterns"]

    for step in realization["derivation"]:
        role = roles["roles"].get(step["role"])
        if role is None:
            failures.append(f"LEARNER_STEP_WITHOUT_MATHEMATICAL_STATE_TRANSITION:"
                            f"{item}:{step['step_id']}:unknown_role")
            continue
        operation = step["operation"]["name"].upper()
        justification = step["operation"]["rule_or_justification"]
        explanation = step["learner_explanation"]

        if not role["substantive"] or step["trivial"]:
            continue
        substantive += 1

        if step.get("input_state") is None:
            failures.append(f"LEARNER_STEP_WITHOUT_MATHEMATICAL_STATE_TRANSITION:"
                            f"{item}:{step['step_id']}:no_input_state")
        elif role["requires_state_change"] and \
                digest(step["input_state"]) == digest(step["output_state"]):
            failures.append(f"LEARNER_STEP_WITHOUT_MATHEMATICAL_STATE_TRANSITION:"
                            f"{item}:{step['step_id']}:output_equals_input")

        if operation in demonstration_required:
            demonstrated = (
                step.get("substitution") is not None
                or (step.get("input_state") is not None
                    and digest(step["input_state"]) != digest(step["output_state"]))
            )
            if not demonstrated:
                failures.append(f"MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED:"
                                f"{item}:{step['step_id']}:{operation}")

        for pattern in generic_patterns:
            if pattern in justification.lower():
                failures.append(f"MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED:"
                                f"{item}:{step['step_id']}:generic_justification")
            if pattern in explanation.lower():
                failures.append(f"LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS:"
                                f"{item}:{step['step_id']}:{pattern}")

        if _anchored(explanation, anchors) or _anchored(justification, anchors):
            anchored_substantive += 1

        failures.extend(validate_equivalence_witness(step, roles))

    if substantive:
        ratio = anchored_substantive / substantive
        if ratio < float(grounding["min_anchored_substantive_steps_ratio"]):
            failures.append(f"LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS:"
                            f"{item}:anchored_ratio={ratio:.2f}")

    # -- scaffold --------------------------------------------------------
    step_ids = {s["step_id"] for s in realization["derivation"]}
    final_output = typeset_unicode(realization["derivation"][-1]["output_state"], reg) \
        if realization["derivation"] else ""
    answer_text = ""
    if realization["answer_custody"].get("final_answer") is not None:
        answer_text = typeset_unicode(realization["answer_custody"]["final_answer"], reg)
    for name, hint in realization["scaffold"].items():
        if hint["derived_from_step_id"] not in step_ids:
            failures.append(f"LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM:"
                            f"{item}:{name}:unresolved_step")
        if not _anchored(hint["text"], anchors):
            failures.append(f"LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM:{item}:{name}")
        for pattern in generic_patterns:
            if pattern in hint["text"].lower():
                failures.append(f"LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS:{item}:{name}")
        for secret in (answer_text, final_output):
            if secret and len(secret) >= 2 and secret in hint["text"]:
                failures.append(f"SCAFFOLD_DISCLOSES_SOLUTION:{item}:{name}")

    # -- sufficiency (item 5) -------------------------------------------
    if parameterized:
        states = [s for s in realization["derivation"] if s["role"] == "CHECK_SUFFICIENCY"]
        if not states:
            failures.append(f"PARAMETERIZED_ITEM_WITHOUT_SUFFICIENCY_CHECK:{item}")
        elif any(s.get("sufficiency") is None for s in states):
            failures.append(f"PARAMETERIZED_ITEM_WITHOUT_SUFFICIENCY_CHECK:{item}:no_status")

    # -- answer custody (item 8) ----------------------------------------
    attempt_texts = [statement] + [h["text"] for h in realization["scaffold"].values()]
    failures.extend(validate_answer_custody(realization["answer_custody"],
                                            attempt_surface_texts=attempt_texts, reg=reg))

    # -- learner-copy boundary (item 9) ---------------------------------
    try:
        audit_learner_copy(texts, stage="LEARNER_REALIZATION")
    except ValueError as exc:
        failures.extend(str(exc).split("|"))

    # -- math typesetting (item 1) --------------------------------------
    for text in texts:
        for code in detect_flattening(text, reg):
            failures.append(f"{code}@{item}")

    return sorted(set(failures))


def seal_realization(realization: dict) -> dict:
    out = copy.deepcopy(realization)
    out["answer_custody"] = seal_custody(out["answer_custody"])
    out.pop("realization_id", None)
    out.pop("realization_digest", None)
    realization_id = "MATH-LMR-" + digest(out)[:16]
    out["realization_id"] = realization_id
    out["realization_digest"] = digest(out, "realization_digest")
    return out


def audit_realizations(realizations: Iterable[dict], *, roles: dict | None = None,
                       policy: dict | None = None,
                       parameterized_items: Iterable[str] = ()) -> dict:
    """Fail-closed audit over a corpus of learner realizations."""
    roles = roles if roles is not None else load(DEFAULT_ROLE_REGISTRY)
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    reg = GlyphRegistry()
    realizations = list(realizations)
    parameterized = set(parameterized_items)
    failures: list[str] = []

    for realization in realizations:
        failures.extend(validate_realization(
            realization, roles=roles, policy=policy, reg=reg,
            parameterized=realization["item_ref"] in parameterized,
        ))

    # cross-item adversarial check: identical learner derivation prose across two
    # different items means the support is metadata, not instruction
    seen: dict[str, str] = {}
    for realization in realizations:
        for step in realization["derivation"]:
            key = digest([step["learner_explanation"], step["operation"]["rule_or_justification"]])
            owner = seen.get(key)
            if owner is not None and owner != realization["item_ref"]:
                failures.append("LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS:"
                                f"{owner}~{realization['item_ref']}:{step['step_id']}")
            seen.setdefault(key, realization["item_ref"])

    # digest integrity
    for realization in realizations:
        expected = digest(realization, "realization_digest")
        if realization["realization_digest"] != expected:
            failures.append(f"LEARNER_REALIZATION_DIGEST_DRIFT:{realization['item_ref']}")

    expressions: dict[str, dict] = {}
    for realization in realizations:
        expressions.update(realization_expressions(realization))

    if failures:
        fail("LEARNER_REALIZATION_GATE_FAILED", "|".join(sorted(set(failures))))

    typeset_audit = audit_expressions(expressions, reg=reg)

    substantive_steps = sum(
        1 for r in realizations for s in r["derivation"]
        if roles["roles"][s["role"]]["substantive"] and not s["trivial"]
    )
    return {
        "status": "PASS",
        "realization_count": len(realizations),
        "topics": sorted({r["topic_ref"] for r in realizations}),
        "roles_realized": sorted({r["role"] for r in realizations}),
        "substantive_steps": substantive_steps,
        "equivalence_witnesses": sum(
            1 for r in realizations for s in r["derivation"]
            if s.get("equivalence_witness")
        ),
        "sufficiency_states": sorted({
            s["sufficiency"]["status"] for r in realizations for s in r["derivation"]
            if s.get("sufficiency")
        }),
        "answer_kinds": sorted({r["answer_custody"]["answer_kind"] for r in realizations}),
        "typesetting_audit": typeset_audit,
        "corpus_digest": digest(sorted(r["realization_digest"] for r in realizations)),
        "checks": [
            "EVERY_SUBSTANTIVE_STEP_SHOWS_A_STATE_TRANSITION",
            "NO_OPERATION_NAMED_WITHOUT_DEMONSTRATION",
            "NO_UNINSTANTIATED_AUTHORING_OBLIGATION",
            "LEARNER_SUPPORT_GROUNDED_IN_THE_ITEM",
            "DERIVATION_PROSE_NOT_TRANSPLANTABLE_ACROSS_ITEMS",
            "SCAFFOLD_DOES_NOT_DISCLOSE_THE_ANSWER",
            "EQUIVALENCE_TRANSFORMATIONS_CARRY_INVARIANT_WITNESSES",
            "EVERY_LEARNER_QUESTION_HAS_ANSWER_CUSTODY",
            "NO_INTERNAL_LABEL_IN_LEARNER_COPY",
            "NO_ASCII_MATH_FLATTENING",
        ],
        "release_meaning": "PUBLICATION_ENGINEERING only; subject/pedagogy/assessment/"
                           "visual/expert review PENDING",
    }
