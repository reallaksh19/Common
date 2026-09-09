---
name: grade9-chapter-closeout-auditor
description: Audit a completed Grade 9 chapter against its full frozen external corpus (ExamSIDE, PYQ index, or equivalent) and its supplied source, backfill missed eligible items, preserve one canonical primary home per item, and block chapter closeout until source, corpus, typography, layout and duplicate-placement checks pass. Subject-agnostic sibling of grade9-transfer-coverage-auditor (subtopic scope) - use this one at final chapter/whole-topic acceptance, across Physics, Chemistry, Mathematics or any other Grade 9 subject.
---

# Grade 9 Chapter Closeout Auditor

Use this skill only after the individual subtopics of a chapter have been drafted via the subject's own subtopic-book-builder and audited subtopic-by-subtopic with `grade9-transfer-coverage-auditor`.

This skill extracts the subject-agnostic 90% of the closeout pattern first proven for Redox
(`grade9-redox-chapter-closeout-auditor`). Subject-specific concerns - outside-dependency
lists, notation/typography checks, glyph rendering - belong in a thin subject profile that
uses this skill's contract, not in a second copy of it. See "Subject profiles" below.

## 1. Full corpus before chapter acceptance

Do not infer the chapter denominator by adding the item counts from incremental subtopic builds.

Before final acceptance:

```text
FETCH / FREEZE FULL EXTERNAL-CORPUS INDEX
-> ENUMERATE EVERY CANDIDATE
-> ASSIGN SCOPE STATUS TO EVERY CANDIDATE
-> ASSIGN EXACTLY ONE PRIMARY SUBTOPIC TO EVERY ELIGIBLE ITEM
-> COMPARE AGAINST ACTUAL TRANSFER BOOKS
-> BACKFILL MISSING ELIGIBLE ITEMS
-> RE-AUDIT
```

A repeated or duplicate reasoning pattern still requires a deliberate placement. `DUPLICATE_REASONING` means "no new teaching architecture", not "may be omitted from transfer coverage".

## 2. Required candidate statuses

Every frozen corpus candidate receives exactly one:

```text
ELIGIBLE_IN_SCOPE
PARTIAL_SCOPE
OUT_OF_SCOPE
SOURCE_UNRESOLVED
```

Eligibility is based on the minimum solution path, not the source's own topic label. A subject profile records its own explicit outside-dependency list (see "Subject profiles") to make this judgment concrete and reviewable rather than left to per-item discretion.

## 3. Canonical primary placement

For every `ELIGIBLE_IN_SCOPE` item record:

```text
candidate_id
source/date
question_family
primary_subtopic_id
primary_concept_id
transfer_book_id
hint_depth
appendix_solution_status
source_link_status
placement_status
```

Each eligible item has exactly one primary home. Cumulative/revision books may reuse items, but must not change or duplicate primary ownership.

## 4. Backfill gate

Run the reverse comparison:

```text
FULL_ELIGIBLE_LEDGER - ACTUAL_PRIMARY_PLACEMENTS
```

Any non-empty result is a blocking `MISSING` set.

Backfill missing items into the correct subtopic even when:

- the reasoning family is already taught;
- the item adds no new concept;
- the item is nearly a duplicate of an existing corpus item.

Do not inflate the Study Guide/Concept Book just to accommodate duplicate reasoning. Add practice placement, hints, source link and Appendix A solution instead.

## 5. Source closeout

Freeze source obligations from the supplied source material and report:

```text
SOURCE_OBLIGATIONS_REQUIRED = n
SOURCE_OBLIGATIONS_TAUGHT = n
SOURCE_OBLIGATIONS_MISSING = 0
```

If a source-internal item requires a prerequisite that the source itself does not teach, record a `SOURCE_PREREQUISITE_EXCEPTION` rather than silently introducing a new unit.

## 6. Chapter acceptance counters

Required final counters:

```text
CHAPTER_CANDIDATES_TOTAL = n
CHAPTER_ELIGIBLE_TOTAL = n
CHAPTER_PARTIAL_TOTAL = n
CHAPTER_OUT_OF_SCOPE_TOTAL = n
CHAPTER_PLACED_UNIQUE = CHAPTER_ELIGIBLE_TOTAL
CHAPTER_MISSING = 0
CHAPTER_DUPLICATE_PRIMARY_PLACEMENTS = 0
CHAPTER_UNTAUGHT_DEPENDENCY = 0
CHAPTER_BROKEN_SOURCE_LINKS = 0
CHAPTER_HINT_FAILURES = 0
CHAPTER_SOLUTION_FAILURES = 0
CHAPTER_LAYOUT_FAILURES = 0
CHAPTER_STATUS = PASS
```

A subject profile may add its own typography/notation counter (e.g. `CHAPTER_TYPOGRAPHY_FAILURES` for chemistry glyphs, or an equation-legibility counter for Physics/Math) alongside these, not instead of them.

## 7. Required artifacts

Produce, when requested:

1. a human-readable full-corpus audit PDF;
2. a machine-readable candidate ledger (JSON/CSV);
3. corrected subtopic transfer books for any backfill;
4. merged master Study Guide / Concept Book;
5. merged master transfer book with the corpus audit appended or linked.

## 8. Render-first final QA

Render every final PDF. Inspect at minimum:

- master cover;
- chapter map;
- source-obligation ledger;
- backfill pages;
- dense candidate-ledger pages;
- final placement summary;
- final subtopic audit page.

The rendered pages are authoritative. Repair clipping, hidden rows, title collisions, footer overlap, or missing/incorrect subject-specific glyphs before declaring PASS.

## 9. Final invariant

> A chapter is not complete because each subtopic individually passed. It is complete only after a full frozen-corpus audit proves that every eligible item is uniquely placed and every source obligation is taught without scope leakage.

## Subject profiles

A subject profile is a short document that:

1. names its explicit outside-dependency list for eligibility judgments (§2) - e.g. Redox's titration/normality/full-balancing/coordination-chemistry list, or a Physics profile's list of out-of-scope mechanics (e.g. rotational dynamics, relativistic effects) for a given chapter's stated scope;
2. names its subject-specific render-QA checks to add to §8 (chemistry subscript/superscript/ionic-charge/`e⁻` legibility; Physics vector-arrow, unit and sign-convention legibility; math equation/proof-step legibility);
3. points at its own `grade9-transfer-coverage-auditor`-driven subtopic builds as the input this skill closes out.

`grade9-redox-chapter-closeout-auditor` is the first such profile (Chemistry/Redox). Do not duplicate this skill's counters, statuses or workflow inside a new subject profile - reference this skill and add only what is genuinely subject-specific.
