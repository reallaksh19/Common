# Similarity, Ratio, Area & Centroid Structure

## The governing question
Most problems here become short after one choice: **what relation is actually preserved?** Do not start by calculating every length. Prove the structure first, then transfer only the information the structure licenses.

## 1. Similarity is a proof, not a visual impression
Two triangles are similar when corresponding angles match and corresponding sides have one common scale factor. Standard routes are AA, SAS and SSS. The correspondence order matters: if `A <-> P`, `B <-> Q`, `C <-> R`, then write ratios in that order.

A common trap is to upgrade similarity to congruence. Equal angles determine shape, not size. Congruence is the special case where the scale factor is 1.

### A quick contrast
Triangles with sides `3,4,5` and `6,8,10` are similar but not congruent. Triangles with sides `3,4,5` and `3,4,5` are both similar and congruent.

## 2. Decide whether the target is linear or area
If similar figures have length scale factor `k`, then corresponding lengths and perimeters scale by `k`, while areas scale by `k^2`.

This is not a memorization trick. If both base and height are multiplied by `k`, the factor `1/2 * base * height` picks up two factors of `k`.

### Reverse direction
If two figures are already known to be similar and their areas are in ratio `25:49`, the positive side ratio is `5:7`. Without known similarity, equal or proportional areas alone do not determine the side ratio.

## 3. Area ratios can work without similarity
For triangles sharing the same altitude, area ratio equals base ratio. For triangles sharing the same base, area ratio equals height ratio. These are often cheaper than proving similarity.

Suppose points `P` and `Q` lie on the same line `BC`. Triangles `ABP` and `ABQ` have the same altitude from `A` to line `BC`, so `[ABP]:[ABQ]=BP:BQ`.

## 4. Parallel lines are ratio-transfer machines
If `D` lies on `AB`, `E` lies on `AC`, and `DE` is parallel to `BC`, then triangle `ADE` is similar to triangle `ABC`. One proved parallel relation transfers the division ratio across the two sides:

`AD/AB = AE/AC = DE/BC`.

If `AD/AB=2/5`, the area ratio is not `2/5`; it is `4/25`.

## 5. The centroid: use the invariant that matches the target
The three medians meet at the centroid `G`. Along a median from vertex `A` to midpoint `M` of `BC`,

`AG:GM = 2:1`.

For area questions, an even more useful statement is

`[GAB] = [GBC] = [GCA] = (1/3)[ABC]`.

All three medians together split the whole triangle into six equal-area small triangles. These facts are shape-independent; no side lengths or angles are required.

Coordinates can verify the centroid, but do not reach for a coordinate formula when the area share closes the problem in one line.

## 6. Area decomposition: compute fractions before lengths
When lines cut a figure into pieces, label each piece as a fraction of a convenient whole. Add or subtract only after the fractions are controlled by similarity, common altitude/base, midpoint, or centroid facts.

This avoids a frequent dead end: computing several side lengths merely to feed an area formula when the entire answer is already determined by ratios.

## 7. Two validated historical mechanisms
- `IOQM-2024-Q12`: a square with side-trisection points and two crossing lines. A ratio/coordinate intersection gives the target triangle area. The independently recomputed answer is 96.
- `IOQM-2023-Q05`: medians, their centroid and midpoints on the medians. The requested area is a shape-independent fraction of the whole; the independently recomputed answer is 10.

Both source problems are text-only in the frozen corpus; no historical figure is reproduced here.

## 8. Representation choice
Use a synthetic ratio route when parallels, midpoint relations or obvious similar triangles already control the picture. Use coordinates when several line intersections are numerical and a clean placement turns them into two linear equations. A coordinate solution is not automatically more rigorous or more advanced; it is simply another representation. The best route is the one with the shortest justified chain.

## 9. A complete example
In triangle `ABC`, point `D` lies on `AB` with `AD:DB=3:2`, point `E` lies on `AC`, and `DE` is parallel to `BC`. If `[ADE]=54`, find `[ABC]`.

`AD/AB = 3/5`, so the area scale is `(3/5)^2=9/25`. Therefore `[ABC]=54*(25/9)=150`.

Notice the sequence: prove/recognize similarity -> identify linear scale -> square because the target is area -> solve.

## 10. Self-check questions before you calculate
- What exactly proves the triangles similar?
- Have I written the correct vertex correspondence?
- Is the target a length/perimeter or an area?
- Do the compared triangles share a base or altitude?
- Is a median/centroid fact enough without coordinates?
- Is a line really parallel, or does it merely look parallel?
- Can I express the desired region as a fraction of a larger area first?
