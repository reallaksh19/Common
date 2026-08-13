# Grade 4 Mathematics — Division Publishing Contract

**Status:** Division-specific bridge between learning content and `Grade4PublishingSchema.md`  
**Parent learning schema:** `Grade4MathDivisionSchema.md`  
**Parent publishing schema:** `Grade4PublishingSchema.md`

---

# 1. Purpose

This document binds the Division learning schema to the shared Grade 4 publishing system without mixing page/layout rules into the pedagogical model.

The relationship is:

```text
Grade4MathDivisionSchema.md
        ↓
Division concept map / Learning Cells / questions / diagnostics
        ↓
THIS CONTRACT
        ↓
Grade4PublishingSchema.md
        ↓
chapter plan / page plan / visual models / edition rules / rendering / QA
        ↓
Student / Teacher / Workbook / Assessment PDF
```

The Division learning schema remains authoritative for mathematical meaning, pedagogy, sequence constraints, question correctness, hints, diagnostics, mastery, and transfer.

The publishing schema remains authoritative for page composition, visibility, working space, visual rendering, output editions, and PDF QA.

---

# 2. Required Division publishing bindings

Every renderable Division chapter must provide the following publication-facing data.

```yaml
division_publishing_contract:
  chapter_id: DIV-G4
  learning_schema: Grade4MathDivisionSchema.md
  publishing_schema: Grade4PublishingSchema.md

  chapter_plan_id: ...
  output_profile_ids: []
  page_plan_ids: []
  visual_model_ids: []
  design_token_profile: ...
  qa_report_id: ...
```

---

# 3. Learning Cell → page-component mapping

Recommended bindings:

```text
learning_cell.objective
→ LEARNING_GOAL

learning_cell.big_idea
→ BIG_IDEA

learning_cell.child_friendly_meaning
→ CONCEPT_DISCOVERY / REMEMBER_BOX

learning_cell.launch_context
→ LAUNCH_CONTEXT

learning_cell.representation_sequence
→ VISUAL_MODEL components

learning_cell.what_to_notice
→ WHAT_SHOULD_I_NOTICE

learning_cell.concept_trigger
→ CONCEPT_TRIGGER

learning_cell.worked_examples
→ WORKED_EXAMPLE

learning_cell.guided_practice
→ GUIDED_PRACTICE

learning_cell.independent_practice
→ PRACTICE_BLOCK

learning_cell.misconceptions
→ MISTAKE_DETECTIVE / TEACHER_NOTE

learning_cell.mastery_evidence
→ EXIT_CHECK / CHECKPOINT / teacher overlay

learning_cell.transfer_tasks
→ TRANSFER_CHALLENGE / OLYMPIAD_BRIDGE
```

The renderer must not invent these pedagogical values when the corresponding learning data is absent.

---

# 4. Question → page-component mapping

Division question fields map as follows.

```text
question.stem
→ QUESTION STEM

question.assets / visual model binding
→ INSTRUCTIONAL MODEL

what_to_notice
→ WHAT SHOULD I NOTICE?

helper
→ optional HELPER BOX

hints
→ HINT system / teacher overlay / digital reveal

solution.strategy
→ THINK / PLAN

solution.representation
→ MODEL IT / REPRESENT

solution.steps
→ SOLVE

solution.verification
→ CHECK

takeaway
→ REMEMBER

misconceptions
→ MISTAKE DETECTIVE / teacher note

diagnostic_probes
→ teacher-only diagnostic overlay

transfer_links
→ NEXT CHALLENGE / TRANSFER block
```

---

# 5. Division visual-model contract

Division should preferentially use structured instructional models rather than manually drawn one-off images.

Supported core Division visual types:

```text
COUNTERS
EQUAL_GROUPS
ARRAY
NUMBER_LINE
BAR_MODEL
PLACE_VALUE_BLOCKS
PARTITION_MODEL
FACT_FAMILY
DIVISION_EQUATION
MISSING_VALUE_EQUATION
WRITTEN_DIVISION
REMAINDER_CONTEXT_MODEL
```

Example:

```json
{
  "id": "DIV-VM-0001",
  "type": "EQUAL_GROUPS",
  "instructional_role": "REPRESENT_GROUPING_DIVISION",
  "data": {
    "total": 24,
    "group_size": 6,
    "number_of_groups": 4
  },
  "display": {
    "show_objects": true,
    "show_group_boundaries": true,
    "show_labels": true,
    "show_equation": false
  }
}
```

A model is valid only if it preserves the mathematical structure encoded in the question fingerprint.

---

# 6. Recommended Division page rhythm

The Division chapter may use the following default sequence, subject to source/curriculum alignment:

```text
CHAPTER OPENER

LC-01 Equal sharing
LC-02 Equal grouping
CHECKPOINT — meaning

LC-03 Multiplication–division connection
LC-04 Representation flexibility
LC-05 Division facts / mental strategies
CHECKPOINT — facts and representations

LC-06 Estimate quotients
LC-07 Multi-digit Division through place value
LC-08 Efficient written procedure
CHECKPOINT — computation

LC-09 Remainders
LC-10 Recognize Division in problems
LC-11 Multi-step Division

PROBLEM-SOLVING / REASONING LAB
MISTAKE DETECTIVE
TRANSFER / OLYMPIAD BRIDGE
MIXED REVIEW
CHAPTER ASSESSMENT
ANSWER KEY
```

Do not force this order when a supplied source has a materially different intended progression. The source-aligned chapter plan must take precedence.

---

# 7. Canonical Division page types

## 7.1 Concept discovery

Recommended components:

```text
LESSON_HEADER
LEARNING_GOAL
LAUNCH_CONTEXT
VISUAL_MODEL
WHAT_SHOULD_I_NOTICE
CONCEPT_TRIGGER
TRY_IT
```

## 7.2 Connect representations

Recommended composition:

```text
STORY
  ↓
PICTURE / STRUCTURAL MODEL
  ↓
MULTIPLICATION CONNECTION
  ↓
DIVISION EQUATION
```

This page type is especially important for LC-01 to LC-04.

## 7.3 Worked-example page

Recommended component sequence:

```text
EXAMPLE
WHAT SHOULD I NOTICE?
MODEL / REPRESENT
THINK / PLAN
SOLVE
CHECK
REMEMBER
```

## 7.4 Guided-practice page

Use fading scaffolds:

```text
full structure completion
↓
partial structure completion
↓
independent calculation/application
```

## 7.5 Mistake Detective page

Must contain:

```text
student-like incorrect response
↓
diagnostic question
↓
reasoning about the error
↓
repair
↓
retry
```

Do not reduce this page to a warning box.

## 7.6 Reasoning / transfer page

Prioritize:

- missing values;
- comparison without full calculation;
- explanation;
- multiple possible answers;
- constraints;
- remainder interpretation;
- representation-hidden problems;
- Olympiad bridge.

---

# 8. Question presentation metadata for Division

Each question may optionally add publication metadata outside the immutable learning fingerprint.

```json
{
  "presentation": {
    "preferred_component": "GUIDED_PRACTICE",
    "working_space": "MEDIUM",
    "keep_with_asset": true,
    "allow_page_split": false,
    "show_question_number": true,
    "show_hint_marker": false,
    "answer_lines": 0,
    "option_layout": "SINGLE_COLUMN"
  }
}
```

Examples:

### Direct calculation

```yaml
working_space: SMALL
```

### Model drawing

```yaml
working_space: LARGE
keep_with_asset: true
```

### Explain reasoning

```yaml
working_space: LARGE
answer_lines: 4
```

### Multi-step word problem

```yaml
working_space: HALF_PAGE
```

Working space must reflect the expected response, not only the length of the stem.

---

# 9. Student edition visibility for Division

Show when selected by page plan:

- child-facing objective;
- big idea;
- models;
- `What should I notice?`;
- worked examples;
- guided/independent practice;
- reasoning and transfer;
- intended helper/hints;
- response space.

Hide by default:

- correct answer metadata;
- diagnostic IDs;
- difficulty vector;
- error-signature IDs;
- teacher repair paths;
- source implementation metadata;
- mastery-state thresholds.

---

# 10. Teacher edition visibility for Division

Teacher edition may expose:

```text
OBJECTIVE
PREREQUISITES
EXPECTED REASONING
REPRESENTATION PURPOSE
WHAT TO WATCH FOR
MISCONCEPTION
ERROR SIGNATURE
DIAGNOSTIC PROBE
REPAIR PATH
ANSWER
ALTERNATIVE METHOD
DIFFICULTY PROFILE
MASTERY EVIDENCE
TRANSFER LEVEL
```

Example teacher note:

> Watch for learners who solve `24 ÷ 6 = 4` but cannot tell whether `4` represents the group size or number of groups. Probe sharing vs grouping meaning before increasing calculation difficulty.

---

# 11. Division-specific render QA

In addition to `Grade4PublishingSchema.md`, validate:

```text
equal-group diagrams actually contain equal groups
array dimensions match equation
bar model total and parts match values
number-line jumps are equal and counted correctly
place-value blocks match dividend/decomposition
written procedure preserves place value
remainder shown is smaller than divisor
remainder-context final answer matches story
multiplication check matches quotient/divisor/dividend
question and essential model remain together
student edition does not expose final answer accidentally
```

For generated instructional models, mathematical validation is required before visual approval.

---

# 12. Example Division page-plan binding

```yaml
page_plan:
  page_id: DIV-P013
  page_type: CONNECT_REPRESENTATIONS
  learning_cell_id: DIV-LC-02

  components:
    - type: LESSON_HEADER
      content: Make Equal Groups

    - type: LEARNING_GOAL
      bind: learning_cell.objective

    - type: LAUNCH_CONTEXT
      content: 24 apples are packed 6 in each basket. How many baskets can be filled?

    - type: VISUAL_MODEL
      model_id: DIV-VM-0001

    - type: WHAT_SHOULD_I_NOTICE
      bind: learning_cell.what_to_notice

    - type: CONCEPT_CONNECTION
      content: |
        6 × 4 = 24
        24 ÷ 6 = 4

    - type: TRY_IT
      question_ids:
        - DIV-G4-GROUP-002
        - DIV-G4-GROUP-003
```

---

# 13. Release contract

A Division PDF is release-ready only when all of the following are true:

```text
LEARNING CONTENT VALIDATED
        ✓
QUESTION ANSWERS VERIFIED
        ✓
CHAPTER PLAN APPROVED
        ✓
PAGE PLAN VALID
        ✓
VISUAL MODELS MATHEMATICALLY VALID
        ✓
EDITION VISIBILITY VALID
        ✓
PDF RENDER COMPLETE
        ✓
ALL PAGES RENDERED TO IMAGES
        ✓
VISUAL QA PASSED
        ✓
PEDAGOGY QA PASSED
        ✓
FINAL RELEASE
```

The presence of a visually polished PDF is not sufficient if any mathematical, pedagogical, or answer-visibility validation fails.
