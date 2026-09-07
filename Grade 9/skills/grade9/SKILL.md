---
name: grade9
description: Route Grade 9 learning-material tasks to the correct source-grounding, concept architecture, question-bank, enrichment, subtopic-completeness audit, transfer-coverage audit, subject, concept-book, and publishing workflows. Use for Grade 9 source analysis, textbook creation, concept books, difficulty-matched question banks, HOTS/competitive-foundation practice, diagnostics, mixed mastery, challenge appendices, external-PYQ coverage audits, and linked student/teacher PDF production in Mathematics, Physics, or Chemistry.
---

# Grade 9 Router Skill

Use this skill as the entry point for Grade 9 educational-content work.

## Canonical workflow

```text
SOURCE / USER REQUEST
  -> grade9-source-grounding
  -> relevant subject skill
  -> grade9-concept-architect
  -> grade9-question-bank
  -> grade9-learning-enrichment
  -> grade9-subtopic-completeness-auditor for each drafted subtopic
  -> grade9-transfer-coverage-auditor when external/PYQ transfer coverage is required
  -> canonical master data
  -> grade9-textbook-publisher when a rendered artifact is requested
  -> final QA
```

## Route by task

- Source PDF, images, notes, worksheet, PYQ, or pasted notes -> `../grade9-source-grounding/SKILL.md` first.
- Mathematics -> `../grade9-math/SKILL.md`.
- Physics -> `../grade9-physics/SKILL.md`.
- Physics subtopic-wise paired **Study Guide + ExamSIDE/PYQ Transfer Book** production -> `../grade9-physics-subtopic-book-builder/SKILL.md` after `grade9-physics`.
- Chemistry -> `../grade9-chemistry/SKILL.md`.
- Concept IDs, prerequisites, dependency maps, textbook-to-bank links -> `../grade9-concept-architect/SKILL.md`.
- Similar questions, same-level practice, Core N, HOTS, challenge appendix, mixed tests -> `../grade9-question-bank/SKILL.md`.
- Helpers, progressive hints, misconceptions, diagnostics, transfer questions -> `../grade9-learning-enrichment/SKILL.md`.
- Whole-subtopic audit for source completeness, explanatory structure, real-life/context bridges, concept helpers, misconception repair, scaffold coverage, typography, and rendered layout -> `../grade9-subtopic-completeness-auditor/SKILL.md`.
- Subtopic-by-subtopic external/PYQ accounting, required-question self-checks, duplicate/missing placement, concept-link/hint/solution/source-link coverage -> `../grade9-transfer-coverage-auditor/SKILL.md`.
- Student textbook, question bank, integrated edition, PDF layout, internal links, render/preflight -> `../grade9-textbook-publisher/SKILL.md`.

## Mathematics concept-book routing

When the user asks for a Grade 9 Mathematics **Concept Book**, chalkboard-style explanation, formula-understanding book, or asks to make mathematics structurally understandable rather than formula-first:

1. route through `grade9-math` Concept Book mode;
2. preserve source/anchor coverage authority;
3. use `SEE -> REALIZE -> UNDERSTAND -> ADOPT` as the cognitive sequence;
4. treat `CONNECT` as traceability/navigation rather than a learning stage;
5. require pattern/invariant/representation/reconstruction/transfer before publication;
6. keep Concept Book, First-Step Reference, and Question Bank as distinct companion products.

For Sequence & Series, the Mathematics specialist includes the worked exemplar and summation/hidden-series bridge rules.

## Physics routing

When the user asks for a Grade 9 Physics Concept Book, route through `grade9-physics` and use `SEE THE EQUATION -> REALIZE -> UNDERSTAND`, retaining CONNECT as source traceability/navigation.

When the user instead asks to build Physics **subtopic-wise**, requests the school-reference-book-style information structure, or requests paired **Study Guide + ExamSIDE/PYQ question book** outputs, route:

```text
grade9-source-grounding
-> grade9-physics
-> grade9-physics-subtopic-book-builder
-> grade9-learning-enrichment
-> grade9-subtopic-completeness-auditor
-> grade9-transfer-coverage-auditor when external/PYQ is present
-> grade9-textbook-publisher
```

The Physics subtopic builder owns the paired-product information architecture and incremental build contract; `grade9-physics` remains authoritative for subject correctness.

## Non-negotiable rules

1. Treat user-supplied sources as the primary authority when the request is source-grounded.
2. Never silently repair or replace defective source content. Record QC status and preserve provenance.
3. Treat difficulty as a cognitive profile, not an Easy/Medium/Hard label.
4. Preserve the uploaded anchor difficulty distribution unless the user asks for a different level.
5. Default Core bank size is 30 only when the user does not specify a count.
6. Default next-level appendix is 20 only when the user does not specify a count.
7. Every scored question must have one `primary_concept_id` and may have secondary concepts.
8. Generate textbook/question-bank artifacts from canonical structured master data, not from previously laid-out PDF pages.
9. Keep source-derived, externally verified, and newly authored content distinguishable.
10. Do not declare a rendered product complete until page rendering, link validation, and content QA pass.
11. When an external/PYQ corpus is part of the brief, do not declare a subtopic or chapter complete until the transfer-coverage audit proves all eligible questions are uniquely placed or explicitly deferred to named future subtopics; final chapter acceptance requires zero missing and zero deferred eligible questions.
12. Do not declare a subtopic complete merely because all source facts appear. The subtopic-completeness audit must also pass explanation order, context/bridge, helper, misconception, scaffold, typography, and layout checks.
13. For chemistry PDFs, formula subscripts/superscripts, ionic charges, oxidation-number notation, and equation glyphs must be visually unambiguous at 100% zoom.
14. For Physics paired subtopic books, do not advance to the next subtopic until both Study Guide and transfer book pass the specialist's source/content/visual/font/layout/render and coverage gates.

## Completion gates

Apply the relevant gates:

- `QG1 SOURCE_FIDELITY`
- `QG2 SOURCE_QC`
- `QG3 GRADE_AND_SCOPE`
- `QG4 CONCEPT_COVERAGE`
- `QG5 DIFFICULTY_CALIBRATION`
- `QG6 QUESTION_VARIATION`
- `QG7 PEDAGOGICAL_ENRICHMENT`
- `QG8 DIAGNOSTICS_AND_MASTERY`
- `QG9 PROVENANCE`
- `QG10 PUBLICATION_QA`
- `QG11 TRANSFER_COVERAGE`
- `QG12 SUBTOPIC_COMPLETENESS`

Read `references/grade9-workflow.md` when a full multi-stage build is requested. Use `references/grade9-master.schema.json` as the unchanged canonical structured-data contract when producing reusable master data.
