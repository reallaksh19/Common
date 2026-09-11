---
name: grade9
description: Route Grade 9 learning-material tasks to source grounding, subject reasoning, concept architecture, question-bank/enrichment, subject-specific topic builders, completeness/transfer audits, publication reconstruction, publication review and final publishing workflows for Mathematics, Physics and Chemistry.
---

# Grade 9 Router Skill

Use this skill as the entry point for Grade 9 educational-content work.

## Canonical workflow

```text
SOURCE / USER REQUEST
  -> grade9-source-grounding
  -> relevant subject skill
  -> subject-specific topic builder when applicable
  -> grade9-concept-architect
  -> grade9-question-bank
  -> grade9-learning-enrichment
  -> grade9-subtopic-completeness-auditor
  -> grade9-transfer-coverage-auditor when external/PYQ transfer is in scope
  -> publication / review gate
  -> final QA
```

## Route by task

- Source PDF/images/notes/PYQs -> `../grade9-source-grounding/SKILL.md` first.
- Mathematics -> `../grade9-math/SKILL.md`.
- Physics -> `../grade9-physics/SKILL.md`.
- Chemistry subject reasoning -> `../grade9-chemistry/SKILL.md`.
- **Any Chemistry topic learner build** -> `../grade9-chemistry-topic-builder/SKILL.md`.
- **Chemistry publication/review package** -> `../grade9-chemistry-publication-review/SKILL.md`.
- Redox-specific reasoning -> `../grade9-redox-subtopic-book-builder/SKILL.md` under the generic Chemistry topic-builder contract.
- Concept IDs/dependencies -> `../grade9-concept-architect/SKILL.md`.
- Question banks -> `../grade9-question-bank/SKILL.md`.
- Helpers/hints/misconceptions/diagnostics -> `../grade9-learning-enrichment/SKILL.md`.
- Source-PDF reconstruction -> `../grade9-publication/SKILL.md`.
- Whole-subtopic completeness -> `../grade9-subtopic-completeness-auditor/SKILL.md`.
- External/PYQ accounting -> `../grade9-transfer-coverage-auditor/SKILL.md`.
- Canonical master-data PDF publication -> `../grade9-textbook-publisher/SKILL.md`.

## Chemistry topic-production routing — mandatory

When a Chemistry topic is taken up, the generic Chemistry contract requires exactly two learner-facing PDFs:

```text
1. CORE STUDY GUIDE
   Appendix A = Core Practice
   Appendix B = Core Solutions
   Appendix C = Printable Handout

2. EXAMSIDE SOLUTION & TRANSFER
   source/difficulty/transfer/concept badges
   PRIMARY vs SUPPORT concept segregation label
   H0 attempt-first + optional H1/H2/H3
   Core/source links
   complete solution
```

Appendix C is mandatory and lives inside the Core Study Guide; do not create a third handout PDF.

For Redox, use both `$grade9-chemistry-topic-builder` and `$grade9-redox-subtopic-book-builder`. The Redox skill may specialize chemistry reasoning but cannot change the two-file/Appendix A-B-C contract.

## Publication reconstruction routing

When the user supplies an existing educational PDF/book and asks to rebuild/revamp it while preserving core content:

1. run `grade9-source-grounding`;
2. use the relevant subject skill;
3. invoke `grade9-publication` before large-scale layout work;
4. freeze source obligations with stable IDs;
5. separate source content from value-add/editorial change;
6. run anti-drift and render-first QA;
7. require zero unmapped core units, unapproved changes, broken links, or clipped core content before claiming completeness.

## Non-negotiable rules

1. User-supplied sources are the primary authority for source-grounded work.
2. Never silently repair/replace defective source content; record QC/provenance.
3. Treat difficulty as a cognitive profile, not only a label.
4. Every scored question has exactly one `primary_concept_id`; secondary concepts may be recorded separately.
5. Keep source-derived, externally verified and newly authored content distinguishable.
6. Do not declare a rendered product complete until page rendering, link validation and content QA pass.
7. When an external/PYQ corpus is in scope, every eligible question needs exactly one canonical primary home; final chapter acceptance requires zero missing/deferred eligible questions.
8. A subtopic/topic cannot pass merely because facts are present: explanation order, helper, misconception repair, practice, typography and layout must pass.
9. For Chemistry, every topic build must satisfy the two-file contract and Core Appendix A/B/C, with Appendix C as a printable standalone handout.
10. For Chemistry ExamSIDE products, required questions must carry visible concept segregation, source/difficulty/transfer badges, progressive hints as required, Core/source links and complete solutions.
11. Chemistry notation must be visually unambiguous at 100% zoom.
12. Technical publication PASS does not imply independent pedagogy/classroom validation.

## Completion gates

Apply relevant gates:

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
- `QG14 CHEMISTRY_TOPIC_TWO_FILE_DELIVERY`
- `QG15 CHEMISTRY_APPENDIX_A_B_C`
- `QG16 CHEMISTRY_EXAMSIDE_SUPPORT`

Read `references/grade9-workflow.md` for full multi-stage builds.
