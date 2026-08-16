# Grade 4 IMO - Intervention and Support Schema

## Purpose

This document defines the cross-domain learning loop for a Grade 3 -> Grade 4 learner preparing for IMO-style work.

The central rule is:

> A difficult question can change role. Once the learner struggles with it and support begins, that exact question becomes an instructional example and must no longer be used as evidence of independent mastery.

This applies to Mathematical Core, Logical Reasoning, and Everyday Mathematics.

The system may be sophisticated internally, but the child-facing journey should stay simple.

```text
TRY A QUESTION
    |
    +-- comfortable -> keep climbing
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
                  close new question
                         |
                         v
                  later fresh transfer
```

## 1. Object roles

### `assessment_item`

Purpose: obtain unsupported evidence before teaching.

Rules:

- no instructional hint;
- no extra representation added to make the target easier;
- intrinsic diagrams remain part of the item;
- record independent / guessed / needed help.

### `converted_worked_example`

Purpose: teach from the exact question that was difficult.

Conversion occurs when the learner has already attempted an assessment or ladder item and the adult/system decides to support it.

After conversion:

- preserve the original numbers, figures, clues, wording, and answer choices;
- explicitly treat the item as instruction rather than assessment;
- reveal the first useful structure or step;
- do not fully remove the child's thinking when a partial example is sufficient;
- mark the original item as `instructionally_exposed: true`;
- never later count a corrected answer to that same item as independent evidence.

Suggested learner-facing wording:

```text
LET'S WORK THIS ONE OUT TOGETHER
We'll find the first step, then you can finish it.
```

Avoid learner-facing language such as:

```text
THIS QUESTION NOW BECOMES OUR EXAMPLE
We are not testing it anymore
```

The internal role change is important; the child does not need assessment vocabulary.

### `diagnostic_probe`

Purpose: isolate the nearest prerequisite or atomic reasoning move when the failure path is genuinely ambiguous.

Important: the probe is **conditional**, not mandatory.

Use it when one difficult item could plausibly reflect several different bottlenecks and current evidence cannot distinguish them.

Rules:

- usually one small check;
- cue-free before teaching is revealed;
- reduced cognitive load, not arbitrarily lower grade level;
- stop once the failure path is clear;
- do not turn it into a prerequisite worksheet.

### `instructional_activity`

Purpose: expose the structure that was hidden in the original item.

May include:

- worked steps;
- partially completed examples;
- place-value charts;
- number lines;
- digit slots;
- relation tables;
- clue boards;
- direction or transformation arrows;
- concise verbal explanation;
- elimination of distractors;
- externalization of multi-step information.

### `guided_reinforcement_item`

Purpose: use the same atomic idea with one scaffold still supplied.

### `independent_near_item`

Purpose: require the learner to reconstruct the same method with little or no supplied scaffold.

Success is stronger than guided practice but is still near-transfer evidence.

### `transfer_item`

Purpose: test whether the method survives after support is removed and surface cues are mixed or changed.

Rules:

- unseen;
- no Help Book visible;
- not the converted original question;
- vary numbers, context, clue order, representation, or neighboring concepts;
- use this evidence to distinguish `supported` from `independent`.

## 2. Conversion layer

The conversion layer sits between a difficult question and any optional Quick Check / See-Build instruction.

```text
QUESTION ATTEMPT
      |
      v
DIFFICULT?
      |
      v
CONVERT THE SAME QUESTION TO A WORKED EXAMPLE
      |
      +-- failure path unclear -> optional QUICK CHECK
      |
      v
SEE / BUILD THE ORIGINAL QUESTION
      |
      v
CHILD COMPLETES A KEY STEP
      |
      v
GUIDED OR CLOSE NEW QUESTION
      |
      v
LESS-SUPPORTED NEW QUESTION
```

The converted item is now a teaching artifact.

Do not ask the learner to "prove independence" by retrying the same exposed question. A retry may be useful for reconstruction or confidence, but its evidence state remains `supported`.

## 3. Preferred help-page contract

For a learner who needs additional scaffolding, the standard page should be:

```text
YOUR QUESTION
     |
     v
LET'S WORK THIS ONE OUT TOGETHER
     |
     +-- optional: SMALL CHECK if the first step is unclear
     |
     v
SEE / BUILD THIS SAME QUESTION
     |
     v
YOUR STEP - finish one important part
     |
     v
TRY ONE - close new question
```

If the learner still needs support on `TRY ONE`, add one more faded item rather than jumping immediately to a much harder problem.

The page does not need every internal stage printed as a separate colored box. Visual hierarchy should reduce, not add, cognitive load.

## 4. Quick Check is conditional

Do **not** automatically put a Quick Check on every difficult question.

Use it only when diagnostic value justifies the extra step.

Examples where a Quick Check is useful:

```text
large inclusive range wrong
-> check whether small inclusive counting is understood

multi-constraint number puzzle wrong
-> check the relational clue separately if other evidence is unclear

multi-turn direction item wrong
-> check one turn if direction vocabulary may be unstable
```

Examples where it may be unnecessary:

```text
learner already demonstrates the prerequisite independently elsewhere
failure is clearly due to clue organization
failure is clearly due to an unfamiliar representation
```

## 5. Worked example should preserve thinking

The default is not to solve the entire difficult question immediately.

Prefer a **partial worked example** when possible.

Example:

```text
2,400 = 6 x ? x 20

show:
6 x 20 = 120
2,400 = 120 x ?

child completes:
? = ____
```

For reasoning:

```text
show the first transformation
ask the learner to identify whether the same transformation repeats
then let the learner apply it to the next step
```

Support should make the next thinking step achievable, not make thinking unnecessary.

## 6. Fading

Use a gradual hand-back of responsibility:

```text
converted original: high support
-> child finishes a late/key step
-> close new item with partial support
-> close new item with no supplied representation
-> later mixed transfer
```

If the learner needs more support, insert another faded item.

If the learner quickly reconstructs the method, fade faster.

## 7. Evidence rules

Suggested interpretation:

```text
item correct before support
    -> independent evidence

item difficult; item converted to example
    -> item is burned for independent evidence

converted example completed correctly
    -> supported learning

close new item solved with partial support
    -> supported / emerging

close new item solved without supplied scaffold
    -> near-independent evidence

later unseen mixed transfer solved without help
    -> independent evidence

later transfer retained across time and mixed retrieval
    -> secure
```

Suggested record:

```yaml
originalItem:
  itemId: NUM-R1-C3-Q2
  initialResult: incorrect
  convertedToWorkedExample: true
  instructionallyExposed: true

probe:
  used: false

instruction:
  groundedToOriginalItem: true
  representation: digit_slots
  childCompletionRequired: true

reinforcement:
  guidedItemId: NUM-R1-C3-Q2-G1
  guidedResult: correct
  nearItemId: NUM-R1-C3-Q2-N1
  nearResult: correct

stateAfterHelp: supported

transfer:
  itemId: NUM-R2-Q07
  result: correct
  supportUsed: []
  stateAfter: independent
```

## 8. Round 1 and Round 2 have different jobs

Round 1 and Round 2 must not be generated from the same randomization policy.

### Round 1 - structured learning ladder

Round 1 is a **clustered bridge**, especially for a learner performing below the expected level.

Its purpose is to build momentum and reveal the learner's boundary while teaching can occur immediately.

Rules:

- group questions by conceptual family;
- order each family from accessible -> one added demand -> application/reasoning;
- keep neighboring questions conceptually similar enough that the learner can reuse a method;
- change one major demand at a time;
- use Grade 3 knowledge as the entry rung and Grade 4 knowledge as the destination;
- if a rung is difficult, convert that rung into the worked example, then continue with a close new rung;
- do not randomize unrelated concepts inside a cluster;
- do not interpret Round 1 as a single clean exam score.

Preferred cluster shape:

```text
RUNG 1 - familiar prerequisite / late Grade 3
RUNG 2 - direct Grade 4 extension
RUNG 3 - Grade 4 application or one extra reasoning demand
```

The first rung in a cluster may be a clean diagnostic. Later rungs remain unsupported attempts unless an earlier rung has already triggered instruction.

### Round 2 - mixed pre-IMO transfer

Round 2 is the clean mixed retrieval stage.

Rules:

- shuffle concept families;
- remove cluster headings that reveal the method;
- use mostly Grade 4 core / pre-IMO application with some Grade 3 retrieval;
- do not show helper representations;
- use plausible distractors;
- vary wording, number size, context, and clue order;
- include a small number of higher-demand questions without turning the whole round into Achievers.

Round 2 answers are useful evidence only if solved without the Help Book.

If Round 2 help is needed, the Round 2 question may itself be converted to a worked example, but it is then burned for transfer evidence and a later unseen item is required.

## 9. Round 1 cluster design rules

A good Round 1 cluster should have **conceptual continuity**.

Bad:

```text
place value -> Roman numerals -> interval counting -> forming numbers
```

Better:

```text
place value of a digit
-> place value in a 5-digit number
-> expanded/regrouped representation of the same idea
```

Another example:

```text
compare two familiar numbers
-> compare close 5-digit numbers
-> order four close 5-digit numbers / identify second-highest
```

The learner should feel, "I know what kind of thinking this is," before the task adds another layer.

## 10. Learner-facing language

Recommended labels:

```text
ROUND 1: CLIMB THE LADDER
YOUR QUESTION
LET'S WORK THIS ONE OUT TOGETHER
IF THIS PART IS HARD...        # optional probe
SEE IT THIS WAY
YOUR STEP
TRY ONE

ROUND 2: MIX IT UP
```

Do not expose:

```text
assessment
converted_worked_example
diagnostic_probe
Part B
Part C
fade
transfer
module ID
```

## 11. Logical Reasoning adaptation

The conversion rule applies directly to Logical Reasoning.

If a reasoning question is difficult, annotate the exact original figures, sequence, path, code, or clues.

Examples:

```text
sequence
-> mark the change from frame 1 to frame 2
-> child checks whether the same change repeats
-> close sequence with one feature changed

analogy
-> expose the A-to-B relation on the original pair
-> child applies it to C
-> close analogy with new symbols

direction
-> draw the first move/turn from the original path
-> child completes the remaining path
-> close path with changed directions

ranking
-> place one original clue on a line
-> child places the next clue
-> close ranking problem with new names

rotation/reflection
-> trace the first transformation on the original figure
-> child identifies the next transformation
-> close figure with changed orientation
```

The aim is to teach a reusable reasoning routine, not merely reveal the answer.

## 12. Presentation requirements

For printable Grade 3-4 material:

- one dominant idea per page;
- original question at the top;
- conversion message immediately after it when help is used;
- short, child-friendly wording;
- large readable type;
- consistent alignment;
- one useful representation rather than decorative clutter;
- child response space embedded inside the example;
- close-practice item spatially separated from the worked example;
- avoid too many equally prominent sections;
- preserve whitespace;
- use visual flow from top to bottom.

## 13. Planner contract

```text
ROUND 1 CLUSTER
   |
   v
rung attempted
   |
   +-- independent -> next rung in same concept family
   |
   +-- difficult
          |
          v
   convert exact rung to worked example
          |
          +-- uncertainty about prerequisite? -> optional small probe
          |
          v
   expose first useful structure
          |
          v
   child completes a key step
          |
          v
   close new item
          |
          v
   continue cluster / fade support

AFTER CLUSTERS
   |
   v
ROUND 2 MIXED PRE-IMO
   |
   +-- independent success -> independent evidence
   |
   +-- difficult -> may convert to instruction, but burn item for transfer evidence
                      |
                      v
                later unseen transfer
```

## 14. Non-goals

This schema does not:

- randomize Round 1 as if it were an exam;
- force a Quick Check onto every help page;
- count a taught original question as independent mastery;
- solve every difficult question completely for the learner;
- keep the learner on one concept forever;
- jump from a worked example directly to an Achievers-level problem;
- use visual support merely because a question is hard;
- infer a broad ability deficit from one wrong item;
- expose internal taxonomy to the child.
