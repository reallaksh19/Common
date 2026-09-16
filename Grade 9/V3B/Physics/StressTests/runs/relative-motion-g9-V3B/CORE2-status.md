# Core2 — status (Motion in two dimensions: vector representation and subtraction; relative velocity in a plane)

Status: **HELD**.

Core2 is defined as "existing source questions and ladder hints, source identity and answers; preserve supplied frozen wording and figures" (V3B-Pending-Activity-Handover.md). This run supplied `sources.frozen_core2: []` deliberately (V3B-Motion-Grade9-Example.md: "The empty local/frozen lists are deliberate, not fictional file paths"). No frozen, owner-supplied or officially sourced Core2 question bank exists in the repository for this topic. This matches the microtopic library's own finding: `ISS-NO-CORPUS` in `V3B-Relative-Motion-Library-Seed.json` — "Only one authored candidate question; no official or frozen local bank acquired."

## What exists instead

`corpus_mode: BUILD_REVIEW_CORPUS` was in effect. An **author-created review corpus** of 8 candidate questions was authored for this run (`inputs/sources/source.json`, source id `AUTHOR`, `origin: AUTHOR_CREATED`) and used to build Core2A/Core2B practice, per the template's explicit permission ("Authored questions may supplement allowed practice, with local IDs and truthful AUTHORED provenance; never invent an official exam/year/question number").

This review corpus is **not** a substitute for Core2 and is not represented as one anywhere in this run's outputs — every question object in `publication/CORE2A.html` and `publication/CORE2B.html` visibly carries `AUTHOR_CREATED` provenance and the exact citation string, not a CBSE/NCERT question number.

## Path to closing this hold

1. Acquire an authorized frozen or official Motion-in-2D/relative-velocity question corpus (owner-supplied local bank, or a reconciled official source with confirmed rights/edition), matching this run's exact subtopic scope.
2. Switch `sources.corpus_mode` to `FROZEN_SUPPLIED` and `sources.frozen_core2` to the acquired file paths in a future stress-test invocation.
3. Re-run the vertical slice; Core2 becomes a real product only once frozen source questions with confirmed identity/wording/figures exist to preserve.

No fabricated exam identifiers, editions or question numbers were introduced to close this hold artificially.
