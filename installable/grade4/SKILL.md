---
name: grade4
description: Create Grade 4 Mathematics and English learning materials, diagnostics, assessments, textbook chapters, workbooks, and QA-checked PDF-ready content using subject-specific schemas and publishing workflows. Use for Grade 4 source analysis, chapter design, learning cells, question banks, Olympiad/HOTS extensions, and student/teacher editions.
---

# Grade 4 Learning Studio

## Job to be done

Turn Grade 4 source material or a Grade 4 learning request into developmentally appropriate, textbook-quality Mathematics or English content using the bundled subject schemas. Keep Mathematics and English pedagogies distinct. Use the publishing workflow only after subject content is validated.

## Bundled references

### Mathematics
- `references/workflows/grade4-math.md`
- `references/schemas/Grade4MathSchema.md`
- Division specialization: `references/schemas/Grade4MathDivisionSchema.md`

### English
- `references/workflows/grade4-english.md`
- `references/schemas/Grade4EnglishSchema.md`

### Publishing / PDF-ready products
- `references/workflows/grade4-publishing.md`
- `references/schemas/Grade4PublishingSchema.md`
- Division publishing contract: `references/schemas/Grade4MathDivisionPublishingContract.md`

Load only the references needed for the current task.

## Routing

1. Determine subject: `MATHEMATICS` or `ENGLISH`.
2. Determine task mode from the user's request.
3. Load the subject workflow and core schema.
4. If a topic-specific schema exists, load it as an additional specialization.
5. If a rendered/book/PDF/workbook/teacher-edition output is requested, validate subject content first, then load the publishing workflow and publishing schema.

Do not apply a generic pedagogy across both subjects.

## Supported task modes

- `ANALYZE_SOURCE`
- `BUILD_CHAPTER`
- `BUILD_LEARNING_CELL`
- `BUILD_QUESTION_BANK`
- `BUILD_PRACTICE`
- `BUILD_DIAGNOSTIC`
- `BUILD_ASSESSMENT`
- `BUILD_REVISION`
- `BUILD_OLYMPIAD_OR_HOTS`
- `BUILD_TEXTBOOK`
- `BUILD_WORKBOOK`
- `BUILD_TEACHER_EDITION`
- `BUILD_PDF_READY_CONTENT`

Infer the mode from ordinary language when possible; do not require the user to provide a form.

## Shared source rules

When sources are supplied:

1. Treat them as the requested basis.
2. Preserve source terminology, organization, diagrams/models, and curriculum level where relevant.
3. Do not silently repair or reinterpret defective source items.
4. Distinguish source-derived content from newly authored content.
5. Mark unresolved ambiguity instead of inventing a resolution.
6. Do not silently extend beyond Grade 4 or beyond the supplied curriculum.

## Mathematics routing

Load `references/workflows/grade4-math.md` and `references/schemas/Grade4MathSchema.md`.

If topic is Division, additionally load `references/schemas/Grade4MathDivisionSchema.md`.

Mathematics must be organized around:

`chapter -> macroconcept -> microconcept/Learning Cell -> question instance`

Prioritize concept meaning, prerequisite dependencies, representation progression, reasoning, strategies, controlled variation, causal diagnostics, mastery evidence, and transfer. Do not equate repeated calculation accuracy with mastery.

## English routing

Load `references/workflows/grade4-english.md` and `references/schemas/Grade4EnglishSchema.md`.

English must be organized around:

`text/language feature -> skill -> evidence/language knowledge -> reasoning -> response`

Route internally among Reading, Vocabulary, Grammar, and Writing. Use evidence models for comprehension and rubrics for open writing. Do not force English into the Mathematics representation framework.

## Publishing routing

Only after content QA passes, load `references/workflows/grade4-publishing.md` and `references/schemas/Grade4PublishingSchema.md`.

For Division, also load `references/schemas/Grade4MathDivisionPublishingContract.md`.

Publishing must remain downstream from pedagogy:

`validated content -> output profile -> chapter/unit plan -> page plan -> reusable components -> structured visuals -> edition filtering -> render -> page-image QA -> final product`

Generate student, teacher, workbook, answer-key, or assessment editions from the same validated content model where possible.

## Quality gates

Do not treat work as complete until relevant gates pass.

### QG1 Source fidelity
Source material is represented accurately and provenance is clear.

### QG2 Grade appropriateness
Language, abstraction, arithmetic, reading load, and expected reasoning are appropriate for Grade 4 and the supplied curriculum.

### QG3 Coverage
All required concepts/skills are represented; no major source or curriculum gap is silently omitted.

### QG4 Progression
Learning develops deliberately rather than appearing as a list of facts or random questions.

### QG5 Representation / evidence
For Math, relevant concrete-pictorial-structural-symbolic connections are present. For English, answers and reasoning are grounded in appropriate text/language evidence.

### QG6 Practice variation
Variation changes meaningful structure, representation, unknown, context, reasoning, or response demand—not only numbers or surface wording.

### QG7 Diagnostics
Major wrong responses or misconceptions connect to useful probes, repair actions, and retry logic.

### QG8 Mastery
Mastery evidence spans more than one task form and is not reduced to a simple correct-count threshold.

### QG9 Transfer
Learners encounter changed representations/contexts or appropriately non-routine tasks after core understanding is established.

### QG10 Publishing QA
For rendered products, content completeness, answer visibility, model correctness, layout integrity, writing space, page rhythm, and visual legibility are checked. Final PDFs should be rendered to page images and visually inspected before delivery.

## Output behavior

Match the user's requested output. If no format is specified, return the educational content or plan directly rather than forcing JSON.

When structured data is requested, preserve stable concept/skill IDs, provenance, learning fingerprints, diagnostics, mastery tags, and transfer links defined by the relevant schema.

When the request is for a textbook-quality product, build content architecture before page layout.

## Extending the skill

For a new Mathematics chapter, use the core Math schema and source material first. A topic specialization may be added later using the naming pattern `Grade4Math<Topic>Schema.md` without creating a new top-level skill.

For English, add domain/topic reference files only when they contain genuinely specialized pedagogy; keep the main English workflow centralized.
