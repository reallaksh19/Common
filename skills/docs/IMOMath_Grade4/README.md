# IMO Mathematics Grade 4 — Learning Schema

This folder defines the learning architecture for Grade 4 IMO preparation, especially for a learner transitioning from secure Grade 3 mathematics into Grade 4 Olympiad work.

## Core principle

Do not model the learner as:

`exam section -> chapter -> easy/medium/hard worksheet`

Instead separate three kinds of truth:

1. **Mathematical Core** — concepts and mathematical skills such as number sense, operations, fractions, geometry and measurement.
2. **Logical Reasoning** — an independent reasoning-capability graph.
3. **Everyday Mathematics** — an application/transfer layer that references Mathematical Core skills rather than duplicating them.

`Achievers` is not a fourth curriculum. It is a higher cognitive-demand mode applied to existing mathematical or reasoning skills.

## Grade 3 -> Grade 4 bridge principle

Use challenge-first diagnosis:

`transition/core probe -> locate boundary -> probe downward only when needed -> teach missing micro-skill -> transfer -> Olympiad application -> Achievers`

Do not start all learners with low-level prerequisite questions. Easier items should normally remain fallback probes.

## Learner evidence

Avoid chapter-level scores such as `Numbers = 58%` or `Logical Reasoning = 62%` as the primary model.

Track evidence at atomic-skill and question-archetype level using states such as:

- `unknown`
- `needs_instruction`
- `supported`
- `independent`
- `secure`

Also track:

- support used;
- representation dependence;
- transfer success;
- failure mode;
- reasoning/cognitive load;
- whether the learner can explain the method.

## Difficulty model

Difficulty is multidimensional. A question may vary independently in:

- concept complexity;
- reasoning steps;
- number of simultaneous constraints;
- representation;
- distractor similarity;
- language load;
- memory load;
- transfer distance;
- information load;
- unit/conversion load.

A single scalar `difficulty = 3` is insufficient as the underlying schema.

## Documents

- `logical-reasoning-schema.md` — independent reasoning-capability model for IMO Logical Reasoning.
- `everyday-mathematics-schema.md` — application/transfer model for Everyday Mathematics.

## Architecture

```text
                    IMO Exam Blueprint
                           |
         ---------------------------------------
         |                  |                  |
 Mathematical Core   Logical Reasoning    Application Schema
         |                  |                  |
     skill graph        reasoning graph      problem schemas
         |                  |                  |
         -------- Learner Evidence -----------
                           |
                     Bridge Planner
                           |
         --------------------------------
         |              |               |
     instruction     transfer        challenge
                                     /Achievers
```

The bridge planner should determine whether a learner lacks the underlying mathematics, lacks the reasoning structure, or knows both but cannot transfer them into an Olympiad-style question. Those cases must not receive the same remediation.
