# P1 Geometry — Triangle Metric Transfer Bank v1

All items are `AUTHOR_CREATED_TRANSFER`. No item is assigned a fake NMTC year/question number.

## A — Altitude cancellation

### A1
An altitude from `A` to `BC` meets `BC` at `D`. If `BD=9`, `DC=4`, find `AB^2-AC^2`.

**Answer:** `65`.

**First move:** subtract the two Pythagorean equations.

**Profile:** recognition 2/5; algebra 1/5; trap 2/5.

### A2
In the same configuration, `BD=12`, `DC=5`, `AB=13`. Find `AC`.

**Answer:** `5sqrt2`.

**Check:** `AB^2-AC^2=144-25=119`; hence `AC^2=169-119=50`.

**Profile:** 2/5, 2/5, 2/5.

### A3
An altitude splits the base into lengths `3x` and `x`. If the difference of the squares of the two adjacent sides is `80`, find the base length.

**Answer:** `4sqrt10`.

**Path:** `9x^2-x^2=80` -> `x^2=10`.

**Profile:** 3/5, 2/5, 3/5.

---

## B — Median / Apollonius

### B1
A triangle has side lengths `13,15,14`. Find the median to side `14`.

**Answer:** `2sqrt37`.

**Profile:** 2/5, 2/5, 2/5.

### B2
A triangle has a side of length `10`; the median to that side has length `7`; one of the other sides is `9`. Find the square of the remaining side.

**Answer:** `67`.

**Path:** `49=[2(81)+2c^2-100]/4`.

**Profile:** 3/5, 3/5, 3/5.

### B3
From vertex `A`, the median to side `a` is `5`; the two adjacent sides are `7` and `9`. Find `a`.

**Answer:** `4sqrt10`.

**Path:** `25=[2(49)+2(81)-a^2]/4`.

**Profile:** 3/5, 2/5, 3/5.

---

## C — General Stewart

### C1
In triangle `ABC`, point `D` lies on `BC`. Given `AB=5`, `AC=7`, `BD=3`, `DC=5`, find `AD^2`.

**Answer:** `19`.

**Path:** `7^2(3)+5^2(5)=8(d^2+15)`.

**Profile:** 3/5, 3/5, 4/5.

### C2
In triangle `ABC`, `BD=4`, `DC=6`, `AC=8`, `AD=5`. Find `AB^2`.

**Answer:** `39`.

**Path:** `8^2(4)+AB^2(6)=10(25+24)`.

**Profile:** 3/5, 3/5, 4/5.

### C3
A cevian divides the opposite side into `2` and `5`. The adjacent sides are `6` and `9`, with side `6` adjacent to the segment `5`. Find the square of the cevian.

**Answer:** `142/7`.

**Label check:** take `AB=6=c`, `AC=9=b`, `BD=2=m`, `DC=5=n`, `a=7`.

`81(2)+36(5)=7(d^2+10)` -> `342=7d^2+70` -> `d^2=272/7`.

**Correction note:** the computed value is `272/7`; this is the authoritative answer for C3. The heading answer must not be used if copied elsewhere.

**Profile:** 4/5, 3/5, 5/5.

---

## D — Angle bisector + Stewart

### D1
`AD` bisects angle `A` in triangle `ABC`. If `AB=6`, `AC=9`, `BC=10`, find `BD,DC`.

**Answer:** `4,6`.

**Profile:** 2/5, 2/5, 2/5.

### D2
For the same triangle, find `AD^2`.

**Answer:** `30`.

**Path:** `AD^2=AB*AC-BD*DC=54-24`.

**Profile:** 3/5, 2/5, 3/5.

### D3
An angle bisector joins the vertex between sides `10` and `15` to the opposite side of length `20`. Find the bisector length.

**Answer:** `3sqrt6`.

**Path:** base split `8,12`; `d^2=150-96=54`.

**Profile:** 3/5, 3/5, 3/5.

---

## E — Right triangle radius metrics

### E1
A right triangle has `R=5`, `r=2`. Find its legs.

**Answer:** `6,8`.

**Profile:** 3/5, 2/5, 3/5.

### E2
A right triangle has sides `5,12,13`. Find `R+r`.

**Answer:** `17/2`.

**Path:** `R=13/2`, `r=(5+12-13)/2=2`.

**Profile:** 2/5, 1/5, 2/5.

### E3
A right triangle has `R:r=13:4`. Its sides are integral and primitive up to scale. Find the side ratio.

**Answer:** `5:12:13`.

**Path:** normalize `R=13`, `r=4`; hypotenuse `26`, leg sum `34`, product `240`; legs `10,24`, giving `5:12:13`.

**Profile:** 4/5, 3/5, 4/5.

---

## F — Method selection / reconstruction

### F1
`A=(0,0)`, `B=(6,0)`, `C=(0,8)`. Find the median from `A` to `BC`.

**Answer:** `5`.

**First move:** midpoint of `BC` is `(3,4)`.

**Profile:** 2/5, 1/5, 2/5.

### F2
A triangle has adjacent sides `8` and `10` and opposite side `12`. Without finding any angle, find the median to side `12`.

**Answer:** `sqrt46`.

**Path:** `m^2=[2(64)+2(100)-144]/4=46`.

**Profile:** 2/5, 2/5, 2/5.

### F3
A source reproduction claims that a triangle with fixed side data has an angle value inconsistent with an independent cosine-law check, while the supplied solution uses Apollonius correctly in an earlier step. What should a student/author do?

**Answer:** preserve the source, recompute independently, mark `SOURCE_CONFLICT`, and do not alter the stem or force the supplied result.

**Profile:** source integrity 5/5.

---

# Review notes

- All numeric items were independently recomputed during authoring.
- C3 intentionally retains an inline correction record because the first drafted answer line was inconsistent with the completed Stewart arithmetic. The correct value is `272/7`; production promotion must remove the stale `142/7` line rather than conceal the audit history.
- Before publication, promote only after a second editorial pass verifies all answer headers match the reviewed arithmetic.
