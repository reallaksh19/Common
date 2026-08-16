# Grade 3 -> Grade 4 Number Sense Bridge Schema

## Purpose

This document defines the Numbers / Number Sense bridge for a learner moving from Grade 3 into Grade 4 IMO preparation.

The bridge should not be a random collection of number questions.

Round 1 is a **concept-cluster learning ladder**. Round 2 is a **mixed pre-IMO transfer round**.

## Curriculum boundary

For the current SOF IMO structure:

- Class 3 Number Sense uses 4-digit numbers.
- Class 4 Number Sense extends to more than 4-digit numbers.
- Class 4 Large Numbers topics include place value, number names, expanded/short form, comparing, ordering, forming numbers, rounding, even/odd numbers, and Roman numerals.

Factors and Multiples belongs to a separate Class 4 chapter and should not be silently mixed into the Number Sense bridge unless the activity is explicitly broader than Number Sense.

## Round 1 role

Round 1 is not an exam simulation.

It should be generated as several short climbs. Each climb keeps the underlying idea stable while increasing one demand at a time.

Recommended Round 1 clusters:

### C1 - Place value and representation

```text
R1: 4-digit place/face value retrieval
R2: place value in a 5-digit number
R3: expanded/regrouped representation of a 5-digit number
```

Atomic skills:

```text
identify_digit_place
identify_place_value
read_place_value_chart
compose_from_expanded_form
decompose_to_expanded_form
regroup_place_value_units
```

### C2 - Compare and order

```text
R1: compare two familiar 4-digit numbers
R2: compare close 5-digit numbers / boundary crossing
R3: order several close 5-digit numbers or identify second-highest/second-lowest
```

Atomic skills:

```text
compare_left_to_right
recognize_number_of_digits
compare_close_numbers
order_multiple_numbers
identify_ranked_number
```

### C3 - Form numbers under rules

```text
R1: form greatest/smallest number from digits
R2: handle zero correctly in the leading position
R3: add one condition such as odd/even or greater-than boundary
```

Atomic skills:

```text
form_greatest_number
form_smallest_number
handle_zero_in_number_formation
use_parity_constraint
use_boundary_constraint
optimize_under_constraints
```

### C4 - Rounding

```text
R1: round 4-digit number to nearest 10/100
R2: round 5-digit number to nearest 100/1000
R3: reverse or reasoning item: identify a number/range from its rounded value
```

Atomic skills:

```text
identify_rounding_place
inspect_next_digit
round_up_or_down
round_large_number
reason_from_rounded_value
```

### C5 - Roman numerals

```text
R1: recall common symbols / simple additive form
R2: convert a two-digit number using subtraction notation
R3: compare or correct a Roman numeral expression
```

Atomic skills:

```text
roman_symbol_value
roman_additive_form
roman_subtractive_form
convert_roman_to_hindu_arabic
convert_hindu_arabic_to_roman
validate_roman_numeral
```

## Optional C0 - number names

Number names may be embedded in C1 if the learner is already secure.

If not secure, use a short C0 bridge:

```text
4-digit number name
-> 5-digit number name
-> match number name to numeral with zero in an interior place
```

## Round 1 generation constraints

Each cluster should normally contain 3 items.

Difficulty progression:

```text
late Grade 3 retrieval
-> direct Grade 4 extension
-> Grade 4 application / one extra reasoning demand
```

Only one major new demand should be introduced between neighboring items.

Do not create a sequence such as:

```text
place value -> Roman numeral -> rounding -> number formation
```

inside one climb.

The learner should be able to reuse the previous item's method.

## Question-to-example behavior inside Round 1

When a Round 1 rung is difficult:

```text
original rung
-> LET'S WORK THIS ONE OUT TOGETHER
-> same rung becomes worked/partial example
-> optional small diagnostic check only if needed
-> child finishes a key step
-> close replacement item
-> continue the cluster
```

The converted rung is burned for independent evidence.

The replacement item should be conceptually adjacent, not merely numerically easier.

## Round 2 role

Round 2 is mixed retrieval and pre-IMO transfer.

Remove cluster headings and mix the families.

Suggested composition for a Grade 3 -> Grade 4 bridge:

```text
~40% Grade 3 retrieval / bridge content
~60% Grade 4 current-class Number Sense
```

This reflects the broad SOF Level 1 current/previous-class balance, while the exact distribution may be adjusted for the learner's evidence.

Recommended demand mix:

```text
20% bridge / confidence items
45% Grade 4 core
25% pre-IMO transfer
10% higher-demand but not full Achievers
```

Round 2 should include:

- mixed concepts;
- close distractors;
- changed wording;
- some context such as codes, serial numbers, labels, or records;
- no supplied instructional representation;
- no cluster title that reveals the method.

## Evidence interpretation

Round 1 is primarily a learning-boundary instrument.

Do not reduce it to a single percentage score.

Track per cluster:

```yaml
clusterId: NUM-C3-forming-numbers
entryRung: independent
grade4Rung: supported
applicationRung: not_attempted
convertedExamples:
  - NUM-R1-C3-Q2
currentState: supported
```

Round 2 is stronger evidence of transfer because concepts are mixed.

```yaml
round2Item:
  itemId: NUM-R2-Q07
  cluster: forming_numbers
  result: correct
  supportUsed: []
  recognitionCueFromClusterHeading: false
  stateAfter: independent
```

## Distractor design

Distractors should reflect plausible errors.

Examples:

### Place value

- face value instead of place value;
- one place shifted left/right;
- regrouping error.

### Compare/order

- compare last digits first;
- ignore number of digits;
- confuse second-highest with second-lowest.

### Forming numbers

- leading zero;
- parity rule violated;
- boundary rule violated;
- valid number but not smallest/greatest.

### Rounding

- round to wrong place;
- inspect wrong digit;
- always round up;
- retain digits that should become zero.

### Roman numerals

- additive form used where subtractive form is needed;
- symbol order reversed;
- wrong symbol value.

## Presentation

Round 1:

- show cluster names in child-friendly language;
- show a simple 1 -> 2 -> 3 climb graphic;
- one cluster per page or spread where practical;
- maintain similar visual structure across the three rungs;
- do not include hints on the initial attempt;
- if help is needed, use a separate question-to-example page or clearly separated help area.

Round 2:

- remove cluster labels;
- number questions consecutively;
- use exam-like MCQ formatting;
- preserve generous spacing;
- avoid decorative images unless mathematically relevant.

## Child-facing cluster names

Suggested labels:

```text
CLIMB 1 - BUILD THE NUMBER
CLIMB 2 - WHICH NUMBER IS BIGGER?
CLIMB 3 - MAKE THE NUMBER
CLIMB 4 - ROUND IT
CLIMB 5 - ROMAN NUMBERS
```

The backend retains the precise atomic skill labels.

## Non-goals

This bridge does not:

- mix every Numbers-related chapter into Number Sense;
- randomize Round 1;
- use only easy questions to build confidence;
- keep the learner at Grade 3 level after success;
- treat the final question in a cluster as Achievers by default;
- count a converted worked example as independent success;
- expose skill IDs or grade-band labels to the learner.
