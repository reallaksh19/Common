---
name: grade9-redox-chapter-closeout-auditor
description: Audit the completed Redox chapter against the full frozen ExamSIDE corpus and supplied source PDF, backfill missed eligible PYQs, preserve one canonical primary home per question, and block chapter closeout until source, corpus, typography, layout, and duplicate-placement checks pass.
---

# Grade 9 Redox Chapter Closeout Auditor

Use this skill only after the individual Redox subtopics have been drafted.

## 1. Full corpus before chapter acceptance

Do not infer the chapter denominator by adding the question counts from incremental subtopic builds.

Before final acceptance:

```text
FETCH / FREEZE FULL EXAMSIDE INDEX
-> ENUMERATE EVERY CANDIDATE
-> ASSIGN SCOPE STATUS TO EVERY CANDIDATE
-> ASSIGN EXACTLY ONE PRIMARY SUBTOPIC TO EVERY ELIGIBLE ITEM
-> COMPARE AGAINST ACTUAL TRANSFER BOOKS
-> BACKFILL MISSING ELIGIBLE ITEMS
-> RE-AUDIT
```

A repeated or duplicate reasoning pattern still requires a deliberate placement. `DUPLICATE_REASONING` means "no new teaching architecture", not "may be omitted from transfer coverage".

## 2. Required candidate statuses

Every frozen ExamSIDE candidate receives exactly one:

```text
ELIGIBLE_IN_SCOPE
PARTIAL_SCOPE
OUT_OF_SCOPE
SOURCE_UNRESOLVED
```

Eligibility is based on the minimum solution path, not the website topic label.

Explicit outside dependencies include, where absent from the supplied source:

- titration / normality / equivalent weight;
- full redox balancing or half-reaction balancing;
- solution-concentration stoichiometry beyond simple electron accounting;
- medium-specific reagent products;
- salt / qualitative analysis;
- coordination chemistry;
- acid-base indicator theory;
- reaction-specific inorganic product knowledge;
- oxidation-strength or stability trends not taught by the source.

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

Each eligible item has exactly one primary home. Cumulative/revision books may reuse questions, but must not change or duplicate primary ownership.

## 4. Backfill gate

Run the reverse comparison:

```text
FULL_ELIGIBLE_LEDGER - ACTUAL_PRIMARY_PLACEMENTS
```

Any non-empty result is a blocking `MISSING` set.

Backfill missing items into the correct subtopic even when:

- the reasoning family is already taught;
- the item adds no new concept;
- the question is nearly a duplicate of an existing PYQ.

Do not inflate the Study Guide just to accommodate duplicate reasoning. Add practice placement, hints, source link, and Appendix A solution instead.

## 5. Source closeout

Freeze source obligations from the supplied PDF and report:

```text
SOURCE_OBLIGATIONS_REQUIRED = n
SOURCE_OBLIGATIONS_TAUGHT = n
SOURCE_OBLIGATIONS_MISSING = 0
```

If a source-internal question requires a prerequisite that the source theory itself does not teach, record a `SOURCE_PREREQUISITE_EXCEPTION` rather than silently introducing a new unit.

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
CHAPTER_TYPOGRAPHY_FAILURES = 0
CHAPTER_LAYOUT_FAILURES = 0
CHAPTER_STATUS = PASS
```

## 7. Required artifacts

Produce, when requested:

1. a human-readable full-corpus audit PDF;
2. a machine-readable candidate ledger (JSON/CSV);
3. corrected subtopic transfer books for any backfill;
4. merged Master Study Guide;
5. merged Master ExamSIDE Transfer Book with the corpus audit appended or linked.

## 8. Render-first final QA

Render every final PDF. Inspect at minimum:

- master cover;
- chapter map;
- source-obligation ledger;
- backfill pages;
- dense candidate-ledger pages;
- final placement summary;
- final subtopic audit page.

The rendered pages are authoritative. Repair clipping, hidden rows, title collisions, footer overlap, or missing chemistry glyphs before declaring PASS.

## 9. Final invariant

> A Redox chapter is not complete because each subtopic individually passed. It is complete only after a full frozen-corpus audit proves that every eligible question is uniquely placed and every source obligation is taught without scope leakage.
