---
name: grade9
description: Route Grade 9 learning-material tasks to the correct source-grounding, concept architecture, question-bank, enrichment, subject, and publishing workflows. Use for Grade 9 source analysis, textbook creation, concept maps, difficulty-matched question banks, HOTS/competitive-foundation practice, diagnostics, mixed mastery, challenge appendices, and linked student/teacher PDF production in Mathematics, Physics, or Chemistry.
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
  -> canonical master data
  -> grade9-textbook-publisher when a rendered artifact is requested
  -> QA
```

## Route by task

- Source PDF, images, notes, worksheet, PYQ, or pasted notes -> `../grade9-source-grounding/SKILL.md` first.
- Mathematics -> `../grade9-math/SKILL.md`.
- Physics -> `../grade9-physics/SKILL.md`.
- Chemistry -> `../grade9-chemistry/SKILL.md`.
- Concept IDs, prerequisites, dependency maps, textbook-to-bank links -> `../grade9-concept-architect/SKILL.md`.
- Similar questions, same-level practice, Core N, HOTS, challenge appendix, mixed tests -> `../grade9-question-bank/SKILL.md`.
- Helpers, progressive hints, misconceptions, diagnostics, transfer questions -> `../grade9-learning-enrichment/SKILL.md`.
- Student textbook, question bank, integrated edition, PDF layout, internal links, render/preflight -> `../grade9-textbook-publisher/SKILL.md`.

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

Read `references/grade9-workflow.md` when a full multi-stage build is requested. Use `references/grade9-master.schema.json` as the canonical structured-data contract when producing reusable master data.
