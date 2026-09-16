#!/usr/bin/env python3
"""Build the reference learner-realization corpus.

Four of the seven stress-tested topics, realized as *actual mathematics* rather than
authoring obligations. These are data instances of the subject-wide contracts — no topic
contributes a schema shape of its own.

    NUMBER_SYSTEMS      rationalising a surd denominator (conjugate / difference of squares)
    POLYNOMIALS         factor theorem, real substitution, complete factorisation
    COORDINATE_GEOMETRY distance and midpoint with declared spatial semantics
    LINEAR_EQUATIONS    parameter determination plus an information-sufficiency verdict

Run this module to regenerate ``math-reference-realizations.fixture.json``; the committed
JSON is the artifact the gates run against, so a regeneration that changes it is visible
in review.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path[:0] = [str(MATH / "MathTypesetting" / "engine"), str(PHASE / "engine")]

from math_expression import (  # noqa: E402
    aligned, call, frac, group, num, op, power, radical, rel, seq, setrel, sub, sym, txt,
)
from learner_realization import seal_realization  # noqa: E402

OUT = PHASE / "fixtures" / "math-reference-realizations.fixture.json"


# -------------------------- small readable helpers --------------------------
def pair(a: dict, b: dict) -> dict:
    return group(seq(a, txt(", "), b))


def eq(lhs: dict, rhs: dict) -> dict:
    return seq(lhs, rel("EQ"), rhs)


def M(*items: dict) -> dict:
    return {"segment": "MATH", "expression": seq(*items) if len(items) > 1 else items[0]}


def T(text: str) -> dict:
    return {"segment": "TEXT", "text": text}


def hint(text: str, step: str, evidence: str | None = None) -> dict:
    return {"text": text, "derived_from_step_id": step, "discloses_output": False,
            "core1_evidence_ref": evidence}


def step(step_id, role, operation, rule, output, *, input_state=None, substitution=None,
         why_valid="", explanation="", witness=None, sufficiency=None, evidence=None,
         trivial=False) -> dict:
    out = {
        "step_id": step_id,
        "role": role,
        "input_state": input_state,
        "operation": {"name": operation, "rule_or_justification": rule},
        "substitution": substitution,
        "output_state": output,
        "why_valid": why_valid,
        "learner_explanation": explanation,
        "equivalence_witness": witness,
        "sufficiency": sufficiency,
        "core1_evidence_ref": evidence,
        "trivial": trivial,
    }
    return out


def witness(tid, operation, before, after, invariant, precondition, reversible=True,
            extraneous=None) -> dict:
    return {
        "transformation_id": tid,
        "operation": operation,
        "before_relation": before,
        "after_relation": after,
        "preserved_invariant": invariant,
        "precondition": precondition,
        "reversible": reversible,
        "extraneous_root_check": extraneous,
    }


# ==========================================================================
# 1. NUMBER SYSTEMS — rationalise 1/(√7 − 2)
# ==========================================================================
def number_systems() -> dict:
    root7 = radical(num(7))
    denom = seq(root7, op("MINUS"), num(2))
    conj = seq(root7, op("PLUS"), num(2))
    start = frac(num(1), denom)
    one_in_disguise = frac(conj, conj)
    product = seq(start, op("TIMES"), one_in_disguise)
    expanded = frac(conj, seq(power(root7, num(2)), op("MINUS"), power(num(2), num(2))))
    reduced = frac(conj, seq(num(7), op("MINUS"), num(4)))
    final = frac(conj, num(3))

    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "role": "WORKED",
        "item_ref": "NS-W1",
        "topic_ref": "NUMBER_SYSTEMS",
        "capability_refs": ["MATH-CAP-SURD-RATIONALISATION"],
        "problem_family_ref": "MATH-PF-SURD-RATIONALISATION",
        "statement": [
            T("Write"), M(start),
            T("with a rational denominator, leaving the answer in exact surd form."),
        ],
        "item_anchors": ["√7", "√7 − 2"],
        "derivation": [
            step("S1", "INTERPRET", "READ_GIVEN",
                 "The given number is a single fraction whose denominator is √7 − 2.",
                 start, trivial=True,
                 why_valid="Reading the given number changes nothing about it.",
                 explanation="You are given the fraction with √7 − 2 underneath."),
            step("S2", "CLASSIFY", "IDENTIFY_STRUCTURE",
                 "The denominator √7 − 2 is a difference of two terms, one of which is a surd.",
                 start, input_state=start, trivial=True,
                 why_valid="Naming the structure does not change the number.",
                 explanation="√7 − 2 has the shape a − b, and that shape has a partner a + b."),
            step("S3", "SELECT_THEOREM", "CHOOSE_IDENTITY",
                 "For any real a and b, (a − b)(a + b) = a² − b², which removes a square root "
                 "when a is a square root.",
                 seq(group(seq(sym("a"), op("MINUS"), sym("b"))),
                     group(seq(sym("a"), op("PLUS"), sym("b"))),
                     rel("EQ"),
                     seq(power(sym("a"), num(2)), op("MINUS"), power(sym("b"), num(2)))),
                 input_state=start, trivial=True,
                 why_valid="The identity is true for every pair of real numbers.",
                 explanation="With a = √7 and b = 2 this identity turns √7 into the whole "
                             "number 7."),
            step("S4", "TRANSFORM", "MULTIPLY_BY_ONE_IN_DISGUISE",
                 "Multiplying by (√7 + 2) over (√7 + 2) is multiplying by 1, so the value is "
                 "untouched.",
                 product, input_state=start,
                 substitution=one_in_disguise,
                 why_valid="(√7 + 2) is not zero, so (√7 + 2)/(√7 + 2) is exactly 1.",
                 explanation="Multiply above and below by √7 + 2. Nothing about the number "
                             "changes because you multiplied by 1.",
                 witness=witness("T1", "MULTIPLY_BY_ONE_IN_DISGUISE", start, product, "VALUE",
                                 "√7 + 2 is non-zero, so the multiplier is a genuine 1."),
                 evidence="MATH-C1L-SURD-CONJUGATE"),
            step("S5", "EXECUTE", "EXPAND",
                 "Apply (a − b)(a + b) = a² − b² to the denominator (√7 − 2)(√7 + 2).",
                 expanded, input_state=product,
                 substitution=seq(power(root7, num(2)), op("MINUS"), power(num(2), num(2))),
                 why_valid="The identity is an equality, so replacing the product by a² − b² "
                           "preserves the value.",
                 explanation="The bottom becomes (√7)² − 2², and (√7)² is just 7.",
                 witness=witness("T2", "EXPAND",
                                 seq(group(seq(root7, op("MINUS"), num(2))),
                                     group(seq(root7, op("PLUS"), num(2)))),
                                 seq(power(root7, num(2)), op("MINUS"), power(num(2), num(2))),
                                 "VALUE",
                                 "√7 is a real number, so the difference-of-squares identity "
                                 "applies.")),
            step("S6", "EXECUTE", "EVALUATE",
                 "Work out (√7)² − 2² as 7 − 4.",
                 reduced, input_state=expanded,
                 substitution=seq(num(7), op("MINUS"), num(4)),
                 why_valid="Squaring a square root of a positive number returns the number.",
                 explanation="(√7)² = 7 and 2² = 4, so the denominator under √7 + 2 is 7 − 4."),
            step("S7", "EXECUTE", "SIMPLIFY",
                 "7 − 4 is 3, so the denominator is the rational number 3.",
                 final, input_state=reduced,
                 substitution=num(3),
                 why_valid="3 is rational, which is what the question asked for.",
                 explanation="The denominator is now 3, a whole number, and no √7 is left "
                             "underneath."),
            step("S8", "VERIFY", "CHECK",
                 "Multiply the answer by the original denominator √7 − 2 and expect exactly 1.",
                 eq(seq(final, op("TIMES"), group(denom)), num(1)),
                 input_state=final,
                 substitution=seq(group(denom)),
                 why_valid="If the rewritten number really equals the original, undoing the "
                           "original denominator must return 1.",
                 explanation="(√7 + 2)(√7 − 2) is 3, and 3 over 3 is 1, so the rewrite is "
                             "correct."),
        ],
        "scaffold": {
            "H1": hint("The denominator √7 − 2 has a partner that clears the square root. "
                       "What is it?", "S2", "MATH-C1L-SURD-CONJUGATE"),
            "H2": hint("Write a fraction equal to 1 whose top and bottom are both √7 + 2.",
                       "S4", "MATH-C1L-SURD-CONJUGATE"),
            "H3": hint("Multiply the given fraction by that fraction and expand only the "
                       "denominator (√7 − 2)(√7 + 2) first.", "S5"),
        },
        "answer_custody": {
            "question_ref": "NS-W1",
            "answer_kind": "EXPRESSION",
            "final_answer": final,
            "final_answer_prose": None,
            "model_proof_steps": [],
            "acceptance_rule": None,
            "admissible_answers": [],
            "construction_verification_conditions": [],
            "counterexample_witness": None,
            "independent_verification": {
                "kind": "RECOMBINE_WITH_ORIGINAL_DENOMINATOR",
                "executable": True,
                "statement": "Multiply the answer by the original denominator √7 − 2. "
                             "The product must simplify to exactly 1.",
                "expected": num(1),
            },
            "quick_check": "Is there any square root left underneath?",
            "placement": "AFTER_ATTEMPT",
            "attempt_surface_answer_neutral": True,
        },
        "source_distance": {
            "source_question_reuse": False,
            "basis": "Authored inside the surd-rationalisation family; no assessment item "
                     "supplies 1 over √7 − 2.",
        },
    }


# ==========================================================================
# 2. POLYNOMIALS — factor theorem and complete factorisation
# ==========================================================================
def polynomials() -> dict:
    x = sym("x")
    poly = seq(power(x, num(3)), op("MINUS"), num(2), power(x, num(2)),
               op("MINUS"), x, op("PLUS"), num(2))
    p_of_x = eq(call("p", x), poly)
    substituted = seq(power(num(2), num(3)), op("MINUS"), num(2), power(num(2), num(2)),
                      op("MINUS"), num(2), op("PLUS"), num(2))
    arithmetic = seq(num(8), op("MINUS"), num(8), op("MINUS"), num(2), op("PLUS"), num(2))
    zero = eq(call("p", num(2)), num(0))
    factor_x_minus_2 = group(seq(x, op("MINUS"), num(2)))
    quotient = group(seq(power(x, num(2)), op("MINUS"), num(1)))
    partial = eq(call("p", x), seq(factor_x_minus_2, quotient))
    complete = eq(call("p", x),
                  seq(factor_x_minus_2,
                      group(seq(x, op("MINUS"), num(1))),
                      group(seq(x, op("PLUS"), num(1)))))
    final = seq(factor_x_minus_2, group(seq(x, op("MINUS"), num(1))),
                group(seq(x, op("PLUS"), num(1))))

    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "role": "WORKED",
        "item_ref": "PY-W1",
        "topic_ref": "POLYNOMIALS",
        "capability_refs": ["MATH-CAP-FACTOR-THEOREM", "MATH-CAP-POLYNOMIAL-FACTORISATION"],
        "problem_family_ref": "MATH-PF-FACTOR-THEOREM-FACTORISATION",
        "statement": [
            T("Show that"), M(factor_x_minus_2),
            T("is a factor of"), M(p_of_x),
            T("and then factorise it completely."),
        ],
        "item_anchors": ["x³ − 2x² − x + 2", "(x − 2)"],
        "derivation": [
            step("S1", "INTERPRET", "READ_GIVEN",
                 "The cubic is x³ − 2x² − x + 2 and the suggested factor is (x − 2).",
                 p_of_x, trivial=True,
                 why_valid="Restating the given cubic changes nothing.",
                 explanation="You are given the cubic x³ − 2x² − x + 2 and asked about "
                             "(x − 2)."),
            step("S2", "CLASSIFY", "IDENTIFY_STRUCTURE",
                 "A suggested linear factor (x − 2) means the root to test is x = 2.",
                 p_of_x, input_state=p_of_x, trivial=True,
                 why_valid="Naming the candidate root does not change the cubic.",
                 explanation="(x − 2) is zero when x = 2, so 2 is the number to test."),
            step("S3", "SELECT_THEOREM", "CHOOSE_THEOREM",
                 "Factor theorem: (x − a) is a factor of p(x) exactly when p(a) = 0.",
                 eq(call("p", sym("a")), num(0)),
                 input_state=p_of_x, trivial=True,
                 why_valid="The factor theorem is an equivalence, so the test decides the "
                           "question either way.",
                 explanation="Instead of dividing first, test whether p(2) is 0."),
            step("S4", "SETUP", "SUBSTITUTE",
                 "Put x = 2 into every term of x³ − 2x² − x + 2.",
                 eq(call("p", num(2)), substituted),
                 input_state=p_of_x,
                 substitution=substituted,
                 why_valid="A polynomial is defined for every real input, so x = 2 is legal.",
                 explanation="Replace each x in x³ − 2x² − x + 2 by 2: that gives "
                             "2³ − 2(2²) − 2 + 2.",
                 witness=witness("T1", "SUBSTITUTE", p_of_x, eq(call("p", num(2)), substituted),
                                 "VALUE",
                                 "x = 2 lies in the domain of the polynomial, so substitution "
                                 "preserves the value."),
                 evidence="MATH-C1L-FACTOR-THEOREM"),
            step("S5", "EXECUTE", "EVALUATE",
                 "2³ = 8 and 2(2²) = 8, so the four terms are 8 − 8 − 2 + 2.",
                 zero, input_state=eq(call("p", num(2)), substituted),
                 substitution=arithmetic,
                 why_valid="Each term is evaluated by ordinary arithmetic.",
                 explanation="8 − 8 − 2 + 2 = 0, so p(2) = 0 exactly."),
            step("S6", "INFER", "APPLY_THEOREM",
                 "p(2) = 0, so by the factor theorem (x − 2) divides the cubic exactly.",
                 seq(factor_x_minus_2, txt(" is a factor of "), call("p", sym("x"))),
                 input_state=zero,
                 why_valid="The factor theorem turns the value p(2) = 0 into a divisibility "
                           "statement.",
                 explanation="Because p(2) came out as 0, (x − 2) really is a factor of "
                             "x³ − 2x² − x + 2."),
            step("S7", "EXECUTE", "DIVIDE",
                 "Divide x³ − 2x² − x + 2 by (x − 2); the division is exact and leaves x² − 1.",
                 partial,
                 input_state=p_of_x,
                 substitution=quotient,
                 why_valid="The remainder is p(2) = 0, so the quotient is a polynomial of "
                           "degree 2.",
                 explanation="Dividing x³ − 2x² − x + 2 by (x − 2) gives x² − 1 with nothing "
                             "left over.",
                 witness=witness("T2", "FACTOR", p_of_x, partial, "VALUE",
                                 "The division is exact because p(2) = 0, so no remainder "
                                 "term is dropped.")),
            step("S8", "TRANSFORM", "FACTOR",
                 "x² − 1 is a difference of squares, so it splits as (x − 1)(x + 1).",
                 complete, input_state=partial,
                 substitution=seq(group(seq(x, op("MINUS"), num(1))),
                                  group(seq(x, op("PLUS"), num(1)))),
                 why_valid="a² − b² = (a − b)(a + b) with a = x and b = 1.",
                 explanation="x² − 1 is x² minus 1², so it becomes (x − 1)(x + 1) and the "
                             "cubic is fully split.",
                 witness=witness("T3", "FACTOR", partial, complete, "VALUE",
                                 "x² − 1 is a difference of squares with a = x and b = 1.")),
            step("S9", "VERIFY", "CHECK",
                 "Multiply the three factors back out and expect the original cubic term for "
                 "term.",
                 eq(seq(factor_x_minus_2, group(seq(x, op("MINUS"), num(1))),
                        group(seq(x, op("PLUS"), num(1)))), poly),
                 input_state=complete,
                 substitution=poly,
                 why_valid="Factorisation is only correct if expanding returns the original "
                           "polynomial exactly.",
                 explanation="Expanding (x − 2)(x − 1)(x + 1) returns x³ − 2x² − x + 2, so "
                             "the factorisation is right."),
        ],
        "scaffold": {
            "H1": hint("A suggested factor (x − 2) points at one particular value of x. "
                       "Which value, and what should p do there?", "S2",
                       "MATH-C1L-FACTOR-THEOREM"),
            "H2": hint("Test the value rather than dividing first: work out p at that value "
                       "using x³ − 2x² − x + 2.", "S3", "MATH-C1L-FACTOR-THEOREM"),
            "H3": hint("Substitute into every term of x³ − 2x² − x + 2 and evaluate the four "
                       "numbers before deciding anything.", "S4"),
        },
        "answer_custody": {
            "question_ref": "PY-W1",
            "answer_kind": "EXPRESSION",
            "final_answer": final,
            "final_answer_prose": None,
            "model_proof_steps": [],
            "acceptance_rule": None,
            "admissible_answers": [],
            "construction_verification_conditions": [],
            "counterexample_witness": None,
            "independent_verification": {
                "kind": "EXPAND_TO_RECOVER_ORIGINAL",
                "executable": True,
                "statement": "Multiply the three factors out. The expansion must return "
                             "x³ − 2x² − x + 2 term for term, with no leftover terms.",
                "expected": poly,
            },
            "quick_check": "Do the three factors have the right degrees to make a cubic?",
            "placement": "AFTER_ATTEMPT",
            "attempt_surface_answer_neutral": True,
        },
        "source_distance": {
            "source_question_reuse": False,
            "basis": "Authored inside the factor-theorem family with coefficients not used "
                     "by any assessment item.",
        },
    }


# ==========================================================================
# 3. COORDINATE GEOMETRY — distance and midpoint
# ==========================================================================
def coordinate_geometry() -> dict:
    A = pair(num(-2), num(3))
    B = pair(num(4), num(3))
    y_equal = aligned(
        (sub(sym("y"), num(1)), "EQ", num(3)),
        (sub(sym("y"), num(2)), "EQ", num(3)),
    )
    distance_formula = eq(
        sym("AB"),
        radical(seq(power(group(seq(sub(sym("x"), num(2)), op("MINUS"), sub(sym("x"), num(1)))),
                          num(2)),
                    op("PLUS"),
                    power(group(seq(sub(sym("y"), num(2)), op("MINUS"), sub(sym("y"), num(1)))),
                          num(2)))))
    distance_substituted = eq(
        sym("AB"),
        radical(seq(power(group(seq(num(4), op("MINUS"), num(-2))), num(2)),
                    op("PLUS"),
                    power(group(seq(num(3), op("MINUS"), num(3))), num(2)))))
    distance_value = eq(sym("AB"), num(6))
    midpoint_formula = eq(sym("M"), pair(frac(seq(sub(sym("x"), num(1)), op("PLUS"),
                                                  sub(sym("x"), num(2))), num(2)),
                                         frac(seq(sub(sym("y"), num(1)), op("PLUS"),
                                                  sub(sym("y"), num(2))), num(2))))
    midpoint_substituted = eq(sym("M"), pair(frac(seq(num(-2), op("PLUS"), num(4)), num(2)),
                                             frac(seq(num(3), op("PLUS"), num(3)), num(2))))
    midpoint_value = eq(sym("M"), pair(num(1), num(3)))
    check = aligned(
        (sym("AM"), "EQ", num(3)),
        (sym("MB"), "EQ", num(3)),
    )

    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "role": "GUIDED",
        "item_ref": "CG-G1",
        "topic_ref": "COORDINATE_GEOMETRY",
        "capability_refs": ["MATH-CAP-COORDINATE-DISTANCE", "MATH-CAP-COORDINATE-MIDPOINT"],
        "problem_family_ref": "MATH-PF-COORDINATE-DISTANCE",
        "statement": [
            T("The points A"), M(A), T("and B"), M(B),
            T("are plotted on the coordinate plane. Find the length AB and the coordinates "
              "of the midpoint M of AB."),
        ],
        "item_anchors": ["(−2, 3)", "(4, 3)"],
        "derivation": [
            step("S1", "INTERPRET", "READ_GIVEN",
                 "A is (−2, 3) and B is (4, 3); both are given exactly.",
                 seq(A, txt(" and "), B), trivial=True,
                 why_valid="Reading the two ordered pairs changes nothing.",
                 explanation="A sits at (−2, 3) and B sits at (4, 3)."),
            step("S2", "REPRESENT", "READ_OFF_COORDINATES",
                 "Both points have y-coordinate 3, so AB is a horizontal segment.",
                 y_equal, input_state=seq(A, txt(" and "), B),
                 why_valid="Two points with equal y-coordinates lie on the same horizontal "
                           "line.",
                 explanation="(−2, 3) and (4, 3) share the same height 3, so AB runs straight "
                             "across.",
                 evidence="MATH-C1L-PLANE-ORIENTATION"),
            step("S3", "SETUP", "SUBSTITUTE",
                 "Write the distance formula with the actual coordinates of A and B in it.",
                 distance_substituted, input_state=distance_formula,
                 substitution=distance_substituted,
                 why_valid="The distance formula holds for any two points of the plane.",
                 explanation="Put (4, 3) and (−2, 3) into the formula; the x-difference is "
                             "4 − (−2) and the y-difference is 3 − 3.",
                 witness=witness("T1", "SUBSTITUTE", distance_formula, distance_substituted,
                                 "VALUE",
                                 "A and B are ordinary points of the plane, so the formula "
                                 "applies to them unchanged."),
                 evidence="MATH-C1L-DISTANCE-FORMULA"),
            step("S4", "EXECUTE", "EVALUATE",
                 "4 − (−2) is 6 and 3 − 3 is 0, so AB is the square root of 36 + 0.",
                 distance_value, input_state=distance_substituted,
                 substitution=radical(seq(num(36), op("PLUS"), num(0))),
                 why_valid="Subtracting a negative adds, so the x-difference really is 6.",
                 explanation="From (−2, 3) to (4, 3) the horizontal gap is 6 and the vertical "
                             "gap is 0, so AB = 6."),
            step("S5", "SETUP", "SUBSTITUTE",
                 "Write the midpoint formula with the coordinates of A and B in it.",
                 midpoint_substituted, input_state=midpoint_formula,
                 substitution=midpoint_substituted,
                 why_valid="The midpoint formula averages coordinates and holds for any two "
                           "points.",
                 explanation="Average the x-values of (−2, 3) and (4, 3), then average the "
                             "y-values.",
                 witness=witness("T2", "SUBSTITUTE", midpoint_formula, midpoint_substituted,
                                 "VALUE",
                                 "Averaging coordinates is defined for every pair of real "
                                 "coordinates."),
                 evidence="MATH-C1L-MIDPOINT-FORMULA"),
            step("S6", "EXECUTE", "EVALUATE",
                 "(−2 + 4)/2 is 1 and (3 + 3)/2 is 3.",
                 midpoint_value, input_state=midpoint_substituted,
                 substitution=pair(num(1), num(3)),
                 why_valid="Both averages are ordinary arithmetic on the given coordinates.",
                 explanation="The midpoint of (−2, 3) and (4, 3) is therefore (1, 3), which "
                             "still has height 3."),
            step("S7", "VERIFY", "CHECK",
                 "Measure from A to M and from M to B; a midpoint must split AB into two "
                 "equal halves.",
                 check, input_state=midpoint_value,
                 substitution=num(3),
                 why_valid="If M is genuinely the midpoint, AM and MB must be equal and each "
                           "must be half of AB.",
                 explanation="From (−2, 3) to (1, 3) is 3, and from (1, 3) to (4, 3) is also "
                             "3, and 3 + 3 is the 6 found for AB."),
        ],
        "scaffold": {
            "H1": hint("Compare the two y-coordinates of (−2, 3) and (4, 3) before reaching "
                       "for any formula.", "S2", "MATH-C1L-PLANE-ORIENTATION"),
            "H2": hint("Which formula turns two ordered pairs such as (−2, 3) and (4, 3) into "
                       "a length?", "S3", "MATH-C1L-DISTANCE-FORMULA"),
            "H3": hint("Write the x-difference for (−2, 3) and (4, 3) as 4 − (−2) before "
                       "squaring anything.", "S4"),
        },
        "answer_custody": {
            "question_ref": "CG-G1",
            "answer_kind": "ORDERED_PAIR",
            "final_answer": midpoint_value,
            "final_answer_prose": "The length AB is 6 units and the midpoint M is (1, 3).",
            "model_proof_steps": [],
            "acceptance_rule": None,
            "admissible_answers": [],
            "construction_verification_conditions": [],
            "counterexample_witness": None,
            "independent_verification": {
                "kind": "RECOMPUTE_INVARIANT",
                "executable": True,
                "statement": "Recompute AM and MB from the coordinates. Both must equal 3 "
                             "and their sum must equal the AB you found.",
                "expected": check,
            },
            "quick_check": "Does the midpoint lie between the two given points?",
            "placement": "AFTER_ATTEMPT",
            "attempt_surface_answer_neutral": True,
        },
        "source_distance": {
            "source_question_reuse": False,
            "basis": "Authored inside the coordinate-distance family; the coordinates are "
                     "not taken from an assessment item.",
        },
    }


# ==========================================================================
# 4. LINEAR EQUATIONS — parameter determination plus sufficiency verdict
# ==========================================================================
def linear_equations() -> dict:
    x, y, k = sym("x"), sym("y"), sym("k")
    first = eq(seq(num(2), x, op("PLUS"), k, y), num(8))
    second = eq(seq(num(4), x, op("PLUS"), num(2), k, y), num(16))
    point = pair(num(2), num(1))
    substituted = eq(seq(num(2), group(num(2)), op("PLUS"), k, group(num(1))), num(8))
    simplified = eq(seq(num(4), op("PLUS"), k), num(8))
    solved = eq(k, num(4))
    dependent = eq(seq(num(4), x, op("PLUS"), num(8), y),
                   seq(num(2), group(seq(num(2), x, op("PLUS"), num(4), y))))
    verify = eq(seq(num(2), group(num(2)), op("PLUS"), num(4), group(num(1))), num(8))

    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "role": "INDEPENDENT",
        "item_ref": "LE-I1",
        "topic_ref": "LINEAR_EQUATIONS",
        "capability_refs": ["MATH-CAP-LINEAR-PARAMETER-SUFFICIENCY"],
        "problem_family_ref": "MATH-PF-LINEAR-PARAMETER-SUFFICIENCY",
        "statement": [
            T("The line"), M(first),
            T("passes through the point"), M(point),
            T("Find the value of k. Then decide whether the pair of equations"), M(first),
            T("and"), M(second),
            T("fixes one single ordered pair as its solution."),
        ],
        "item_anchors": ["2x + ky", "(2, 1)"],
        "derivation": [
            step("S1", "INTERPRET", "READ_GIVEN",
                 "The line is 2x + ky = 8 and the point it passes through is (2, 1).",
                 seq(first, txt(" through "), point), trivial=True,
                 why_valid="Restating the given line and point changes nothing.",
                 explanation="2x + ky = 8 must be true when x is 2 and y is 1."),
            step("S2", "SETUP", "SUBSTITUTE",
                 "A point lies on a line exactly when its coordinates satisfy the equation, "
                 "so put x = 2 and y = 1 into 2x + ky = 8.",
                 substituted, input_state=first,
                 substitution=point,
                 why_valid="Lying on the line is defined by the equation being satisfied.",
                 explanation="Putting (2, 1) into 2x + ky gives 2(2) + k(1), which must "
                             "equal 8.",
                 witness=witness("T1", "SUBSTITUTE", first, substituted, "SOLUTION_SET",
                                 "(2, 1) is a declared point of the line, so substituting it "
                                 "states a true equation rather than assuming one."),
                 evidence="MATH-C1L-POINT-ON-LINE"),
            step("S3", "EXECUTE", "EVALUATE",
                 "2(2) is 4 and k(1) is k, so the equation becomes 4 + k = 8.",
                 simplified, input_state=substituted,
                 substitution=seq(num(4), op("PLUS"), k),
                 why_valid="Both products are evaluated by ordinary arithmetic.",
                 explanation="After putting (2, 1) in, 2x + ky = 8 has collapsed to the "
                             "single equation 4 + k = 8."),
            step("S4", "TRANSFORM", "REARRANGE",
                 "Subtract 4 from both sides of 4 + k = 8.",
                 solved, input_state=simplified,
                 substitution=num(4),
                 why_valid="Subtracting the same number from both sides is reversible, so no "
                           "solution is gained or lost.",
                 explanation="4 + k = 8 gives k = 4, so the line through (2, 1) is "
                             "2x + 4y = 8.",
                 witness=witness("T2", "SUBTRACT_FROM_BOTH_SIDES", simplified, solved,
                                 "SOLUTION_SET",
                                 "Subtracting 4 from both sides is reversible by adding 4, so "
                                 "the solution set is unchanged."),
                 evidence="MATH-C1L-EQUALITY-PRESERVATION"),
            step("S5", "CHECK_SUFFICIENCY", "COMPARE_VALUES",
                 "With k = 4 the second equation is exactly twice the first, so the two "
                 "equations carry the same information.",
                 dependent, input_state=second,
                 substitution=num(2),
                 why_valid="Two equations that are multiples of each other describe the same "
                           "line, so their common solutions form that whole line.",
                 explanation="4x + 8y = 16 is 2 times 2x + 4y = 8, so every point of the "
                             "line satisfies both and (2, 1) is not the only one.",
                 sufficiency={
                     "status": "MULTIPLE",
                     "reason": "The second equation is a multiple of the first, so the pair "
                               "is dependent and every point of the line is a solution.",
                     "parameter_refs": ["k"],
                 },
                 evidence="MATH-C1L-INFORMATION-SUFFICIENCY"),
            step("S6", "VERIFY", "CHECK",
                 "Substitute (2, 1) into 2x + 4y and expect exactly 8.",
                 verify, input_state=solved,
                 substitution=point,
                 why_valid="The value of k is only correct if the original point still "
                           "satisfies the completed equation.",
                 explanation="2(2) + 4(1) is 4 + 4, which is 8, so k = 4 really does put "
                             "(2, 1) on the line."),
        ],
        "scaffold": {
            "H1": hint("What does it mean, as an equation, for (2, 1) to be on the line "
                       "2x + ky = 8?", "S2", "MATH-C1L-POINT-ON-LINE"),
            "H2": hint("Turn the statement about (2, 1) into a single equation in k alone.",
                       "S3", "MATH-C1L-POINT-ON-LINE"),
            "H3": hint("Replace x and y in 2x + ky by the numbers from (2, 1) before doing "
                       "anything with k.", "S4"),
        },
        "answer_custody": {
            "question_ref": "LE-I1",
            "answer_kind": "NUMERIC",
            "final_answer": solved,
            "final_answer_prose": "k = 4. With that value the second equation is twice the "
                                  "first, so the pair does not fix a single ordered pair: "
                                  "every point of the line 2x + 4y = 8 is a solution.",
            "model_proof_steps": [],
            "acceptance_rule": None,
            "admissible_answers": [],
            "construction_verification_conditions": [],
            "counterexample_witness": None,
            "independent_verification": {
                "kind": "SUBSTITUTE_BACK",
                "executable": True,
                "statement": "Substitute x = 2 and y = 1 into 2x + 4y. The result must be "
                             "exactly 8, and one further point such as x = 0, y = 2 must "
                             "also satisfy both equations.",
                "expected": verify,
            },
            "quick_check": "Is your k a single number or a range?",
            "placement": "ANSWER_APPENDIX",
            "attempt_surface_answer_neutral": True,
        },
        "source_distance": {
            "source_question_reuse": False,
            "basis": "Authored inside the linear-parameter-sufficiency family; the parameter "
                     "and point are not taken from an assessment item.",
        },
    }


BUILDERS = (number_systems, polynomials, coordinate_geometry, linear_equations)
PARAMETERIZED_ITEMS = ("LE-I1",)


def build() -> dict:
    realizations = [seal_realization(builder()) for builder in BUILDERS]
    return {
        "fixture_id": "MATH-REFERENCE-REALIZATIONS-v1",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "purpose": "Reference learner mathematical realizations for four of the seven "
                   "stress-tested Grade 9 topics. Data instances of the subject-wide "
                   "contracts; no topic contributes a schema shape.",
        "parameterized_items": list(PARAMETERIZED_ITEMS),
        "realizations": realizations,
    }


def main() -> None:
    payload = build()
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(payload['realizations'])} realizations")
    for realization in payload["realizations"]:
        print(f"  {realization['topic_ref']:>20} {realization['item_ref']:<7} "
              f"{realization['role']:<12} steps={len(realization['derivation'])} "
              f"{realization['realization_id']}")


if __name__ == "__main__":
    main()
