# Practice and Transfer Bank — GEO-01

Status: `AUTHORED_ITEM_BANK_V1_TEACHER_KEY_REQUIRED`

Attempt each item before using any hint. The fade sequence is `F0 -> F1 -> F2 -> F3 -> F4`; support decreases while method selection increases.

---

## F0 — direct structure

### F0-1 Feasibility count
Two sides of a triangle are `7` and `10`. How many integer values can the third side have?

Hint H3: write the strict interval first.

### F0-2 Acute/right/obtuse
Classify the triangle with side lengths `8,10,12`.

Hint H3: identify the largest side before comparing squares.

### F0-3 Boundary contrast
Classify `5,12,13`, and explain why the equality case is not “acute enough.”

---

## F1 — explicit special segments

### F1-1 Median metric
In triangle `ABC`, `AB=13`, `AC=15`, `BC=14`, and `M` is the midpoint of `BC`. Find `AM`.

Hint H2: midpoint -> median -> Apollonius.

### F1-2 Angle-bisector split
In triangle `ABC`, `AD` bisects `angle A`, `AB:AC=3:5`, and `BC=24`. Find `BD` and `DC`.

Hint H2: the opposite side is divided in the adjacent-side ratio.

### F1-3 WHY-NOT
A diagram shows `AD` from `A` to `BC`, and the picture appears symmetric. No midpoint, perpendicular, or equal-angle information is stated. Which special-cevian facts are legally available?

---

## F2 — choose the special metric relation

### F2-1 Stewart fallback
In triangle `ABC`, `AB=13`, `AC=15`, `BC=14`. Point `D` lies on `BC` with `BD=6`, `DC=8`. Find `AD^2`.

Hint H1: this split is not a midpoint; map Stewart variables before substitution.

### F2-2 Right-triangle altitude
A right triangle has altitude `h` to the hypotenuse. The altitude divides the hypotenuse into segments `9` and `16`. Find `h`, the hypotenuse, and the two legs.

Hint H1: start with `h^2=pq`.

### F2-3 Exradius reconstruction
For a triangle, the exradii opposite `a,b,c` are respectively `6,3,2`. Reconstruct the side lengths.

Hint H1: set `x=s-a`, `y=s-b`, `z=s-c` and route through area.

---

## F3 — geometry plus discrete filtering

### F3-1 Isosceles integer family
How many non-congruent isosceles triangles with integer side lengths have perimeter `31`?

Hint H1: equal sides `a`; base `31-2a`; impose positivity and strict triangle inequality before counting.

### F3-2 Extremal acute threshold
Consider the set

`n, n+3, n+6, ..., n+30`.

Three values may be selected **with repetition**. Find the least positive integer `n` such that every selected triple forms an acute triangle.

Hint H1: identify the hardest legal triple before solving the inequality.

### F3-3 Integer factor filter
A right triangle has integer hypotenuse `c`, integer perimeter, and altitude `10` to the hypotenuse. Derive a difference-of-squares equation involving `c` and the sum of the legs. Do not enumerate factor pairs until the geometric equation is complete.

---

## F4 — changed surface / route selection

### F4-1 Quadrilateral diagonal transfer
A quadrilateral has side lengths `9,16,25,40`. A diagonal separates the pairs `(9,16)` and `(25,40)`. Which of `14,20,30` can be that diagonal?

No hint on first attempt.

### F4-2 Retrieval versus metric
In a triangle, a line through one side is proved parallel to another side and the target is a pure side ratio. Explain why a GEO-03 similarity route should be tested before Stewart.

No hint on first attempt.

### F4-3 Cevian misclassification trap
In right triangle `ABC`, point `D` lies on hypotenuse `BC` with `BD:DC=2:1`. No angle-bisector or midpoint condition is given. A student writes `BD/DC=AB/AC` immediately. Diagnose the error and name a legal first route.

No hint on first attempt.

### F4-4 Representation choice
A right triangle is given numerically and a cevian endpoint has a simple rational division ratio on the hypotenuse. State one condition under which coordinates would be a cheaper alternate and one condition under which a synthetic metric relation remains preferable.

---

## Transfer Bank

For each prompt, write the invariant that survives the surface change.

1. triangle third-side problem -> quadrilateral diagonal problem;
2. side-length classification -> “every allowed triple” threshold;
3. midpoint-marked median -> arbitrary ratio-marked cevian;
4. explicit angle bisector -> misleading symmetric sketch;
5. right-triangle altitude -> integer hypotenuse/perimeter problem;
6. exradius data -> side reconstruction;
7. synthetic metric diagram -> coordinate alternate;
8. historical verified answer -> exact source-page/figure custody requirement.

---

## H0 transition rule

Move to the H0 mastery test only when the learner can, without labels:

- reject impossible triangles before calculating;
- identify the largest side for square classification;
- classify a cevian from givens rather than appearance;
- choose Apollonius/angle-bisector/right-triangle structure before Stewart where appropriate;
- retrieve GEO-03 instead of duplicating similarity machinery;
- delay integer filtering until the continuous geometry is closed.
