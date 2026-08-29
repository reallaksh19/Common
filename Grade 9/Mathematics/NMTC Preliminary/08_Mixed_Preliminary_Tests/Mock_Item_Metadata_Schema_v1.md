# NMTC Preliminary Mock Item Metadata Schema v1

Authority file: `Mock_Item_Metadata_v1.csv`.

## Purpose

Provide deterministic machine-readable custody for every author-created mock item without confusing the item with an official NMTC PYQ.

## Required fields

| Field | Meaning | Rule |
|---|---|---|
| `id` | stable author-created item ID | `NMTC-MOCK-[A-C]-QNN`; unique |
| `mock` | paper A/B/C | must match ID |
| `question` | 1–30 | unique within mock |
| `response_type` | `mcq` or `numeric` | Q01–Q15 MCQ, Q16–Q30 numeric in v1 |
| `answer` | authoritative v1 answer | string representation; must match teacher key |
| `package_primary` | primary curriculum package | one of P0-1..P2-2 or AF |
| `package_secondary` | optional bridge package | blank unless genuinely cross-package |
| `domain` | broad domain | Algebra / Geometry / NumberTheory / Combinatorics / ArithmeticFoundation |
| `diagnostic_tags` | likely failure mechanisms | pipe-separated controlled tags |
| `provenance` | content provenance | always `AUTHOR_CREATED_TRANSFER` in v1 mocks |
| `profile` | paper profile | `T24_CURRENT_LIKE_TRAINING` |
| `official_nmtc_question` | official-question flag | must be `false` for every v1 mock item |
| `classroom_timing_status` | timing evidence state | currently `NOT_RUN` |

## Controlled diagnostic tags

- `REC`
- `FM`
- `REP`
- `ALG`
- `DOM`
- `CASE`
- `COUNT`
- `FIG`
- `LOGIC`
- `CHECK`
- `TIME`

Multiple tags are separated by `|`.

## Package codes

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
- `AF` Arithmetic/Foundation modeling

## Validation invariants

For v1 the ledger must satisfy:

```text
row_count = 90
unique_id_count = 90
questions_per_mock = 30
mcq_per_mock = 15
numeric_per_mock = 15
official_nmtc_question_true_count = 0
provenance_distinct = {AUTHOR_CREATED_TRANSFER}
classroom_timing_status_distinct = {NOT_RUN}
```

The answer field must match the corresponding teacher key after every editorial revision.

## Revision rule

If a question stem or answer changes materially:

1. update the student paper;
2. update the teacher key;
3. update the metadata row;
4. re-run the mock-system mathematical audit;
5. if classroom calibration already exists, increment the item/paper revision and do not combine pre/post-revision timing as a single calibration sample.

## Historical attribution guardrail

These IDs are deliberately **not** `NMTC-BH-P-YYYY-QNN` IDs. They must never be presented as previous-year questions.
