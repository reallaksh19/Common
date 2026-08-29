# Greatest / Least Integer Functions — NMTC Bhaskara Preliminary

## Status

`INTERNAL_PACKAGE_COMPLETE_NOT_PUBLICATION_READY`

`SECOND_MATH_EDITORIAL_PASS: PASS`

## Why this unit exists

Greatest Integer / Least Integer functions are an explicit Junior syllabus obligation even though the currently qualified 2018/2019/2023/2024/2025 Preliminary corpus does not show a stable direct recurrence family.

This package is therefore **syllabus-first**.

Performance spine:

`IDENTIFY FLOOR/CEILING -> TRANSLATE TO INTERVAL -> PRESERVE OPEN/CLOSED ENDPOINTS -> SOLVE -> FILTER INTEGER/DOMAIN CASES -> CHECK BOUNDARIES -> TRANSFER`

## Core definitions

For real `x`:

- `floor(x)` is the greatest integer `<=x`;
- `ceil(x)` is the least integer `>=x`.

Master translations for integer `m`:

`floor(x)=m <=> m<=x<m+1`

`ceil(x)=m <=> m-1<x<=m`.

## Connected coverage

- definitions and step-interval grammar;
- negative inputs and truncation falsifier;
- integer shifts;
- `ceil(x)=-floor(-x)` reflection;
- fractional part `x-floor(x)` including negative values;
- floor/ceiling equations and inequalities;
- `x` coupled to `floor(x)` via `n=floor(x)`;
- nested/idempotent forms;
- floor-sum bounds and fractional-part case splits;
- integer counting in real intervals;
- square-root and quotient/grouping bridges;
- source-QC distinction between primary mechanism and incidental final floor operation.

## Evidence boundary

The five-year recurrence authority classifies Greatest/Least Integer functions as `P2 coverage risk`: explicit syllabus, weak/absent current five-year evidence. No historical frequency is fabricated.

`NMTC-BH-P-2024-Q27` is retained only as **bridge evidence** because its qualified GP solution ends with a floor operation; the primary mechanism is infinite GP, not a Greatest Integer Function problem.

## Internal assets

- concept spec + source coverage map + student draft;
- 14 First-Step cards;
- 10 mechanism ladders;
- 18 reviewed author-created transfer items;
- 20 recognition items;
- 12 first-line items;
- 12-question unlabelled mixed mastery test;
- second math/editorial audit;
- QA `PASS_INTERNAL` / internal-complete promotion.

## Publication-stage blockers

- classroom timing/readability calibration;
- final student/teacher output separation;
- production-bank machine-readable metadata;
- final typography/equation/render QA;
- global 2022 source recovery may alter historical evidence status.
