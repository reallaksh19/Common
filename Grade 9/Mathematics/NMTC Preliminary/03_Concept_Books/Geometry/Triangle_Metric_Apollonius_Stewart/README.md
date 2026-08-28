# Triangle Metric Recognition — Apollonius, Stewart & Mixed Triangle Geometry

## Why this unit exists

NMTC Preliminary triangle problems are often not long proof problems. They are short metric chains where the decisive step is recognizing which segment relation makes an unknown disappear.

Performance spine:

`SEE TRIANGLE -> CLASSIFY THE SPECIAL SEGMENT -> WRITE THE CHEAPEST METRIC RELATION -> CANCEL/REDUCE -> CHECK -> TRANSFER`

## Student mastery target

The learner can:

1. distinguish a median, altitude, angle bisector and general cevian;
2. reconstruct Apollonius from Stewart rather than memorize both as unrelated formulas;
3. use Stewart on a general cevian with correct side/segment labels;
4. subtract Pythagorean equations to eliminate a shared altitude;
5. combine the angle-bisector theorem with Stewart when a bisector length is involved;
6. use right-triangle circumradius/inradius relations as compact metric bridges;
7. recognize when coordinates/vectors are shorter than theorem expansion;
8. refuse to canonicalize a figure-dependent/source-conflicted PYQ without exact geometry custody.

## Core invariant network

For triangle `ABC`, let `D` lie on `BC`, with

- `BD=m`, `DC=n`, `BC=a=m+n`;
- `AB=c`, `AC=b`;
- `AD=d`.

Then Stewart gives

`b^2 m + c^2 n = a(d^2 + mn)`.

Specializations:

- median: `m=n=a/2` -> Apollonius;
- altitude: two Pythagorean equations can be subtracted directly;
- angle bisector: combine `m/n=c/b` with Stewart.

## Clean/source-useful historical evidence

- `NMTC-BH-P-2019-Q02` — median geometry; Apollonius/vector metric route;
- `NMTC-BH-P-2018-Q23` — altitude-square difference cancellation;
- `NMTC-BH-P-2025-Q06` — right-triangle `R:r` metric bridge;
- `NMTC-BH-P-2024-Q19` — trigonometric/side-ratio triangle bridge.

Source-QC contrast:

- `NMTC-BH-P-2023-Q02` uses an Apollonius-first route in the supplied solution, but the recovered side data and angle claim conflict. It is `SOURCE_CONFLICT_EVIDENCE`, not a canonical student exercise.

## Package products

- `Triangle_Metric_Concept_Book_Spec.md`
- `Triangle_Metric_Source_Coverage_Map.md`
- `Triangle_Metric_Student_Draft_v0.1.md`
- `../../../04_First_Step_Reference/P1_Geometry_Triangle_Metric_First_Step_Cards.md`
- `../../../05_Practice_Ladders/P1_Geometry_Triangle_Metric_Ladder.md`
- `../../../06_Speed_Labs/P1_Geometry_Triangle_Metric_Recognition_Lab_v1.md`
- `../../../06_Speed_Labs/P1_Geometry_Triangle_Metric_First_Line_Lab_v1.md`
- `../../../07_Mastery_Banks/P1_Geometry_Triangle_Metric_Transfer_Bank_v1.md`
- `../../../08_Mixed_Preliminary_Tests/P1_Geometry_Triangle_Metric_Mastery_Test_v1.md`
- `../../../09_QA/P1_Geometry_Triangle_Metric_QA.md`

## Source boundary

Theorems may be taught from complete author-created diagrams/text. Historical figure-dependent items remain gated until exact source figures are retained. A known answer or solution prose is not figure custody.

## Current state

`STATUS: PACKAGE_AUTHORING`
