# Mixed Preliminary Mock System — QA v1

## Verdict

`INTERNAL_MOCK_SYSTEM_COMPLETE_NOT_PUBLICATION_READY`

The three author-created full mocks, teacher keys, blueprint and diagnostic record have passed a second mathematical/editorial audit.

## Scope

Assets audited:

- `08_Mixed_Preliminary_Tests/Mock_System_Blueprint_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_A_Student_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_A_Teacher_Key_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_B_Student_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_B_Teacher_Key_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_C_Student_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_C_Teacher_Key_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_Diagnostic_Record_Template_v1.md`

Total full-mock items reviewed: **90**.

## Format/source custody

PASS.

- 2024 qualified paper profile is the authority for the T24 training convention: 2 hours, 30 marks, `+1/-1/2`.
- 15-option + 15-numerical structure is taken from the qualified 2024 answer-key shape.
- The mock system explicitly states that this is an author-created current-like training profile, not a universal historical NMTC format.
- Every mock item is `AUTHOR_CREATED_TRANSFER`.
- No fake historical year/question attribution exists.
- No historical figure is inferred or redrawn.

## Student/teacher separation

PASS.

Student papers contain no package codes, chapter labels, first-move hints, diagnostic tags or solutions.

Teacher keys contain answer, package, first useful move, compact check and likely diagnostic tag.

This preserves `PRELIM-25 MIXED_UNLABELLED`.

## Final answer vectors

### Mock A

MCQ:

`B A B B C C C B C A C B C B B`

Numerical Q16–Q30:

`5, 7, 5, 5, 4, 93, 20, 6, 65, 21, 3, 96, 8, 42, 7`

### Mock B

MCQ:

`A B D C B C C B B B A B C B C`

Numerical Q16–Q30:

`16, 6, 9, 8, 3, 55, 30, 2, 19, 26, 2, 75, 1, 9, 8`

### Mock C

MCQ:

`C B C B B C C B A C B D B B A`

Numerical Q16–Q30:

`4, 5, 4, 113, 4, 48, 20, 24, 54, 2, -1, 54, 1, 42, 60`

## Mathematical audit coverage

The second pass explicitly recomputed/checks:

- Vieta symmetric expressions and common-root substitution;
- polynomial remainders modulo `x^2-1`, `x^2+1`, `x^2+x+1`;
- radical hidden-square identities;
- exponent/log common-base and domain transformations;
- AM-GM minimum/equality and unbounded-maximum falsifiers;
- Cauchy/Engel reciprocal bound;
- absolute-value denominator exclusion;
- modular cycles, multiplicative order, LCM same-remainder and GCD-difference structures;
- divisibility by 9 and 11;
- tangent right triangles, tangent-chord, cyclic angle, intersecting-chord and tangent-secant power;
- Apollonius, altitude cancellation, Stewart, angle-bisector and right-triangle `R/r` metrics;
- AP/GP, recurrence, telescoping and infinite-GP reconstruction;
- permutations with repetition, subset parity, coefficient-as-count, pigeonhole and inclusion-exclusion;
- induction step-size coverage, strong-induction recognition and direct-proof method selection;
- floor/ceiling with negative values, fractional part, interval translation and integer counting;
- rate change, clock-angle and mensuration foundation items.

No unresolved mathematical answer defect remains in the v1 mock set.

## Defects caught before promotion

### QA-CORR-01 — geometry allocation

Initial drafts contained only five geometry items per mock, below the blueprint target.

Correction:

- Mock A Q19 changed from a redundant modular-cycle item to a right-triangle circumradius item;
- Mock B Q19 changed from a redundant CRT item to tangent-length geometry;
- Mock C Q19 changed from a redundant modulo-5 item to cyclic-quadrilateral geometry.

Final: **6 geometry questions per mock**.

### QA-CORR-02 — Mock B Q13 remainder boundary

Initial wording asked for the least positive integer leaving remainder 5 under 6, 8 and 9. That made `5` itself valid.

Correction:

stem now says **greater than 5**, making the intended LCM result `77` mathematically authoritative.

No stale answer remains in the student paper or teacher key.

## Frozen per-paper domain allocation

| Domain | Mock A | Mock B | Mock C | Total / 90 |
|---|---:|---:|---:|---:|
| Algebra incl. P2 + Sequences | 16 | 16 | 15 | 47 |
| Geometry | 6 | 6 | 6 | 18 |
| Number Theory | 4 | 4 | 4 | 12 |
| Combinatorics | 3 | 3 | 4 | 10 |
| Arithmetic/Foundation | 1 | 1 | 1 | 3 |
| **Total** | **30** | **30** | **30** | **90** |

This is a training allocation, not an official or reconstructed historical weighting table.

## Package item totals across 90 questions

| Package | Items |
|---|---:|
| P0-1 Polynomial & Root Structure | 11 |
| P0-2 Radicals / Exponents / Logs | 8 |
| P0-3 Inequalities / Bounds / Equality | 8 |
| P0-4 Modular / Divisibility / Digits | 12 |
| P0-5 Circle / Tangent | 9 |
| P1-1 Sequence & Series | 7 |
| P1-2 Combinatorics | 10 |
| P1-3 Triangle Metric | 9 |
| P2-1 Mathematical Induction | 5 |
| P2-2 Greatest / Least Integer | 8 |
| AF Arithmetic/Foundation | 3 |
| **Total** | **90** |

P2 topics are intentionally present despite weak five-year direct recurrence.

## Gate review

- `PRELIM-01 PRELIMINARY_ONLY`: PASS
- `PRELIM-02 SYLLABUS_CUSTODY`: PASS for all mock mechanisms
- `PRELIM-03 NO_FREQUENCY_OVERFIT`: PASS
- `PRELIM-07 SOURCE_DEFECTS_VISIBLE`: PASS
- `PRELIM-08 NO_FAKE_OFFICIAL`: PASS
- `PRELIM-10 HIDDEN_STRUCTURE`: PASS through teacher key first moves
- `PRELIM-11 FIRST_MOVE`: PASS
- `PRELIM-12 MINIMUM_PATH`: PASS where detailed check is useful; remaining items are direct one-step verified answers
- `PRELIM-13 TRAP_MODEL`: PASS through diagnostic tags
- `PRELIM-22 RECOGNITION_DRILL`: PASS through capstone mixed recognition demand
- `PRELIM-23 FIRST_LINE_DRILL`: PASS via attempt protocol + package First-Line labs
- `PRELIM-24 SHORT_SOLVE`: PASS
- `PRELIM-25 MIXED_UNLABELLED`: PASS
- `PRELIM-26 CHECK_STRATEGY`: PASS
- `PRELIM-27 YEAR_COVERAGE`: GLOBAL_PARTIAL — 2022 remains blocked
- `PRELIM-29 FIGURE_RECOVERY`: NOT_APPLICABLE to author-created text-complete v1 mocks; historical figure backlog remains globally open
- `PRELIM-30 CROSS_YEAR_RECURRENCE`: PASS for the evidence model used to shape broad emphasis; no six-year claim

## Calibration status

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`

Therefore:

- no pass score is frozen;
- no percentile is claimed;
- no qualification probability is claimed;
- Mock A/B/C labels describe design intent, not psychometric difficulty bands.

Raw score must be accompanied by first-move, error-code and time-completion diagnostics.

## Remaining publication blockers

1. classroom timing/readability calibration with actual Grade IX/X learners;
2. final student/teacher copy separation into publication artifacts;
3. machine-readable mock item metadata;
4. final typography/equation/render QA;
5. 2022 source recovery before any six-year weighting revision;
6. broader cross-package editorial consistency pass.

## Promotion

The capstone mock system is promoted to:

`INTERNAL_MOCK_SYSTEM_COMPLETE_NOT_PUBLICATION_READY`
