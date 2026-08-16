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

Use challenge-first diagnosis, but keep assessment, diagnosis, instruction and transfer as different object types.

Internal learning loop:

`assessment -> diagnose when needed -> teach missing structure -> fade support -> transfer -> Olympiad application -> Achievers`

Learner-facing loop:

`ROUND 1 -> HELP -> ROUND 2`

Do not start all learners with low-level prerequisite questions. Easier items should normally remain fallback diagnostic probes, used only when the failure path is ambiguous.

A wrong question is evidence, not a diagnosis. Before remediation, determine whether the learner lacks the underlying skill, cannot organize the information, is overloaded by language/working memory, or fails only when the skill is transferred into an unfamiliar Olympiad form.

## Assessment and intervention objects

The schema distinguishes:

- `assessment_item` — clean independent attempt before instruction;
- `diagnostic_probe` — minimal cue-free probe used only to classify an ambiguous failure;
- `instructional_activity` — teaching, representation, worked example or strategy support;
- `transfer_item` — fresh unsupported item used after teaching to test independence.

A visual cue is not a diagnostic level. A mathematical representation is an instructional component that should be used only when it exposes the relevant mathematical or reasoning structure.

See `intervention-and-support-schema.md` for the full cross-domain contract.

## Question-grounded help

When a learner needs help, the child-facing material should remain visibly tied to the question that triggered it.

Preferred page pattern:

`YOUR QUESTION -> LOOK AT THIS QUESTION THIS WAY -> TRY YOUR QUESTION AGAIN`

The helper page should repeat the original question number, exact question and answer choices before unpacking the same numbers, clues or relationships.

The backend may map several items to one skill or representation family, but the child should navigate by the question they remember rather than by internal module IDs.

Internal labels such as `diagnose`, `fade`, `transfer`, `T3` or `H5` should not become learner-facing navigation burden.

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
- whether the learner can explain the method;
- whether the answer was independent, guessed or completed with help;
- whether a diagnostic probe was necessary before instruction.

Success on a helper page with a supplied representation is normally `supported`, not `independent`. Fresh unsupported transfer is required before upgrading the evidence state.

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

Difficulty is also separate from `representationAffordance`. Do not automatically give visual support to a fixed percentage of the hardest questions. Some hard questions need clue organization rather than a picture; some simpler questions strongly benefit from a number line, place-value chart, array, interval diagram or bar model.

## Documents

- `logical-reasoning-schema.md` — independent reasoning-capability model for IMO Logical Reasoning.
- `everyday-mathematics-schema.md` — application/transfer model for Everyday Mathematics.
- `intervention-and-support-schema.md` — cross-domain assessment, diagnosis, question-grounded help, representation, fading and transfer contract.

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
          -----------------------------------
          |                |                |
     assessment        diagnosis        instruction
       ROUND 1          if needed           HELP
          |                                  |
          |                              fade support
          |                                  |
          ---------------- transfer ----------
                         ROUND 2
                           |
                  Olympiad / Achievers
```

The bridge planner should determine whether a learner lacks the underlying mathematics, lacks the reasoning structure, cannot organize multiple constraints, is overloaded by representation/language/working memory, or knows the skill but cannot transfer it into an Olympiad-style question. Those cases must not receive the same remediation.

## Printable-material principle

For learner-facing support pages:

- repeat the exact triggering question;
- keep one dominant mathematical idea per page;
- use large readable type and consistent alignment;
- prefer one useful representation over decorative visuals;
- keep explanations short and spatially close to the relevant part of the question;
- preserve whitespace;
- make the route back to the original question obvious.

The representation must do mathematical work. Decoration alone is not support.
