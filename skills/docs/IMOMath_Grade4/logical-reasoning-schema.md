# Grade 4 IMO — Logical Reasoning Schema

## Purpose

Logical Reasoning is an independent reasoning-capability domain. It must not be represented as a single chapter score or as a collection of worksheets ordered only by difficulty.

Primary structure:

`reasoning family -> atomic reasoning skill -> question archetype -> representation -> cognitive load -> learner evidence`

The schema should answer not only whether a learner solved a question, but what reasoning operation was required, how it was represented, how many rules/clues had to be coordinated, and what support was necessary.

## Reasoning families

### LR-SEQ — Sequence reasoning

Typical tasks:

- repeating patterns;
- growing patterns;
- missing terms;
- next figure/term;
- alternating/interleaved rules;
- incorrect-term detection.

Example atomic skills:

```text
LR-SEQ-01 observe_sequence_order
LR-SEQ-02 compare_changing_attributes
LR-SEQ-03 recognize_repetition
LR-SEQ-04 identify_repeating_unit
LR-SEQ-05 continue_repeating_pattern
LR-SEQ-06 detect_growth_or_change
LR-SEQ-07 state_pattern_rule
LR-SEQ-08 continue_growing_pattern
LR-SEQ-09 identify_alternating_rule
LR-SEQ-10 find_missing_middle_term
LR-SEQ-11 detect_incorrect_term
LR-SEQ-12 solve_mixed_sequence_reasoning
```

### LR-ANA — Analogy

Typical tasks:

- A:B :: C:?;
- shape/number/letter relation transfer;
- transformation analogy.

Atomic-skill examples:

```text
LR-ANA-01 identify_relation
LR-ANA-02 apply_relation_to_new_pair
LR-ANA-03 distinguish_surface_similarity_from_rule
LR-ANA-04 solve_multi_attribute_analogy
```

### LR-CLS — Classification

Typical tasks:

- odd one out;
- group by governing property;
- identify common rule.

### LR-COD — Coding and decoding

```text
LR-COD-01 recognize_symbol_mapping
LR-COD-02 apply_fixed_mapping
LR-COD-03 reverse_mapping
LR-COD-04 detect_mapping_rule
LR-COD-05 apply_shift_or_relation_rule
LR-COD-06 decode_multi_symbol_expression
```

### LR-RNK — Ordering and ranking

Typical skills:

- interpret relative rank;
- order several entities;
- derive missing position;
- reconcile two or more rank clues.

### LR-DIR — Directional reasoning

```text
LR-DIR-01 identify_left_right
LR-DIR-02 follow_single_turn
LR-DIR-03 follow_multiple_turns
LR-DIR-04 determine_final_direction
LR-DIR-05 determine_relative_position
LR-DIR-06 reverse_perspective
LR-DIR-07 solve_mixed_direction_path
```

### LR-SPA — Spatial transformation

Typical skills:

- rotation;
- mirror image;
- reflection;
- orientation matching;
- viewpoint change.

### LR-CMP — Visual composition

Typical skills:

- embedded figures;
- shape decomposition;
- shape construction;
- part-whole visual matching.

### LR-COM — Combination reasoning

Typical skills:

- enumerate possibilities;
- eliminate impossible combinations;
- constrained arrangements.

### LR-TMP — Temporal reasoning

Typical skills:

- clock relations;
- calendar relations;
- before/after intervals;
- day/date shifts.

### LR-MIX — Mixed reasoning

Use only when two or more reasoning families are materially required. Do not create a generic `mixed` label when one family is actually dominant.

## Question archetype

Each question should identify the form in which the reasoning skill is tested.

Suggested values:

```text
direct_recognition
missing_element
next_element
incorrect_element
analogy
classification
fixed_mapping
reverse_mapping
relative_order
multi_clue_order
direction_path
rotation
reflection
embedded_figure
combination_count
clock_relation
calendar_relation
multi_rule
```

Question archetype is separate from the underlying reasoning skill.

## Representation

Suggested values:

```text
number
letter
symbol
shape
diagram
grid
arrow
clock
calendar
mixed
```

A learner may be independent in one representation and supported in another. That distinction should remain visible in evidence.

## Difficulty dimensions

### `ruleCount`

```text
1 = one governing rule
2 = two linked rules
3 = alternating/interleaved rules
4 = multiple interacting clues/rules
```

### `memoryLoad`

```text
low
medium
high
```

### `transformationDepth`

Suggested spatial values:

```text
identity
single_rotation
multiple_rotation
reflection
rotation_plus_reflection
viewpoint_change
```

### `distractorSimilarity`

```text
low
medium
high
```

High similarity means distractors differ only by small but meaningful transformations.

### `languageLoad`

```text
minimal
short_instruction
multi_clue
conditional
```

### `transferDistance`

```text
same_form
near_transfer
far_transfer
```

## Difficulty ladder

Do not use grade labels as the reasoning skill identity. The following bands describe instructional demand only.

### LR0 — prerequisite rescue

One obvious relation; usually hidden as fallback remediation.

Example: simple ABAB repetition.

### LR1 — transition

One rule in a familiar representation.

Example: four-direction rotation sequence.

### LR2 — core reasoning

The rule must be inferred rather than copied.

Example: growing visual pattern or straightforward code rule.

### LR3 — Olympiad transfer

The same reasoning capability appears in an unfamiliar representation or with a second demand.

### LR4 — Achievers-style reasoning

Multiple clues/rules, high distractor similarity, interleaving, reversal, or multi-step spatial/directional reasoning.

## Challenge-first diagnostic behavior

Start near the expected transition/core boundary, not at LR0.

Example for direction reasoning:

1. Present a multi-turn path.
2. If solved independently, do not test basic left/right.
3. If failed, probe a single-turn problem.
4. If single-turn is correct, record the gap as multi-step tracking/working-memory load rather than direction vocabulary.
5. If single-turn is also incorrect, assign foundational direction instruction.

The same downward-probe logic applies to sequence, coding, ranking and spatial families.

## Learner evidence

Evidence should be keyed to atomic skill + archetype + representation where useful.

Example:

```yaml
skillId: LR-DIR-03
state: independent
accuracy: 0.8
supportUsed: []
representationEvidence:
  diagram: independent
  verbal: supported
failureModes:
  - loses_position_after_multiple_steps
transfer:
  near: independent
  far: supported
explanationQuality: partial
```

Do not collapse this to `Direction Sense = 80%`.

## Suggested failure modes

```text
rule_not_detected
wrong_rule_selected
loses_position
forgets_intermediate_state
confuses_rotation_reflection
reverses_perspective
misses_alternating_structure
surface_match_bias
fails_to_eliminate_distractors
language_overload
working_memory_overload
careless_execution
unknown
```

Failure modes should describe observed evidence, not diagnose the learner clinically.

## Support library

Support must remain separate from proficiency.

Suggested Logical Reasoning supports:

```text
highlight_change
mark_repeating_unit
split_alternating_sequences
draw_direction_arrows
mark_positions
overlay_rotation
show_mirror_axis
cross_out_impossible_choices
make_relation_table
externalize_clues
reduce_visible_choices
```

A learner can be conceptually independent while still benefiting from a lower-memory presentation.

## Transfer requirement

Mastery should require more than repeated success in one visual form.

For example, sequence reasoning may be checked across:

- shapes;
- numbers;
- arrows/orientation;
- positions;
- symbols.

Suggested progression:

`direct -> changed representation -> mixed representation -> multi-rule`

## Advancement rule

Do not advance solely on percentage correct.

A stronger criterion is:

- solves independently;
- explains or reconstructs the governing rule;
- succeeds when representation changes;
- does not require the same support repeatedly;
- retains performance in later mixed retrieval.

## Exam mapping

Exam section is metadata, not skill identity.

Example:

```yaml
examMapping:
  competition: SOF IMO
  section: logical_reasoning
  classLevel: 4
```

The same reasoning skill may later map to another competition or grade without changing its underlying skill ID.

## Non-goals

This schema does not:

- encode Logical Reasoning as one mastery percentage;
- use `easy/medium/hard` as the only difficulty model;
- treat Patterns as the entire Logical Reasoning curriculum;
- conflate visual capacity support with conceptual deficiency;
- create separate grade-labelled copies of reusable reasoning skills;
- treat Achievers as a separate reasoning curriculum.
