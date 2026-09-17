# Recognition and First-Line Lab — GEO-01

Status: `LEARNER_LAB_V1`

For each item, do **not** solve fully on the first pass. Record only:

1. the structure you recognize;
2. the first legal line you would write;
3. one attractive wrong route you are rejecting.

---

## A. Feasibility recognition

### R1
Two sides of a triangle are `11` and `17`; the third side is `x`.

Recognition target: feasibility interval.

First line: `6<x<28`.

Reject: `x>0` alone.

### R2
A quadrilateral has side lengths `8,13,21,30`. A proposed diagonal `d` separates the pairs `(8,13)` and `(21,30)`.

Recognition target: intersection of two triangle intervals.

First line: `5<d<21` and `9<d<51`.

Reject: testing only one triangle.

---

## B. Acute/right/obtuse recognition

### R3
A triangle has side lengths `9,12,15`.

Recognition target: largest-side square test.

First line: `15^2 ? 9^2+12^2`.

Reject: comparing an arbitrary side square.

### R4
Every allowed triple is required to be acute. The allowed numbers come from an interval-like finite set and repetition is permitted.

Recognition target: extremal triple under exact selection semantics.

First line: choose the largest legal `c` and the two smallest legal `a,b`, allowing `a=b` if the source permits repetition.

Reject: silently forcing distinct choices.

---

## C. Cevian classification

### R5
`D` lies on `BC` and `BD=DC`.

Recognition target: median.

First line: `AD` is a median because `D` is the midpoint of `BC`.

Reject: angle-bisector theorem without angle information.

### R6
`D` lies on `BC` and `BD:DC=3:2`; no angle or midpoint condition is given.

Recognition target: arbitrary cevian with known split.

First line: record the split only.

Reject: calling `AD` a median or angle bisector.

### R7
`angle BAD=angle DAC`.

Recognition target: angle bisector.

First line: `BD/DC=AB/AC`.

Reject: `BD=DC` unless additionally proved.

---

## D. Method selection

### R8
A cevian is a median and the target is its length from the three side lengths.

Recognition target: Apollonius.

First line: `AB^2+AC^2=2(AM^2+BM^2)`.

Reject: Stewart as first choice.

### R9
An arbitrary cevian has known split `m:n`, and all three side lengths are known.

Recognition target: Stewart fallback.

First line: map `BD=m`, `DC=n`, `AD=d`, `AC=b`, `AB=c`.

Reject: writing Stewart before fixing the variable correspondence.

### R10
A right triangle has an altitude to the hypotenuse and the target involves the two hypotenuse projections.

Recognition target: right-triangle metric package.

First line: `h^2=pq`.

Reject: using Stewart merely because an interior segment appears.

---

## E. Radius bridges

### R11
The three exradii are known and the sides are requested.

Recognition target: semiperimeter complements.

First line: `x=s-a=Delta/r_a`, `y=s-b=Delta/r_b`, `z=s-c=Delta/r_c`.

Reject: guessing side order directly from exradius order.

### R12
The inradius and semiperimeter are known.

Recognition target: area bridge.

First line: `Delta=rs`.

Reject: Heron expansion before using the direct bridge.

---

## F. Integer filters

### R13
An integer side must lie in the feasible interval `7<x<19`.

Recognition target: terminal integer filtering.

First line: derive/confirm the interval before listing `8,...,18`.

Reject: listing candidates before geometry.

### R14
A metric equation becomes `(N-u)(N+u)=144` with integer variables and positivity constraints.

Recognition target: factor-pair filter after geometry.

First line: state parity/order/positivity restrictions on the factor pair.

Reject: accepting every divisor pair of `144`.

---

## G. Retrieval vs new theorem

### R15
Parallel lines create two similar triangles and the target is a side ratio.

Recognition target: retrieve GEO-03.

First line: identify the corresponding triangles and similarity criterion.

Reject: Stewart.

### R16
The diagram is numerical, right-angled, and naturally axis-aligned; a synthetic metric route is four lines while coordinates would be two equations.

Recognition target: representation choice.

First line: state the geometric structure, then choose coordinates if genuinely shorter.

Reject: coordinates as an automatic default.

---

## First-Line Sprint

Write only the first line for each cue.

1. two fixed sides `p,q`, third side `d` -> `|p-q|<d<p+q`.
2. triangle type by side lengths -> sort and write `c^2 ? a^2+b^2`.
3. midpoint `M` on `BC` -> `BM=CM`.
4. angle bisector `AD` -> `BD/DC=AB/AC`.
5. arbitrary cevian -> write the Stewart variable map.
6. right-triangle altitude -> identify `h^2=pq` or the direct area relation.
7. exradii -> `Delta=r_a(s-a)=r_b(s-b)=r_c(s-c)`.
8. integer answer requested -> write the continuous geometric constraint first.

The learner passes this lab only if the first line is legal **before** any heavy algebra begins.
