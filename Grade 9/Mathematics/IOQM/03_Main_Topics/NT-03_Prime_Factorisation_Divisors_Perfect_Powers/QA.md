# NT-03 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

## Static gate table

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | 8 stable anchors retain validated paper/key custody and independent answer agreement. |
| G1 dependency | PASS_STATIC | NT-01 retrieved; no NT-04/NT-02 canon required for learner progression. |
| G2 governing model | PASS_STATIC | `INTEGER -> PRIME EXPONENT VECTOR -> EXPONENT RESTRICTION -> COUNT / RECONSTRUCT -> CHECK`. |
| G3 ownership/overlap | PASS_STATIC | FTA/exponents/divisors/perfect powers/squarefree/valuations/factor-pair restrictions are NT-03-owned; gcd/lcm remains NT-01. |
| G4 research-interface discipline | PASS_STATIC | 7 separate A-P microstream interface files; consolidated interface is index-only. |
| G5 lead integration | PASS_STATIC | one integrated learner book and one vocabulary/router. |
| G6 deduplication | PASS_STATIC | prerequisite retrieval used instead of a second gcd/lcm chapter. |
| G7 cross-boundary contrasts | PASS_STATIC | more than 8 explicit mechanism contrasts. |
| G8 fading | PASS_STATIC | internal fading plan present; later learner items remove support. |
| G9 First-Step | PASS_STATIC | one integrated First-Step Reference follows the Assimilation Book. |
| G10 independent mastery | PASS_STATIC | learner title is `Independent Mastery Check`; no method labels in first attempt. |
| G11 mathematics | PASS_STATIC | 8 historical anchors and all authored numerical items independently recomputed; high-risk items brute-forced. |
| G12 source custody | PASS_STATIC | historical IDs preserved; author-created items have no fake historical attribution. |
| G13 student hygiene | PASS_STATIC | forbidden control-label scan returned no matches on learner sources. |
| G14 render authority | PASS_STATIC | one fixed PDF generation path for the full student pack. |
| G15 render/preflight | PASS_CURRENT_BLOB_8_OF_8 | structural preflight PASS; every rendered page visually inspected. |
| G16 transfer quality | PASS_STATIC | representation, context, discrete/extremal and cross-domain transfer included. |
| G17 ownership completeness | PASS_STATIC | recognition, derivation, boundary, first move, independent solve and transfer all covered. |
| G18 evidence-dependent | NOT_RUN | classroom timing/readability, retention, psychometrics, qualification probability, percentile/pass-mark calibration. |

## Historical anchor verification

- `IOQM-2025-Q06` -> 15: PASS.
- `IOQM-2024-Q01` -> 11: PASS.
- `IOQM-2024-Q25` -> 22: PASS.
- `IOQM-2024-Q28` -> 20: PASS.
- `IOQM-2024-Q29` -> 28: PASS.
- `IOQM-2023-Q01` -> 22: PASS.
- `IOQM-2023-Q09` -> 17: PASS.
- `IOQM-2023-Q30` -> 18: PASS.

## Render evidence

Canonical learner inputs:
- `02_Assimilation_Book.md`
- `03_First_Step_Reference.md`
- `04_Recognition_and_First_Line_Lab.md`
- `05_Practice_and_Transfer_Bank.md`
- `06_H0_Mastery_Test.md`

Artifact: `PDFs/NT03_Student_Pack_v1.pdf`

- expected Git blob SHA: `7047d67be42f63fb9643f09188457f288fbffadb`
- SHA-256: `41ad7011b9068fd66a62fd97262a1c70b4d0e6ee41c13095e3a51b38db6baef1`
- byte size: `13737`
- PDF version: `1.4`
- page size: US Letter, `612 x 792 pt`
- page count: `8`
- encrypted: no
- forms/attachments/annotations: none
- learner control-label scan: PASS
- page-by-page visual inspection: PASS `8/8`
- clipping/overlap/broken-glyph/overflow check: PASS

The Git blob identity is the SHA-1 over the exact final inspected PDF bytes and is re-read after branch commit.

## Frozen downstream interface

`Authoring/NT03_Stable_Divisor_PerfectPower_Interface_v1.md`

State: `FROZEN_FOR_DOWNSTREAM_CONSUMPTION`.

NT-04 may retrieve this interface after NT-03 is merged to the production base.

## Promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS
WAVE4_H0_MASTERY_PASS
WAVE5_INDEPENDENT_QA_PASS
WAVE6_STATIC_RENDER_QA_PASS
BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED
```

No classroom, retention, psychometric, qualification-probability, percentile or publication-readiness claim is made.
