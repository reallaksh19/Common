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

Use challenge-first diagnosis, but keep assessment, diagnostic evidence, instruction, reinforcement and transfer as different object types.

Internal learning loop:

`assessment -> probe -> teach -> reinforce -> fade -> transfer -> Olympiad application -> Achievers`

Learner-facing loop:

`ROUND 1 -> HELP -> ROUND 2`

Do not start all learners with low-level prerequisite questions. A wrong question is evidence, not a diagnosis. Determine whether the learner lacks the underlying skill/reasoning move, cannot organize the information, is overloaded by language/working memory, or fails only when the skill is transferred into an unfamiliar Olympiad form.

## Assessment and intervention objects

The schema distinguishes:

- `assessment_item` — clean independent attempt before instruction;
- `diagnostic_probe` — minimal cue-free check of the nearest prerequisite or atomic reasoning move;
- `instructional_activity` — teaching, representation, worked step or strategy support;
- `reinforcement_item` — guided and near-independent practice used to fade support;
- `transfer_item` — fresh unsupported item used to test independence.

A visual cue is not a diagnostic level. A mathematical or reasoning representation is an instructional component used when it exposes the relevant structure.

See `intervention-and-support-schema.md` for the full cross-domain contract.

## One-page reinforcement Help Book

The Help Book is designed to make the learner progressively independent, not merely explain the answer.

For each Round 1 or Round 2 question that needs support, use one question-grounded page:

```text
YOUR QUESTION
    |
    v
QUICK CHECK                 # internal Part B
    |
    v
STOP — TRY FIRST
    |
    v
SEE / BUILD                 # internal Part C
    |
    v
PRACTICE WITH ME
    |
    v
YOUR TURN
    |
    v
TRY YOUR ORIGINAL QUESTION AGAIN
```

The page repeats the original question number, exact question and answer choices. The Quick Check remains above a reveal boundary so it retains diagnostic value. The teaching block then works with the same numbers, figures, clues or relationships from the original item.

The guided example and independent near example reinforce the same atomic skill before the learner retries the original question.

Child-facing material should not use labels such as `Part B`, `Part C`, `diagnose`, `fade`, `transfer`, `T3` or `H5`.

## Round 2 evidence rule

Round 2 is first attempted as a clean transfer assessment.

If the learner needs the Round 2 Help page, the corrected answer is `supported`, not `independent`.

A later unseen item without help is required to establish independent transfer.

```text
Round 2 independent success -> independent evidence
Round 2 + Help success       -> supported evidence
later unseen success         -> independent evidence
```

## Logical Reasoning adaptation

The same Help Book architecture applies to Logical Reasoning, but the Quick Check normally probes an **atomic reasoning move** rather than a mathematical prerequisite.

Examples:

```text
sequence       -> what changed between two frames?
analogy        -> what is the A-to-B relation?
coding         -> decode one mapping pair
ranking        -> place one relative pair
direction      -> follow one turn
rotation       -> turn or mirror?
reflection     -> identify the mirror axis
composition    -> identify one component shape
combination    -> apply one constraint
time/calendar  -> perform one shift
```

The `SEE / BUILD` block should annotate the original reasoning material: mark sequence changes, draw the original direction arrows, place original ranking clues into slots, trace a rotation, show a mirror axis, create a relation table from the original code, or eliminate original choices using the governing rule.

See `logical-reasoning-reinforcement-schema.md` for the domain-specific page patterns.

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
- Quick Check result;
- whether the Quick Check was attempted before reveal;
- guided reinforcement result;
- independent near-reinforcement result;
- original-item retry result;
- transfer success;
- failure mode;
- reasoning/cognitive load;
- whether the learner can explain the first useful step;
- whether the original answer was independent, guessed or completed with help.

Success on a Help page is normally `supported`, not `independent`. Fresh unsupported transfer is required before upgrading the evidence state.

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

Difficulty is also separate from `representationAffordance`. Do not automatically give visual support to a fixed percentage of the hardest questions. Some hard questions need clue organization rather than a picture; some simpler questions strongly benefit from a number line, transformation arrow, place-value chart, interval diagram, relation table or ranking line.

## Documents

- `logical-reasoning-schema.md` — independent reasoning-capability model for IMO Logical Reasoning.
- `logical-reasoning-reinforcement-schema.md` — question-grounded Quick Check / See-Build / reinforcement patterns for Logical Reasoning.
- `everyday-mathematics-schema.md` — application/transfer model for Everyday Mathematics.
- `intervention-and-support-schema.md` — cross-domain assessment, same-page reinforcement, question-grounded help, fading and transfer contract.

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
               ROUND 1 clean assessment
                           |
                     HELP if needed
                           |
        --------------------------------------
        |          |          |              |
   Quick Check  See/Build  Guided Practice  Your Turn
        --------------------------------------
                           |
                    retry original
                           |
                   ROUND 2 transfer
                           |
              independent? / help again
                           |
                  later unseen transfer
                           |
                  Olympiad / Achievers
```

The bridge planner should determine whether a learner lacks the underlying mathematics, lacks the atomic reasoning move, cannot organize multiple constraints, is overloaded by representation/language/working memory, is misled by distractors, or knows the skill but cannot transfer it into an Olympiad-style question. Those cases must not receive the same intervention.

## Printable-material principle

For learner-facing support pages:

- repeat the exact triggering question;
- keep the Quick Check above a clear reveal boundary;
- use one main mathematical/reasoning idea per page;
- use large readable type and consistent alignment;
- prefer one useful representation over decorative visuals;
- keep explanations short and spatially close to the relevant part of the question;
- distinguish guided practice from independent near practice;
- preserve whitespace;
- make the route back to the original question obvious.

The representation must do mathematical or reasoning work. Decoration alone is not support.
