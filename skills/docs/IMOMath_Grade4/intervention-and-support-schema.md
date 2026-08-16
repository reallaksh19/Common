# Grade 4 IMO — Intervention and Support Schema

## Purpose

This document defines the cross-domain learning loop used after an IMO question is attempted. It applies to Mathematical Core, Logical Reasoning, and Everyday Mathematics.

The central rule is:

> Assessment, diagnosis, instruction, support, and transfer are different objects. Do not model them as progressively easier worksheets.

The system may be sophisticated internally, but the learner-facing journey should remain simple.

```text
learner-facing:  ROUND 1 -> HELP -> ROUND 2
internal:        assess -> diagnose -> teach -> fade -> transfer
```

## 1. Distinct object types

### `assessment_item`

Purpose: determine what the learner can do independently before instruction.

Rules:

- no instructional hint;
- no added representation whose purpose is to make the target reasoning easier;
- record whether the answer was independent, guessed, or required help;
- preserve diagrams that are intrinsic to the problem itself.

### `diagnostic_probe`

Purpose: determine why an assessment item failed.

A diagnostic probe is not a lesson and should not silently teach the target strategy.

Rules:

- use only when the failure path is ambiguous;
- normally 1–2 probes, not a worksheet;
- probe the nearest prerequisite or reduced-load form;
- keep it cue-free when the aim is to measure independent understanding;
- stop probing once the failure mode is sufficiently classified.

### `instructional_activity`

Purpose: change understanding or strategy after the missing structure has been identified.

Instruction may include:

- mathematical representations;
- worked examples;
- guided completion;
- externalized clues;
- concise verbal explanation;
- elimination strategy;
- reduced working-memory demand.

### `transfer_item`

Purpose: determine whether learning survives after support is removed and the surface form changes.

Rules:

- fresh item, not the original assessment item;
- no helper page visible during the attempt;
- preserve the target skill while varying numbers, context, representation, or clue order;
- use transfer evidence to distinguish `supported` from `independent`.

## 2. Representation is not a diagnostic stage

A visual cue or mathematical representation is an instructional component, not a separate proficiency level.

Do not use:

```text
wrong answer -> visual cue -> easier question -> more practice
```

as the default architecture.

Use:

```text
assessment item
    |
    v
classify whether failure is already clear
    |
    +-- ambiguous --> diagnostic probe(s)
    |
    v
instruction using the representation that exposes the mathematical structure
    |
    v
fade support
    |
    v
fresh transfer item
```

Difficulty and representation affordance are independent dimensions. A difficult question may not need a picture; a simpler question may strongly benefit from a number line, place-value chart, array, bar model, clue board, or interval diagram.

Suggested representation metadata:

```yaml
representationAffordance: high | medium | low
preferredRepresentations:
  - number_line
  - place_value_chart
  - digit_slots
  - interval_diagram
  - bar_model
  - array
  - relation_table
  - clue_board
  - elimination_grid
  - none
```

## 3. Question-grounded help

A helper activity must remain visibly connected to the question that triggered it.

Child-facing help should begin by repeating:

- the Round 1 question number;
- the exact original question;
- the exact answer choices when multiple choice.

Then unpack that same question using the selected representation.

Avoid making the learner first solve an unrelated example and infer how it connects back to the original problem.

A preferred child-facing page sequence is:

```text
YOUR QUESTION
      |
      v
LOOK AT THIS QUESTION THIS WAY
      |
      v
TRY YOUR QUESTION AGAIN
```

A separate diagnostic probe may still occur before the helper page when needed, but it is an adult/system routing mechanism and does not need to become part of the learner-visible navigation.

## 4. Learner-facing language vs internal schema language

Internal terms should not become navigation burden for a Grade 3–4 learner.

Recommended translation:

| Internal object | Learner-facing language |
|---|---|
| assessment item | ROUND 1 — TRY IT |
| diagnostic probe | FIRST, TRY THIS / adult-hidden check |
| instructional representation | NOW LOOK |
| worked example | LET'S DO ONE TOGETHER |
| faded practice | FINISH THIS |
| independent near check | YOUR TURN |
| transfer assessment | ROUND 2 — TRY AGAIN |

Avoid learner-facing labels such as `diagnose`, `remediate`, `fade`, `transfer`, `H2`, `T3`, or `module family` unless they are genuinely useful to the child.

Complexity belongs in the system, not in learner navigation.

## 5. Routing by original question

The learner should navigate by the question they remember, not by an unfamiliar taxonomy.

Example:

```text
Round 1 Q9 difficult -> HELP Q9
Round 1 Q10 difficult -> HELP Q10
```

The backend may map both questions to the same underlying skill or instructional representation, but the learner-facing page should stay grounded to the original item.

Example backend mapping:

```yaml
round1ItemId: NUM-A09
helpEntryId: HELP-A09
instructionalConcepts:
  - inclusive_counting
  - identify_counted_object
sharedRepresentationFamily: points_vs_intervals
```

## 6. Failure classification before remediation

A wrong answer is evidence, not a diagnosis.

Possible failure classes include:

```text
concept_gap
procedure_gap
representation_misread
operation_selection
constraint_organization
working_memory_load
language_load
transfer_failure
careless_execution
guess
unknown
```

The intervention planner should ask:

1. Is the underlying skill already independently demonstrated elsewhere?
2. Did the learner fail because the problem added representation, language, constraints, or multi-step load?
3. Is a diagnostic probe necessary, or is the failure path already clear from existing evidence?
4. Which representation reveals the missing relationship with the least irrelevant information?
5. How quickly can support be faded?

## 7. Fading rule

Instructional support should not become the new permanent problem format.

Preferred progression:

```text
full representation
-> partially completed representation
-> learner creates/finishes representation
-> no supplied representation
-> changed surface form
```

Fading speed depends on learner evidence. If the learner already had the concept and only needed organization support, fade quickly. If the prerequisite probe also failed, use fuller instruction before fading.

## 8. Transfer and evidence states

Suggested evidence interpretation:

```text
Round 1 correct independently
    -> independent evidence

Round 1 wrong; helper succeeds only with representation
    -> supported

Round 1 wrong; helper succeeds; fresh Round 2 item succeeds independently
    -> independent

Fresh transfer succeeds across changed form and later retrieval
    -> secure
```

The evidence state should remain attached to the atomic skill/archetype/representation combination where useful.

Suggested record:

```yaml
assessment:
  itemId: NUM-A09
  result: incorrect
  supportUsed: []
  confidenceMarker: independent_attempt

diagnosis:
  status: classified
  failureModes:
    - boundary_count_error
    - identify_counted_object
  probesUsed: []

instruction:
  helperEntryId: HELP-A09
  groundedToOriginalItem: true
  representation:
    type: interval_diagram
    supplied: true
  supportLevel: full

transfer:
  itemId: NUM-D06
  result: correct
  supportUsed: []
  stateAfter: independent
```

## 9. Example — ticket labels vs road-marker jumps

These questions can look similar but ask for different objects to be counted.

### Ticket labels

If labels run from `38,756` through `39,125` including both ends:

```text
distance = 39,125 - 38,756 = 369
included labels = 369 + 1 = 370
```

The key atomic idea is not merely memorizing `+1`. It is identifying that the question counts points/labels, including both endpoints.

### Road-marker jumps

If markers run from `24,750 m` to `30,000 m` every `750 m`, and the question asks for jumps:

```text
24,750 -> 25,500 -> ... -> 30,000
```

Count intervals/jumps, not markers.

A shared representation family may be:

```text
points_vs_intervals
```

but the two learner-facing helper pages should remain grounded to Q9 and Q10 respectively.

## 10. Example — constrained number formation

A question such as:

> Use `0, 2, 4, 7, 9` exactly once. The number is odd, greater than `70,000`, and hundreds is twice tens. Find the greatest possible number.

may fail for different reasons:

- place-value ordering;
- odd/even rule;
- relational constraint `hundreds = 2 x tens`;
- optimization for greatest number;
- holding several conditions simultaneously.

Do not automatically route every failure to basic number-formation practice.

If simpler constrained formation is already independent, teach clue externalization / constraint organization instead.

A useful representation may be:

```text
[10,000s] [1,000s] [100s] [10s] [1s]
```

with relation clues written beside the slots rather than held in working memory.

## 11. Helper-book presentation requirements

For printable Grade 3–4 support material:

- one main mathematical idea per page;
- repeat the original question at the top;
- use large, readable type;
- maintain consistent left alignment and spacing;
- prefer one dominant representation over several decorative visuals;
- use short labels rather than explanatory paragraphs;
- keep answer choices aligned and easy to scan;
- preserve whitespace;
- distinguish the question, representation, and retry areas visually;
- avoid visual clutter that adds cognitive load without exposing structure.

The representation must do mathematical work. Decoration alone is not support.

## 12. Planner contract

The planner should implement the following logic:

```text
ROUND 1 assessment
        |
        v
independent success? ---- yes ---> record evidence; no helper
        |
        no
        v
failure already classifiable from evidence?
        |                         |
       yes                       no
        |                         |
        |                   run minimal probe
        |                         |
        -----------+-------------
                   v
        select instructional target
                   |
                   v
        open question-grounded HELP
                   |
                   v
        teach with useful representation
                   |
                   v
              fade support
                   |
                   v
        ROUND 2 fresh transfer
```

## 13. Non-goals

This schema does not:

- turn every difficult question into a picture;
- use the hardest 50% of questions as an automatic visual-support set;
- treat a visual cue as a diagnostic probe;
- assume a wrong Olympiad item means the underlying concept is weak;
- send the learner through long prerequisite worksheets by default;
- expose internal routing codes as learner navigation;
- require an unrelated warm-up before explaining the question the learner actually missed;
- count success with permanent scaffolding as independent mastery.
