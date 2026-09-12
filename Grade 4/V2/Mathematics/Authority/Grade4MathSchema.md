# Grade 4 Mathematics — Concept, Learning, Question-Bank & Textbook Production Schema

**Status:** Grade 4 production standard  
**Primary use cases:** textbook-quality chapter creation, source-grounded question banks, adaptive tutoring, Olympiad bridge material, teacher/student editions, and concept-level analytics.  
**Design principle:** Grade 4 mathematics is not a smaller Grade 9 question bank. The central object is the **learning progression of a mathematical idea**, including representation, reasoning, strategy, misconception diagnosis, mastery, and transfer.

---

## 1. Purpose

This schema defines how to turn a Grade 4 mathematics source — textbook pages, worksheets, school material, Olympiad papers, teacher notes, or syllabus — into a structured learning system.

The output should preserve textbook-quality pedagogy, not merely produce `question + hints + answer` records.

A complete Grade 4 mathematics chapter should contain:

1. a **source-faithful extraction layer**;
2. a **chapter concept map**;
3. a **prerequisite/dependency graph**;
4. a **learning progression** from concrete experience to abstract reasoning;
5. a **representation progression**;
6. one or more **learning cells** per microconcept;
7. a controlled **question archetype space**;
8. a **learning fingerprint** for each question;
9. a multidimensional **difficulty profile**;
10. **helpers and progressive hints** that follow the child’s reasoning state;
11. **worked solutions and verification**;
12. **misconception/error diagnostics** with repair paths;
13. **practice sequencing** rather than random question accumulation;
14. a **mastery model** based on multiple forms of evidence;
15. a **transfer ladder** ending in non-routine/Olympiad-style application;
16. provenance, editorial QC, and textbook-rendering QA.

The architecture is:

```text
SOURCE
  ↓
CHAPTER REVERSE-ENGINEERING
  ↓
CONCEPT MAP
  ↓
PREREQUISITE GRAPH
  ↓
LEARNING PROGRESSION
  ↓
REPRESENTATION PROGRESSION
  ↓
LEARNING CELLS
  ↓
QUESTION ARCHETYPES
  ↓
QUESTION INSTANCES + LEARNING FINGERPRINTS
  ↓
DIFFICULTY PROFILE
  ↓
PEDAGOGICAL ENRICHMENT
  ↓
DIAGNOSTICS + REPAIR
  ↓
PRACTICE SEQUENCING
  ↓
MASTERY
  ↓
TRANSFER / OLYMPIAD
  ↓
TEXTBOOK PRODUCTION + QA
```

---

# 2. Non-negotiable principles

## 2.1 Source fidelity first

Do not silently repair, simplify, reinterpret, redraw, or replace a source question, worked example, or diagram.

Each extracted item must have one of:

- `VERIFIED_TRANSCRIPTION`
- `RECONSTRUCTED`
- `QC_ALERT`
- `SOURCE_UNRESOLVED`

For Grade 4, visual models are part of the mathematical content. Arrays, number lines, counters, bar models, place-value blocks, tables, diagrams, and layout must be preserved in the master record when mathematically relevant.

## 2.2 Concepts before questions

Do not begin by generating a large question bank.

First determine:

- what the chapter teaches;
- what children are expected to understand;
- which ideas depend on earlier ideas;
- which representations are used;
- which strategies are introduced;
- what changes from one lesson to the next;
- how the textbook moves from modelling to independent reasoning.

A question bank without this concept architecture will drift into repetition and shallow difficulty variation.

## 2.3 Representation is part of the mathematics

For Grade 4, a picture, model, equation, written algorithm, and verbal problem are not interchangeable surface forms. Moving between them is itself a learning objective.

The system must therefore distinguish:

```text
Can calculate 84 ÷ 4
```

from:

```text
Can model 84 ÷ 4
Can select the model for 84 ÷ 4
Can convert a model into 84 ÷ 4
Can explain why 84 ÷ 4 = 21
Can recognize division in a story
```

## 2.4 Difficulty is a profile, not a label

Do not classify questions only as `easy / medium / hard`.

At Grade 4, difficulty may come from:

- concept understanding;
- fact fluency;
- place value;
- representation;
- language;
- operation recognition;
- strategy selection;
- procedural load;
- number of reasoning steps;
- interpretation of remainder;
- transfer distance.

## 2.5 Correctness is not mastery

A child who answers ten nearly identical calculations correctly has demonstrated fluency on one form of the task, not necessarily mastery.

Mastery requires evidence across conceptual understanding, representation, calculation/fluency, application, explanation/reasoning, and transfer.

## 2.6 Diagnostics must be causal

Do not label a child simply as `weak in division`.

Use the observed response to form one or more hypotheses, probe the prerequisite, identify the likely broken step, repair it, and retry with an isomorphic structure.

## 2.7 Transfer is deliberate

“Similar questions” must not mean questions with the same keywords.

Transfer should be designed by controlled variation of:

- numbers;
- representation;
- unknown position;
- context;
- strategy;
- reasoning demand;
- number of steps;
- constraints.

---

# 3. Core entity hierarchy

The Grade 4 Mathematics system has four instructional content levels.

```text
CHAPTER
  ↓
MACROCONCEPT
  ↓
MICROCONCEPT / LEARNING CELL
  ↓
QUESTION INSTANCE
```

Student-attempt data must remain separate.

```text
Question content record     ≠     StudentQuestionAttempt
Learning cell               ≠     StudentLearningState
```

This allows the content bank to remain stable while learner data accumulates independently.

---

# 4. Stage A — Source ingestion and editorial extraction

## 4.1 Source record

```json
{
  "source_id": "SRC-MATH-001",
  "type": "TEXTBOOK",
  "title": "...",
  "publisher": "...",
  "grade": 4,
  "edition": "...",
  "pages": "...",
  "url": "...",
  "verified": true,
  "verification_date": "YYYY-MM-DD"
}
```

## 4.2 Extract lesson structure before individual questions

For every source range capture:

```text
lesson title
learning objective
vocabulary
concept introduction
models / manipulatives
worked examples
teacher prompts
practice sections
review sections
reasoning/problem-solving sections
challenge/extension sections
assessment items
```

## 4.3 Extract each question/example

```json
{
  "seed_id": "DIV-LESSON4-Q07",
  "source_page": 112,
  "source_question_number": 7,
  "provenance_class": "USER_UPLOADED_ANCHOR",
  "transcription_status": "VERIFIED_TRANSCRIPTION",
  "raw_question": "...",
  "assets": [],
  "source_answer": "...",
  "editorial_notes": "..."
}
```

## 4.4 Grade 4 editorial QC

Check:

- missing diagram labels;
- missing units;
- unclear array/grouping artwork;
- whether pictured objects match the text;
- ambiguous use of `each`, `altogether`, `left`, `more`, `difference`, etc.;
- whether multiple answers are possible;
- whether the expected answer form matches the story context;
- whether a remainder must be interpreted;
- whether visual scale or icon repetition changes the intended meaning;
- whether a number pattern is uniquely determined;
- whether a graph/table contains all needed labels.

---

# 5. Stage B — Chapter reverse-engineering

Before building a schema for questions, reverse-engineer the chapter as a teaching sequence.

For each chapter answer:

```text
1. What are the chapter big ideas?
2. Which prior ideas are assumed?
3. What new ideas are introduced?
4. Which representations are used first?
5. Which representations appear later?
6. Which strategies are modelled?
7. When does the text ask the child to choose a strategy?
8. When does direct calculation become problem solving?
9. Where are misconceptions likely?
10. How does practice vary?
11. What evidence would show mastery?
12. What is the natural Olympiad/non-routine extension?
```

### Example: Division chapter

```text
Understand division
→ equal sharing
→ equal grouping
→ connect multiplication and division
→ division facts
→ represent division
→ estimate quotients
→ divide larger numbers
→ remainders
→ word-problem structures
→ multi-step problems
→ reasoning and transfer
```

---

# 6. Stage C — Concept map

## 6.1 Hierarchy

```text
DOMAIN
  ↓
CHAPTER
  ↓
MACROCONCEPT
  ↓
MICROCONCEPT
  ↓
KNOWLEDGE COMPONENT
```

## 6.2 Example: Grade 4 Division

```text
DIVISION
│
├── A. Meaning of division
│   ├── A1 Equal sharing / find group size
│   ├── A2 Equal grouping / find number of groups
│   ├── A3 Repeated subtraction interpretation
│   ├── A4 Division vocabulary
│   └── A5 Relationship to multiplication
│
├── B. Division facts
│   ├── B1 Fact families
│   ├── B2 Missing-factor reasoning
│   ├── B3 Divide by 1
│   ├── B4 Divide a number by itself
│   ├── B5 Patterns
│   └── B6 Mental division
│
├── C. Representation
│   ├── C1 Counters / objects
│   ├── C2 Equal groups
│   ├── C3 Arrays
│   ├── C4 Number line
│   ├── C5 Bar model
│   ├── C6 Place-value model
│   └── C7 Equation
│
├── D. Estimate quotient
│   ├── D1 Multiples of divisor
│   ├── D2 Compatible numbers
│   ├── D3 Benchmark quotient
│   ├── D4 Quotient range
│   └── D5 Reasonableness
│
├── E. Larger-number division
│   ├── E1 Place-value decomposition
│   ├── E2 Distributive reasoning
│   ├── E3 Partial quotients
│   ├── E4 Regrouping
│   └── E5 Efficient written procedure
│
├── F. Remainders
│   ├── F1 Meaning of remainder
│   ├── F2 Quotient and remainder
│   ├── F3 Remainder < divisor
│   ├── F4 Verify D × Q + R = dividend
│   └── F5 Interpret remainder in context
│
├── G. Problem solving
│   ├── G1 Find group size
│   ├── G2 Find number of groups
│   ├── G3 Find missing divisor
│   ├── G4 Choose operation
│   ├── G5 Multi-step
│   ├── G6 Extra/missing information
│   └── G7 Interpret answer in context
│
├── H. Mathematical reasoning
│   ├── H1 Explain strategy
│   ├── H2 Compare strategies
│   ├── H3 Error analysis
│   ├── H4 Reasonableness
│   ├── H5 Missing-number reasoning
│   └── H6 Multiple solutions
│
└── I. Transfer / Olympiad
    ├── I1 Reverse problem
    ├── I2 Constraint problem
    ├── I3 Pattern + division
    ├── I4 Multiple-condition problem
    ├── I5 Logic + division
    └── I6 Non-routine transfer
```

---

# 7. Stage D — Prerequisite graph

Prerequisites are stored as dependencies, not a flat list.

```json
{
  "microconcept_id": "DIV-E2",
  "dependencies": [
    {
      "concept_id": "PLACE-VALUE-DECOMPOSITION",
      "strength": "CRITICAL"
    },
    {
      "concept_id": "DIVISION-FACTS",
      "strength": "CRITICAL"
    },
    {
      "concept_id": "DISTRIBUTIVE-PROPERTY-INTUITIVE",
      "strength": "STRONG"
    },
    {
      "concept_id": "ESTIMATE-QUOTIENT",
      "strength": "SUPPORTING"
    }
  ]
}
```

Allowed dependency strengths:

```text
CRITICAL
STRONG
SUPPORTING
```

The graph powers:

- diagnostics;
- repair sequencing;
- prerequisite review;
- adaptive lesson selection;
- spiral review.

---

# 8. Stage E — Learning progression

Each microconcept should be designed across the following learning sequence.

```text
EXPERIENCE
  ↓
NOTICE
  ↓
MODEL
  ↓
REPRESENT
  ↓
CONNECT
  ↓
GENERALISE
  ↓
PRACTISE
  ↓
REASON
  ↓
TRANSFER
```

### Example: division as equal grouping

```text
REAL SITUATION
24 apples; 6 apples in each basket
      ↓
ACT / MODEL
make groups of 6
      ↓
NOTICE
all groups have equal size
      ↓
QUESTION
how many groups can be made?
      ↓
REPRESENT
6 + 6 + 6 + 6 = 24
      ↓
CONNECT
4 × 6 = 24
      ↓
SYMBOLISE
24 ÷ 6 = 4
      ↓
GENERALISE
total ÷ amount in each group = number of groups
      ↓
TRANSFER
recognize the same structure in a different story/model
```

---

# 9. Stage F — Representation progression

Use stable representation levels.

```text
R0 — CONCRETE
real objects / manipulatives / physical grouping

R1 — PICTORIAL
drawings / pictures / icons

R2 — STRUCTURAL MODEL
arrays / bar models / number lines / area models / place-value models / tables

R3 — SYMBOLIC
numbers / equations / expressions

R4 — STRATEGIC
mental strategies / decomposition / properties / known facts

R5 — PROCEDURAL
written algorithm / formal multi-step calculation

R6 — ABSTRACT REASONING
explain / compare / justify / constrain / generalise
```

Question records should identify:

```json
{
  "representation": {
    "input_level": "R1_PICTORIAL",
    "input_type": "EQUAL_GROUPS_DIAGRAM",
    "expected_working_level": "R3_SYMBOLIC",
    "expected_working_type": "DIVISION_EQUATION",
    "answer_level": "R3_SYMBOLIC"
  }
}
```

Representation shifts are themselves valuable question archetypes.

---

# 10. Stage G — Learning Cell

The Learning Cell is the central Grade 4 instructional object.

## 10.1 Canonical Learning Cell

```yaml
learning_cell_id: DIV-A2-01
title: Find the number of equal groups
chapter: Division
macroconcept: Meaning of division
microconcept: Equal grouping

learning_objective: >
  Given a total and the equal size of each group, determine the number of groups
  and represent the situation with a division equation.

big_idea: >
  Division can tell us how many equal groups can be made from a total.

child_friendly_meaning: >
  If I know how many things there are altogether and how many go in each group,
  division helps me find how many groups I can make.

vocabulary:
  - divide
  - equal groups
  - dividend
  - divisor
  - quotient

prerequisites:
  - equal groups
  - repeated addition
  - multiplication facts

concept_invariant: >
  Every group has the same size, and all objects in the total are accounted for
  unless the situation includes a remainder.

representation_path:
  - concrete_groups
  - pictorial_groups
  - repeated_addition
  - multiplication_equation
  - division_equation

recognition_cues:
  - total amount is known
  - size of each group is known
  - number of groups is unknown

concept_trigger: >
  Total + amount in each group + find number of groups → divide.

strategies:
  - make_equal_groups
  - repeated_subtraction
  - use_related_multiplication_fact

worked_examples: []
guided_practice: []
variation_practice: []
independent_practice: []
misconceptions: []
diagnostics: []
mastery_evidence: []
transfer_links: []
```

## 10.2 Required Learning Cell sections

Every important microconcept should include:

```text
Learning objective
Big idea
Child-friendly meaning
Vocabulary
Prerequisites
Concept invariant
Concrete model
Pictorial model
Structural model
Symbolic form
Recognition cues
What should I notice?
Concept trigger
Strategies
Worked example 1
Worked example 2
Guided practice
Controlled variation
Independent practice
Misconception clinic
Diagnostic probes
Repair path
Mastery evidence
Near transfer
Far transfer
Olympiad bridge
Spiral-review links
```

---

# 11. Stage H — Question archetype space

Question generation must be controlled by archetype.

## 11.1 Core archetypes

```text
CALCULATE
MODEL
MODEL_TO_EQUATION
EQUATION_TO_MODEL
COMPLETE
MISSING_VALUE
REVERSE
ESTIMATE
COMPARE
ORDER
WORD_PROBLEM
CHOOSE_OPERATION
CHOOSE_STRATEGY
EXPLAIN
JUSTIFY
VERIFY
ERROR_ANALYSIS
MULTI_STEP
OPEN_RESPONSE
CONSTRAINT
PATTERN
DATA_INTERPRETATION
VISUAL_REASONING
SPATIAL_REASONING
OLYMPIAD_TRANSFER
```

## 11.2 Example space around one seed

Seed:

```text
84 ÷ 4 = ?
```

Controlled variants:

```text
Direct calculation:
84 ÷ 4 = ?

Numerical variation:
96 ÷ 4 = ?

Model:
Show 84 ÷ 4 using equal groups.

Model → equation:
Which equation matches this array?

Equation → model:
Which picture represents 84 ÷ 4?

Missing value:
84 ÷ □ = 21

Unknown-position variation:
□ ÷ 4 = 21

Inverse connection:
4 × □ = 84

Word problem — sharing:
84 stickers are shared equally among 4 children.

Word problem — grouping:
84 stickers are packed 4 in each bag.

Estimate:
About how much is 83 ÷ 4?

Compare:
Without calculating exactly, which is greater: 84 ÷ 4 or 84 ÷ 6?

Error analysis:
A student says 84 ÷ 4 = 24. Explain the error.

Method choice:
Which method would be most efficient for 84 ÷ 4?

Open response:
Write a division story whose answer is 21.

Constraint:
A number divided by 4 has quotient 21 and remainder 2. Find the number.

Olympiad bridge:
Find values satisfying two division conditions.
```

---

# 12. Stage I — Question learning fingerprint

A Grade 4 question receives a learning fingerprint rather than only topic labels.

## 12.1 Canonical fingerprint

```json
{
  "learning_fingerprint": {
    "mathematical_idea": "...",
    "microconcept_id": "...",
    "task_action": "...",

    "situation_structure": {},
    "unknown_role": "...",

    "number_structure": {},

    "representation": {
      "input": [],
      "working": [],
      "output": []
    },

    "recognition_cues": [],
    "reasoning_moves": [],
    "strategy": "...",
    "knowledge_components": [],
    "constraints": [],
    "answer_form": "...",
    "expected_reasoning_path": [],
    "concept_invariant": "...",
    "transfer_invariant": "..."
  }
}
```

## 12.2 Task actions

Suggested controlled vocabulary:

```text
CALCULATE
ESTIMATE
MODEL
REPRESENT
MATCH
COMPARE
ORDER
COMPLETE
FIND_MISSING
TRANSLATE
CHOOSE_OPERATION
CHOOSE_STRATEGY
EXPLAIN
JUSTIFY
VERIFY
ERROR_ANALYZE
SOLVE_WORD_PROBLEM
SOLVE_MULTI_STEP
GENERALISE
```

## 12.3 Reasoning moves

Suggested examples:

```text
IDENTIFY_TOTAL
IDENTIFY_GROUP_SIZE
IDENTIFY_NUMBER_OF_GROUPS
IDENTIFY_UNKNOWN
RECOGNIZE_EQUAL_GROUPS
MAP_STORY_TO_OPERATION
CONNECT_MULTIPLICATION_AND_DIVISION
DECOMPOSE_BY_PLACE_VALUE
REGROUP
USE_COMPATIBLE_NUMBERS
ESTIMATE_QUOTIENT
FORM_EQUATION
CALCULATE
INTERPRET_REMAINDER
CHECK_REASONABLENESS
COMPARE_STRATEGIES
USE_INVERSE_OPERATION
ELIMINATE_IMPOSSIBLE_OPTIONS
SATISFY_CONSTRAINTS
```

## 12.4 Number structure

```json
{
  "number_structure": {
    "dividend_digits": 3,
    "divisor_digits": 1,
    "exact_division": false,
    "remainder_present": true,
    "regrouping_required": true,
    "zero_internal": false,
    "fact_fluency_required": ["4-times-table"],
    "place_value_bridge": true
  }
}
```

---

# 13. Stage J — Difficulty profile

Use a 0–10 score only as an internal calibration aid. Do not let a composite score replace the profile.

```json
{
  "difficulty": {
    "overall": 5.0,
    "concept_demand": 4,
    "fact_fluency_demand": 4,
    "place_value_demand": 5,
    "recognition_demand": 6,
    "representation_demand": 4,
    "strategy_selection_demand": 3,
    "procedure_demand": 4,
    "calculation_demand": 3,
    "language_demand": 5,
    "working_memory_demand": 4,
    "remainder_interpretation_demand": 0,
    "reasoning_step_count": 3,
    "transfer_distance": 2
  }
}
```

A story problem with simple arithmetic may be harder than a long calculation if its recognition/language/interpretation demands are higher.

---

# 14. Stage K — “What should I notice?” taxonomy

Do not use empty advice such as “read carefully”.

Every notice should point to a mathematically meaningful feature.

Allowed types:

```text
STRUCTURE
UNKNOWN
NUMBER
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
      "text": "The objects are being put into equal groups."
    },
    {
      "type": "UNKNOWN",
      "text": "We know how many go in each group, but not how many groups there are."
    },
    {
      "type": "CONNECTION",
      "text": "A multiplication fact can help find the quotient."
    }
  ]
}
```

---

# 15. Stage L — Concept trigger

`recognition_cues` are question-specific. `concept_trigger` is transferable.

Example:

```text
Question-specific recognition cues:
“98 pupils”, “8 in each van”, “how many vans?”

Concept trigger:
total + capacity of each group + find number of groups → division
```

This distinction should be retained in the schema.

---

# 16. Stage M — Helper architecture

A helper is not a hint. It is a teacher-style question that helps the child orient to the problem.

```json
{
  "helper": {
    "understand": "What does each number represent?",
    "unknown": "What are you trying to find?",
    "notice": "Which quantities form equal groups?",
    "represent": "Can you show the situation with a picture or equation?",
    "connect": "Which fact or earlier idea might help?",
    "check": "What would make your answer reasonable?"
  }
}
```

Not every question needs every helper type.

---

# 17. Stage N — Progressive hint architecture

Keep five hint levels, but assign each a pedagogical job.

```text
H1 — NOTICE      10%
Where should I look?

H2 — REMEMBER    25%
What idea/fact should I activate?

H3 — REPRESENT   45%
How should I show or organise the problem?

H4 — PLAN        70%
What strategy/operation should I use?

H5 — DO          90%
What exact next execution step should I perform?
```

Example for a bus/remainder problem:

```text
H1 NOTICE
What does 8 tell you about each van?

H2 REMEMBER
You know the total number of pupils and the capacity of each van.

H3 REPRESENT
Write total ÷ capacity.

H4 PLAN
Find 98 ÷ 8 and pay attention to the remainder.

H5 DO
12 vans are full; ask what must happen to the pupils left over.
```

## 17.1 Hint leakage rule

H1 and H2 must not reveal the operation when operation recognition is the target skill.

Hints must attach to reasoning nodes, not merely become progressively longer versions of the solution.

---

# 18. Stage O — Solution architecture

Grade 4 solutions should expose meaning before procedure when conceptually relevant.

Recommended layers:

```text
1. Strategy
2. Model / representation (when useful)
3. Step-by-step reasoning
4. Calculation
5. Answer with unit/context
6. Verification / reasonableness
7. Alternative method (only when genuinely useful)
8. Learning takeaway
```

Example verification methods:

```text
ESTIMATE
INVERSE_OPERATION
SUBSTITUTION
VISUAL_CHECK
RANGE_CHECK
UNIT_CHECK
RECALCULATE_ANOTHER_WAY
```

---

# 19. Stage P — Misconception and error model

Misconceptions must describe specific wrong mental models.

## 19.1 Error classes

```text
CONCEPT_ERROR
FACT_RECALL_ERROR
PLACE_VALUE_ERROR
REPRESENTATION_ERROR
OPERATION_SELECTION_ERROR
STRATEGY_ERROR
PROCEDURE_ERROR
CALCULATION_SLIP
LANGUAGE_INTERPRETATION_ERROR
REMAINDER_INTERPRETATION_ERROR
CONSTRAINT_REASONING_ERROR
```

## 19.2 Diagnostic record

```json
{
  "misconception_id": "DIV-REM-03",
  "wrong_model": "The quotient alone is always the final answer.",
  "error_signatures": [
    "98 pupils / 8 per van → 12 vans"
  ],
  "error_stage": "REMAINDER_INTERPRETATION_ERROR",
  "diagnostic_probe": "Where will the 2 pupils left over sit?",
  "evidence_expected": "Student recognizes that another van is required.",
  "repair": "Model 12 full groups and the remaining pupils.",
  "repair_concept_id": "DIV-F5",
  "retry_question_id": "..."
}
```

## 19.3 Diagnostic pipeline

```text
Observed answer
  ↓
Error signature
  ↓
Possible hypothesis/hypotheses
  ↓
Diagnostic probe
  ↓
Evidence
  ↓
Repair microconcept
  ↓
Repair question
  ↓
Retry isomorphic question
  ↓
Return to original / transfer
```

Avoid overdiagnosing from one wrong answer. Store hypotheses and confidence when more than one cause is plausible.

---

# 20. Stage Q — Practice sequencing

A textbook-quality practice set should vary purpose, not just numbers.

Recommended sequence:

```text
1. Worked example
2. Guided practice
3. Direct independent practice
4. Controlled numerical variation
5. Representation variation
6. Unknown-position variation
7. Context/application variation
8. Mixed strategy practice
9. Reasoning/explanation
10. Error analysis
11. Multi-step application
12. Transfer/challenge
13. Spiral review
```

Question distribution should reflect the learning objective. Early lessons may contain more modelling/guided items; later lessons should increase independent reasoning and transfer.

---

# 21. Stage R — Mastery model

Mastery is multidimensional.

```json
{
  "mastery_evidence": {
    "conceptual_understanding": [],
    "representation_flexibility": [],
    "fact_or_procedural_fluency": [],
    "strategy_selection": [],
    "application": [],
    "reasoning_and_explanation": [],
    "verification": [],
    "transfer": []
  }
}
```

Example: division mastery should include evidence that the learner can:

```text
✓ explain equal sharing/grouping
✓ connect multiplication and division
✓ interpret a visual model
✓ create an equation from a situation
✓ calculate appropriate quotients
✓ estimate/check reasonableness
✓ interpret a remainder
✓ recognize division in an unfamiliar story
✓ explain or compare strategies
✓ solve a changed-context transfer item
```

## 21.1 Hint-sensitive mastery

Store hint usage separately in learner data.

A correct answer after H5 should not count identically to an independent correct answer.

## 21.2 Mastery state suggestion

```text
NOT_STARTED
EMERGING
GUIDED
DEVELOPING
SECURE
TRANSFER_READY
```

Do not derive state from raw percentage alone.

---

# 22. Stage S — Transfer ladder

Replace a generic challenge appendix with a deliberate transfer ladder.

```text
T0 — PREREQUISITE REPAIR
T1 — NEAR TWIN
T2 — NUMBER VARIATION
T3 — REPRESENTATION TRANSFER
T4 — UNKNOWN-POSITION TRANSFER
T5 — CONTEXT TRANSFER
T6 — STRATEGY-CHOICE TRANSFER
T7 — MULTI-STEP APPLICATION
T8 — CONSTRAINT / REASONING
T9 — OLYMPIAD / NON-ROUTINE TRANSFER
```

Transfer metadata:

```json
{
  "transfer": {
    "level": "T5_CONTEXT_TRANSFER",
    "preserved_invariant": "find number of equal groups",
    "changed_dimensions": ["context", "language"],
    "source_question_id": "DIV-A2-Q03"
  }
}
```

---

# 23. Stage T — Similar-question / analogue system

Do not store fixed fields such as `analogue_A`, `analogue_B`, etc.

Use an array:

```json
{
  "analogues": [
    {
      "question_id": "...",
      "role": "NEAR_TWIN",
      "similarity": {
        "concept": 1.0,
        "reasoning": 0.95,
        "representation": 0.8,
        "number_structure": 0.7,
        "surface_context": 0.4
      },
      "difference_summary": "Same grouping structure, new context and numbers."
    }
  ]
}
```

Suggested roles:

```text
PREREQUISITE_REPAIR
NEAR_TWIN
NUMBER_VARIATION
REPRESENTATION_TRANSFER
UNKNOWN_TRANSFER
CONTEXT_TRANSFER
STRATEGY_TRANSFER
MULTI_STEP_TRANSFER
ADVANCED_TRANSFER
OLYMPIAD_TRANSFER
```

Similarity should prioritize the learning fingerprint over surface wording.

---

# 24. Canonical Grade 4 Math question record

```json
{
  "id": "DIV-A2-WP-001",

  "question": {
    "stem": "...",
    "question_type": "SHORT_ANSWER",
    "options": [],
    "assets": [],
    "expected_answer": "..."
  },

  "provenance": {
    "source_id": "...",
    "source_page": null,
    "source_question_number": null,
    "provenance_class": "ORIGINAL_CALIBRATED",
    "transcription_status": null,
    "verified": true
  },

  "classification": {
    "subject": "Mathematics",
    "grade": 4,
    "domain": "Number and Operations",
    "chapter": "Division",
    "macroconcept": "Meaning of division",
    "microconcept_id": "DIV-A2",
    "question_archetype": "WORD_PROBLEM"
  },

  "learning_fingerprint": {
    "mathematical_idea": "division as equal grouping",
    "task_action": "SOLVE_WORD_PROBLEM",
    "situation_structure": {
      "total": "known",
      "group_size": "known",
      "number_of_groups": "unknown"
    },
    "unknown_role": "NUMBER_OF_GROUPS",
    "number_structure": {},
    "representation": {
      "input": ["WORD_PROBLEM"],
      "working": ["DIVISION_EQUATION"],
      "output": ["NUMBER_WITH_UNIT"]
    },
    "recognition_cues": [],
    "reasoning_moves": [],
    "strategy": "RELATED_MULTIPLICATION_FACT",
    "knowledge_components": [],
    "constraints": [],
    "answer_form": "NUMBER_WITH_UNIT",
    "expected_reasoning_path": [],
    "concept_invariant": "equal group size",
    "transfer_invariant": "total ÷ size of each group = number of groups"
  },

  "difficulty": {},

  "prerequisites": [],
  "what_to_notice": [],
  "concept_trigger": "",
  "helper": {},
  "hints": [],

  "solution": {
    "strategy": "...",
    "model": "...",
    "steps": [],
    "full": "...",
    "answer": "...",
    "verification": {},
    "alternative_methods": []
  },

  "diagnostics": [],
  "learning_takeaway": "...",
  "transfer_links": [],
  "analogues": []
}
```

---

# 25. Student data — separate schema

Do not place these fields in the immutable content record:

```text
student_answer
attempt_count
time_taken
hints_used
mastery_state
confidence
last_seen
```

Use a separate object:

```json
{
  "student_question_attempt": {
    "student_id": "...",
    "question_id": "...",
    "attempt_number": 1,
    "answer": "...",
    "correct": false,
    "hints_used": [1, 2],
    "diagnostic_path": [],
    "timestamp": "..."
  }
}
```

And separately:

```json
{
  "student_concept_state": {
    "student_id": "...",
    "microconcept_id": "DIV-A2",
    "state": "DEVELOPING",
    "evidence": [],
    "known_gaps": [],
    "next_recommended_cells": []
  }
}
```

---

# 26. Chapter assembly standard

A Grade 4 chapter should normally include:

```text
Chapter opener / big idea
Prerequisite check
Concept map
Vocabulary

Learning Cell 1
  concept launch
  model
  worked examples
  guided practice
  independent practice
  reasoning

Learning Cell 2
...

Mixed practice
Problem-solving lesson
Reasoning / error-analysis lesson
Transfer / challenge
Chapter review
Mastery check
Spiral review
```

Do not force every chapter into identical page counts; preserve the concept progression.

---

# 27. Source-grounded question-bank production

When building a bank from uploaded/source questions:

```text
SOURCE ANCHORS
  ↓
classify each anchor by microconcept + archetype + fingerprint
  ↓
check coverage across concept map
  ↓
identify missing instructional forms
  ↓
generate/retrieve controlled variants
  ↓
rank by fingerprint similarity and pedagogical role
  ↓
enrich with helpers/hints/solutions/diagnostics
  ↓
QA for level, correctness, repetition, and coverage
```

Do not automatically create five variants per seed. Create variants only when they fill a defined learning role.

---

# 28. Provenance classes

Recommended master-data values:

```text
USER_UPLOADED_ANCHOR
OFFICIAL_SOURCE
PUBLISHED_REFERENCE
ORIGINAL_CALIBRATED
RECONSTRUCTED_FROM_SCAN
WEB_ANALOGUE_METADATA_ONLY
```

Keep provenance separate from pedagogical classification.

---

# 29. Mathematical verification / QA

Every scored question must pass:

1. **solvability** — sufficient data and unambiguous target;
2. **answer correctness**;
3. **representation correctness** — diagram/model matches values;
4. **Grade 4 appropriateness** — no accidental higher-grade machinery unless explicitly transfer/challenge;
5. **unit/context validity**;
6. **remainder interpretation validity**;
7. **alternative-answer check** — especially open/constraint problems;
8. **distractor validity** — distractors should map to plausible misconceptions where possible;
9. **hint leakage check**;
10. **difficulty re-score after the clean solution is known**;
11. **language load check** — math difficulty should not be accidentally dominated by reading complexity unless intended;
12. **concept coverage check**;
13. **repetition check** — avoid surface-only variation.

---

# 30. Textbook-quality rendering standard

Textbook quality means editorial hierarchy and mathematical clarity, not just exported text.

Use consistent visual systems for:

```text
BIG IDEA
VOCABULARY
MODEL
NOTICE
WORKED EXAMPLE
TRY IT
HELPER
HINT
MISCONCEPTION CLINIC
CHECK YOUR THINKING
REASONING
CHALLENGE
TAKEAWAY
```

Grade 4-specific design requirements:

- generous white space;
- strong figure-to-text alignment;
- large readable labels;
- avoid decorative artwork that competes with the mathematics;
- consistent visual encoding for counters/groups/arrows;
- short paragraph lengths;
- clear separation of worked example and student task;
- no overcrowded answer areas;
- ensure diagrams remain legible in print and on tablets.

Every final PDF should be rendered to images and visually inspected.

---

# 31. Division prototype acceptance test

Before declaring this schema stable, build one complete Division microconcept end to end:

```text
Microconcept:
Division as finding the number of equal groups
```

The prototype is accepted only if it includes:

```text
✓ source alignment
✓ concept definition
✓ prerequisite graph
✓ concrete/pictorial/structural/symbolic progression
✓ recognition cues
✓ concept trigger
✓ 2 worked examples
✓ guided practice
✓ 10+ controlled archetype variations
✓ difficulty profiles
✓ meaningful “what to notice” prompts
✓ five-level hint ladders
✓ specific misconceptions
✓ error signatures
✓ diagnostic probes
✓ repair path
✓ mastery evidence
✓ transfer ladder through non-routine application
✓ textbook-layout specification
```

Only after this works should the same architecture be generalized across the full Grade 4 mathematics curriculum.

---

# 32. Final schema philosophy

The Grade 4 Mathematics engine should model this process:

```text
UNDERSTAND THE SITUATION
  ↓
NOTICE MATHEMATICAL STRUCTURE
  ↓
CONNECT TO PRIOR KNOWLEDGE
  ↓
REPRESENT THE IDEA
  ↓
CHOOSE A STRATEGY
  ↓
EXECUTE
  ↓
INTERPRET
  ↓
VERIFY
  ↓
EXPLAIN
  ↓
TRANSFER
```

The goal is not merely to answer Grade 4 questions. The goal is to model **how Grade 4 mathematical understanding develops**, how it breaks, how it is repaired, and how it transfers to unfamiliar problems.
