---
name: grade9-source-grounding
description: Extract, verify, classify, and preserve Grade 9 source material from uploaded PDFs, scans, handwritten notes, worksheets, screenshots, pasted notes, official papers, and web references. Use before source-grounded textbook or question-bank work when notation, provenance, omissions, or source defects matter.
---

# Grade 9 Source Grounding

Establish a reliable source layer before enrichment or new-question generation.

## Source statuses

- `VERIFIED_TRANSCRIPTION` — faithful and clear.
- `RECONSTRUCTED` — ambiguity required an explicit reconstruction.
- `QC_ALERT` — source is internally inconsistent, defective, incomplete, or likely misprinted.
- `SOURCE_UNRESOLVED` — do not use as a scored item until resolved.

## Provenance classes

`USER_UPLOADED_ANCHOR`, `OFFICIAL_PYQ`, `SECONDARY_VERIFIED_PYQ`, `PUBLISHED_REFERENCE`, `ORIGINAL_CALIBRATED`, `RECONSTRUCTED_FROM_SCAN`.

## Workflow

1. Inspect visual/rendered source content when equations, diagrams, or handwriting matter.
2. Preserve terminology, organization, notation, examples, and intended level.
3. Record page/question/source identifiers.
4. Check signs, exponents, subscripts, inequalities, brackets, units, bases, summation limits, diagrams, labels, and answer attainability.
5. Recalculate source examples before reusing them as instructional or scored material.
6. Do not silently fill a missing source point with model knowledge.
7. When outside verification or expansion is requested/necessary, clearly separate source-derived content from outside research or inference.
8. Emit structured source records for concept and question work.

Never silently replace source text with a correction. Store source statement/status and verified correction separately.

When research is part of the task, prefer official curriculum/exam/mark-scheme sources, government/academic sources, recognized references, then secondary sources for discovery. Do not bulk-copy commercial banks.

Output source inventory, anchor records, QC/transcription status, provenance, verified answer where applicable, unresolved issues, and concept clues.
