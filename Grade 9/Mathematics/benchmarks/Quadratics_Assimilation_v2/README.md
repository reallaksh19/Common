# Quadratics Assimilation v2 — Benchmark Manifest

## Purpose

This folder holds the canonical **internal quality benchmark** for the Grade 9 Mathematics partial-knowledge assimilation workflow.

The benchmark is not a text/layout template. A successor agent should preserve or improve:

- learner assimilation;
- concept-map completeness;
- missing-link repair;
- contrast/decision boundaries;
- attempt-before-hint;
- H3 -> H0 fading;
- first-move independence;
- non-identical transfer;
- source custody;
- mathematical correctness;
- production/render quality.

Do not copy wording, exercise text, colors, typography, page composition, or layout.

## Committed repository benchmark

| File | Purpose | Pages | SHA-256 |
|---|---|---:|---|
| `Quadratics_Assimilation_Benchmark_v2.pdf` | portable 9-page benchmark edition capturing the complete pedagogy/decision architecture | 9 | `ac83ce14f195eba87743d8bf2d4e99942b301449a4a8769161e34ee15d2f1841` |

The committed PDF has been rendered page-by-page and preflighted:

- page count: 9;
- openable: PASS;
- encrypted: no;
- likely scanned: no;
- XFA: no;
- visible clipping/overlap/broken glyphs: none observed.

This PDF is the single repository comparator for agent takeover. It intentionally emphasizes the teaching architecture rather than serving as the complete student publication.

## Full production artifacts from the authoring run

The authoring run also generated the fuller student artifacts below. Their source Markdown is committed in the repository and remains the content authority. Their hashes are retained for reproducibility/audit even when a companion binary is not required for agent execution.

| Artifact | Purpose | Pages | SHA-256 |
|---|---|---:|---|
| `Quadratics_Concept_Map_v2.pdf` | teaching/learning map | 1 | `6497a97c591782ed54f4d0c73f9ca4a4090bd18a8946bfdb1740d52e4e53c473` |
| `Quadratics_Assimilation_Book_v2.pdf` | concept assimilation / missing-link repair | 9 | `6c2f1c16b0990b108ba364aab92203cded8e1dcb75df6b799ce2014b990a711d` |
| `Quadratics_First_Step_Reference_v2.pdf` | compressed recognition/revision layer | 4 | `f1536df9f242d6142d5ccdcbbef7600a4bbceb2a3c5ce077b4905cb6edf021da` |
| `Quadratics_Complete_Learning_Pack_v2.pdf` | concept map -> assimilation -> first-step combined order | 14 | `199b752193ea8a9fd718c147aa1587aed0ae37ff78699fb3289c2f99e066452a` |

## Canonical source files

- `../../NMTC Preliminary/03_Concept_Books/Algebra/Polynomial_Root_Structure/Quadratics_Assimilation_Concept_Map.md`
- `../../NMTC Preliminary/03_Concept_Books/Algebra/Polynomial_Root_Structure/Quadratics_Assimilation_Book_v2.md`
- `../../NMTC Preliminary/03_Concept_Books/Algebra/Polynomial_Root_Structure/Quadratics_First_Step_Reference_v2.md`
- `../../NMTC Preliminary/09_QA/Quadratics_Assimilation_v2_QA.md`

## Reproduction authority

A successor agent should start here:

1. `../../../skills/grade9-math-assimilation/SKILL.md`
2. `../../../skills/grade9-math-assimilation/references/quadratics-v2-retrace-runbook.md`
3. `../../../skills/grade9-math-assimilation/references/quadratics-subtopic-prompt-pack.md`
4. the relevant child issue below;
5. this benchmark PDF.

## GitHub issue program

- #36 — Foundations / representations / method selection
- #37 — Discriminant / repeated roots / parameter conditions
- #38 — Vieta / root invariants / symmetric targets
- #39 — Transformed & integer roots / structural reduction
- #40 — Mixed mastery / transfer / first-move independence
- #41 — coordination index
- #42 — benchmark publication/retrace task

Recommended implementation order:

`#36 -> #37 -> #38 -> #39 -> #40`

Do not combine child outputs into a monolithic publication before each child passes its own internal QA.

## Required benchmark comparison

A successor agent must record at least:

| Gate | Question |
|---|---|
| Concept map | Are prior knowledge, half-knowledge, missing bridge, invariant, representation, misconception, decision boundary, first move, transfer and source nodes explicit? |
| Assimilation | Can a partially prepared student understand why the method works? |
| Contrast | Does each major concept show a near-miss requiring a different method? |
| Attempt | Does the learner attempt before seeing full scaffolding? |
| Fading | Does help genuinely reduce from H3 to H0? |
| First move | Can the student start an unlabelled problem? |
| Transfer | Is the final problem structurally related but not a number swap? |
| Source | Are provenance and source conflicts preserved? |
| Math | Were answers independently recomputed? |
| PDF | Was every rendered page visually inspected and preflighted? |

## Current evidence state

- static benchmark QA: `PASS_INTERNAL`;
- repository benchmark binary: `COMMITTED_AND_RENDER_VERIFIED`;
- classroom timing/readability calibration: `NOT_RUN`;
- longitudinal student mastery evidence: `NOT_RUN`;
- publication approval: `NOT_READY`.

The benchmark may be used now as an **internal authoring/review comparator**. It does not constitute classroom validation or publication approval.
