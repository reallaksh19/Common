# Greatest / Least Integer Functions — NMTC Bhaskara Preliminary

## Why this unit exists

Greatest Integer / Least Integer functions are an explicit Junior syllabus obligation even though the currently qualified 2018/2019/2023/2024/2025 Preliminary corpus does not show a stable direct recurrence family.

This package is therefore **syllabus-first**.

Performance spine:

`IDENTIFY FLOOR/CEILING -> TRANSLATE TO INTERVAL -> PRESERVE OPEN/CLOSED ENDPOINTS -> SOLVE -> FILTER INTEGER/DOMAIN CASES -> CHECK BOUNDARIES -> TRANSFER`

## Core definitions

For real `x`:

- `floor(x)` is the greatest integer `<= x`;
- `ceil(x)` is the least integer `>= x`.

The two most important translations are:

`floor(x)=m  <=>  m <= x < m+1`

`ceil(x)=m   <=>  m-1 < x <= m`

for integer `m`.

## Student mastery target

The learner can:

1. convert floor/ceiling equations into half-open intervals;
2. handle negative inputs without truncation errors;
3. use `ceil(x)=-floor(-x)`;
4. work with fractional part `{x}=x-floor(x)`;
5. solve floor/ceiling equations and inequalities;
6. count integers in real intervals;
7. analyze nested and shifted floor/ceiling expressions;
8. use boundary points correctly;
9. distinguish identities from case-dependent statements;
10. recognize when floor/ceiling is only a final bridge inside another topic rather than the primary mechanism.

## Evidence boundary

The five-year recurrence authority classifies Greatest/Least Integer functions as `P2 coverage risk`: explicit syllabus, weak/absent current five-year evidence. No historical frequency is fabricated.

`NMTC-BH-P-2024-Q27` is retained only as **bridge evidence** because its qualified GP solution ends with a floor operation; the primary mechanism is infinite GP, not a Greatest Integer Function problem.

## Package products

- `Greatest_Least_Integer_Concept_Book_Spec.md`
- `Greatest_Least_Integer_Source_Coverage_Map.md`
- `Greatest_Least_Integer_Student_Draft_v0.1.md`
- `../../../04_First_Step_Reference/P2_Greatest_Least_Integer_First_Step_Cards.md`
- `../../../05_Practice_Ladders/P2_Greatest_Least_Integer_Ladder.md`
- `../../../06_Speed_Labs/P2_Greatest_Least_Integer_Recognition_Lab_v1.md`
- `../../../06_Speed_Labs/P2_Greatest_Least_Integer_First_Line_Lab_v1.md`
- `../../../07_Mastery_Banks/P2_Greatest_Least_Integer_Transfer_Bank_v1.md`
- `../../../08_Mixed_Preliminary_Tests/P2_Greatest_Least_Integer_Mastery_Test_v1.md`
- `../../../09_QA/P2_Greatest_Least_Integer_QA.md`

## Current state

`STATUS: PACKAGE_AUTHORING`
