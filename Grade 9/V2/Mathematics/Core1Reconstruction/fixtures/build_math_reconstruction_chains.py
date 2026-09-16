#!/usr/bin/env python3
"""Build the Core1 reconstruction-chain fixture.

Two chains, deliberately different in treatment so the depth requirement is shown to be
treatment-sensitive rather than blanket:

* ``MATH-C1L-FACTOR-THEOREM`` (``ACTIVE_STUDY``) realizes the full chain
  ANCHOR -> REPRESENT -> EXPLAIN -> RECONSTRUCT -> WORKED -> GUIDED -> FADED ->
  INDEPENDENT -> VERIFY -> TRANSFER. Its ``WORKED`` stage reuses the Polynomials
  realization from the LearnerRealization reference corpus (this is the item 2 -> item 6
  dependency), and the four remaining practice roles are fresh instances of the same
  family generated here.
* ``MATH-C1L-IRRATIONAL-PRODUCT`` (``VERIFY_ONLY``) realizes a shorter chain, but its
  ``RECONSTRUCT`` stage still carries a real derivation: the universal-claim ->
  search-edge-case -> counterexample -> infer route the owner asked Number Systems to teach.
  Its theorem direction records a **false** converse together with its counterexample.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path[:0] = [str(MATH / "MathTypesetting" / "engine"),
                str(MATH / "LearnerRealization" / "engine"),
                str(PHASE / "engine")]

from math_expression import call, group, num, op, power, radical, rel, seq, sym, txt  # noqa: E402
from learner_realization import load, seal_realization  # noqa: E402
from validate_core1_reconstruction import seal_chain  # noqa: E402

REALIZATION_FIXTURE = MATH / "LearnerRealization" / "fixtures" \
    / "math-reference-realizations.fixture.json"
OUT = PHASE / "fixtures" / "math-reconstruction-chains.fixture.json"

LESSON_FACTOR = "MATH-C1L-FACTOR-THEOREM"
LESSON_IRRATIONAL = "MATH-C1L-IRRATIONAL-PRODUCT"


def eq(lhs: dict, rhs: dict) -> dict:
    return seq(lhs, rel("EQ"), rhs)


def T(text: str) -> dict:
    return {"segment": "TEXT", "text": text}


def M(node: dict) -> dict:
    return {"segment": "MATH", "expression": node}


def step(step_id, role, operation, rule, output, *, input_state=None, substitution=None,
         why_valid="", explanation="", witness=None, sufficiency=None, evidence=None,
         trivial=False) -> dict:
    return {
        "step_id": step_id, "role": role,
        "input_state": input_state,
        "operation": {"name": operation, "rule_or_justification": rule},
        "substitution": substitution, "output_state": output,
        "why_valid": why_valid, "learner_explanation": explanation,
        "equivalence_witness": witness, "sufficiency": sufficiency,
        "core1_evidence_ref": evidence, "trivial": trivial,
    }


def witness(tid, operation, before, after, invariant, precondition, reversible=True,
            extraneous=None) -> dict:
    return {"transformation_id": tid, "operation": operation, "before_relation": before,
            "after_relation": after, "preserved_invariant": invariant,
            "precondition": precondition, "reversible": reversible,
            "extraneous_root_check": extraneous}


def hint(text: str, step_id: str, evidence: str | None = None) -> dict:
    return {"text": text, "derived_from_step_id": step_id, "discloses_output": False,
            "core1_evidence_ref": evidence}


# --------------------------------------------------------------------------
# the factor-theorem family generator
# --------------------------------------------------------------------------
def _signed(value: int) -> tuple[str, str]:
    return ("PLUS", str(value)) if value >= 0 else ("MINUS", str(-value))


def _cubic(roots: tuple[int, int, int]) -> tuple[dict, str, int, int, int]:
    r, s, t = roots
    b = -(r + s + t)
    c = r * s + r * t + s * t
    d = -(r * s * t)
    x = sym("x")
    items: list[dict] = [power(x, num(3))]
    for coefficient, tail in ((b, power(x, num(2))), (c, x), (d, None)):
        if coefficient == 0:
            continue
        sign, magnitude = _signed(coefficient)
        items.append(op(sign))
        if tail is None:
            items.append(num(magnitude))
        elif magnitude == "1":
            items.append(tail)
        else:
            items.extend([num(magnitude), tail])
    poly = seq(*items)
    return poly, "", b, c, d


def _poly_text(roots: tuple[int, int, int]) -> str:
    from math_expression import typeset_unicode
    poly, *_ = _cubic(roots)
    return typeset_unicode(poly)


def _factor(value: int) -> dict:
    sign = "MINUS" if value >= 0 else "PLUS"
    return group(seq(sym("x"), op(sign), num(abs(value))))


def factor_theorem_instance(role: str, item_ref: str, roots: tuple[int, int, int],
                            tested_root: int, *, transfer_note: str | None = None) -> dict:
    """A fresh, real instance of the factor-theorem family.

    Every learner-visible string carries this instance's own coefficients, so the support
    cannot be transplanted onto another instance.
    """
    from math_expression import typeset_unicode

    poly, _, b, c, d = _cubic(roots)
    x = sym("x")
    r = tested_root
    others = [v for v in roots if v != r] or list(roots[1:])
    poly_text = typeset_unicode(poly)
    root_factor = _factor(r)
    root_factor_text = typeset_unicode(root_factor)

    p_of_x = eq(call("p", x), poly)
    substituted_terms: list[dict] = [power(num(r), num(3))]
    for coefficient, power_of_x in ((b, 2), (c, 1), (d, 0)):
        if coefficient == 0:
            continue
        sign, magnitude = _signed(coefficient)
        substituted_terms.append(op(sign))
        if power_of_x == 0:
            substituted_terms.append(num(magnitude))
        elif magnitude == "1":
            substituted_terms.append(power(num(r), num(power_of_x)) if power_of_x > 1
                                     else num(r))
        else:
            substituted_terms.extend([num(magnitude),
                                      power(num(r), num(power_of_x)) if power_of_x > 1
                                      else num(r)])
    substituted = seq(*substituted_terms)
    arithmetic_values = [r ** 3]
    if b:
        arithmetic_values.append(b * r ** 2)
    if c:
        arithmetic_values.append(c * r)
    if d:
        arithmetic_values.append(d)
    arithmetic_items: list[dict] = [num(arithmetic_values[0])]
    for value in arithmetic_values[1:]:
        sign, magnitude = _signed(value)
        arithmetic_items.extend([op(sign), num(magnitude)])
    arithmetic = seq(*arithmetic_items)
    zero = eq(call("p", num(r)), num(0))

    quadratic_sum = others[0] + others[1]
    quadratic_product = others[0] * others[1]
    quad_items: list[dict] = [power(x, num(2))]
    if quadratic_sum:
        sign, magnitude = _signed(-quadratic_sum)
        quad_items.extend([op(sign), x] if magnitude == "1"
                          else [op(sign), num(magnitude), x])
    if quadratic_product:
        sign, magnitude = _signed(quadratic_product)
        quad_items.extend([op(sign), num(magnitude)])
    quadratic = group(seq(*quad_items))
    quadratic_text = typeset_unicode(quadratic)

    partial = eq(call("p", x), seq(root_factor, quadratic))
    complete_factors = seq(root_factor, _factor(others[0]), _factor(others[1]))
    complete = eq(call("p", x), complete_factors)

    statement = [T("Show that"), M(root_factor),
                 T("is a factor of"), M(p_of_x),
                 T("and then factorise it completely.")]
    if transfer_note:
        statement.append(T(transfer_note))

    derivation = [
        step("S1", "INTERPRET", "READ_GIVEN",
             f"The cubic is {poly_text} and the suggested factor is {root_factor_text}.",
             p_of_x, trivial=True,
             why_valid="Restating the given cubic changes nothing.",
             explanation=f"You are given {poly_text} and asked about {root_factor_text}."),
        step("S2", "SETUP", "SUBSTITUTE",
             f"Put x = {r} into every term of {poly_text}.",
             eq(call("p", num(r)), substituted),
             input_state=p_of_x, substitution=substituted,
             why_valid="A polynomial accepts every real input, so this substitution is "
                       "legal.",
             explanation=f"Replace each x in {poly_text} by {r}.",
             witness=witness("T1", "SUBSTITUTE", p_of_x,
                             eq(call("p", num(r)), substituted), "VALUE",
                             f"x = {r} lies in the domain of the polynomial, so "
                             "substituting it preserves the value."),
             evidence=f"{LESSON_FACTOR}#SETUP"),
        step("S3", "EXECUTE", "EVALUATE",
             f"Work the four terms of {poly_text} out at x = {r}.",
             zero, input_state=eq(call("p", num(r)), substituted),
             substitution=arithmetic,
             why_valid="Each term is evaluated by ordinary arithmetic.",
             explanation=f"The terms come to {typeset_unicode(arithmetic)}, which is 0, so "
                         f"p({r}) = 0 exactly."),
        step("S4", "INFER", "APPLY_THEOREM",
             f"p({r}) = 0, so by the factor theorem {root_factor_text} divides the cubic "
             "exactly.",
             seq(root_factor, txt(" is a factor of "), call("p", x)),
             input_state=zero,
             why_valid="The factor theorem turns the value 0 into a divisibility statement.",
             explanation=f"Because p({r}) came out as 0, {root_factor_text} really is a "
                         f"factor of {poly_text}."),
        step("S5", "EXECUTE", "DIVIDE",
             f"Divide {poly_text} by {root_factor_text}; the division is exact and leaves "
             f"{quadratic_text}.",
             partial, input_state=p_of_x, substitution=quadratic,
             why_valid=f"The remainder is p({r}) = 0, so the quotient is a quadratic.",
             explanation=f"Dividing {poly_text} by {root_factor_text} leaves "
                         f"{quadratic_text} with nothing over.",
             witness=witness("T2", "FACTOR", p_of_x, partial, "VALUE",
                             f"The division is exact because p({r}) = 0, so no remainder "
                             "term is dropped.")),
        step("S6", "TRANSFORM", "FACTOR",
             f"Factorise {quadratic_text} by finding two numbers with sum "
             f"{quadratic_sum} and product {quadratic_product}.",
             complete, input_state=partial,
             substitution=seq(_factor(others[0]), _factor(others[1])),
             why_valid="Two numbers with the required sum and product give the linear "
                       "factors directly.",
             explanation=f"{quadratic_text} splits using {others[0]} and {others[1]}, so "
                         f"{poly_text} is now fully factorised.",
             witness=witness("T3", "FACTOR", partial, complete, "VALUE",
                             f"{quadratic_text} factorises over the integers, so the split "
                             "loses no solutions.")),
        step("S7", "VERIFY", "CHECK",
             f"Multiply the three factors back out and expect {poly_text} term for term.",
             eq(complete_factors, poly), input_state=complete, substitution=poly,
             why_valid="A factorisation is only correct if expanding returns the original "
                       "polynomial.",
             explanation=f"Expanding the three factors returns {poly_text}, so the "
                         "factorisation is right."),
    ]

    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "role": role,
        "item_ref": item_ref,
        "topic_ref": "POLYNOMIALS",
        "capability_refs": ["MATH-CAP-FACTOR-THEOREM"],
        "problem_family_ref": "MATH-PF-FACTOR-THEOREM-FACTORISATION",
        "statement": statement,
        "item_anchors": [poly_text, root_factor_text],
        "derivation": derivation,
        "scaffold": {
            "H1": hint(f"A suggested factor {root_factor_text} points at one value of x. "
                       "Which value, and what must p do there?", "S1",
                       f"{LESSON_FACTOR}#SETUP"),
            "H2": hint(f"Test that value in {poly_text} rather than dividing first.",
                       "S2", f"{LESSON_FACTOR}#SETUP"),
            "H3": hint(f"Substitute into every term of {poly_text} and evaluate the numbers "
                       "before deciding anything.", "S3"),
        },
        "answer_custody": {
            "question_ref": item_ref,
            "answer_kind": "EXPRESSION",
            "final_answer": complete_factors,
            "final_answer_prose": None,
            "model_proof_steps": [],
            "acceptance_rule": None,
            "admissible_answers": [],
            "construction_verification_conditions": [],
            "counterexample_witness": None,
            "independent_verification": {
                "kind": "EXPAND_TO_RECOVER_ORIGINAL",
                "executable": True,
                "statement": f"Multiply the three factors out. The expansion must return "
                             f"{poly_text} term for term, with no leftover terms.",
                "expected": poly,
            },
            "quick_check": "Do the three factors multiply to give a cubic?",
            "placement": "ANSWER_APPENDIX",
            "attempt_surface_answer_neutral": True,
        },
        "source_distance": {
            "source_question_reuse": False,
            "basis": "Authored inside the factor-theorem family with coefficients chosen "
                     "here, not taken from an assessment item.",
        },
    }


# --------------------------------------------------------------------------
# chain 1 — the full factor-theorem chain
# --------------------------------------------------------------------------
FACTOR_DIRECTION = {
    "theorem_ref": "FACTOR_THEOREM",
    "learner_name": "The factor theorem",
    "forward": {
        "condition": "p(a) = 0 for a polynomial p and a number a",
        "conclusion": "(x − a) is a factor of p(x)",
    },
    "converse": {
        "condition": "(x − a) is a factor of p(x)",
        "conclusion": "p(a) = 0 for a polynomial p and a number a",
        "is_true": True,
        "justification": "If (x − a) divides p(x) exactly then p(x) = (x − a)q(x), and "
                         "putting x = a gives p(a) = 0.",
    },
    "direction_taught": "BOTH",
    "counterexample_when_converse_false": None,
}


def reconstruct_derivation() -> list[dict]:
    """The RECONSTRUCT stage: build the factor theorem rather than assert it."""
    x, a = sym("x"), sym("a")
    division = eq(call("p", x), seq(group(seq(x, op("MINUS"), a)), call("q", x),
                                    op("PLUS"), sym("R")))
    at_a = eq(call("p", a), seq(group(seq(a, op("MINUS"), a)), call("q", a),
                                op("PLUS"), sym("R")))
    collapsed = eq(call("p", a), sym("R"))
    conclusion = eq(sym("R"), num(0))
    return [
        step("S1", "REPRESENT", "WRITE_DIVISION_FORM",
             "Any polynomial divided by (x − a) leaves a quotient and a constant "
             "remainder R.",
             division, input_state=eq(call("p", x), call("p", x)),
             why_valid="Division by a linear polynomial always leaves a remainder of "
                       "degree 0.",
             explanation="Write p(x) as (x − a)q(x) + R, where R is just a number."),
        step("S2", "EXECUTE", "SUBSTITUTE",
             "Put x = a into p(x) = (x − a)q(x) + R.",
             at_a, input_state=division, substitution=at_a,
             why_valid="The identity holds for every x, so it holds at x = a.",
             explanation="At x = a the bracket (a − a) is 0, whatever q(a) happens to be.",
             witness=witness("T1", "SUBSTITUTE", division, at_a, "VALUE",
                             "The division identity holds for every real x, so x = a is an "
                             "admissible choice.")),
        step("S3", "EXECUTE", "SIMPLIFY",
             "(a − a) is 0, so the whole first product vanishes.",
             collapsed, input_state=at_a, substitution=num(0),
             why_valid="Zero times any number is zero, so only R survives.",
             explanation="That leaves p(a) = R, so the remainder is exactly the value of p "
                         "at a."),
        step("S4", "INFER", "APPLY_THEOREM",
             "(x − a) is a factor precisely when the remainder R is 0, and R = p(a).",
             conclusion, input_state=collapsed,
             why_valid="Being a factor means the remainder is zero, and the remainder has "
                       "just been identified as p(a).",
             explanation="So testing p(a) is the same as testing whether (x − a) divides "
                         "p(x)."),
    ]


def factor_chain(realizations: dict[str, dict]) -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "lesson_ref": LESSON_FACTOR,
        "capability_ref": "MATH-CAP-FACTOR-THEOREM",
        "treatment": "ACTIVE_STUDY",
        "theorem_direction": FACTOR_DIRECTION,
        "stages": [
            {"stage": "ANCHOR", "evidence_kind": "PROSE",
             "learner_heading": "Start with something you can see",
             "prose": "A cubic can sometimes be split into three simple brackets. Before "
                      "dividing anything, it is worth asking whether one particular bracket "
                      "works at all, because testing is much quicker than dividing.",
             "derivation": [], "realization_ref": None},
            {"stage": "REPRESENT", "evidence_kind": "PROSE",
             "learner_heading": "Picture it another way",
             "prose": "Think of p(x) = (x − a)q(x) + R as a division sum written sideways: "
                      "the bracket is the divisor, q(x) is the quotient and R is whatever "
                      "is left over.",
             "derivation": [], "realization_ref": None},
            {"stage": "EXPLAIN", "evidence_kind": "PROSE",
             "learner_heading": "What is going on",
             "prose": "Dividing by a bracket of the form (x − a) can only leave a plain "
                      "number behind, never another x term, because the remainder has to "
                      "be of lower degree than the divisor. That single fact is what makes "
                      "the whole test work, and it is worth being sure of it before going "
                      "on.",
             "derivation": [], "realization_ref": None},
            {"stage": "RECONSTRUCT", "evidence_kind": "DERIVATION",
             "learner_heading": "Build the rule for yourself",
             "prose": None, "derivation": reconstruct_derivation(), "realization_ref": None},
            {"stage": "WORKED", "evidence_kind": "REALIZATION",
             "learner_heading": "Worked example", "prose": None, "derivation": [],
             "realization_ref": "PY-W1"},
            {"stage": "GUIDED", "evidence_kind": "REALIZATION",
             "learner_heading": "Guided practice", "prose": None, "derivation": [],
             "realization_ref": "FT-G1"},
            {"stage": "FADED", "evidence_kind": "REALIZATION",
             "learner_heading": "Less-help practice", "prose": None, "derivation": [],
             "realization_ref": "FT-F1"},
            {"stage": "INDEPENDENT", "evidence_kind": "REALIZATION",
             "learner_heading": "Your turn", "prose": None, "derivation": [],
             "realization_ref": "FT-I1"},
            {"stage": "VERIFY", "evidence_kind": "PROSE",
             "learner_heading": "Check your work",
             "prose": "Expand your three brackets and compare every term with the cubic you "
                      "started from. If one term differs, the factorisation is wrong even if "
                      "the test value came out as zero.",
             "derivation": [], "realization_ref": None},
            {"stage": "TRANSFER", "evidence_kind": "REALIZATION",
             "learner_heading": "Challenge", "prose": None, "derivation": [],
             "realization_ref": "FT-T1"},
        ],
    }


# --------------------------------------------------------------------------
# chain 2 — the shorter, VERIFY_ONLY chain with a false converse
# --------------------------------------------------------------------------
IRRATIONAL_DIRECTION = {
    "theorem_ref": "IRRATIONAL_PRODUCT",
    "learner_name": "Multiplying two irrational numbers",
    "forward": {
        "condition": "a and b are both rational numbers",
        "conclusion": "the product ab is rational",
    },
    "converse": {
        "condition": "the product ab is rational",
        "conclusion": "a and b are both rational numbers",
        "is_true": False,
        "justification": "A rational product does not force either factor to be rational.",
    },
    "direction_taught": "BOTH",
    "counterexample_when_converse_false": "√2 × √2 = 2 is rational while neither factor is.",
}


def counterexample_derivation() -> list[dict]:
    root2 = radical(num(2))
    a, b = sym("a"), sym("b")
    claim = seq(txt("if "), a, txt(" and "), b, txt(" are irrational then "), a, b,
                txt(" is irrational"))
    tested = eq(seq(root2, op("TIMES"), root2), num(2))
    verdict = seq(txt("the claim is false, because "), num(2), txt(" is rational"))
    return [
        step("S1", "CLASSIFY", "IDENTIFY_STRUCTURE",
             "The statement is a universal claim: it says something about every pair of "
             "irrational numbers.",
             claim, trivial=True,
             why_valid="Naming the shape of the claim does not change it.",
             explanation="A claim about every pair can be destroyed by a single pair."),
        step("S2", "REPRESENT", "WRITE_AS_IMPLICATION",
             "Write the claim as a condition and a conclusion so the counterexample has "
             "something definite to break.",
             seq(a, txt(" irrational and "), b, txt(" irrational "), rel("IMPLIES"),
                 seq(a, b, txt(" irrational"))),
             input_state=claim,
             why_valid="An implication is false exactly when the condition holds and the "
                       "conclusion fails.",
             explanation="So look for two irrational numbers whose product is rational."),
        step("S3", "EXECUTE", "SUBSTITUTE",
             "Try the most obvious edge case: take a and b to be the same irrational "
             "number √2.",
             tested,
             input_state=seq(a, op("TIMES"), b),
             substitution=seq(root2, op("TIMES"), root2),
             why_valid="√2 is irrational, so it is an admissible choice for both a and b.",
             explanation="√2 × √2 is 2, and 2 is a whole number, so the product is rational.",
             witness=witness("T1", "SUBSTITUTE", seq(a, op("TIMES"), b), tested, "VALUE",
                             "√2 is a real irrational number, so choosing it for both "
                             "factors is a legal instance of the claim.")),
        step("S4", "INFER", "APPLY_THEOREM",
             "The condition held and the conclusion failed, so the universal claim is false.",
             verdict, input_state=tested,
             why_valid="One counterexample is enough to refute a universal claim.",
             explanation="The pair √2 and √2 satisfies the condition but gives the rational "
                         "product 2, so the claim cannot be true for every pair."),
    ]


def irrational_chain() -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "lesson_ref": LESSON_IRRATIONAL,
        "capability_ref": "MATH-CAP-IRRATIONAL-PRODUCT",
        "treatment": "VERIFY_ONLY",
        "theorem_direction": IRRATIONAL_DIRECTION,
        "stages": [
            {"stage": "ANCHOR", "evidence_kind": "PROSE",
             "learner_heading": "Start with something you can see",
             "prose": "It is tempting to assume that multiplying two numbers with endless "
                      "decimals must give another number with endless decimals.",
             "derivation": [], "realization_ref": None},
            {"stage": "RECONSTRUCT", "evidence_kind": "DERIVATION",
             "learner_heading": "Build the rule for yourself",
             "prose": None, "derivation": counterexample_derivation(),
             "realization_ref": None},
            {"stage": "VERIFY", "evidence_kind": "PROSE",
             "learner_heading": "Check your work",
             "prose": "When a claim says every, one well-chosen pair settles it. Check that "
                      "your pair really does satisfy the condition before trusting it.",
             "derivation": [], "realization_ref": None},
        ],
    }


# --------------------------------------------------------------------------
# bridge rows
# --------------------------------------------------------------------------
def bridge_rows() -> list[dict]:
    def state(role: str, trivial: bool, ref: str | None, converse: bool = False) -> dict:
        return {"role": role, "trivial": trivial, "core1_evidence_ref": ref,
                "uses_converse": converse}

    return [
        {
            "core2_question_ref": "Q3",
            "atomic_ask_ref": "Q3#SUB-a",
            "concept_refs": ["MATH-CONCEPT-FACTOR-THEOREM"],
            "prerequisite_refs": ["MATH-CAP-SUBSTITUTION"],
            "reasoning_states": [
                state("INTERPRET", True, None),
                state("SETUP", False, f"{LESSON_FACTOR}#SETUP"),
                state("EXECUTE", False, f"{LESSON_FACTOR}#EXECUTE"),
                state("INFER", False, f"{LESSON_FACTOR}#INFER"),
                state("VERIFY", False, f"{LESSON_FACTOR}#VERIFY"),
            ],
            "representation_requirements": ["ANNOTATED_DERIVATION"],
            "verification_witness": "Evaluate p at the tested value and require exactly 0.",
            "core1_evidence_refs": [f"{LESSON_FACTOR}#SETUP", f"{LESSON_FACTOR}#EXECUTE"],
            "first_recovery_evidence_ref": f"{LESSON_FACTOR}#SETUP",
        },
        {
            "core2_question_ref": "Q3",
            "atomic_ask_ref": "Q3#SUB-b",
            "concept_refs": ["MATH-CONCEPT-POLYNOMIAL-FACTORISATION"],
            "prerequisite_refs": ["MATH-CAP-FACTOR-THEOREM"],
            "reasoning_states": [
                state("TRANSFORM", False, f"{LESSON_FACTOR}#TRANSFORM"),
                state("VERIFY", False, f"{LESSON_FACTOR}#VERIFY"),
                # the reverse direction of the factor theorem is needed here, and the
                # lesson declares direction_taught = BOTH
                state("INFER", False, f"{LESSON_FACTOR}#INFER", converse=True),
            ],
            "representation_requirements": ["ALIGNED_TRANSFORMATION_STACK"],
            "verification_witness": "Expand the factors and recover the original cubic term "
                                    "for term.",
            "core1_evidence_refs": [f"{LESSON_FACTOR}#TRANSFORM"],
            "first_recovery_evidence_ref": f"{LESSON_FACTOR}#TRANSFORM",
        },
        {
            "core2_question_ref": "Q5",
            "atomic_ask_ref": "Q5#COUNTEREXAMPLE",
            "concept_refs": ["MATH-CONCEPT-IRRATIONAL-NUMBERS"],
            "prerequisite_refs": ["MATH-CAP-NUMBER-CLASSIFICATION"],
            "reasoning_states": [
                state("CLASSIFY", True, None),
                state("REPRESENT", False, f"{LESSON_IRRATIONAL}#REPRESENT"),
                state("EXECUTE", False, f"{LESSON_IRRATIONAL}#EXECUTE"),
                state("INFER", False, f"{LESSON_IRRATIONAL}#INFER", converse=True),
            ],
            "representation_requirements": ["PARALLEL_MEET_CONTRAST"],
            "verification_witness": "Check the chosen pair really satisfies the condition of "
                                    "the claim before accepting it as a counterexample.",
            "core1_evidence_refs": [f"{LESSON_IRRATIONAL}#INFER"],
            "first_recovery_evidence_ref": f"{LESSON_IRRATIONAL}#REPRESENT",
        },
    ]


GENERATED = (
    ("GUIDED", "FT-G1", (1, 2, 3), 1, None),
    ("FADED", "FT-F1", (-1, 2, 4), 2, None),
    ("INDEPENDENT", "FT-I1", (1, -2, 5), 1, None),
    ("TRANSFER", "FT-T1", (3, -1, -2), 3,
     "Notice that one of the usual terms is missing before you start."),
)


def build() -> dict:
    reference = load(REALIZATION_FIXTURE)
    realizations = {r["item_ref"]: r for r in reference["realizations"]}
    generated = []
    for role, item_ref, roots, tested, note in GENERATED:
        instance = seal_realization(
            factor_theorem_instance(role, item_ref, roots, tested, transfer_note=note))
        realizations[item_ref] = instance
        generated.append(instance)

    chains = [seal_chain(factor_chain(realizations), realizations),
              seal_chain(irrational_chain(), realizations)]
    return {
        "fixture_id": "MATH-RECONSTRUCTION-CHAINS-v1",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "purpose": "Realized Core1 reconstruction chains plus the fresh family instances "
                   "their practice stages reference, and the cross-core bridge rows checked "
                   "against them.",
        "theorem_based_lessons": [LESSON_FACTOR, LESSON_IRRATIONAL],
        "generated_realizations": generated,
        "chains": chains,
        "bridge_rows": bridge_rows(),
    }


def main() -> None:
    payload = build()
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(payload['chains'])} chains, "
          f"{len(payload['generated_realizations'])} generated instances, "
          f"{len(payload['bridge_rows'])} bridge rows")
    for chain in payload["chains"]:
        print(f"  {chain['lesson_ref']:<32} {chain['treatment']:<13} "
              f"stages={len(chain['stages'])} "
              f"evidence={len(chain['realized_teaching_evidence'])}")


if __name__ == "__main__":
    main()
