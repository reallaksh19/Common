# Circles, Cyclicity and Tangency — Assimilation Book

A circle problem becomes much easier when you stop asking **“Which theorem do I remember?”** and start asking:

> **What circle structure is actually proved here, and what is the smallest local relation that can close the problem?**

The working routine for this topic is:

`IDENTIFY STRUCTURE -> JUSTIFY IT -> CHOOSE ONE LOCAL RELATION -> CLOSE -> CHECK`

The picture may suggest a circle fact. The givens must justify it.

---

## 1. Reconnect: what you already own

You already know how to close ordinary angle information:

- angles on a line;
- angles in a triangle;
- parallel-line angle relations and their converses;
- the sum of the angles of a quadrilateral;
- symmetry only after it has been proved;
- coordinates as an alternate representation when they simplify the metric data.

Those facts remain available. They are **not** circle theorems.

The new question is:

> What extra information does the circle add?

A generic quadrilateral gives only a `360°` angle sum. A **cyclic** quadrilateral gives a much stronger local relation. A line that merely touches a drawing is not automatically a tangent. A product of four lengths is not automatically a power relation.

This topic is about earning the right to use the extra structure.

---

# Part I — Angles created by a circle

## 2. The same chord is the first clue

Suppose `A,B,C` lie on a circle with centre `O`.

If `∠ACB` subtends chord `AB`, then the central angle subtending the same chord is twice as large:

`∠AOB = 2∠ACB`.

This is useful only when the two angles genuinely see the **same endpoints `A,B`**.

### Recognition cue

Before writing an angle equation, underline the two endpoints of the chord or arc being viewed.

If two inscribed angles subtend the same chord `AB` from the same side of the chord, then they are equal.

So if `C,D` lie on the same arc-side of chord `AB`,

`∠ACB = ∠ADB`.

### Why this matters

A complicated angle chase can often collapse as soon as you notice that two angles are simply different views of the same chord.

### Contrast

**Looks similar:** two angles both have a point on the circle.

**Not enough:** they do not subtend the same chord.

The circle does not make arbitrary angles equal.

---

## 3. Diameter means a right angle — but only through the diameter

If `AB` is a diameter and `C` lies on the circle, then

`∠ACB = 90°`.

Why? The central angle `∠AOB` is `180°`, so the inscribed angle is half of it.

### First-move cue

If a problem gives a diameter, immediately scan for a triangle whose third vertex lies on the circle.

### Common error

A long chord that looks like a diameter is not enough. You need the centre on the chord, or an explicit statement that it is a diameter.

---

# Part II — Prove cyclicity before using cyclicity

## 4. Cyclic quadrilateral versus ordinary quadrilateral

For an ordinary quadrilateral `ABCD`,

`∠A+∠B+∠C+∠D=360°`.

If `A,B,C,D` are concyclic, then opposite angles are supplementary:

`∠A+∠C=180°`,

and

`∠B+∠D=180°`.

This is a stronger statement, so it needs a stronger hypothesis.

### Recognition rule

Write a cyclic angle relation only after one of these has happened:

1. the problem explicitly says the four points are concyclic;
2. you have proved opposite angles supplementary;
3. you have proved two equal angles subtend the same segment;
4. another valid circle criterion has been established.

### Converse as a proof tool

If, for a quadrilateral,

`∠A+∠C=180°`,

then the quadrilateral is cyclic.

This direction is often more useful than the theorem itself: you manufacture a `180°` sum from ordinary angle facts, then **upgrade** the quadrilateral to cyclic.

### The recognition chain

`ordinary angles -> supplementary pair -> cyclicity -> stronger circle relation`.

Do not reverse the order.

---

## 5. Equal subtended angles can prove cyclicity

Suppose points `A,B,C,D` satisfy

`∠ACB = ∠ADB`.

Both angles subtend segment `AB`. Under the usual non-degenerate configuration, this is a signal that `A,B,C,D` are concyclic.

This is especially effective when an angle chase naturally produces equality before the circle is visible.

### Diagnostic contrast

**Valid:** prove the equal angles first, then claim cyclicity.

**Invalid:** draw a circle through the four points because it looks plausible, then use equal angles.

---

# Part III — Tangency: a local perpendicular structure

## 6. Tangent and radius at the point of contact

If a line is tangent to a circle at `T` and `O` is the centre, then

`OT ⟂ tangent at T`.

This gives a right angle immediately.

### Recognition cue

When you see the word **tangent**, locate all three of these objects:

- the centre;
- the contact point;
- the tangent line.

Then write the perpendicular relation before chasing any other angle.

### Contrast: tangent versus chord

A chord meets the circle at two points.
A tangent meets it at one point locally.

A line drawn nearly tangent is not a tangent theorem hypothesis.

---

## 7. Equal tangents from one external point

If tangents from external point `P` touch the same circle at `A` and `B`, then

`PA = PB`.

The hidden structure is two right triangles:

- `OA ⟂ PA`;
- `OB ⟂ PB`;
- `OA=OB`;
- `OP` is common.

So the two right triangles are congruent.

### First-move cue

If the same external point sends two tangent segments to one circle, mark them equal before introducing variables.

### Why not use this everywhere?

Equal tangents require the **same external point** and the **same circle**. Two unrelated tangent segments need not be equal.

---

# Part IV — Alternate segment: translate a tangent angle into a circle angle

## 8. The theorem as a translation rule

Let the tangent at `A` meet chord `AB`. If `C` is on the opposite arc, then the angle between the tangent and chord `AB` equals the inscribed angle subtending chord `AB`:

`angle(tangent at A, AB) = ∠ACB`.

The most useful way to remember this is not as a sentence. Remember the **shared chord `AB`**.

### Recognition chain

`tangent at A + chord AB -> find an inscribed angle that also sees AB`.

### Contrast: alternate segment versus generic angle chase

If a tangent and chord appear together, first test whether alternate segment gives the target angle in one step.

Do not start a five-line parallel/triangle chase unless the circle relation fails to connect the needed endpoints.

### Hypothesis discipline

You may use alternate segment only after tangency is stated or proved.

A line that merely touches the sketch is not enough.

---

# Part V — Power of a point: one invariant, several surfaces

## 9. The idea before the formulas

For a fixed circle and a fixed point `P`, different lines through `P` can produce the same length product.

That common value is the power of `P` with respect to the circle.

The important learner question is:

> **Which point owns the power?**

Do not begin by memorizing products. First identify `P`.

---

## 10. Intersecting chords inside a circle

Suppose chords `AB` and `CD` intersect at interior point `P`.

Then

`PA·PB = PC·PD`.

### First-move cue

Circle the common intersection point `P`, then pair the two segments lying on each complete chord.

### Wrong product warning

The product uses the two pieces of the **same line through `P`**.

Do not pair visually nearby segments from different chords.

---

## 11. Two secants from an external point

Suppose `P` is outside the circle. One secant meets the circle at near point `A` and far point `B`; another meets it at near point `C` and far point `D`.

Then

`PA·PB = PC·PD`.

Here `PB` and `PD` are whole distances from the external point to the far intersections.

### Common error

Using “outside piece × inside piece” instead of

`outside distance × whole secant distance`.

Always label the four points in order from `P` before multiplying.

---

## 12. Tangent-secant power

If `PT` is tangent and `PAB` is a secant through the same external point `P`, then

`PT^2 = PA·PB`.

Again, the owner is `P`.

### Decision boundary

- two chords crossing inside -> chord product;
- two secants from outside -> external secant product;
- tangent plus secant from outside -> tangent square equals secant product.

The invariant is the same. The visible surface changes.

---

# Part VI — Common chords and intersecting circles

## 13. Two circles intersecting at A and B

If two circles with centres `O1,O2` intersect at `A,B`, then the line joining the centres is perpendicular to the common chord `AB`.

At this level, use this as a local geometric fact; there is no need to build a full radical-axis chapter.

### Recognition cue

Two circles + common chord + centres -> test perpendicularity.

This can combine with another right angle to prove two lines parallel or collinear.

### Why this matters in hard problems

Sometimes the circle theorem does not directly give the numerical answer. It gives a **direction** or **alignment** that makes a coordinate or metric calculation short.

That is still a successful circle-first route.

---

# Part VII — Choosing synthetic or coordinate geometry

## 14. Circle structure first; representation second

Coordinates are not a failure of synthetic geometry. They are an alternate representation.

Use this decision rule:

### Prefer a short synthetic chain when

- the target is an angle;
- cyclicity/tangency immediately creates a local angle relation;
- a power product closes the required length relation;
- equal tangents remove variables.

### Test coordinates when

- the diagram already has a right triangle, square or rectangle;
- lengths are numerical;
- symmetry gives a natural axis;
- the circle condition becomes one quadratic equation;
- a synthetic route would require several unrelated auxiliary constructions.

### Bad coordinate use

Introducing eight variables before using the circle structure.

### Good coordinate use

Use the circle relation to decide what needs to be preserved, then place the geometry so most coordinates are zero or symmetric.

---

# Part VIII — Five historical patterns

The historical problems below are not five new theorems. They are five examples of **representation choice**.

## 15. Square inside a right triangle with a circle condition

The useful structure is not “square theorem plus circle theorem.”

It is:

1. place the right triangle on axes;
2. represent the square with one side length;
3. use line membership for one square vertex;
4. use the circle equation for the other;
5. reject the geometric branch that does not fit the interior configuration.

This pattern yields the verified historical value `29`.

### Transfer cue

When a circle is embedded in an otherwise coordinate-friendly metric configuration, use the circle condition as one precise equation rather than launching an angle chase.

---

## 16. Rectangle plus concyclicity

A rectangle alone gives many metric possibilities.

The extra statement that four points are concyclic is the decisive constraint.

The useful chain is:

`rectangle coordinates -> use equal lengths -> impose cyclicity -> exclude degenerate branch -> finish metric ratio`.

The canonical historical interpretation is non-degenerate; the branch that makes the stated cyclic condition vacuous is not accepted.

Verified historical value: `03`.

---

## 17. Two circles tangent internally to a larger circle

The decisive local fact is that the common chord of the two inner circles is perpendicular to their line of centres.

A supplied right angle creates another perpendicular to the same chord. This aligns the centre geometry and turns the radius condition into a short invariant calculation.

Verified historical value: `10`.

### Transfer cue

When several circles interact, ask first what is forced about their centres and common chords before writing circle equations.

---

## 18. Symmetric isosceles triangle and a parallel chord

The problem has a circumcircle, but symmetry makes coordinates cheaper than a long chord theorem chain.

The efficient route is:

1. centre the base on an axis;
2. find the altitude;
3. locate the circumcentre on the symmetry axis;
4. use distance from the centre to the horizontal chord;
5. recover the chord length.

Verified historical value: `25`.

---

## 19. Circumcentres inside a square

The word “circumcentre” is a signal for perpendicular bisectors.

In a unit square, coordinates make those bisectors cheap. The perimeter condition removes the remaining symmetric expression.

Verified historical value: `03`.

### Transfer cue

When several circumcentres occur in an orthogonal coordinate-friendly shape, compare coordinate cost with synthetic cost before committing.

---

# Part IX — Error laboratory inside the lesson

## 20. “It looks cyclic.”

**Error:** writing opposite angles supplementary because four points appear to lie on a circle.

**Repair:** state or prove cyclicity first.

---

## 21. “The line touches the circle, so it is tangent.”

**Error:** reading tangency from a sketch.

**Repair:** use an explicit tangent statement, or prove the radius is perpendicular at the contact point.

---

## 22. “Power means multiply four lengths.”

**Error:** choosing products by visual proximity.

**Repair:** identify the power point, then pair segments along each line through that point.

---

## 23. “A circle problem must have a synthetic solution.”

**Error:** refusing coordinates even when the metric shape is already a right triangle, square or rectangle.

**Repair:** preserve the circle structure first, then choose the cheapest representation.

---

## 24. “Coordinates solve everything.”

**Error:** replacing a one-step tangent or cyclic angle relation with many variables.

**Repair:** test the shortest local circle theorem before coordinate expansion.

---

# Part X — Adopt the method

Before doing any serious calculation, write these four lines in your head:

1. **Circle structure:** What is stated or proved — same chord, cyclicity, tangent, common chord, power point?
2. **Local relation:** What one theorem directly uses that structure?
3. **Representation:** Is a short synthetic chain cheaper, or do symmetry/metric givens make coordinates cheaper?
4. **Check:** Did I use a theorem whose hypotheses were actually established?

You have assimilated this topic when an unfamiliar diagram no longer makes you search randomly through circle theorems. You first identify the structure, justify it, and then choose the shortest legal move.
