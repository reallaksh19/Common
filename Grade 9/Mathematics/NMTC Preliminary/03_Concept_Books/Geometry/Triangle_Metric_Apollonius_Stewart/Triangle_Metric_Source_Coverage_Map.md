# Triangle Metric Recognition — PYQ Source Coverage Map v1

## Purpose

Map triangle-metric teaching mechanisms to the qualified Bhaskara Preliminary corpus without fabricating source diagrams or repairing conflicts.

## Evidence vocabulary

- `CLEAN_SCORED_ANCHOR`
- `BRIDGE_EVIDENCE`
- `SOURCE_CONFLICT_EVIDENCE`
- `FIGURE_GATED`
- `SYLLABUS_REQUIRED_AUTHOR_CREATED_CORE`

## Coverage table

| Mechanism | PYQ | Role | First move / invariant |
|---|---|---|---|
| median metric / Apollonius | `NMTC-BH-P-2019-Q02` | `CLEAN_SCORED_ANCHOR` | translate the two medians metrically; Apollonius/vector elimination before angle work |
| altitude-square cancellation | `NMTC-BH-P-2018-Q23` | `CLEAN_SCORED_ANCHOR` | subtract two Pythagorean equations so the altitude cancels |
| right-triangle `R:r` bridge | `NMTC-BH-P-2025-Q06` | `CLEAN_SCORED_ANCHOR` | use hypotenuse `=2R` and `r=(a+c-b)/2` before half-angle ratios |
| triangle side/trig ratio | `NMTC-BH-P-2024-Q19` | `BRIDGE_EVIDENCE` | convert tangent conditions to side/sine-cosine relations before solving angles |
| incenter angle relation | `NMTC-BH-P-2018-Q14` | `BRIDGE_EVIDENCE` | identify incenter structure before angle chase |
| median / Apollonius route with inconsistent source | `NMTC-BH-P-2023-Q02` | `SOURCE_CONFLICT_EVIDENCE` | supplied solution uses Apollonius first, but source side data conflict with the asserted angle |

## Syllabus-required mechanisms without clean direct five-year anchor

### Stewart theorem

Status: `SYLLABUS_REQUIRED_AUTHOR_CREATED_CORE`.

Teach as the general cevian metric identity:

`b^2m+c^2n=a(d^2+mn)`.

Use complete author-created diagrams/problems. Do not invent an NMTC year/question number.

### Angle-bisector length via Stewart

Status: `SYLLABUS_REQUIRED_AUTHOR_CREATED_CORE`.

Use angle-bisector ratio `m/n=c/b`, then Stewart. Derive the standard length relation rather than presenting it naked.

### Median theorem / Apollonius reconstruction

Clean support exists through 2019 Q02, but the concept derivation should still be author-created and diagram-complete.

## Source-QC case: 2023 Q02

The qualified record says the supplied solution starts with Apollonius and obtains `AD=7`, but the stated side lengths themselves do not support the supplied downstream angle claim. Therefore:

1. retain the item as evidence that Apollonius is a relevant Preliminary first move;
2. do not publish the recovered stem as a clean worked example;
3. do not adjust a side length/angle silently to reconcile the solution;
4. use an author-created structurally similar problem for teaching.

## Publication implication

The theorem network is authorable now. Exact historical geometry reproduction remains separately figure/source-gated where necessary.
