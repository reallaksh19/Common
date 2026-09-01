# ALG-04 — QA

Status: `STATIC_SOURCE_REPAIRED__RENDER_REVALIDATION_REQUIRED`

This QA state supersedes older benchmark-ready claims after remediation of the independent review findings. Current-source claims and current-PDF claims are kept separate.

## Gate table

| Gate | State | Evidence |
|---|---|---|
| Wave 0 concept/dependency map | PASS | scope, owner boundary, representations, misconceptions and transfer endpoints remain coherent |
| canonical router | PASS | `TERM/SUM -> EXPLICIT/RECURRENT -> LOCAL/GLOBAL -> NEARBY SUBTRACTION -> TELESCOPE -> COMPUTE` |
| source anchors | PASS | canonical stable IDs `IOQM-2025-Q26`, `IOQM-2023-Q10` |
| anchor key/source join | PASS | Q26=10; Q10=51 with canonical ledger custody |
| independent mathematical audit | PASS_STATIC_SECOND_ROUTE | prior independent recomputation remains valid for unchanged historical anchors |
| recurrence interface | PASS_STABLE | notation, initialization, verification and local cancellation interface unchanged |
| per-microstream schema | PASS_STATIC_REPAIRED | seven `IOQM-G9-ALG-04__W1-*__*__interface.md` files now follow the mandatory naming/header/A-P contract |
| canonical overlap ownership | PASS_REPAIRED | authored Practice #14 and mastery #9 now stop at the recurrence invariant result; divisor-count doctrine is no longer required before NT-03 |
| attempt before support | PASS_STATIC | learner text requests independent attempt before optional support |
| support fading | PASS_STATIC_REPAIRED | learner-facing support uses descriptive labels rather than H-level control codes |
| term vs sum contrast | PASS_STATIC | concept, lab, practice and mastery |
| AP vs GP contrast | PASS_STATIC | includes `neither` boundary |
| explicit vs recurrence contrast | PASS_STATIC | includes initialization and verification |
| compute-many vs nearby subtraction | PASS_STATIC | windows, first differences and invariant |
| algebraic vs counting recurrence | PASS_STATIC | supplied recurrence use separated from counting-model derivation |
| integrated First-Step Reference | PASS_STATIC | one topic-wide router/reference |
| changed-surface transfer | PASS_STATIC_REPAIRED | learner-facing transfer items no longer expose T2/T3/T4 control labels |
| mastery | PASS_STATIC_REPAIRED | learner-facing title is `Independent Mixed Mastery Check`; H0 remains only in metadata/teacher control |
| teacher diagnostic key | PASS_STATIC_REPAIRED | Practice #14 and mastery #9 keys now end at `D_20=7^19`; no NT-03 divisor-count theorem required |
| item metadata | PASS_STATIC_REPAIRED | migrated from custom 16-column format to frozen 31-column schema; historical rows use canonical stable IDs and exact source/key authority fields |
| student-source scrub | PASS_STATIC_REPAIRED | H/T control labels removed from repaired practice/mastery learner prose |
| repository PDF custody | STALE_AFTER_SOURCE_CHANGE | existing 5-page PDF predates the repaired practice/mastery sources |
| PDF structural preflight | NOT_RUN_CURRENT_SOURCE | regenerate from current sources first |
| PDF page-by-page visual QA | NOT_RUN_CURRENT_SOURCE | independent current-blob inspection required after regeneration |
| classroom timing/readability | NOT_RUN | evidence-dependent |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent |
| publication approval | NOT_RUN | separate decision |

## Dependency repair

The historical `IOQM-2023-Q10` remains a legitimate cross-domain source anchor and keeps its official divisor-count finish in source custody. However, new ALG-04 Practice #14 and learner mastery #9 now ask only for the recurrence invariant endpoint `D_20=7^19`. The prime-power divisor-count rule is explicitly deferred to canonical owner `IOQM-G9-NT-03`.

## Metadata repair

`Item_Metadata.csv` now follows the exact 31-column header from `IOQM_G9_Question_Metadata_Schema_v1.csv`.

Historical rows are keyed directly by:
- `IOQM-2025-Q26` with `HBCSE_OFFICIAL` / `FINAL_OFFICIAL` and canonical paper/key URLs;
- `IOQM-2023-Q10` with `HBCSE_LINKED_MTAI` / `HBCSE_LINKED_MTAI_EMBEDDED_KEY` and canonical source URL.

Local `ALG04-PYQ-*` aliases are no longer used as historical item IDs.

## Per-microstream interfaces

Current required authoring interfaces:
- `Authoring/IOQM-G9-ALG-04__W1-A__ap-gp-recognition__interface.md`
- `Authoring/IOQM-G9-ALG-04__W1-B__term-vs-sum__interface.md`
- `Authoring/IOQM-G9-ALG-04__W1-C__recurrence-reading__interface.md`
- `Authoring/IOQM-G9-ALG-04__W1-D__window-differences__interface.md`
- `Authoring/IOQM-G9-ALG-04__W1-E__telescoping__interface.md`
- `Authoring/IOQM-G9-ALG-04__W1-F__recurrence-invariants__interface.md`
- `Authoring/IOQM-G9-ALG-04__W1-G__source-pyq-audit__interface.md`

The former consolidated file is retained only as synopsis evidence and is not used to claim schema conformance.

## Historical anchor audit

### IOQM-2025-Q26
Adjacent 4-term and 7-term windows reduce to shifted term inequalities; the independently checked result remains `10`.

### IOQM-2023-Q10
The Cassini-type target satisfies a geometric recurrence; the historical source finish gives divisor count `51`. This source fact does not license teaching the divisor-count theorem inside newly authored ALG-04 items.

## Render custody

The committed `PDFs/ALG04_Student_Pack_v1.pdf` and its old 5-page hash/visual inspection apply to the pre-remediation source state. They must not certify the repaired learner artifacts.

Before promotion:
1. regenerate the student PDF from current canonical sources;
2. record the new Git blob SHA and SHA-256;
3. run structural/leakage preflight;
4. independently inspect every page of the exact current blob;
5. only then restore render PASS claims.

## Current promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE_REPAIRED
WAVE2_INTEGRATED_ASSIMILATION_SOURCE_REPAIRED
WAVE3_FIRST_STEP_PASS
WAVE4_MASTERY_SOURCE_PASS
WAVE5_STATIC_SOURCE_QA_PASS
WAVE6_CURRENT_RENDER_QA_NOT_RUN
NOT_READY__RENDER_REVALIDATION_REQUIRED
```

Classroom timing/readability, retention, psychometrics, qualification probability, percentile/pass-mark calibration and publication approval remain `NOT_RUN`.
