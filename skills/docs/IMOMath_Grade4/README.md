# IMO Mathematics Grade 4 - Learning Schema

This folder defines the learning architecture for Grade 4 IMO preparation, especially for a learner bridging from Grade 3 into Grade 4 work.

## Core principle

Do not model the learner as:

`exam section -> chapter -> easy/medium/hard worksheet`

Separate:

1. **Mathematical Core** - mathematical concepts and skills.
2. **Logical Reasoning** - reusable reasoning capabilities.
3. **Everyday Mathematics** - application/transfer structures that reference Mathematical Core skills.

`Achievers` is a higher-demand mode, not a separate curriculum.

## Two rounds with different jobs

Round 1 and Round 2 must not use the same question-order policy.

### Round 1 - CLIMB THE LADDER

Round 1 is a structured learning bridge, not an exam simulation.

Questions are grouped into short concept clusters:

```text
familiar Grade 3 rung
-> direct Grade 4 extension
-> Grade 4 application / one extra reasoning demand
```

Neighboring questions should be conceptually similar enough that the learner can reuse a method and experience progress.

If a rung is difficult, the exact question changes role:

```text
question attempt
-> LET'S WORK THIS ONE OUT TOGETHER
-> same question becomes a partial worked example
-> optional small diagnostic check only if needed
-> child completes a key step
-> close new question
-> continue the cluster
```

Once converted to an example, the original question is `instructionally_exposed` and can no longer prove independent mastery.

### Round 2 - MIX IT UP

Round 2 is mixed pre-IMO transfer.

Concept families are shuffled, cluster headings disappear, and the learner must recognize which idea to use.

Round 2 should:

- mix previous- and current-class retrieval;
- contain mostly Grade 4 core and pre-IMO application;
- use plausible distractors;
- vary wording and surface form;
- provide no instructional representation;
- include only a small amount of higher-demand material unless explicitly building an Achievers round.

A Round 2 item solved after opening help is `supported`, not `independent`. A later unseen item is required.

## Question-to-example conversion

A difficult question is not merely followed by an explanation. The difficult question itself becomes the instructional example.

Preferred child-facing wording:

```text
LET'S WORK THIS ONE OUT TOGETHER
We'll find the first step, then you can finish it.
```

Preferred page flow:

```text
YOUR QUESTION
-> LET'S WORK THIS ONE OUT TOGETHER
-> optional: IF THIS PART IS HARD...
-> SEE IT THIS WAY
-> YOUR STEP
-> TRY ONE
```

The original numbers, figures, sequence, path, clues, and answer choices remain visible so the learner does not have to infer how a separate example connects back.

The worked example should usually be partial: expose enough structure to make the next thinking step achievable, then give responsibility back to the learner.

See `intervention-and-support-schema.md`.

## Quick Check is conditional

Do not force a diagnostic probe onto every help page.

Use a small cue-free check only when the failure path is ambiguous and the result will change what is taught.

If the prerequisite is already independently demonstrated elsewhere, teach the actual missing structure directly.

## Number Sense bridge

For Numbers / Number Sense, use the dedicated Grade 3 -> Grade 4 bridge in `number-sense-bridge-schema.md`.

The Class 3 -> Class 4 transition is especially suited to clustered Round 1 design:

```text
4-digit understanding
-> larger-number extension
-> reasoning/application
```

Recommended clusters include:

- place value and representation;
- comparing and ordering;
- forming numbers under rules;
- rounding;
- Roman numerals;
- number names as an optional bridge when needed.

Factors and Multiples should remain a separate mathematical cluster/chapter rather than being silently mixed into Number Sense.

## Logical Reasoning adaptation

The same conversion rule applies to Logical Reasoning.

If a reasoning item is difficult, teach from the exact original material:

```text
sequence       -> mark the first change; child checks/repeats it
analogy        -> expose A-to-B relation; child applies it to C
coding         -> reveal one original mapping; child completes the table
ranking        -> place one original clue; child places the next
方向/direction -> draw the first move/turn; child completes the path
rotation       -> trace the first transformation; child applies the next
reflection     -> show the original mirror axis; child predicts the image
```

The objective is a reusable reasoning routine, not answer revelation.

See `logical-reasoning-schema.md` and `logical-reasoning-reinforcement-schema.md`.

## Learner evidence

Avoid chapter-level percentages as the primary evidence model.

Track states such as:

- `unknown`
- `needs_instruction`
- `supported`
- `independent`
- `secure`

Also track:

- initial unsupported result;
- guessed / needed help;
- whether the original item was converted to a worked example;
- whether a diagnostic probe was used;
- representation used;
- child-completed step;
- guided reinforcement result;
- near-independent result;
- fresh transfer result;
- failure mode;
- ability to explain the first useful step.

A converted original item is burned for independent evidence.

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
- unit/conversion load.

Difficulty is separate from `representationAffordance`.

Do not automatically add a picture to the hardest questions. Use a representation only when it exposes useful structure.

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
              ROUND 1 CLUSTERS
                        |
        independent? / convert-to-example
                        |
                faded close practice
                        |
               ROUND 2 MIXED TRANSFER
                        |
          independent / supported / later retry
                        |
                Olympiad / Achievers
```

## Documents

- `intervention-and-support-schema.md` - question-to-example conversion, optional probing, fading and evidence rules.
- `number-sense-bridge-schema.md` - Grade 3 -> Grade 4 Number Sense clusters and Round 1 / Round 2 generation contract.
- `logical-reasoning-schema.md` - Logical Reasoning capability model.
- `logical-reasoning-reinforcement-schema.md` - question-grounded reasoning reinforcement patterns.
- `everyday-mathematics-schema.md` - application/transfer schema.

## Printable-material principle

For learner-facing material:

- use child-friendly labels;
- keep one dominant idea per page or cluster;
- use large readable type and consistent alignment;
- preserve whitespace;
- keep explanations short and spatially close to the relevant question step;
- require the child to complete something inside a worked example;
- keep a close new item after the example;
- avoid exposing internal terms such as `diagnostic_probe`, `fade`, `transfer`, `Part B`, or skill IDs.

Complexity belongs in the system, not in the child's navigation.
