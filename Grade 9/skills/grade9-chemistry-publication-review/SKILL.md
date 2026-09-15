---
name: grade9-chemistry-publication-review
description: Apply the subject-wide Grade 9 Chemistry publication/review schema to completed Chemistry topics or chapters. Verify the mandatory two-file topic contract, Core Appendix A/B/C including Appendix C Printable Handout, ExamSIDE concept/badge/hint/solution support, source/corpus reconciliation, exact learner-artifact custody, chemistry render QA, fail-closed validation, and learner-first draft-PR review.
---

# Grade 9 Chemistry Publication Review

Use this skill after a Chemistry topic/chapter has passed its upstream source/content/question audits and needs a **reviewable, reproducible publication package**.

This is Chemistry-wide. Redox is the first conforming instance, not the publication schema itself.

Read:

- `Grade 9/Chemistry/CHEMISTRY_PUBLICATION_SCHEMA.md`
- `Grade 9/Chemistry/schema/chemistry-topic-delivery.schema.json`
- `Grade 9/Chemistry/schema/chemistry-publication-package.schema.json`

## Required order

```text
VERIFY PER-TOPIC TWO-FILE DELIVERY
-> VERIFY CORE APPENDIX A / B / C
-> VERIFY APPENDIX C PRINTABLE HANDOUT
-> VERIFY EXAMSIDE LABELS / BADGES / HINTS / COMPLETE SOLUTIONS
-> FREEZE REVIEWED LEARNER ARTIFACTS
-> COPY SOURCE / FROZEN CORPUS EVIDENCE
-> BUILD PAGE-INDEXED REVIEW GUIDE
-> BUILD CONCEPT / SOURCE / EXTERNAL-CORPUS MAPS
-> RECORD REPRODUCIBILITY BOUNDARY
-> GENERATE FILE MANIFEST + PACKAGE VALIDATION
-> RUN FAIL-CLOSED PACKAGE VALIDATOR
-> CREATE / UPDATE REVIEW BRANCH
-> OPEN / UPDATE DRAFT PR
```

## Topic deliverable gate — blocking

For every topic represented in the publication package, require exactly two learner-facing topic PDFs:

```text
1. Core Study Guide
2. ExamSIDE Solution & Transfer Book
```

The Core Study Guide must contain:

```text
Appendix A = Core Practice
Appendix B = Core Solutions
Appendix C = Printable Handout
```

Appendix C must be a recognisable detachable/printable learner handout, not merely a heading. It should be standalone-usable, concise, source-bounded and free of independent-practice answer leakage.

Fail publication if any topic is missing one of the two files or any of the three Core appendices.

## ExamSIDE support gate — blocking

Every required/placed external question must expose, in the learner artifact and/or machine-readable publication model:

- canonical question ID;
- source/year/shift badge and source link;
- primary concept ID/label;
- visible concept segregation label separating `PRIMARY` from prerequisite/supporting concepts;
- difficulty badge;
- transfer badge;
- H0 attempt-first state;
- difficulty-appropriate progressive H1/H2/H3 hints;
- Core Study Guide cross-link;
- concept helper / misconception watch when relevant;
- complete solution in the same ExamSIDE PDF;
- placement/source-link/solution status in the corpus ledger.

Do not accept a plain question dump plus answer key as the ExamSIDE product.

## Chemistry-specific review gates

Reviewers must be able to inspect:

- formula subscripts/superscripts and ionic charges at 100% zoom;
- electron notation where relevant;
- conservation / symbolic bookkeeping;
- macro/particle/symbolic representation quality;
- topic-specific exceptions/conditions;
- misconception repair;
- Appendix C handout usability and print readability;
- answer separation between attempt pages and solution pages;
- scope boundaries when a PYQ needs chemistry outside the supplied source.

## Required review package

At minimum:

```text
README.md
REVIEW_GUIDE.md
CONCEPT_REVIEW_MAP.md
SOURCE_COVERAGE_MAP.md
EXAMSIDE_COVERAGE_MAP.md (when an external corpus is in scope)
CHEMISTRY_REBUILD_REVIEW.md
REPRODUCE.md
DELIVERY_RECORD.md
Packaging_Validation.json
FILE_MANIFEST.json
Chemistry_Publication_Package.json
topic-delivery records
learner-facing PDFs
source/corpus audit evidence
```

## Artifact custody modes

Prefer, in order:

1. direct committed learner PDF bytes;
2. exact learner PDF bytes stored as deterministic text-safe chunks plus manifest and unpacker;
3. canonical content model plus deterministic renderer.

A fingerprint with no recoverable artifact or deterministic renderer is blocking.

## Fail-closed rule

The technical gate returns:

- `0` only for technical PASS;
- `1` for validation mismatch/failure;
- `2` for blocking custody/manual states.

There is no exit-code-0 blocked state.

## Release-claim discipline

Technical checks may justify claims such as:

- required files/appendices exist and parse;
- page count/hash matches;
- source/corpus ledgers reconcile;
- canonical placement counters close;
- expected links resolve;
- chemistry notation/layout gates pass.

They do **not** justify claims such as independent teacher approval, classroom effectiveness, psychometric validity or whole-syllabus certification. Keep those `PENDING` / `NOT_RUN` until evidence exists.

## Draft PR rule

Keep the PR draft until the exact learner artifacts are accessible from repository/CI state and all technical gates—including two-file delivery, Appendix A/B/C and ExamSIDE support—are green. Marking ready or merging still requires explicit user/owner authorization.
