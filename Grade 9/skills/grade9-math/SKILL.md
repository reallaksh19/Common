---
name: grade9-math
description: Apply Grade 9 Mathematics reasoning, concept fingerprinting, difficulty calibration, solution-path analysis, and misconception logic to source-grounded textbooks and question banks. Use for algebra, number systems, polynomials, sequences and series, geometry, coordinate geometry, statistics/probability, school HOTS, Olympiad foundation, and competitive-foundation mathematics within the Grade 9 learning workflow.
---

# Grade 9 Mathematics

Provide the subject-specific reasoning layer for the shared Grade 9 workflow.

## Mathematical fingerprint

For each anchor/question identify:

- chapter and primary topic;
- secondary topics;
- mathematical mechanism(s);
- hidden structure;
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

The question-bank skill remains authoritative for acceptance/rejection policy.

## Solution-path rule

Record the shortest legitimate expert reasoning path as meaningful steps. Reject same-level candidates that collapse a high-recognition anchor into routine substitution even if the arithmetic is longer.

## Representation strategy

Train recognition of useful representations, for example:

- symmetric AP/GP terms;
- factorized polynomial forms;
- finite differences;
- algebraic substitution;
- coordinate setup;
- auxiliary construction in geometry;
- invariants and symmetry.

## Misconceptions

Capture specific wrong mathematical models, such as sign errors in Vieta, reciprocal-of-sum confusion, treating HP as AP, endpoint attainability errors, or applying a theorem without its conditions.

## Scope discipline

Stay within the intended Grade 9/competitive-foundation scope unless higher-level extension is explicitly labeled. Do not introduce advanced formalism merely because it is elegant.

Use `../grade9-question-bank/SKILL.md` for bank construction and `../grade9-learning-enrichment/SKILL.md` for hints/diagnostics.
