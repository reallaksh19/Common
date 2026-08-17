# IMO Mathematics Grade 4 - Learning Schema

This folder defines the learning architecture for Grade 4 IMO preparation, including both Grade 3 -> Grade 4 bridge work and Grade 4 -> pre-IMO transfer.

## Core principle

Do not model the learner as:

`exam section -> chapter -> easy/medium/hard worksheet`

Separate:

1. **Mathematical Core** - concepts and mathematical skills.
2. **Logical Reasoning** - reusable reasoning capabilities.
3. **Everyday Mathematics** - application structures that reference the Mathematical Core.

`Achievers` is a higher-demand mode, not a separate curriculum.

## Round 1 and Round 2 have different jobs

Round 1 teaches and strengthens thinking tools. Round 2 tests whether the learner can recognize those tools when the surface cues disappear.

### Round 1 - build the thinking tools

Round 1 is intentionally sequenced, not randomized.

Two valid modes exist.

#### Bridge mode

For Grade 3 -> Grade 4 transition:

```text
familiar prerequisite
-> direct Grade 4 extension
-> one extra reasoning demand
```

Tight clusters are useful because the learner can reuse a method while only one demand changes.

#### Grade 4 pre-IMO mode

Once enough Grade 4 core is present, avoid teaching with repetitive near-copy templates.

Use a curated progression of different question archetypes that share a compact conceptual backbone.

For Number Sense this may include:

- place-value magnitude;
- flexible regrouping;
- missing-digit inequalities;
- distance / equal spacing;
- number-boundary continuity;
- rounding intervals;
- Roman numeral operations;
- parity reasoning;
- equality / balance;
- systematic enumeration;
- clue / constraint organization.

Conceptual continuity remains, but surface repetition is reduced.

### Round 2 - deliberately interleaved transfer

Round 2 is mixed, but not random in the loose sense.

It should require the learner to decide:

> What kind of structure is hidden here, and what tool could help me?

Rules:

- concept labels disappear;
- question forms change relative to Round 1;
- families are interleaved;
- obvious near-copies are avoided;
- no instructional representation is supplied;
- the learner may create their own number line, place-value columns, digit slots, list, case table, clue board, or balance model;
- plausible distractors reflect real misconceptions;
- most items remain Grade 4 core / pre-IMO unless an Achievers round is explicitly intended.

## Question-to-example conversion

If a question is difficult, that exact question changes role.

```text
question attempt
-> LET'S WORK THIS ONE OUT TOGETHER
-> same question becomes a partial worked example
-> optional small diagnostic check only if needed
-> SEE IT THIS WAY
-> child completes a key step
-> TRY ONE: fresh close question
```

Once converted, the original is `instructionally_exposed` and can no longer prove independent mastery.

Preferred child-facing wording:

```text
LET'S WORK THIS ONE OUT TOGETHER
We'll find the first step, then you can finish it.
```

See `intervention-and-support-schema.md`.

## Quick Check is conditional

Do not force a diagnostic probe onto every Help page.

Use a small cue-free check only when the failure path is ambiguous and the result will change what is taught.

## Learner-created representations

A major transfer goal is the shift from:

```text
teacher supplies the representation
```

to:

```text
learner recognizes the structure
-> learner chooses / draws a useful representation
```

This is positive evidence, not a sign that the learner failed to work mentally.

Examples:

- drawing an equal-spacing number line;
- aligning place values;
- building digit boxes from clues;
- listing valid cases systematically;
- drawing balance bars;
- crossing out candidates that violate a condition.

Suggested evidence:

```yaml
selfGeneratedRepresentation:
  used: true
  type: clue_board
  appropriate: true
  promptedByAdult: false
```

## Round 2 Help rule

Round 2 must first be attempted cleanly.

An optional Help Book may exist afterward.

If Round 2 Help is opened:

```text
Round 2 item
-> converted to worked example
-> supported learning
-> fresh close item
-> later unseen transfer required
```

A corrected Round 2 answer after Help is `supported`, not `independent`.

## Number Sense

See `number-sense-bridge-schema.md` for the full Number Sense contract.

It now covers:

- Grade 3 -> Grade 4 clustered bridge mode;
- Grade 4 pre-IMO varied-archetype Round 1;
- deliberately interleaved Round 2;
- self-generated representation evidence;
- optional Round 2 Help behavior;
- distractor and archetype guidance.

Factors and Multiples remains a separate mathematical topic family rather than being silently mixed into a Number Sense-only set.

## Logical Reasoning adaptation

The same architecture applies to Logical Reasoning.

Do not build transfer by showing ten surface copies of one reasoning puzzle.

Preserve the reasoning capability while varying the surface form:

```text
sequence       -> detect transformation -> apply to changed symbols
analogy        -> relation recognition -> changed representation
coding         -> mapping -> reverse / partial mapping
ranking        -> pairwise relation -> multi-clue order
direction      -> one turn -> changed path
rotation       -> transform -> distinguish from reflection
combination    -> one constraint -> systematic elimination
```

If a question is difficult, teach from the exact original figures or clues and hand one step back to the learner.

See `logical-reasoning-schema.md` and `logical-reasoning-reinforcement-schema.md`.

## Learner evidence

Primary evidence states:

- `unknown`
- `needs_instruction`
- `supported`
- `independent`
- `secure`

Track:

- initial unsupported result;
- guessed / needed help;
- whether the original became a worked example;
- diagnostic probe use;
- supplied representation;
- learner-generated representation;
- child-completed step;
- close-practice result;
- mixed transfer result;
- failure mode;
- ability to explain the first useful step.

Key rules:

```text
converted original -> supported
fresh close item -> near-independent at best
unseen Round 2 success without Help -> independent transfer
unseen Round 2 success using a self-generated appropriate representation -> independent transfer + positive strategy evidence
Round 2 success after Help -> supported
later retained mixed success -> secure
```

## Difficulty model

Difficulty is multidimensional. Track dimensions such as:

- concept complexity;
- reasoning steps;
- simultaneous constraints;
- representation;
- distractor similarity;
- language load;
- memory load;
- transfer distance;
- information load;
- question-archetype novelty.

Difficulty is separate from `representationAffordance`.

Do not automatically add a picture to the hardest questions. Use a representation when it exposes structure; in later transfer, allow the learner to decide whether to create it.

## Architecture

```text
                 IMO Exam Blueprint
                        |
        ---------------------------------
        |               |               |
 Mathematical Core  Logical Reasoning  Application
        |               |               |
        -------- Learner Evidence -------
                        |
                  Bridge Planner
                        |
                 ROUND 1
          bridge ladder / pre-IMO progression
                        |
        independent? / convert-to-example
                        |
                 fresh close item
                        |
             ROUND 2 INTERLEAVED TRANSFER
                        |
       recognize structure + select strategy
                        |
      independent / supported / later unseen
                        |
                Olympiad / Achievers
```

## Documents

- `intervention-and-support-schema.md` - conversion, partial worked examples, fading, interleaved transfer, representation evidence, and support rules.
- `number-sense-bridge-schema.md` - bridge and pre-IMO Number Sense generation contract.
- `logical-reasoning-schema.md` - Logical Reasoning capability model.
- `logical-reasoning-reinforcement-schema.md` - question-grounded reasoning reinforcement patterns.
- `everyday-mathematics-schema.md` - application / transfer schema.

## Printable-material principle

For learner-facing material:

- use child-friendly labels;
- keep initial attempts free of instructional hints;
- preserve whitespace for learner-created work;
- keep explanations short and spatially close to the relevant step;
- require the learner to complete something inside a worked example;
- include a fresh close question after support;
- keep Round 2 concept labels hidden;
- avoid exposing internal terms such as `diagnostic_probe`, `fade`, `transfer`, or skill IDs.

Complexity belongs in the system, not in the child's navigation.
