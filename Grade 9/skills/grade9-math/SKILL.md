---
name: grade9-math
description: Apply Grade 9 Mathematics reasoning, concept fingerprinting, difficulty calibration, solution-path analysis, misconception logic, partial-knowledge assimilation pedagogy, and concept-book authoring to source-grounded textbooks and question banks. Use for algebra, number systems, polynomials, sequences and series, geometry, coordinate geometry, statistics/probability, school HOTS, Olympiad foundation, competitive-foundation mathematics, and SEE -> REALIZE -> UNDERSTAND -> ADOPT concept-book work.
---

# Grade 9 Mathematics

Provide the subject-specific Mathematics reasoning and teaching layer for the shared Grade 9 workflow.

## Default learner model for difficult concepts

Unless the task clearly targets first exposure, design for a learner who has roughly **50% of the concept**:

- recognizes some vocabulary;
- remembers one or two formulas/procedures;
- can solve routine examples;
- has incomplete connections;
- is unreliable at method recognition, representation choice, boundary conditions, and transfer.

Do not treat formula recall as mastery. Do not reteach from zero when a short reconnect diagnostic can reveal what the learner already owns.

Before authoring a difficult concept, read:

- `references/concept-book-see-realize-understand-adopt.md`
- `references/partial-knowledge-assimilation-concept-map.md`

## Mandatory concept map before prose

Create a topic concept map before drafting the student book. Include:

- prior-knowledge nodes;
- missing bridge nodes;
- core invariants;
- representations;
- decision boundaries;
- misconceptions;
- first moves;
- transfer endpoints;
- source-custody nodes where applicable.

Every major concept must contain:

`PRIOR -> BRIDGE -> INVARIANT -> FIRST MOVE -> TRANSFER`

and at least one competing-method path:

`VISIBLE CLUE -> TEMPTING WRONG MODEL -> CONTRAST -> CORRECT DECISION`.

## Mathematical fingerprint

For each anchor/question identify:

- chapter and primary topic;
- secondary topics;
- mathematical mechanism(s);
- hidden structure or invariant;
- representation choice;
- answer type;
- minimum expert solution path;
- common traps and case conditions;
- likely partial-knowledge misconception;
- visible clue that should trigger the first move;
- nearest competing method and the decision boundary between them.

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

Also record the **expert noticing step**: what feature of the problem made that path preferable *before* calculation began.

## Representation strategy

Train movement among useful mathematical representations, for example:

- visible list / pattern;
- table;
- finite-difference or ratio marks;
- algebraic expression / general term;
- sigma notation;
- factorized form;
- coefficient/root form;
- graph;
- coordinate or geometric representation;
- auxiliary construction;
- invariants and symmetry.

For partial-knowledge learners, representation switching is often the missing bridge. Make the switch explicit rather than presenting the final representation as obvious.

## Mathematics Concept Book mode

For a Mathematics Concept Book, read `references/concept-book-see-realize-understand-adopt.md` before authoring.

Macro cognitive sequence:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Operational assimilation loop for difficult concepts:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Use `CONNECT` only for source traceability/navigation; it is not a cognitive stage.

- **SEE / RECONNECT** — retrieve a familiar case and place a pattern, table, diagram, worked fragment, transformation or contrast on the board before the general rule.
- **DISCOVER / REALIZE** — let the learner notice and then name the invariant or hidden structure.
- **MAKE SENSE / UNDERSTAND** — derive/reconstruct the result, explain why each term/factor/exponent/sign is present, switch representations, test edge/special cases, and expose wrong models.
- **TRY** — require an H0 independent first move before giving support.
- **DIAGNOSE** — classify the actual gap: recognition, representation, concept, first move, algebra, condition/domain, or transfer.
- **FADE** — move H3 -> H2 -> H1 -> H0 across practice; do not preserve permanent scaffolding.
- **ADOPT** — convert the idea into a reusable internal rule: “when I see..., I test... because...”.
- **TRANSFER** — use a changed surface form, mixed-topic disguise, or boundary/source-integrity case.

For Sequence & Series, read `references/sequence-series-concept-book-example.md` as a worked exemplar, but do not copy its surface layout mechanically.

### Hint levels

- `H0 INDEPENDENT` — no hint.
- `H1 RECOGNITION` — point to the clue/question type.
- `H2 STRUCTURE` — name the invariant or representation.
- `H3 EXECUTION` — give the first algebraic relation only.

The student should encounter H0 before H1-H3. Repeated practice must fade support.

### Six-question assimilation test

For each major concept require evidence that the learner can answer:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation would require a different method?
5. Can you write the first two useful lines without help?
6. Can you solve a disguised version?

If the learner can repeat a worked solution but cannot answer 3, 4, or 6, the concept is not assimilated.

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
- `MSRU-16 PARTIAL_KNOWLEDGE_RECONNECT`
- `MSRU-17 MISSING_LINK_EXPLICIT`
- `MSRU-18 ATTEMPT_BEFORE_HINT`
- `MSRU-19 DIAGNOSTIC_REPAIR`
- `MSRU-20 HINT_FADING`
- `MSRU-21 SIX_QUESTION_ASSIMILATION`
- `MSRU-22 REFERENCE_IS_COMPRESSION`

## Mathematics misconceptions

Capture specific wrong mathematical models, not generic “careless mistakes.” Examples include sign errors in Vieta, reciprocal-of-sum confusion, treating HP as AP, endpoint attainability errors, confusing `a_n` with `S_n`, using a GP formula without convergence conditions, solving roots when only invariants are needed, or applying a theorem outside its assumptions.

For each major misconception record:

- why it is attractive to a partly prepared student;
- the smallest contrast that exposes it;
- the repair statement the student should internalize.

## Contrast-pair rule

Every important method must have a nearby competing method or non-example. Change as little as possible between the pair so the decision boundary becomes visible.

The learner must explain both:

- why the chosen method fits;
- why the tempting alternative is inferior or invalid.

## Scope discipline

Stay within the intended Grade 9/competitive-foundation scope unless higher-level extension is explicitly labeled. Do not introduce advanced formalism merely because it is elegant.

## Linked learning products

### Assimilation Book — primary teaching layer

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Use for difficult concepts and partial-knowledge repair.

### First-Step Reference — compression/revision layer

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

Use recognition atlas, phrase decoder, decision tree, first-step cards, traps, recognition-only drills, and source-to-mechanism map.

**Do not use the First-Step Reference as the only teaching layer for a difficult concept.**

### Question Bank

`RECOGNIZE -> SOLVE -> CHECK -> TRANSFER`

Use `../grade9-question-bank/SKILL.md` for bank construction and `../grade9-learning-enrichment/SKILL.md` for hints/diagnostics.
