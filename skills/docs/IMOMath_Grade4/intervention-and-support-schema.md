# Grade 4 IMO — Intervention and Support Schema

## Purpose

This document defines the cross-domain learning loop used after an IMO question is attempted. It applies to Mathematical Core, Logical Reasoning, and Everyday Mathematics.

The central rule is:

> Assessment, diagnosis, instruction, reinforcement, and transfer are different evidence objects, even when several of them are presented on one learner-facing help page.

The system may be sophisticated internally, but the learner-facing journey should remain simple.

```text
learner-facing:  ROUND 1 -> HELP -> ROUND 2
internal:        assess -> probe -> teach -> reinforce -> fade -> transfer
```

The Help Book is designed to move the learner toward independence. It is not an answer-explanation booklet and it is not a collection of easier worksheets.

## 1. Distinct object types

### `assessment_item`

Purpose: determine what the learner can do independently before instruction.

Rules:

- no instructional hint;
- no added representation whose purpose is to make the target reasoning easier;
- record whether the answer was independent, guessed, or required help;
- preserve diagrams that are intrinsic to the problem itself.

### `diagnostic_probe`

Purpose: determine whether the nearest prerequisite or atomic reasoning move is independently available.

A diagnostic probe is not a lesson and should not silently teach the target strategy.

Rules:

- keep it short: normally one small check;
- use a reduced-load or prerequisite form of the same underlying idea;
- keep it cue-free before instructional material is revealed;
- use it to distinguish concept/reasoning gaps from transfer, organization, language, or working-memory load;
- do not turn it into a prerequisite worksheet.

### `instructional_activity`

Purpose: make the hidden mathematical or reasoning structure visible after the learner has attempted the probe.

Instruction may include:

- mathematical or reasoning representations;
- worked steps grounded in the original item;
- guided completion;
- externalized clues;
- transformation arrows;
- relation tables;
- concise verbal explanation;
- elimination strategy;
- reduced working-memory demand.

### `reinforcement_item`

Purpose: help the learner reconstruct and then use the same idea with decreasing support.

Two useful levels are:

```text
guided_near_example
independent_near_example
```

These are instructional evidence. Success here does not by itself prove independent mastery.

### `transfer_item`

Purpose: determine whether learning survives after support is removed and the surface form changes.

Rules:

- fresh item, not the original assessment item;
- no helper page visible during the attempt;
- preserve the target skill while varying numbers, context, representation, clue order, or surface features;
- use transfer evidence to distinguish `supported` from `independent`.

## 2. The same-page reinforcement contract

For printable learner support, Part B and Part C should normally be brought onto the same question-grounded page rather than forcing the child to navigate among separate diagnostic and teaching sections.

The page should follow this order:

```text
YOUR QUESTION
    |
    v
QUICK CHECK                    # Part B: cue-free diagnostic probe
    |
    v
STOP / COVER LINE              # prevents accidental preview of teaching
    |
    v
SEE / BUILD THE IDEA           # Part C: teach using the original item
    |
    v
PRACTICE WITH ME               # guided near example
    |
    v
YOUR TURN                      # independent near example
    |
    v
RETRY YOUR ORIGINAL QUESTION
```

This is a presentation composition, not a collapse of the evidence model.

The system should still record the Quick Check separately from the teaching that follows it.

### Why the reveal barrier matters

If the child sees the representation before answering the Quick Check, the probe no longer measures independent prerequisite understanding.

Therefore the printed page should include a strong visual separator such as:

```text
STOP — TRY THE QUICK CHECK BEFORE LOOKING BELOW
```

The adult may physically cover the lower part of the page when useful.

## 3. Question-grounded help

Every help page must remain visibly connected to the exact question that triggered it.

The page should repeat:

- round number;
- question number;
- exact original question;
- exact answer choices when multiple choice.

The instructional block should then work with the same numbers, figures, sequence, directions, clues, or relationships from that question.

Avoid making the learner first solve an unrelated example and infer how it connects back to the original problem.

The original item is the anchor. The guided and independent examples come only after the original structure has been unpacked.

## 4. Part B — Quick Check design

The Quick Check should test the smallest useful prerequisite or atomic move that helps classify the original failure.

Good Quick Checks are:

- short;
- cue-free;
- obviously related after instruction, but not already solved by the instructional picture;
- lower in cognitive load rather than arbitrarily lower in grade level;
- targeted to one plausible bottleneck.

Examples:

```text
original: inclusive count across a large number boundary
quick check: how many whole numbers from 7 through 10, including both ends?

original: multi-turn direction path
quick check: after one right turn from North, which direction are you facing?

original: alternating visual sequence
quick check: what changes from frame 1 to frame 2?

original: constrained digit puzzle
quick check: if tens = 2 and hundreds is twice tens, what is hundreds?
```

The Quick Check is not required to be an easier copy of the original question. It should isolate the suspected reasoning operation.

## 5. Part C — See / Build design

Part C should expose the structure of the original item with the least unnecessary information.

Preferred representations include:

```text
number_line
place_value_chart
digit_slots
interval_diagram
bar_model
array
relation_table
clue_board
ranking_line
direction_arrows
transformation_arrows
mirror_axis
overlay_rotation
sequence_change_marks
elimination_grid
calendar_timeline
```

The representation must do cognitive work. Decoration alone is not support.

The Part C block should answer:

> What was hidden in this question that the learner needed to see, organize, or externalize?

## 6. Reinforcement after Part C

A help page should not end immediately after explaining the original question.

The learner needs a short transition from supported understanding toward independent use.

### `PRACTICE WITH ME`

Use one closely related example with partial structure supplied.

Examples:

- one place-value box already filled;
- one direction arrow already drawn;
- one sequence change already marked;
- one relation-table row completed;
- one impossible choice already crossed out;
- one interval already identified.

### `YOUR TURN`

Use one near-transfer example with the same atomic skill but without the key representation already completed.

Vary only enough surface detail to require reconstruction rather than memorization.

Do not jump directly from a full worked example to an Achievers-level variation.

## 7. Retry the original question

After reinforcement, return the child to the exact original item at the top of the page.

The learner should:

- choose the answer again;
- point to or state the first useful step;
- ideally explain why the selected answer works or why a distractor fails.

This retry is still `supported` evidence because the page was used.

## 8. Round 1 and Round 2 help behavior

### Round 1

Round 1 is the initial clean assessment.

If an item is difficult:

```text
Round 1 item
-> question-grounded help page
-> Quick Check
-> See / Build
-> Practice With Me
-> Your Turn
-> retry original Round 1 item
-> later fresh Round 2 item
```

A fresh unsupported Round 2 success can upgrade evidence toward `independent`.

### Round 2

Round 2 is intended to be a fresh unsupported transfer attempt.

However a Round 2 Help page may still exist for a question the learner cannot solve independently.

If Round 2 help is used:

```text
Round 2 item failed independently
-> Round 2 question-grounded help page
-> reinforcement loop
-> supported success only
-> require another fresh unsupported item later
```

Do not count a Round 2 answer corrected with the Help Book as independent transfer.

The next clean evidence may be a later mixed-retrieval item, a new Round 3 item, or another unseen transfer item generated from the same atomic skill.

## 9. Learner-facing language vs internal schema language

Internal terms should not become navigation burden for a Grade 3–4 learner.

Recommended translation:

| Internal object | Learner-facing language |
|---|---|
| assessment item | ROUND 1 — TRY IT |
| diagnostic probe | QUICK CHECK |
| reveal boundary | STOP — TRY FIRST |
| instructional representation | SEE / BUILD |
| guided reinforcement | PRACTICE WITH ME |
| independent near reinforcement | YOUR TURN |
| original-item reattempt | TRY YOUR QUESTION AGAIN |
| transfer assessment | ROUND 2 — TRY AGAIN |

Avoid learner-facing labels such as `diagnose`, `remediate`, `fade`, `transfer`, `H2`, `T3`, `module family`, `Part B`, or `Part C` unless needed by an adult.

Complexity belongs in the system, not in learner navigation.

## 10. Routing by original question

The learner should navigate by the question they remember, not by an unfamiliar taxonomy.

Example:

```text
Round 1 Q9 difficult -> HELP Round 1 Q9
Round 2 Q6 difficult -> HELP Round 2 Q6
```

The backend may map several questions to the same atomic skill or representation family, but each learner-facing page remains grounded to its triggering item.

Example backend mapping:

```yaml
assessmentItemId: NUM-R1-Q09
helpEntryId: HELP-NUM-R1-Q09
atomicSkills:
  - inclusive_counting
  - identify_counted_object
quickCheckSkill: inclusive_count_small_range
representationFamily: points_vs_intervals
reinforcement:
  guided: NUM-R1-Q09-G1
  independentNear: NUM-R1-Q09-N1
```

## 11. Failure classification before remediation

A wrong answer is evidence, not a diagnosis.

Possible failure classes include:

```text
concept_gap
procedure_gap
rule_not_detected
wrong_rule_selected
representation_misread
operation_selection
constraint_organization
working_memory_load
language_load
transfer_failure
distractor_elimination_failure
careless_execution
guess
unknown
```

The intervention planner should ask:

1. What atomic skill or reasoning move was required?
2. Is that move independently demonstrated elsewhere?
3. What does the Quick Check show?
4. Did the original item add representation, language, constraints, distractors, or multi-step load?
5. Which representation exposes the hidden structure with the least irrelevant information?
6. What closely related guided example will reinforce the move?
7. What near-transfer item can test reconstruction without the full support?
8. What later fresh unsupported item will establish independence?

## 12. Representation is not a difficulty level

A visual cue or representation is an instructional component, not a separate proficiency stage.

Do not use:

```text
wrong answer -> picture -> easier worksheet -> answer
```

as the default architecture.

Difficulty and representation affordance are independent dimensions.

Suggested metadata:

```yaml
difficulty:
  conceptComplexity: 2
  reasoningSteps: 3
  constraintCount: 2
  memoryLoad: medium
  transferDistance: near

representationAffordance: high
preferredRepresentations:
  - interval_diagram
  - clue_board
```

A difficult question may need clue organization rather than a picture. A simpler question may strongly benefit from a number line, arrow path, relation table, or place-value model.

## 13. Fading rule

Within the Help page, fading should be visible across the sequence:

```text
original-item representation: full support
PRACTICE WITH ME: partial support
YOUR TURN: reduced or no supplied representation
later transfer: no support
```

Fading speed depends on evidence.

If the Quick Check is correct and the original failure appears to be organization or transfer load, fade quickly.

If the Quick Check is also wrong, give fuller instruction and a more explicit guided example before reducing support.

## 14. Transfer and evidence states

Suggested interpretation:

```text
Round 1 correct independently
    -> independent evidence

Round 1 wrong; Help page retry correct
    -> supported

Round 1 wrong; Help page succeeds; Round 2 fresh item correct independently
    -> independent

Round 2 wrong; Round 2 Help page retry correct
    -> supported, not independent

Later fresh unseen transfer correct without help
    -> independent

Fresh transfer succeeds across changed form and later mixed retrieval
    -> secure
```

Suggested record:

```yaml
assessment:
  itemId: NUM-R1-Q09
  result: incorrect
  supportUsed: []

helpPage:
  id: HELP-NUM-R1-Q09
  groundedToOriginalItem: true
  quickCheck:
    attemptedBeforeReveal: true
    result: correct
  instruction:
    representation: interval_diagram
    originalItemValuesUsed: true
  reinforcement:
    guidedResult: correct
    independentNearResult: correct
  retryOriginal:
    result: correct
  stateAfter: supported

transfer:
  itemId: NUM-R2-Q06
  result: correct
  supportUsed: []
  stateAfter: independent
```

## 15. Mathematical example — points vs intervals

Ticket labels and marker jumps may look similar while asking for different objects to be counted.

### Ticket labels

```text
38,756 through 39,125, including both ends
```

Part B Quick Check:

```text
How many whole numbers from 7 through 10, including both ends?
```

Part C See / Build:

```text
39,125 - 38,756 = 369 steps
both endpoint labels count
369 + 1 = 370 labels
```

Guided reinforcement uses a smaller inclusive range.

Independent near reinforcement uses a different ticket range.

### Marker jumps

Part B Quick Check:

```text
How many jumps of 1 from 7 to 10?
```

Part C See / Build draws the actual marker sequence and counts spaces/arrows rather than points.

The shared representation family may be `points_vs_intervals`, but each help page stays grounded to its own item.

## 16. Logical Reasoning application

The same-page loop applies to Logical Reasoning, but Part B and Part C must target reasoning operations rather than mathematical prerequisites.

Typical mapping:

```text
YOUR QUESTION
-> QUICK CHECK: isolate one reasoning move
-> SEE / BUILD: annotate the exact original figures/clues
-> PRACTICE WITH ME: same rule with one scaffold
-> YOUR TURN: same atomic skill with changed surface features
-> RETRY ORIGINAL QUESTION
```

Examples of Quick Check targets:

```text
sequence        -> identify what changed between two frames
analogy         -> state the A-to-B relation
classification  -> identify one governing property
coding          -> decode one mapping pair
ranking         -> compare one pair or place one item
方向/direction   -> follow one turn or one move
rotation        -> distinguish turn from mirror
reflection      -> locate the mirror axis
composition     -> identify one component shape
combination     -> apply one constraint
calendar/time   -> perform one shift
```

Part C should mark, trace, align, rotate, connect, or externalize the exact original material rather than replacing it with a generic reasoning lesson.

See `logical-reasoning-reinforcement-schema.md` for domain-specific patterns.

## 17. Helper-book presentation requirements

For printable Grade 3–4 support material:

- one original question per page whenever practical;
- repeat the exact triggering question at the top;
- keep the Quick Check above a strong reveal boundary;
- use large, readable type;
- maintain consistent left alignment and spacing;
- prefer one dominant representation over several decorative visuals;
- use short labels rather than explanatory paragraphs;
- keep answer choices aligned and easy to scan;
- keep guided and independent reinforcement visually distinct;
- preserve whitespace;
- make the route back to the original question obvious;
- do not let the lower teaching section visually leak into the Quick Check area.

The representation must do mathematical or reasoning work. Decoration alone is not support.

## 18. Planner contract

```text
ROUND 1 assessment
        |
        v
independent success? ---- yes ---> record evidence; no help needed
        |
        no
        v
open question-grounded HELP page
        |
        v
QUICK CHECK before reveal
        |
        v
classify likely bottleneck
        |
        v
SEE / BUILD original question
        |
        v
PRACTICE WITH ME
        |
        v
YOUR TURN
        |
        v
retry original item
        |
        v
later ROUND 2 fresh transfer
        |
        +-- independent success -> independent evidence
        |
        +-- failure -> optional Round 2 HELP page -> supported only
                                      |
                                      v
                              later unseen transfer
```

## 19. Non-goals

This schema does not:

- turn every difficult question into a picture;
- use the hardest percentage of questions as an automatic visual-support set;
- treat a visual cue as a diagnostic probe;
- assume a wrong Olympiad item means the underlying concept or reasoning family is weak;
- send the learner through long prerequisite worksheets by default;
- expose internal routing codes as learner navigation;
- require an unrelated warm-up before explaining the question the learner actually missed;
- stop after explaining the answer without reinforcement;
- count a Help-page retry as independent mastery;
- count a Round 2 correction made with help as successful independent transfer.
