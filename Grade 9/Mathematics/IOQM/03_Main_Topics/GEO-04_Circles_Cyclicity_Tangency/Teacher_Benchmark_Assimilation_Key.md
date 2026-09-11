# Teacher Benchmark Assimilation Key — Circles, Cyclicity and Tangency

This key evaluates whether the learner can **earn and select** a circle relation rather than merely recall theorem names.

## A. RECONNECT

1. Check that cyclicity is stated or proved before using opposite supplementary angles.
2. Test equality: inscribed angles subtending the same chord from the same segment are equal.
3. Radius to the point of tangency is perpendicular to the tangent.
4. The tangent segments must start from the same external point and touch the same circle.
5. The shared chord links the tangent-chord angle to the inscribed angle in the alternate segment.
6. Identify the point whose power with respect to the fixed circle is being computed.
7. The line joining the two centres is perpendicular to the common chord.
8. Test coordinates when symmetry/right angles/rectangles/squares and numerical metric data make a low-variable coordinate model cheaper than a long synthetic chain.

Suggested diagnostic codes:

- 1-2: `CYCLICITY_ASSUMED_FROM_PICTURE` / same-chord recognition weakness;
- 3-5: `TANGENCY_NOT_PROVED` / `TANGENT_CHORD_CONFUSED`;
- 6: `POWER_POINT_MISMATCH`;
- 7: intersecting-circle recognition weakness;
- 8: `COORDINATE_OVERKILL` or synthetic overcommitment.

---

## B. Error laboratory

### Error 1
First invalid move: treating visual concyclicity as a hypothesis.

Repair: prove cyclicity, for example from supplementary opposite angles or an appropriate equal-angle converse, or cite the explicit concyclicity statement.

### Error 2
First invalid move: reading tangency from the sketch.

Repair: require explicit tangency or prove that the line is perpendicular to the radius at a point on the circle.

### Error 3
First invalid move: pairing segments by size rather than by complete line through the power point.

Repair: for chords through `P`, use `PA·PB=PC·PD` with `A,B` on one line and `C,D` on the other.

### Error 4
First invalid move: using outside piece × inside piece.

Repair: for an external secant `P-A-B`, use `PA·PB`, where `PB` is the whole distance from `P` to the far intersection.

### Error 5
First inefficient move: theorem catalogue search before identifying structure.

Repair: write the structure first — same chord, cyclicity, tangent, power point, common chord — then choose the smallest theorem that uses it.

### Error 6
First conceptual error: treating “circle problem” as synonymous with “synthetic only.”

Repair: preserve the circle condition explicitly, then compare synthetic and coordinate cost.

---

## C. ADOPT — expected first two lines

1. `ABCD` cyclic -> opposite angle to `117°` equals `63°`.
2. `83°+97°=180°` -> conclude the quadrilateral is cyclic.
3. Mark `OT` perpendicular to the tangent at `T`; then identify the chord seen by the tangent-chord angle.
4. Mark the two tangent lengths equal and connect the centre to the contact points if a proof is required.
5. Identify `P` as the power point and write `PA·PB=PC·PD`.
6. Identify `P` as the power point and write `PT^2=PA·PB`.
7. State that the line of centres is perpendicular to common chord `AB`.
8. Place the base symmetrically on an axis and put the apex/centre on the symmetry axis; then use the circle/chord distance relation.

---

## D. TRANSFER — route expectations

1. The `180°` opposite-angle sum proves cyclicity. After that upgrade, opposite supplementary and same-chord circle relations become legal.
2. Identify the common external point. If the road segment is tangent `PT` and another path is secant `PAB`, write `PT^2=PA·PB`.
3. Each centre is equidistant from `A,B`, so both lie on the perpendicular bisector of `AB`; hence the line joining the centres is perpendicular to `AB`.
4. The rectangle alone does not determine the metric ratio. Concyclicity must be converted into an algebraic circle relation; it is the extra constraint that removes the remaining degree of freedom.
5. If the target angle and the tangent-chord angle see the same chord, alternate segment is one step and is cheaper. Otherwise continue with ordinary angle closure or another justified circle relation.
6. Accept any coherent coordinate-friendly example, such as a symmetric isosceles triangle with a circumcircle and horizontal chord. The circle condition must still appear explicitly as a radius/distance/circle equation or an equivalent chord-distance relation.

---

## E. Six-question assimilation rubric

A strong response should contain all six components:

1. **Notice:** identifies the actual circle structure rather than naming a chapter.
2. **Legality:** states the hypothesis/proof that earns the relation.
3. **Recognition cue:** gives a transferable clue such as same chord, tangent + chord, power point, or common chord.
4. **Contrast:** names a similar-looking case where the theorem would be illegal or inefficient.
5. **First move:** writes two mathematically useful lines without solution scaffolding.
6. **Disguise:** changes the surface while preserving the same invariant/structure and outlines a valid route.

Do not award full assimilation credit to a learner who can solve one familiar numeric item but cannot explain why cyclicity/tangency/power is legal or cannot start a changed-surface version.

---

## Static evidence boundary

All deterministic benchmark-lab routes were independently checked against the authored prompts. Classroom timing/readability, retention, psychometric calibration, qualification/pass-mark calibration and publication approval remain `NOT_RUN`.
