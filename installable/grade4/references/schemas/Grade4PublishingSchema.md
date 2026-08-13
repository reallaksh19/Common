# Grade 4 Publishing, Page-Plan & PDF Rendering Schema

**Status:** Grade 4 shared publishing standard  
**Applies to:** Grade 4 Mathematics and Grade 4 English content schemas  
**Primary use cases:** student textbook PDFs, teacher editions, workbooks, answer keys, assessment booklets, screen PDFs, and reusable digital page rendering.  
**Design principle:** Pedagogy/content and publishing/layout are separate systems. Learning schemas define *what* must be taught and assessed; this schema defines *how validated structured content becomes a coherent rendered product*.

---

# 1. Purpose

This schema defines the publishing layer that sits after subject-specific Grade 4 learning content.

It must support the pipeline:

```text
SUBJECT LEARNING SCHEMA
        ↓
STRUCTURED CONTENT DATA
        ↓
CHAPTER / UNIT PLAN
        ↓
PAGE PLAN
        ↓
PAGE COMPONENTS
        ↓
VISUAL / MODEL RENDERING
        ↓
EDITION FILTERING
        ↓
PDF / DIGITAL RENDER
        ↓
CONTENT + VISUAL QA
        ↓
FINAL PRODUCT
```

The publishing layer must never silently alter mathematical meaning, language meaning, answers, source provenance, instructional sequence, or diagnostic logic.

---

# 2. Core separation of responsibilities

## 2.1 Subject learning schema owns

- chapter/unit concepts or skills;
- prerequisite graphs;
- learning cells;
- question objects;
- worked solutions;
- hints;
- misconceptions and diagnostics;
- mastery evidence;
- transfer relationships;
- source provenance.

## 2.2 Publishing schema owns

- edition type;
- editorial sequence;
- page type;
- page-component composition;
- answer/teacher metadata visibility;
- writing-space allocation;
- visual-model rendering;
- typography and layout tokens;
- page-break behavior;
- navigation;
- print/screen behavior;
- render QA.

Never place curriculum logic inside CSS/layout rules. Never place page-specific spacing logic inside the learning fingerprint.

---

# 3. Output profiles

Every rendered product must declare an `output_profile`.

```yaml
output_profile:
  id: G4-MATH-STUDENT-A4
  edition: STUDENT
  medium: PRINT_PDF
  page_size: A4
  orientation: PORTRAIT
  color_mode: COLOR
  language: en

  answers_visibility: HIDDEN
  worked_solutions_visibility: SELECTIVE
  hints_visibility: SELECTIVE
  diagnostics_visibility: HIDDEN
  misconception_ids_visibility: HIDDEN
  difficulty_metadata_visibility: HIDDEN
  provenance_visibility: HIDDEN

  show_learning_objectives: true
  show_vocabulary: true
  show_page_numbers: true
  show_section_navigation: true
```

Supported editions:

```text
STUDENT
TEACHER
WORKBOOK
ANSWER_KEY
ASSESSMENT
DIAGNOSTIC
REVISION
```

Supported media:

```text
PRINT_PDF
SCREEN_PDF
DIGITAL_PAGE
```

---

# 4. Edition visibility policy

## 4.1 Student edition

Usually show:

- chapter/lesson title;
- learning goal;
- child-facing explanations;
- source-safe models/illustrations;
- worked examples selected by page plan;
- questions;
- intended helpers/hints;
- writing space;
- review and challenge tasks.

Usually hide:

- correct answer metadata;
- diagnostic codes;
- error-signature IDs;
- difficulty vectors;
- internal concept IDs;
- provenance implementation fields;
- teacher commentary.

## 4.2 Teacher edition

May additionally show:

- objective and prerequisite notes;
- expected reasoning;
- answer and solution;
- misconceptions;
- error signatures;
- diagnostic probe;
- repair suggestion;
- alternative strategy;
- mastery evidence;
- question difficulty;
- transfer level;
- provenance/reference notes where appropriate.

## 4.3 Workbook edition

Prioritize:

- concise concept reminder;
- guided/independent practice;
- adequate writing space;
- reduced teacher exposition;
- no exposed answer content.

## 4.4 Answer-key edition

Prioritize compact cross-referenced answers, with worked solutions only where useful.

---

# 5. Chapter / unit plan

The concept/skill map answers **what must be learned**. The `chapter_plan` answers **what editorial sequence the learner experiences**.

```yaml
chapter_plan:
  id: DIV-G4-CHAPTER-PLAN-01
  subject: Mathematics
  grade: 4
  chapter_id: DIV-G4
  title: Division

  sections:
    - id: S01
      type: CHAPTER_OPENER

    - id: S02
      type: LEARNING_CELL
      learning_cell_id: DIV-LC-01

    - id: S03
      type: LEARNING_CELL
      learning_cell_id: DIV-LC-02

    - id: S04
      type: CHECKPOINT
      concept_ids:
        - DIV-M1.1
        - DIV-M1.2

    - id: S05
      type: LEARNING_CELL
      learning_cell_id: DIV-LC-03

    - id: S06
      type: REASONING_LAB

    - id: S07
      type: MIXED_REVIEW

    - id: S08
      type: CHAPTER_ASSESSMENT
```

Common section types:

```text
CHAPTER_OPENER
UNIT_OPENER
LEARNING_CELL
CONCEPT_DISCOVERY
WORKED_EXAMPLE_SET
GUIDED_PRACTICE
INDEPENDENT_PRACTICE
CHECKPOINT
MISCONCEPTION_CLINIC
REASONING_LAB
PROBLEM_SOLVING
TRANSFER_CHALLENGE
OLYMPIAD_BRIDGE
MIXED_REVIEW
SPIRAL_REVIEW
CHAPTER_ASSESSMENT
ANSWER_KEY
TEACHER_NOTES
```

---

# 6. Page plan

A `page_plan` is the deterministic composition contract for a rendered page.

```yaml
page_plan:
  page_id: DIV-P012
  page_type: CONCEPT_DISCOVERY
  chapter_id: DIV-G4
  learning_cell_id: DIV-LC-02

  components:
    - type: LESSON_HEADER
      source: learning_cell.title

    - type: LEARNING_GOAL
      source: learning_cell.objective

    - type: LAUNCH_CONTEXT
      source: learning_cell.launch_context

    - type: VISUAL_MODEL
      model_id: VM-DIV-024-GROUPS

    - type: WHAT_SHOULD_I_NOTICE
      source: learning_cell.what_to_notice

    - type: CONCEPT_CONNECTION
      source: learning_cell.concept_trigger

    - type: TRY_IT
      question_ids:
        - DIV-G4-0012
```

The page plan controls composition. It must not invent learning content that does not exist in source data.

---

# 7. Canonical Grade 4 page types

Recommended reusable page types:

```text
P01 CHAPTER_OPENER
P02 CONCEPT_DISCOVERY
P03 CONNECT_REPRESENTATIONS
P04 WORKED_EXAMPLE
P05 GUIDED_PRACTICE
P06 INDEPENDENT_PRACTICE
P07 WORD_PROBLEM_LAB
P08 REASONING_PAGE
P09 MISCONCEPTION_CLINIC
P10 CHECKPOINT
P11 TRANSFER_CHALLENGE
P12 MIXED_REVIEW
P13 ASSESSMENT
P14 ANSWER_KEY
P15 TEACHER_GUIDANCE
```

A lesson may use multiple pages. Do not force one Learning Cell into exactly one page.

---

# 8. Page-component library

Pages should be assembled from reusable components rather than hand-formatted each time.

## 8.1 Shared components

```text
CHAPTER_HEADER
LESSON_HEADER
SECTION_HEADER
LEARNING_GOAL
BIG_IDEA
VOCABULARY_BOX
LAUNCH_CONTEXT
WHAT_SHOULD_I_NOTICE
CONCEPT_TRIGGER
HELPER_BOX
WORKED_EXAMPLE
GUIDED_EXAMPLE
TRY_IT
PRACTICE_BLOCK
REMEMBER_BOX
CHECK_BOX
MISTAKE_DETECTIVE
REASONING_CHALLENGE
TRANSFER_CHALLENGE
OLYMPIAD_BRIDGE
EXIT_CHECK
SPIRAL_REVIEW
ANSWER_BLOCK
TEACHER_NOTE
PROVENANCE_NOTE
```

## 8.2 Mathematics-specific components

```text
COUNTER_MODEL
EQUAL_GROUPS_MODEL
ARRAY_MODEL
BAR_MODEL
NUMBER_LINE_MODEL
PLACE_VALUE_MODEL
PARTITION_MODEL
FACT_FAMILY_MODEL
EQUATION_MODEL
WRITTEN_ALGORITHM_MODEL
GEOMETRY_DIAGRAM
TABLE_OR_GRAPH
```

## 8.3 English-specific components

```text
PASSAGE_BLOCK
POEM_BLOCK
TEXT_EVIDENCE_BOX
VOCABULARY_CONTEXT_BOX
GRAMMAR_PATTERN_BOX
SENTENCE_EDIT_BLOCK
WRITING_PROMPT
WRITING_PLANNER
REVISION_CHECKLIST
RUBRIC_BLOCK
```

---

# 9. Structured visual-model specification

Instructional visuals should preferably be generated from structured data rather than stored only as raster screenshots.

## 9.1 Visual-model record

```json
{
  "id": "VM-DIV-024-GROUPS",
  "subject": "Mathematics",
  "type": "EQUAL_GROUPS",
  "instructional_role": "STRUCTURAL_MODEL",
  "data": {
    "total": 24,
    "group_size": 6,
    "number_of_groups": 4
  },
  "display": {
    "show_group_boundaries": true,
    "show_labels": true,
    "show_equation": false
  }
}
```

Supported Grade 4 mathematics model types may include:

```text
COUNTERS
EQUAL_GROUPS
ARRAY
BAR_MODEL
NUMBER_LINE
PLACE_VALUE_BLOCKS
PARTITION_MODEL
FACT_FAMILY
NUMBER_PATTERN
FRACTION_MODEL
MEASUREMENT_MODEL
GEOMETRY_DIAGRAM
TABLE
GRAPH
WRITTEN_ALGORITHM
```

## 9.2 Asset classes

Every asset must be classified as one of:

```text
SOURCE_ASSET
GENERATED_INSTRUCTIONAL_MODEL
AUTHOR_CREATED_DIAGRAM
DECORATIVE_ILLUSTRATION
ICON
```

Decorative illustrations must not carry mathematical or textual meaning unless explicitly encoded as instructional assets.

---

# 10. Presentation metadata on questions

Pedagogical content remains immutable, but a renderer needs layout hints.

```json
{
  "presentation": {
    "preferred_component": "GUIDED_PRACTICE",
    "working_space": "MEDIUM",
    "keep_with_asset": true,
    "allow_page_split": false,
    "show_question_number": true,
    "show_hint_marker": false,
    "option_layout": "SINGLE_COLUMN",
    "answer_lines": 0
  }
}
```

`working_space` values:

```text
NONE
SMALL
MEDIUM
LARGE
FULL_WIDTH
HALF_PAGE
```

For explanation/writing items, `answer_lines` or a response-area specification should be explicit.

Do not infer answer space only from character count.

---

# 11. Page-break and grouping rules

Keep semantically coupled content together.

Required constraints:

```text
question + essential diagram stay together
worked-example stem + solution opening stay together
heading + first content block stay together
MCQ stem + options stay together where possible
teacher-note anchor stays on same or facing page
answer key cross-reference must remain valid
```

Allow deliberate page breaks before:

```text
new lesson
major checkpoint
reasoning lab
chapter assessment
answer key
```

Avoid orphan headings and single-line spillovers.

---

# 12. Design-token system

Store design decisions centrally.

```yaml
design_tokens:
  page:
    size: A4
    margin_top_mm: 15
    margin_bottom_mm: 15
    margin_inner_mm: 16
    margin_outer_mm: 14

  typography:
    body_role: BODY
    body_min_pt: 10.5
    question_min_pt: 11
    caption_min_pt: 9

  spacing:
    base_unit_pt: 4

  borders:
    component_radius_pt: 6

  navigation:
    show_page_number: true
    show_chapter_marker: true
```

Exact fonts/colors belong to a visual theme, not subject pedagogy.

---

# 13. Rendering pipeline

Recommended production architecture:

```text
JSON / structured content
        ↓
content validation
        ↓
chapter-plan compiler
        ↓
page-plan compiler
        ↓
HTML/CSS or equivalent page templates
        ↓
vector/SVG instructional models
        ↓
PDF renderer
        ↓
render each PDF page to image
        ↓
visual QA
        ↓
correction / regeneration
        ↓
final PDF
```

A DOCX-based path may be used when editable authoring is required, but automated high-volume textbook generation should still preserve the structured content/page-plan separation.

---

# 14. Content validation before rendering

Before layout begins, validate:

```text
all referenced question IDs exist
all learning-cell IDs exist
all required answers exist
all visual-model IDs exist
all source assets resolve
all question options are complete
all answer types match answers
all internal cross-references resolve
all edition-visibility rules are valid
all required page components have data
```

Do not use layout/rendering to hide content defects.

---

# 15. PDF/render QA contract

Every final PDF must pass three QA layers.

## 15.1 Content QA

```text
no missing questions
no duplicated question IDs
no missing assets
answer key complete
question numbering consistent
cross-references valid
page references valid
source attribution preserved where required
```

## 15.2 Pedagogy QA

```text
student edition does not reveal answers accidentally
early hints do not reveal full solution
visual model matches the actual question/equation
worked solution matches final answer
remainder/context answer is correct
teacher diagnostic corresponds to actual misconception
writing space matches task demand
lesson sequence preserves intended progression
```

## 15.3 Layout/visual QA

```text
no text overflow
no overlapping components
no clipped diagrams
no orphan headings
no unintended blank pages
no question separated from essential diagram
no option list split awkwardly
minimum font sizes respected
diagrams legible at normal print size
writing space adequate
margins consistent
page rhythm visually coherent
```

Final QA workflow:

```text
RENDER PDF
   ↓
RENDER ALL PAGES TO IMAGES
   ↓
INSPECT
   ↓
CORRECT CONTENT / PAGE PLAN / TEMPLATE
   ↓
RENDER AGAIN
   ↓
REPEAT UNTIL PASS
```

---

# 16. Student/teacher single-source rule

The same immutable question and Learning Cell data should feed all editions.

```text
                     STRUCTURED CONTENT
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
       STUDENT PDF     TEACHER PDF     WORKBOOK PDF
```

Do not maintain independent copies of the same question for student and teacher editions merely to change answer visibility.

Edition differences belong in `output_profile`, page plan, and component visibility.

---

# 17. Example — Division student page plan

```yaml
page_plan:
  page_id: DIV-P021
  page_type: WORKED_EXAMPLE
  output_profiles:
    - G4-MATH-STUDENT-A4

  learning_cell_id: DIV-LC-07

  components:
    - type: LESSON_HEADER
      content: Divide Using Place Value

    - type: LEARNING_GOAL
      bind: learning_cell.objective

    - type: WORKED_EXAMPLE
      question_id: DIV-G4-PLACE-001
      display:
        show_what_to_notice: true
        show_strategy: true
        show_verification: true

    - type: GUIDED_PRACTICE
      question_ids:
        - DIV-G4-PLACE-002
        - DIV-G4-PLACE-003
      presentation:
        working_space: MEDIUM

    - type: EXIT_CHECK
      question_id: DIV-G4-PLACE-004
```

---

# 18. Example — Division teacher overlay

The same page may expose teacher-only metadata:

```yaml
teacher_overlay:
  for_page_id: DIV-P021

  notes:
    - bind: learning_cell.prerequisites
    - bind: question.misconceptions
    - bind: question.diagnostic_probes
    - bind: question.mastery_evidence_tags

  answers:
    visibility: SHOW

  difficulty_profile:
    visibility: SHOW_COMPACT
```

---

# 19. File/data organization recommendation

```text
chapter/
├── chapter.json
├── concept-map.json
├── prerequisite-graph.json
├── chapter-plan.json
│
├── learning-cells/
│   ├── ...
│
├── questions/
│   ├── question-library.json
│   └── assessment-library.json
│
├── models/
│   ├── visual-models.json
│
├── assets/
│   ├── source/
│   ├── generated/
│   └── decorative/
│
└── publishing/
    ├── output-profiles.json
    ├── page-plan.json
    ├── design-tokens.json
    └── qa-report.json
```

---

# 20. Publishing QA report schema

```json
{
  "qa_report": {
    "artifact_id": "DIV-G4-STUDENT-PDF-V1",
    "content_validation": "PASS",
    "pedagogy_validation": "PASS",
    "layout_validation": "PASS",
    "visual_page_review": "PASS",

    "issues": [],

    "render": {
      "page_count": 0,
      "page_size": "A4",
      "edition": "STUDENT"
    },

    "approved_for_release": true
  }
}
```

Any unresolved correctness or visibility issue must block release even if the page looks visually attractive.

---

# 21. Non-negotiable publishing rules

1. **Do not write directly into PDF as the primary content-authoring step.** Structured validated content must exist first.
2. **Do not couple pedagogy to page geometry.** A Learning Cell must remain valid even if the visual theme/page size changes.
3. **Do not rasterize instructional models unnecessarily.** Prefer structured/vector models where practical.
4. **Do not duplicate student/teacher content records.** Use edition filtering.
5. **Do not let layout hide missing content or wrong answers.** Validate first.
6. **Do not allow decorative art to become mathematically or linguistically ambiguous.**
7. **Render every final PDF to page images and visually inspect it before release.**
8. **Preserve provenance and source distinctions in the master data even when hidden from the student edition.**
9. **Writing/working space is instructional design.** Allocate it intentionally.
10. **The final artifact is a rendered product, not an exported text dump.**

---

# 22. Relationship to subject schemas

```text
Grade4MathSchema.md
        │
        ├── Grade4MathDivisionSchema.md
        │          ↓
        │     structured Division content
        │          ↓
        └──── Grade4PublishingSchema.md
                   ↓
             Student / Teacher /
             Workbook / Assessment PDF

Grade4EnglishSchema.md
        │
        └──── Grade4PublishingSchema.md
                   ↓
             English rendered products
```

The publishing schema is deliberately shared. The Math and English **learning schemas remain distinct**.
