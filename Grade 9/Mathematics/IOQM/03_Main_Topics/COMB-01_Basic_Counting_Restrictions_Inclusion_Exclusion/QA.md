# COMB-01 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This QA record applies to the canonical counting/model provider, seven separate microstream interfaces, frozen-schema metadata, integrated learner sources and the exact committed PDF blobs below.

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | seven required historical anchors retain frozen corpus paper/key custody and independently verified answers |
| G1 governing model | PASS_STATIC | `DEFINE OBJECT -> IDENTITY/ORDER -> RESTRICTIONS -> CASES/STAGES -> DIRECT/COMPLEMENT/IE -> COUNT -> CHECK` |
| G2 canonical ownership | PASS_STATIC | owns basic counting/restrictions/IE; recurrence, graph coloring and arithmetic digit-rule derivation remain with their canonical owners |
| G3 counted-object / exact-one discipline | PASS_STATIC | learner book and provider interface explicitly define identity, disjointness, exhaustiveness and stage semantics before formulas |
| G4 per-microstream interfaces | PASS | seven W1-A through W1-G files satisfy mandatory filename/header/A-P schema; consolidated file is index-only |
| G5 stable downstream provider interface | PASS | `COMB01_Stable_Counting_Model_Interface_v1.md` exports C01-1 through C01-10 and passes T1 through T6 for COMB-03 retrieval |
| G6 permutation/combination derivation | PASS_STATIC | ordered selections precede combination formula; unordered counts remove the exact order overcount |
| G7 repeated-object identity | PASS_STATIC | multiset formula is derived from labelled overcount and gated on genuine indistinguishability |
| G8 restrictions / complement / IE | PASS_STATIC | position-first restrictions, complement-universe matching and overlap correction are integrated and contrasted |
| G9 digit-string boundary | PASS_STATIC | counts admissible digit strings once arithmetic restrictions are known; digit-rule derivation is routed out |
| G10 attempt-before-help / fading | PASS_STATIC | learner support uses descriptive Full/Medium/Light/Independent language; H-level controls remain teacher/authoring-only |
| G11 practice ladder | PASS | 30 authored items spanning foundation through preliminary-style transfer; key independently recomputed |
| G12 independent mixed mastery | PASS | 16 learner-unlabelled items; exact student inventory 1-16 |
| G13 frozen metadata | PASS | 31-column schema; 53 data rows = 7 historical + 30 practice + 16 mastery; no malformed-width rows |
| G14 independent mathematics | PASS | repository verification authority plus `Authoring/Independent_Mathematics_Audit.md`; all seven anchor answers and authored key values checked |
| G15 student-export hygiene | PASS | exact student PDF contains no H0-H3, T2-T4, Wave/PR/Issue or internal COMB/NT topic control codes |
| G16 durable render authority | PASS | `Authoring/render_comb01_pdfs.py` deterministically renders student and teacher artifacts from canonical Markdown |
| G17 exact render QA | PASS | student 10/10 and teacher 3/3 pages rasterized with safe bounds; no footer-only student pages; inventories intact; PDFs openable, unencrypted and form-free |
| classroom timing/readability | NOT_RUN | evidence-dependent |
| longitudinal retention/transfer | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent |

## Historical anchor closure

- `IOQM-2025-Q05 = 45` — bounded digit-pair count.
- `IOQM-2025-Q15 = 40` — restricted injection of three coupon-pairs; IE check `120-120+48-8`.
- `IOQM-2025-Q18 = 40` — exact multiset/relative-order count `540`, requested remainder mod 100.
- `IOQM-2024-Q02 = 12` — restricted units digit then `3!`.
- `IOQM-2023-Q07 = 48` — fix opposite 1/2 axis, six cyclic label orders and eight opposite-pair colourings.
- `IOQM-2023-Q17 = 66` — verified order-statistic symmetry route.
- `IOQM-2023-Q20 = 43` — verified cardinality/maximum factorization plus binomial counts.

## COMB-03 provider acceptance

`Authoring/COMB01_Stable_Counting_Model_Interface_v1.md` provides:
- C01-1 counted-object definition;
- C01-2 disjoint addition semantics;
- C01-3 sequential multiplication semantics;
- C01-4 exhaustive/exact-one branch discipline;
- C01-5 ordered/unordered structural decision;
- C01-6 direct/complement cue;
- C01-7 restriction/state-memory vocabulary;
- C01-8 fail-closed overlap/inclusion-exclusion boundary;
- C01-9 repeated-object identity rule;
- C01-10 digit-string counting boundary.

Compatibility tests T1-T6 are explicitly PASS in the provider artifact, including the exact downstream question `Does every valid object enter exactly one branch?`.

## Current student PDF custody

- path: `PDFs/COMB01_Student_Pack_v1.pdf`
- page size: A4, 595.276 x 841.89 pt
- page count: **10**
- file size: **61,967 bytes**
- Git blob SHA: **`503a24b1cca77017a2c9a55b3f1f72ca3dc6010d`**
- SHA-256: **`d81b291834ebb0388f4db6dcd5bdca7e97f44c3b3d3a55d2af64319ff69b304b`**
- encrypted: **no**
- forms/XFA: **none**
- forbidden learner-control scan: **NONE**
- Practice inventory: **1-30**
- Independent Mastery inventory: **1-16**
- raster page count: **10**
- raster bounds: **PASS**
- substantive extracted text per page after footer removal: **PASS**; minimum count 74, no footer-only page

## Current teacher PDF custody

- path: `PDFs/COMB01_Teacher_Key_v1.pdf`
- page size: A4, 595.276 x 841.89 pt
- page count: **3**
- file size: **47,882 bytes**
- Git blob SHA: **`d33a84cc0a24668782f744c51a1f1e1a16c328b1`**
- SHA-256: **`85d5463cd938d2a85654fd50e80aa3c383443f40bfade630296a725f3192b8bc`**
- encrypted: **no**
- forms/XFA: **none**
- raster bounds: **PASS**

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

This is a static benchmark/readiness claim only. Classroom calibration, retention evidence, psychometric validation, publication approval and qualification probability remain `NOT_RUN`.
