# P1 Geometry — Triangle Metric QA

## Package

`Triangle Metric Recognition — Apollonius / Stewart / mixed triangle geometry`

## Gate result

`PASS_INTERNAL`

Overall status:

`INTERNAL_PACKAGE_COMPLETE_NOT_PUBLICATION_READY`

## Gate audit

| Gate | Result | Evidence |
|---|---|---|
| concept structure derived, not formula-only | PASS | Stewart derived from Pythagorean elimination; Apollonius derived as median specialization |
| segment-type recognition explicit | PASS | median / altitude / angle bisector / general cevian contrast |
| clean PYQ mechanism grounding | PASS | 2018 Q23, 2019 Q02, 2025 Q06; 2024 Q19 bridge |
| source-conflict separation | PASS | 2023 Q02 retained only as `SOURCE_CONFLICT_EVIDENCE` |
| Stewart label discipline | PASS | explicit `BD=m,DC=n,AB=c,AC=b` mapping in concept/student/assessment layers |
| angle-bisector integration | PASS | ratio first, Stewart second; standard length relation derived |
| method-choice contrast | PASS | theorem vs coordinates/vectors vs Pythagorean subtraction vs cosine law |
| author-created transfer separation | PASS | 18 transfer items carry no fake historical IDs |
| recognition lab | PASS | 20 prompts |
| first-line lab | PASS | 12 prompts |
| mixed mastery | PASS | 12 unlabeled questions + diagnostic tags |
| numerical answer review | PASS | second arithmetic pass completed; authored C3 header mismatch corrected before promotion |
| figure/source custody | PASS_INTERNAL | package uses text-complete author-created items; exact historical figure publication remains separately gated |

## Mathematical audit points

Second pass explicitly checked:

- altitude subtraction sign/orientation;
- Apollonius coefficient `a^2/2` / equivalent median formula;
- Stewart side-square/base-segment pairing;
- angle-bisector split direction and `d^2=bc-mn`;
- right-triangle `h=2R` and `r=(p+q-h)/2`;
- coordinate midpoint distances;
- mastery Q7 rational Stewart result `234/5`;
- transfer C3 corrected result `272/7`.

## Historical source boundaries

- 2019 Q02: clean mechanism anchor.
- 2018 Q23: clean altitude-cancellation anchor.
- 2025 Q06: clean right-triangle radius bridge.
- 2023 Q02: source conflict; cannot be a canonical worked exercise.
- figure-dependent items elsewhere remain gated until exact figure custody.

## Remaining publication blockers

1. classroom/readability timing calibration;
2. final student/teacher split;
3. production-bank machine-readable metadata;
4. final typography/equation/render QA;
5. exact source-figure ingestion for any historical figure-based anchor promoted into final pages.

## Next content target

Mathematical Induction, then Greatest/Least Integer functions, followed by mixed Preliminary synthesis/mocks.
