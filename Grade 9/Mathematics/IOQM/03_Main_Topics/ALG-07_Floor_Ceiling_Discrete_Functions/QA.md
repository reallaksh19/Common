# ALG-07 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This QA record applies to the repaired current-source branch and the exact committed student PDF blob listed below.

## Gate table

| Gate | State | Evidence |
|---|---|---|
| source authority | PASS_STATIC | HBCSE 2024 official paper/key; stable anchors `IOQM-2024-Q21`, `IOQM-2024-Q26` |
| dependency ownership | PASS_STATIC | floor/ceiling/discrete filtering remain ALG-07-owned; general inequality optimization remains downstream |
| governing model | PASS_STATIC | `DISCRETE VALUE -> HALF-OPEN INTERVAL -> CONTINUOUS CONDITION -> INTEGER FILTER -> ENDPOINT CHECK` |
| per-microstream interfaces | PASS_REPAIRED | seven per-microstream files follow the mandatory filename/header/A-P schema; consolidated synopsis is index-only |
| pedagogy / integration | PASS_STATIC | one integrated learner book, one First-Step layer, recognition lab, practice bank, independent mastery |
| learner-label hygiene | PASS_REPAIRED | H-level/T-level/Wave/PR/Issue/downstream-topic control codes are absent from the regenerated learner PDF; support is described in learner language |
| independent mathematics | PASS_STATIC | Q21=91 and Q26=33 remain independently recomputed; authored answer custody unchanged |
| metadata | PASS_STATIC | frozen 31-column schema retained |
| render authority | PASS_CURRENT_SOURCE | PDF regenerated from the repaired canonical learner files |
| structural PDF preflight | PASS | openable, unencrypted, non-scanned, no XFA |
| exact-blob custody | PASS | local Git blob SHA equals committed GitHub blob SHA |
| page-by-page visual QA | PASS | 7/7 pages rendered and inspected; no clipping, overlap, broken glyphs, or answer leakage observed |
| classroom timing/readability | NOT_RUN | evidence-dependent |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent |

## Historical anchors

- `IOQM-2024-Q21`: independent reconstruction gives the unique `n=8991`, hence answer `91`.
- `IOQM-2024-Q26`: with `n=floor(x)` and `x in [n,n+1)`, only `n=16,17` are feasible, hence `33`.

## Current student PDF custody

- path: `PDFs/ALG07_Student_Pack_v1.pdf`
- page size: US Letter, 612 x 792 pt
- page count: **7**
- file size: **8576 bytes**
- Git blob SHA: **`67089913765a7c3a286c6b36d9ff00c9ecc024f5`**
- SHA-256: **`38b2c0930d433fa9b81e9c4934c9aabcc1ef462ec4e00d07b21c5017f1cb10f8`**
- structural preflight: **PASS**
- visual inspection: **7/7 PASS**
- learner-control-label scan: **PASS**

The renderer is deliberately simple and deterministic: standard Helvetica, fixed margins/leading, Flate-compressed page streams, and no external font dependency. The PDF contains the repaired canonical learner content rather than the superseded compact preview.

## Promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS
WAVE4_MASTERY_PASS
WAVE5_INDEPENDENT_QA_PASS
WAVE6_STATIC_RENDER_QA_PASS
BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED
```

This is a static benchmark/readiness claim only. It is not a claim of classroom calibration, retention evidence, psychometric validation, publication approval, or qualification probability.
