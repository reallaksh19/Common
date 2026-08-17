# Grade 4 IMO - Intervention and Support Schema

## Purpose

This document defines the cross-domain learning loop for Grade 4 IMO preparation, including learners who need a more explicit bridge from Grade 3 and learners moving from Grade 4 core into pre-IMO transfer.

The central rule is:

> A difficult question can change role. Once support begins, that exact question becomes an instructional example and must no longer be used as evidence of independent mastery.

This applies to Mathematical Core, Logical Reasoning, and Everyday Mathematics.

The child-facing journey should remain simple even when the backend evidence model is detailed.

```text
TRY
 |
 +-- independent -> continue
 |
 +-- difficult -> LET'S WORK THIS ONE OUT TOGETHER
                     |
                     v
              same question becomes example
                     |
                     v
              child completes a key step
                     |
                     v
                fresh close item
                     |
                     v
              later mixed transfer
```

## 1. Object roles

### `assessment_item`

Purpose: obtain unsupported evidence before teaching.

Rules:

- no instructional hint;
- no added representation whose purpose is to reveal the method;
- intrinsic diagrams remain part of the item;
- record independent / guessed / needed help.

### `converted_worked_example`

Purpose: teach from the exact question that was difficult.

After conversion:

- preserve the original numbers, figures, clues, wording, and answer choices;
- treat the item as instruction, not assessment;
- expose the first useful structure or step;
- prefer partial completion over fully solving the item when possible;
- mark `instructionallyExposed: true`;
- never later count a corrected answer to that same item as independent evidence.

Preferred learner-facing wording:

```text
LET'S WORK THIS ONE OUT TOGETHER
We'll find the first step, then you can finish it.
```

### `diagnostic_probe`

Purpose: isolate the nearest prerequisite or atomic reasoning move only when the failure path is ambiguous.

The probe is conditional, not mandatory.

Rules:

- usually one small cue-free check;
- use reduced cognitive load, not arbitrary grade reduction;
- stop once the failure path is clear;
- do not turn the Help Book into a prerequisite worksheet.

### `instructional_activity`

Purpose: expose hidden structure in the original question.

May include:

- number line;
- place-value alignment;
- digit slots;
- clue board;
- relation table;
- balance bars;
- ordered list;
- possibility / case table;
- direction or transformation arrows;
- elimination marks;
- concise worked steps.

### `guided_reinforcement_item`

Purpose: reuse the atomic idea with one scaffold still supplied.

### `independent_near_item`

Purpose: require reconstruction of the same idea with little or no supplied scaffold.

### `transfer_item`

Purpose: determine whether the learner can recognize and use the idea when surface cues change.

Rules:

- unseen;
- no Help Book visible;
- not the converted original question;
- change context, wording, representation, clue order, or question archetype while preserving the intended underlying structure;
- allow learner-created representations.

## 2. Conversion layer

The conversion layer sits between the failed attempt and instruction.

```text
QUESTION ATTEMPT
      |
      v
DIFFICULT?
      |
      v
CONVERT SAME QUESTION TO WORKED EXAMPLE
      |
      +-- failure path unclear -> optional SMALL CHECK
      |
      v
SEE / BUILD ORIGINAL QUESTION
      |
      v
CHILD COMPLETES KEY STEP
      |
      v
FRESH CLOSE ITEM
```

The original question is now a teaching artifact.

Do not use a retry of the exposed original to prove independence.

## 3. Help-page contract

Preferred page:

```text
YOUR QUESTION
     |
     v
LET'S WORK THIS ONE OUT TOGETHER
     |
     +-- optional: IF THIS PART IS HARD...
     |
     v
SEE IT THIS WAY
     |
     v
YOUR STEP
     |
     v
TRY ONE
```

The Help page should not feel like six different worksheets. Use visual hierarchy and whitespace so the learner experiences one continuous path.

## 4. Partial worked examples

Default to preserving some thinking for the child.

Example:

```text
show:
6 x 20 = 120
2,400 = 120 x ?

child completes:
? = ____
```

For a clue-number problem:

```text
show digit slots
fill direct clues
externalize one relationship

child completes the final missing pair
```

For a visual reasoning problem:

```text
mark the first transformation
child checks whether it repeats
child applies the next step
```

Support should make the next thinking step achievable, not make thinking unnecessary.

## 5. Fading

Use gradual hand-back:

```text
converted original: high support
-> child completes a key step
-> close item with partial support
-> close item with no supplied representation
-> later mixed transfer
```

If the learner quickly reconstructs the method, fade faster. If the close item is still difficult, insert one more faded item rather than changing topic immediately.

## 6. Round 1 has two legitimate forms

Round 1 should never be treated as a random mini-exam, but its structure depends on the learner stage.

### Bridge Round 1

For a Grade 3 -> Grade 4 transition, use tight concept ladders:

```text
familiar prerequisite
-> direct Grade 4 extension
-> one extra reasoning demand
```

Neighboring questions may share the same archetype because controlled extension is the goal.

### Pre-IMO Round 1

For a learner with enough Grade 4 core to begin transfer work, do **not** teach by repeating ten near-identical templates.

Use a curated progression of different question archetypes that exercise a connected conceptual backbone.

Example Number Sense progression:

```text
place-value magnitude
-> equivalent regrouping
-> missing-digit comparison constraint
-> number-line distance
-> boundary continuity
-> rounding interval
-> representation conversion
-> parity structure
-> equality / balance
-> systematic enumeration
```

The learner should encounter varied surfaces while still being able to connect them to a manageable set of thinking tools.

## 7. Round 2 is deliberately interleaved transfer

Round 2 should be mixed, but not random in the loose sense.

Its purpose is method recognition:

> What kind of structure is hidden here, and what tool could help me?

Rules:

- remove concept-family labels;
- do not simply reuse Round 1 wording with different numbers;
- change question archetype when possible;
- mix families across the round;
- avoid obvious adjacent near-copies;
- use plausible distractors;
- provide no instructional representation;
- allow the learner to construct their own representation;
- keep most items at Grade 4 core / pre-IMO demand unless the task explicitly targets Achievers.

Examples of useful transfer changes:

```text
place value -> quantify whole-number change after a digit substitution
comparison -> smallest digit satisfying an inequality
distance -> equally spaced markers
rounding -> smallest value in a rounding interval
clue construction -> identify which candidate satisfies all clues
number formation -> count all valid cases
Roman recognition -> decode, operate, encode
expanded form -> compose nonstandard place-value groups
successor -> nth value after crossing a number boundary
midpoint -> predecessor/successor symmetry or balance
```

## 8. Learner-created representations are positive evidence

`No supplied representation` does not mean `no drawing allowed`.

In transfer rounds, a child who independently draws an appropriate representation is demonstrating strategy selection.

Useful self-generated representations include:

- number line;
- place-value columns;
- digit slots;
- clue board;
- ordered list;
- case table;
- balance bars;
- elimination marks.

Suggested record:

```yaml
selfGeneratedRepresentation:
  used: true
  type: number_line
  appropriate: true
  promptedByAdult: false
```

The goal is not to remove visual thinking. The goal is to move from **representation supplied by teacher** to **representation selected and built by learner**.

## 9. Round 2 Help behavior

An optional Round 2 Help Book may exist, but only after the clean attempt.

If opened:

```text
Round 2 item attempted independently
-> difficult
-> convert exact Round 2 item to worked example
-> supported learning
-> fresh close item
-> later unseen transfer required
```

The original Round 2 item is burned for transfer evidence.

Do not count a corrected answer after Help as independent.

## 10. Evidence states

Suggested interpretation:

```text
initial item correct without support
-> independent

item converted to example
-> supported

fresh close item correct with scaffold
-> supported / emerging

fresh close item correct without supplied scaffold
-> near-independent

Round 2 unseen item correct without Help
-> independent transfer

Round 2 item correct after learner independently creates a useful representation
-> independent transfer + positive strategy-selection evidence

Round 2 item corrected after Help
-> supported

later unseen mixed retrieval succeeds
-> independent / secure depending on retention
```

Suggested record:

```yaml
originalItem:
  itemId: NUM-R1-Q04
  initialResult: incorrect
  convertedToWorkedExample: true
  instructionallyExposed: true

instruction:
  representation: number_line
  childCompletionRequired: true

reinforcement:
  closeItemResult: correct
  suppliedRepresentation: false

stateAfterHelp: supported

transfer:
  itemId: NUM-R2-Q03
  result: correct
  helpUsed: false
  selfGeneratedRepresentation:
    used: true
    type: equal_spacing_line
    appropriate: true
  stateAfter: independent
```

## 11. Failure classification

A wrong answer is evidence, not a diagnosis.

Possible failure classes:

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
systematic_enumeration_failure
boundary_count_error
careless_execution
guess
unknown
```

Ask:

1. What atomic skill or reasoning move was required?
2. Is that move independently demonstrated elsewhere?
3. Did the learner fail because the representation was missing, misread, or never selected?
4. Was the challenge concept complexity, wording, multiple constraints, distractors, or working memory?
5. What is the least-supportive useful representation?
6. What fresh close item can hand the thinking back?
7. What later interleaved item can test genuine recognition and transfer?

## 12. Logical Reasoning adaptation

The same architecture applies to Logical Reasoning.

A pre-IMO Round 1 should not be ten surface copies of one sequence or coding pattern. Preserve the reasoning capability while varying the surface form.

Examples:

```text
sequence -> identify transformation -> apply to changed symbols
analogy -> relation recognition -> changed representation
ranking -> pairwise clue -> multi-clue order
coding -> mapping -> reverse / partial mapping
spatial -> rotation -> distinguish rotation from reflection
combination -> one constraint -> systematic elimination
```

If a Logical Reasoning question is difficult, teach from the exact original figures / clues and hand one step back to the learner.

## 13. Presentation requirements

For printable Grade 3-4 material:

- one dominant idea per Help page;
- exact original question at top;
- conversion message immediately after it;
- short child-friendly wording;
- large readable type;
- one useful representation rather than decorative clutter;
- response space inside the worked example;
- fresh close practice visually separated;
- enough workspace in transfer rounds for learner-created representations;
- do not expose internal evidence labels.

## 14. Planner contract

```text
ROUND 1
   |
   v
unsupported attempt
   |
   +-- independent -> continue planned progression
   |
   +-- difficult
          |
          v
   convert exact item to worked example
          |
          +-- prerequisite ambiguity? -> optional probe
          |
          v
   expose useful structure
          |
          v
   child completes key step
          |
          v
   fresh close item

AFTER ROUND 1
   |
   v
ROUND 2 DELIBERATELY INTERLEAVED TRANSFER
   |
   +-- independent success -> independent evidence
   |
   +-- independently self-generates useful representation -> positive strategy evidence
   |
   +-- difficult -> optional Help -> supported only
                         |
                         v
                 later unseen transfer
```

## 15. Non-goals

This schema does not:

- randomize Round 1 as if it were an exam;
- teach pre-IMO transfer through repetitive near-copy worksheets;
- force a Quick Check onto every Help page;
- count a taught original question as independent mastery;
- forbid drawing or self-created representations in transfer rounds;
- treat a supplied picture as automatically helpful;
- use `right-brain / left-brain learner` as a scientific classification;
- infer a broad learner deficit from one wrong item;
- jump directly from a worked example to full Achievers complexity.
