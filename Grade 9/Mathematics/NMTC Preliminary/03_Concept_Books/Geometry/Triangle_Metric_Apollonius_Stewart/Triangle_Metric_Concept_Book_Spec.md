# Triangle Metric Recognition — Concept Book Specification v1

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Performance contract:

`SEGMENT TYPE -> METRIC RELATION -> ELIMINATE -> REDUCE -> CHECK`

The learner should finish believing:

> A median, altitude, angle bisector and general cevian are not four unrelated chapters. They are different constraints on one triangle metric network.

---

# Unit architecture

## Unit 0 — foundations diagnostic

Check without hints:

1. Pythagoras in two adjacent right triangles;
2. algebraic subtraction of squared equations;
3. midpoint/median meaning;
4. ratio interpretation on a segment;
5. basic angle-bisector theorem;
6. right-triangle circumradius `R=hypotenuse/2`;
7. semiperimeter/inradius relation `Delta=rs`.

## Unit 1 — classify the special segment first

Given `AD` from vertex `A` to side `BC`, ask:

- Is `D` midpoint? -> median.
- Is `AD perpendicular BC`? -> altitude.
- Is `angle BAD=angle DAC`? -> angle bisector.
- None of these? -> general cevian.

The segment type determines what extra relation is available.

## Unit 2 — altitude cancellation before heavy theorems

If altitude `AD` meets `BC` at `D`, then:

`AB^2=AD^2+BD^2`

`AC^2=AD^2+CD^2`.

Subtract:

`AB^2-AC^2=BD^2-CD^2`.

The shared altitude disappears.

PYQ anchor: `NMTC-BH-P-2018-Q23`.

Wrong move: solve the altitude first when the target only needs a difference of side squares.

## Unit 3 — derive Stewart, do not memorize it naked

Let:

- `BD=m`, `DC=n`, `BC=a=m+n`;
- `AB=c`, `AC=b`;
- `AD=d`.

Drop an altitude from `A` to line `BC`, write two Pythagorean equations, multiply/eliminate the foot coordinate, and derive:

`b^2 m + c^2 n = a(d^2+mn)`.

Interpretation: Stewart packages the two adjacent right-triangle equations into one cevian identity.

## Unit 4 — Apollonius is Stewart with a midpoint

For median `AD`, `m=n=a/2`.

Substitute into Stewart:

`b^2(a/2)+c^2(a/2)=a[d^2+a^2/4]`.

Divide by `a/2`:

`b^2+c^2=2d^2+a^2/2`.

Therefore

`d^2=(2b^2+2c^2-a^2)/4`.

This is Apollonius.

Clean PYQ evidence: 2019 Q02.

## Unit 5 — median problems: choose theorem vs coordinates/vectors

A median problem with perpendicular medians may be shorter in vectors/coordinates than by repeated scalar formulas.

Decision rule:

- only lengths requested -> Apollonius is often cheapest;
- perpendicularity/direction dominates -> vectors/coordinates may collapse faster;
- mixed constraints -> use whichever creates the fewest unknowns.

## Unit 6 — angle bisector + Stewart

If `AD` bisects angle `A`, angle-bisector theorem gives:

`m/n = c/b`.

With `m+n=a`, solve:

`m=ac/(b+c)`, `n=ab/(b+c)`.

Insert into Stewart to derive:

`d^2 = bc - mn`

and hence

`d^2 = bc[1-a^2/(b+c)^2]`.

The target is understanding where the formula comes from.

## Unit 7 — right-triangle metric bridge

For a right triangle with legs `p,q`, hypotenuse `h`:

`R=h/2`.

Area gives:

`pq/2 = rs`, where `s=(p+q+h)/2`.

Equivalent compact relation:

`r=(p+q-h)/2`.

Use these before trigonometric half-angle formulas when the data are radius-based.

Clean PYQ anchor: 2025 Q06.

## Unit 8 — side-square identities and Stewart contrasts

Train recognition among:

- altitude subtraction;
- median/Apollonius;
- general cevian/Stewart;
- angle-bisector theorem + Stewart;
- cosine law when the included angle is given;
- coordinates when ratios/perpendicularity dominate.

The goal is choosing the cheapest relation, not proving every theorem again during the test.

## Unit 9 — mixed triangle first-move network

Possible triggers:

- `midpoint` -> median;
- `perpendicular` -> Pythagoras / coordinate dot product;
- `bisects angle` -> angle-bisector ratio;
- arbitrary side split + cevian -> Stewart;
- two side-square expressions sharing altitude -> subtract;
- right triangle + `R,r` -> radius metric identities.

## Unit 10 — source-integrity laboratory

Use abstracted 2023 Q02 behavior:

1. a supplied solution invokes a correct theorem;
2. downstream numerical claims conflict with the printed side data;
3. independently recompute;
4. classify `SOURCE_CONFLICT`;
5. do not change the problem silently to make the key work.

---

# ADOPT laboratory

Unlabelled items must force selection among:

- `ALTITUDE SUBTRACTION`;
- `APOLLONIUS`;
- `STEWART`;
- `ANGLE BISECTOR + STEWART`;
- `RIGHT-TRIANGLE R/r`;
- `COORDINATE/VECTOR`;
- `SOURCE CHECK`.

## Mastery standard

Student is internally ready when they can:

1. classify at least 8/10 first moves;
2. reconstruct Stewart/Apollonius logic with labels;
3. solve 7/10 mixed compact metric items;
4. avoid side-label swaps in Stewart;
5. detect one source-conflict case rather than force the supplied result.

## Provenance rule

Author-created geometry problems must be labeled as such. Figure-gated or source-conflicted historical questions remain non-canonical until exact custody is resolved.
