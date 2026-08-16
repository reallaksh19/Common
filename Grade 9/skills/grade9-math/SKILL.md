---
name: grade9-math
description: Apply Grade 9 Mathematics reasoning, concept fingerprinting, difficulty calibration, solution-path analysis, misconception logic, and concept-book pedagogy to source-grounded textbooks and question banks. Use for algebra, number systems, polynomials, sequences and series, geometry, coordinate geometry, statistics/probability, school HOTS, Olympiad foundation, competitive-foundation mathematics, and SEE -> REALIZE -> UNDERSTAND -> ADOPT concept-book work.
---

# Grade 9 Mathematics

Provide the subject-specific Mathematics reasoning layer for the shared Grade 9 workflow.

## Mathematical fingerprint

For each anchor/question identify:

- chapter and primary topic;
- secondary topics;
- mathematical mechanism(s);
- hidden structure or invariant;
- representation choice;
- answer type;
- minimum expert solution path;
- common traps and case conditions.

Prefer stable archetypes such as:

- `POLYNOMIAL_ROOTS_IN_GP`
- `RECURRENCE_ZERO_SECOND_DIFFERENCE`
- `PARTIAL_SUM_TO_TERM_DIFFERENCE`
- `SIMILAR_TRIANGLES_RATIO_TRANSFER`
- `COORDINATE_DISTANCE_CONSTRAINT`

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

Calculation burden is informative but must not substitute for conceptual difficulty.

A useful screening score is:

`D = 0.25C + 0.25R + 0.15S + 0.15A + 0.10H + 0.10K`

This is a local screening heuristic, not psychometric calibration. The question-bank skill remains authoritative for acceptance/rejection policy.

## Solution-path rule

Record the shortest legitimate expert reasoning path as meaningful steps. Reject same-level candidates that collapse a high-recognition anchor into routine substitution even if the arithmetic is longer.

## Representation strategy

Train movement among useful mathematical representations, for example:

- visible list / pattern;
- table;
- finite-difference or ratio marks;
- algebraic expression / general term;
- sigma notation;
- factorized form;
- coordinate or geometric representation;
- auxiliary construction;
- invariants and symmetry.

## Mathematics Concept Book mode

For a Mathematics Concept Book, read `references/concept-book-see-realize-understand-adopt.md` before authoring.

Core cognitive sequence:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Use `CONNECT` only for source traceability/navigation; it is not a fifth cognitive stage.

- **SEE** — place a pattern, table, diagram, worked fragment, transformation or contrast on the board before the general rule.
- **REALIZE** — name the invariant or hidden structure: constant difference, ratio, symmetry, accumulation, recurrence, reciprocal structure, cancellation, factorization, conservation of form, etc.
- **UNDERSTAND** — derive/reconstruct the result, explain why each term/factor/exponent/sign is present, switch representations, test edge/special cases, and expose wrong models.
- **ADOPT** — recognize the idea in disguise, choose the first move without a chapter label, reject a tempting wrong method, transfer to a non-identical problem, and rebuild the result if the formula is forgotten.

For Sequence & Series, read `references/sequence-series-concept-book-example.md` as the worked exemplar.

### Mathematics concept-book gates

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

## Mathematics misconceptions

Capture specific wrong mathematical models, such as sign errors in Vieta, reciprocal-of-sum confusion, treating HP as AP, endpoint attainability errors, confusing `a_n` with `S_n`, using a GP formula without convergence conditions, or applying a theorem outside its assumptions.

## Scope discipline

Stay within the intended Grade 9/competitive-foundation scope unless higher-level extension is explicitly labeled. Do not introduce advanced formalism merely because it is elegant.

## Linked learning products

- Concept Book: `SEE -> REALIZE -> UNDERSTAND -> ADOPT`
- First-Step Reference: `SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`
- Question Bank: `RECOGNIZE -> SOLVE -> CHECK -> TRANSFER`

Use `../grade9-question-bank/SKILL.md` for bank construction and `../grade9-learning-enrichment/SKILL.md` for hints/diagnostics.
