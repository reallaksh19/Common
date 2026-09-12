# Grade 4 Mathematics — Division Concept, Learning & Question-Bank Schema

**Status:** Division-specific Grade 4 production blueprint  
**Parent standard:** `Grade4MathSchema.md`  
**Primary use cases:** textbook-quality Division chapter creation, adaptive tutoring, source-grounded question banks, school assessment, reasoning/HOTS practice, Olympiad bridge material, teacher/student editions, and diagnostic analytics.  
**Design principle:** Division is not one procedure. A Grade 4 learner must build meaning, connect representations, understand the multiplication–division relationship, estimate and reason about quotients, develop flexible strategies, interpret remainders, recognize division structures in problems, explain methods, diagnose errors, and transfer the idea to unfamiliar situations.

---

# 1. Purpose

This document applies the Grade 4 Mathematics production schema specifically to **Division**.

It is designed to prevent a shallow chapter of the form:

```text
rule
→ worked example
→ 20 calculations
→ word problems
→ test
```

Instead, the chapter should develop a connected learning system:

```text
MEANING
  ↓
CONCRETE EXPERIENCE
  ↓
PICTORIAL / STRUCTURAL MODELS
  ↓
MULTIPLICATION–DIVISION CONNECTION
  ↓
SYMBOLIC REPRESENTATION
  ↓
FACT FLUENCY
  ↓
ESTIMATION / QUOTIENT SENSE
  ↓
PLACE-VALUE STRATEGIES
  ↓
EFFICIENT PROCEDURE
  ↓
REMAINDERS
  ↓
WORD-PROBLEM STRUCTURES
  ↓
REASONING / EXPLANATION
  ↓
ERROR ANALYSIS
  ↓
TRANSFER / OLYMPIAD
```

The central instructional object is a **Division Learning Cell**. Individual questions are instances underneath a Learning Cell; they are not the chapter architecture themselves.

---

# 2. Scope gate

## 2.1 Default Grade 4 scope

Unless the supplied curriculum/source says otherwise, this blueprint assumes Grade 4 Division may include:

- division as equal sharing;
- division as forming equal groups;
- division vocabulary and notation;
- connection between multiplication and division;
- fact families and missing-factor reasoning;
- visual/structural representations;
- division facts and mental strategies;
- estimating quotients;
- division of larger whole numbers by one-digit divisors;
- place-value decomposition / partial quotient thinking;
- regrouping and efficient written methods;
- quotient with remainder;
- interpreting remainders in context;
- one-step and multi-step division problems;
- operation and strategy selection;
- explanation, justification, comparison, and error analysis;
- non-routine transfer and Olympiad bridge questions.

## 2.2 Do not silently extend scope

Do not introduce the following as core Grade 4 content unless present in the source/curriculum:

- decimal division;
- fraction division;
- algebraic long-division notation beyond age-appropriate missing-number equations;
- divisibility-rule formalism as a major topic;
- multi-digit divisors if not required;
- ratio/proportion formalism;
- negative-number division.

If an external source contains these, tag them as `OUT_OF_CORE_SCOPE`, `EXTENSION`, or the relevant curriculum-specific status.

---

# 3. Chapter big ideas

Every Division chapter should explicitly preserve these conceptual invariants.

## BI-1 — Division organizes a total into equal-sized relationships

Division is meaningful only when equality of groups/shares matters.

## BI-2 — Division has two fundamental situations

### Partitive / sharing division

Known:

- total amount;
- number of groups.

Unknown:

- amount in each group.

```text
24 objects shared equally among 6 children
→ how many does each child receive?
```

### Quotitive / grouping division

Known:

- total amount;
- amount in each group.

Unknown:

- number of groups.

```text
24 objects packed 6 per box
→ how many boxes can be made?
```

Both may be represented by `24 ÷ 6 = 4`, but the meanings of `6` and `4` are different.

## BI-3 — Multiplication and division are inverse relationships

```text
6 × 4 = 24
24 ÷ 6 = 4
24 ÷ 4 = 6
```

The connection should be used for:

- fact fluency;
- missing-number reasoning;
- checking answers;
- understanding quotient/divisor roles;
- developing efficient strategies.

## BI-4 — Place value explains multi-digit division

The written procedure must grow from place-value reasoning, not replace it.

Example conceptual decomposition:

```text
84 ÷ 4
= (80 ÷ 4) + (4 ÷ 4)
= 20 + 1
= 21
```

## BI-5 — A remainder has meaning

A remainder is not decorative notation. It may mean:

- items left over;
- an incomplete group;
- one additional container/group is required;
- only full groups count;
- the remainder itself is the answer;
- the problem should report quotient and remainder.

## BI-6 — Quotients should make sense before and after exact calculation

Learners should develop quotient magnitude and estimation sense.

## BI-7 — A division problem is recognized by structure, not keywords

Words such as `each`, `shared`, `left`, or `groups` are clues, not rules. The child must identify what is known and what is unknown.

## BI-8 — Mastery includes explanation and transfer

Calculation fluency alone is insufficient evidence of Division mastery.

---

# 4. Division concept graph

Use stable IDs so questions, diagnostics, practice, mastery, and analytics can link to the same concepts.

```text
DIVISION
│
├── DIV-M1 MEANING OF DIVISION
│   ├── DIV-M1.1 Equal sharing / find group size
│   ├── DIV-M1.2 Equal grouping / find number of groups
│   ├── DIV-M1.3 Equal-group invariant
│   ├── DIV-M1.4 Repeated subtraction connection
│   ├── DIV-M1.5 Division notation and vocabulary
│   └── DIV-M1.6 Distinguish sharing from grouping
│
├── DIV-M2 MULTIPLICATION–DIVISION RELATIONSHIP
│   ├── DIV-M2.1 Inverse operations
│   ├── DIV-M2.2 Fact families
│   ├── DIV-M2.3 Missing-factor reasoning
│   ├── DIV-M2.4 Check division using multiplication
│   └── DIV-M2.5 Unknown-position equations
│
├── DIV-M3 REPRESENT DIVISION
│   ├── DIV-M3.1 Concrete objects / counters
│   ├── DIV-M3.2 Equal-group drawings
│   ├── DIV-M3.3 Arrays
│   ├── DIV-M3.4 Number line / repeated jumps
│   ├── DIV-M3.5 Bar models
│   ├── DIV-M3.6 Place-value models
│   ├── DIV-M3.7 Equations
│   └── DIV-M3.8 Translate between representations
│
├── DIV-M4 DIVISION FACTS & MENTAL STRATEGIES
│   ├── DIV-M4.1 Use known multiplication facts
│   ├── DIV-M4.2 Divide by 1
│   ├── DIV-M4.3 Divide a nonzero number by itself
│   ├── DIV-M4.4 Related facts and patterns
│   ├── DIV-M4.5 Decompose a dividend mentally
│   └── DIV-M4.6 Choose an efficient mental strategy
│
├── DIV-M5 ESTIMATE QUOTIENTS
│   ├── DIV-M5.1 Benchmark quotient size
│   ├── DIV-M5.2 Compatible numbers
│   ├── DIV-M5.3 Nearby multiples of divisor
│   ├── DIV-M5.4 Estimate before calculating
│   ├── DIV-M5.5 Bound a quotient
│   └── DIV-M5.6 Judge reasonableness
│
├── DIV-M6 MULTI-DIGIT DIVISION
│   ├── DIV-M6.1 Place-value decomposition
│   ├── DIV-M6.2 Distributive reasoning
│   ├── DIV-M6.3 Partial quotients
│   ├── DIV-M6.4 Regrouping
│   ├── DIV-M6.5 Written division procedure
│   ├── DIV-M6.6 Internal zeros / place-value attention
│   ├── DIV-M6.7 Check with multiplication
│   └── DIV-M6.8 Compare strategies
│
├── DIV-M7 REMAINDERS
│   ├── DIV-M7.1 Meaning of remainder
│   ├── DIV-M7.2 Quotient and remainder notation
│   ├── DIV-M7.3 Remainder must be smaller than divisor
│   ├── DIV-M7.4 Verify dividend = divisor × quotient + remainder
│   ├── DIV-M7.5 Interpret remainder: leftovers
│   ├── DIV-M7.6 Interpret remainder: one more group needed
│   ├── DIV-M7.7 Interpret remainder: full groups only
│   ├── DIV-M7.8 Interpret remainder: remainder is target
│   └── DIV-M7.9 Choose correct answer form from context
│
├── DIV-M8 WORD-PROBLEM STRUCTURES
│   ├── DIV-M8.1 Find group size
│   ├── DIV-M8.2 Find number of groups
│   ├── DIV-M8.3 Find total / inverse connection
│   ├── DIV-M8.4 Find missing divisor
│   ├── DIV-M8.5 Remainder-context problem
│   ├── DIV-M8.6 Choose operation
│   ├── DIV-M8.7 Multi-step division problem
│   ├── DIV-M8.8 Relevant vs irrelevant information
│   ├── DIV-M8.9 Missing information / cannot determine
│   └── DIV-M8.10 Multiple possible solutions
│
├── DIV-M9 MATHEMATICAL REASONING
│   ├── DIV-M9.1 Explain a division model
│   ├── DIV-M9.2 Explain a strategy
│   ├── DIV-M9.3 Compare two strategies
│   ├── DIV-M9.4 Decide which method is efficient
│   ├── DIV-M9.5 Explain why an answer is reasonable
│   ├── DIV-M9.6 Error analysis
│   ├── DIV-M9.7 Missing-value reasoning
│   ├── DIV-M9.8 Constraint reasoning
│   └── DIV-M9.9 Generalize a pattern
│
└── DIV-M10 TRANSFER / OLYMPIAD BRIDGE
    ├── DIV-M10.1 Reverse problems
    ├── DIV-M10.2 Multiple constraints
    ├── DIV-M10.3 Remainder patterns
    ├── DIV-M10.4 Range / possibility problems
    ├── DIV-M10.5 Multiple valid answers
    ├── DIV-M10.6 Logic + division
    ├── DIV-M10.7 Representation-hidden problems
    └── DIV-M10.8 Multi-concept transfer
```

---

# 5. Prerequisite graph

Each microconcept stores prerequisites with dependency strength.

```text
CRITICAL   — concept is unlikely to be learned reliably without it
STRONG     — weakness substantially increases difficulty
SUPPORTING — useful but not required for every item
```

## 5.1 Chapter prerequisite map

```text
Counting / equal groups
        ↓
Addition and repeated addition
        ↓
Multiplication meaning
        ↓
Multiplication facts
        ↓
Multiplication–division relationship
        ↓
Division facts
        ↓
Place value + decomposition
        ↓
Multi-digit division strategies
        ↓
Remainders
        ↓
Problem interpretation
        ↓
Multi-step / transfer reasoning
```

## 5.2 Example prerequisite record

For `156 ÷ 3`:

```json
{
  "prerequisites": [
    {"id": "MUL-FACT-3", "strength": "CRITICAL"},
    {"id": "DIV-M1", "strength": "CRITICAL"},
    {"id": "PV-DECOMPOSE", "strength": "CRITICAL"},
    {"id": "ADD-COMPONENTS", "strength": "STRONG"},
    {"id": "DIV-M5-ESTIMATE", "strength": "SUPPORTING"}
  ]
}
```

A diagnostic system should descend this graph rather than merely issue another random Division question.

---

# 6. Learning progression model

Every Division microconcept should be taught through a deliberate progression.

```text
1 EXPERIENCE
  learner encounters a meaningful equal-sharing/grouping situation

2 NOTICE
  learner identifies equality, total, groups, group size, unknown

3 MODEL
  learner acts, draws, arranges, jumps, partitions, or uses blocks

4 REPRESENT
  learner connects the model to an equation

5 CONNECT
  learner links division to multiplication / repeated subtraction / place value

6 GENERALIZE
  learner states a transferable rule or relationship

7 PRACTISE
  learner works carefully varied instances

8 CHOOSE
  learner chooses representation / strategy / operation

9 EXPLAIN
  learner communicates why the method works

10 TRANSFER
  learner applies the idea in a changed or hidden structure
```

A textbook chapter should not skip directly from `EXPERIENCE` to `PROCEDURE` unless the source explicitly assumes prior mastery.

---

# 7. Representation ladder

Representation is a learning dimension, not artwork.

```text
R0 — CONCRETE
objects, counters, manipulatives, physical sharing/grouping

R1 — PICTORIAL
object drawings, equal groups, circles, tally-like drawings

R2 — STRUCTURAL MODEL
arrays, bar models, number lines, place-value blocks, area/partition models

R3 — SYMBOLIC
division equation, multiplication inverse, missing-number equation

R4 — STRATEGIC
mental decomposition, known facts, compatible numbers, partial quotients

R5 — PROCEDURAL
efficient written algorithm

R6 — ABSTRACT REASONING
compare, explain, constrain, reverse, generalize, prove reasonableness
```

Each question records:

```json
{
  "representation": {
    "input_level": "R2_STRUCTURAL_MODEL",
    "input_type": "ARRAY",
    "expected_working_level": "R3_SYMBOLIC",
    "expected_working_type": "DIVISION_EQUATION",
    "output_level": "R3_SYMBOLIC",
    "output_type": "NUMBER"
  }
}
```

## 7.1 Representation translation pairs

The bank should deliberately contain:

```text
objects → picture
picture → equation
equation → picture
array → division equation
bar model → equation
word problem → model
word problem → equation
equation → word problem
written procedure → place-value explanation
place-value model → written procedure
```

---

# 8. Number-structure progression

Random number changes are not sufficient question variation. Number structure changes the cognitive demand.

## 8.1 Number-structure dimensions

```text
dividend size
divisor size
exact vs non-exact division
fact-family familiarity
regrouping required
number of regroupings
internal zero
trailing zero
near-compatible dividend
quotient digit count
remainder size
relationship between dividend and divisor
```

## 8.2 Suggested progression

### NS-1 — Direct fact structure

```text
24 ÷ 6
35 ÷ 5
56 ÷ 8
```

### NS-2 — Easy place-value decomposition

```text
84 ÷ 4
96 ÷ 3
63 ÷ 3
```

### NS-3 — Decomposition requiring a non-obvious split

```text
72 ÷ 4
96 ÷ 6
85 ÷ 5
```

### NS-4 — Larger exact quotient

```text
156 ÷ 3
248 ÷ 4
```

### NS-5 — Remainder introduced

```text
86 ÷ 4
95 ÷ 3
67 ÷ 5
```

### NS-6 — Place-value attention / zeros

```text
408 ÷ 4
606 ÷ 6
```

Only include forms aligned with the actual source/curriculum.

## 8.3 Canonical number-structure record

```json
{
  "number_structure": {
    "dividend": 156,
    "dividend_digits": 3,
    "divisor": 3,
    "divisor_digits": 1,
    "exact_division": true,
    "remainder": 0,
    "regrouping_required": true,
    "internal_zero": false,
    "compatible_number_proximity": "MEDIUM",
    "fact_families_required": ["3-times-table"]
  }
}
```

---

# 9. Division Learning Cell schema

Each microconcept should have one or more Learning Cells.

```yaml
learning_cell:
  id: DIV-LC-...
  macroconcept: ...
  microconcept: ...
  status: CORE | REVIEW | EXTENSION | OLYMPIAD_BRIDGE

  objective: ...
  success_criteria: []
  big_idea: ...
  child_friendly_meaning: ...
  concept_invariant: ...

  vocabulary: []
  prerequisites: []
  connections: []

  launch_context: ...

  representation_sequence:
    concrete: ...
    pictorial: ...
    structural: ...
    symbolic: ...
    strategic: ...
    procedural: ...

  what_to_notice: []
  recognition_cues: []
  concept_trigger: ...

  strategies: []
  expected_reasoning_path: []

  worked_examples: []
  guided_practice: []
  variation_practice: []
  independent_practice: []
  mixed_spiral_practice: []

  misconceptions: []
  diagnostic_probes: []
  repair_paths: []

  mastery_evidence: []
  transfer_tasks: []
```

---

# 10. Core Learning Cells for the Division chapter

The exact chapter sequence should follow the source, but the following cells define a strong default architecture.

## LC-01 — Division as equal sharing

**Microconcept:** `DIV-M1.1`  
**Objective:** Given a total and number of equal groups, find the amount in each group.  
**Big idea:** Sharing equally means every group receives the same amount.  
**Child-friendly meaning:** “I know how many groups there are. I need to find how many go in each group.”  
**Invariant:** every share is equal.

**Representation sequence:**

```text
physical sharing
→ equal-group picture
→ bar/equal-parts model
→ division equation
→ multiplication check
```

**What to notice:**

- the total is known;
- the number of groups/people is known;
- `each group` is the unknown;
- all groups must be equal.

**Concept trigger:**

```text
total + number of equal groups + find each share
→ sharing division
```

**Canonical archetypes:** model, model-to-equation, word problem, inverse check, explanation, error analysis.

**Common misconception:** subtract the number of groups once rather than share the total equally.

**Mastery evidence:** child can act it, draw it, write the equation, solve it, and explain what the quotient means.

---

## LC-02 — Division as forming equal groups

**Microconcept:** `DIV-M1.2`  
**Objective:** Given a total and amount per group, determine number of groups.  
**Child-friendly meaning:** “I know how many belong in one group. I need to find how many groups I can make.”

**Representation sequence:**

```text
make groups physically
→ circle equal groups
→ repeated jumps/subtraction
→ equation
→ multiplication check
```

**What to notice:**

- total known;
- size of each group known;
- number of groups unknown.

**Concept trigger:**

```text
total + amount in each group + find how many groups
→ grouping division
```

**Mastery discriminator:** learner can distinguish this structure from LC-01 even when both use the same numeric equation.

---

## LC-03 — Connect multiplication and division

**Microconcepts:** `DIV-M2.1–M2.5`  
**Objective:** Use multiplication relationships to solve and verify division equations.

**Core relationship:**

```text
if 6 × 4 = 24,
then 24 ÷ 6 = 4
and 24 ÷ 4 = 6
```

**Question variation:**

```text
6 × □ = 24
24 ÷ 6 = □
24 ÷ □ = 4
□ ÷ 6 = 4
```

**Misconception target:** treating operand positions as arbitrary.

**Mastery evidence:** solve missing values, create fact families, explain inverse relationship, verify division by multiplication.

---

## LC-04 — Represent division flexibly

**Microconcepts:** `DIV-M3.1–M3.8`  
**Objective:** Translate among objects, groups, arrays, number lines, bar models, and equations.

**Mastery requirement:** at least one task in each direction:

```text
model → equation
equation → model
story → model
model → story
```

**Misconception target:** selecting a picture because it contains the same numbers but does not preserve equal-group structure.

---

## LC-05 — Division facts and mental strategies

**Microconcepts:** `DIV-M4.*`  
**Objective:** Use multiplication facts, patterns, and decomposition to find quotients efficiently.

**Strategies may include:**

- known multiplication fact;
- missing factor;
- split dividend into divisible parts;
- use a nearby fact;
- repeated subtraction when instructionally appropriate.

**Strategy-choice prompt:**

> Which method is quickest for this number structure, and why?

The bank should not require the same strategy for every item unless the lesson is explicitly teaching that strategy.

---

## LC-06 — Estimate and reason about quotients

**Microconcepts:** `DIV-M5.*`  
**Objective:** Predict quotient magnitude and use compatible multiples to estimate/check.

**What to notice:**

- nearby multiples of divisor;
- whether quotient should be tens, hundreds, etc.;
- whether proposed answer is plausible.

**Question types:** estimate only, choose best estimate, bound quotient, reject unreasonable answer, estimate then calculate, compare exact answer with estimate.

---

## LC-07 — Multi-digit division through place value

**Microconcepts:** `DIV-M6.1–M6.4`  
**Objective:** Decompose a multi-digit dividend into parts that can be divided and recombined.

**Example conceptual path:**

```text
156 ÷ 3
= (120 ÷ 3) + (36 ÷ 3)
= 40 + 12
= 52
```

The decomposition need not be unique. This cell should celebrate valid efficient decompositions before standardizing a procedure.

**Question types:** complete decomposition, choose useful decomposition, compare decompositions, explain a partial quotient, repair incorrect decomposition.

---

## LC-08 — Efficient written division procedure

**Microconcepts:** `DIV-M6.4–M6.7`  
**Objective:** Use an age-appropriate written method while retaining quotient-place-value meaning.

Every written step should be connectable to:

```text
estimate / choose quotient amount
multiply
subtract / find what remains
regroup if needed
continue
check
```

Do not present the algorithm as unexplained symbol manipulation.

**Diagnostic requirement:** distinguish procedural error from weak facts, place-value error, or concept error.

---

## LC-09 — Understand and interpret remainders

**Microconcepts:** `DIV-M7.*`  
**Objective:** Compute and interpret quotient/remainder according to mathematical and story context.

**Required remainder cases:**

```text
A. report quotient and remainder
B. leftover amount matters
C. one more group/container is required
D. count only full groups
E. remainder itself is target
```

Example distinction:

```text
26 children, 4 per car
6 R2 mathematically
but 7 cars are required
```

versus:

```text
26 cookies, 4 per bag
6 full bags with 2 cookies left
```

**Mastery requirement:** learner must not automatically use one interpretation for every remainder problem.

---

## LC-10 — Recognize Division in word problems

**Microconcepts:** `DIV-M8.1–M8.6`  
**Objective:** Identify quantities, unknown, equal-group relationship, and operation without keyword matching.

**Structure frame:**

```text
TOTAL
NUMBER OF GROUPS
SIZE OF EACH GROUP
UNKNOWN
```

Students should explicitly identify which of the three quantities is unknown.

---

## LC-11 — Multi-step Division problem solving

**Microconcept:** `DIV-M8.7`  
**Objective:** Decide the correct sequence of operations when Division occurs within a multi-step situation.

Required variations:

```text
combine then divide
divide then combine
multiply then divide
subtract then divide
divide then compare
```

Do not raise difficulty only by increasing numbers; raise it through planning and relationship reasoning.

---

## LC-12 — Explain, compare, diagnose, and transfer

**Microconcepts:** `DIV-M9.*`, `DIV-M10.*`  
**Objective:** Demonstrate flexible understanding beyond direct calculation.

Tasks include:

- explain why a strategy works;
- compare two methods;
- choose more efficient method;
- determine whether answer is reasonable;
- find and repair an error;
- solve reverse/missing-value problems;
- satisfy multiple constraints;
- find all possible values;
- reason about remainder patterns;
- solve Olympiad-bridge questions.

---

# 11. Word-problem structure taxonomy

Division word problems must be classified structurally, not by keywords.

## WP-A — Find group size

```text
Total known
Number of groups known
Group size unknown
```

## WP-B — Find number of groups

```text
Total known
Group size known
Number of groups unknown
```

## WP-C — Inverse / find total

```text
Group size known
Number of groups known
Total unknown
```

Useful for multiplication–division relationship.

## WP-D — Find missing divisor/group count

```text
Total known
Quotient known
Other multiplicative component unknown
```

## WP-E — Remainder interpretation

Calculation alone does not determine final response.

## WP-F — Multi-step

Division is one step among several.

## WP-G — Relevant/irrelevant information

Learner decides what matters.

## WP-H — Insufficient information

Correct conclusion may be `cannot determine`.

## WP-I — Multiple possible answers

Promotes open reasoning and constraint checking.

---

# 12. Question archetype library

Each microconcept should define which archetypes provide valid evidence.

```text
DIV-QA-01 DIRECT_CALCULATION
DIV-QA-02 DIRECT_FACT
DIV-QA-03 MODEL_DIVISION
DIV-QA-04 MODEL_TO_EQUATION
DIV-QA-05 EQUATION_TO_MODEL
DIV-QA-06 STORY_TO_MODEL
DIV-QA-07 MODEL_TO_STORY
DIV-QA-08 MISSING_VALUE
DIV-QA-09 FACT_FAMILY
DIV-QA-10 INVERSE_OPERATION
DIV-QA-11 ESTIMATE_QUOTIENT
DIV-QA-12 BOUND_QUOTIENT
DIV-QA-13 COMPARE_QUOTIENTS
DIV-QA-14 CHOOSE_STRATEGY
DIV-QA-15 COMPLETE_STRATEGY
DIV-QA-16 EXPLAIN_STRATEGY
DIV-QA-17 COMPARE_STRATEGIES
DIV-QA-18 WORD_PROBLEM_SHARING
DIV-QA-19 WORD_PROBLEM_GROUPING
DIV-QA-20 REMAINDER_CONTEXT
DIV-QA-21 MULTI_STEP
DIV-QA-22 ERROR_ANALYSIS
DIV-QA-23 REASONABLENESS
DIV-QA-24 OPEN_RESPONSE
DIV-QA-25 CREATE_A_PROBLEM
DIV-QA-26 REVERSE_PROBLEM
DIV-QA-27 CONSTRAINT_PROBLEM
DIV-QA-28 PATTERN_GENERALIZATION
DIV-QA-29 MULTIPLE_SOLUTIONS
DIV-QA-30 OLYMPIAD_TRANSFER
```

A strong bank samples several archetypes. It does not create twenty copies of `DIRECT_CALCULATION`.

---

# 13. Controlled variation engine

For each seed, generate deliberate transformations.

```text
SEED QUESTION
  │
  ├── number variation
  ├── exact ↔ remainder variation
  ├── sharing ↔ grouping meaning variation
  ├── model variation
  ├── representation-direction variation
  ├── unknown-position variation
  ├── inverse-operation variation
  ├── context variation
  ├── strategy requirement variation
  ├── estimate/exact variation
  ├── explanation variation
  ├── error-analysis variation
  ├── multi-step variation
  └── constraint / Olympiad variation
```

Every generated question should record which dimensions changed from its parent/anchor.

---

# 14. Division Learning Fingerprint

Every question should carry a fingerprint rich enough to distinguish mathematically different Division tasks.

```json
{
  "learning_fingerprint": {
    "chapter": "Division",
    "macroconcept_id": "DIV-M8",
    "microconcept_ids": ["DIV-M8.2"],

    "big_idea": "Division can determine how many equal groups can be made.",

    "division_meaning": "FIND_NUMBER_OF_GROUPS",

    "situation_structure": {
      "total": "KNOWN",
      "number_of_groups": "UNKNOWN",
      "group_size": "KNOWN"
    },

    "task_action": "SOLVE_WORD_PROBLEM",
    "question_archetype": "DIV-QA-19",

    "number_structure": {},

    "representation": {
      "input": "WORD_PROBLEM",
      "working": ["EQUATION"],
      "output": "NUMBER_WITH_UNIT"
    },

    "recognition_cues": [
      "total amount is known",
      "same amount is placed in every group",
      "question asks how many groups"
    ],

    "reasoning_moves": [
      "IDENTIFY_TOTAL",
      "IDENTIFY_GROUP_SIZE",
      "IDENTIFY_UNKNOWN",
      "RECOGNIZE_EQUAL_GROUP_STRUCTURE",
      "SELECT_DIVISION",
      "FORM_EQUATION",
      "CALCULATE_QUOTIENT",
      "INTERPRET_ANSWER"
    ],

    "strategy": "OPEN",

    "knowledge_components": [
      "division meaning",
      "multiplication facts",
      "equal groups"
    ],

    "constraints": [],
    "answer_form": "WHOLE_NUMBER_WITH_CONTEXT_UNIT",

    "concept_invariant": "Every group has equal size.",

    "expected_reasoning_path": [
      "identify quantities",
      "identify unknown",
      "recognize grouping division",
      "divide",
      "interpret quotient"
    ]
  }
}
```

---

# 15. Difficulty profile for Division

Score dimensions independently. A single overall value is optional and secondary.

```json
{
  "difficulty": {
    "concept_demand": 0,
    "fact_fluency_demand": 0,
    "place_value_demand": 0,
    "recognition_demand": 0,
    "representation_demand": 0,
    "strategy_selection_demand": 0,
    "procedure_demand": 0,
    "calculation_demand": 0,
    "language_demand": 0,
    "working_memory_demand": 0,
    "remainder_interpretation_demand": 0,
    "reasoning_step_count": 0,
    "transfer_distance": 0,
    "overall": 0
  }
}
```

## 15.1 Why the vector matters

`864 ÷ 4` may have high procedural/calculation load but low recognition load.

A bus-capacity problem involving `98 ÷ 8` may have easier arithmetic but much higher recognition and remainder-interpretation demand.

Do not rank the first automatically as more difficult because its numbers are larger.

---

# 16. What Should I Notice? taxonomy

`what_to_notice` is a designed teaching layer, not filler text.

Use one or more categories:

```text
STRUCTURE
UNKNOWN
NUMBER
FACT
PLACE_VALUE
PATTERN
REPRESENTATION
LANGUAGE
CONNECTION
CONSTRAINT
REMAINDER
REASONABLENESS
```

Example:

```json
{
  "what_to_notice": [
    {
      "type": "STRUCTURE",
      "text": "The total is being separated into equal-sized groups."
    },
    {
      "type": "UNKNOWN",
      "text": "The number in each group is known, but the number of groups is not."
    },
    {
      "type": "CONNECTION",
      "text": "A multiplication fact can help you find the quotient."
    }
  ]
}
```

Avoid empty prompts such as `read carefully` or `look at the numbers`.

---

# 17. Recognition cue and concept trigger

Keep these separate.

## Recognition cue

Question-specific clue:

```text
“8 students fit in each van”
```

## Concept trigger

Transferable rule:

```text
total + size of each group + find number of groups
→ divide
```

A tutor should gradually fade recognition cues while preserving the concept trigger in review/feedback.

---

# 18. Helper architecture

Helpers are teacher-like prompts and should not give away the solution.

```json
{
  "helper": {
    "understand": "What does each number represent?",
    "unknown": "What are you trying to find?",
    "notice": "Are the groups supposed to be equal?",
    "represent": "Could you show this with groups, a bar, or an equation?",
    "connect": "Which multiplication fact might help?",
    "plan": "Which operation matches the relationship?",
    "check": "Does your answer fit the original situation?"
  }
}
```

Not every question needs every helper field.

---

# 19. Progressive hint ladder

Use five pedagogically distinct stages.

```text
H1 NOTICE     — direct attention to the important structure
H2 REMEMBER   — activate relevant prior knowledge
H3 REPRESENT  — help form a useful model/equation
H4 PLAN       — identify the strategy or critical reasoning step
H5 DO         — provide the near-execution step without replacing the worked solution
```

Recommended internal reveal values:

```text
H1 10%
H2 25%
H3 45%
H4 70%
H5 90%
```

Example for 98 pupils, 8 per van:

```text
H1 NOTICE
What does the 8 tell you about each van?

H2 REMEMBER
You know the total and the size of each group.

H3 REPRESENT
Write a division equation for total ÷ pupils per van.

H4 PLAN
After dividing, think about what any remainder represents.

H5 DO
If some pupils remain after filling the full vans, they need another van.
```

Hints attach to reasoning nodes rather than merely becoming longer versions of the same clue.

---

# 20. Solution architecture

Every solution should support learning, not just provide arithmetic.

```text
1 Strategy summary
2 Representation / equation
3 Step-by-step reasoning
4 Calculation
5 Contextual answer
6 Verification / reasonableness
7 Alternative strategy when useful
8 One-sentence takeaway
```

Example verification modes:

```text
MULTIPLICATION_CHECK
ESTIMATE
INVERSE_OPERATION
MODEL_CHECK
RANGE_CHECK
REMAINDER_CHECK
UNIT_CONTEXT_CHECK
ALTERNATIVE_METHOD
```

---

# 21. Misconception and error taxonomy

## 21.1 Error stages

```text
CONCEPT_ERROR
EQUAL_GROUP_ERROR
FACT_RECALL_ERROR
PLACE_VALUE_ERROR
REPRESENTATION_ERROR
UNKNOWN_IDENTIFICATION_ERROR
OPERATION_SELECTION_ERROR
STRATEGY_ERROR
PROCEDURE_ERROR
CALCULATION_SLIP
LANGUAGE_INTERPRETATION_ERROR
REMAINDER_RULE_ERROR
REMAINDER_CONTEXT_ERROR
REASONABLENESS_ERROR
```

## 21.2 Misconception library

### DIV-ERR-01 — Confuses sharing and grouping

Learner obtains a number but cannot explain whether it means group size or number of groups.

### DIV-ERR-02 — Keyword dependence

Learner treats `each` as automatically meaning multiplication or division without identifying structure.

### DIV-ERR-03 — Inverse relationship weak

Learner does not connect `24 ÷ 6` to `6 × ? = 24`.

### DIV-ERR-04 — Unequal groups accepted

Learner models division using groups of different sizes.

### DIV-ERR-05 — Repeated subtraction stops incorrectly

Learner miscounts groups/jumps.

### DIV-ERR-06 — Place-value decomposition invalid

Learner splits a number into parts that are then divided incorrectly or recombined incorrectly.

### DIV-ERR-07 — Quotient place-value loss

Learner produces digits without understanding tens/ones value.

### DIV-ERR-08 — Standard procedure step omitted/reordered

Procedure is memorized incompletely.

### DIV-ERR-09 — Remainder ≥ divisor accepted

Learner has not completed enough full groups.

### DIV-ERR-10 — Remainder ignored

Learner reports quotient when context requires more.

### DIV-ERR-11 — Always rounds quotient up

Learner generalizes container/bus logic to contexts where full groups only or leftovers matter.

### DIV-ERR-12 — Always reports `q R r`

Learner computes correctly but does not interpret story context.

### DIV-ERR-13 — Implausible quotient not detected

Learner lacks estimation/reasonableness check.

### DIV-ERR-14 — Divides numbers in presented order

Learner does not preserve quantity roles.

### DIV-ERR-15 — Multi-step premature division

Learner selects Division before determining the total or relevant quantity required for the division step.

---

# 22. Diagnostic record schema

Diagnostics should test hypotheses, not assume one cause from one wrong answer.

```json
{
  "diagnostic": {
    "observed_response": "...",
    "error_signature": "...",
    "possible_causes": [
      {
        "hypothesis": "PLACE_VALUE_ERROR",
        "confidence": "MEDIUM",
        "probe": "What is 120 ÷ 3?",
        "interpretation_if_correct": "Basic place-value division may be intact; test decomposition/recombination next.",
        "interpretation_if_wrong": "Repair division of tens/hundreds before retrying."
      }
    ],
    "repair_concept_ids": [],
    "repair_activity": "...",
    "repair_question_ids": [],
    "retry_policy": "ISOMORPHIC_NEW_NUMBERS_THEN_ORIGINAL"
  }
}
```

## 22.1 Diagnostic example: `156 ÷ 3 = 42`

Possible probe chain:

```text
What is 120 ÷ 3?
↓
What is 36 ÷ 3?
↓
Can 156 be written as 120 + 36?
↓
What is 40 + 12?
```

The system can distinguish weak facts from decomposition, recombination, or procedural misunderstanding.

---

# 23. Practice sequencing blueprint

Practice must be designed, not shuffled randomly.

For each Learning Cell:

```text
P0 prerequisite check
P1 teacher/worked model
P2 guided completion
P3 direct independent practice
P4 controlled number variation
P5 representation variation
P6 unknown-position variation
P7 word/application problem
P8 explanation / justification
P9 error-analysis item
P10 mixed/spiral item
P11 transfer item
```

Not every lesson requires all eleven stages, but chapter-level coverage should include them.

## 23.1 Interleaving rule

After initial acquisition, mix:

- sharing and grouping;
- exact and remainder cases;
- calculation and representation;
- direct and word problems;
- current and prior concepts.

Avoid blocks where the operation is obvious solely because every question on the page is Division.

---

# 24. Mastery model

Do not define mastery as `x correct out of y` alone.

## 24.1 Mastery dimensions

```text
M1 CONCEPTUAL
Can explain what division means and distinguish sharing/grouping.

M2 REPRESENTATIONAL
Can move among model, equation, and context.

M3 FACT / FLUENCY
Can retrieve/use appropriate facts accurately.

M4 PLACE VALUE / PROCEDURE
Can solve curriculum-appropriate multi-digit Division accurately.

M5 RECOGNITION / APPLICATION
Can recognize when Division is appropriate in an unfamiliar problem.

M6 STRATEGY
Can choose and explain an efficient strategy.

M7 REMAINDER INTERPRETATION
Can adapt final answer to context.

M8 REASONING
Can explain, compare, justify, and diagnose.

M9 TRANSFER
Can solve changed-representation, reverse, constraint, or non-routine tasks.
```

## 24.2 Suggested mastery evidence rule

A microconcept should require evidence from more than one archetype.

Example for `DIV-M1.2 Find number of groups`:

```text
✓ model task
✓ direct/equation task
✓ word problem
✓ changed context or representation
✓ explanation or reasoning task
```

The exact thresholds belong in learner-state logic, not the immutable content record.

---

# 25. Transfer ladder

```text
T0 PREREQUISITE_REPAIR
T1 NEAR_TWIN
T2 NUMBER_VARIATION
T3 REPRESENTATION_TRANSFER
T4 UNKNOWN_POSITION_TRANSFER
T5 CONTEXT_TRANSFER
T6 STRATEGY_TRANSFER
T7 MULTI_STEP_TRANSFER
T8 CONSTRAINT_REASONING
T9 OLYMPIAD_TRANSFER
```

Example lineage from `84 ÷ 4 = ?`:

```text
T1 96 ÷ 4
T2 86 ÷ 4 with remainder
T3 choose the array showing 84 ÷ 4
T4 □ ÷ 4 = 21
T5 84 objects packed 4 per box
T6 solve 84 ÷ 4 in two ways and compare
T7 combine two quantities then divide
T8 find all values in a range satisfying a division condition
T9 solve a multi-constraint remainder/pattern problem
```

Olympiad difficulty should emerge from **structure, constraints, reverse reasoning, pattern, and transfer**, not oversized arithmetic.

---

# 26. Similar-question / analogue schema

Do not store fixed fields `Analogue A`, `Analogue B`, etc. Use an array.

```json
{
  "analogues": [
    {
      "question_id": "...",
      "role": "REPRESENTATION_TRANSFER",
      "similarity": {
        "concept": 1.0,
        "division_meaning": 1.0,
        "reasoning": 0.9,
        "number_structure": 0.7,
        "surface_context": 0.3
      },
      "difference_summary": "Same grouping structure; model rather than word problem."
    }
  ]
}
```

Recommended roles:

```text
PREREQUISITE_REPAIR
NEAR_TWIN
NUMBER_VARIATION
REPRESENTATION_TRANSFER
UNKNOWN_TRANSFER
CONTEXT_TRANSFER
STRATEGY_TRANSFER
REINFORCEMENT
ADVANCED_TRANSFER
OLYMPIAD_TRANSFER
```

---

# 27. Canonical Division question object

```json
{
  "id": "DIV-G4-0001",

  "question": {
    "stem": "...",
    "question_type": "MCQ",
    "options": [],
    "correct_answer": "...",
    "answer_type": "WHOLE_NUMBER",
    "assets": []
  },

  "source": {
    "source_id": "...",
    "provenance_class": "...",
    "page": null,
    "question_number": null,
    "url": "...",
    "transcription_status": "VERIFIED_TRANSCRIPTION"
  },

  "classification": {
    "subject": "Mathematics",
    "grade": 4,
    "chapter": "Division",
    "macroconcept_id": "DIV-M8",
    "microconcept_ids": ["DIV-M8.2"],
    "learning_cell_id": "DIV-LC-02",
    "question_archetype": "DIV-QA-19"
  },

  "learning_fingerprint": {},
  "number_structure": {},
  "difficulty": {},
  "prerequisites": [],

  "what_to_notice": [],
  "recognition_cues": [],
  "concept_trigger": "...",
  "helper": {},
  "hints": [],

  "solution": {
    "strategy": "...",
    "representation": "...",
    "steps": [],
    "answer": "...",
    "context_interpretation": "...",
    "verification": "...",
    "alternative_methods": []
  },

  "misconceptions": [],
  "error_signatures": [],
  "diagnostic_probes": [],
  "repair_links": [],

  "takeaway": "...",
  "mastery_evidence_tags": [],
  "transfer_links": [],
  "analogues": []
}
```

---

# 28. Fully illustrated question record

Example problem:

> 98 pupils are going on a trip. Each van can carry 8 pupils. What is the least number of vans needed?

```json
{
  "id": "DIV-G4-REMAINDER-001",

  "classification": {
    "chapter": "Division",
    "macroconcept_id": "DIV-M7",
    "microconcept_ids": ["DIV-M7.6", "DIV-M8.5"],
    "learning_cell_id": "DIV-LC-09",
    "question_archetype": "DIV-QA-20"
  },

  "learning_fingerprint": {
    "division_meaning": "FIND_NUMBER_OF_GROUPS",
    "situation_structure": {
      "total": "KNOWN",
      "group_size": "KNOWN",
      "number_of_groups": "UNKNOWN"
    },
    "task_action": "SOLVE_AND_INTERPRET_REMAINDER",
    "representation": {
      "input": "WORD_PROBLEM",
      "working": "DIVISION_EQUATION",
      "output": "CONTEXTUAL_WHOLE_NUMBER"
    },
    "reasoning_moves": [
      "IDENTIFY_TOTAL",
      "IDENTIFY_CAPACITY",
      "IDENTIFY_UNKNOWN",
      "SELECT_DIVISION",
      "CALCULATE_QUOTIENT_AND_REMAINDER",
      "INTERPRET_REMAINDER",
      "ADJUST_FINAL_ANSWER"
    ],
    "concept_invariant": "Every pupil must be assigned to a van."
  },

  "number_structure": {
    "dividend": 98,
    "divisor": 8,
    "exact_division": false,
    "remainder": 2
  },

  "what_to_notice": [
    {
      "type": "UNKNOWN",
      "text": "We need the number of vans, not the number of pupils in each van."
    },
    {
      "type": "REMAINDER",
      "text": "Any pupils left after filling full vans still need transport."
    }
  ],

  "concept_trigger": "total + capacity of each group + find groups → divide; leftover people require another group",

  "helper": {
    "understand": "What do 98 and 8 represent?",
    "unknown": "Are you finding pupils per van or number of vans?",
    "check": "Will every pupil fit in the number of vans you found?"
  },

  "hints": [
    {"level": 1, "role": "NOTICE", "reveal": 10, "text": "Focus on how many pupils fit in one van."},
    {"level": 2, "role": "REMEMBER", "reveal": 25, "text": "You know the total and the size of each group."},
    {"level": 3, "role": "REPRESENT", "reveal": 45, "text": "Write 98 ÷ 8."},
    {"level": 4, "role": "PLAN", "reveal": 70, "text": "Interpret what any remainder means in this situation."},
    {"level": 5, "role": "DO", "reveal": 90, "text": "Twelve full vans do not carry the remaining two pupils, so another van is required."}
  ],

  "solution": {
    "strategy": "Divide total pupils by van capacity, then interpret the remainder.",
    "steps": [
      "98 ÷ 8 = 12 remainder 2.",
      "12 vans carry 96 pupils.",
      "2 pupils still need a van.",
      "Therefore one additional van is needed."
    ],
    "answer": "13 vans",
    "verification": "13 vans have enough capacity for all 98 pupils; 12 do not."
  },

  "misconceptions": [
    {
      "id": "DIV-ERR-10",
      "wrong_model": "Report 12 because 12 is the quotient.",
      "diagnostic_question": "Where will the remaining 2 pupils sit?",
      "repair": "Connect the remainder to the story before writing the final answer."
    }
  ],

  "takeaway": "A remainder must be interpreted using the situation; the quotient alone may not be the final answer."
}
```

---

# 29. Source and provenance policy

Every item must keep provenance distinct.

Recommended classes:

```text
USER_UPLOADED_ANCHOR
TEXTBOOK_SOURCE
OFFICIAL_CURRICULUM_ITEM
OFFICIAL_OLYMPIAD_OR_EXAM
PUBLISHED_REFERENCE
ORIGINAL_CALIBRATED
RECONSTRUCTED_FROM_SCAN
```

For derived questions, store:

```json
{
  "derived_from": ["DIV-SRC-014"],
  "variation_dimensions": [
    "NUMBER_VARIATION",
    "REPRESENTATION_TRANSFER"
  ],
  "copied_from_source": false
}
```

Do not make newly authored questions appear to be original textbook questions.

---

# 30. Chapter bank construction principles

Do not set one universal question count before inspecting the source and concept coverage.

Instead enforce coverage across:

```text
meaning
representations
facts/inverse relationship
estimation
place-value strategy
procedure
remainder
word-problem structures
reasoning
transfer
```

A bank is incomplete if one dimension dominates even when the total question count is large.

## 30.1 Coverage matrix

Track at minimum:

```text
rows    = microconcepts
columns = question archetypes / representation levels / mastery dimensions
```

Use the matrix to detect holes such as:

```text
many calculation questions
zero model translation
zero grouping word problems
zero remainder interpretation
zero error analysis
zero transfer
```

---

# 31. Textbook page / lesson anatomy for Division

A strong lesson may use this page rhythm:

```text
1 LESSON QUESTION / CONTEXT
2 LEARNING GOAL
3 NOTICE / DISCUSS
4 MODEL IT
5 CONNECT THE MODEL
6 WORKED EXAMPLE
7 TRY WITH SUPPORT
8 PRACTISE
9 EXPLAIN / REASON
10 MISCONCEPTION CLINIC
11 APPLY IN A STORY
12 CHALLENGE / TRANSFER
13 EXIT CHECK
14 SPIRAL REVIEW
```

Do not force every Learning Cell into exactly one page; preserve page rhythm and cognitive load.

---

# 32. Chapter-level mastery assessment blueprint

A final Division assessment should sample distinct evidence, not only arithmetic.

Recommended coverage categories:

```text
A meaning / equal groups
B multiplication–division relationship
C representation translation
D facts / mental strategies
E estimation / reasonableness
F multi-digit calculation
G remainder computation
H remainder interpretation
I word-problem recognition
J multi-step problem solving
K explanation / error analysis
L transfer / non-routine reasoning
```

A student profile should report these separately when enough evidence exists.

---

# 33. Student-attempt data stays separate

Do not put mutable learner state inside question records.

```json
{
  "student_question_attempt": {
    "student_id": "...",
    "question_id": "DIV-G4-0001",
    "response": "...",
    "correct": false,
    "hints_used": [1, 2],
    "attempt_count": 1,
    "time_seconds": null,
    "error_signature_detected": "...",
    "diagnostic_path": [],
    "mastery_evidence_generated": []
  }
}
```

Learning state should aggregate evidence separately by microconcept and mastery dimension.

---

# 34. Production QA checklist

Before declaring a Grade 4 Division chapter complete, verify:

## Source fidelity

- source questions/examples preserved accurately;
- visual models preserved or faithfully recreated when allowed;
- provenance classes correct;
- source defects not silently repaired.

## Concept coverage

- sharing and grouping both present;
- inverse multiplication connection explicit;
- models precede/justify abstract procedure where appropriate;
- remainder meaning and interpretation included;
- word-problem structures varied.

## Representation coverage

- concrete/pictorial/structural/symbolic connections present;
- at least some bidirectional translation tasks;
- procedure linked back to place-value meaning.

## Practice quality

- not dominated by one archetype;
- deliberate number variation;
- representation variation;
- recognition/application questions;
- explanation/error-analysis questions;
- mixed/spiral review.

## Diagnostics

- misconceptions are specific;
- error signatures map to plausible causes;
- diagnostic probes exist for high-value misconceptions;
- repair points to prerequisite concepts;
- retry questions test the repaired idea.

## Mastery

- conceptual + representational + procedural + application + reasoning + transfer evidence;
- no claim of mastery from repetitive fluency alone.

## Transfer

- near transfer present;
- representation/context transfer present;
- reverse/constraint reasoning present when appropriate;
- Olympiad bridge preserves Grade 4 concepts rather than introducing out-of-scope mathematics.

## Editorial / textbook QA

- child-facing language is age appropriate;
- diagrams/models are legible;
- answer units/context are correct;
- remainders interpreted consistently with stories;
- worked examples are mathematically verified;
- early hints do not reveal the answer;
- teacher and student editions show only appropriate fields.

---

# 35. Production pipeline

```text
SOURCE MATERIAL
      ↓
extract lesson structure + questions + models
      ↓
map source to DIV-M concept graph
      ↓
identify prerequisite dependencies
      ↓
define / refine Learning Cells
      ↓
map representation progression
      ↓
map number-structure progression
      ↓
define question archetype coverage
      ↓
fingerprint source questions
      ↓
identify coverage gaps
      ↓
author / retrieve calibrated questions
      ↓
enrich with notice/helper/hints/solutions
      ↓
attach misconceptions + diagnostics + repair
      ↓
build guided → independent → mixed sequence
      ↓
add mastery evidence and transfer ladder
      ↓
mathematical + editorial QA
      ↓
render textbook / bank / tutor package
      ↓
visual QA
```

---

# 36. Final design rule

The Division system should be able to answer all of the following about a learner:

```text
Does the child understand what division means?
Can the child distinguish sharing from grouping?
Can the child connect division to multiplication?
Can the child move between models and equations?
Can the child estimate the size of a quotient?
Can the child use place value to divide larger numbers?
Can the child execute an efficient procedure accurately?
Can the child interpret remainders correctly?
Can the child recognize division in unfamiliar stories?
Can the child choose an efficient strategy?
Can the child explain and verify an answer?
Can the child diagnose an incorrect method?
Can the child transfer division reasoning to a new representation or constraint?
```

If the chapter/question bank cannot distinguish these abilities, it is not yet textbook-quality Grade 4 Division content.
