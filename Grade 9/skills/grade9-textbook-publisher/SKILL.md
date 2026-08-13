---
name: grade9-textbook-publisher
description: Turn validated Grade 9 master data into kid-friendly textbook, question-bank, workbook, teacher, or integrated linked PDF products. Use when the user requests textbook-quality layout, reduced accidental whitespace, concept-to-practice navigation, internal PDF links, mixed mastery sections, answer/hint appendices, or publication QA.
---

# Grade 9 Textbook Publisher

Treat the PDF as a rendered product generated from canonical master data, not as the source of truth.

## Required upstream state

Before layout, require:

- validated source/QC records;
- stable concept IDs;
- validated question IDs and answers;
- primary concept mapping;
- enrichment objects where requested;
- provenance metadata.

Do not change pedagogy or answers merely to make content fit a page.

## Student-facing design language

Prefer a compact young-technical-magazine style rather than report pages or childish decoration.

Useful recurring modules:

- `MISSION`
- `SPOT THE PATTERN`
- `FIRST MOVE`
- `TOOLBOX`
- `COMMON TRAP`
- `WORK IT OUT`
- `TRY NOW`
- `LEVEL UP`
- `EXIT TICKET`
- `WORK ZONE`

Use a consistent small visual vocabulary and subject-aware diagrams.

## Page-density rule

Target roughly 70-85% meaningful occupancy on typical learning pages. Meaningful occupancy includes deliberate working space, annotation areas, reflection prompts, diagrams, or practice previews.

Avoid accidental half-page voids, oversized headers, isolated hint boxes on nearly empty pages, and unnecessary forced page breaks. Also avoid cramming pages above useful readability.

## Linked architecture

The preferred integrated product implements:

```text
Concept
  <-> Core practice
  <-> Level-Up challenge
  <-> Helper / hint
  <-> Solution / answer
  <-> Misconception diagnosis
  <-> Mixed-test diagnosis
```

Use stable IDs as internal destinations. Page numbers are derived after layout.

## Learning mode vs testing mode

- Concept-grouped practice may show concept labels and study links.
- Mixed mastery tests must hide concept labels before the attempt.
- After marking, route errors back to exact concept IDs.

## Typical products

- Student textbook: concept-focused, worked anchors, practice paths.
- Question bank: Core N + Level-Up + mixed mastery + hint/answer support.
- Integrated edition: textbook and bank combined with bidirectional internal links.
- Teacher edition: may expose source/QC, difficulty, misconceptions, solution paths, and diagnostics more explicitly.

## PDF QA

For each final PDF:

1. save the final artifact;
2. render every page to images;
3. inspect equations, clipping, page rhythm, density, headers/footers, and diagram labels;
4. validate internal links and return links;
5. preflight page count/dimensions and structural readability;
6. verify IDs/answer keys match master data.

Run `scripts/check_master_links.py` before rendering when master JSON is available.

## Provenance display

Keep student pages uncluttered with concise badges such as `UPLOADED ANCHOR`, `OFFICIAL PYQ`, `CALIBRATED ORIGINAL`, or `QC NOTE`. Put full provenance in an appendix or teacher/master data.
