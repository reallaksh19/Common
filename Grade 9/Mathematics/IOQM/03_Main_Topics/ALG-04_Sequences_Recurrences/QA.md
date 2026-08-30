# ALG-04 — QA

Status: `BENCHMARK_PREVIEW_READY_NOT_CLASSROOM_CALIBRATED`

| Gate | State |
|---|---|
| Wave 0 architecture | PASS |
| governing local-cancellation router | PASS |
| source anchors | PASS — 2025-Q26, 2023-Q10 |
| anchor answer verification | PASS |
| canonical overlap ownership | PASS — counting-state modelling kept in COMB-03 |
| attempt-before-hints | PASS_STATIC |
| H3->H0 fading | PASS_STATIC |
| term-vs-sum contrast | PASS_STATIC |
| AP-vs-GP contrast | PASS_STATIC |
| algebraic-vs-counting recurrence contrast | PASS_STATIC |
| integrated First-Step layer | PASS_STATIC |
| H0 mastery | PASS_STATIC |
| teacher diagnostic key | PASS_STATIC |
| fresh independent reviewer | PARTIAL |
| repository PDF preflight | PASS_PREVIEW — 1-page A4 compact preview, openable, unencrypted, non-scanned, no XFA |
| repository PDF visual QA | PASS_PREVIEW — page inspected; no clipping, overlap or broken glyphs |
| student/teacher leakage | PASS_PREVIEW |
| classroom timing | NOT_RUN |
| psychometrics | NOT_RUN |

## Repository PDF artifact

- path: `PDFs/ALG04_Student_Pack_v1.pdf`
- page count: 1
- SHA-256: `9c98f5627beb744033c1184c7270bb3b55d9bcb86a1fae80d4b06995872d2633`
- disposition: compact benchmark-preview artifact for repository custody.

A separate 3-page higher-typography production preview was generated and visually inspected during authoring; its SHA-256 is `94eab6f204533a84ce702d6aed96a2133cff184e242808259137c15f74613ddb`.

## Mathematical spot checks

- moving-window identity `W_{i+1}-W_i=a_{i+k}-a_i` is correct;
- telescoping decompositions are correct;
- H0 #2 solution `a_n=4^{n-1}+1` satisfies initial values and recurrence;
- H0 #7 first-difference solution gives `a_n=2^{n+1}-1` and `a_20=2097151`;
- equal k-term adjacent windows correctly imply period dividing k.

## Promotion state

`BENCHMARK_PREVIEW_READY_NOT_CLASSROOM_CALIBRATED`

Do not call this publication-ready until a fresh independent reviewer and evidence-dependent classroom gates close.