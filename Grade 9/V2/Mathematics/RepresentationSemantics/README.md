# Mathematics V2 — Representation Semantics (M-H)

Tracking: #243. Consumes M-D problem/representation vocabulary and M-G Core1 instructional semantics.

## Boundary

This layer owns **why a mathematical representation exists, what semantic data it is allowed to render, what the learner must notice/do, and how it translates back to formal mathematics**.

It does not own mathematical truth, learner diagnosis, treatment selection, PCK promotion, final typography, page layout, or renderer-authored mathematical meaning.

```text
Core1 lesson / Core2 transfer intent
+ required representation semantics
+ teaching primitive registry
+ page-intent profile
+ authored RepresentationSpec[]
        ↓
RepresentationSemantics gate
        ↓
MathRepresentationPlan
        ↓
renderer/layout
```

The renderer is downstream. It receives declared semantic data; it may choose geometry/layout within constraints, but it may not invent mathematical claims.

## Teaching primitives

The registry closes the initial #243 primitive set:

```text
ALIGNED_TRANSFORMATION_STACK
TERM_HIGHLIGHT_VIEW
EQUIVALENCE_BALANCE_VIEW
COORDINATE_PLANE
SLOPE_TRIANGLE_VIEW
CORRECT_WRONG_TRANSFORMATION_CONTRAST
SIDE_BY_SIDE_METHOD_VIEW
ANNOTATED_DERIVATION
INVARIANT_HIGHLIGHT
SUBSTITUTION_CHECK_VIEW
PARALLEL_MEET_CONTRAST
MIRROR_SOLUTION_VIEW
```

Each primitive declares its supported instructional jobs, required source-semantic fields, contrast capability and renderer constraints.

## Representation contract

Every representation instance binds:

```text
semantic_requirement_ref
primitive_id
capability_ref
problem_family_ref?
instructional_job
attention_target
translation_obligation
source_semantic_data
learner_action_expected
misconception_or_contrast_ref?
accessibility_text
renderer_constraints
```

`source_semantic_data` separates declared mathematical claims from renderer payload. The representation cannot satisfy coverage unless it is instructional, capability-bound and tied to a required semantic representation from the lesson/transfer context.

## Current Mathematics vocabulary closure

The page-intent profile provides an explicit primitive route for every representation requirement currently owned by M-D:

```text
NATURAL_LANGUAGE_STATEMENT
ORDERED_PAIR
GEOMETRIC_DISTANCE_RELATION
SYMBOLIC_LINEAR_EQUATION
UNORDERED_PAIR_MODEL
SLOPE_RATIO
ANGLE_RELATION
PARAMETER_CONDITION
SYSTEM_OF_LINEAR_EQUATIONS
CARTESIAN_AXIS_CONSTRAINT
UNIT_RATE
RATE_CONTEXT_MODEL
```

A new M-D representation vocabulary item therefore fails closed in M-H until an explicit page-intent binding is added.

## Cross-cutting obligations

If upstream PCK/StudyModel semantics require `ERROR_CONTRAST`, at least one representation must perform `DISCRIMINATE_CASES`.

If upstream semantics require `VERIFICATION_LOOP` or `VERIFICATION_HABIT`, at least one representation must perform `VERIFY_REASONING`.

This means a decorative or merely related picture cannot discharge a pedagogical obligation.

## Falsifiers

The executable suite blocks:

```text
DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS
VISUAL_WITHOUT_CAPABILITY_BINDING
RENDERER_INVENTS_UNDECLARED_MATH_MEANING
CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED
SOURCE_SEMANTIC_DATA_INCOMPLETE
REPRESENTATION_REQUIREMENT_UNCOVERED
PRIMITIVE_NOT_ALLOWED_FOR_REQUIREMENT
ERROR_CONTRAST_REQUIRED_BUT_NOT_REPRESENTED
VERIFICATION_REPRESENTATION_REQUIRED_BUT_MISSING
TEACHING_PRIMITIVE_REGISTRY_DIGEST_MISMATCH
```

Representative fixtures exercise equality preservation, slope/collinearity, Euclid fifth-postulate transfer and the two valid equilateral-triangle branches.

## Non-claims

This phase does not claim that a particular visual treatment is empirically optimal, does not replace human PCK review required by #242, and does not produce final pages/PDFs. It creates a deterministic semantic contract that downstream publication must obey.
