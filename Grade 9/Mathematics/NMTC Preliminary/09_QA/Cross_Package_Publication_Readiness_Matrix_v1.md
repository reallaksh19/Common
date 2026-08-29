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

| Package / system | Internal math/editorial QA | Student/teacher source split | Machine-readable item metadata | Static notation/source QA | Classroom timing/readability | Render/PDF QA | Historical figure custody | Publication state |
|---|---|---|---|---|---|---|---|---|
| P0-1 Polynomial & Root Structure | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-2 Radicals / Exponents / Logs | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-3 Inequalities / Bounds | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-4 Modular / Divisibility / Digits | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P0-5 Circle / Tangent | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `BLOCKED_SOURCE` for exact historical figures | `NOT_READY` |
| P1-1 Sequence & Series Preliminary | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P1-2 Combinatorics | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | historical figure-gated items remain non-canonical | `NOT_READY` |
| P1-3 Triangle Metric / Apollonius / Stewart | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | source-conflicted/figure-dependent historical anchors remain gated | `NOT_READY` |
| P2-1 Mathematical Induction | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PARTIAL` | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| P2-2 Greatest / Least Integer Functions | `PASS_INTERNAL` | `PASS_STATIC` manifest frozen; rendered leakage audit pending | `NOT_RUN` | `PASS_STATIC` for current author-created package | `NOT_RUN` | `NOT_RUN` | `N/A` | `NOT_READY` |
| Mixed Mock System A/B/C | `PASS_INTERNAL` | `PASS_STATIC` — student paper/key physically separated | `PASS_STATIC` — 90-row live-key-reconciled ledger | `PASS_STATIC` source/editorial; rendering still pending | `NOT_RUN` | `NOT_RUN` | `N/A` — all v1 questions are author-created and text-complete | `NOT_READY` |

## Topic source split now closed statically

`Topic_Package_Production_Manifests_v1.md` defines the allowed student and teacher projections for all ten packages.

This closes the **semantic/source-level** split:

```text
PACKAGE_MANIFESTS_DEFINED = 10/10
TOPIC_SOURCE_LEVEL_SPLIT = PASS_STATIC
```

It does not yet prove that a rendered student PDF contains no leaked solution/diagnostic material. That remains part of final render QA.

## Mock machine metadata now closed statically

`Mock_Item_Metadata_v1.csv` contains 90 unique author-created item IDs and has been reconciled against the current live A/B/C teacher keys.

`Mock_Item_Metadata_Validation_v1.md` freezes:

- 90 unique rows;
- 30 questions per mock;
- 15 MCQ + 15 numeric per mock;
- 47 Algebra, 18 Geometry, 12 Number Theory, 10 Combinatorics, 3 Arithmetic/Foundation;
- no official-NMTC flags;
- timing status `NOT_RUN` for all items.

## Static checks that are already legitimate

The following can be closed without classroom data:

1. provenance labels;
2. answer/key consistency;
3. source-conflict visibility;
4. no fake official attribution;
5. notation conventions at source level;
6. student/teacher source-role separation;
7. mock machine-readable metadata completeness;
8. deterministic mock question IDs;
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

`PASS_INTERNAL -> source split -> metadata -> static notation/source QA -> classroom timing/readability evidence -> render/PDF QA -> source blockers resolved where applicable -> publication decision`

## Current aggregate verdict

```text
TOPIC_PACKAGES_INTERNAL_COMPLETE = 10/10
MIXED_MOCK_SYSTEM_INTERNAL_COMPLETE = YES
TOPIC_SOURCE_LEVEL_SPLIT = PASS_STATIC
MOCK_MACHINE_METADATA = PASS_STATIC
MOCK_SOURCE_NOTATION_QA = PASS_STATIC
CLASSROOM_TIMING_CALIBRATION = NOT_RUN
PRODUCTION_RENDER_QA = NOT_RUN
TOPIC_MACHINE_METADATA = NOT_RUN
2022_RECOVERY = BLOCKED_SOURCE
FINAL_PUBLICATION = NOT_READY
```
