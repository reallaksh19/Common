# NMTC Preliminary Scope and Source Policy

## 1. Target examination

Target only the **NMTC Junior / Bhaskara Preliminary (Screening) Test for Grades IX–X**.

Do not use Stage II / Final questions to set:

- curriculum weight;
- question difficulty;
- expected solution length;
- archetype recurrence;
- timed-drill targets;
- mock-paper composition.

Stage II may only be referenced later as explicitly labeled optional extension material.

## 2. Syllabus authority

Current Junior syllabus transcription supplied for this project:

### Algebra

- Quadratic and higher-degree algebraic equations
- Logarithms
- Remainder theorem
- Sequences and series
- Scales of notations
- Mathematical induction
- Basic inequalities

### Geometry

- Circle theorems
- Chords
- Arcs
- Angles in segments
- Cyclic quadrilaterals
- Tangents
- Intersecting chord theorem
- Apollonius theorem
- Alternate Segment theorem
- Stewart's theorem

### Number Theory

- Modular arithmetic
- Greatest Integer function
- Least Integer function

### Combinatorics

- Fundamental Principle of Counting
- Basics of permutations and combinations
- Pigeonhole principle
- Principle of inclusion and exclusion

This transcription must be reconciled to an exact official AMTI 2026 prospectus locator before being promoted to `P0_OFFICIAL_AMTI_ORIGINAL` inside the source ledger.

## 3. Preliminary evidence hierarchy

Use the strongest available source for each paper/question.

1. `P0_OFFICIAL_AMTI_ORIGINAL` — original AMTI paper/prospectus/key.
2. `P1_VERIFIED_FAITHFUL_REPRODUCTION` — reproduction checked against an original or independent matching copy.
3. `P2_REPUTABLE_SECONDARY_ARCHIVE` — reputable archive but not independently verified against original.
4. `P3_PARTIAL_OR_UNVERIFIED_TRANSCRIPTION` — incomplete, image-dependent, transcription-damaged, or uncertain.

The current Cheenta 2024 and 2025 Bhaskara Screening pages begin as `P2_REPUTABLE_SECONDARY_ARCHIVE`. Individual question records may be downgraded to P3 when a figure or transcription is insufficient for independent reconstruction.

## 4. Stable question IDs

Format:

`NMTC-BH-P-YYYY-QNN`

Examples:

- `NMTC-BH-P-2024-Q01`
- `NMTC-BH-P-2025-Q30`

Do not encode a coaching-site page title into the stable mathematical ID.

## 5. Question fingerprint contract

Every question must record at least:

- stable ID;
- source provenance and locator;
- response format;
- primary and secondary concepts;
- visible form;
- hidden structure / invariant;
- best first move;
- minimum expert solution path;
- tempting wrong move / trap;
- case or domain restrictions;
- Preliminary difficulty vector;
- archetype ID;
- source completeness status;
- student-facing use classification.

## 6. Copyright-safe corpus policy

The repository should prefer **question metadata, mathematical fingerprints, short descriptive summaries, and source locators** rather than reproducing entire third-party paper pages verbatim.

Exact wording may be retained only when source rights and project policy permit it. Author-created foundation and transfer questions must be original and clearly labeled.

## 7. Curriculum weighting rule

Historical paper evidence answers:

- which mechanisms recur;
- how concepts are disguised;
- what level of algebraic compression is expected;
- which traps recur;
- what combinations of topics occur;
- what response formats and time-pressure patterns appear.

Historical frequency does **not** remove an explicit syllabus topic.

Use:

`syllabus authority + PYQ recurrence + prerequisite dependency + transfer value`

for curriculum priority.

## 8. Preliminary-specific pedagogy

Concept learning:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Performance learning:

`SEE -> RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

The student must learn to identify the structure without being told the chapter label.

## 9. Source defect rule

Never silently repair a source defect.

Record one of:

- `SOURCE_COMPLETE`
- `SOURCE_IMAGE_REQUIRED`
- `SOURCE_TRANSCRIPTION_SUSPECT`
- `SOURCE_INCOMPLETE`
- `SOURCE_CONFLICT`

A question with unresolved source defects may inform research but cannot be used as a clean canonical anchor until resolved.
