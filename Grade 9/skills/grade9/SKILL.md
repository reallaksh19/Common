---
name: grade9
description: Route Grade 9 learning-material tasks to the correct source-grounding, concept architecture, question-bank, enrichment, publication-reconstruction, subtopic-completeness audit, transfer-coverage audit, subject, concept-book, Redox subtopic-book, and publishing workflows. Use for Grade 9 source analysis, source-faithful PDF reconstruction, textbook creation, concept books, difficulty-matched question banks, HOTS/competitive-foundation practice, diagnostics, mixed mastery, challenge appendices, external-PYQ coverage audits, and linked student/teacher PDF production in Mathematics, Physics, or Chemistry.
---

# Grade 9 Router Skill

Use this skill as the entry point for Grade 9 educational-content work.

## Canonical workflow

```text
SOURCE / USER REQUEST
  -> grade9-source-grounding
  -> relevant subject skill
  -> specialist builder when applicable (for Redox: grade9-redox-subtopic-book-builder)
  -> grade9-concept-architect
  -> grade9-question-bank
  -> grade9-learning-enrichment
  -> grade9-publication when an existing source PDF/book must be reconstructed without losing core content
  -> grade9-subtopic-completeness-auditor for each drafted subtopic
  -> grade9-transfer-coverage-auditor when external/PYQ transfer coverage is required
  -> canonical master data
  -> grade9-textbook-publisher when a validated master-data product is rendered
  -> final QA
```

## Route by task

- Source PDF, images, notes, worksheet, PYQ, or pasted notes -> `../grade9-source-grounding/SKILL.md` first.
- Mathematics -> `../grade9-math/SKILL.md`.
- Physics -> `../grade9-physics/SKILL.md`.
- Chemistry -> `../grade9-chemistry/SKILL.md`.
- Source-grounded Redox Study Guide + ExamSIDE subtopic build -> `../grade9-redox-subtopic-book-builder/SKILL.md` together with the completeness and transfer auditors.
- Concept IDs, prerequisites, dependency maps, textbook-to-bank links -> `../grade9-concept-architect/SKILL.md`.
- Similar questions, same-level practice, Core N, HOTS, challenge appendix, mixed tests -> `../grade9-question-bank/SKILL.md`.
- Helpers, progressive hints, misconceptions, diagnostics, transfer questions -> `../grade9-learning-enrichment/SKILL.md`.
- Reconstruct an existing educational PDF/book with zero-loss source mapping, teacher-value additions, benchmarked layout, stable renumbering/cross-links, missing-figure evidence rules, and anti-drift checkpoints -> `../grade9-publication/SKILL.md`.
- Physics subtopic-by-subtopic Study Guide + ExamSIDE/PYQ transfer book -> `../grade9-physics-subtopic-book-builder/SKILL.md`.
- Physics B30/B80/B90 differentiated Core book with Appendix A/B, typed PDF schema and anti-drift audit for a bounded Physics subtopic -> `../grade9-physics-publication/SKILL.md`, with `../grade9-physics-examside/SKILL.md` for its external ExamSIDE/PYQ ledger. Both are executable adapters over `grade9-physics`/`grade9-physics-subtopic-book-builder`/`grade9-publication`, not a replacement authority: use `grade9-physics-subtopic-book-builder` when the deliverable is the paired Study Guide + transfer book itself, and `grade9-physics-publication` when the deliverable is a typed, schema-validated, render-audited Core PDF for a bounded two-topic-scale pilot.
- Whole-subtopic audit for source completeness, explanatory structure, real-life/context bridges, concept helpers, misconception repair, scaffold coverage, chemistry typography, and rendered layout -> `../grade9-subtopic-completeness-auditor/SKILL.md`.
- Subtopic-by-subtopic external/PYQ accounting, required-question self-checks, duplicate/missing placement, concept-link/hint/solution/source-link coverage -> `../grade9-transfer-coverage-auditor/SKILL.md`.
- Student textbook, question bank, integrated edition, PDF layout, internal links, render/preflight from validated canonical master data -> `../grade9-textbook-publisher/SKILL.md`.

## Publication reconstruction routing

When the user supplies an existing PDF/book and asks to rebuild, revamp, benchmark, repaginate, add teacher value, or preserve 100% core content while changing the design:

1. run `grade9-source-grounding` first;
2. use the relevant subject skill to protect subject-specific meaning and representation;
3. invoke `grade9-publication` before large-scale layout work;
4. freeze the source-unit denominator and stable source IDs before redesign;
5. separate `CORE_SOURCE`, `PRESENTATION_SOURCE`, `VALUE_ADD`, and `EDITORIAL_CHANGE` objects;
6. prototype only 6-8 representative pages before scaling;
7. run anti-drift checkpoints every subtopic or 5-10 pages;
8. generate visible numbering/page references from stable targets after pagination;
9. require zero unmapped core units, zero unapproved editorial changes, zero broken links, and zero hidden/clipped core content before claiming 100% reconstruction;
10. use `grade9-textbook-publisher` only when the project transitions to canonical master-data-driven publication rather than source-PDF reconstruction.

## Redox subtopic-book routing

When the task is the continuing Redox project:

1. read the supplied Redox source boundary first;
2. use `grade9-redox-subtopic-book-builder` for one focused subtopic at a time;
3. keep source-derived content separate from external ExamSIDE evidence;
4. freeze the canonical direct-primary ExamSIDE set before publication;
5. require the approved learning grammar, Redox-specific concept helpers, misconception repair, chemistry-safe typography, H1-H3 support and Appendix A;
6. run both `grade9-subtopic-completeness-auditor` and `grade9-transfer-coverage-auditor`;
7. render every page, repair clipping/overlap/glyph issues, and re-render before declaring PASS.

## Mathematics concept-book routing

When the user asks for a Grade 9 Mathematics **Concept Book**, chalkboard-style explanation, formula-understanding book, or asks to make mathematics structurally understandable rather than formula-first:

1. route through `grade9-math` Concept Book mode;
2. preserve source/anchor coverage authority;
3. use `SEE -> REALIZE -> UNDERSTAND -> ADOPT` as the cognitive sequence;
4. treat `CONNECT` as traceability/navigation rather than a learning stage;
5. require pattern/invariant/representation/reconstruction/transfer before publication;
6. keep Concept Book, First-Step Reference, and Question Bank as distinct companion products.

For Sequence & Series, the Mathematics specialist includes the worked exemplar and summation/hidden-series bridge rules.

## Physics concept-book routing

When the user asks for a Grade 9 Physics Concept Book, route through `grade9-physics` and use `SEE THE EQUATION -> REALIZE -> UNDERSTAND`, retaining CONNECT as source traceability/navigation.

## Non-negotiable rules

1. Treat user-supplied sources as the primary authority when the request is source-grounded.
2. Never silently repair or replace defective source content. Record QC status and preserve provenance.
3. Treat difficulty as a cognitive profile, not an Easy/Medium/Hard label.
4. Preserve the uploaded anchor difficulty distribution unless the user asks for a different level.
5. Default Core bank size is 30 only when the user does not specify a count.
6. Default next-level appendix is 20 only when the user does not specify a count.
7. Every scored question must have one `primary_concept_id` and may have secondary concepts.
8. Generate textbook/question-bank artifacts from canonical structured master data, not from previously laid-out PDF pages, unless `grade9-publication` is explicitly reconstructing the supplied PDF as a source obligation set.
9. Keep source-derived, externally verified, and newly authored content distinguishable.
10. Do not declare a rendered product complete until page rendering, link validation, and content QA pass.
11. When an external/PYQ corpus is part of the brief, do not declare a subtopic or chapter complete until the transfer-coverage audit proves all eligible questions are uniquely placed or explicitly deferred to named future subtopics; final chapter acceptance requires zero missing and zero deferred eligible questions.
12. Do not declare a subtopic complete merely because all source facts appear. The subtopic-completeness audit must also pass explanation order, context/bridge, helper, misconception, scaffold, typography, and layout checks.
13. For chemistry PDFs, formula subscripts/superscripts, ionic charges, oxidation-number notation, and equation glyphs must be visually unambiguous at 100% zoom.
14. For source-PDF reconstruction, zero-loss means zero unmapped core source units, zero unapproved editorial changes, zero broken source relationships/links, and zero core items hidden or clipped in the rendered artifact; identical page count or coordinates are not required.

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
- `QG13 PUBLICATION_RECONSTRUCTION_INTEGRITY`

Read `references/grade9-workflow.md` when a full multi-stage build is requested. Use `references/grade9-master.schema.json` as the unchanged canonical structured-data contract when producing reusable master data.
