# Grade 4 IMO — Everyday Mathematics Schema

## Purpose

Everyday Mathematics is not a separate mathematics curriculum. It is an application and transfer layer over Mathematical Core skills.

Primary structure:

`required mathematical skills + problem schema + context + information structure + operation plan + representation + learner evidence`

The schema must distinguish a mathematical-concept gap from a translation, planning, unit, reading, or working-memory failure.

## Core rule

Never duplicate mathematical skills merely because they appear in a word problem.

For example, this problem:

> A shop had 4,850 pencils. It received 1,275 more and sold 960. How many remain?

references Mathematical Core skills such as addition and subtraction. Everyday Mathematics adds:

- a change situation;
- a two-step operation plan;
- quantity tracking;
- language interpretation;
- transfer into context.

If the learner calculates correctly but chooses the wrong operations, that is not the same failure as being unable to add or subtract the numbers.

## Problem families

### EM-CHG — Change

Something increases or decreases.

Canonical structures:

```text
start + change = result
start - change = result
```

Unknown may be start, change, or result.

### EM-CMB — Combine / part-whole

Canonical structure:

```text
part + part = whole
```

May extend to three or more parts.

### EM-CMP — Compare

Canonical structure:

```text
larger - smaller = difference
```

The wording `more` or `less` must not be treated as a direct operation cue; the learner should identify the relationship.

### EM-EQG — Equal groups

Canonical structures:

```text
groups x items_per_group = total
total / groups = items_per_group
total / items_per_group = groups
```

### EM-MEA — Measurement

Typical demands:

- length;
- mass;
- capacity;
- perimeter;
- unit selection;
- unit conversion.

### EM-MNY — Money

Typical demands:

- total cost;
- balance;
- change;
- repeated items;
- multi-purchase comparison.

### EM-TIM — Time

Typical demands:

- clock reading;
- elapsed time;
- start/end time;
- calendar intervals.

### EM-DAT — Data

Typical representations:

- table;
- pictograph;
- bar graph;
- simple chart.

Typical tasks:

- retrieve;
- compare;
- combine;
- infer.

### EM-NIC — Number in context

Transfers Number Sense into realistic or semi-realistic structures such as:

- serial numbers;
- populations;
- ticket ranges;
- odometers;
- locker/access codes;
- rankings;
- records.

### EM-MIX — Mixed multi-step

Use when two or more problem schemas are materially required.

Example:

`combine -> compare`

or

`increase -> decrease`

Do not label a problem `mixed` simply because it contains two arithmetic operations if the situation schema remains one coherent type.

## Problem-schema representation

Each problem should record its situation structure explicitly.

Example:

```yaml
problemSchema:
  type: change
  unknown: result
```

Compare example:

```yaml
problemSchema:
  type: compare
  unknown: difference
```

Multi-step example:

```yaml
problemSchema:
  type: multi_step
  sequence:
    - combine
    - compare
```

## Required mathematical skills

Every Everyday Mathematics item references one or more Mathematical Core skills.

Example:

```yaml
requiredSkills:
  - addition.five_digit_regrouping
  - subtraction.five_digit_regrouping
```

These skills remain owned by the Mathematical Core schema. Everyday Mathematics must not create duplicate aliases such as `everyday_addition`.

## Difficulty dimensions

### `mathComplexity`

How difficult is the underlying mathematics independent of context?

Suggested ordinal scale:

```text
0 = prerequisite/basic
1 = transition
2 = grade-level core
3 = advanced grade-level combination
```

### `stepCount`

```text
1
2
3+
```

### `schemaComplexity`

```text
direct
inverse
mixed
```

Direct example:

> There are 8 boxes with 6 pencils each. How many pencils?

Inverse example:

> 48 pencils are packed equally in 8 boxes. How many pencils per box?

### `informationLoad`

```text
minimal
moderate
extra_information
high
```

`extra_information` means the learner must identify and ignore non-required data.

### `languageLoad`

```text
simple
relational
multi_sentence
conditional
```

### `representation`

```text
text
table
diagram
bill
calendar
map
number_line
chart
mixed
```

### `unitLoad`

```text
none
same_units
conversion_required
multiple_units
```

### `transferDistance`

```text
same_form
near_transfer
far_transfer
```

### `distractorQuality`

Distractors should be linked to plausible failure paths where possible, such as:

- correct first step but missed second step;
- reversed subtraction;
- wrong unit conversion;
- included irrelevant value;
- omitted one quantity.

## Difficulty ladder

These bands describe problem demand, not separate curricula.

### EM0 — explicit model / fallback

One obvious operation with direct wording. Usually hidden as remediation.

### EM1 — Grade 3 -> Grade 4 transition

One operation or simple schema, but the learner must select the operation independently.

### EM2 — Grade 4 core

Grade-level mathematics in a context with moderate interpretation demand.

### EM3 — transfer

Two-step reasoning, less familiar representation, or indirect wording.

### EM4 — Olympiad

The mathematical structure is disguised by context, information order, comparison, interval counting, inverse structure, or representation switching.

### EM5 — Achievers-style application

Multiple schemas, indirect unknowns, simultaneous constraints, extra information, or several reasoning steps.

## Diagnostic principle

Do not infer `math skill weak` from a wrong Everyday Mathematics answer.

Classify the failure path first.

Suggested failure modes:

```text
concept_gap
computation_error
operation_selection
schema_identification
missed_step
quantity_tracking
unit_error
reading_error
irrelevant_information
working_memory
inverse_structure_error
boundary_count_error
careless_execution
unknown
```

### Example

Problem:

> 8 cartons have 1,250 bottles each. Another 375 bottles are loose. How many bottles altogether?

Learner answer: `10,000`.

Likely evidence:

- `8 x 1,250` was calculated correctly;
- the loose 375 bottles were omitted.

Do not record multiplication as deficient automatically.

A more accurate evidence record may be:

```yaml
mathematicalEvidence:
  multiplication.equal_groups: independent
applicationEvidence:
  quantity_tracking: supported
  multi_step_planning: supported
failureModes:
  - missed_second_quantity
```

## Downward probing

If a contextual problem is wrong, probe the underlying layer instead of immediately reteaching the chapter.

Example:

1. Learner fails a two-step inventory problem.
2. Present the two arithmetic calculations separately.
3. If both are solved correctly, retain the mathematical skills as independent and target operation planning / quantity tracking.
4. If a standalone calculation also fails, route to Mathematical Core remediation for that exact skill.

This prevents over-remediation.

## Support library

Everyday Mathematics support should externalize story structure without changing the mathematics.

Suggested supports:

```text
underline_quantities
label_units
story_strip
bar_model
part_whole_diagram
change_diagram
comparison_bar
write_operation_plan
number_sentence
cross_out_irrelevant_data
step_checklist
mark_start_change_result
mark_groups_items_total
```

Support usage is evidence about capacity/presentation need, not automatic evidence of conceptual deficiency.

## Operation plan

Multi-step questions should optionally store an explicit intended plan for diagnostic comparison.

Example:

```yaml
operationPlan:
  - operation: multiply
    purpose: find_carton_total
  - operation: add
    purpose: include_loose_items
```

This enables the system to distinguish:

- wrong operation selection;
- correct first step but missed second step;
- correct plan with computational error.

## Learner evidence model

Example:

```yaml
problemFamily: EM-EQG
state: supported
mathSkillStates:
  multiplication.equal_groups: independent
applicationSkills:
  identify_equal_groups: independent
  track_extra_quantity: supported
  build_two_step_plan: supported
supportUsed:
  - underline_quantities
  - write_operation_plan
transfer:
  same_context: independent
  new_context: supported
failureModes:
  - missed_second_quantity
```

Avoid reducing this to `Everyday Mathematics = 70%`.

## Transfer requirement

Success should be tested across different contexts using the same mathematical structure.

For example, equal-groups reasoning can transfer through:

- boxes and pencils;
- rows and chairs;
- tickets per packet;
- bottles per crate.

The context should change without changing the underlying skill.

Similarly, number sense may transfer through:

- population;
- odometer;
- serial range;
- locker code;
- ticket number.

## Advancement rule

Do not advance solely because several similarly worded problems were correct.

A stronger criterion is:

- underlying mathematical skill is independently correct;
- learner identifies the problem schema without operation-keyword guessing;
- operation plan is complete;
- units/quantities are tracked correctly;
- learner succeeds in a changed context or representation;
- later mixed retrieval remains successful.

## Exam mapping

Exam section is metadata rather than the mathematical hierarchy.

Example:

```yaml
examMapping:
  competition: SOF IMO
  section: everyday_mathematics
  classLevel: 4
```

The same Mathematical Core skill can also appear in Mathematical Reasoning or Achievers mode without being duplicated.

## Achievers policy

Do not create `Achievers` skills.

Increase cognitive demand through combinations of:

- indirect unknowns;
- multiple problem schemas;
- higher step count;
- more constraints;
- representation switching;
- extra information;
- stronger distractors;
- farther transfer.

The underlying mathematical skills remain the same.

## Suggested item record

```yaml
problemId: EM-00425
requiredSkills:
  - addition.five_digit_regrouping
  - subtraction.five_digit_regrouping
problemSchema:
  type: multi_step
  sequence:
    - increase
    - decrease
context:
  family: inventory
difficulty:
  mathComplexity: 2
  stepCount: 2
  schemaComplexity: direct
  languageLoad: relational
  informationLoad: moderate
  unitLoad: none
  transferDistance: near_transfer
operationPlan:
  - operation: add
    purpose: apply_increase
  - operation: subtract
    purpose: apply_decrease
examMapping:
  competition: SOF IMO
  section: everyday_mathematics
  classLevel: 4
```

## Non-goals

This schema does not:

- duplicate Mathematical Core skills;
- classify every word problem as one generic `word_problem` skill;
- use keywords such as `more = add` as the conceptual model;
- infer conceptual weakness from every wrong contextual answer;
- treat Everyday Mathematics as a separate chapter tree parallel to Numbers/Fractions/etc.;
- create separate Achievers skills;
- use a single `easy/medium/hard` label as the only difficulty representation.
