# NMTC Preliminary — Mock Item Metadata Validation v1

Authority inputs:

- `08_Mixed_Preliminary_Tests/Mock_A_Teacher_Key_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_B_Teacher_Key_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_C_Teacher_Key_v1.md`
- `08_Mixed_Preliminary_Tests/Mock_Item_Metadata_v1.csv`

## Reason for this validation

The first metadata reconstruction used a stale pre-rebalance key snapshot and exposed a discrepancy against the PR's frozen domain allocation. The ledger was **not accepted silently**.

The live branch keys were re-read and the metadata was reconciled to the current committed papers.

Three material stale-row corrections were required:

1. `NMTC-MOCK-A-Q19`: stale metadata said Number Theory / answer `1`; live paper/key is Triangle Metric geometry / answer `5`.
2. `NMTC-MOCK-B-Q25`: stale metadata classified the recurrence item primarily as Mathematical Induction; live key classifies it as Sequence & Series / answer `26`.
3. `NMTC-MOCK-C-Q19`: stale metadata said Number Theory / answer `2`; live paper/key is Circle Geometry / answer `113`.

The authoritative CSV now reflects the live keys.

## Structural invariants

```text
row_count = 90
unique_item_ids = 90
duplicate_item_ids = 0
mocks = {A, B, C}
questions_per_mock = 30
mcq_per_mock = 15
numeric_per_mock = 15
provenance = AUTHOR_CREATED_TRANSFER for 90/90
official_nmtc_question = false for 90/90
classroom_timing_status = NOT_RUN for 90/90
```

## Frozen domain allocation

| Domain | Count |
|---|---:|
| Algebra incl. Sequences/P2 | 47 |
| Geometry | 18 |
| Number Theory | 12 |
| Combinatorics | 10 |
| Arithmetic/Foundation | 3 |
| **Total** | **90** |

This is a training allocation, not official AMTI/NMTC weightage.

## Frozen primary-package allocation

| Package | Count |
|---|---:|
| P0-1 Polynomial & Root Structure | 11 |
| P0-2 Radicals / Exponents / Logs | 8 |
| P0-3 Inequalities / Bounds | 8 |
| P0-4 Modular / Divisibility / Digits | 12 |
| P0-5 Circle / Tangent | 9 |
| P1-1 Sequence & Series | 7 |
| P1-2 Combinatorics | 10 |
| P1-3 Triangle Metric | 9 |
| P2-1 Mathematical Induction | 5 |
| P2-2 Greatest / Least Integer | 8 |
| AF Arithmetic/Foundation | 3 |
| **Total** | **90** |

## Frozen answer vectors

### Mock A

MCQ:

`B A B B C C C B C A C B C B B`

Numeric:

`5, 7, 5, 5, 4, 93, 20, 6, 65, 21, 3, 96, 8, 42, 7`

### Mock B

MCQ:

`A B D C B C C B B B A B C B C`

Numeric:

`16, 6, 9, 8, 3, 55, 30, 2, 19, 26, 2, 75, 1, 9, 8`

### Mock C

MCQ:

`C B C B B C C B A C B D B B A`

Numeric:

`4, 5, 4, 113, 4, 48, 20, 24, 54, 2, -1, 54, 1, 42, 60`

## Validation verdict

```text
LIVE_KEY_RECONCILIATION = PASS
METADATA_ROW_COUNT = PASS
ID_UNIQUENESS = PASS
RESPONSE_TYPE_SHAPE = PASS
PROVENANCE_BOUNDARY = PASS
DOMAIN_ALLOCATION = PASS
ANSWER_VECTOR_MATCH = PASS
CLASSROOM_TIMING_FIELDS = NOT_RUN by design

MOCK_MACHINE_METADATA = PASS_STATIC
```

Any subsequent paper/key edit must update the CSV and re-run this validation before promotion.
