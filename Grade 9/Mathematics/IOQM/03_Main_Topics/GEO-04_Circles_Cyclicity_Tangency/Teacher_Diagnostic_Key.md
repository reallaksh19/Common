# Teacher Diagnostic Key — Circles, Cyclicity and Tangency

Use this companion to diagnose **representation and theorem-selection errors**, not only final answers.

Core diagnostic codes:

- `CYCLICITY_ASSUMED_FROM_PICTURE`
- `GENERIC_QUAD_RULE_USED`
- `TANGENCY_NOT_PROVED`
- `TANGENT_CHORD_CONFUSED`
- `POWER_POINT_MISMATCH`
- `WRONG_PRODUCT_SEGMENTS`
- `SYNTHETIC_CHAIN_NOT_RECOGNIZED`
- `COORDINATE_OVERKILL`

---

## Recognition and First-Line Lab

1. **C.** Without cyclicity, only the generic quadrilateral angle sum is safe.
2. **A.** Same chord `AB`, same segment -> equal inscribed angles.
3. **B.** A diameter subtends a right angle at the circumference.
4. **B.** Radius to the point of tangency is perpendicular to the tangent.
5. **A.** Tangents from the same external point to the same circle are equal.
6. **B.** Tangent + chord is the direct recognition cue for alternate segment.
7. **B.** The power point is `P`; pair the two pieces on each chord through `P`.
8. **B.** The line of centres is perpendicular to the common chord.
9. First line: `∠A+∠C=180°`, hence `∠C=68°`.
10. Conclude `ABCD` is cyclic by the converse of the opposite-supplementary-angle theorem.
11. First mark `OT` perpendicular to the tangent at `T`; only then translate the tangent-chord angle via alternate segment if useful.
12. `PT^2=PA·PB`.
13. `PA·PB=PC·PD`.
14. Test coordinates when the right/square metric structure gives a low-variable placement and the circle condition becomes one short equation.
15. Missing target: prove cyclicity, for example by a supplementary opposite-angle pair or a valid equal-subtended-angle converse.
16. The line of centres is perpendicular to `AB`; the other stated line is also perpendicular to `AB`, so the two lines are parallel.

Diagnostic emphasis:

- 1,9,10,15 -> `CYCLICITY_ASSUMED_FROM_PICTURE` or `GENERIC_QUAD_RULE_USED`;
- 4,6,11 -> `TANGENCY_NOT_PROVED` / `TANGENT_CHORD_CONFUSED`;
- 7,12,13 -> `POWER_POINT_MISMATCH` / `WRONG_PRODUCT_SEGMENTS`;
- 14,16 -> route-selection diagnosis.

---

## Practice and Transfer Bank

1. `64°`.
2. `76°`.
3. `90°`.
4. `13`.
5. `37°`.
6. The quadrilateral is cyclic because `72°+108°=180°`.
7. `∠ACB=90°`; with hypotenuse `AB=10` and leg `AC=6`, `BC=8`.
8. `12^2=8·PB`, so `PB=18`.
9. `3·12=4·PD`, so `PD=9`.
10. `5·20=4·PD`, so `PD=25`.
11. `48°` by alternate segment.
12. Equal tangents give `PB=10`; perimeter `10+10+12=32`.
13. Join centre `O` to contact points `A,B`. Triangles `OAP` and `OBP` are right triangles with `OA=OB` and common hypotenuse `OP`; hence congruent, so `PA=PB`.
14. `∠ABD` and `∠ACD` both subtend segment `AD`. Equality is the converse same-segment signal; justify `A,B,C,D` concyclic before using cyclic relations.
15. `O1O2` is perpendicular to common chord `AB`. The additional line is also perpendicular to `AB`, hence it is parallel to `O1O2`.
16. The rectangle supplies natural orthogonal coordinates and the equal lengths give low-degree equations. Concyclicity must still be imposed explicitly; it is the decisive extra constraint.
17. `25`. Independent historical reconstruction: symmetry-axis coordinate placement, circumcentre on the axis, horizontal chord through the midpoint.
18. `29`. Independent historical reconstruction gives square side `2/5`, area `4/25`, hence `4+25=29`.
19. `03`. The canonical non-degenerate branch gives `(AB/BC)^2=2/1`.
20. `10`. Common-chord/line-of-centres structure plus internal tangency yields radius sum `10`.
21. `03`. Independent circumcentre calculation gives `(OP/OA)^2=1/2`.
22. Power is `PA·PB=4·9=36`. Thus `6·PD=36`, so `PD=6`; also `PT^2=36`, hence `PT=6`.

Historical answers `25,29,03,10,03` were independently re-derived in `Authoring/Independent_Math_and_Source_Audit.md` before this key was written.

---

## Mixed Mastery Test

1. `73°`.
2. `112°`.
3. The quadrilateral is cyclic because `95°+85°=180°`.
4. `15^2=9·PB`, so `PB=25`.
5. `6·8=4·PD`, so `PD=12`.
6. `3·18=6·PD`, so `PD=9`.
7. `41°`.
8. Equal tangents give `PA=PB=17`. With included angle `60°`, the cosine rule gives `AB^2=17^2+17^2-2·17·17·cos60°=17^2`, hence `AB=17`.
9. Since `O1A=O1B`, centre `O1` lies on the perpendicular bisector of chord `AB`. Likewise `O2A=O2B`, so `O2` lies on the same perpendicular bisector. Therefore `O1O2` is perpendicular to `AB`.
10. Distance from centre `(0,0)` to chord line `y=3` is `3`. Half-chord length is `sqrt(25-9)=4`; full chord length `8`. Coordinates are natural because the circle and horizontal chord are already in coordinate form.
11. The move is invalid because tangency is neither stated nor proved; visual contact is not a hypothesis. It is sufficient to know `l` is tangent at `T`, or to prove `T` lies on the circle and `OT` is perpendicular to `l`, which establishes tangency.
12. Alternate segment gives `∠ACB=52°`. If `D` lies in the same segment as `C` and also subtends chord `AB`, then `∠ADB=∠ACB=52°`.

---

## Failure interpretation

### Cyclicity errors
If a learner uses supplementary opposite angles without establishing cyclicity, require them to rewrite the solution in two columns:

- what is known before cyclicity;
- what becomes legal only after cyclicity.

### Tangency errors
If a learner uses a tangent theorem from appearance, require the exact tangent hypothesis or a radius-perpendicular proof before any angle work.

### Power errors
If a learner writes the wrong product, have them circle the power point and trace each entire line through it. The two factors in each product must belong to the same line from that point.

### Route-selection errors
If the learner uses coordinates for a one-step angle theorem, ask for a synthetic first move only. If the learner persists with a long synthetic chain in a symmetric metric rectangle/right-triangle setup, ask them to design a coordinate placement before solving.

---

## Static evidence boundary

All deterministic learner-item answers/routes in this key were independently recomputed from the authored statements. This is static authoring evidence only. Classroom timing/readability, longitudinal retention, psychometric calibration, qualification/pass-mark calibration and publication approval remain `NOT_RUN`.
