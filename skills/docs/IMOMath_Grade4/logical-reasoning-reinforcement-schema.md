# Grade 4 IMO — Logical Reasoning Reinforcement Schema

## Purpose

This document applies the shared question-grounded reinforcement loop to Logical Reasoning.

It extends `logical-reasoning-schema.md` and follows the cross-domain contract in `intervention-and-support-schema.md`.

The learner-facing page remains simple:

```text
YOUR QUESTION
-> QUICK CHECK
-> SEE / BUILD
-> PRACTICE WITH ME
-> YOUR TURN
-> TRY YOUR QUESTION AGAIN
```

Internally, these are different evidence stages:

```text
assessment_item
-> atomic_reasoning_probe
-> instructional_representation
-> guided_reinforcement
-> independent_near_reinforcement
-> original_item_retry
-> later_fresh_transfer
```

A help page is designed to help the learner reconstruct a reasoning process independently. It should not merely reveal the correct option.

## 1. Core Logical Reasoning rule

For mathematics, Part B often probes a prerequisite calculation or concept.

For Logical Reasoning, Part B should usually probe the **atomic reasoning move** embedded inside the original item.

Examples:

```text
sequence question
-> can the learner identify what changes between two frames?

analogy question
-> can the learner state or select the A-to-B relation?

direction question
-> can the learner follow one turn correctly?

rotation question
-> can the learner distinguish rotation from reflection?

ranking question
-> can the learner place one relative pair correctly?

coding question
-> can the learner decode one mapping pair?
```

The objective is not to make the question easier in a generic sense. The objective is to isolate the smallest reasoning operation whose failure would explain the original miss.

## 2. Question-grounded page contract

Each Logical Reasoning help page should repeat:

- round number;
- question number;
- exact original figures, symbols, clues, sequence, or diagram;
- exact answer choices.

The learner should never have to infer which generic reasoning lesson applies.

The `SEE / BUILD` section must annotate the original material whenever possible.

Examples:

- mark what changes between the original sequence frames;
- draw the original direction path with arrows;
- place the original ranking clues onto position slots;
- draw the mirror axis on the original figure;
- trace the rotation on the original shape;
- write the original coding pairs into a relation table;
- cross out original distractors using the governing rule.

## 3. Sequence reasoning — LR-SEQ

### Typical original tasks

```text
next_element
missing_element
incorrect_element
alternating_sequence
growing_sequence
```

### Quick Check

Probe one local observation rather than asking another full sequence question.

Examples:

```text
What changed from frame 1 to frame 2?
Which two positions repeat?
Does the arrow turn clockwise or anticlockwise?
Which attribute changes: shape, number, position, or direction?
```

### See / Build

Annotate the original sequence.

Useful supports:

```text
highlight_change
mark_repeating_unit
number_positions
split_alternating_sequences
transformation_arrows
```

Example:

```text
frame 1 -> frame 2 -> frame 3 -> frame 4
   +1 side    +1 side    +1 side
```

or:

```text
odd positions:  1, 3, 5
                 one rule

even positions: 2, 4, 6
                 second rule
```

### Practice With Me

Use a very close sequence where one change arrow or repeating unit is already marked.

### Your Turn

Use the same atomic rule with changed shapes/numbers and no supplied markings.

### Evidence distinction

If the Quick Check is correct but the original multi-rule sequence failed, prefer failure labels such as:

```text
misses_alternating_structure
working_memory_overload
multi_rule_tracking_failure
```

rather than `sequence_skill_weak`.

## 4. Analogy — LR-ANA

### Quick Check

Ask for the relation between the first pair only.

```text
A -> B: what changed?
```

Possible relation types:

```text
rotate
reflect
increase_count
decrease_count
swap_position
change_fill
add_component
remove_component
number_operation
symbol_mapping
```

### See / Build

Draw an explicit transformation arrow over the original A:B pair, then apply the same arrow to C.

```text
A --rotate 90°--> B
C --same move---> ?
```

### Practice With Me

Supply the transformation label and let the learner apply it to a new simple pair.

### Your Turn

Remove the label and use a new pair that preserves the same relation.

Do not teach analogy as surface matching.

## 5. Classification — LR-CLS

### Quick Check

Ask the learner to name or select one property shared by two obvious members.

```text
What do these two have in common?
```

### See / Build

Create a small property table from the original choices.

```text
choice   sides   shaded   orientation   follows rule?
A        4       yes      up            yes
B        4       yes      up            yes
C        3       yes      up            no
```

### Practice With Me

Complete one row together.

### Your Turn

Give a new set where the same governing property must be found without the table completed.

Avoid teaching `odd one out` as visual dissimilarity. The target is the governing property.

## 6. Coding and decoding — LR-COD

### Quick Check

Probe one mapping pair.

```text
If A -> D, what shift happened?
If CAT -> DBU by +1 letters, what does C become?
```

### See / Build

Use a relation table grounded to the original code.

```text
original   coded   change
A          D       +3
B          E       +3
C          F       +3
```

For symbol substitution, use direct mapping boxes.

For reverse mapping, show the arrow direction explicitly.

### Practice With Me

Complete one missing row.

### Your Turn

Decode a fresh word/symbol expression using the same rule without the completed table.

Distinguish:

```text
mapping_unknown
rule_detection_failure
reverse_mapping_error
multi_symbol_tracking_failure
```

## 7. Ordering and ranking — LR-RNK

### Quick Check

Reduce the original clue set to one pair.

```text
Mira is ahead of Riya. Who is earlier?
A is taller than B. Which one goes higher?
```

### See / Build

Externalize the exact original clues onto a line or slots.

```text
1st   2nd   3rd   4th   5th
[ ]   [ ]   [ ]   [ ]   [ ]
```

Add one clue at a time.

Use arrows for relative relations:

```text
A > B
C < B
```

### Practice With Me

Provide a partially filled ranking line.

### Your Turn

Use new names but the same number of relational steps.

If the learner handles pairwise comparisons but fails the original item, record clue coordination or working-memory load rather than basic comparison weakness.

## 8. Direction reasoning — LR-DIR

### Quick Check

Probe one movement or one turn.

Examples:

```text
Facing North, turn right. Which direction now?
Move 2 steps East. Where are you relative to the start?
```

### See / Build

Draw the exact original path.

Use:

```text
start_dot
direction_arrows
turn_marks
step_numbers
final_position_marker
```

The child should see each state change rather than hold the full route mentally.

### Practice With Me

Give a similar route with the first arrow already drawn.

### Your Turn

Give a new route with no arrows supplied.

Possible evidence split:

```text
single_turn: independent
multi_turn_tracking: supported
final_relative_position: supported
```

## 9. Spatial transformation — LR-SPA

### Quick Check

Probe the transformation identity.

```text
Did the figure turn or flip?
Which way did it rotate?
Where would the mirror line be?
```

### See / Build

Use the original figures with one dominant support:

```text
overlay_rotation
rotation_arrow
mirror_axis
corner_anchor
orientation_marker
```

Avoid adding many decorative arrows or colors that do not encode the transformation.

### Practice With Me

Supply one anchor point or rotation arrow.

### Your Turn

Use a new shape/orientation with no supplied overlay.

Distinguish:

```text
rotation_direction_error
rotation_amount_error
reflection_confusion
viewpoint_change_error
```

## 10. Visual composition — LR-CMP

### Quick Check

Ask the child to identify one component shape or trace one small segment.

### See / Build

Work directly on the original figure:

- trace boundaries;
- mark shared edges;
- separate overlapping parts;
- identify anchor corners;
- cross out options missing a required component.

### Practice With Me

Partially trace one component.

### Your Turn

Use a new composition where the child must find the same part-whole relation independently.

The visual support should clarify structure, not redraw the problem into an unrelated picture.

## 11. Combination reasoning — LR-COM

### Quick Check

Probe one constraint.

```text
If red cannot sit next to blue, is this pair allowed?
```

### See / Build

Use the exact original choices with a possibility grid or elimination table.

```text
option   rule 1   rule 2   possible?
A        yes      no       no
B        yes      yes      yes
```

### Practice With Me

Complete one row together.

### Your Turn

Use a new small arrangement with the same constraint structure.

Teach systematic elimination before exhaustive guessing.

## 12. Temporal reasoning — LR-TMP

### Quick Check

Probe one shift.

```text
3 days after Monday = ?
20 minutes after 4:30 = ?
```

### See / Build

Use the original clock/calendar/time clues with a timeline, marked calendar row, or clock arc.

### Practice With Me

Supply the first shift.

### Your Turn

Use a new time/date with the same direction and interval structure.

## 13. Mixed reasoning — LR-MIX

Do not create a generic mixed Help page.

First identify the dominant atomic move and the secondary load.

Example:

```text
original: multi-clue ranking with coded symbols
primary: ranking
secondary: decoding
```

The Quick Check should normally test the primary bottleneck first.

If both component moves are independently secure, Part C should focus on coordination/externalization rather than reteaching either component.

## 14. Distractor-aware reinforcement

Olympiad Logical Reasoning often uses distractors that preserve surface similarity while violating one rule.

The `SEE / BUILD` block may therefore use option elimination as a reasoning representation.

Example:

```text
A: correct rotation, wrong shading     -> cross out
B: wrong rotation, correct shading     -> cross out
C: correct rotation + correct shading  -> keep
D: mirror image                        -> cross out
```

This is not test-taking trickery when each elimination is tied to the governing rule.

Record whether the learner can explain why an option is impossible.

## 15. Fading in Logical Reasoning

A useful support sequence is:

```text
SEE / BUILD
  original figure fully annotated

PRACTICE WITH ME
  one transformation / clue / arrow supplied

YOUR TURN
  no supplied annotation

fresh transfer
  changed figures or symbols, no helper visible
```

For a learner whose atomic move is already secure, skip unnecessary low-level repetition and fade quickly.

## 16. Representation affordance

Logical Reasoning is often visual, but `visual question` does not mean `more pictures = more help`.

Representations should externalize the reasoning operation.

Useful metadata:

```yaml
representationAffordance: high
supportRepresentation:
  type: transformation_arrows
  purpose: externalize_rotation_rule
```

Bad support:

```yaml
supportRepresentation:
  type: decorative_image
  purpose: make_page_fun
```

The latter should not be treated as instructional support.

## 17. Example item record

```yaml
itemId: LR-R1-Q06
reasoningFamily: LR-DIR
atomicSkills:
  - LR-DIR-03
  - LR-DIR-04
archetype: direction_path
difficulty:
  ruleCount: 3
  memoryLoad: medium
  languageLoad: short_instruction

helpPage:
  groundedToOriginalItem: true
  quickCheck:
    targetSkill: LR-DIR-02
    result: correct
    attemptedBeforeReveal: true
  instruction:
    representation: direction_arrows
    originalDiagramAnnotated: true
  guidedReinforcement:
    suppliedSupport:
      - first_arrow
    result: correct
  independentNear:
    suppliedSupport: []
    result: correct
  retryOriginal:
    result: correct

failureInterpretation:
  atomicDirectionVocabulary: independent
  multiStepTracking: supported

stateAfterHelp: supported
```

A later fresh direction-path item solved without help is required before recording `independent` for the multi-turn skill.

## 18. Round 2 behavior

Round 2 Logical Reasoning questions should first be attempted without the Help Book.

If Round 2 fails, the same page architecture may be used:

```text
Round 2 original
-> Quick Check
-> See / Build
-> Practice With Me
-> Your Turn
-> retry Round 2 original
```

But the corrected Round 2 answer remains `supported` evidence.

Require another unseen Logical Reasoning item with the same atomic skill and no helper visible before upgrading to `independent`.

## 19. Non-goals

This schema does not:

- teach Logical Reasoning as a list of answer tricks;
- replace the original missed figure with an unrelated worksheet first;
- assume a miss on a multi-rule item means the basic reasoning family is weak;
- over-decorate already visual questions;
- reveal the instructional annotation before the Quick Check;
- count success with annotated figures as independent mastery;
- keep the same supplied arrows, clue board, or overlay permanently;
- collapse all sequence, direction, coding, or spatial failures into one chapter percentage.
