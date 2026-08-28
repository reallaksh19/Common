# NMTC Bhaskara Preliminary — Mixed Mock System Blueprint v1

## Purpose

This is the capstone assessment layer over the ten internally complete Preliminary packages.

It is designed to test the performance chain:

`SEE -> RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> SWITCH DOMAIN -> TRANSFER`

It is not an official AMTI paper, an official weightage table, or a psychometrically calibrated score scale.

## Source and format custody

The qualified 2024 Bhaskara Preliminary paper explicitly states:

- time: 2 hours;
- maximum marks: 30;
- correct response: `+1`;
- incorrect response: `-1/2`.

The 2024 answer-key shape is 15 option responses followed by 15 numerical responses.

For author-created mocks, this package adopts a **T24 current-like training profile**:

- 30 questions;
- 120 minutes;
- Q01–Q15 multiple choice;
- Q16–Q30 numerical response;
- training score `+1` correct, `-0.5` incorrect, `0` blank.

This is an author-created training convention grounded to the evidence-controlled 2024 profile. It must never be described as the universal NMTC format for all years.

## Provenance

Every mock question is:

`AUTHOR_CREATED_TRANSFER`

No mock question receives an NMTC year/question number.

No historical figure is redrawn or inferred. The v1 mocks are text-complete and diagram-independent.

## Three-mock progression

### Mock A — Baseline mixed execution

Purpose:

- check whether the student can switch among all major domains;
- favor clean, compact first moves;
- expose formula-first or chapter-label dependence.

### Mock B — Disguised transfer

Purpose:

- increase representation switching;
- require source-independent recognition of the invariant;
- increase complement/case, remainder, endpoint and method-choice traps.

### Mock C — High-ceiling mixed recognition

Purpose:

- compress first-move latency;
- mix high-ceiling modular, coefficient, recurrence, geometry and floor/ceiling reasoning;
- test whether the student can reject an attractive but structurally wrong method.

## Allocation policy

The five-year scored corpus signal is approximately:

- Algebra 45.2%;
- Geometry 23.7%;
- Number Theory 17.8%;
- Combinatorics 5.9%;
- Arithmetic/Foundation 7.4%.

These are **not official weightages**.

Mock allocation uses them only as a broad historical signal. It deliberately prevents frequency overfit by ensuring that sparse-but-explicit syllabus nodes appear across the three-paper rotation.

Target per 30-question mock, with small rotation allowed:

- Algebra / sequences / inequalities / radicals / polynomial / P2 algebra: 12–14;
- Geometry: 6–7;
- Number Theory: 4–6;
- Combinatorics: 2–3;
- cumulative arithmetic/modeling: 1–2.

Across the three mocks, both P2 topics—Mathematical Induction and Greatest/Least Integer Functions—must be assessed repeatedly despite weak current PYQ recurrence.

## Package codes used by teacher keys

- `P0-1` Polynomial & Root Structure
- `P0-2` Radicals / Exponents / Logs
- `P0-3` Inequalities / Bounds / Equality
- `P0-4` Modular / Divisibility / Digit Structure
- `P0-5` Circle / Tangent Recognition
- `P1-1` Sequence & Series Preliminary
- `P1-2` Combinatorics / Pigeonhole / Inclusion–Exclusion
- `P1-3` Triangle Metric / Apollonius / Stewart
- `P2-1` Mathematical Induction
- `P2-2` Greatest / Least Integer Functions
- `AF` cumulative Arithmetic/Foundation modeling

## Diagnostic error codes

Teacher keys classify misses by mechanism, not merely chapter:

- `REC` — concept/archetype not recognized;
- `FM` — wrong first useful move;
- `REP` — failed representation switch;
- `ALG` — algebra/calculation error after correct method;
- `DOM` — domain/sign/boundedness/endpoint error;
- `CASE` — missing/overlapping case;
- `COUNT` — overcount/undercount;
- `FIG` — geometry relation/label error;
- `LOGIC` — induction/proof logic error;
- `CHECK` — answer not independently checked;
- `TIME` — correct method not completed under time pressure.

## Attempt protocol

### Pass 1 — recognition sweep

Before full solving, the learner should identify the likely first move for as many questions as possible.

Recommended training record per question:

`recognized? | first move | solve | check | confidence`

Do not expose package labels on the student paper.

### Pass 2 — solve

Prioritize questions with a clear first line.

### Pass 3 — boundary check

Before finalizing, recheck:

- sign/domain;
- floor/ceiling endpoints;
- parity/integrality;
- boundedness/equality attainability;
- leading zero / overcount;
- modular cycle index;
- geometry segment labels;
- whether the requested quantity was actually answered.

## Scoring and calibration rule

The raw T24 training score is:

`correct - 0.5*wrong`.

No universal mastery cutoff is frozen in v1.

Until classroom timing/readability calibration is run, score interpretation must remain diagnostic rather than psychometric. Use:

- raw score;
- correct/wrong/blank;
- package hit rate;
- error-code counts;
- first-move accuracy;
- time-completion record.

## Retest routing

A missed question must route back to the smallest useful remediation unit:

`question -> error code -> first-step card -> relevant F-level ladder -> non-identical transfer -> mixed retest`

Do not send a student back to an entire chapter when the failure is a specific boundary or first-move error.

## Mock separation policy

Student papers contain only:

- training-profile note;
- instructions;
- unlabelled questions.

Teacher keys contain:

- answer;
- package;
- first move;
- minimum path/check;
- likely error tag.

This separation prevents chapter labels from leaking the intended method.

## Current status

`STATUS: MOCK_SYSTEM_AUTHORING`

Publication blockers remain:

- classroom timing calibration;
- final copyedit and rendered-paper QA;
- machine-readable item metadata;
- 2022 source recovery before any six-year weighting claim.
