# NMTC Bhaskara Preliminary — Cross-Package Publication Readiness Matrix v1

## Purpose

This matrix separates **mathematical/internal completeness** from **publication readiness** across the ten topic packages and the mixed mock system.

A package can be mathematically complete while still being blocked from student publication by timing, artifact separation, metadata, rendering, or source-figure custody.

## Status vocabulary

- `PASS_INTERNAL` — mathematical/editorial package QA passed.
- `PASS_STATIC` — a static source/editorial check was completed without requiring student trials.
- `PARTIAL` — useful structure exists but the publication gate is not fully closed.
- `NOT_RUN` — the gate requires work/evidence that has not yet been executed.
- `BLOCKED_SOURCE` — cannot be closed without source recovery.
- `N/A` — gate does not apply.

## Current matrix

| Package / system | Internal math/editorial QA | Student/teacher production split | Machine-readable item metadata | Static notation/source QA | Classroom timing/readability | Render/PDF QA | Historical figure custody | Publication state |
|---|---|---|---|---|---|---|---|---|
| P0-1 Polynomial & Root Structure | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-2 Radicals / Exponents / Logs | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-3 Inequalities / Bounds | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-4 Modular / Divisibility / Digits | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-5 Circle / Tangent | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `BLOCKED_SOURCE` for exact historical figures | `NOT_READY` |
| P1-1 Sequence & Series Preliminary | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P1-2 Combinatorics | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | historical figure-gated items remain non-canonical | `NOT_READY` |
| P1-3 Triangle Metric / Apollonius / Stewart | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | source-conflicted/figure-dependent historical anchors remain gated | `NOT_READY` |
| P2-1 Mathematical Induction | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P2-2 Greatest / Least Integer Functions | `PASS_INTERNAL` | `PARTIAL` | `NOT_RUN` | `PASS_STATIC` for current author-created package | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| Mixed Mock System A/B/C | `PASS_INTERNAL` | `PASS_STATIC` — student paper/key physically separated | `PASS_STATIC` for v1 mock ledger once `Mock_Item_Metadata_v1.csv` is present | `PASS_STATIC` source/editorial; rendering still pending | `NOT_RUN` | `NOT_RUN` | `N/A` — all v1 questions are author-created and text-complete | `NOT_READY` |

## Why `PARTIAL` is used for topic student/teacher split

The topic architecture already separates student drafts, first-step references, transfer banks, mastery tests and QA files. That is sufficient for authoring, but it is **not yet a frozen production manifest** proving that no answer, teacher cue, provenance note, or diagnostic tag leaks into a student export.

The production split must therefore be governed by a separate manifest before publication.

## Static checks that are already legitimate

The following can be closed without classroom data:

1. provenance labels;
2. answer/key consistency;
3. source-conflict visibility;
4. no fake official attribution;
5. notation conventions at source level;
6. student/teacher file-role separation;
7. machine-readable metadata completeness;
8. deterministic question IDs;
9. mock domain/package allocation;
10. answer-vector consistency.

## Gates that cannot be inferred from desk review

The following must remain `NOT_RUN` until evidence exists:

- actual recognition time;
- actual solve time;
- student misunderstanding rate;
- reading-load problems;
- whether a page layout causes missed information;
- percentile/pass thresholds;
- qualification probability;
- psychometric difficulty/discrimination.

## Global source blockers

### 2022

`2022 = BLOCKED_SOURCE_RECOVERY`.

No six-year recurrence or six-year weighting claim is permitted until the actual 54th NMTC 2022 Bhaskara Preliminary source is recovered and qualified.

### Historical geometry figures

A recovered solution or answer does not establish custody of an original figure. Exact historical figure-dependent anchors remain non-canonical until the original figure is retained and checked.

## Promotion rule

No row may become `NMTC_PRELIMINARY_PUBLISHED` solely because `PASS_INTERNAL` exists.

Minimum publication path:

`PASS_INTERNAL -> production split -> metadata -> static notation/source QA -> classroom timing/readability evidence -> render/PDF QA -> source blockers resolved where applicable -> publication decision`

## Current aggregate verdict

```text
TOPIC_PACKAGES_INTERNAL_COMPLETE = 10/10
MIXED_MOCK_SYSTEM_INTERNAL_COMPLETE = YES
CLASSROOM_TIMING_CALIBRATION = NOT_RUN
PRODUCTION_RENDER_QA = NOT_RUN
2022_RECOVERY = BLOCKED_SOURCE
FINAL_PUBLICATION = NOT_READY
```
