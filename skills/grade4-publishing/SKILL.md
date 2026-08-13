---
name: grade4-publishing
description: Convert validated Grade 4 Mathematics or English content into chapter plans, page plans, reusable page components, structured visuals, student/teacher/workbook/answer-key editions, and QA-checked PDF products without changing the underlying pedagogy.
---

# Grade 4 Publishing Skill

## Mandatory reference

Always load and follow:

- `../../Grade4PublishingSchema.md`

Also load the active subject schema and any chapter-specific publishing contract.

Known example:

- Division -> `../../Grade4MathDivisionPublishingContract.md`

## Core principle

Publishing is downstream from pedagogy.

```text
VALIDATED SUBJECT CONTENT
  -> OUTPUT PROFILE
  -> CHAPTER / UNIT PLAN
  -> PAGE PLAN
  -> PAGE COMPONENTS
  -> VISUAL / MODEL RENDERING
  -> EDITION FILTERING
  -> PDF RENDER
  -> PAGE-IMAGE QA
  -> FINAL PRODUCT
```

Never alter mathematical meaning, reading text, grammar target, answer logic, rubric criteria, or learning progression merely to make content fit a page.

## Preconditions

Before publishing, confirm the subject workflow has produced validated content containing the applicable items:

- chapter/unit structure;
- Learning Cells;
- questions/tasks;
- answers or writing rubrics;
- worked examples/model responses;
- instructional visuals/models or specifications;
- teacher notes/diagnostics where relevant;
- provenance/source metadata.

If content is pedagogically incomplete, return to the subject skill rather than solving the gap with layout.

## Supported output profiles

```text
STUDENT_TEXTBOOK
TEACHER_EDITION
WORKBOOK
ANSWER_KEY
ASSESSMENT_BOOKLET
REVISION_BOOKLET
SCREEN_PDF
PRINT_PDF
```

An output may combine profile + medium, e.g. `STUDENT_TEXTBOOK + PRINT_PDF`.

## Stage 1 — Build output profile

Resolve:

```yaml
edition: STUDENT | TEACHER | WORKBOOK | ANSWER_KEY | ASSESSMENT
medium: PRINT_PDF | SCREEN_PDF
page_size: A4 | source_required_size
color_mode: COLOR | GRAYSCALE
answer_visibility: HIDDEN | VISIBLE
hint_visibility: HIDDEN | SELECTIVE | VISIBLE
diagnostics_visibility: HIDDEN | TEACHER_ONLY
provenance_visibility: INTERNAL | APPENDIX | VISIBLE
```

Do not expose teacher-only diagnostic metadata in a student edition.

## Stage 2 — Build chapter/unit plan

The subject schema defines **what must be learned**. The chapter/unit plan defines **the editorial order in which the learner experiences it**.

Possible section types:

```text
CHAPTER_OPENER
UNIT_OPENER
LEARNING_CELL
CONCEPT_DISCOVERY
WORKED_EXAMPLE
GUIDED_PRACTICE
INDEPENDENT_PRACTICE
CHECKPOINT
REASONING_LAB
MISCONCEPTION_CLINIC
APPLICATION
TRANSFER_CHALLENGE
MIXED_REVIEW
CHAPTER_ASSESSMENT
ANSWER_KEY
TEACHER_NOTES
PROVENANCE_APPENDIX
```

Preserve source sequence for source-faithful products unless redesign is explicitly requested.

## Stage 3 — Build page plan

Every page should have an explicit `page_type` and ordered component list.

Example:

```yaml
page_id: P012
page_type: CONCEPT_DISCOVERY
learning_cell_id: ...
components:
  - LESSON_HEADER
  - LEARNING_GOAL
  - LAUNCH_CONTEXT
  - INSTRUCTIONAL_MODEL
  - WHAT_SHOULD_I_NOTICE
  - CONCEPT_CONNECTION
  - TRY_IT
```

Do not make the renderer infer pedagogy from raw prose.

## Stage 4 — Reusable component system

Prefer reusable semantic components over hand-formatted pages.

Shared components may include:

```text
ChapterHeader
UnitHeader
LessonHeader
LearningObjective
BigIdea
VocabularyBox
LaunchContext
WhatShouldINotice
ConceptConnection
WorkedExample
GuidedPractice
IndependentPractice
TryIt
RememberBox
MistakeDetective
ReasoningChallenge
TransferChallenge
ReviewBlock
AssessmentBlock
AnswerKeyBlock
TeacherNote
ProvenanceNote
```

Math-specific components may include:

```text
ConcreteModel
EqualGroupsModel
ArrayModel
BarModel
NumberLineModel
PlaceValueModel
FactFamilyModel
EquationModel
WrittenProcedureModel
```

English-specific components may include:

```text
PassageBlock
PoemBlock
VocabularyFocus
TextEvidenceBox
GrammarRuleBox
SentenceModel
WritingPrompt
PlanningOrganizer
ModelResponse
RevisionChecklist
WritingRubric
```

## Stage 5 — Structured visual models

Whenever possible, store instructional visuals as data rather than screenshots.

Example:

```json
{
  "type": "EQUAL_GROUPS",
  "total": 24,
  "group_size": 6,
  "show_labels": true,
  "show_equation": false
}
```

Supported math model families may include:

```text
COUNTERS
EQUAL_GROUPS
ARRAY
BAR_MODEL
NUMBER_LINE
PLACE_VALUE_BLOCKS
PARTITION_MODEL
FACT_FAMILY
EQUATION
WRITTEN_PROCEDURE
```

For English, preserve source illustrations when instructional meaning depends on them; otherwise use clearly marked authored/supporting visuals.

Every visual must have a semantic purpose. Decorative imagery must never obscure or substitute for instructional models.

## Stage 6 — Presentation metadata

Allow content records to carry non-pedagogical presentation hints such as:

```json
{
  "presentation": {
    "preferred_component": "GUIDED_PRACTICE",
    "working_space": "MEDIUM",
    "keep_with_asset": true,
    "allow_page_split": false,
    "show_question_number": true,
    "answer_lines": 3,
    "option_layout": "ONE_COLUMN"
  }
}
```

Presentation metadata must not change question meaning or difficulty.

## Stage 7 — Edition filtering

### Student edition

Typically show:

- learning goals;
- concept explanations;
- examples/models;
- selected helpers/hints when intended;
- practice/tasks;
- reasoning/transfer;
- review/assessment.

Typically hide:

- correct answers before answer-key section;
- internal difficulty vectors;
- misconception IDs;
- diagnostic codes;
- mastery metadata;
- internal provenance fields.

### Teacher edition

May additionally show:

- prerequisites;
- expected reasoning;
- what to watch for;
- misconceptions/error signatures;
- diagnostic probes;
- repair suggestions;
- answers and alternative methods;
- rubric notes;
- difficulty/transfer level;
- mastery evidence;
- provenance/editorial notes.

### Workbook

Favor response space, reduced exposition, deliberate practice progression, mixed review, and clear references to the corresponding learning concept.

### Answer key

Keep question IDs/numbers stable and provide enough reasoning to verify answers. Do not silently introduce alternative numbering.

## Stage 8 — Page rhythm and cognitive load

A Grade 4 page must be visually and cognitively manageable.

Avoid:

- walls of text;
- too many unrelated callouts;
- tiny instructional diagrams;
- excessive questions without writing space;
- answer choices split awkwardly across pages;
- a question separated from its required model/passage;
- a worked example continued invisibly without clear navigation.

Use whitespace and hierarchy as instructional tools.

## Stage 9 — Rendering pipeline

Preferred general pipeline:

```text
STRUCTURED JSON / CONTENT
  -> PAGE COMPILER
  -> HTML/CSS or equivalent semantic templates
  -> PDF
  -> RENDER EVERY PAGE TO IMAGE
  -> VISUAL QA
  -> FIX
  -> RE-RENDER
  -> FINAL PDF
```

A DOCX intermediate is acceptable when editability is the priority, but maintain semantic component mapping and run final PDF QA.

Use the host environment's PDF/document capabilities and follow their artifact-generation requirements.

## Stage 10 — Content QA before render

Check:

- no missing questions/tasks;
- no missing answers/rubrics;
- no missing instructional assets;
- model/equation/text consistency;
- question numbering unique and stable;
- cross-references valid;
- edition visibility rules correct;
- provenance retained internally;
- source content not silently altered.

## Stage 11 — Layout QA after render

Render every PDF page to an image and inspect:

- text overflow/clipping;
- component overlap;
- orphan headings;
- awkward page breaks;
- question separated from required asset/passage;
- tiny/illegible diagrams;
- broken symbols/equations;
- excessive whitespace or overcrowding;
- inconsistent margins/spacing;
- adequate response space;
- accidental answer visibility;
- page numbers/navigation consistency.

## Stage 12 — Pedagogical render QA

Visual correctness is not enough. Also verify:

- instructional model matches the source/data;
- answer key matches rendered question;
- hints do not leak unintended answers;
- student edition does not expose teacher diagnostics;
- page sequence preserves intended learning progression;
- writing tasks have adequate planning/drafting space;
- reading questions remain attached to the relevant text;
- source-faithful content has not been editorially changed by layout operations.

## Stage 13 — Product validation record

For each final product retain at minimum:

```yaml
product_id: ...
edition: ...
source_content_version: ...
page_count: ...
render_date: ...
content_qa: PASS | FAIL
layout_qa: PASS | FAIL
pedagogy_qa: PASS | FAIL
known_issues: []
```

## Publishing quality gates

A rendered product is not complete until all applicable gates pass:

- `P-QG1 VALIDATED_INPUT_CONTENT`
- `P-QG2 OUTPUT_PROFILE_COMPLETE`
- `P-QG3 CHAPTER_UNIT_PLAN_VALID`
- `P-QG4 PAGE_PLAN_COMPLETE`
- `P-QG5 COMPONENT_BINDINGS_VALID`
- `P-QG6 VISUAL_MODEL_SEMANTICS_VALID`
- `P-QG7 EDITION_FILTERING_VALID`
- `P-QG8 CONTENT_QA_PASS`
- `P-QG9 FULL_PAGE_RENDER_COMPLETE`
- `P-QG10 LAYOUT_QA_PASS`
- `P-QG11 PEDAGOGICAL_RENDER_QA_PASS`
- `P-QG12 FINAL_PRODUCT_RECORD_COMPLETE`

## Handoff rule

If publishing exposes a missing concept, ambiguous answer, weak diagnostic, unsuitable question, or source discrepancy, return the issue to the appropriate subject skill. Do not repair pedagogical content inside the publishing layer without updating the source content record.
