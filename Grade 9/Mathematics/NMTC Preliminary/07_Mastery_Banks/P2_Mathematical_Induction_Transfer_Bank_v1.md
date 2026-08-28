# P2 Mathematical Induction — Transfer Bank v1

All items are `AUTHOR_CREATED_TRANSFER` unless marked otherwise.

## A — Statement, domain and base

### A1
State `P(n)` precisely for the claim `1+3+...+(2n-1)=n^2`.

**Answer:** `P(n): 1+3+...+(2n-1)=n^2` for integers `n>=1`.

### A2
A claim is asserted for every integer `n>=4`. What is the correct base case?

**Answer:** `P(4)`.

### A3
A proof establishes `P(k)->P(k+2)`. What minimum base information is needed to reach all integers `n>=1`?

**Answer:** at least `P(1)` and `P(2)`.

---

## B — Sum identities

### B1
Prove by induction that `2+4+...+2n=n(n+1)` for `n>=1`.

**Solution:** base `n=1`: `2=2`. Assume `S_k=k(k+1)`. Then `S_{k+1}=k(k+1)+2(k+1)=(k+1)(k+2)`.

### B2
Prove `1+3+...+(2n-1)=n^2`.

**Solution:** base 1. If `S_k=k^2`, then `S_{k+1}=k^2+2k+1=(k+1)^2`.

### B3
Prove `1^2+2^2+...+n^2=n(n+1)(2n+1)/6`.

**Solution:** assume formula at k. Add `(k+1)^2`:
`k(k+1)(2k+1)/6+(k+1)^2=(k+1)[k(2k+1)+6(k+1)]/6=(k+1)(k+2)(2k+3)/6`.

---

## C — Divisibility

### C1
Prove `7 | (8^n-1)` for `n>=1`.

**Solution:** base gives 7. If `8^k-1` is divisible by 7, then `8^(k+1)-1=8(8^k-1)+7`.

### C2
Prove `8 | (3^(2n)-1)` for `n>=1`.

**Solution:** write `9^n-1`. Base `8`. If divisible for k, then `9^(k+1)-1=9(9^k-1)+8`.

### C3
Prove `11 | (12^n-1)` for `n>=1`.

**Solution:** `12^(k+1)-1=12(12^k-1)+11`.

---

## D — Inequalities

### D1
Prove `2^n>=n+1` for integers `n>=0`.

**Solution:** base `n=0`. If `2^k>=k+1`, then `2^(k+1)>=2k+2>=k+2` for `k>=0`.

### D2
Prove `n!>=2^(n-1)` for integers `n>=1`.

**Solution:** base `1=1`. Assume `k!>=2^(k-1)`. Then `(k+1)!=(k+1)k!>=(k+1)2^(k-1)>=2^k` since `k+1>=2`.

### D3
Prove `3^n>n^2` for `n>=2`.

**Solution:** base `9>4`. Assume `3^k>k^2`. Then `3^(k+1)>3k^2`; for `k>=2`, `3k^2-(k+1)^2=2k^2-2k-1>0`.

---

## E — Recurrence / multiple previous cases

### E1
Given `a_1=2`, `a_{n+1}=2a_n+1`, prove `a_n=3*2^(n-1)-1`.

**Solution:** base 1. Substitute IH into recurrence: `a_{k+1}=2[3*2^(k-1)-1]+1=3*2^k-1`.

### E2
Let `a_1=1,a_2=2`, and `a_{n+2}=a_{n+1}+2a_n`. Prove `a_n=2^(n-1)` for all `n>=1`.

**Solution:** bases `n=1,2`. Assuming formulas for k and k+1, `a_{k+2}=2^k+2*2^(k-1)=2^(k+1)`.

### E3
Why are two base cases natural in E2?

**Answer:** the recurrence uses two previous terms, so the induction step requires two consecutive established cases.

---

## F — Proof audit and method selection

### F1
A proof checks `P(1)` and proves `P(k)->P(k+2)`, then concludes all positive integers. Diagnose.

**Answer:** invalid coverage; only the odd chain is established. Need `P(2)` as well.

### F2
A student proves `6 | (n^3-n)` by induction. Give a shorter direct proof.

**Answer:** `n^3-n=n(n-1)(n+1)` is a product of three consecutive integers, hence divisible by 2 and 3, therefore by 6.

### F3
A worksheet labels one of these author-created items `NMTC 2024 Q31`. What is the correct action?

**Answer:** remove the fabricated attribution, retain the item as author-created, and require an actual source locator before historical labeling.

---

# Second-review checklist

- B3 factorization checked.
- C1–C3 next-case decompositions checked.
- D1 domain starts at 0.
- D2 uses `k+1>=2` for `k>=1`.
- D3 threshold `n>=2` checked.
- E2 bases and recurrence arithmetic checked.

`MATH_REVIEW: PASS_INTERNAL`
