# ALG-04 — QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

## Gate table

| Gate | State | Evidence |
|---|---|---|
| Wave 0 concept/dependency map | PASS | exact scope, owner boundary, representations, misconceptions, transfer endpoints |
| canonical router | PASS | `TERM/SUM -> EXPLICIT/RECURRENT -> LOCAL/GLOBAL -> NEARBY SUBTRACTION -> TELESCOPE -> COMPUTE` |
| source anchors | PASS | `IOQM-2025-Q26`, `IOQM-2023-Q10` only as ALG-04 primaries |
| anchor key/source join | PASS | Q26=10; Q10=51 |
| independent mathematical audit | PASS_STATIC_SECOND_ROUTE | `Authoring/Independent_Mathematical_Audit.md` |
| recurrence interface | PASS_STABLE | notation, semantics, initialization, explicit-v-recursive, verification, local cancellation |
| canonical overlap ownership | PASS | counting-state recurrence derivation kept under COMB-03 |
| attempt before hint | PASS_STATIC | all supported tasks state H0 attempt before optional hints |
| H3 -> H2 -> H1 -> H0 fading | PASS_STATIC | support-fading track decreases maximum available support |
| term vs sum contrast | PASS_STATIC | concept, lab, practice, H0 |
| AP vs GP contrast | PASS_STATIC | includes “neither” boundary |
| explicit vs recurrence contrast | PASS_STATIC | includes initialization and verification |
| compute-many vs nearby subtraction | PASS_STATIC | windows, first differences, invariant |
| algebraic vs counting recurrence | PASS_STATIC | owner boundary + T4 bridge |
| integrated First-Step Reference | PASS_STATIC | one topic-wide router/reference |
| real changed-surface transfer | PASS_STATIC | T2/T3/T4 representation, rolling-total, machine-invariant, counting-state boundary |
| H0 mixed mastery | PASS_STATIC | first-line, full solve, same-surface/different-decision, transfer, WHY-NOT |
| teacher diagnostic key | PASS_STATIC | full answers + 12 diagnostic codes/remediation routes |
| item metadata | PASS_STATIC | 48 metadata rows including anchors, practice, transfer and H0 items |
| student-export scrub | PASS | no GitHub/Issue/PR/Wave/agent/teacher-control or internal topic-code leakage in final PDF text |
| PDF structural preflight | PASS | openable, unencrypted, non-scanned, no XFA |
| PDF render | PASS | 20 A4 pages rendered at 160 dpi |
| PDF page-by-page visual QA | PASS | all 20 final rendered pages inspected; no clipping, overlap, broken glyphs or table overflow |
| classroom timing/readability observation | NOT_RUN | evidence-dependent |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric difficulty/discrimination | NOT_RUN | evidence-dependent |
| publication approval | NOT_RUN | separate decision |

## Independent historical-anchor audit

### IOQM-2025-Q26

Second-route audit proves:
- length 11 is impossible from the strict cycle  
  `a_1<a_5<a_9<a_2<a_6<a_10<a_3<a_7<a_11<a_4<a_8<a_1`;
- length 10 exists, for example  
  `(2,5,8,0,3,6,9,1,4,7)`.

Result: `10` — PASS.

### IOQM-2023-Q10

Validated paper initialization:
- `a_0=1`;
- `a_1=-4`;
- `a_{n+2}=-4a_{n+1}-7a_n`.

With
`D_n=a_n^2-a_{n-1}a_{n+1}`,

`D_{n+1}=7D_n`.

Since `a_2=9`,
`D_1=16-9=7`,
so `D_50=7^50` and the divisor count is `51`.

Result: `51` — PASS.

## PDF artifact

- path: `PDFs/ALG04_Student_Pack_v1.pdf`
- page count: `20`
- page size: A4
- SHA-256: `17c56ed4d5bf5c333a5afaed79a48e7038557852006c1cd96c76b0cbd15f046a`
- renderer used: repository PDF render pipeline (`render_pdf.py`, 160 dpi)
- visual disposition: PASS on pages 1–20
- leakage scan: PASS
- structural preflight: PASS

The previous one-page compact preview is replaced by this integrated 20-page student pack.

## Static completion state

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This state means:
- source, mathematics, pedagogy structure, metadata and static render QA are complete;
- it does **not** claim classroom validation, retention evidence, psychometric calibration, qualification probability or final publication approval.
