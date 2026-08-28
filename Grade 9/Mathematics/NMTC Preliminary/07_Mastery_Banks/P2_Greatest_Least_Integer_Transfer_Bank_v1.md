# P2 Greatest / Least Integer Functions — Transfer Bank v1

All items are `AUTHOR_CREATED_TRANSFER` except the final source-QC classification item. No fake NMTC year/question numbers are assigned.

## A — Direct interval translation

### A1
Solve `floor(3x-1)=5`.

**Answer:** `2<=x<7/3`.

### A2
Solve `ceil(2x+3)=0`.

**Answer:** `-2<x<=-3/2`.

### A3
Solve `floor(x^2)=4`.

**Answer:** `(-sqrt5,-2] union [2,sqrt5)`.

---

## B — Negative values and fractional part

### B1
For `x=-17/5`, find `floor(x)`, `ceil(x)` and `{x}`.

**Answer:** `-4,-3,3/5`.

### B2
Find all `x` in `[-2,2)` satisfying `{x}=1/4`.

**Answer:** `-7/4,-3/4,1/4,5/4`.

### B3
If `x` is not an integer, evaluate `floor(x)+floor(-x)`.

**Answer:** `-1`.

---

## C — x coupled to its floor

### C1
Solve `x+floor(x)=9/2`.

**Answer:** `x=5/2`.

**Check:** take `n=floor(x)`; `x=9/2-n`; interval consistency forces `n=2`.

### C2
Solve `2x-floor(x)=7`.

**Answer:** `x=13/2` or `x=7`.

**Check:** with `n=floor(x)`, consistency gives `n=6,7`.

### C3
Solve `floor(x)=floor(2x)`.

**Answer:** `-1/2<=x<1/2`.

**Path:** write `x=n+r`, `0<=r<1`; compare `n` with `2n+floor(2r)`.

---

## D — Sum identities

### D1
Evaluate `floor(2.7)+floor(-2.7)`.

**Answer:** `-1`.

### D2
Prove `floor(x)+floor(x+1/2)=floor(2x)` for all real `x`.

**Answer path:** write `x=n+r`, split `0<=r<1/2` and `1/2<=r<1`.

### D3
Give the exact condition for

`floor(x)+floor(y)=floor(x+y)`.

**Answer:** `{x}+{y}<1`.

---

## E — Integer counting

### E1
How many integers lie in `(-3.2,7.8]`?

**Answer:** `11` (`-3` through `7`).

### E2
How many positive integers `n` satisfy `floor(sqrt(n))=8`?

**Answer:** `17` (`64` through `80`).

### E3
How many integers `x` satisfy `floor((x+1)/3)=2`?

**Answer:** `3` (`5,6,7`).

---

## F — Ceiling and transfer bridges

### F1
A vehicle carries at most 12 students. What is the minimum number of vehicles required for 137 students?

**Answer:** `ceil(137/12)=12`.

### F2
Solve `ceil(sqrt(x))=6` for real `x>=0`.

**Answer:** `25<x<=36`.

### F3 — source classification
A qualified Preliminary GP problem performs substantial GP algebra and then takes the floor of the final real quantity. Should it be counted as a canonical Greatest Integer Function PYQ?

**Answer:** No. It is `BRIDGE_EVIDENCE`; the primary mechanism is GP. Preserve it as a transfer bridge without inflating floor-function recurrence.

---

# Second-math review

Checked independently:

- A1/A2 endpoint orientation;
- A3 square inequality and endpoint inclusion;
- B1 negative floor/fractional part;
- B2 bounded integer shifts;
- C1/C2 interval consistency;
- C3 both `n=0` and `n=-1` cases;
- D2 split exactly at `r=1/2`;
- E2 count `81-64=17`;
- F2 strict lower / closed upper boundary.

`SECOND_MATH_PASS: PASS`
