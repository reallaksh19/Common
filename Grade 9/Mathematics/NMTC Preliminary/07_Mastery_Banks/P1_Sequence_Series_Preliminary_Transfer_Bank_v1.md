# P1 Sequence & Series — Preliminary Transfer Bank v1

18 original, non-identical transfer items. All are `AUTHOR_CREATED_TRANSFER`, not NMTC PYQs.

## A — AP / term-sum discrimination

### A1
An AP has first term 7 and common difference 4. Find `a_25`.

**Answer:** `103`.

**Solution:** `7+24·4=103`.

### A2
In an AP, `a_8=23` and `a_20=59`. Find `S_30`.

**Answer:** `1365`.

**Solution:** `12d=36`, so `d=3`, `a=2`, `a_30=89`; `S_30=15(2+89)=1365`.

### A3
If `S_n=3n²+2n`, find `a_n`.

**Answer:** `6n-1`.

**Solution:** `a_n=S_n-S_{n-1}=3n²+2n-(3n²-4n+1)=6n-1`.

---

## B — GP / selected terms / high indices

### B1
A GP has `a_3=12`, `a_6=96`. Find `a_10`.

**Answer:** `1536`.

**Solution:** `r³=8`, so `r=2`; `a=3`; `a_10=3·2^9=1536`.

### B2
A GP has `a_2=6`, `a_5=162`. Find `a_20/a_17`.

**Answer:** `27`.

**Solution:** `r³=27`; and `a_20/a_17=r³=27`. No huge powers are needed.

### B3
An infinite GP has sum `12` and the sum of the squares of its terms is `48`. Find `a` and `r`.

**Answer:** `a=6`, `r=1/2`.

**Solution:** `a/(1-r)=12`; `a²/(1-r²)=48`. Substitute `a=12(1-r)` to get `3(1-r)/(1+r)=1`, hence `r=1/2`, `a=6`.

---

## C — weighted / nested accumulation

### C1
Evaluate `Σ_{n=1}^{10} n(2n+1)`.

**Answer:** `825`.

**Solution:** `2Σn²+Σn=2·385+55=825`.

### C2
Evaluate `Σ_{n=1}^{20} n(n+1)`.

**Answer:** `3080`.

**Solution:** `Σn²+Σn=2870+210=3080`.

### C3
Evaluate `Σ_{k=1}^{n} Σ_{j=1}^{k} 1`.

**Answer:** `n(n+1)/2`.

**Solution:** inner sum is `k`; total is `Σk`.

---

## D — recurrence transformation

### D1
`a_{m+n}=a_m+a_n+2mn` for positive integers `m,n`, and `a_1=1`. Find `a_8`.

**Answer:** `64`.

**Solution:** use doubling: `a_2=4`, `a_4=16`, `a_8=64`. Equivalently the relation is consistent with `a_n=n²`.

### D2
`a_1=1` and `a_{n+1}=a_n/(1+a_n)`. Find `a_20`.

**Answer:** `1/20`.

**Solution:** let `b_n=1/a_n`; then `b_{n+1}=b_n+1`, `b_1=1`, so `b_n=n`.

### D3
`a_1=1`, `a_{n+1}=2a_n+3`. Find `a_10`.

**Answer:** `2045`.

**Solution:** let `b_n=a_n+3`; then `b_{n+1}=2b_n`, `b_1=4`, so `b_n=2^{n+1}`; `a_10=2048-3`.

---

## E — telescoping

### E1
Evaluate `Σ_{k=1}^{20} 1/[k(k+1)]`.

**Answer:** `20/21`.

**Solution:** `1/[k(k+1)]=1/k-1/(k+1)`.

### E2
Evaluate `Σ_{k=1}^{24} 1/(sqrt(k)+sqrt(k+1))`.

**Answer:** `4`.

**Solution:** rationalize each term to `sqrt(k+1)-sqrt(k)`; result `sqrt25-sqrt1=4`.

### E3
Evaluate `Σ_{k=1}^{n} 1/[(2k-1)(2k+1)]`.

**Answer:** `n/(2n+1)`.

**Solution:** term is `(1/2)[1/(2k-1)-1/(2k+1)]`.

---

## F — finite differences / mixed structure

### F1
Find the 15th term of `2,6,12,20,30,...`.

**Answer:** `240`.

**Solution:** pattern is `n(n+1)`; `a_15=15·16`.

### F2
Find the 8th term of `1,8,27,64,...`.

**Answer:** `512`.

**Solution:** `a_n=n³`.

### F3
The sequence is `1,-2,3,-4,5,-6,...`. Find `S_100`.

**Answer:** `-50`.

**Solution:** pair terms: `(1-2)+(3-4)+...+(99-100)`, fifty pairs each equal `-1`.

---

## Review state

`MATH_REVIEW: PASS_v1`

Checked independently for term counts, index shifts, convergence, recurrence transforms and telescoping endpoints.

Common error tags:

- `TERM_SUM_CONFUSION`
- `INDEX_SHIFT_OFF_BY_ONE`
- `GP_HIGH_POWER_EXPANDED`
- `INFINITE_GP_CONVERGENCE_OMITTED`
- `WEIGHTED_SUM_NOT_SPLIT`
- `RECURRENCE_TRANSFORM_MISSED`
- `TELESCOPING_ENDPOINT_ERROR`
- `FINITE_DIFFERENCE_CLASSIFICATION_ERROR`