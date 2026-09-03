---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-F
microstream_title: Chords, secants and metric circle structure
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-F — Chords, Secants and Metric Circle Structure

## A. Scope boundary
Included: perpendicular from centre bisects chord, equal chords/equal distances from centre, chord-length via radius-distance, intersecting chord/secant metric routes, and deciding synthetic vs coordinate metric representation. Excluded: full coordinate-circle canon, mensuration and advanced chord loci.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: Pythagoras, midpoint, radius.
LIKELY_HALF_KNOWLEDGE: treats every chord problem as an angle theorem or writes circle equations immediately.
MISSING_BRIDGES: chord length is controlled by radius and perpendicular distance from centre; symmetry can make metric calculation one-dimensional.
OWNERSHIP_TARGET: CHORD + CENTRE -> PERPENDICULAR/MIDPOINT -> RIGHT TRIANGLE OR POWER -> LENGTH.
```

## C. Mathematical invariant / governing structure
The perpendicular from the centre to a chord bisects the chord. If circle radius is `R` and chord is distance `d` from centre, chord length is `2 sqrt(R^2-d^2)`. Equal chords are equidistant from centre and conversely.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| centre-perpendicular | half-chord right triangle | drop perpendicular | centre known | angle chase |
| symmetry axis | one coordinate | place symmetric chord horizontally | symmetry proved | arbitrary coordinate algebra |
| power/secant | product lengths | use W1-E | common point product visible | chord-distance formula |
| circle equation | metric fallback | choose symmetric coordinates | alternate route shorter | default analytic method |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| centre + chord length | right triangle | angle theorem | is radius/distance data available? | circle suggests angles |
| isosceles triangle circumcircle | symmetry coordinates/centre | general circle equation | is there an axis? | formula appears rigorous |
| two secants | power | chord-distance | do lines share an external point? | both are metric |
| parallel chord through midpoint | centre-distance | similarity only | can symmetry locate centre/chord level cheaply? | triangle surface |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: GEO04-CHD-01
WRONG_MOVE: assume a radius to a chord endpoint bisects the chord.
WHY_TEMPTING: all radii are equal.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: it is the perpendicular from the centre to the chord that bisects it.
FALSIFIER_OR_CONTRAST: oblique radius to endpoint.

ERROR_CODE: GEO04-CHD-02
WRONG_MOVE: use chord formula with distance measured from a non-centre point.
WHY_TEMPTING: a convenient midpoint is mistaken for centre.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: identify the actual centre and perpendicular distance.
FALSIFIER_OR_CONTRAST: off-centre point.
```

## G. First-move cues
- centre and chord -> drop perpendicular and halve chord.
- isosceles/circle symmetry -> place centre on symmetry axis.
- chord through a known midpoint parallel to base -> compute its height relative to centre.
- secants through one point -> route to W1-E.

## H. H3 -> H0 fading plan
H3: perpendicular/half-chord marked. H2: cue “centre to chord.” H1: provide centre/chord data only. H0: changed circumcircle configuration where learner chooses symmetric coordinates or right-triangle metric route.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q17 | 2024/Q17 | CLEAN_OFFICIAL | primary | circumcircle chord through midpoint parallel base | source figure/custody pending | 25 independently verified |
| IOQM-2023-Q15 | 2023/Q15 | CLEAN_VALIDATED | bridge | circumcentres in a square | text/geometry surface | 03 independently verified |

## J. Source-independent mathematical trace
Q17: symmetric coordinates give height `5sqrt7`, circumcentre `-5/sqrt7` on axis, `R²=1600/7`; chord at midpoint level has half-length `25/2`, so `PQ=25`. Q15: unit-square coordinates plus triangle-perimeter relation reduce the circumcentre-distance ratio to `OP²/OA²=1/2`, hence answer 03. Full algebra is independently audited.

## K. Contrast-pair candidates
1. radius to endpoint vs perpendicular to chord;
2. angle route vs metric chord route;
3. symmetric coordinates vs general circle equation;
4. chord-distance vs power product;
5. equal chords vs equal arcs/angles;
6. synthetic metric vs GEO-05 alternate representation.

## L. Transfer candidates
T2 chord at fixed distance; T2 equal-chord comparison; T3 integer chord/radius condition; T4 isosceles-triangle circumcircle solved synthetically then checked by coordinates.

## M. Candidate mastery items
Recognition: centre-chord first move. First-line: draw perpendicular and half-chord. Full solve: chord length from radius/distance. WHY-NOT: reject wrong bisector radius. Verification: compare synthetic and coordinate answers.

## N. Dependency declarations
`REQUIRES`: GEO-02 perpendicular/Pythagorean core; W1-E if secant products used.  
`BRIDGE_REQUIRES`: GEO-05 coordinates only as alternate/check.  
Downstream may assume chord metric problems begin with centre-perpendicular structure.

## O. Lead integration notes
Place after angle/cyclicity/tangency so learners learn to select metric vs angle routes. Q17 is a strong method-selection anchor; avoid turning it into a coordinate lesson.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: HBCSE page-image custody pending for Q17; classroom calibration NOT_RUN
```
