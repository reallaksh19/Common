---
name: grade9-redox-chapter-closeout-auditor
description: Audit the completed Redox chapter against the full frozen ExamSIDE corpus and supplied source PDF, backfill missed eligible PYQs, preserve one canonical primary home per question, and block chapter closeout until source, corpus, typography, layout, and duplicate-placement checks pass.
---

# Grade 9 Redox Chapter Closeout Auditor

This is the Chemistry/Redox subject profile of `../grade9-chapter-closeout-auditor/SKILL.md`.
That skill owns the subject-agnostic workflow, statuses, counters and invariant. This file adds only
the Redox outside-dependency list and chemistry typography/glyph checks. For a non-Redox chapter,
use the generic skill with a new subject profile rather than copying this file.

Use this skill only after the individual Redox subtopics have been drafted. Read and execute the
generic closeout skill in full; the sections below are the only Redox-specific additions.

## Redox eligibility delta

When applying the generic candidate-status rules, treat these as explicit outside dependencies
where they are absent from the supplied source:

- titration / normality / equivalent weight;
- full redox balancing or half-reaction balancing;
- solution-concentration stoichiometry beyond simple electron accounting;
- medium-specific reagent products;
- salt / qualitative analysis;
- coordination chemistry;
- acid-base indicator theory;
- reaction-specific inorganic product knowledge;
- oxidation-strength or stability trends not taught by the source.

## Redox render-QA delta

Add `CHAPTER_TYPOGRAPHY_FAILURES = 0` to the generic acceptance counters. Inspect subscripts,
superscripts, ionic charges, oxidation numbers and `e⁻` glyphs on every dense or repaired page.
All generic source, placement, batch, artifact and final-invariant requirements remain owned by
`grade9-chapter-closeout-auditor` and are not repeated here.
