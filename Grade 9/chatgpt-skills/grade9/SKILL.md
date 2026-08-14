---
name: grade9
description: Orchestrate Grade 9 learning-material work across source grounding, subject reasoning, concept architecture, difficulty-matched question banks, learning enrichment, diagnostics, and textbook/question-bank publication. Use for multi-stage Grade 9 Mathematics, Physics, or Chemistry tasks, including source-based chapter creation, Part 2 gap supplements, HOTS/competitive-foundation practice, mixed mastery, challenge appendices, and linked learning products.
---

# Grade 9 Learning System

Use this as the umbrella workflow for Grade 9 educational-content work.

## Current methodology policy

Use the current Grade 9 schema as the operational baseline. Do not redesign or migrate the schema unless the user explicitly asks. Treat numeric difficulty windows and the page-occupancy target as local engineering heuristics, not scientific laws. Prefer production-driven improvement: use the system on real chapters, log concrete gaps, and research only genuine blockers.

## Multi-skill workflow

When the relevant specialist skills are installed, combine them as needed:

1. `grade9-source-grounding` for uploaded/source material.
2. The relevant subject skill: `grade9-math`, `grade9-physics`, or `grade9-chemistry`.
3. `grade9-concept-architect` for stable concept IDs and prerequisite/link architecture.
4. `grade9-question-bank` for Core N, same-level practice, challenges, and mixed mastery.
5. `grade9-learning-enrichment` for helpers, hints, misconceptions, diagnostics, solutions, transfer, and mastery evidence.
6. `grade9-textbook-publisher` only when a rendered textbook/question-bank/workbook/teacher/integrated product is requested.

ChatGPT may use more than one installed skill for a full build. For narrow work, use only specialists that materially apply.

## Non-negotiable rules

1. User-supplied sources are the primary authority for source-grounded work.
2. Never silently repair, reconcile, or replace defective source content. Preserve source statement and QC status; store verified correction separately.
3. Do not silently fill source gaps with general knowledge unless the user asks to expand/research; distinguish any outside material.
4. Treat difficulty as a cognitive profile, not only Easy/Medium/Hard.
5. Preserve anchor difficulty distribution unless the user asks for a different level.
6. Core bank default is 30 only when the user gives no count.
7. Challenge default is 20 only when the user gives no count.
8. Every scored question has exactly one `primary_concept_id`; secondary concepts are optional.
9. Canonical structured master data is authoritative; PDF/page numbers are publication outputs.
10. Keep source-derived, externally verified, and newly authored content distinguishable.
11. Do not declare a rendered product complete until applicable content, render, and navigation QA pass.

## Canonical workflow

```text
SOURCE / USER REQUEST
  -> source fidelity + QC + provenance
  -> subject-specific reasoning fingerprint
  -> stable concepts + prerequisites
  -> difficulty-calibrated Core N
  -> next-level/challenge items
  -> helpers / hints / misconceptions / diagnostics
  -> mixed mastery / transfer
  -> canonical master data
  -> textbook / question bank / integrated edition
  -> QA
```

## Completion gates

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

For a full build, use `references/grade9-workflow.md`. For reusable structured master data, use the unchanged `references/grade9-master.schema.json`.
