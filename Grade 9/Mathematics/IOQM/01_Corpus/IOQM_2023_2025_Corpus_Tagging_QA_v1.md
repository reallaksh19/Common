# IOQM Grade 9 — 90-Question Corpus Tagging QA v1

Status: `PASS_STATIC_90Q_CORPUS_AND_ANSWER_VERIFICATION`

## Structural validation

| Check | Result |
|---|---|
| total rows | PASS — 90 |
| unique item IDs | PASS — 90 |
| 2023 question sequence | PASS — Q01–Q30 |
| 2024 question sequence | PASS — Q01–Q30 |
| 2025 question sequence | PASS — Q01–Q30 |
| exactly one primary domain/item | PASS |
| exactly one primary main-topic ID/item | PASS |
| primary-domain denominator | PASS — 90 |
| main-topic denominator | PASS — 90 |
| all 22 architecture topics represented | PASS — 22/22 |
| stable IDs `IOQM-YYYY-QNN` | PASS |
| official/validated source links present | PASS |
| official answer-key value captured | PASS — 90/90 |
| known 2025 provisional-key correction preserved | PASS — `IOQM-2025-Q11` |
| independent answer recomputation | PASS — 90/90 |
| independent/key answer mismatches | PASS — 0 |
| repository metadata defects isolated | PASS — 2 |
| difficulty calibration | NOT_RUN |
| classroom timing/readability | NOT_RUN |
| psychometric calibration | NOT_RUN |

## Independent verification authority

Answer verification is recorded in:

- `Verification/IOQM_Independent_Answer_Verification_Batch_A_Q01_Q10_v1.md`;
- `Verification/IOQM_Independent_Answer_Verification_Batch_B_Q11_Q20_v1.md`;
- `Verification/IOQM_Independent_Answer_Verification_Batch_C_Q21_Q30_v1.md`;
- `Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`.

The three batches independently recompute Q01–Q30 for each of 2023, 2024 and 2025. All 90 recomputed answers agree with the validated/final key authority.

This closes **answer-level mathematical verification** for the seed corpus. It does not by itself qualify every future transcription, diagram recreation, classroom explanation or derived transfer item.

## Metadata-correction overlay

Two errors were found in the repository's classifier/extraction metadata. Neither is a historical source defect.

### `IOQM-2023-Q04`

Validated paper mathematics contains `x^4`, not `x/4`.

Disposition:

- historical source remains clean;
- answer `07` independently verified;
- downstream teaching/source use must read the validated paper or correction overlay, not the stale flattened clue in the first classifier row.

### `IOQM-2025-Q28`

Validated paper mathematics is the nested radical

`√(x - √(x+a)) = √a - y`.

The first classifier row flattened this to a difference of two radicals.

Disposition:

- historical source remains clean;
- answer `91` independently verified from the nested-radical statement;
- downstream teaching/source use must use the validated paper or correction overlay.

These are `REPOSITORY_METADATA_CORRECTION_REQUIRED`, not `SOURCE_CONFLICT`.

## Domain totals

- NT: 24
- ALG: 18
- GEO: 25
- COMB: 23

These are single-primary-classification counts over this three-paper seed corpus. They are operational curriculum signals only, **not official IOQM weightage**.

## Classification-review status

- `SECOND_PASS_STEM_REVIEWED`: 90/90
- HIGH primary-ownership confidence: 49
- MEDIUM primary-ownership confidence: 41
- LOW: 0

The confidence field applies to **taxonomy ownership**, not source authenticity or student difficulty.

## Source custody

### 2025

- official HBCSE paper;
- final official key dated 2 October 2025;
- final key explicitly corrects the provisional answer for M1 Q11 from 61 to 26;
- final key documents a rejected degenerate alternate interpretation for M1 Q23;
- paper-level gcd notation typo is preserved as a source event.

### 2024

- official HBCSE paper;
- HBCSE answer key captured for Q01–Q30.

### 2023

- HBCSE past-paper index points to the MTAI paper;
- the question paper contains the embedded 30-answer key.

## Non-inflation rule

Secondary domains/mechanisms are pedagogical bridge tags only. Recurrence tables use the single primary `main_topic_id` unless a future analysis explicitly defines another denominator.

## Promotion gate

The corpus may now drive:

- source coverage maps;
- main-topic issue scoping;
- recognition/misconception research;
- candidate PYQ-anchor selection;
- answer-level historical teaching authority for the 90 validated items, provided the exact paper statement/figure is used;
- production planning and recurrence analysis using the explicit 90-question denominator.

It must **not** be used to claim:

- official IOQM topic weightage;
- classroom difficulty/timing;
- psychometric discrimination;
- qualification probability;
- publication readiness of future student books.

For `IOQM-2023-Q04` and `IOQM-2025-Q28`, the correction overlay is mandatory until the detailed classifier ledger itself is regenerated from the exact validated stem.