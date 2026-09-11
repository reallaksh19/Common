# Angles, Lines, Quadrilaterals & Polygon Structure

## Start with a decision, not a theorem list
When a geometry problem looks busy, first ask: **what structure is actually proved?** Then choose the smallest accounting system. Local angle relations are cheap when only a few unknowns interact. A global polygon formula is cheap when regularity makes every turn identical. Coordinates are useful only when numerical directions and lengths collapse the picture faster than a synthetic chase.

## 1. Local angle closure
A straight line contributes 180 degrees. Angles around a point contribute 360 degrees. Vertically opposite angles are equal. These facts become powerful when you write only the relation that removes an unknown.

### Reconnect
If one angle at an intersection is 68 degrees, its vertical opposite is 68 and each adjacent angle is 112. The point is not memorising four labels; it is noticing that one known angle determines the whole intersection.

### Parallel lines: theorem and converse are different jobs
If two lines are already known parallel, corresponding and alternate interior angle equalities may be used. If parallelism is *not* given, an appropriate equality can instead prove the lines parallel. A diagram that merely looks parallel proves nothing.

<!-- ITEM:GEO02-A01 -->
### Try first
Two lines are known parallel. A transversal makes a 73 degree angle with the first line. Write the first relation that determines the adjacent obtuse angle on the second line.

## 2. Quadrilaterals: reconstruct 360 degrees
Draw one diagonal of any nondegenerate quadrilateral. It creates two triangles, so the four interior angles total `180 + 180 = 360` degrees. This derivation matters because the same diagonal can split a harder angle network into two small ones.

Do not import properties of rectangles, parallelograms, kites or cyclic quadrilaterals unless they are proved or stated. “It looks special” is not a hypothesis.

## 3. Regular polygons: think in turns
Walking around a convex polygon, the total exterior turn is 360 degrees. In a regular n-gon every turn is equal, so

`exterior angle = 360/n`

and

`interior angle = 180 - 360/n`.

The formula is therefore a global symmetry statement, not a magic expression. If the problem asks whether an angle can occur, solve for `n = 360/(180 - interior angle)` and then enforce that n is an integer at least 3.

### Local vs global contrast
If a regular 18-gon asks for one interior angle, the global turn is immediate. If a quadrilateral shows four unrelated labelled angles, a local chase is usually smaller than pretending the figure has regularity.

## 4. Diagonals: use them with a purpose
Each vertex of an n-gon connects by a diagonal to `n-3` non-neighbouring vertices. This counts every diagonal twice, hence

`number of diagonals = n(n-3)/2`.

A diagonal may also be an auxiliary line: it can split a quadrilateral into two triangles or expose an isosceles substructure. But adding a diagonal that creates more unknowns is not progress.

## 5. Symmetry must be earned
A regular polygon has rotational symmetry through multiples of `360/n` degrees. Reflection axes depend on the polygon. For a non-regular figure, symmetry may still be proved from congruent subfigures or equal-distance conditions, but it may never be inferred from the sketch alone.

<!-- ITEM:GEO02-A02 -->
### Try first
A regular 15-gon is rotated by 72 degrees. Decide whether it maps onto itself, and write the one divisibility statement that answers the question.

## 6. When coordinates/vectors are cheaper
Stay synthetic when angle equalities, parallel lines, regularity or a useful diagonal close the problem quickly. Switch representation when lengths and fixed directions are numeric but the synthetic picture has too few angle relations. The coordinate chapter owns the full technique; here the decision is only whether to route there.

## 7. Trapezium feasibility before integer counting
When four lengths are assigned to a trapezium, not every assignment produces positive height. Let the bases differ by d and the legs have lengths p and q. The horizontal projections form a triangle-like feasibility condition:

`|p-q| < d < p+q`.

Equality collapses the height to zero. Only after geometric feasibility should integer/congruence counting begin.

## 8. Adopt the router
Before calculating, say aloud:
1. What structure is proved?
2. Is the target local or global?
3. Would a diagonal reduce unknowns?
4. Is the symmetry proved or merely visible?
5. Would coordinates reduce the number of variables?
6. What geometric condition must remain nondegenerate?
