---
name: grade9-math
description: Apply Grade 9 Mathematics reasoning, concept fingerprinting, difficulty profiling, solution-path analysis, misconception logic, and concept-book pedagogy to source-grounded learning material and question banks. Use for number systems, algebra, polynomials, sequences and series, geometry, coordinate geometry, statistics/probability, HOTS, Olympiad foundation, competitive-foundation mathematics, and SEE -> REALIZE -> UNDERSTAND -> ADOPT concept-book work.
---

# Grade 9 Mathematics

Provide the Mathematics reasoning layer within the Grade 9 workflow.

## Fingerprint

For each item identify chapter/topic, secondary topics, mathematical mechanisms, hidden structure/invariant, representation choice, answer type, minimum expert solution path, traps, and case conditions.

Use stable archetypes where useful, e.g. `POLYNOMIAL_ROOTS_IN_GP`, `RECURRENCE_ZERO_SECOND_DIFFERENCE`, `PARTIAL_SUM_TO_TERM_DIFFERENCE`, `SIMILAR_TRIANGLES_RATIO_TRANSFER`.

## Difficulty vector

Use 0-10 dimensions:

- `conceptual`
- `recognition`
- `reasoning_steps`
- `algebra`
- `hidden_structure`
- `constraints_cases`
- `calculation_burden`
- `trap_density`

Current scalar screening score:

`D = 0.25C + 0.25R + 0.15S + 0.15A + 0.10H + 0.10K`

Treat it as a local engineering screen, not psychometric calibration. The `grade9-question-bank` policy is authoritative for acceptance/rejection.

## Representation strategy

Train useful switches among list/pattern, table, finite-difference or ratio marks, algebraic general term, sigma notation, factorization, coordinates/geometry, auxiliary construction, invariants and symmetry.

## Mathematics Concept Book mode

When the user asks for a Mathematics Concept Book, chalkboard-style explanation, formula-understanding book, or asks to make mathematics genuinely understandable rather than merely provide formulas, read `references/concept-book-see-realize-understand-adopt.md` before authoring.

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

`CONNECT` is source traceability/navigation, not a fifth cognitive stage.

- **SEE** — show a pattern, table, diagram, expansion, transformation or contrast before the general formula.
- **REALIZE** — identify the invariant/hidden structure in ordinary language.
- **UNDERSTAND** — derive/reconstruct, explain factors/exponents/signs/index shifts, switch representations, and test special/boundary cases.
- **ADOPT** — recognize in disguise, choose the first move independently, reject a tempting wrong method, transfer to a non-identical problem, and rebuild if the formula is forgotten.

For Sequence & Series, read `references/sequence-series-concept-book-example.md` as the worked exemplar.

## Mathematics concept-book gates

- `MSRU-01 NO_NAKED_FORMULA`
- `MSRU-02 SEE_BEFORE_NAME`
- `MSRU-03 INVARIANT_EXPLICIT`
- `MSRU-04 ORIGIN_OF_TERMS_FACTORS_EXPONENTS_SIGNS`
- `MSRU-05 REPRESENTATION_TRANSLATION`
- `MSRU-06 CONTRAST_PAIR`
- `MSRU-07 FIRST_MOVE_INDEPENDENCE`
- `MSRU-08 RECONSTRUCTION_TEST`
- `MSRU-09 TRANSFER_IN_DISGUISE`
- `MSRU-10 SOURCE_TRACEABILITY`
- `MSRU-11 SOURCE_DEFECTS_NOT_SILENTLY_REPAIRED`
- `MSRU-12 GRADE9_DEPTH`
- `MSRU-13 SUMMATION_AS_REPEATED_ADDITION`
- `MSRU-14 TRANSFORM_BEFORE_CALCULATE`
- `MSRU-15 ADOPT_MASTERY`

## Misconceptions

Capture specific wrong models: sign errors in Vieta, reciprocal-of-sum confusion, HP treated as AP, `a_n` confused with `S_n`, finite/infinite GP conditions ignored, endpoint attainability errors, theorem use outside its conditions, etc.

## Linked products

- Concept Book: `SEE -> REALIZE -> UNDERSTAND -> ADOPT`
- First-Step Reference: `SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`
- Question Bank: `RECOGNIZE -> SOLVE -> CHECK -> TRANSFER`

Combine with `grade9-question-bank` for bank engineering and `grade9-learning-enrichment` for hints/diagnostics when those skills are installed.
