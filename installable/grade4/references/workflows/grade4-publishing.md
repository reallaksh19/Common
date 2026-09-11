---
name: grade4-publishing
description: Convert validated Grade 4 Mathematics or English content into visual-first, child-friendly student products and separate teacher/parent/workbook/answer-key editions with structured instructional visuals, reusable page components, page-image QA, and explicit release gates.
---

# Grade 4 Publishing Skill

## Mandatory references

Always load and follow:

- `../schemas/Grade4PublishingSchema.md`
- `../schemas/Grade4VisualPublishingAcceptance.md`

Also load the active subject schema and any chapter-specific publishing contract.

Known example:

- Division -> `../schemas/Grade4MathDivisionPublishingContract.md`

## Core principle

Publishing is downstream from pedagogy, but child usability is a release criterion.

```text
VALIDATED SUBJECT CONTENT
  -> OUTPUT PROFILE
  -> CHAPTER / UNIT PLAN
  -> PAGE PLAN
  -> PAGE COMPONENTS
  -> VISUAL / MODEL RENDERING
  -> EDITION FILTERING
  -> PDF RENDER
  -> RENDER EVERY PAGE TO IMAGE
  -> CHILD-USABILITY + LAYOUT + PEDAGOGY QA
  -> FINAL PRODUCT
```

A technically correct PDF that reads like a research paper or adult notes is not an acceptable Grade 4 student product.

## VISUAL_FIRST student default

Unless the source explicitly requires a text-heavy format, Grade 4 study/revision products should default to `VISUAL_FIRST`.

A student concept/worked-example page should normally include:

- one dominant learning idea;
- at least one meaningful instructional visual/model/organizer when one exists;
- short child-facing chunks instead of long paragraphs;
- generous whitespace and readable diagrams;
- one visible child action such as notice, point, draw, choose, complete, explain, solve, or check;
- adequate working/response space.

Avoid walls of text, research-style explanations, teacher terminology, diagnostic codes, dense bullets without models, tiny diagrams, and several consecutive explanation-only pages.

If content does not fit child-readably, split or redesign the page plan rather than shrinking the page.

## Student / adult edition separation

Prefer separate outputs:

```text
STUDENT PRODUCT
  child-facing concept visuals
  worked examples
  short cues
  practice
  reasoning / transfer
  self-check

TEACHER / PARENT PRODUCT
  what to watch for
  possible error patterns
  diagnostic probes
  H1-H3 quick hints
  repair suggestion
  independent retry
  support-fading / stop rule
```

A student guide must not become a diagnostic manual.

## H1-H3 Teacher / Parent quick-hint profile

For a visual Teacher / Parent key:

```text
H1 NOTICE
  Point to the important feature without supplying the method.

H2 REMEMBER
  Trigger a relevant fact, rule, relationship, place-value idea, or unit fact.

H3 REPRESENT
  Change or externalize representation: groups, bar model, place-value chart,
  number line, unit chain, multiples strip, organizer, etc.
```

Use progressively:

```text
H1 -> if insufficient H2 -> if insufficient H3 -> NEW INDEPENDENT RETRY
```

If H1 works, stop. If H3 works, fade/remove the representation on the next retry where appropriate.

Hints restart thinking; they must not become staged answer revelation.

For misconception/error cards, prefer:

```text
WHAT YOU MAY SEE
      ↓
VISUAL EXAMPLE / STRUCTURE
      ↓
H1 NOTICE
      ↓
H2 REMEMBER
      ↓
H3 REPRESENT
      ↓
INDEPENDENT RETRY
      ↓
STOP / FADE RULE
```

## Page/component planning

Every page should have an explicit page type and ordered semantic components. Do not make the renderer infer pedagogy from raw prose.

Useful components include:

```text
LessonHeader
LearningObjective
LaunchContext
InstructionalModel
WhatShouldINotice
WorkedExample
GuidedPractice
IndependentPractice
TryIt
RememberBox
MistakeDetective
ReasoningChallenge
TransferChallenge
AnswerKeyBlock
TeacherNote
HintLadderCard
IndependentRetry
```

## Structured visuals

Use structured instructional models where possible.

Math examples:

```text
COUNTERS
EQUAL_GROUPS
ARRAY
BAR_MODEL
NUMBER_LINE
PLACE_VALUE_MODEL
FACT_FAMILY
MULTIPLES_STRIP
EQUATION
WRITTEN_PROCEDURE
UNIT_CHAIN
REMAINDER_CONTEXT_MODEL
ERROR_COMPARISON
```

English examples:

```text
STORY_SEQUENCE
CHARACTER_EVIDENCE_MAP
MAIN_IDEA_DETAIL_MAP
COMPARE_CONTRAST_MAP
GRAMMAR_PATTERN_STRIP
SENTENCE_MODEL
WORD_FAMILY_MAP
WRITING_PLANNER
TEXT_EVIDENCE_HIGHLIGHT
```

Visuals should carry instructional meaning. Decorative imagery may support engagement but cannot replace the model.

## Division publishing expectations

For Grade 4 Division, visually support relevant items such as:

- equal sharing vs equal grouping;
- multiplication/division fact family;
- estimation before exact division;
- multiples strip for 2-digit divisors;
- long-division place-value alignment;
- zero in the quotient;
- word-problem structure;
- quantity/unit chains such as dozen -> items -> money;
- remainder meaning;
- mistake-detective comparison.

Teacher / Parent keys using hints should include visual H1-H3 sequences for high-value patterns such as wrong operation choice, missing zero in quotient, unit/dozen conversion, 2-digit divisor support, and remainder interpretation. Each repair sequence ends with a fresh independent retry.

## Workbook / answer key

Workbook pages favor response space, concise reminders, guided -> independent progression, mixed review, and minimal exposition.

Answer keys retain stable numbering and provide enough reasoning to verify answers without becoming a second textbook unless requested.

## Rendering and QA

```text
STRUCTURED CONTENT / PAGE PLAN
  -> RENDER PDF
  -> RENDER EVERY PAGE TO IMAGE
  -> INSPECT PAGE IMAGES
  -> FIX PAGE PLAN / VISUAL / TYPE / SPACING
  -> RE-RENDER
  -> REPEAT UNTIL PASS
```

Do not approve a Grade 4 PDF from source text or code alone.

### Child-usability QA

Ask:

- Does this look designed for a Grade 4 child, or like adult notes placed into a PDF?
- Is there enough visual structure?
- Is prose short and child-facing?
- Can the learner tell what to notice and what to do next?
- Does the page ask the learner to do something?
- Would an average learner need an adult simply to decode the page design/explanation?

If the last answer is YES, revise before delivery.

### Teacher/Parent hint QA

Verify:

- H1/H2/H3 are progressive, not paraphrases;
- early hints do not leak answers;
- an independent retry follows repair;
- a stop/fade rule prevents over-helping.

## Product validation record

Retain at minimum:

```yaml
product_id: ...
edition: ...
visual_profile: VISUAL_FIRST | SOURCE_FAITHFUL_TEXT_HEAVY
page_count: ...
content_qa: PASS | FAIL
layout_qa: PASS | FAIL
child_usability_qa: PASS | FAIL
pedagogy_qa: PASS | FAIL
hint_ladder_qa: PASS | NOT_APPLICABLE | FAIL
known_issues: []
```

## Publishing quality gates

```text
P-QG1  VALIDATED_INPUT_CONTENT
P-QG2  OUTPUT_PROFILE_COMPLETE
P-QG3  CHAPTER_UNIT_PLAN_VALID
P-QG4  PAGE_PLAN_COMPLETE
P-QG5  COMPONENT_BINDINGS_VALID
P-QG6  VISUAL_MODEL_SEMANTICS_VALID
P-QG7  EDITION_FILTERING_VALID
P-QG8  CONTENT_QA_PASS
P-QG9  FULL_PAGE_RENDER_COMPLETE
P-QG10 LAYOUT_QA_PASS
P-QG11 PEDAGOGICAL_RENDER_QA_PASS
P-QG12 FINAL_PRODUCT_RECORD_COMPLETE
P-QG13 CHILD_FACING_VISUAL_FIRST
P-QG14 CHILD_LANGUAGE_AND_DENSITY_PASS
P-QG15 STUDENT_ADULT_EDITION_SEPARATION
P-QG16 INSTRUCTIONAL_VISUAL_COVERAGE
P-QG17 LEARNER_ACTION_DENSITY
P-QG18 HINT_LADDER_RENDER_VALID
P-QG19 INDEPENDENT_RETRY_VISIBLE
P-QG20 PAGE_IMAGE_CHILD_USABILITY_PASS
```

For normal Grade 4 student guides, failure of P-QG13, P-QG14, P-QG16, P-QG17, or P-QG20 blocks release.

For Teacher / Parent diagnostic keys with hints, failure of P-QG18 or P-QG19 blocks release.

## Cold-start checklist

Before delivery, answer YES where applicable:

```text
[ ] Is the intended reader explicit?
[ ] Is the student edition visual-first unless source constraints require otherwise?
[ ] Does every major new concept have a meaningful visual/model when one exists?
[ ] Is prose chunked and child-friendly rather than research-style?
[ ] Are adult diagnostics separated from student content?
[ ] Are there observable learner actions, not only explanations?
[ ] If hints are shown to adults, are H1 NOTICE, H2 REMEMBER, H3 REPRESENT progressive?
[ ] Does repair end with an independent retry?
[ ] Were all PDF pages rendered to images and visually inspected?
[ ] Would an average Grade 4 learner understand how to use the page without repeatedly asking what the page means?
```

If the last answer is NO, the product is not finished.
