# Mathematics V2 — Core (2A): textbook-quality transfer realization

Core (2) is the governed semantic transfer/practice plan over the **original source questions**. Core (2A) is the learner-product layer that turns that approved transfer structure into a textbook-quality practice PDF.

```text
Core (2): governed source-question transfer semantics
        |
        v
Core (2A): textbook-quality transfer realization
        |
        +--> core2a_textbook_manuscript.json
        +--> core2a_quality_audit.json
        `--> core2a_student_practice.pdf
```

Core (2A) exists for the same reason Core (1A) exists: the semantic product should remain auditable and machine-facing, while the final learner artifact should read like a professionally authored mathematics book.

## Immutable transfer structure

Core (2A) must preserve the approved Core (2) structure and source authority. In particular:

- original source-question order is unchanged;
- source stems, givens, options, units and subparts are unchanged;
- question identifiers remain unchanged;
- each question retains its Core (1) linkage state;
- assessment-safety classifications remain unchanged;
- multiple-solution and underdetermined cases remain intact;
- source corrections/notes remain traceable;
- the attempt surface remains before the worked solution;
- for the approved paired-page format, each attempt page is immediately followed by its worked solution page;
- reasoning, solution and verification remain distinct semantic objects.

Core (2A) may not regroup all questions into one section and all solutions into another, may not renumber questions, and may not replace source problems with newly authored substitutes.

## What Core (2A) is allowed to improve

Structure preservation does **not** mean preserving sparse or weak page composition. Core (2A) may substantially improve:

- mathematical representation on the attempt page;
- workspace shaped to the response demanded by the question;
- progressive learner hints, provided they do not disclose the solution prematurely;
- worked-solution narration and visual hierarchy;
- step labelling where it helps the learner follow a multi-stage argument;
- diagrams, tables and equation annotations grounded in the Core (2) representation plan;
- independent verification/checking presentation;
- typography, spacing and pagination;
- Core (1A) review backlinks where the linkage is publication-legal.

The governing principle is:

```text
preserve source problem + approved attempt/solution architecture
while materially improving learner comprehension and mathematical representation
```

## Attempt-page contract

The attempt page is not a second worked solution. It must preserve productive thinking.

For each question, support should remain downstream of the source prompt and should respect the Core (2) hint ladder:

```text
H0  attempt the original question
H1  notice the relevant structure
H2  choose a representation or method
H3  take the first executable mathematical step
```

Core (2A) may make these supports more readable or visually meaningful, but it must not collapse H1/H2/H3 into the answer.

## Worked-page contract

The worked page should execute the mathematics fully enough for a learner to diagnose an error. A textbook-quality solution should, where mathematically relevant:

1. identify the governing relation or representation;
2. substitute the actual data;
3. show the intermediate algebra/arithmetic;
4. state the conclusion;
5. perform an independent check.

A compact answer-only or solution-summary rendering is not acceptable when the Core (2) semantic solution is multi-stage.

## Structural falsifiers

Core (2A) should fail closed on at least the following classes of drift:

```text
CORE2A_SOURCE_ORDER_DRIFT
CORE2A_SOURCE_STEM_DRIFT
CORE2A_QUESTION_ID_DRIFT
CORE2A_ATTEMPT_SOLUTION_ADJACENCY_LOST
CORE2A_HINT_DISCLOSES_SOLUTION
CORE2A_SOLUTION_DEPTH_COLLAPSED
CORE2A_VERIFICATION_LOST
CORE2A_CORE1_LINK_DRIFT
CORE2A_ASSESSMENT_SAFETY_LOST
CORE2A_MULTI_SOLUTION_COLLAPSED
CORE2A_INTERNAL_JARGON_LEAK
CORE2A_QUALITY_GATE_FAILED
```

## Relationship to Core (1A)

The learner-product architecture is intentionally symmetric:

```text
Core (1)  --> Core (1A): textbook-quality teaching realization
Core (2)  --> Core (2A): textbook-quality transfer realization
```

Core (1A) may author fresh learner instances inside governed problem families. Core (2A) must not: it realizes the original source questions supplied by Core (2).

The two A-stages therefore have different authoring permissions but the same product-quality objective: preserve approved semantics and structure while producing learner-facing textbook-quality content and representation.

## Release meaning

Core (2A) inherits the publication legality and Core (1) linkage state of its source Core (2) plan. It cannot promote an unapproved Core (1) link, alter assessment validity, or bypass existing human gates.
