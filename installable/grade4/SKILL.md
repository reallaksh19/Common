---
name: grade4
description: Create Grade 4 Mathematics and English learning materials, diagnostics, assessments, textbook chapters, workbooks, and visual-first QA-checked PDF products using subject-specific schemas, Primary teaching semantics, and publishing workflows. Use for Grade 4 source analysis, chapter design, learning cells, question banks, Olympiad/HOTS extensions, student editions, teacher/parent keys, and PDF-ready content.
---

# Grade 4 Learning Studio

## Job to be done

Turn Grade 4 source material or a Grade 4 learning request into developmentally appropriate, textbook-quality Mathematics or English content using the bundled subject schemas. Keep Mathematics and English pedagogies distinct. Use the publishing workflow only after subject content is validated.

For child-facing rendered products, correctness alone is insufficient: the result must also pass the visual-first, child-language, learner-action, and page-image usability gates.

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
- **Mandatory child-facing acceptance:** `references/schemas/Grade4VisualPublishingAcceptance.md`
- Division publishing contract: `references/schemas/Grade4MathDivisionPublishingContract.md`

Load only the references needed for the current task, except that any Grade 4 PDF/book/workbook/teacher-key task must load the publishing workflow, publishing schema, and visual publishing acceptance contract.

## Routing

1. Determine subject: `MATHEMATICS` or `ENGLISH`.
2. Determine task mode from the user's request.
3. Load the subject workflow and core schema.
4. If a topic-specific schema exists, load it as an additional specialization.
5. If a rendered/book/PDF/workbook/teacher-edition output is requested, validate subject content first, then load the publishing workflow, publishing schema, and `Grade4VisualPublishingAcceptance.md`.
6. If a Teacher / Parent diagnostic key exposes hints, use the visual H1-H3 quick-hint publishing profile and require an independent retry.

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
- `BUILD_TEACHER_PARENT_KEY`
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

Only after content QA passes, load:

- `references/workflows/grade4-publishing.md`
- `references/schemas/Grade4PublishingSchema.md`
- `references/schemas/Grade4VisualPublishingAcceptance.md`

For Division, also load `references/schemas/Grade4MathDivisionPublishingContract.md`.

Publishing must remain downstream from pedagogy:

`validated content -> output profile -> chapter/unit plan -> page plan -> reusable components -> structured visuals -> edition filtering -> render -> every-page image QA -> final product`

Generate student, teacher, workbook, answer-key, or assessment editions from the same validated content model where possible.

### Default child-facing rule

For normal Grade 4 student study guides/revision booklets, use `VISUAL_FIRST` unless the source requires text-heavy fidelity.

A student product should not look like adult notes converted to PDF. It should use meaningful visual models/organizers, short child-facing text chunks, whitespace, readable diagrams, and frequent observable learner actions.

### Student / adult separation

Keep full diagnostic reasoning in teacher/parent products rather than exposing it in the child guide.

For visual Teacher / Parent hint keys, prefer:

`H1 NOTICE -> H2 REMEMBER -> H3 REPRESENT -> independent retry -> stop/fade`

Do not automatically show all hints; stop at the smallest level that restarts thinking.

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
For rendered products, content completeness, answer visibility, model correctness, layout integrity, writing space, page rhythm, visual legibility, child-language density, instructional visual coverage, learner-action density, and student/adult edition separation are checked. Final PDFs must be rendered to page images and visually inspected before delivery.

### QG11 Child-facing visual usability
For student guides, fail release if the product is text-dominant, research-style, lacks meaningful instructional visuals where available, or requires an adult simply to decode how the page works.

### QG12 Hint-key quality
For Teacher / Parent keys that expose hints, H1/H2/H3 must be progressive (`NOTICE`, `REMEMBER`, `REPRESENT`), early hints must not leak the answer, and each repair sequence must end with a fresh independent retry.

## Output behavior

Match the user's requested output. If no format is specified, return the educational content or plan directly rather than forcing JSON.

When structured data is requested, preserve stable concept/skill IDs, provenance, learning fingerprints, diagnostics, mastery tags, and transfer links defined by the relevant schema.

When the request is for a textbook-quality product, build content architecture before page layout.

When the request is for a PDF, do not deliver before page-image QA and the visual publishing acceptance checklist pass.

## Extending the skill

For a new Mathematics chapter, use the core Math schema and source material first. A topic specialization may be added later using the naming pattern `Grade4Math<Topic>Schema.md` without creating a new top-level skill.

For English, add domain/topic reference files only when they contain genuinely specialized pedagogy; keep the main English workflow centralized.
