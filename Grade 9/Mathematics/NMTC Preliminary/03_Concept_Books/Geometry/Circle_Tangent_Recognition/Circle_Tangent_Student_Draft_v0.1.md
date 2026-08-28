# Circle & Tangent Recognition
## NMTC Bhaskara Preliminary — Student Concept Book Draft v0.1

> Geometry speed comes from seeing what is forced before trying to calculate.

Use:

`SEE -> MARK -> RELATE -> CHOOSE -> CHAIN -> CHECK -> ADOPT`

---

# 0. Diagnostic

Without notes, answer:

1. A tangent touches a circle at A and O is the centre. What angle does OA make with the tangent?
2. From P, tangents PA and PB touch the same circle. Compare PA and PB.
3. A central angle standing on arc AB is 120°. What is an inscribed angle standing on the same arc?
4. AB is a diameter and C is on the circle. Find `∠ACB`.
5. Opposite angles of a cyclic quadrilateral are 74° and ?
6. Chords AB and CD intersect at X inside a circle. Which product equality is relevant?
7. A tangent PT and secant P-A-B start from P. Which relation is relevant?
8. May you measure an angle from a diagram that says “not to scale”?

### Answers

1. 90°.
2. `PA=PB`.
3. 60°.
4. 90°.
5. 106°.
6. `XA·XB=XC·XD`.
7. `PT²=PA·PB`.
8. No.

---

# 1. The geometry routine: mark before you chase

Suppose you see a circle, a tangent and several lines.

Do not begin by writing every theorem you know.

First mark:

- the centre;
- radii;
- tangent points;
- diameter, if any;
- equal radii;
- right angles forced by tangency;
- equal tangent lengths;
- the chord/arc named by the target.

Then ask:

> Which one relation touches the target most directly?

That question is more useful than “Which chapter is this?”

---

# 2. Radius to tangent: the first forced right angle

Let a tangent touch a circle at A and let O be the centre.

Then:

`OA ⟂ tangent at A`.

## Why?

The perpendicular from a point to a line is the shortest distance from the point to the line.

If the tangent line had a point closer to O than A, that point would lie inside the circle, contradicting tangency.

So OA must be perpendicular to the tangent.

## First move

When a tangent point and centre are visible:

`MARK 90°`.

## Contrast

A radius to some other point of the circle is not automatically perpendicular to the tangent at A.

---

# 3. Two tangents from one external point are equal

From external point P, let PA and PB be tangents to a circle with centre O.

Then:

`PA=PB`.

## Derivation

`OA=OB` because both are radii.

`OA⊥PA` and `OB⊥PB`.

Triangles OAP and OBP are right triangles with:

- common hypotenuse OP;
- equal legs OA, OB.

Therefore the triangles are congruent, so:

`PA=PB`.

## Why this matters

Equal tangents often create:

- an isosceles triangle;
- equal angles;
- a perimeter shortcut;
- a metric relation that avoids coordinates.

---

# 4. Angle at centre is twice the angle at the circumference

Let A and B be points on a circle and O its centre. Let C be another point on the same relevant arc/segment.

Then:

`∠AOB = 2∠ACB`.

The words **same arc AB** matter.

## SEE

A problem gives an angle at the centre and asks for an angle at the circumference—or the reverse.

## FIRST MOVE

Name the endpoints A,B. Verify both angles stand on the same chord/arc.

## Example

If `∠AOB=146°`, then an inscribed angle on the same arc is:

`73°`.

## Common error

Do not halve a central angle unless the other angle subtends the same endpoints.

---

# 5. Angles in the same segment

If C and D are points on the same segment of a circle and both angles subtend chord AB, then:

`∠ACB = ∠ADB`.

Why?

Each is half the same central angle `∠AOB`.

## Recognition trigger

Two angles with the same chord endpoints.

## Trap

Do not use “same segment” merely because four points lie on a circle. Check the chord endpoints.

---

# 6. Diameter gives a right angle

If AB is a diameter and C lies on the circle, then:

`∠ACB=90°`.

Why?

The central angle `∠AOB=180°`.

So the angle at C is half of 180°.

This is often the doorway to:

- Pythagoras;
- similarity;
- tangent-length geometry.

---

# 7. Cyclic quadrilateral: supplementary opposite angles

If A,B,C,D lie on one circle, then:

`∠A+∠C=180°`

and

`∠B+∠D=180°`.

## Reverse use

If a quadrilateral has a pair of opposite angles supplementary, that is a strong route to proving it cyclic.

## Example

If one angle is 112°, its opposite cyclic angle is 68°.

## Preliminary habit

If four points are cyclic, write a supplementary relation before beginning a long chase.

---

# 8. Tangent-chord / alternate segment theorem

At point A, a tangent meets chord AB.

The angle between the tangent and chord AB equals the angle in the alternate segment subtended by chord AB.

## Safe routine

1. name tangent point A;
2. name chord AB;
3. find the remote angle whose endpoints are A and B;
4. transfer the angle.

## Why learners get this wrong

They remember “tangent angle equals circle angle” but fail to preserve the chord endpoints.

The theorem is not about any convenient angle elsewhere on the circle.

## Parallel-line bridge

If a parallel line is also present, first transfer an angle using parallel lines, then apply the alternate-segment theorem.

This is a common Preliminary-style compression.

---

# 9. Intersecting chords: product inside the circle

Chords AB and CD intersect at X inside the circle.

Then:

`XA·XB = XC·XD`.

## Why?

The triangles formed around X have:

- equal vertical angles;
- equal angles subtended by the same chords.

So they are similar, leading to the product relation.

## Example

If `XA=3`, `XB=8`, `XC=4`, then:

`3·8=4·XD`

so `XD=6`.

---

# 10. Power of a point outside the circle

## Two secants

From external point P, secants meet the circle at A,B and C,D, with A,C nearer P.

Then:

`PA·PB = PC·PD`.

Remember:

`external × whole`.

## Tangent + secant

If PT is tangent and P-A-B is a secant:

`PT² = PA·PB`.

## Contrast with internal chords

Inside:

`XA·XB=XC·XD`.

Outside:

`external × whole`.

Do not mix the segment conventions.

---

# 11. Tangent plus parallel line: transfer first

A figure may contain a tangent and a line parallel to a chord or radius-related line.

The efficient order is usually:

`PARALLEL TRANSFER -> TANGENT/CIRCLE THEOREM -> TARGET`.

Not:

`TRY EVERY CIRCLE THEOREM -> NOTICE PARALLEL LATE`.

Qualified 2024 and 2025 Preliminary evidence contains this kind of short-chain recognition, although exact historical diagrams remain figure-gated in this workspace.

---

# 12. Tangent circles: join the centres

If two circles are tangent, the line through their centres passes through the point of tangency.

For radii `r1,r2`:

- external tangency: `O1O2=r1+r2`;
- internal tangency: `O1O2=|r1-r2|`.

If circles are tangent to both sides of the same angle, their centres lie on the angle bisector. Similar triangles then make radius proportional to distance from the vertex.

This creates a useful scale/homothety bridge.

Qualified 2024 Q13 supports this mechanism cleanly enough to use as a mechanism anchor.

---

# 13. Circle metric problems: use the right angle you already earned

Once radius ⟂ tangent or diameter -> 90° is marked, metric problems often reduce to:

- Pythagoras;
- similar triangles;
- tangent equality;
- power of a point.

## Example

A tangent PT from P has length 12. A secant from P has external part 8 and whole length x.

Power of point:

`12²=8x`.

So:

`x=18`.

No coordinate geometry is needed.

---

# 14. Do not trust the visual scale

A competition diagram is a logical object, not a measurement drawing.

If a diagram looks isosceles, perpendicular or equal-length but the information is not given or forced, you may not use it.

The 2024 reproduced paper explicitly states that diagrams are visual guides/not to scale. That is an excellent general discipline even though we do not project the exact 2024 wording onto every historical year.

## Student check

Before using a fact, ask:

> Was it GIVEN, FORCED, or merely SEEN?

Only GIVEN/FORCED facts are usable.

---

# 15. Source integrity is part of geometry

Geometry source defects are especially dangerous because a missing line or mislabeled point changes the mathematics.

Examples from the qualified corpus include:

- 2023 Q05: starred scoring plus option conflict;
- 2023 Q06: target-label transcription conflict;
- several 2019–2025 questions whose answers/solutions are known but exact source figures are not yet retained in the workspace.

Correct action:

`FLAG -> TEACH MECHANISM WITH CLEAN AUTHOR-CREATED ANALOGUE -> DO NOT CLAIM EXACT PYQ FIGURE`.

---

# 16. Contrast lab

For each pair, state the correct trigger.

1. radius+tangent vs tangent+chord;
2. same chord from same segment vs opposite cyclic angles;
3. intersecting chords inside vs two secants outside;
4. equal tangents vs equal radii;
5. diameter right angle vs arbitrary chord;
6. parallel-angle transfer vs circle theorem.

A Preliminary solver must discriminate these quickly.

---

# 17. First-move lab — do not solve fully

Write only the first forced relation.

1. Tangent at A, centre O.
2. Tangents PA,PB from P.
3. Central angle AOB and inscribed angle ACB on arc AB.
4. AB diameter, C on circle.
5. ABCD cyclic, `∠A=71°`.
6. Chords AB,CD meet at X inside.
7. Tangent PT and secant P-A-B.
8. Tangent-chord angle at A plus a parallel line through another point.
9. Two circles externally tangent.
10. Historical solution refers to a diagram that is missing.

### Expected first moves

1. `OA⊥tangent`.
2. `PA=PB`.
3. `∠AOB=2∠ACB`.
4. `∠ACB=90°`.
5. `∠C=109°`.
6. `XA·XB=XC·XD`.
7. `PT²=PA·PB`.
8. transfer the parallel angle first.
9. join centres; centre distance = sum of radii.
10. `FIGURE_GATED`.

---

# 18. Adoption checklist

You have adopted this unit when you can:

- mark forced facts without prompting;
- select one theorem rather than list many;
- preserve chord/arc endpoints in angle theorems;
- distinguish internal chord products from external power products;
- use a tangent-created right angle for metric work;
- reject visual-scale assumptions;
- solve a new mixed circle/tangent problem without a chapter label;
- refuse to invent a missing historical figure.

## PYQ grounding note

The package is grounded to the qualified Preliminary mechanism corpus, but many exact geometry anchors remain figure-gated. Stable IDs are used for traceability without reproducing unretained diagrams.
