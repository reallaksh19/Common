# Assimilation Book — Triangle Feasibility, Metric Relations and Special Cevians

Status: `INTEGRATED_LEARNER_CORE_V1_SOURCE_FIGURE_CUSTODY_PENDING`

## Learner promise

A triangle metric problem should not begin with a formula hunt. Use this router:

`CHECK FEASIBILITY -> CLASSIFY THE SEGMENT/CONSTRAINT -> CHOOSE THE CHEAPEST VALID RELATION -> APPLY METRIC OR DISCRETE FILTER -> CHECK THE ORIGINAL CONDITIONS`.

The central habit is **classification before calculation**.

---

## 1. Feasibility comes before geometry

For positive side lengths `a,b,c`, a non-degenerate triangle exists exactly when each side is smaller than the sum of the other two. If two sides `p,q` are fixed and the third side is `d`, compress the three inequalities to

`|p-q| < d < p+q`.

The inequalities are strict. Equality gives a degenerate straight-line configuration, not a triangle.

### Why this matters

Many contest problems hide feasibility inside an integer count, a proposed diagonal, or an algebraic side relation. If the object does not exist, later metric work is irrelevant.

### Reconnect

A quadrilateral diagonal is simultaneously a side of two triangles. Therefore a candidate diagonal must lie in **both** triangle-feasibility intervals.

### Diagnostic contrast

- `3,4,7` are positive lengths but do not form a triangle.
- `3,4,6` form a triangle.

Do not replace “positive” with “geometrically feasible.”

---

## 2. Acute, right or obtuse: sort first

Let `a<=b<=c` and first verify feasibility. Then compare

`c^2` with `a^2+b^2`.

- `c^2 < a^2+b^2` -> acute triangle;
- `c^2 = a^2+b^2` -> right triangle;
- `c^2 > a^2+b^2` -> obtuse triangle.

The comparison belongs to the **largest side**.

### Extremal reasoning for “every triple”

If a set of candidate side lengths must make every allowed triple acute, make the left side of

`c^2 < a^2+b^2`

as large as possible and the right side as small as possible, subject to the source selection rule.

If repetition is allowed, the two smallest selected sides may be equal. For the historical IOQM-2024-Q15 mechanism, the source allows choices “not necessarily distinct,” so the extremal triple is `(n,n,n+38)`, not `(n,n+2,n+38)`.

---

## 3. Classify the cevian before choosing a theorem

A **cevian** is a segment from a triangle vertex to the opposite side. Four common roles must not be conflated.

- **median**: ends at the midpoint of the opposite side;
- **altitude**: perpendicular to the opposite side or its extension;
- **angle bisector**: divides the vertex angle into two equal angles;
- **arbitrary cevian**: none of those special properties is known.

A diagram that looks symmetric proves nothing.

### First classification questions

For cevian `AD` in triangle `ABC`, ask:

1. Is `BD=DC` stated or proved? Then `AD` is a median.
2. Is `AD perpendicular BC` stated or proved? Then `AD` is an altitude.
3. Is `angle BAD = angle DAC` stated or proved? Then `AD` is an angle bisector.
4. If none holds, treat `AD` as arbitrary.

A ratio such as `BD:DC=2:1` does **not** make `AD` a median or angle bisector.

---

## 4. Median structure: Apollonius before Stewart

If `M` is the midpoint of `BC`, then

`AB^2 + AC^2 = 2(AM^2 + BM^2)`.

Equivalently, if `BC=a`, `CA=b`, `AB=c`, and median `AM=m_a`,

`b^2+c^2 = 2m_a^2 + a^2/2`.

This is Apollonius’ theorem.

### Why it is cheaper

Stewart’s theorem also works, but midpoint information makes the algebra collapse immediately. Use the special theorem before the general fallback.

### Retrieval boundary

If the problem instead turns on similarity, area ratios, parallel transfer, or centroid `2:1`, retrieve those facts from GEO-03 rather than rebuilding them here.

---

## 5. Angle bisector: side ratio, not midpoint

If `AD` bisects `angle A` in triangle `ABC`, then

`BD/DC = AB/AC`.

A clean derivation uses areas: triangles `ABD` and `ACD` share the same altitude from `A` to line `BC`, so

`[ABD]/[ACD] = BD/DC`.

They also have included angles at `A` equal, hence the same sine factor in the area formula, giving

`[ABD]/[ACD] = AB/AC`.

Therefore the two ratios are equal.

### Mandatory contrast

Angle bisector means equal **angles**, not equal opposite-side pieces. Only if `AB=AC` does the angle bisector also become a median.

---

## 6. Stewart: the general metric fallback

In triangle `ABC`, let `D` lie on `BC` with

`BD=m`, `DC=n`, `BC=m+n`, `AD=d`, `AC=b`, `AB=c`.

Then Stewart’s theorem is

`b^2 m + c^2 n = (m+n)(d^2 + mn)`.

### Use Stewart when

- the cevian is genuinely arbitrary;
- the split `m:n` is known;
- the target is metric;
- no one-step similarity, right-triangle, median or angle-bisector relation is cheaper.

### Do not use Stewart merely because a cevian is drawn

A right triangle plus a side relation may close with Pythagoras. A median may close with Apollonius. An angle bisector may close through a ratio and one additional equation.

The theorem is a fallback, not a reflex.

---

## 7. Right-triangle metric structures

For right triangle `ABC` with right angle at `A`, hypotenuse `BC=c`, and altitude `AH=h` to the hypotenuse, let

`BH=p`, `HC=q`.

Then

`p+q=c`,

`h^2=pq`,

`AB^2=cp`,

`AC^2=cq`.

Also, from area,

`AB*AC = c*h`.

### Method selection

If the problem gives legs, hypotenuse, an altitude, or a divided hypotenuse, test these relations and direct Pythagoras before Stewart.

---

## 8. Radius bridges reconstruct side data

Let triangle area be `Delta`, semiperimeter `s`, inradius `r`, circumradius `R`, and exradii `r_a,r_b,r_c`.

Core bridges:

`Delta = r s`,

`Delta = r_a(s-a) = r_b(s-b) = r_c(s-c)`,

`Delta = abc/(4R)`.

### Complement variables

Set

`x=s-a`, `y=s-b`, `z=s-c`.

Then

`a=y+z`, `b=z+x`, `c=x+y`, and `s=x+y+z`.

Exradius data often gives `x,y,z` more directly than the sides themselves.

### Heron bridge

`Delta^2=s(s-a)(s-b)(s-c)=sxyz`.

Use this only as far as needed. The goal is metric reconstruction, not a separate polynomial chapter.

---

## 9. Continuous geometry first, integer filtering second

A contest item may ask for integer sides, an integer perimeter, or a least integer threshold. Do not begin by listing integers.

First derive the geometric interval or equation. Then impose integrality.

### Example pattern: right triangle with integer hypotenuse

If the altitude to the hypotenuse is fixed and area gives `ac=hb`, combine that with

`a^2+c^2=b^2`.

If `a+c` is also constrained to be integral, a difference-of-squares factorization may appear. That factorization is the **terminal discrete filter**, not the starting point.

---

## 10. Method-selection table

| Surface cue | First classification | Cheapest first test |
|---|---|---|
| two sides fixed, third unknown | feasibility | `|p-q|<d<p+q` |
| triangle type requested | sort largest side | `c^2 ? a^2+b^2` |
| midpoint on opposite side | median | Apollonius |
| equal angle marks at vertex | angle bisector | side-ratio theorem |
| arbitrary split `m:n` | arbitrary cevian | Stewart if no cheaper route |
| right angle + hypotenuse split | right-triangle metric | projection/altitude identities |
| exradii/inradius/circumradius | radius bridge | area identities + complements |
| integer count/least integer | continuous geometry first | interval/equation, then filter |
| parallel/similar/area-ratio surface | prerequisite retrieval | GEO-03 |
| highly symmetric numeric geometry | representation choice | synthetic first; coordinates only if cheaper |

---

## 11. Historical anchor map

Historical mathematics is independently closed, but exact source-page/figure custody is still a separate publication gate. Until that custody closes, use these as **mechanism records**, not as rendered PYQ reproductions.

- `IOQM-2025-Q04 -> 06`: isosceles integer triangle; feasibility then counting.
- `IOQM-2025-Q09 -> 28`: intersect two diagonal-feasibility intervals.
- `IOQM-2024-Q10 -> 05`: algebra collapses to square relations; triangle feasibility remains the final gate.
- `IOQM-2024-Q15 -> 92`: acute criterion with repeated selections allowed; extremal triple `(n,n,n+38)`.
- `IOQM-2024-Q22 -> 34`: divided hypotenuse in a right triangle; do not misclassify the cevian.
- `IOQM-2024-Q27 -> 27`: local angle structure creates cyclic right-angle quadrilaterals and an equilateral pedal triangle.
- `IOQM-2024-Q30 -> 25`: right-triangle altitude relation, then integer factor filtering.
- `IOQM-2023-Q13 -> 58`: exradii -> semiperimeter complements -> sides.

---

## 12. Transfer habits

When the surface changes, keep the invariant.

- Quadrilateral diagonal -> two triangle intervals.
- Algebraic side relation -> solve algebra, then test geometric admissibility.
- “Every triple” -> identify the extremal admissible triple before solving.
- Cevian diagram -> classify from givens, not appearance.
- Radius data -> move through area to complements or sides.
- Integer geometry -> derive the real-valued constraint before discrete filtering.

The final check is always against the original statement: positivity, strict inequalities, segment location, stated special properties, and any integer/source-selection conditions.
