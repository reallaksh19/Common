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
| attempt before hint | PASS_STATIC | supported tasks require H0 attempt before optional hints |
| H3 -> H2 -> H1 -> H0 fading | PASS_STATIC | support-fading tracks reduce available support across practice |
| term vs sum contrast | PASS_STATIC | concept, lab, practice, H0 |
| AP vs GP contrast | PASS_STATIC | includes `neither` boundary |
| explicit vs recurrence contrast | PASS_STATIC | includes initialization and verification |
| compute-many vs nearby subtraction | PASS_STATIC | windows, first differences, invariant |
| algebraic vs counting recurrence | PASS_STATIC | owner boundary + transfer bridge |
| integrated First-Step Reference | PASS_STATIC | one topic-wide router/reference |
| real changed-surface transfer | PASS_STATIC | rolling-total, machine-recurrence and counting-state boundaries |
| H0 mixed mastery | PASS_STATIC | first-line, full solve, contrast, transfer, WHY-NOT |
| teacher diagnostic key | PASS_STATIC | full answers + diagnostic/remediation routes |
| item metadata | PASS_STATIC | 48 rows including anchors, practice, transfer and H0 items |
| student-export scrub | PASS | extracted final repository PDF contains no Issue/PR/Wave/agent/teacher-control/internal topic-code leakage |
| repository PDF byte custody | PASS | GitHub blob `f78ab3ee0fe2fdd403fa64ed86b674241ccfe97c` equals independently computed Git blob SHA for the local audited bytes |
| PDF structural preflight | PASS | 5 A4 pages; openable; unencrypted; non-scanned; no XFA |
| PDF render | PASS | 5 pages rendered at 180 dpi |
| PDF page-by-page visual QA | PASS | 5/5 pages inspected; no clipping, overlap, broken glyphs or overflow |
| classroom timing/readability observation | NOT_RUN | evidence-dependent |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric difficulty/discrimination | NOT_RUN | evidence-dependent |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent |
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

Validated initialization:
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

## Repository PDF artifact

- path: `PDFs/ALG04_Student_Pack_v1.pdf`
- page count: `5`
- page size: A4
- SHA-256: `5e1c0cde9ee29c70e34ea25c7fc7f49d6e0926be6883abc820b042e904eb908d`
- Git blob SHA: `f78ab3ee0fe2fdd403fa64ed86b674241ccfe97c`
- repository commit introducing this blob: `2418bd947ce7171db2774395036789fa0a0f252e`
- local independently computed Git blob SHA: `f78ab3ee0fe2fdd403fa64ed86b674241ccfe97c` — exact byte match
- renderer: repository PDF render pipeline at 180 dpi
- visual disposition: PASS on 5/5 pages
- leakage scan: PASS
- structural preflight: PASS

The former one-page preview is replaced by this integrated source-grounded student pack. Full teacher diagnostics, expanded practice and metadata remain separate repository artifacts rather than being leaked into the student PDF.

## Static completion state

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This means source, mathematics, pedagogy structure, metadata, student-export hygiene and static render QA are complete. It does **not** claim classroom validation, longitudinal retention, psychometric calibration, qualification probability or publication approval.
