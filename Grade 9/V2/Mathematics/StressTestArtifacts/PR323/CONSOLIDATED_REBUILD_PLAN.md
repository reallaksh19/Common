# Consolidated rebuild plan

## Completion definition

A chapter is not complete because Core1 and Core2 PDFs exist. It is complete when all of the following hold:

1. frozen source corpus coverage is complete;
2. atomic source asks/subparts are reconciled;
3. topic concept and prerequisite graph is explicit;
4. Core1 reconstructs every reasoning capability Core2 will demand;
5. every non-trivial Core2 reasoning state maps to explicit Core1 teaching evidence;
6. every Core1 learner-facing question has answer authority;
7. Core2 attempt pages do not leak answers;
8. every Core2 atomic ask has a full solution and verification witness;
9. math typography, diagrams, workspace, pagination and source choices/subparts survive final rendering correctly;
10. post-render semantic/visual QA passes.

## Core1 lesson evidence model

Recommended evidence IDs follow the pattern `<TOPIC>-C<n>-<STAGE>`, where stage is one of:

- `ANCHOR`
- `PREREQ`
- `REPRESENT`
- `EXPLAIN`
- `RECONSTRUCT`
- `WORKED`
- `CONTRAST`
- `REPAIR`
- `GUIDED`
- `FADED`
- `INDEPENDENT`
- `TRANSFER`
- `VERIFY`
- `READINESS`

Not every concept needs a separate full page for every stage, but the required evidence must be realized, not merely labelled.

## Core2 route model

Reasoning routes should be problem-family-specific and variable-depth. Use only the states actually needed, selected from roles such as:

- `INTERPRET`
- `REPRESENT`
- `MODEL`
- `SETUP`
- `EXECUTE`
- `TRANSFORM`
- `COMPARE`
- `INFER`
- `VERIFY`

Each non-trivial state carries `core1_evidence_ref` and, where relevant, a hint binding.

## Hint semantics

- H1: governing invariant / conceptual clue;
- H2: representation or method selection;
- H3: first executable mathematical move.

## Answer authority

Core1 answers must be separated enough to preserve an honest attempt. Suitable patterns:

- short lesson-local `Check after you try` block;
- end-of-lesson answer strip;
- Core1 Appendix A for substantial independent/transfer/readiness tasks.

Open-response items require acceptance criteria. Proof questions require a model proof / proof skeleton with provenance. Multiple-valid-answer tasks require the admissible answer rule.

## Publication hard gates

Suggested falsifiers consolidated from the stress test:

```
CORE2_SOURCE_CORPUS_COVERAGE_GAP
CORE2_SOURCE_SUBPART_COVERAGE_GAP
RENDERED_SOURCE_OPTION_COVERAGE_GAP
ASSESSMENT_OBJECT_OCCLUSION
ASSESSMENT_OBJECT_CLIPPED
MATH_EXPRESSION_FLATTENED_TO_PLAIN_TEXT
MATH_SCRIPT_NOT_TYPESET
MATH_FONT_NOT_BOUND
REQUIRED_MATH_GLYPH_MISSING
TEXT_BELOW_MIN_READABLE_SIZE
LAYOUT_EXCESSIVE_UNUSED_AREA
VISUAL_ELEMENT_COLLISION
ROUTE_PANEL_OVERFLOW
QUESTION_PANEL_TRUNCATED
WORKSPACE_MISMATCHES_RESPONSE_MODE
REASONING_ROUTE_INCOMPLETE
CORE2_REASONING_STATE_WITHOUT_CORE1_EVIDENCE
CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED
CORE1_GENERATED_INSTANCE_DEGENERATE
CORE1_GENERATED_INSTANCE_UNVERIFIED
ATTEMPT_REPRESENTATION_LEAKS_ANSWER
VERIFICATION_NOT_EXECUTABLE
SPATIAL_MATHEMATICAL_FIDELITY_FAILURE
LEARNER_QUESTION_WITHOUT_ANSWER_AUTHORITY
ATOMIC_ASK_WITHOUT_SOLUTION
OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA
ANSWER_WITHOUT_VERIFICATION
ATTEMPT_PAGE_ANSWER_LEAKAGE
```

## Remaining consolidation order

1. Linear Equations in Two Variables - full final cross-core rebuild.
2. Coordinate Geometry - full final cross-core rebuild.
3. Lines & Angles - preserve Core1 v2 depth, retrofit final bridge/answer contract.
4. Surface Areas & Volumes - preserve deep concept architecture, retrofit bridge/answer contract and strengthen 3-D diagrams.
5. Run one seven-topic audit: `Core2 reasoning demands - Core1 teaching evidence = empty set`.
