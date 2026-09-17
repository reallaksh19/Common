# GEO-01 Topic-Lead Integration Map

Status: `INTERFACES_COMPLETE_READY_FOR_INTEGRATED_PROSE_PAGE_IMAGE_CUSTODY_PENDING`

## Learner promise
The learner should classify the geometric object before selecting a formula:

`CHECK FEASIBILITY -> CLASSIFY SEGMENT/CONSTRAINT -> RETRIEVE CHEAPEST VALID RELATION -> APPLY METRIC/DISCRETE FILTER -> CHECK ORIGINAL`.

## Integrated order
1. **Triangle feasibility first** — strict triangle inequality and the interval `|p-q|<d<p+q`; reject impossible geometry before calculation.
2. **Right/acute/obtuse by side squares** — sort sides, verify feasibility, compare `c^2` with `a^2+b^2`; use extremal monotonicity for “every triple” problems.
3. **Classify special cevians** — median, altitude, angle bisector, arbitrary cevian; properties come only from stated/proved data.
4. **Median / Apollonius** — midpoint symmetry gives the special metric identity; retrieve centroid `2:1` only from GEO-03 if needed.
5. **Angle-bisector side ratio** — derive from area ratios; emphasize “bisects the angle, not the opposite side.”
6. **Stewart as the general fallback** — use only when similarity or a special cevian relation is not cheaper.
7. **Right-triangle metric structures** — altitude/projection relations and direct Pythagorean equations; do not force Stewart merely because a cevian appears.
8. **Radius bridges** — `Delta=rs`, `Delta=r_a(s-a)`, `Delta=abc/(4R)` and complement variables for reconstruction.
9. **Integer geometry filters** — geometry first, then integer interval/factor-pair filtering; no hidden NT-04 chapter.
10. **Mixed method selection and transfer** — synthetic metric vs GEO-03 ratio/area retrieval vs GEO-05 coordinate alternate.

## Teach once globally
- strict feasibility/degeneracy rule;
- `classify the segment before choosing a relation`;
- visual appearance never proves midpoint/perpendicularity/equal angles;
- continuous geometry precedes integer filtering;
- use the cheapest relation that targets the requested quantity.

## Retrieve, do not reteach
From GEO-03: similarity criteria/correspondence, scale and area-square ratios, shared-altitude/shared-base area ratios, parallel-line transfer, centroid `2:1` and centroid area facts.

From GEO-05: coordinates/vectors only as an alternate/check when they are demonstrably shorter. Do not make coordinates the default method.

From number theory: only elementary integer/factor filtering as a bridge. NT-04 is not assumed frozen.

## Mandatory contrast placements
- feasible triangle vs positive lengths: opening lesson;
- acute/right/obtuse vs infeasible: immediately after square test;
- median vs altitude vs angle bisector: before any cevian formula;
- median/Apollonius vs Stewart: generalization sequence;
- angle-bisector ratio vs midpoint misconception: angle-bisector lesson;
- similarity/area retrieval vs metric theorem: before Stewart;
- continuous metric optimum vs integer admissibility: integer-geometry section;
- synthetic metric vs coordinate alternate: final transfer lab.

## Historical anchor placement
### IOQM-2025-Q04 = 06
Opening feasibility/integer-filter anchor. Equal sides `a`, base `23-2a`; positivity and strict triangle inequality give `a=6..11`.

### IOQM-2025-Q09 = 28
Shared-diagonal feasibility transfer. Convert a quadrilateral surface into two triangle-interval constraints and intersect them.

### IOQM-2024-Q10 = 05
Bridge between algebra and geometry. First collapse the quadratic form into two squares, then apply triangle feasibility to the resulting side ratio; geometry is still a gate after algebra.

### IOQM-2024-Q15 = 92
Acute-triangle extremal anchor. Preserve the exact source phrase allowing choices “not necessarily distinct”; hardest triple is `(n,n,n+38)`, not `(n,n+2,n+38)`.

### IOQM-2024-Q22 = 34
Cevian-classification boundary. `BD:DC=2:1` does not make `AD` a median or angle bisector. The right-triangle metric relation is cheaper than Stewart.

### IOQM-2024-Q27 = 27
Late transfer anchor. Equal angle differences force the local angle structure; pedal feet create cyclic quadrilaterals and an equilateral pedal triangle. Keep advanced point naming optional; behavior first.

### IOQM-2024-Q30 = 25
Right-triangle metric plus integer-filter anchor. Use area/altitude relation, turn the integer perimeter/hypotenuse condition into a difference of squares, then factor.

### IOQM-2023-Q13 = 58
Radius-bridge anchor. Exradii recover semiperimeter complements, then sides `(13,14,15)`; polynomial symmetric sums are a terminal packaging step rather than an imported ALG-03 chapter.

## Recognition Lab targets
- feasibility interval from two known sides;
- largest-side acute/right/obtuse criterion;
- classify median/altitude/bisector/arbitrary cevian from explicit givens;
- decide GEO-03 similarity retrieval vs new metric theorem;
- decide Apollonius vs Stewart;
- choose radius/area bridge;
- detect integer filtering as terminal structure;
- choose synthetic vs coordinate alternate.

## First-Line Lab targets
- `|p-q|<d<p+q`;
- sort and write `c^2 ? a^2+b^2`;
- `BM=CM` only if midpoint established;
- `BD/DC=AB/AC` only if angle bisector established;
- correct Stewart variable map;
- `Delta=rs` or `Delta=r_a(s-a)`;
- write the geometric equation/interval before listing integers.

## F0 -> F4 ladder
- F0: feasibility and direct side-square classification.
- F1: special-cevian recognition with explicit marks.
- F2: Apollonius / angle-bisector / simple right-triangle metric items.
- F3: Stewart, radius bridges, and integer filters with reduced support.
- F4: mixed changed-surface items requiring retrieval vs metric vs coordinate route selection.

## H0 mastery design
First attempt unlabelled/unhinted. Include at least:
- one feasibility interval item;
- one acute/right/obtuse classification or threshold item;
- one cevian-classification item;
- one median/Apollonius item;
- one angle-bisector item;
- one Stewart or arbitrary-cevian item;
- one radius bridge;
- one integer metric filter;
- one WHY-NOT item based on an attractive but unstated diagram property.

## Teacher diagnostic codes
- `FEASIBILITY_SKIPPED`
- `DEGENERATE_EQUALITY_ALLOWED`
- `LARGEST_SIDE_NOT_IDENTIFIED`
- `CEVIAN_MISCLASSIFIED`
- `VISUAL_PROPERTY_ASSUMED`
- `CHEAPER_GEO03_ROUTE_MISSED`
- `STEWART_OVERUSED`
- `ANGLE_BISECTOR_SIDE_MISCONCEPTION`
- `RADIUS_COMPLEMENT_MISMATCH`
- `INTEGER_FILTER_APPLIED_TOO_EARLY`
- `SOURCE_SELECTION_SEMANTICS_LOST`

## Source and publication gates
Historical mathematics: 8/8 PASS. All eight A–P interfaces are complete. The Q15 repeated-choice correction is embedded in the source map, audit, and integration plan. Exact HBCSE page-image/figure custody remains `PENDING` for figure-dependent 2024-Q22,Q27,Q30; this blocks final historical-figure promotion/rendering but not integrated prose authoring. Before ready-for-review: independently checked authored items, frozen metadata, integrated learner materials, teacher key, canonical student/teacher PDFs, hash/blob/page count and page-by-page visual/figure QA. Classroom timing/retention/psychometrics remain `NOT_RUN`.
