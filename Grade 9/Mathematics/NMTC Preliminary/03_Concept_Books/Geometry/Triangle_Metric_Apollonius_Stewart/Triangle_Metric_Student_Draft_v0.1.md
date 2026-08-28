# Triangle Metric Recognition
## Student Draft v0.1

Use this loop:

`SEE -> MARK -> CHOOSE RELATION -> ELIMINATE -> SOLVE -> CHECK`

The main question is not “Which theorem do I remember?”

It is:

> What special segment is present, and what quantity can I eliminate fastest?

---

# 1. First classify the segment

Triangle `ABC`, point `D` on `BC`, segment `AD`.

- `BD=DC` -> median.
- `AD perpendicular BC` -> altitude.
- `angle BAD=angle DAC` -> angle bisector.
- none of these -> general cevian.

Do this classification before calculation.

---

# 2. Altitude: subtract before solving

If `AD perpendicular BC`, then

`AB^2=AD^2+BD^2`

and

`AC^2=AD^2+DC^2`.

Subtract:

`AB^2-AC^2=BD^2-DC^2`.

The altitude disappears.

### Example

Suppose `BD=10`, `DC=6` and `AB^2-AC^2` is required.

Do not solve `AD`.

Answer:

`10^2-6^2=64`.

### PYQ connection

`NMTC-BH-P-2018-Q23` uses exactly this kind of cancellation-first thinking.

---

# 3. Stewart: one formula for a general cevian

Let

- `BD=m`;
- `DC=n`;
- `BC=a=m+n`;
- `AB=c`;
- `AC=b`;
- `AD=d`.

Then:

`b^2m+c^2n=a(d^2+mn)`.

## How to remember safely

Do not chant letters.

Use this sentence:

> each side square is multiplied by the adjacent opposite base segment; the base multiplies `cevian^2 + product of base parts`.

Always redraw/relabel before substitution.

### Example

`AB=7`, `AC=8`, `BD=3`, `DC=5`. Find `AD^2`.

Here:

`c=7`, `b=8`, `m=3`, `n=5`, `a=8`.

Stewart:

`8^2(3)+7^2(5)=8(d^2+15)`.

`192+245=8d^2+120`.

`317=8d^2`.

So `d^2=317/8`.

---

# 4. Apollonius: Stewart when the cevian is a median

If `D` is the midpoint, then

`m=n=a/2`.

Stewart becomes:

`b^2+c^2=2d^2+a^2/2`.

Equivalently:

`d^2=(2b^2+2c^2-a^2)/4`.

Here `d` is the median from `A` to side `a=BC`.

### Example

A triangle has sides adjacent to vertex `A` equal to 7 and 9, and opposite side 8. Find the median to side 8.

`d^2=[2(7^2)+2(9^2)-8^2]/4`

`=[98+162-64]/4=196/4=49`.

So `d=7`.

### PYQ connection

2019 Q02 is a clean median-geometry anchor. The right first move is metric reduction before a long angle chase.

---

# 5. When coordinates/vectors beat Apollonius

If two medians are perpendicular, the word **perpendicular** may suggest dot products.

Example setup:

Place one vertex at the origin and write median vectors. Perpendicularity becomes one scalar equation:

`u dot v = 0`.

Use Apollonius when lengths dominate; use vectors when direction/perpendicularity dominates.

The theorem is a tool, not a compulsory route.

---

# 6. Angle bisector: ratio first, Stewart second

If `AD` bisects angle `A`, then

`BD/DC = AB/AC = c/b`.

If `BC=a`, then

`BD=ac/(b+c)`

and

`DC=ab/(b+c)`.

Now Stewart gives the bisector length.

A useful derived relation is:

`AD^2 = bc - BD*DC`.

Equivalent form:

`AD^2 = bc[1-a^2/(b+c)^2]`.

### Why this matters

The angle-bisector theorem tells you **where D sits**.

Stewart tells you **how long AD is**.

---

# 7. Right triangle: radius data are metric data

For a right triangle with legs `p,q` and hypotenuse `h`:

`R=h/2`.

Also:

`r=(p+q-h)/2`.

So if `R:r` is given, convert it into side information before using half-angle formulas.

### Example

If `R:r=5:2`, normalize `h=10`, `r=2`.

Then:

`p+q = h+2r = 14`.

With `p^2+q^2=100`,

`(p+q)^2=p^2+q^2+2pq`

`196=100+2pq`, so `pq=48`.

Thus the legs are 6 and 8.

This is the metric core behind the 2025 Q06 route.

---

# 8. Choose among six first moves

## Trigger: midpoint
Write Apollonius or Stewart with equal base parts.

## Trigger: altitude + side-square difference
Subtract Pythagoras.

## Trigger: arbitrary cevian + side/base lengths
Use Stewart.

## Trigger: angle bisector
Write base ratio first, then Stewart if a length is needed.

## Trigger: perpendicular medians / directional condition
Try coordinates or vectors.

## Trigger: right triangle + `R,r`
Convert radii to side relations before trigonometry.

---

# 9. Wrong-move contrasts

### Contrast A
Target is `AB^2-AC^2` and one altitude splits the base.

Wrong: solve altitude.

Better: subtract.

### Contrast B
Median length asked, all three side lengths known.

Wrong: introduce angles and cosine law twice.

Better: Apollonius.

### Contrast C
General cevian with unequal base split.

Wrong: use the median formula.

Better: Stewart.

### Contrast D
Angle bisector with side lengths.

Wrong: assume it is also a median.

Better: use the angle-bisector ratio.

---

# 10. Source integrity is part of geometry

A recovered solution can invoke a correct theorem and still be inconsistent with the printed data.

That happens in the qualified record for 2023 Q02: Apollonius is a plausible first move, but the downstream angle claim does not agree with the reproduced side data.

Correct behavior:

`RECOMPUTE -> RECORD CONFLICT -> DO NOT SILENTLY REPAIR`.

---

# Self-test

1. A triangle has sides 10, 14, 16. Find the median to side 16.
2. An altitude splits the base into 12 and 5. Find `AB^2-AC^2` if `B` is adjacent to the 12 segment.
3. In a triangle, `AB=9`, `AC=11`, `BD=4`, `DC=6`. Find `AD^2`.
4. An angle bisector from `A` meets `BC` at `D`; `AB=6`, `AC=9`, `BC=10`. Find `BD,DC`.
5. A right triangle has `R=5`, `r=2`. Find the legs.

## Answers

1. `m^2=[2(10^2)+2(14^2)-16^2]/4=84`, so `m=2sqrt21`.
2. `12^2-5^2=119`.
3. Stewart: `11^2(4)+9^2(6)=10(d^2+24)` -> `970=10d^2+240`, so `d^2=73`.
4. `BD/DC=6/9=2/3`, so `BD=4`, `DC=6`.
5. hypotenuse `10`, leg sum `14`, product `48`; legs `6,8`.
