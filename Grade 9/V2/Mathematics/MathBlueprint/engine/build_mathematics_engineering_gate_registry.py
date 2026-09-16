#!/usr/bin/env python3
"""Builds the canonical Mathematics Technical Engineering Gate Registry (v1).

Enforces mathematical rigor, definition domains, symbol structures, representation schemas,
and 10-point technical readiness across Grades 9-11 foundational mathematics.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = ROOT / "policies"
OUT_PATH = POLICY_DIR / "mathematics-technical-engineering-gates.v1.json"


def build_registry() -> dict:
    if OUT_PATH.exists():
        return json.loads(OUT_PATH.read_text(encoding="utf-8"))
    subtopics = [
        # 1. MATH-NUM-RADICALS
        {
            "subtopic_id": "MATH-NUM-RADICALS",
            "learner_title": "Real Numbers, Radicals & Conjugate Rationalization",
            "chapter": "Number Systems",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class IX Mathematics, Chapter 1: Number Systems",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-REAL-NUMBER-SYSTEM",
                "CON-MATH-PRINCIPAL-SQUARE-ROOT-ABS",
                "CON-MATH-CONJUGATE-RATIONALIZATION"
            ],
            "prerequisite_ids": [],
            "linked_buckets": ["BUCKET-MATH-NUMBERS"],
            "linked_problem_family_ids": [
                "PF-MATH-RADICAL-SIMPLIFICATION",
                "PF-MATH-CONJUGATE-RATIONALIZATION"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-REAL-NUMBER-SYSTEM",
                    "canonical_statement": "Real numbers comprise rational numbers Q and irrational numbers R \\ Q, represented uniquely on a continuous geometric number line.",
                    "why_required": "Grounds the domain of discourse for arithmetic operations and square roots.",
                    "failure_if_omitted": "Learner cannot distinguish terminating/repeating rationals from non-terminating non-repeating surds."
                },
                {
                    "concept_id": "CON-MATH-PRINCIPAL-SQUARE-ROOT-ABS",
                    "canonical_statement": "For any real number x, the principal square root is defined such that sqrt(x^2) = |x| >= 0. The principal square root function maps [0, inf) to [0, inf).",
                    "why_required": "Prevents the fatal fallacy that sqrt(25) = +-5, distinguishing function output from polynomial root finding.",
                    "failure_if_omitted": "Equations involving radicals produce extraneous negative solutions and violate function single-valuedness."
                },
                {
                    "concept_id": "CON-MATH-CONJUGATE-RATIONALIZATION",
                    "canonical_statement": "Fractions with radical binomial denominators a +- sqrt(b) are rationalized by multiplying numerator and denominator by the conjugate a -+ sqrt(b) via (a+b)(a-b) = a^2 - b^2.",
                    "why_required": "Standard canonical form for real algebraic evaluation and comparison.",
                    "failure_if_omitted": "Denominator radicals prevent algebraic addition and comparison of real values."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-RADICAL-IDENTITY",
                    "formula": "\\sqrt{x^2} = |x|",
                    "meaning_of_symbols": "x is any real number; |x| is the absolute value guaranteeing non-negativity.",
                    "symbols": [
                        {
                            "symbol": "x",
                            "name": "Real Variable",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Radicand base"
                        },
                        {
                            "symbol": "|x|",
                            "name": "Absolute Value",
                            "domain": "[0, \\infty)",
                            "geometric_or_algebraic_role": "Principal radical non-negative magnitude"
                        }
                    ],
                    "reference_frame_or_sign": "Principal square root is non-negative on [0, \\infty)",
                    "conditions_of_validity": "Valid for all real x.",
                    "obligations": ["EXPLAIN", "INTERPRET", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-CONJUGATE-RATIONAL",
                    "formula": "\\frac{1}{a + \\sqrt{b}} = \\frac{a - \\sqrt{b}}{a^2 - b}",
                    "meaning_of_symbols": "a is rational, b is non-negative rational not a perfect square, a^2 != b.",
                    "symbols": [
                        {
                            "symbol": "a",
                            "name": "Rational Term",
                            "domain": "\\mathbb{Q}",
                            "geometric_or_algebraic_role": "Rational component of binomial"
                        },
                        {
                            "symbol": "b",
                            "name": "Radicand",
                            "domain": "\\mathbb{Q}^+ \\setminus \\{k^2 : k \\in \\mathbb{Q}\\}",
                            "geometric_or_algebraic_role": "Surd radicand"
                        }
                    ],
                    "reference_frame_or_sign": "Denominator non-zero: a^2 != b",
                    "conditions_of_validity": "b >= 0, a^2 - b != 0",
                    "obligations": ["DERIVE", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-NUMBER-LINE-INTERVAL",
                    "representation_type": "NUMBER_LINE_INTERVAL",
                    "name": "Real Number Line Interval Representation",
                    "math_encoded": "Continuous 1D axis with origin 0, positive right, showing nested sqrt(2), sqrt(3), pi geometric spiral points.",
                    "mandatory_labels": ["Origin (0)", "Unit 1", "Irrational Position \\sqrt{2}", "Positive Direction"],
                    "what_cannot_be_omitted": "Metric scale uniformity and non-negative root placement.",
                    "common_incorrect_version": "Treating irrational points as approximate integers without exact geometric projection.",
                    "verification_method": "Pythagorean spiral projection check (hypotenuse of 1, 1 gives sqrt(2))."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Radicand under square root must be non-negative in real domain (x >= 0 for sqrt(x)).",
                    "why_needed": "Real number field is not algebraically closed for negative square roots.",
                    "what_changes_if_violated": "Values become complex numbers, violating real number system scope."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Identify radicand domain and evaluate principal square root non-negativity.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Construct conjugate factor of radical binomial denominator.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Expand denominator using difference of squares to eliminate all irrational radical terms.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Radical fraction with surd denominator",
                    "to_mode": "Rationalized denominator standard form",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Transform 1/(a + sqrt(b)) into (a - sqrt(b))/(a^2 - b) using algebraic conjugate."
                },
                {
                    "from_mode": "Radical equation algebraic solution",
                    "to_mode": "Domain-checked verified principal root",
                    "target_core_role": "CORE2B_GENERATIVE_TRANSFER",
                    "description": "Filter extraneous solutions arising from squaring by verifying original equation."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-SQUARE-ROOT-PLUS-MINUS",
                    "incorrect_belief": "Believing sqrt(25) = +-5 rather than strictly +5.",
                    "why_plausible": "Confusing the solutions of x^2 = 25 (which are x = +5 and x = -5) with the output of the principal square root function sqrt(25).",
                    "required_counterexample": "Evaluate sqrt((-5)^2). If sqrt meant +-, sqrt((-5)^2) would be -5, but by definition of absolute value sqrt((-5)^2) = |-5| = +5.",
                    "required_technical_repair": "Strictly enforce sqrt(x^2) = |x| >= 0 as a single-valued function."
                }
            ],
            "mandatory_verifications": [
                "Square the rationalized expression and compare with original.",
                "Verify non-negativity of principal radical evaluation on test values."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-RADICAL-SIMPLIFICATION",
                    "name": "Simplification of Compound Surd Expressions",
                    "recognition_cues": "Radical expressions with nested or fractional surds.",
                    "first_technical_move": "Factor radicands into prime powers and extract perfect squares using sqrt(a^2 b) = |a| sqrt(b).",
                    "common_fatal_error": "Distributing radical over addition: sqrt(a+b) = sqrt(a) + sqrt(b).",
                    "typical_unknown": "Simplified canonical radical form"
                },
                {
                    "family_id": "PF-MATH-CONJUGATE-RATIONALIZATION",
                    "name": "Conjugate Rationalization of Binomial Denominators",
                    "recognition_cues": "Fractions with radical expressions in denominator.",
                    "first_technical_move": "Multiply numerator and denominator by algebraic conjugate.",
                    "common_fatal_error": "Multiplying only denominator or using wrong sign in conjugate.",
                    "typical_unknown": "Rationalized fraction"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 0,
                "element_interactivity": 1,
                "inferential_jump_severity": 1,
                "representation_translation": 1,
                "model_discrimination": 1,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 1,
                "abstraction": 1,
                "misconception_density": 2,
                "synthesis": 1,
                "provisional_difficulty": "EASY",
                "difficulty_basis": "Elementary real arithmetic and radical identities.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["RADICAL_RIGOR", "REAL_FOUNDATION"],
                "conditional_badges": ["CONJUGATE_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-RADICAL-01",
                    "authoring_defect": "Omitting absolute value in sqrt(x^2), allowing negative outputs.",
                    "expected_failure_reason": "Violates principal square root definition and single-valued function contract."
                }
            ]
        },

        # 2. MATH-ALG-POLYNOMIALS
        {
            "subtopic_id": "MATH-ALG-POLYNOMIALS",
            "learner_title": "Polynomials, Factor Theorem & Algebraic Identities",
            "chapter": "Algebra",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class IX & X Mathematics, Polynomials",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-POLYNOMIAL-DEGREE",
                "CON-MATH-FACTOR-THEOREM",
                "CON-MATH-ALGEBRAIC-IDENTITIES"
            ],
            "prerequisite_ids": ["MATH-NUM-RADICALS"],
            "linked_buckets": ["BUCKET-MATH-POLYNOMIALS"],
            "linked_problem_family_ids": [
                "PF-MATH-POLYNOMIAL-FACTORIZATION",
                "PF-MATH-IDENTITY-EXPANSION"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-POLYNOMIAL-DEGREE",
                    "canonical_statement": "A polynomial P(x) = sum_{k=0}^n a_k x^k has degree n when a_n != 0. Degree is strictly additive under polynomial multiplication: deg(P * Q) = deg(P) + deg(Q).",
                    "why_required": "Governs maximum number of roots and structural classification.",
                    "failure_if_omitted": "Learner equates polynomials of differing degrees or claims degree of zero polynomial is zero."
                },
                {
                    "concept_id": "CON-MATH-FACTOR-THEOREM",
                    "canonical_statement": "For a polynomial P(x), a linear term (x - c) is a factor if and only if P(c) = 0. Consequently, P(x) = (x - c) Q(x) with remainder R = 0.",
                    "why_required": "Fundamental bridge between roots of algebraic equations and polynomial factorization.",
                    "failure_if_omitted": "Trial-and-error guessing replaces rigorous root-factor equivalence."
                },
                {
                    "concept_id": "CON-MATH-ALGEBRAIC-IDENTITIES",
                    "canonical_statement": "Exact polynomial identities hold universally: (a+b)^2 = a^2 + 2ab + b^2, (a-b)^2 = a^2 - 2ab + b^2, a^2 - b^2 = (a-b)(a+b), and (a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3.",
                    "why_required": "Provides foundational algebraic invariants for expansion and factorization.",
                    "failure_if_omitted": "Produces persistent Freshman's dream algebraic errors."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-FACTOR-THEOREM",
                    "formula": "P(x) = (x - c) Q(x) + P(c)",
                    "meaning_of_symbols": "P(x) is dividend polynomial, (x-c) is linear divisor, Q(x) is quotient polynomial, P(c) is remainder.",
                    "symbols": [
                        {
                            "symbol": "P(x)",
                            "name": "Dividend Polynomial",
                            "domain": "\\mathbb{R}[x]",
                            "geometric_or_algebraic_role": "Target polynomial"
                        },
                        {
                            "symbol": "c",
                            "name": "Evaluation Point",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Potential root"
                        },
                        {
                            "symbol": "Q(x)",
                            "name": "Quotient Polynomial",
                            "domain": "\\mathbb{R}[x]",
                            "geometric_or_algebraic_role": "Degree n-1 quotient"
                        }
                    ],
                    "reference_frame_or_sign": "Divisor degree 1; remainder degree 0 (constant)",
                    "conditions_of_validity": "Valid for all polynomials P(x) with deg(P) >= 1.",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-BINOMIAL-SQUARE",
                    "formula": "(a + b)^2 = a^2 + 2ab + b^2",
                    "meaning_of_symbols": "a and b are real numbers or algebraic expressions; 2ab is mandatory cross-term.",
                    "symbols": [
                        {
                            "symbol": "a",
                            "name": "First Binomial Term",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "First component"
                        },
                        {
                            "symbol": "b",
                            "name": "Second Binomial Term",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Second component"
                        }
                    ],
                    "reference_frame_or_sign": "Cross term sign positive for (a+b)^2, negative for (a-b)^2",
                    "conditions_of_validity": "Valid in any commutative ring.",
                    "obligations": ["EXPLAIN", "REPRESENT", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-ALGEBRAIC-EXPANSION-GRID",
                    "representation_type": "ALGEBRAIC_EXPANSION_GRID",
                    "name": "Algebraic Area Expansion Grid",
                    "math_encoded": "2x2 grid representing area of square (a+b) by (a+b) split into sub-rectangles: a^2, ab, ab, b^2.",
                    "mandatory_labels": ["Side a", "Side b", "Area a^2", "Area ab", "Area b^2", "Total Area (a+b)^2"],
                    "what_cannot_be_omitted": "The two ab rectangular quadrants illustrating the 2ab cross-product term.",
                    "common_incorrect_version": "Omitting the two cross-product quadrants, showing only a^2 and b^2.",
                    "verification_method": "Geometric area equality: Area_total = sum(Area_subrectangles)."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Exponents of variable in polynomial must be non-negative integers (n in {0, 1, 2, ...}).",
                    "why_needed": "Expressions with negative or fractional powers are not polynomials.",
                    "what_changes_if_violated": "Division algorithm and factor theorem fail for non-polynomial rational/radical functions."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Check polynomial degree and variable exponent integrality.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Apply Remainder/Factor theorem: evaluate P(c) to test whether (x-c) divides P(x).",
                    "inferential_jump": "MEDIUM"
                },
                {
                    "step": 3,
                    "expert_action": "Synthesize quotient Q(x) via polynomial division or synthetic division, ensuring degree reduction.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Expanded polynomial form",
                    "to_mode": "Factored product of irreducible polynomials",
                    "target_core_role": "CORE1B_GENERATIVE_RECONSTRUCTION",
                    "description": "Factor quadratic and cubic expressions via factor theorem and identity patterns."
                },
                {
                    "from_mode": "Geometric rectangle partition",
                    "to_mode": "Formal algebraic identity expansion",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Translate visual area model into rigorous algebraic identity with cross-product."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-FRESHMANS-DREAM",
                    "incorrect_belief": "Claiming (a+b)^2 = a^2 + b^2 by dropping the cross-product term 2ab.",
                    "why_plausible": "Superficial distribution of exponent 2 across the addition operator.",
                    "required_counterexample": "Let a = 2, b = 3. (2+3)^2 = 5^2 = 25, but 2^2 + 3^2 = 4 + 9 = 13 != 25. The difference is 2*2*3 = 12.",
                    "required_technical_repair": "Enforce geometric expansion grid and algebraic expansion step (a+b)(a+b) = a^2 + ab + ba + b^2."
                }
            ],
            "mandatory_verifications": [
                "Re-expand factors to verify original polynomial is recovered identically.",
                "Verify P(root) equals zero numerically."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-POLYNOMIAL-FACTORIZATION",
                    "name": "Factorization of Quadratics and Cubics via Factor Theorem",
                    "recognition_cues": "Polynomials given with degree >= 2 requiring factor product form.",
                    "first_technical_move": "Find rational zero c from factors of constant term / leading coefficient, verify P(c) = 0.",
                    "common_fatal_error": "Sign error in factor: testing P(c)=0 and writing factor as (x+c) instead of (x-c).",
                    "typical_unknown": "Complete factorization"
                },
                {
                    "family_id": "PF-MATH-IDENTITY-EXPANSION",
                    "name": "Algebraic Expansion & Identity Application",
                    "recognition_cues": "Compound binomial/trinomial squares or cubes requiring standard form.",
                    "first_technical_move": "Match expression with standard identity template (a+-b)^2, (a+-b)^3, or (a+b+c)^2.",
                    "common_fatal_error": "Omitting cross terms or misapplying sign in negative terms.",
                    "typical_unknown": "Fully expanded polynomial"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 1,
                "element_interactivity": 2,
                "inferential_jump_severity": 1,
                "representation_translation": 2,
                "model_discrimination": 1,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 2,
                "abstraction": 2,
                "misconception_density": 3,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Multi-step polynomial factoring and identity expansion.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["POLYNOMIAL_FOUNDATION", "FACTOR_RIGOR"],
                "conditional_badges": ["IDENTITY_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-POLY-01",
                    "authoring_defect": "Allowing (a+b)^2 = a^2 + b^2 without cross-product correction.",
                    "expected_failure_reason": "Violates algebraic identity invariance and distributivity."
                }
            ]
        },

        # 3. MATH-LIN-EQUATIONS
        {
            "subtopic_id": "MATH-LIN-EQUATIONS",
            "learner_title": "Linear Systems in Two Variables & Consistency Classification",
            "chapter": "Algebra",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class X Mathematics, Chapter 3: Pair of Linear Equations in Two Variables",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-LINEAR-SYSTEM-FORM",
                "CON-MATH-LINEAR-SYSTEM-CONSISTENCY",
                "CON-MATH-ALGEBRAIC-ELIMINATION"
            ],
            "prerequisite_ids": ["MATH-ALG-POLYNOMIALS"],
            "linked_buckets": ["BUCKET-MATH-LINEAR-EQUATIONS"],
            "linked_problem_family_ids": [
                "PF-MATH-SYSTEM-SOLVING",
                "PF-MATH-CONSISTENCY-CLASSIFICATION"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-LINEAR-SYSTEM-FORM",
                    "canonical_statement": "A pair of linear equations in two variables has standard form a1 x + b1 y + c1 = 0 and a2 x + b2 y + c2 = 0, where a_i^2 + b_i^2 != 0.",
                    "why_required": "Establishes non-degeneracy of geometric lines in R^2.",
                    "failure_if_omitted": "Allows degenerate equations like 0x + 0y = 5 to be treated as linear equations."
                },
                {
                    "concept_id": "CON-MATH-LINEAR-SYSTEM-CONSISTENCY",
                    "canonical_statement": "System consistency is completely classified by coefficient ratios: a1/a2 != b1/b2 -> unique solution (intersecting); a1/a2 = b1/b2 != c1/c2 -> no solution (inconsistent parallel lines); a1/a2 = b1/b2 = c1/c2 -> infinitely many solutions (coincident lines).",
                    "why_required": "Provides deterministic algebraic classification before embarking on algorithmic solving.",
                    "failure_if_omitted": "Learner performs blind elimination on inconsistent systems resulting in absurdities like 0 = 5."
                },
                {
                    "concept_id": "CON-MATH-ALGEBRAIC-ELIMINATION",
                    "canonical_statement": "Solution sets are preserved under elementary row operations: multiplying an equation by a non-zero constant and adding it to another eliminates one variable deterministically.",
                    "why_required": "Guarantees algebraic correctness of elimination and substitution methods.",
                    "failure_if_omitted": "Learner multiplies equations by variable expressions, introducing extraneous solutions or division by zero."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-RATIO-CONSISTENCY",
                    "formula": "\\frac{a_1}{a_2} = \\frac{b_1}{b_2} = \\frac{c_1}{c_2}",
                    "meaning_of_symbols": "a_i, b_i, c_i are real coefficients of the linear system; equality dictates coincident lines.",
                    "symbols": [
                        {
                            "symbol": "a_1, a_2",
                            "name": "x-coefficients",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Normal vector x-components"
                        },
                        {
                            "symbol": "b_1, b_2",
                            "name": "y-coefficients",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Normal vector y-components"
                        },
                        {
                            "symbol": "c_1, c_2",
                            "name": "Constant terms",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Affine translation offsets"
                        }
                    ],
                    "reference_frame_or_sign": "Standard form a x + b y + c = 0 with all terms on LHS or RHS consistently",
                    "conditions_of_validity": "Valid when a2, b2, c2 != 0; otherwise use cross-multiplication form a1 b2 - a2 b1 = 0.",
                    "obligations": ["EXPLAIN", "INTERPRET", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-CARTESIAN-LINES",
                    "representation_type": "CARTESIAN_COORDINATE_PLOT",
                    "name": "Cartesian Dual-Line Intersecting/Parallel Plot",
                    "math_encoded": "2D Cartesian plane showing L1: a1 x + b1 y + c1 = 0 and L2: a2 x + b2 y + c2 = 0 with intersection point (x*, y*).",
                    "mandatory_labels": ["x-axis", "y-axis", "Line L1", "Line L2", "Intersection Point (x*, y*)"],
                    "what_cannot_be_omitted": "Explicit coordinate values of intersection point and slopes.",
                    "common_incorrect_version": "Sketching parallel lines but claiming a unique solution exists algebraically.",
                    "verification_method": "Substitute intersection coordinates (x*, y*) into both L1 and L2 equations."
                }
            ],
            "model_conditions": [
                {
                    "condition": "At least one coefficient of each variable must be non-zero (a_i^2 + b_i^2 > 0).",
                    "why_needed": "Prevents degenerate relations that do not represent lines.",
                    "what_changes_if_violated": "Equation ceases to represent a line in R^2."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Put both equations into standard form a x + b y + c = 0.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Compute coefficient ratios a1/a2, b1/b2, c1/c2 to determine consistency status.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Execute elimination or substitution to solve for unique point if consistent, or state parallel/coincident conclusion.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Word problem narrative constraints",
                    "to_mode": "Paired linear algebraic equations in standard form",
                    "target_core_role": "CORE2A_DECLARATIVE_WORKED_PROBLEM",
                    "description": "Formulate word problems into standard linear systems."
                },
                {
                    "from_mode": "Algebraic solution pair (x, y)",
                    "to_mode": "Geometric point of intersection on coordinate plane",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Translate algebraic solution into geometric Cartesian intersection."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-PARALLEL-DIVIDE-ZERO",
                    "incorrect_belief": "Attempting to solve parallel linear systems without checking ratios, concluding 0 = 7 means x = 0.",
                    "why_plausible": "Failure to recognize that false statement 0 = k indicates empty solution set (inconsistent).",
                    "required_counterexample": "Solve 2x + 3y = 4 and 4x + 6y = 10. Elimination gives 0 = -2, which means no (x, y) satisfies both lines.",
                    "required_technical_repair": "Check a1/a2 vs b1/b2 vs c1/c2 ratio test before initiating elimination."
                }
            ],
            "mandatory_verifications": [
                "Substitute calculated (x, y) into both original equations.",
                "Verify consistency status matches coefficient ratio conditions."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-SYSTEM-SOLVING",
                    "name": "Solving Simultaneous Linear Systems",
                    "recognition_cues": "Two linear equations with two unknowns requiring exact solution.",
                    "first_technical_move": "Check consistency ratio, then multiply equations to equate coefficients of one variable.",
                    "common_fatal_error": "Sign errors during subtraction of equations.",
                    "typical_unknown": "Ordered pair (x, y)"
                },
                {
                    "family_id": "PF-MATH-CONSISTENCY-CLASSIFICATION",
                    "name": "Classification of Linear Systems by Parameters",
                    "recognition_cues": "Systems containing variable parameter k requiring conditions for unique, none, or infinite solutions.",
                    "first_technical_move": "Set up ratio equations a1/a2 = b1/b2 for parallel/coincident, or != for unique.",
                    "common_fatal_error": "Ignoring constant term ratio c1/c2 when distinguishing parallel from coincident.",
                    "typical_unknown": "Parameter range for specified consistency condition"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 1,
                "element_interactivity": 2,
                "inferential_jump_severity": 1,
                "representation_translation": 2,
                "model_discrimination": 2,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 2,
                "abstraction": 2,
                "misconception_density": 2,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Simultaneous equation elimination and geometric consistency classification.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["LINEAR_SYSTEMS", "CONSISTENCY_GATE"],
                "conditional_badges": ["ELIMINATION_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-LIN-01",
                    "authoring_defect": "Accepting 0=k as x=0 rather than recognizing inconsistent parallel system.",
                    "expected_failure_reason": "Violates logical consistency classification of linear systems."
                }
            ]
        },

        # 4. MATH-QUAD-EQUATIONS
        {
            "subtopic_id": "MATH-QUAD-EQUATIONS",
            "learner_title": "Quadratic Equations, Discriminant Analysis & Vieta Relations",
            "chapter": "Algebra",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class X Mathematics, Chapter 4: Quadratic Equations",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-QUAD-NONZERO-LEAD",
                "CON-MATH-QUAD-DISCRIMINANT-TRICHOTOMY",
                "CON-MATH-VIETA-RELATIONS"
            ],
            "prerequisite_ids": ["MATH-ALG-POLYNOMIALS"],
            "linked_buckets": ["BUCKET-MATH-QUADRATICS"],
            "linked_problem_family_ids": [
                "PF-MATH-QUAD-ROOT-FINDING",
                "PF-MATH-DISCRIMINANT-ANALYSIS"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-QUAD-NONZERO-LEAD",
                    "canonical_statement": "A quadratic equation has the standard form ax^2 + bx + c = 0 where a, b, c in R and leading coefficient a != 0.",
                    "why_required": "Leading coefficient a != 0 guarantees the polynomial degree is exactly 2.",
                    "failure_if_omitted": "Allows division by zero in quadratic formula and misclassifies linear equations as quadratics."
                },
                {
                    "concept_id": "CON-MATH-QUAD-DISCRIMINANT-TRICHOTOMY",
                    "canonical_statement": "The discriminant Delta = b^2 - 4ac partitions solutions into three mutually exclusive regimes: Delta > 0 (two distinct real roots), Delta = 0 (two equal real roots), Delta < 0 (no real roots / complex conjugate pair).",
                    "why_required": "Determines existence and nature of real solutions without full calculation.",
                    "failure_if_omitted": "Learner invents imaginary outputs or attempts real square root of negative numbers without domain qualification."
                },
                {
                    "concept_id": "CON-MATH-VIETA-RELATIONS",
                    "canonical_statement": "For roots alpha, beta of ax^2 + bx + c = 0 (a != 0), sum of roots is alpha + beta = -b/a and product of roots is alpha * beta = c/a.",
                    "why_required": "Permits algebraic synthesis and verification of coefficients from roots.",
                    "failure_if_omitted": "Learner cannot construct quadratics from roots or evaluate symmetric functions of roots."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-QUAD-FORMULA",
                    "formula": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
                    "meaning_of_symbols": "x represents the roots; a is non-zero leading coefficient; b is linear coefficient; c is constant; b^2 - 4ac is discriminant.",
                    "symbols": [
                        {
                            "symbol": "a",
                            "name": "Leading Coefficient",
                            "domain": "\\mathbb{R} \\setminus \\{0\\}",
                            "geometric_or_algebraic_role": "Parabola curvature and leading scale"
                        },
                        {
                            "symbol": "b",
                            "name": "Linear Coefficient",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Axis of symmetry shift"
                        },
                        {
                            "symbol": "c",
                            "name": "Constant Term",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "y-intercept"
                        },
                        {
                            "symbol": "x",
                            "name": "Roots",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "x-intercept solutions"
                        }
                    ],
                    "reference_frame_or_sign": "Denominator sign depends on a; radical +- yields two branches",
                    "conditions_of_validity": "Valid when a != 0; real roots require b^2 - 4ac >= 0.",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-DISCRIMINANT",
                    "formula": "\\Delta = b^2 - 4ac",
                    "meaning_of_symbols": "Delta is the discriminant whose sign determines root multiplicity and reality.",
                    "symbols": [
                        {
                            "symbol": "\\Delta",
                            "name": "Discriminant",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Root nature classifier"
                        }
                    ],
                    "reference_frame_or_sign": "Delta > 0 distinct, Delta = 0 equal, Delta < 0 non-real",
                    "conditions_of_validity": "Valid for all quadratic polynomials with real coefficients.",
                    "obligations": ["INTERPRET", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-PARABOLA-ROOT-PLOT",
                    "representation_type": "SIGN_CHART_OR_DISCRIMINANT_PLOT",
                    "name": "Parabola Axis Intercept & Discriminant Geometry",
                    "math_encoded": "2D Cartesian plot of y = ax^2 + bx + c showing vertex (-b/2a, -Delta/4a) and x-intercepts relative to Delta sign.",
                    "mandatory_labels": ["x-axis", "y-axis", "Vertex", "Axis of Symmetry x = -b/(2a)", "x-intercepts"],
                    "what_cannot_be_omitted": "Sign of Delta illustrated by whether parabola intersects (Delta>0), touches (Delta=0), or avoids (Delta<0) x-axis.",
                    "common_incorrect_version": "Plotting parabola intersecting x-axis when discriminant is negative.",
                    "verification_method": "Check vertex y-coordinate equals -Delta/(4a)."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Leading coefficient a must be non-zero (a != 0).",
                    "why_needed": "If a = 0, the equation reduces to linear and quadratic formula results in division by zero.",
                    "what_changes_if_violated": "Quadratic formula produces 0/0 or division by zero, invalidating derivation."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Verify standard form ax^2 + bx + c = 0 and ensure leading coefficient a != 0.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Compute discriminant Delta = b^2 - 4ac and classify root regime.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Calculate roots via quadratic formula or factoring, verifying with Vieta relations.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Standard quadratic form ax^2 + bx + c = 0",
                    "to_mode": "Completed square form a(x + b/2a)^2 = Delta/(4a)",
                    "target_core_role": "CORE1B_GENERATIVE_RECONSTRUCTION",
                    "description": "Derive quadratic formula by executing completing the square."
                },
                {
                    "from_mode": "Geometric parabola intercept configuration",
                    "to_mode": "Algebraic discriminant sign constraint",
                    "target_core_role": "CORE2B_GENERATIVE_TRANSFER",
                    "description": "Determine parameter bounds for which parabola has specified number of real roots."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-ZERO-LEADING-COEFF",
                    "incorrect_belief": "Assuming ax^2 + bx + c = 0 remains quadratic when parameter a = 0, applying quadratic formula.",
                    "why_plausible": "Treating formula as purely symbolic string without domain restrictions.",
                    "required_counterexample": "Consider (k-1)x^2 + 4x + 2 = 0 with k = 1. Equation becomes 4x + 2 = 0, which has exactly one root x = -1/2, not two roots.",
                    "required_technical_repair": "Enforce mandatory explicit check that leading coefficient a != 0 before quadratic procedures."
                }
            ],
            "mandatory_verifications": [
                "Substitute roots back into ax^2 + bx + c to confirm evaluation to zero.",
                "Verify alpha + beta = -b/a and alpha * beta = c/a."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-QUAD-ROOT-FINDING",
                    "name": "Solving Quadratic Equations via Formula and Factoring",
                    "recognition_cues": "Quadratic equation requiring exact real solutions.",
                    "first_technical_move": "Bring all terms to one side, check a != 0, compute Delta = b^2 - 4ac.",
                    "common_fatal_error": "Sign errors in -b or -4ac when b or c is negative.",
                    "typical_unknown": "Roots x_1, x_2"
                },
                {
                    "family_id": "PF-MATH-DISCRIMINANT-ANALYSIS",
                    "name": "Nature of Roots & Parameter Determination",
                    "recognition_cues": "Problems specifying real, distinct, equal, or no real roots with unknown parameter k.",
                    "first_technical_move": "Express Delta(k) as polynomial in k and set Delta >= 0, Delta = 0, or Delta < 0.",
                    "common_fatal_error": "Forgetting the constraint that leading coefficient a(k) != 0.",
                    "typical_unknown": "Parameter value or interval for k"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 2,
                "element_interactivity": 2,
                "inferential_jump_severity": 2,
                "representation_translation": 2,
                "model_discrimination": 2,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 2,
                "abstraction": 2,
                "misconception_density": 2,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Completing the square, discriminant analysis, and root-coefficient relations.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["QUADRATIC_RIGOR", "DISCRIMINANT_MASTERY"],
                "conditional_badges": ["VIETA_EXPERT"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-QUAD-01",
                    "authoring_defect": "Omitting a != 0 leading coefficient condition.",
                    "expected_failure_reason": "Causes division by zero and violates definition of second-degree polynomial."
                }
            ]
        },

        # 5. MATH-GEO-COORDINATES
        {
            "subtopic_id": "MATH-GEO-COORDINATES",
            "learner_title": "Coordinate Geometry, Distance Metric & Collinearity",
            "chapter": "Coordinate Geometry",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class X Mathematics, Chapter 7: Coordinate Geometry",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-CARTESIAN-DISTANCE-METRIC",
                "CON-MATH-SECTION-MIDPOINT",
                "CON-MATH-VERTICAL-SLOPE-UNDEFINED"
            ],
            "prerequisite_ids": ["MATH-NUM-RADICALS", "MATH-ALG-POLYNOMIALS"],
            "linked_buckets": ["BUCKET-MATH-COORDINATE-GEOMETRY"],
            "linked_problem_family_ids": [
                "PF-MATH-DISTANCE-CALCULATION",
                "PF-MATH-COLLINEARITY-VERIFICATION"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-CARTESIAN-DISTANCE-METRIC",
                    "canonical_statement": "The Euclidean metric d(P, Q) = sqrt((x2 - x1)^2 + (y2 - y1)^2) is non-negative, symmetric d(P, Q) = d(Q, P), and satisfies triangle inequality d(P, R) <= d(P, Q) + d(Q, R).",
                    "why_required": "Foundational distance measure connecting algebra and geometry.",
                    "failure_if_omitted": "Sign errors in delta x and delta y lead to negative square root arguments."
                },
                {
                    "concept_id": "CON-MATH-SECTION-MIDPOINT",
                    "canonical_statement": "The coordinates of a point P dividing the segment joining A(x1, y1) and B(x2, y2) internally in ratio m:n are ((m x2 + n x1)/(m+n), (m y2 + n y1)/(m+n)).",
                    "why_required": "Enables algebraic partition of geometric line segments.",
                    "failure_if_omitted": "Learner inverts internal ratio weights m and n relative to coordinates."
                },
                {
                    "concept_id": "CON-MATH-VERTICAL-SLOPE-UNDEFINED",
                    "canonical_statement": "The slope of a line segment connecting (x1, y1) and (x2, y2) is m = (y2 - y1)/(x2 - x1), defined if and only if x1 != x2. For x1 = x2, the segment is vertical and slope is undefined, not zero.",
                    "why_required": "Avoids division by zero and distinguishes vertical lines (slope undefined) from horizontal lines (slope zero).",
                    "failure_if_omitted": "Vertical lines are treated as having zero slope, conflating horizontal and vertical geometry."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-DISTANCE-FORMULA",
                    "formula": "d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}",
                    "meaning_of_symbols": "d is Euclidean distance; (x1, y1) and (x2, y2) are point coordinates.",
                    "symbols": [
                        {
                            "symbol": "d",
                            "name": "Euclidean Distance",
                            "domain": "[0, \\infty)",
                            "geometric_or_algebraic_role": "Length of segment PQ"
                        },
                        {
                            "symbol": "x_1, x_2, y_1, y_2",
                            "name": "Cartesian Coordinates",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Point coordinates"
                        }
                    ],
                    "reference_frame_or_sign": "Cartesian 2D coordinate plane with orthogonal axes",
                    "conditions_of_validity": "Valid for any two points in R^2.",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-SECTION-FORMULA",
                    "formula": "x = \\frac{m x_2 + n x_1}{m + n}, \\quad y = \\frac{m y_2 + n y_1}{m + n}",
                    "meaning_of_symbols": "m:n is internal division ratio; m+n != 0.",
                    "symbols": [
                        {
                            "symbol": "m, n",
                            "name": "Section Ratio Weights",
                            "domain": "\\mathbb{R}^+",
                            "geometric_or_algebraic_role": "Internal partition weights"
                        }
                    ],
                    "reference_frame_or_sign": "m > 0, n > 0 for internal division",
                    "conditions_of_validity": "m + n != 0",
                    "obligations": ["DERIVE", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-COORDINATE-GRID-DISTANCE",
                    "representation_type": "CARTESIAN_COORDINATE_PLOT",
                    "name": "Right-Triangle Projection for Distance Formula",
                    "math_encoded": "Cartesian plane showing P(x1, y1), Q(x2, y2) and projection point R(x2, y1) forming right triangle with legs |x2 - x1| and |y2 - y1|.",
                    "mandatory_labels": ["x-axis", "y-axis", "Point P(x1, y1)", "Point Q(x2, y2)", "Delta x", "Delta y", "Hypotenuse d"],
                    "what_cannot_be_omitted": "Right-angle marker at projection point R connecting Pythagorean theorem to distance metric.",
                    "common_incorrect_version": "Connecting points with arbitrary curve without showing coordinate projections.",
                    "verification_method": "Pythagorean check: Delta x^2 + Delta y^2 = d^2."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Vertical lines have undefined slope; slope formula requires x1 != x2.",
                    "why_needed": "Division by zero occurs if x1 = x2.",
                    "what_changes_if_violated": "Algorithm crashes or incorrectly produces slope zero."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Plot coordinate pairs on Cartesian plane and identify coordinate differences delta x and delta y.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Apply distance or section formula, strictly verifying ratio weights match endpoint order.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Check collinearity via area of triangle = 0 or distance equality d(A,B) + d(B,C) = d(A,C).",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Right-triangle Pythagorean geometric diagram",
                    "to_mode": "Algebraic coordinate distance metric formula",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Derive distance formula from Cartesian right-triangle projections."
                },
                {
                    "from_mode": "Algebraic collinearity slope equality",
                    "to_mode": "Geometric line coincidence validation",
                    "target_core_role": "CORE2B_GENERATIVE_TRANSFER",
                    "description": "Prove three points are collinear using slope equality or distance additivity."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-VERTICAL-SLOPE-ZERO",
                    "incorrect_belief": "Confusing undefined slope of a vertical line (x1 = x2) with zero slope of a horizontal line (y1 = y2).",
                    "why_plausible": "Both lines are parallel to an axis, leading to sloppy conflation of 0 and undefined.",
                    "required_counterexample": "Take P(3, 2) and Q(3, 8). Delta x = 0, Delta y = 6. m = 6/0 is undefined. Contrast with P(2, 3) and Q(8, 3) where m = 0/6 = 0.",
                    "required_technical_repair": "Strictly classify horizontal (Delta y = 0 -> m = 0) vs vertical (Delta x = 0 -> m undefined)."
                }
            ],
            "mandatory_verifications": [
                "Verify distance metric symmetry: d(P, Q) == d(Q, P).",
                "Check midpoint formula by confirming it is equidistant from both endpoints."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-DISTANCE-CALCULATION",
                    "name": "Distance Formula & Geometric Figure Classification",
                    "recognition_cues": "Given vertices in R^2, determine figure type (equilateral, isosceles, right triangle, parallelogram, rhombus).",
                    "first_technical_move": "Compute all side lengths and diagonal lengths using distance formula.",
                    "common_fatal_error": "Checking only side lengths and confusing a rhombus with a square (omitting diagonal check).",
                    "typical_unknown": "Classification of geometric figure or missing vertex coordinate"
                },
                {
                    "family_id": "PF-MATH-COLLINEARITY-VERIFICATION",
                    "name": "Testing and Establishing Collinearity",
                    "recognition_cues": "Three points given; determine if they lie on a single line.",
                    "first_technical_move": "Check if d(A,B) + d(B,C) = d(A,C) or evaluate area of triangle formula to 0.",
                    "common_fatal_error": "Assuming order of points without checking which pair gives maximum distance.",
                    "typical_unknown": "Boolean collinearity status or unknown coordinate parameter"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 1,
                "element_interactivity": 2,
                "inferential_jump_severity": 1,
                "representation_translation": 2,
                "model_discrimination": 2,
                "sign_or_frame_sensitivity": 3,
                "multi_step_dependency": 2,
                "abstraction": 1,
                "misconception_density": 2,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Cartesian distance metric, section ratios, and coordinate figure proofs.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["COORDINATE_FOUNDATION", "METRIC_RIGOR"],
                "conditional_badges": ["SECTION_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-GEO-01",
                    "authoring_defect": "Treating vertical line slope as 0 instead of undefined.",
                    "expected_failure_reason": "Violates division by zero avoidance and coordinate geometric truth."
                }
            ]
        },

        # 6. MATH-GEO-TRIANGLES
        {
            "subtopic_id": "MATH-GEO-TRIANGLES",
            "learner_title": "Euclidean Triangles: Congruence & Similarity Criteria",
            "chapter": "Geometry",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class IX Chapter 7 (Triangles) & Class X Chapter 6 (Triangles)",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-CONGRUENCE-CRITERIA",
                "CON-MATH-THALES-THEOREM",
                "CON-MATH-SIMILARITY-CRITERIA"
            ],
            "prerequisite_ids": ["MATH-GEO-COORDINATES"],
            "linked_buckets": ["BUCKET-MATH-TRIANGLES"],
            "linked_problem_family_ids": [
                "PF-MATH-CONGRUENCE-PROOF",
                "PF-MATH-SIMILAR-TRIANGLE-PROPORTION"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-CONGRUENCE-CRITERIA",
                    "canonical_statement": "Two triangles are congruent if and only if they satisfy one of the axiomatic criteria: SSS, SAS (included angle), ASA, AAS, or RHS (right angle, hypotenuse, side). SSA and AAA are strictly invalid congruence criteria.",
                    "why_required": "Axiomatic basis of Euclidean deductive geometry.",
                    "failure_if_omitted": "Learner uses invalid SSA ambiguous configuration, producing false proofs."
                },
                {
                    "concept_id": "CON-MATH-THALES-THEOREM",
                    "canonical_statement": "Basic Proportionality Theorem (Thales): If a line is drawn parallel to one side of a triangle intersecting the other two sides, it divides the two sides in the same ratio: AD/DB = AE/EC.",
                    "why_required": "Bridge between Euclidean parallelism and geometric ratio similarity.",
                    "failure_if_omitted": "Learner cannot derive similarity properties or solve transversal segment lengths."
                },
                {
                    "concept_id": "CON-MATH-SIMILARITY-CRITERIA",
                    "canonical_statement": "Two triangles are similar if corresponding angles are equal and corresponding sides are proportional (criteria: AA, SAS, SSS). The ratio of areas of two similar triangles equals the square of the ratio of corresponding sides: Area1/Area2 = (s1/s2)^2.",
                    "why_required": "Governs linear scaling versus quadratic area scaling.",
                    "failure_if_omitted": "Learner scales areas linearly with side ratio rather than quadratically."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-THALES-RATIO",
                    "formula": "\\frac{AD}{DB} = \\frac{AE}{EC}",
                    "meaning_of_symbols": "Line DE parallel to base BC cuts AB at D and AC at E.",
                    "symbols": [
                        {
                            "symbol": "AD, DB, AE, EC",
                            "name": "Segment Lengths",
                            "domain": "\\mathbb{R}^+",
                            "geometric_or_algebraic_role": "Segment lengths on triangle sides"
                        }
                    ],
                    "reference_frame_or_sign": "Lengths strictly positive",
                    "conditions_of_validity": "DE must be parallel to BC in triangle ABC.",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-AREA-SIMILARITY-RATIO",
                    "formula": "\\frac{\\text{Area}(\\triangle ABC)}{\\text{Area}(\\triangle PQR)} = \\left(\\frac{AB}{PQ}\\right)^2",
                    "meaning_of_symbols": "Area ratio of similar triangles equals square of side scale factor.",
                    "symbols": [
                        {
                            "symbol": "AB/PQ",
                            "name": "Linear Scale Factor",
                            "domain": "\\mathbb{R}^+",
                            "geometric_or_algebraic_role": "Similarity ratio k"
                        }
                    ],
                    "reference_frame_or_sign": "Valid when triangle ABC is similar to triangle PQR",
                    "conditions_of_validity": "Triangles must be similar.",
                    "obligations": ["DERIVE", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-GEOMETRIC-TWO-COLUMN-PROOF",
                    "representation_type": "GEOMETRIC_TWO_COLUMN_PROOF",
                    "name": "Formal Two-Column Deductive Proof Structure",
                    "math_encoded": "Tabular structure with numbered Statements on left and formal geometric Reasons/Theorems on right, terminating with Q.E.D.",
                    "mandatory_labels": ["Step Number", "Mathematical Statement", "Geometric Axiom/Reason", "Conclusion"],
                    "what_cannot_be_omitted": "Explicit citation of congruence/similarity criteria and given premises.",
                    "common_incorrect_version": "Narrative essay without explicit theorem citations or skipped intermediate logical deductions.",
                    "verification_method": "Chain integrity: every statement must follow validly from prior proven lines or axioms."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Angle in SAS must be the included angle between the two specified sides.",
                    "why_needed": "Non-included angle (SSA) allows two distinct triangles with same side lengths (ambiguous case).",
                    "what_changes_if_violated": "Congruence proof fails due to ambiguity."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "State Given premises and To Prove target with clearly labelled geometric diagram.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Identify equal corresponding elements (sides, angles) citing geometric theorems.",
                    "inferential_jump": "MEDIUM"
                },
                {
                    "step": 3,
                    "expert_action": "Apply exact congruence (SAS, SSS, ASA, AAS, RHS) or similarity criterion (AA, SAS, SSS).",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Visual geometric diagram with marked parallel lines",
                    "to_mode": "Proportional side ratio equation via Thales theorem",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Translate visual line configurations into rigorous ratio equations."
                },
                {
                    "from_mode": "Linear similarity side ratio k",
                    "to_mode": "Quadratic area ratio k^2",
                    "target_core_role": "CORE2B_GENERATIVE_TRANSFER",
                    "description": "Scale 2D areas using square of linear similarity ratio."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-SSA-CONGRUENCE-FALLACY",
                    "incorrect_belief": "Assuming SSA (two sides and a non-included angle) is a valid congruence criterion.",
                    "why_plausible": "Three components match, giving false intuition of uniqueness.",
                    "required_counterexample": "In triangle ABC, let AB = 5, BC = 4, angle A = 30 deg. An arc of radius 4 from B intersects base AC at two distinct points, creating one acute and one obtuse triangle with identical SSA data.",
                    "required_technical_repair": "Strictly forbid SSA unless angle is 90 deg (which constitutes RHS)."
                }
            ],
            "mandatory_verifications": [
                "Verify correspondence of vertices in triangle similarity/congruence notation (order matters).",
                "Verify area ratio equals square of side ratio, not linear ratio."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-CONGRUENCE-PROOF",
                    "name": "Euclidean Deductive Proof of Congruence",
                    "recognition_cues": "Geometric figures with marked angles and sides requiring proof of part equality.",
                    "first_technical_move": "Pair triangles and list three matching elements with geometric justifications.",
                    "common_fatal_error": "Using non-included angle for SAS or assuming parallel implies equal length.",
                    "typical_unknown": "Rigorous proof of congruence and CPCTC consequence"
                },
                {
                    "family_id": "PF-MATH-SIMILAR-TRIANGLE-PROPORTION",
                    "name": "Similar Triangle Ratios and Area Calculations",
                    "recognition_cues": "Triangles with parallel transversals or shared angles requiring side or area calculation.",
                    "first_technical_move": "Prove similarity via AA criterion, then write corresponding side proportionality equations.",
                    "common_fatal_error": "Writing side ratios with mismatched vertices or failing to square ratio for areas.",
                    "typical_unknown": "Unknown segment length or area"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 2,
                "element_interactivity": 3,
                "inferential_jump_severity": 2,
                "representation_translation": 3,
                "model_discrimination": 3,
                "sign_or_frame_sensitivity": 1,
                "multi_step_dependency": 3,
                "abstraction": 3,
                "misconception_density": 3,
                "synthesis": 3,
                "provisional_difficulty": "HARD",
                "difficulty_basis": "Deductive Euclidean proof chains, non-included angle traps, and quadratic area scaling.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["EUCLIDEAN_RIGOR", "THALES_GATE"],
                "conditional_badges": ["PROOF_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-TRI-01",
                    "authoring_defect": "Accepting SSA as a general triangle congruence criterion.",
                    "expected_failure_reason": "Violates uniqueness of triangle construction (ambiguous case)."
                }
            ]
        },

        # 7. MATH-TRIG-RATIOS
        {
            "subtopic_id": "MATH-TRIG-RATIOS",
            "learner_title": "Trigonometric Ratios & Fundamental Pythagorean Identities",
            "chapter": "Trigonometry",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class X Mathematics, Chapter 8: Introduction to Trigonometry",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-TRIG-RIGHT-TRIANGLE-RATIOS",
                "CON-MATH-TRIG-ACUTE-DOMAIN",
                "CON-MATH-PYTHAGOREAN-IDENTITIES"
            ],
            "prerequisite_ids": ["MATH-GEO-TRIANGLES"],
            "linked_buckets": ["BUCKET-MATH-TRIGONOMETRY"],
            "linked_problem_family_ids": [
                "PF-MATH-TRIG-EVALUATION",
                "PF-MATH-IDENTITY-PROOF"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-TRIG-RIGHT-TRIANGLE-RATIOS",
                    "canonical_statement": "In a right-angled triangle with acute reference angle theta, sin theta = opposite/hypotenuse, cos theta = adjacent/hypotenuse, tan theta = opposite/adjacent, with reciprocal relations csc theta = 1/sin theta, sec theta = 1/cos theta, cot theta = 1/tan theta.",
                    "why_required": "Foundational trigonometric definition linking angles to geometric lengths.",
                    "failure_if_omitted": "Learner mixes reference angle opposite and adjacent sides."
                },
                {
                    "concept_id": "CON-MATH-TRIG-ACUTE-DOMAIN",
                    "canonical_statement": "For acute angles theta in (0, 90 deg), all six trigonometric ratios are strictly positive, with 0 < sin theta < 1 and 0 < cos theta < 1, while tan theta takes all positive real values.",
                    "why_required": "Establishes physical bounds of ratio values in introductory geometry.",
                    "failure_if_omitted": "Learner calculates sin theta > 1 without recognizing physical impossibility in right triangle."
                },
                {
                    "concept_id": "CON-MATH-PYTHAGOREAN-IDENTITIES",
                    "canonical_statement": "Directly from the Pythagorean theorem a^2 + b^2 = c^2, three fundamental identities hold: sin^2 theta + cos^2 theta = 1, 1 + tan^2 theta = sec^2 theta, 1 + cot^2 theta = csc^2 theta.",
                    "why_required": "Provides invariant transformations among trigonometric expressions.",
                    "failure_if_omitted": "Learner treats trigonometric functions as unrelated algebraic variables."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-PYTHAGOREAN-TRIG-IDENTITY",
                    "formula": "\\sin^2\\theta + \\cos^2\\theta = 1",
                    "meaning_of_symbols": "theta is the acute angle; sin^2 theta denotes (sin theta)^2.",
                    "symbols": [
                        {
                            "symbol": "\\theta",
                            "name": "Acute Angle",
                            "domain": "(0, \\frac{\\pi}{2})",
                            "geometric_or_algebraic_role": "Reference angle"
                        },
                        {
                            "symbol": "\\sin\\theta",
                            "name": "Sine Ratio",
                            "domain": "(0, 1)",
                            "geometric_or_algebraic_role": "Opposite to hypotenuse ratio"
                        },
                        {
                            "symbol": "\\cos\\theta",
                            "name": "Cosine Ratio",
                            "domain": "(0, 1)",
                            "geometric_or_algebraic_role": "Adjacent to hypotenuse ratio"
                        }
                    ],
                    "reference_frame_or_sign": "All acute ratios positive",
                    "conditions_of_validity": "Valid for all angles in R (extended), acute domain (0, pi/2).",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-SEC-TAN-IDENTITY",
                    "formula": "1 + \\tan^2\\theta = \\sec^2\\theta",
                    "meaning_of_symbols": "Relation between secant and tangent ratios.",
                    "symbols": [
                        {
                            "symbol": "\\tan\\theta",
                            "name": "Tangent Ratio",
                            "domain": "(0, \\infty)",
                            "geometric_or_algebraic_role": "Opposite to adjacent ratio"
                        },
                        {
                            "symbol": "\\sec\\theta",
                            "name": "Secant Ratio",
                            "domain": "(1, \\infty)",
                            "geometric_or_algebraic_role": "Hypotenuse to adjacent ratio"
                        }
                    ],
                    "reference_frame_or_sign": "Defined for theta != 90 deg",
                    "conditions_of_validity": "cos theta != 0",
                    "obligations": ["DERIVE", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-RIGHT-TRIANGLE-RATIO-SCHEMATIC",
                    "representation_type": "RIGHT_TRIANGLE_RATIO_DIAGRAM",
                    "name": "Right Triangle Ratio Reference Schematic",
                    "math_encoded": "Right-angled triangle ABC with right angle at B and reference angle theta at A, explicitly labelling Opposite side BC, Adjacent side AB, and Hypotenuse AC.",
                    "mandatory_labels": ["Reference Angle \\theta", "Right Angle (90 deg)", "Opposite", "Adjacent", "Hypotenuse"],
                    "what_cannot_be_omitted": "Clear identification of Opposite and Adjacent relative to chosen reference angle theta.",
                    "common_incorrect_version": "Labelling vertical side as Opposite even when reference angle is at top vertex.",
                    "verification_method": "Check Opposite^2 + Adjacent^2 = Hypotenuse^2."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Reference angle theta must be strictly between 0 and 90 degrees in right-triangle context.",
                    "why_needed": "At 0 deg or 90 deg, right triangle degenerates into segment.",
                    "what_changes_if_violated": "Ratios like tan(90 deg) or sec(90 deg) suffer division by zero."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Identify right angle and reference angle theta; label Opposite, Adjacent, and Hypotenuse.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Compute missing side using Pythagorean theorem.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Evaluate required ratios or apply Pythagorean identity substitutions to prove equality.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Given single ratio e.g. sin theta = 3/5",
                    "to_mode": "Complete set of remaining five trigonometric ratios",
                    "target_core_role": "CORE1B_GENERATIVE_RECONSTRUCTION",
                    "description": "Construct reference triangle from single ratio and evaluate all trigonometric ratios."
                },
                {
                    "from_mode": "Complex trigonometric identity LHS",
                    "to_mode": "Simplified identical RHS",
                    "target_core_role": "CORE2A_DECLARATIVE_WORKED_PROBLEM",
                    "description": "Transform identity by expressing in terms of sin and cos or applying Pythagorean identities."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-TRIG-MULTIPLICATION",
                    "incorrect_belief": "Believing sin theta represents multiplication of 'sin' and 'theta', leading to invalid cancellations like sin theta / theta = sin.",
                    "why_plausible": "Juxtaposition in standard notation resembles algebraic product xy.",
                    "required_counterexample": "sin is a function, not a scalar. sin(30 deg) = 1/2. Dividing by 30 deg gives (1/2)/(30 deg), not 'sin'.",
                    "required_technical_repair": "Explicitly treat trigonometric names as functional operators acting on angular inputs."
                }
            ],
            "mandatory_verifications": [
                "Verify sin^2 theta + cos^2 theta == 1 on all computed numerical ratios.",
                "Ensure sin theta <= 1 and cos theta <= 1 for all acute angles."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-TRIG-EVALUATION",
                    "name": "Evaluation of Trigonometric Expressions from Given Ratio",
                    "recognition_cues": "Given one ratio e.g. tan A = 4/3, evaluate algebraic combination of sin A and cos A.",
                    "first_technical_move": "Construct right triangle with sides 4k, 3k and find hypotenuse 5k via Pythagoras.",
                    "common_fatal_error": "Mislabelling adjacent and opposite sides when angle changes from A to C.",
                    "typical_unknown": "Numerical value of trigonometric expression"
                },
                {
                    "family_id": "PF-MATH-IDENTITY-PROOF",
                    "name": "Proving Trigonometric Identities",
                    "recognition_cues": "Equations containing mixed sec, tan, csc, cot, sin, cos requiring verification of equality.",
                    "first_technical_move": "Convert all terms to sin and cos, or utilize sec^2 - tan^2 = 1 directly.",
                    "common_fatal_error": "Treating (sin A + cos A)^2 as sin^2 A + cos^2 A (Freshman's dream in trig).",
                    "typical_unknown": "Deductive equivalence proof"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 2,
                "element_interactivity": 2,
                "inferential_jump_severity": 2,
                "representation_translation": 2,
                "model_discrimination": 2,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 2,
                "abstraction": 2,
                "misconception_density": 2,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Trigonometric operator semantics, reference angle orientation, and identity algebraic proofs.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["TRIG_FOUNDATION", "PYTHAGOREAN_IDENTITIES"],
                "conditional_badges": ["IDENTITY_PROOF_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-TRIG-01",
                    "authoring_defect": "Treating sin theta as multiplication sin * theta allowing cancellation.",
                    "expected_failure_reason": "Violates functional operator semantics of trigonometric ratios."
                }
            ]
        },

        # 8. MATH-GEO-CIRCLES
        {
            "subtopic_id": "MATH-GEO-CIRCLES",
            "learner_title": "Circle Theorems, Tangent Properties & Cyclic Quadrilaterals",
            "chapter": "Geometry",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class IX Chapter 10 (Circles) & Class X Chapter 10 (Circles)",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-TANGENT-RADIUS-PERPENDICULAR",
                "CON-MATH-EQUAL-TANGENTS-EXTERNAL",
                "CON-MATH-CYCLIC-QUAD-SUPPLEMENTARY"
            ],
            "prerequisite_ids": ["MATH-GEO-TRIANGLES"],
            "linked_buckets": ["BUCKET-MATH-CIRCLES"],
            "linked_problem_family_ids": [
                "PF-MATH-TANGENT-LENGTH-CALC",
                "PF-MATH-CYCLIC-ANGLE-CHASING"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-TANGENT-RADIUS-PERPENDICULAR",
                    "canonical_statement": "The tangent at any point of a circle is perpendicular to the radius through the point of contact: if line t is tangent to circle C(O, r) at P, then OP is perpendicular to t.",
                    "why_required": "Establishes fundamental 90-degree angle for all tangent problem deductions.",
                    "failure_if_omitted": "Learner cannot construct right triangles involving circle tangents."
                },
                {
                    "concept_id": "CON-MATH-EQUAL-TANGENTS-EXTERNAL",
                    "canonical_statement": "The lengths of the two tangents drawn from an external point to a circle are equal: if PA and PB are tangents from external point P to points of contact A and B, then PA = PB.",
                    "why_required": "Enables algebraic perimeter and segment chasing around inscribed circles.",
                    "failure_if_omitted": "Learner cannot solve circumscribed polygon segment equations."
                },
                {
                    "concept_id": "CON-MATH-CYCLIC-QUAD-SUPPLEMENTARY",
                    "canonical_statement": "The opposite angles of a cyclic quadrilateral inscribed in a circle sum to 180 degrees: angle A + angle C = 180 deg and angle B + angle D = 180 deg.",
                    "why_required": "Governs angle-chasing in inscribed four-sided figures.",
                    "failure_if_omitted": "Learner confuses cyclic quadrilateral angle relations with general quadrilaterals."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-TANGENT-RADIUS-ANGLE",
                    "formula": "\\angle OPT = 90^\\circ",
                    "meaning_of_symbols": "O is circle center, P is point of contact, T is any other point on tangent line.",
                    "symbols": [
                        {
                            "symbol": "\\angle OPT",
                            "name": "Tangent-Radius Angle",
                            "domain": "\\{90^\\circ\\}",
                            "geometric_or_algebraic_role": "Perpendicular contact angle"
                        }
                    ],
                    "reference_frame_or_sign": "Right angle at point of tangency",
                    "conditions_of_validity": "P must be the exact point of contact.",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-CYCLIC-QUAD-SUPPLEMENTARY",
                    "formula": "\\angle A + \\angle C = 180^\\circ",
                    "meaning_of_symbols": "A and C are opposite interior angles of cyclic quadrilateral ABCD.",
                    "symbols": [
                        {
                            "symbol": "\\angle A, \\angle C",
                            "name": "Opposite Inscribed Angles",
                            "domain": "(0^\\circ, 180^\\circ)",
                            "geometric_or_algebraic_role": "Supplementary angle pair"
                        }
                    ],
                    "reference_frame_or_sign": "Vertices A, B, C, D must lie on a single circle",
                    "conditions_of_validity": "Quadrilateral must be concyclic.",
                    "obligations": ["DERIVE", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-CIRCLE-TANGENT-CONSTRUCTION",
                    "representation_type": "CIRCLE_TANGENT_CONSTRUCTION",
                    "name": "Circle Tangents from External Point Schematic",
                    "math_encoded": "Circle with center O, external point P, tangents PA and PB touching at A and B, showing radii OA and OB perpendicular to PA and PB respectively, and line OP bisecting angle APB.",
                    "mandatory_labels": ["Center O", "External Point P", "Contact Point A", "Contact Point B", "Radius r", "Right Angle Markers"],
                    "what_cannot_be_omitted": "Right angle markers at contact points A and B.",
                    "common_incorrect_version": "Drawing tangents without showing radii or perpendicularity at contact points.",
                    "verification_method": "RHS congruence between triangle OPA and triangle OPB."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Point of tangency P must be the single unique point of intersection between line and circle.",
                    "why_needed": "If line intersects in two points, it is a secant and radius is not perpendicular.",
                    "what_changes_if_violated": "Angle with radius deviates from 90 degrees."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Draw radii to all points of tangency and mark 90-degree right angles.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Identify equal tangent segments from external points (PA = PB).",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Apply cyclic quadrilateral supplementary angles or Pythagoras in right triangle OPA.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Circle with external tangent segments",
                    "to_mode": "Right-angled triangle solvable via Pythagoras OP^2 = OA^2 + PA^2",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Convert tangent-radius perpendicularity into solvable right triangle."
                },
                {
                    "from_mode": "Circumscribed quadrilateral around circle",
                    "to_mode": "Opposite side sum equality AB + CD = AD + BC",
                    "target_core_role": "CORE2B_GENERATIVE_TRANSFER",
                    "description": "Prove opposite sides of circumscribed quadrilateral sum to equal values using equal tangents."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-SECANT-PERPENDICULAR",
                    "incorrect_belief": "Assuming a line passing through a circle is perpendicular to the radius at any arbitrary intersection point.",
                    "why_plausible": "Over-generalizing tangent perpendicularity to general secant lines.",
                    "required_counterexample": "Draw secant cutting circle at A and B. The radius to A forms acute angle with chord AB, never 90 deg unless secant becomes tangent (A=B).",
                    "required_technical_repair": "Restrict perpendicularity strictly to the unique point of contact of a tangent line."
                }
            ],
            "mandatory_verifications": [
                "Verify OP^2 == r^2 + PA^2 for any tangent from external point P.",
                "Verify opposite angles of cyclic quadrilateral sum to 180 degrees."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-TANGENT-LENGTH-CALC",
                    "name": "Length of Tangent and Distance to Center",
                    "recognition_cues": "Radius r given, distance from center d given, find length of tangent t.",
                    "first_technical_move": "Form right triangle OPA with hypotenuse OP = d and legs r and t; apply t = sqrt(d^2 - r^2).",
                    "common_fatal_error": "Treating tangent t as hypotenuse instead of leg.",
                    "typical_unknown": "Tangent length t or radius r"
                },
                {
                    "family_id": "PF-MATH-CYCLIC-ANGLE-CHASING",
                    "name": "Angle Chasing in Cyclic Quadrilaterals and Tangent-Chords",
                    "recognition_cues": "Circle with inscribed quadrilateral or tangent-chord angle requiring unknown angle.",
                    "first_technical_move": "Use angle subtended at center is twice angle at circumference, or supplementary opposite angles.",
                    "common_fatal_error": "Assuming opposite angles of non-cyclic quadrilateral are supplementary.",
                    "typical_unknown": "Unknown angle measure"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 2,
                "element_interactivity": 2,
                "inferential_jump_severity": 2,
                "representation_translation": 2,
                "model_discrimination": 2,
                "sign_or_frame_sensitivity": 1,
                "multi_step_dependency": 2,
                "abstraction": 2,
                "misconception_density": 2,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Tangent-radius perpendicularity, cyclic quad supplementary angles, and inscribed circle proofs.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["CIRCLE_THEOREMS", "TANGENT_PERPENDICULARITY"],
                "conditional_badges": ["CYCLIC_QUAD_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-CIR-01",
                    "authoring_defect": "Treating secants as perpendicular to radius.",
                    "expected_failure_reason": "Violates tangent-radius unique perpendicularity theorem."
                }
            ]
        },

        # 9. MATH-MENS-SURFACES
        {
            "subtopic_id": "MATH-MENS-SURFACES",
            "learner_title": "Mensuration: Surface Areas, Volumes & Composite Solids",
            "chapter": "Mensuration",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class IX Chapter 13 & Class X Chapter 13: Surface Areas and Volumes",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-SOLID-VOLUME-ADDITIVITY",
                "CON-MATH-COMPOSITE-INTERFACE-EXCLUSION",
                "CON-MATH-VOLUME-CONSERVATION-RECAST"
            ],
            "prerequisite_ids": ["MATH-NUM-RADICALS", "MATH-ALG-POLYNOMIALS"],
            "linked_buckets": ["BUCKET-MATH-MENSURATION"],
            "linked_problem_family_ids": [
                "PF-MATH-COMPOSITE-SURFACE-AREA",
                "PF-MATH-MELTING-RECASTING-VOLUME"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-SOLID-VOLUME-ADDITIVITY",
                    "canonical_statement": "The volume of a composite solid formed by combining non-overlapping component solids is strictly additive: V_total = sum(V_i).",
                    "why_required": "Volume measures 3D space content and is invariant under boundary joining.",
                    "failure_if_omitted": "Learner invents volume adjustments for joined faces."
                },
                {
                    "concept_id": "CON-MATH-COMPOSITE-INTERFACE-EXCLUSION",
                    "canonical_statement": "The surface area of a composite solid is the measure of its exposed outer boundary only. The shared interface surface between joined solids is internal and must be excluded: SA_total = SA_1 + SA_2 - 2 A_interface.",
                    "why_required": "Prevents catastrophic over-counting of internal contact surfaces in composite objects.",
                    "failure_if_omitted": "Learner simply sums total surface areas of component solids, counting internal faces."
                },
                {
                    "concept_id": "CON-MATH-VOLUME-CONSERVATION-RECAST",
                    "canonical_statement": "When a solid is melted, remolded, or recasted into a different geometric shape without loss of material, its total volume remains invariant: V_initial = V_final.",
                    "why_required": "Fundamental physical conservation law governing melting/recasting problems.",
                    "failure_if_omitted": "Learner equates surface areas instead of volumes during recasting."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-COMPOSITE-SURFACE-AREA",
                    "formula": "SA_{\\text{total}} = SA_1 + SA_2 - 2 A_{\\text{interface}}",
                    "meaning_of_symbols": "SA_total is exposed surface area; A_interface is area of shared contact face.",
                    "symbols": [
                        {
                            "symbol": "SA_{\\text{total}}",
                            "name": "Composite Surface Area",
                            "domain": "\\mathbb{R}^+",
                            "geometric_or_algebraic_role": "Exposed boundary area"
                        },
                        {
                            "symbol": "A_{\\text{interface}}",
                            "name": "Shared Interface Area",
                            "domain": "\\mathbb{R}^+",
                            "geometric_or_algebraic_role": "Hidden internal contact face"
                        }
                    ],
                    "reference_frame_or_sign": "Subtracted twice because it was counted in both SA_1 and SA_2",
                    "conditions_of_validity": "Valid for solids joined flush along a planar interface.",
                    "obligations": ["EXPLAIN", "DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-VOLUME-CONSERVATION",
                    "formula": "V_{\\text{initial}} = V_{\\text{final}}",
                    "meaning_of_symbols": "Volume remains invariant under melting, remolding, or phase-conserving transformation.",
                    "symbols": [
                        {
                            "symbol": "V",
                            "name": "Volume",
                            "domain": "\\mathbb{R}^+",
                            "geometric_or_algebraic_role": "3D space measure"
                        }
                    ],
                    "reference_frame_or_sign": "Closed system with no material loss",
                    "conditions_of_validity": "No mass/volume lost in recasting process.",
                    "obligations": ["INTERPRET", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-MENSURATION-COMPOSITE-NET",
                    "representation_type": "MENSURATION_NET_OR_COMPOSITE_SCHEMATIC",
                    "name": "Composite Solid Exploded Schematic with Interface Highlight",
                    "math_encoded": "Schematic diagram showing cylinder with hemispherical cap, highlighting the circular interface face with dotted lines and labelling exposed Curved Surface Areas versus internal circular face.",
                    "mandatory_labels": ["Cylinder CSA", "Hemisphere CSA", "Common Interface Face (Excluded)", "Radius r", "Height h"],
                    "what_cannot_be_omitted": "Dotted representation of hidden internal interface face with explicit 'EXCLUDED FROM SA' label.",
                    "common_incorrect_version": "Showing hemisphere and cylinder as separate solids with both circular bases added to total area.",
                    "verification_method": "Dimensional check: Area has units L^2, Volume has units L^3."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Joined solids must meet along identical congruent boundary interfaces.",
                    "why_needed": "If one face is larger than the other, partially exposed interface must be included in surface area.",
                    "what_changes_if_violated": "Interface formula requires differential area correction."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Deconstruct composite solid into canonical geometric primitives (cone, cylinder, sphere, hemisphere, cube).",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Identify which faces are exposed to the exterior and which faces are joined internally.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Sum curved surface areas of exposed parts, or equate total volume to find recasting dimension.",
                    "inferential_jump": "MEDIUM"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Physical composite solid object description",
                    "to_mode": "Sum of exposed surface area components equation",
                    "target_core_role": "CORE1A_DECLARATIVE_CONCEPT_CONSTRUCTION",
                    "description": "Formulate surface area by selecting curved surfaces and excluding joined circular bases."
                },
                {
                    "from_mode": "Initial metallic solid dimensions",
                    "to_mode": "Final recasted geometric shape unknown dimension",
                    "target_core_role": "CORE2A_DECLARATIVE_WORKED_PROBLEM",
                    "description": "Equate V_initial = V_final to solve for unknown radius, height, or number of small spheres."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-ADDITIVE-SURFACE-AREA",
                    "incorrect_belief": "Believing that total surface area of a composite solid equals the sum of the total surface areas of the individual parts.",
                    "why_plausible": "Intuition from volume (which is additive) improperly transferred to surface area.",
                    "required_counterexample": "Join two unit cubes of surface area 6 each. Total combined prism has dimensions 2x1x1 and surface area 2(2*1 + 2*1 + 1*1) = 10, not 6 + 6 = 12. The difference 2 is the two internal faces.",
                    "required_technical_repair": "Mandate exclusion of all interior contact boundaries when calculating surface area."
                }
            ],
            "mandatory_verifications": [
                "Verify dimensional consistency: all surface areas in units^2, all volumes in units^3.",
                "Verify volume conservation in recasting problems."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-COMPOSITE-SURFACE-AREA",
                    "name": "Surface Area of Combined Solids (Toy, Tent, Capsule)",
                    "recognition_cues": "Solids formed by mounting cone/hemisphere on cylinder or scooping out hemispheres.",
                    "first_technical_move": "List all exposed faces: e.g. Capsule = CSA of cylinder + 2 * CSA of hemisphere.",
                    "common_fatal_error": "Adding the area of the circular base of the cylinder/cone that is inside the toy.",
                    "typical_unknown": "Total exposed surface area"
                },
                {
                    "family_id": "PF-MATH-MELTING-RECASTING-VOLUME",
                    "name": "Melting, Recasting and Liquid Transfer",
                    "recognition_cues": "Metallic sphere melted into cylinder, or cylindrical bucket emptied into conical heap.",
                    "first_technical_move": "Equate V_1 = V_2 or n * V_sphere = V_cylinder and solve for unknown dimension.",
                    "common_fatal_error": "Equating surface areas instead of volumes.",
                    "typical_unknown": "Radius, height, or integer count n of recasted solids"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 1,
                "element_interactivity": 2,
                "inferential_jump_severity": 2,
                "representation_translation": 2,
                "model_discrimination": 2,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 2,
                "abstraction": 2,
                "misconception_density": 3,
                "synthesis": 2,
                "provisional_difficulty": "MEDIUM",
                "difficulty_basis": "Boundary surface exclusion versus volume additivity and melting conservation.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["MENSURATION_RIGOR", "SURFACE_INTERFACE_EXCLUSION"],
                "conditional_badges": ["RECASTING_CONSERVATION"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-MENS-01",
                    "authoring_defect": "Adding total surface areas of component solids without subtracting shared interface.",
                    "expected_failure_reason": "Violates boundary surface area definition by including interior hidden faces."
                }
            ]
        },

        # 10. MATH-STAT-PROBABILITY
        {
            "subtopic_id": "MATH-STAT-PROBABILITY",
            "learner_title": "Statistics & Classical Probability Foundations",
            "chapter": "Statistics & Probability",
            "authority_tier": "SOURCE-DEFINED",
            "maturity": "ENGINEERING",
            "technical_readiness": "ENGINEERING_GATE_READY",
            "provenance": {
                "authority_class": "SOURCE-DEFINED",
                "source_curriculum": "CBSE / NCERT / National Curriculum Framework",
                "source_scope": "IN_SCOPE",
                "source_reference": "Class IX & X: Statistics (Ch 14) and Probability (Ch 15)",
                "claim_status": "VERIFIED_CANONICAL"
            },
            "canonical_concept_ids": [
                "CON-MATH-CENTRAL-TENDENCY-MEASURES",
                "CON-MATH-PROBABILITY-BOUNDS",
                "CON-MATH-COMPLEMENTARY-EVENTS"
            ],
            "prerequisite_ids": ["MATH-NUM-RADICALS"],
            "linked_buckets": ["BUCKET-MATH-STATISTICS", "BUCKET-MATH-PROBABILITY"],
            "linked_problem_family_ids": [
                "PF-MATH-CENTRAL-TENDENCY-CALC",
                "PF-MATH-CLASSICAL-PROBABILITY"
            ],
            "technical_core": [
                {
                    "concept_id": "CON-MATH-CENTRAL-TENDENCY-MEASURES",
                    "canonical_statement": "Central tendency is measured by Mean x_bar = sum(f_i x_i)/sum(f_i), Median (50th percentile rank), and Mode (value of maximum frequency). For moderately skewed distributions, empirical relation holds: 3 Median approx Mode + 2 Mean.",
                    "why_required": "Provides statistical summary metrics and empirical cross-verification.",
                    "failure_if_omitted": "Learner computes arithmetic mean of class limits without frequency weighting."
                },
                {
                    "concept_id": "CON-MATH-PROBABILITY-BOUNDS",
                    "canonical_statement": "For any random event E in sample space S, classical probability is P(E) = n(E)/n(S), bounded strictly by 0 <= P(E) <= 1. P(empty) = 0 for impossible event, P(S) = 1 for certain event.",
                    "why_required": "Foundational probability axiom governing valid probability values.",
                    "failure_if_omitted": "Learner outputs probabilities > 1 or negative probabilities without recognizing contradiction."
                },
                {
                    "concept_id": "CON-MATH-COMPLEMENTARY-EVENTS",
                    "canonical_statement": "The complement of event E, denoted not(E) or E_bar, consists of all outcomes in S not in E. Since E and E_bar partition S, P(E) + P(E_bar) = 1, yielding P(E_bar) = 1 - P(E).",
                    "why_required": "Enables efficient calculation of 'at least one' and non-occurrence probabilities.",
                    "failure_if_omitted": "Learner attempts brute-force enumeration of large complementary event spaces."
                }
            ],
            "mandatory_equations": [
                {
                    "equation_id": "EQ-MATH-PROBABILITY-AXIOM",
                    "formula": "0 \\le P(E) \\le 1",
                    "meaning_of_symbols": "P(E) is probability of event E; must lie in closed interval [0, 1].",
                    "symbols": [
                        {
                            "symbol": "P(E)",
                            "name": "Probability of Event",
                            "domain": "[0, 1]",
                            "geometric_or_algebraic_role": "Normalized likelihood measure"
                        }
                    ],
                    "reference_frame_or_sign": "Strictly non-negative and bounded by 1",
                    "conditions_of_validity": "Valid for all events in any finite probability space.",
                    "obligations": ["EXPLAIN", "INTERPRET", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-COMPLEMENTARY-PROB",
                    "formula": "P(\\bar{E}) = 1 - P(E)",
                    "meaning_of_symbols": "Complementary event probability equals one minus event probability.",
                    "symbols": [
                        {
                            "symbol": "P(\\bar{E})",
                            "name": "Complementary Probability",
                            "domain": "[0, 1]",
                            "geometric_or_algebraic_role": "Probability of non-occurrence"
                        }
                    ],
                    "reference_frame_or_sign": "Partition of sample space S",
                    "conditions_of_validity": "E and E_bar are exhaustive mutually exclusive events.",
                    "obligations": ["DERIVE", "APPLY", "VERIFY"]
                },
                {
                    "equation_id": "EQ-MATH-EMPIRICAL-CENTRAL-TENDENCY",
                    "formula": "3 \\,\\text{Median} \\approx \\text{Mode} + 2 \\,\\text{Mean}",
                    "meaning_of_symbols": "Empirical relationship linking the three measures of central tendency.",
                    "symbols": [
                        {
                            "symbol": "\\text{Mean}, \\text{Median}, \\text{Mode}",
                            "name": "Central Tendency Measures",
                            "domain": "\\mathbb{R}",
                            "geometric_or_algebraic_role": "Distribution location parameters"
                        }
                    ],
                    "reference_frame_or_sign": "Empirical approximation for unimodal moderately skewed distributions",
                    "conditions_of_validity": "Unimodal unimodal continuous distributions.",
                    "obligations": ["EXPLAIN", "APPLY", "VERIFY"]
                }
            ],
            "representations": [
                {
                    "representation_id": "REP-MATH-PROBABILITY-VENN-TREE",
                    "representation_type": "PROBABILITY_TREE_OR_VENN",
                    "name": "Venn Diagram / Probability Tree for Sample Space Partition",
                    "math_encoded": "Universal set box representing sample space S with area 1, containing event circle E with area P(E) and complement region E_bar with area 1 - P(E).",
                    "mandatory_labels": ["Sample Space S (Area 1)", "Event E", "Complement Region E_bar", "Impossible Event \\emptyset"],
                    "what_cannot_be_omitted": "Universal set boundary enclosing all outcomes and sum to 1 annotation.",
                    "common_incorrect_version": "Showing event E extending outside universal set S.",
                    "verification_method": "Probability conservation: P(E) + P(E_bar) = 1."
                }
            ],
            "model_conditions": [
                {
                    "condition": "Outcomes in classical probability must be equally likely.",
                    "why_needed": "If outcomes are biased, ratio of favorable to total outcomes does not yield probability.",
                    "what_changes_if_violated": "Classical formula fails; empirical or weighted probability required."
                }
            ],
            "reasoning_sequence": [
                {
                    "step": 1,
                    "expert_action": "Determine sample space size n(S) and verify outcomes are mutually exclusive and equally likely.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 2,
                    "expert_action": "Enumerate favorable outcomes n(E) satisfying the event criterion.",
                    "inferential_jump": "LOW"
                },
                {
                    "step": 3,
                    "expert_action": "Calculate P(E) = n(E)/n(S) and confirm 0 <= P(E) <= 1.",
                    "inferential_jump": "LOW"
                }
            ],
            "required_transformations": [
                {
                    "from_mode": "Exhaustive event outcome description",
                    "to_mode": "Complementary event calculation 1 - P(E)",
                    "target_core_role": "CORE1B_GENERATIVE_RECONSTRUCTION",
                    "description": "Simplify calculation of 'at least one' by evaluating complementary 'none' event."
                },
                {
                    "from_mode": "Grouped frequency distribution table",
                    "to_mode": "Mean, Median, and Mode central tendency values",
                    "target_core_role": "CORE2A_DECLARATIVE_WORKED_PROBLEM",
                    "description": "Calculate mean via step-deviation, median via cumulative frequency, and mode via modal class formula."
                }
            ],
            "misconceptions": [
                {
                    "misconception_id": "MISC-MATH-PROBABILITY-OUT-OF-BOUNDS",
                    "incorrect_belief": "Calculating a probability greater than 1 (e.g. 5/4) or negative by misidentifying the denominator or confusing probability with odds.",
                    "why_plausible": "Inverting fraction or confusing favorable/unfavorable with favorable/total.",
                    "required_counterexample": "Favorable outcomes cannot exceed total outcomes (n(E) <= n(S)). A probability of 1.25 implies 125 outcomes out of 100 trials, which is impossible.",
                    "required_technical_repair": "Strictly assert 0 <= P(E) <= 1 as an inviolable validity check on every probability calculation."
                }
            ],
            "mandatory_verifications": [
                "Verify 0 <= P(E) <= 1 for every computed probability.",
                "Verify P(E) + P(not E) == 1.",
                "Verify empirical central tendency formula: 3 Median approx Mode + 2 Mean."
            ],
            "problem_families": [
                {
                    "family_id": "PF-MATH-CENTRAL-TENDENCY-CALC",
                    "name": "Mean, Median, and Mode of Grouped Data",
                    "recognition_cues": "Class interval frequency tables requiring one or more central measures.",
                    "first_technical_move": "Form cumulative frequency column for median, identify modal class for mode, compute midpoints for mean.",
                    "common_fatal_error": "Using upper class limit instead of class mark (midpoint) in mean formula.",
                    "typical_unknown": "Mean, Median, or Mode value"
                },
                {
                    "family_id": "PF-MATH-CLASSICAL-PROBABILITY",
                    "name": "Classical Probability of Dice, Cards, Coins, and Urns",
                    "recognition_cues": "Standard random experiment with well-defined sample space requiring P(E).",
                    "first_technical_move": "Write down exact total count n(S) and filter favorable count n(E).",
                    "common_fatal_error": "Miscounting sample space size (e.g. thinking two dice have 12 outcomes instead of 36).",
                    "typical_unknown": "Exact fractional probability P(E)"
                }
            ],
            "difficulty_profile": {
                "prerequisite_depth": 0,
                "element_interactivity": 1,
                "inferential_jump_severity": 1,
                "representation_translation": 2,
                "model_discrimination": 1,
                "sign_or_frame_sensitivity": 2,
                "multi_step_dependency": 2,
                "abstraction": 1,
                "misconception_density": 2,
                "synthesis": 1,
                "provisional_difficulty": "EASY",
                "difficulty_basis": "Classical probability bounds, complementary events, and grouped data central tendency.",
                "maturity": "ENGINEERING"
            },
            "release_checklist": {
                "canonical_concepts_present": True,
                "mandatory_equations_present": True,
                "validity_conditions_stated": True,
                "required_representations_present": True,
                "reasoning_chain_complete": True,
                "misconceptions_addressed": True,
                "independent_verification_exists": True,
                "problem_family_map_exists": True,
                "provenance_verified": True,
                "difficulty_profile_validated": True
            },
            "badges": {
                "base_badges": ["PROBABILITY_AXIOMS", "STATISTICS_FOUNDATION"],
                "conditional_badges": ["COMPLEMENT_MASTERY"]
            },
            "falsification_cases": [
                {
                    "test_id": "FALS-STAT-01",
                    "authoring_defect": "Accepting probability value P(E) > 1 or P(E) < 0.",
                    "expected_failure_reason": "Violates fundamental Kolmogorov probability axiom 0 <= P(E) <= 1."
                }
            ]
        }
    ]

    registry = {
        "schema_version": "1.0.0",
        "registry_id": "REG-MATH-TECH-GATE-V1",
        "authority": "SOURCE-DEFINED",
        "governing_standard": "Canonical Mathematics Technical Engineering Readiness Standard",
        "maturity": "ENGINEERING",
        "subtopic_gates": subtopics
    }
    return registry


def main() -> None:
    reg = build_registry()
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Successfully compiled Mathematics Technical Engineering Gate Registry with {len(reg['subtopic_gates'])} gates to {OUT_PATH}")


if __name__ == "__main__":
    main()
