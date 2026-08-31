# ALG-07 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

Static QA covers source custody, mathematics, pedagogy/ownership, metadata, student-export hygiene and final render custody.

## Gate table

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | HBCSE 2024 official paper/key recorded; stable anchors `IOQM-2024-Q21`, `IOQM-2024-Q26`; no Grade-9-only syllabus/weightage claim. |
| G1 dependency | PASS_STATIC | concept/dependency map; general inequality optimization remains ALG-02-owned. |
| G2 governing model | PASS_STATIC | `DISCRETE VALUE -> HALF-OPEN INTERVAL -> CONTINUOUS CONDITION -> INTEGER FILTER -> ENDPOINT CHECK`. |
| G3 ownership/overlap | PASS_STATIC | ALG-07 owns floor/ceiling interval decoding and discrete filtering; ALG-02 general inequality canon excluded. |
| G4 research-interface discipline | PASS_STATIC | authoring-only consolidated interfaces; no separate student chapters. |
| G5 lead integration | PASS_STATIC | one integrated Assimilation Book and one learner vocabulary. |
| G6 deduplication | PASS_STATIC | definitions/derivations taught once; later material retrieves/compresses. |
| G7 cross-boundary contrasts | PASS_STATIC | 9 explicit contrasts, including all four required by assignment. |
| G8 attempt-before-help/fading | PASS_STATIC | TRY uses H3 -> H2 -> H1 -> H0 and requires an attempt first. |
| G9 integrated First-Step | PASS_STATIC | one topic-wide First-Step Reference. |
| G10 H0 mastery | PASS_STATIC | 16 unlabelled items covering first-line, mixed solving, contrast, changed surface and WHY-NOT. |
| G11 independent mathematics | PASS_STATIC_FRESH_REAUDIT | both historical anchors and promoted author-created answers rechecked. |
| G12 source custody | PASS_STATIC | historical IDs/source/key roles explicit; author-created items have no fake attribution. |
| G13 student-export hygiene | PASS_STATIC | source/PDF scans show no Issue/PR/Wave/agent/interface/QA-state terminology. |
| G14 one render authority | PASS_STATIC | one deterministic ReportLab PDF build. |
| G15 render/preflight | PASS_STATIC | 3/3 pages rendered and inspected; preflight passes; hash/page count recorded. |
| G16 transfer quality | PASS_STATIC | T2 interval representation, T3 counting/context and T4 NT/COMB discrete-filter bridge present. |
| G17 six-question ownership | PASS_STATIC | meaning, trigger, boundary, first line, independent solve and changed-surface use covered. |
| G18 evidence-dependent gates | NOT_RUN | classroom timing/readability, longitudinal retention, psychometrics, qualification probability, percentile/pass-mark calibration. |

## Historical source audit

`IOQM-2024-Q21`: fresh reconstruction gives unique `n=8991`, hence answer `91`; official key and verification ledger agree.

`IOQM-2024-Q26`: set `n=floor(x)` and use `x in [n,n+1)`; only `n=16,17` are feasible, sum `33`; official key and verification ledger agree.

## Metadata QA

`Item_Metadata.csv` uses the frozen 31-column schema: columns 31/31, data rows 64, malformed-width rows 0, historical rows 2, author-created rows 62. Difficulty/psychometric fields are not used as evidence.

## Stable prerequisite interface

`Authoring/ALG07_Prerequisite_Interface.md` is frozen as `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`; downstream status `READY_FOR_RETRIEVAL`.

## Final PDF artifact

- path: `PDFs/ALG07_Student_Pack_v1.pdf`
- page size: US Letter, 612 x 792 pt
- page count: **3**
- SHA-256: **`730c89e15ffe61817a4fcb66f3ad5774a81f98000d4f67e6d62d859025132207`**
- encrypted: no
- PyMuPDF openable: yes
- likely scanned: no
- XFA: no

All 3/3 pages were rendered at 150 dpi and visually inspected: no clipping, overlap, missing glyphs, margin overflow or teacher-answer leakage observed.

## Explicit NOT_RUN / non-claims

- classroom timing/readability: `NOT_RUN`;
- longitudinal retention: `NOT_RUN`;
- psychometric difficulty/discrimination: `NOT_RUN`;
- qualification probability: `NOT_RUN`;
- percentile/pass-mark calibration: `NOT_RUN`;
- official IOQM topic weightage from the 90-question corpus: not claimed.

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
