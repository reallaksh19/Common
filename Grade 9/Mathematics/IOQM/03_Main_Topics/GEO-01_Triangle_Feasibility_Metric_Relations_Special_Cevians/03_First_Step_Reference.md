# First-Step Reference — Triangle Metric Relations

Use this after the ideas are understood. It is a **routing sheet**, not a formula dump.

## The five-question start

1. **Does the triangle/configuration exist?**
2. **What is the segment: median, altitude, angle bisector, arbitrary cevian, or just a side?**
3. **Is there a cheaper GEO-03 similarity/area route?**
4. **Which metric relation directly targets the unknown?**
5. **Is an integer/discrete filter needed only at the end?**

---

## If two sides and a third segment must form a triangle

Write

`|p-q| < d < p+q`.

**First line:** the strict interval.

Danger: equality is degenerate, not a triangle.

---

## If acute/right/obtuse is asked

Sort `a<=b<=c`, verify feasibility, then write

`c^2 ? a^2+b^2`.

**First line:** identify the largest side.

For “every allowed triple,” maximize `c` and minimize `a,b` subject to the exact selection rule. If repetition is allowed, repeated minima are legal.

---

## If the cevian ends at a midpoint

Use median structure.

If `M` is midpoint of `BC`,

`AB^2+AC^2 = 2(AM^2+BM^2)`.

**First line:** record `BM=CM` before using Apollonius.

---

## If the cevian bisects an angle

Use

`BD/DC = AB/AC`.

**First line:** record `angle BAD = angle DAC`.

Danger: angle bisector does not automatically mean midpoint.

---

## If the cevian is arbitrary

Try the cheapest direct relation first. If no special route closes, map Stewart carefully:

`b^2 m + c^2 n = (m+n)(d^2+mn)`

for `BD=m`, `DC=n`, `AD=d`, `AC=b`, `AB=c`.

**First line:** write the variable map before the formula.

---

## If the triangle is right-angled

Test Pythagoras and right-triangle metric identities before Stewart.

With altitude `h` to hypotenuse `c`, projections `p,q`:

`h^2=pq`, `a^2=cp`, `b^2=cq`, `ab=ch`.

**First line:** identify the hypotenuse and the relevant projection/area relation.

---

## If inradius/exradii/circumradius appear

Route through area:

`Delta=rs`,

`Delta=r_a(s-a)=r_b(s-b)=r_c(s-c)`,

`Delta=abc/(4R)`.

If exradii are given, set

`x=s-a`, `y=s-b`, `z=s-c`.

Then `a=y+z`, `b=z+x`, `c=x+y`.

**First line:** choose the area bridge before expanding side algebra.

---

## If integers appear

Do geometry first.

**First line:** write the real-valued interval/equation. Only then list integers, factor, or optimize over integer choices.

---

## Synthetic or coordinates?

Prefer synthetic metric when a one-step theorem targets the quantity. Test coordinates only when symmetry/right-angle placement makes the equations shorter.

**Rule:** structure first, representation second.

---

## Eight danger signals

1. “The lengths are positive, so a triangle exists.” -> check strict triangle inequality.
2. “That is obviously the largest side.” -> sort explicitly.
3. “The cevian looks like a median.” -> prove midpoint.
4. “The angle bisector cuts the opposite side in half.” -> only in the isosceles special case.
5. “There is a cevian, so use Stewart.” -> special/right-triangle/GEO-03 route may be cheaper.
6. “The problem asks integers, so start listing.” -> continuous geometry first.
7. “The diagram is symmetric.” -> use only stated/proved structure.
8. “The historical answer is verified, so the figure can be redrawn.” -> exact source-page/figure custody is a separate gate.
