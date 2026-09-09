---
name: grade9-chemistry-publication-review
description: Package a completed Grade 9 Chemistry chapter for draft-PR review with learner-first artifacts, source/corpus maps, quantitative validation, reproducibility limits, manifest hashes and subject-specific review tracks. Use after chapter closeout; it does not replace source grounding, subtopic auditing, transfer coverage or chapter closeout.
---

# Grade 9 Chemistry Publication Review

Use this skill only after the chapter has passed its content/source/corpus closeout.

## Purpose

Turn a completed Chemistry chapter into a reviewable repository package without inflating technical PASS counters into pedagogy or classroom-effectiveness claims.

## Required order

```text
FREEZE REVIEWED LEARNER ARTIFACTS
-> COPY SOURCE / FROZEN CORPUS EVIDENCE
-> BUILD PAGE-INDEXED REVIEW GUIDE
-> BUILD CONCEPT / SOURCE / EXTERNAL-CORPUS MAPS
-> RECORD REPRODUCIBILITY BOUNDARY
-> GENERATE FILE MANIFEST + PACKAGE VALIDATION
-> RUN PACKAGE VALIDATOR
-> CREATE REVIEW BRANCH
-> OPEN DRAFT PR
```

## Chemistry-specific review gates

Reviewers must be able to inspect:

- formula subscripts/superscripts and ionic charges at 100% zoom;
- electron notation such as `e⁻`;
- conservation / oxidation-number bookkeeping;
- exceptions such as peroxide, superoxide and O-F oxygen when relevant;
- process vs agent inversion;
- equation-based role claims rather than memorised reagent reputation;
- reaction-type topology only after Redox status is established;
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
learner-facing PDFs
source/corpus audit evidence
```

## Release-claim discipline

Technical checks may justify claims such as:

- file exists and parses;
- page count matches the reviewed artifact;
- ledger totals reconcile;
- hashes match the manifest;
- canonical placement counters close.

They do **not** justify claims such as:

- the chapter is pedagogically effective;
- independent teachers approve it;
- classroom outcomes are improved;
- the material certifies a whole board/syllabus;
- byte-identical reproduction is available when generator source is absent.

Mark those `PENDING` or `NOT_RUN` explicitly.

## Draft PR structure

Follow learner-first review order:

1. start with the learner artifacts;
2. list included skills/evidence;
3. state validation actually run;
4. expose `PENDING` / `NOT_RUN` items;
5. provide independent review tracks;
6. keep the PR draft until reviewers/owner accept it.

Do not merge or mark ready for review unless explicitly authorized.
