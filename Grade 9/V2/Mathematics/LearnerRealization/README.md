# Mathematics V2 — LearnerRealization (M-UPGRADE-2 items 2, 5, 8, 9)

The PR #323 RCA named the missing layer directly (RC-1): the pipeline jumped from semantic
intent to representation/rendering, so a route could keep its semantic label without ever
proving the mathematical state transition happened.

```text
Core1 lesson stage / Core2 reasoning route      (semantic plan)
        |
        v
LEARNER MATHEMATICAL REALIZATION                (this phase)
        |
        v
representation / layout plan
        |
        v
PDF realization  ->  post-render semantic / visual QA
```

## The defect this phase makes unpublishable

The Theory-of-Equations reproducer, in the owner's own words:

```text
v1   INTERPRET / REPRESENT / EXECUTE / VERIFY            route metadata
v2   "Compute S1, compute S2, compute S3 ..."            operation named, not demonstrated
v3   S2 + a1S1 + 2a2 = 0                                 realized mathematics
     S2 + 0(0) + 2(−7) = 0
     S2 = 14
```

v1 and v2 were both structurally green. Only v3 teaches. So the governing invariant is:

> Naming an operation is not equivalent to demonstrating the operation.

## The shared route-state object

One object shape carries every derivation step, deliberately the same
`{role, input_state, operation, output_state, why_valid}` shape used by the Physics and
Chemistry siblings so a later cross-subject pass has one pattern to generalize:

```json
{
  "step_id": "S4",
  "role": "SETUP",
  "input_state": { "...MathExpression..." },
  "operation": {"name": "SUBSTITUTE", "rule_or_justification": "Put x = 2 into every term"},
  "substitution": { "...MathExpression..." },
  "output_state": { "...MathExpression..." },
  "why_valid": "A polynomial is defined for every real input, so x = 2 is legal.",
  "learner_explanation": "Replace each x in x³ − 2x² − x + 2 by 2 ...",
  "equivalence_witness": { "...invariant witness..." },
  "sufficiency": null,
  "core1_evidence_ref": "MATH-C1L-FACTOR-THEOREM",
  "trivial": false
}
```

Role vocabulary is `INTERPRET, CLASSIFY, REPRESENT, MODEL, SELECT_THEOREM, SETUP,
TRANSFORM, EXECUTE, COMPARE, INFER, CHECK_CONDITION, CHECK_SUFFICIENCY, VERIFY`. The
registry marks which roles are *substantive* and which of those must change state, so a
`CLASSIFY` step is legitimately allowed to restate while an `EXECUTE` step is not.

The same derivation is projected into the recovery ladder, so H1/H2/H3 are not
miscellaneous hints but views of declared steps:

```text
H1  governing invariant / structure       (derived_from_step_id)
H2  representation / method selection     (derived_from_step_id)
H3  first executable mathematical move    (derived_from_step_id)
```

A hint that resolves to no declared step, that contains no item anchor, or that contains
the final answer fails closed.

## Item 5 — equivalence-transformation witnesses and information sufficiency

An algebraic move is not an opaque string. `math-equivalence-transformation.schema.json`
requires `{operation, before_relation, after_relation, preserved_invariant, precondition,
reversible}`. A non-reversible move (squaring both sides, clearing a denominator that can
vanish) that claims `SOLUTION_SET` preservation must also carry an
`extraneous_root_check`, or it fails `SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK`.

`CHECK_SUFFICIENCY` is a first-class role carrying
`UNIQUE | MULTIPLE | UNDERDETERMINED | INCONSISTENT`. A parameterized item with no such
state fails `PARAMETERIZED_ITEM_WITHOUT_SUFFICIENCY_CHECK`.

## Item 8 — answer custody

Every learner-facing question resolves to an explicit answer artifact, and the artifact
kind determines what "resolved" means:

| answer_kind | what must exist |
| --- | --- |
| `NUMERIC` / `EXPRESSION` / `ORDERED_PAIR` / `SET` / `MCQ_CHOICE` | a `final_answer` expression or answer prose |
| `PROOF` | `model_proof_steps`, each with what licenses it |
| `CONSTRUCTION` | `construction_verification_conditions` |
| `MULTIPLE_VALID` | an `acceptance_rule` **and** `admissible_answers` |
| `OPEN_RESPONSE` | an `acceptance_rule` |
| `COUNTEREXAMPLE` | a `counterexample_witness` |

Three things are kept deliberately distinct, because collapsing them is how the stress
test found questions with no answer at all:

```text
final answer          !=  quick check          !=  independent verification
```

A quick check standing in for the answer raises `SELF_CHECK_SUBSTITUTED_FOR_ANSWER`; a
generic "check your answer" verification raises `ANSWER_WITHOUT_VERIFICATION`. Custody
guarantees the answer exists *somewhere reachable* (`AFTER_ATTEMPT`, `LESSON_END`,
`ANSWER_APPENDIX`, `SOLUTION_PAGE`) while the attempt surface stays answer-neutral —
answer availability must not become answer leakage.

## Item 9 — enforcing #351's central learner-language policy (not a parallel ban-list)

`#351` established `LearnerProduct/policies/math-learner-language-policy.json` as the
central learner-language authority: approved public labels (`TRY IT FIRST`, `SMALL CLUE`,
`BIGGER CLUE`, `HOW DO I START?`, `THINK IT THROUGH`, `FULL WORKING`, `QUICK CHECK`,
`WHERE THIS QUESTION CAME FROM`) and a forbidden-internal-terms list, bound by policy id in
`run_learner_product.py`.

Two things were missing, and only those two were built here:

1. **Nothing scanned text against it.** `run_learner_product.py` checks the policy *binding*
   (`LEARNER_PRODUCT_POLICY_BINDING_DRIFT`) and `STAGE_RUNNERS` is intentionally empty, so
   no stage ever compared learner copy to the list. `engine/learner_copy.py` is that
   detector, and it reads the policy file as its authority.
2. **A bare role label passed the list.** The forbidden terms are matched as substrings, so
   a heading of `RECONSTRUCT`, `CONTRAST` or `VERIFY` — an internal reasoning role printed
   as learner copy, the same defect class as pipeline jargon — was not caught. The policy
   file was therefore **extended in place**, keeping `policy_id` (`MATH-LEARNER-LANGUAGE-v1`)
   so the binding check still resolves, with `forbidden_learner_role_labels`,
   `internal_role_label_public_titles`, `internal_identifier_patterns` and
   `role_label_detection`.

`registry/math-learner-copy-registry.json` therefore holds **no ban-list of its own**. It
carries only the consumer bindings (which falsifier each stage raises) and the eight legacy
tokens Core1A enforced before the central policy existed, which are *unioned* with the
policy so adopting it can only widen what Core1A already caught — never narrow it. Core1A's
original list survives verbatim as `LEGACY_FORBIDDEN_LEARNER_TOKENS`.

Core2A's `CORE2A_LEARNER_JARGON_LEAK` was declared in its quality profile with no engine to
raise it; it now has one. Each consumer keeps its own falsifier prefix, and no undeclared
code is invented — Core2A has no separate identifier falsifier, so an identifier leak is
raised under the code its profile does declare.

Detection stays `ALL_CAPS_TOKEN_OR_EXACT_HEADING`: the ordinary English words *verify*,
*represent* and *compare* are perfectly good learner copy, and the policy's own approved
labels are exempt, so `QUICK CHECK` is never mistaken for the `VERIFY` role label.

## Reference corpus

`fixtures/math-reference-realizations.fixture.json` holds four of the seven stress-tested
topics realized as actual mathematics. It is generated by
`fixtures/build_math_reference_realizations.py`, and the committed JSON is what the gates
run against, so a regeneration that changes the product is visible in review.

| topic | role | what it proves |
| --- | --- | --- |
| Number Systems | `WORKED` | conjugate / difference-of-squares rationalisation of `1⁄(√7 − 2)`, real substitutions throughout |
| Polynomials | `WORKED` | factor theorem with `p(2)` actually evaluated, then complete factorisation and an expand-back check |
| Coordinate Geometry | `GUIDED` | distance and midpoint from declared coordinates, with the horizontal-segment observation made before any formula |
| Linear Equations | `INDEPENDENT` | parameter determination plus a `MULTIPLE` information-sufficiency verdict on the resulting dependent pair |

Nothing in that table is a schema shape. Each topic is a data instance of the same
subject-wide contracts.

## Falsifiers

```text
WORKED_EXAMPLE_UNINSTANTIATED                     authoring obligation or template token survived
MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED         the exact Theory-of-Equations v2 defect
LEARNER_STEP_WITHOUT_MATHEMATICAL_STATE_TRANSITION
LEARNER_ROUTE_GENERIC_ACROSS_UNRELATED_ITEMS      incl. a cross-item transplant check
LEARNER_SUPPORT_NOT_GROUNDED_IN_CURRENT_ITEM
INTERNAL_REASONING_LABEL_EXPOSED_AS_LEARNER_COPY
INTERNAL_IDENTIFIER_EXPOSED_AS_LEARNER_COPY
SCAFFOLD_DISCLOSES_SOLUTION
EQUIVALENCE_TRANSFORMATION_WITHOUT_INVARIANT_WITNESS
EQUIVALENCE_TRANSFORMATION_PRECONDITION_MISSING
SOLUTION_SET_NOT_PRESERVED_WITHOUT_CHECK
PARAMETERIZED_ITEM_WITHOUT_SUFFICIENCY_CHECK
LEARNER_QUESTION_WITHOUT_ANSWER
SELF_CHECK_SUBSTITUTED_FOR_ANSWER
PROOF_PROMPT_WITHOUT_MODEL_PROOF
CONSTRUCTION_WITHOUT_VERIFICATION_CONDITIONS
MULTIPLE_VALID_ANSWERS_WITHOUT_ADMISSIBILITY_RULE
OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA
COUNTEREXAMPLE_WITHOUT_WITNESS
ANSWER_WITHOUT_VERIFICATION
ATTEMPT_PAGE_ANSWER_LEAKAGE
LEARNER_REALIZATION_GATE_FAILED
```

The cross-item adversarial check deserves a note, because it is the RCA's RC-7 heuristic
made machine-falsifiable: if the learner-facing prose of one item can be transplanted onto
a semantically unrelated item and still be valid, it was metadata rather than instruction.
The audit therefore refuses two items that share the same explanation/justification pair.

## Release meaning

`PUBLICATION_ENGINEERING` only. Realizing mathematics well does not promote PCK beyond
`PROVISIONAL_PROMOTED` and does not substitute for the subject, pedagogy, assessment,
visual or expert-review gates, all of which remain `PENDING`.
