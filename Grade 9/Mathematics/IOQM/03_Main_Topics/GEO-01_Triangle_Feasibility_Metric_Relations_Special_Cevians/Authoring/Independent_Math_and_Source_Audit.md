# GEO-01 Independent Mathematics and Source Audit

Status: `HISTORICAL_ANSWERS_INDEPENDENTLY_CLOSED_PAGE_IMAGE_CUSTODY_PENDING`

All eight historical numerical answers are independently re-derived below from the controlled source statements. The repository verification ledger is used only as a final answer check. Exact page-image/figure custody remains a separate publication gate for the HBCSE-hosted geometry items.

## IOQM-2025-Q04 — isosceles integer triangle, perimeter 23

Let the two equal sides be `a` and the base be `23-2a`.

Positivity gives

`23-2a > 0`, so `a <= 11`.

The only nontrivial triangle inequality is

`23-2a < 2a`,

so

`a > 23/4`, hence `a >= 6`.

Therefore

`a=6,7,8,9,10,11`,

which gives `6` triangles.

Independent result: `06` — PASS.

---

## IOQM-2025-Q09 — possible quadrilateral diagonal

The side lengths are `10,20,50,75`; a proposed diagonal must split them into two pairs so that the diagonal forms a valid triangle with each pair.

For a pair `(p,q)`, the diagonal `d` must satisfy

`|p-q| < d < p+q`.

Test the three pairings:

1. `(10,20)` and `(50,75)` gives
   `10<d<30` and `25<d<125`, hence `25<d<30`;
2. `(10,50)` and `(20,75)` gives
   `40<d<60` and `55<d<95`, hence `55<d<60`;
3. `(10,75)` and `(20,50)` gives
   `65<d<85` and `30<d<70`, hence `65<d<70`.

Among the source candidates, only `28` lies in one admissible interval.

Independent result: `28` — PASS.

---

## IOQM-2024-Q10 — algebraic zero plus triangle feasibility

The source condition reorganizes as

`a^2 + (p^2+9)b^2 + 9c^2 - 6ab - 6pbc`

`= (a-3b)^2 + (pb-3c)^2`.

For this to be zero,

`a=3b`,

and

`c=pb/3`.

Thus the side ratio is

`a:b:c = 3:1:p/3`.

Triangle inequalities reduce to

`3+1 > p/3`, so `p<12`,

and

`1+p/3 > 3`, so `p>6`.

Hence the positive integer values are

`p=7,8,9,10,11`,

five possibilities.

Independent result: `05` — PASS.

---

## IOQM-2024-Q15 — every three chosen numbers form an acute triangle

The set is

`n,n+2,...,n+38`,

and the source explicitly allows choosing three numbers **not necessarily distinct**.

For sides `a<=b<=c`, an acute triangle requires

`c^2 < a^2+b^2`.

The hardest possible choice is therefore

`a=b=n`, `c=n+38`.

So require

`(n+38)^2 < 2n^2`.

This is equivalent to

`n > 38(1+sqrt(2))`.

Since

`38(1+sqrt(2)) ≈ 91.74`,

the least positive integer is

`n=92`.

Independent result: `92` — PASS.

This corrects the stale first-pass corpus mechanism that used two distinct smallest terms.

---

## IOQM-2024-Q22 — right triangle with a divided hypotenuse

Let

`BD=2t`, `DC=t`,

so `BC=3t`. Write

`AB=x`, `AC=y`.

The source relation

`AB+BD=AC+CD`

gives

`x+2t=y+t`,

so

`y=x+t`.

Because the triangle is right-angled at `A`,

`x^2+y^2=(3t)^2`.

Substitute `y=x+t`:

`2x^2+2xt-8t^2=0`,

hence

`x/t = (-1+sqrt(17))/2`.

Therefore

`AC/AB = (x+t)/x`

`= (9+sqrt(17))/8`.

Thus `m=9`, `p=17`, `n=8`, and

`m+n+p = 34`.

Independent result: `34` — PASS.

Key method-selection point: `BD` is first treated as a ratio-marked segment; no median or angle-bisector property is assumed.

---

## IOQM-2024-Q27 — equal angle differences and pedal triangle

Let the three equal successive angle differences at `P` be `delta`. Adding the three angles around `P` gives

`180 degrees + 3 delta = 360 degrees`,

so

`delta=60 degrees`.

Since `angle BAC=30 degrees`, this gives

`angle BPC=90 degrees`.

Let `D,E,F` be the perpendicular feet from `P` to `BC,CA,AB` respectively.

Write

`alpha = angle PBF`,

`theta = angle PCE`.

Because `PDCE` and `PDFB` are cyclic quadrilaterals (each has two right angles), the angle relations at `D` express `angle EDF` in terms of `alpha+theta`. Also

`angle BPC = angle BAC + alpha + theta`.

Since `angle BPC=90 degrees` and `angle BAC=30 degrees`,

`alpha+theta=60 degrees`.

Hence

`angle EDF=60 degrees`.

The same cyclic argument at the other two vertices gives all three angles of `DEF` equal to `60 degrees`; therefore `DEF` is equilateral.

Further, `A,E,P,F` is cyclic with diameter `AP`, because `angle AEP=angle AFP=90 degrees`. With `AP=12`, this circle has radius `6`.

The chord `EF` subtends

`angle EAF=angle BAC=30 degrees`,

so

`EF=2*6*sin 30 degrees=6`.

Thus the area of equilateral `DEF` is

`(sqrt(3)/4)*6^2 = 9sqrt(3)`.

If the source writes this as `m sqrt(n)`, then

`m*n=9*3=27`.

Independent result: `27` — PASS.

---

## IOQM-2024-Q30 — right-triangle altitude 12 with integer hypotenuse and perimeter

Let the legs be `a,c`, hypotenuse `b`, and altitude to the hypotenuse be `12`.

Area gives

`ac=12b`.

Let the integer perimeter be `a+b+c`; because `b` is integer, set

`l=a+c`,

which is also integer.

Now

`l^2 = a^2+c^2+2ac`

`= b^2+24b`.

Hence

`(b+12)^2-l^2=144`,

so

`(b+12-l)(b+12+l)=144`.

Both factors are positive integers of the same parity. To minimize `b`, maximize the smaller factor subject to an ordered factor pair. The admissible pair `(2,72)` gives

`2(b+12)=74`,

so

`b=25`.

This is realized by the `15-20-25` triangle, whose altitude to the hypotenuse is

`15*20/25=12`,

and perimeter is `60`.

Independent result: `25` — PASS.

---

## IOQM-2023-Q13 — exradii reconstruct the triangle

The exradii are

`r_a=21/2`, `r_b=12`, `r_c=14`.

Let

`x=s-a`, `y=s-b`, `z=s-c`.

Since

`Delta = r_a(s-a)=r_b(s-b)=r_c(s-c)`,

we have

`x=Delta/r_a`, `y=Delta/r_b`, `z=Delta/r_c`.

Also

`s=x+y+z`.

Heron's formula gives

`Delta^2=sxyz`.

Substituting the expressions for `x,y,z` yields

`Delta^2 = (r_a r_b r_c)/(1/r_a+1/r_b+1/r_c)`.

With the given values,

`Delta^2=7056`,

so

`Delta=84`.

Therefore

`x=8`, `y=7`, `z=6`.

The side lengths are

`a=y+z=13`,

`b=z+x=14`,

`c=x+y=15`.

If these are roots of

`t^3-pt^2+qt-r=0`,

then

`p=13+14+15=42`,

`q=13*14+14*15+15*13=587`,

`r=13*14*15=2730`.

Thus

`p+q+r=3359`,

and the nearest integer to `sqrt(3359)` is `58`.

Independent result: `58` — PASS.

---

## Audit disposition

- historical numerical answers independently re-derived: 8/8 PASS;
- Q15 repeated-choice source condition explicitly respected: PASS;
- GEO-03 retrieval boundary respected: PASS;
- no hidden NT-04 or GEO-05 chapter introduced: PASS;
- exact HBCSE source page-image/figure custody: `PENDING` due current screenshot-fetch failure;
- 2023 source statement recovered from validated paper custody;
- classroom timing/readability: `NOT_RUN`.

Next authoring gate: build the eight A-P microstream interfaces, then integrate the learner sequence around the router `classify the segment/constraint -> choose the cheapest valid metric relation -> check feasibility`.
