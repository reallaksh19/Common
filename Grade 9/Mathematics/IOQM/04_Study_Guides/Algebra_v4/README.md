# IOQM Grade 9 Algebra — Study Guide v4

## Purpose

This directory is the durable repository home for the Algebra study-guide package produced from the verified 50-question ALLEN Algebra worksheet/research set plus the Grade 9 IOQM Algebra reference-book rebuild.

The student architecture is:

`Navigator = where to go. Core = how to do it.`

The current student-facing short-horizon layer is intentionally simple: a 4-page three-day Navigator using `T1 ... Tx` diagnostic labels, while the actual Algebra practice corpus remains `Q1 ... Q50`.

## Current generated artifacts

Working-session artifacts:

- `Algebra_IOQM_Grade9_Reference_Book_Simple_3Day_v4.pdf`
  - 51 A4 pages
  - SHA-256 `e011b316240abf9d8abaeed9e2db806792abbebb85daeb2b2992651f2b8995fa`
- `Algebra_3Day_Simple_Navigator_4pp.pdf`
  - 4 A4 pages
  - SHA-256 `beebab77b4da26876ea71a65544836580b3bb1260082aa662d5d194681cb8d51`

The binary PDFs were generated and 200-dpi inspected in the authoring environment. The GitHub connector used for this repository write does not expose a direct binary-file upload parameter, so this commit records the complete repository-side source/data package and exact artifact hashes; the PDFs remain the canonical generated artifacts until a binary upload path is used.

## Repository data locations

- Study-guide metadata and learner-routing data: this directory and `data/`.
- Verified lecture-linked worksheet extraction: `../../../Research/Video_Extraction/ALLEN_Algebra_Marathon_2026/`.
- Reusable authoring rules: `../../../../skills/ioqm-grade9-study-guide-builder/`.

## Corpus boundary

- Algebra worksheet corpus: exactly `Q1 ... Q50`.
- No Algebra worksheet `Q51 ... Q70` exists in the recovered sheet.
- Quick Check labels use `T1 ... Tx`; `T` labels are never source/corpus question numbers.

## Known source/custody exceptions

- Q8: stated target is `|x-y|`; worksheet key gives 2197, while the correct target value is `sqrt(2197)`.
- Q27: ordered triples require all six permutations of `(1,1,8)` and `(4,4,1/2)`.
- Q29: recovered literal wording gives `-19/40` while printed key gives `1/8`; wording remains unresolved and should not be forced to match the key.
- Q36: absolute-value notation restored from the identified source.
- Q43: absolute-value notation restored from the identified source.
- Q49: duplicate of Q37.
- Q50: recurrence restored from the identified 2004 AIME II source.

## Status

The durable v4 reference book predates the newest learner-facing difficulty/source-badge presentation contract added to the reusable builder. Preserve this v4 archive as a known-good study-guide artifact; regenerate a later edition rather than silently relabelling the archived PDF.
