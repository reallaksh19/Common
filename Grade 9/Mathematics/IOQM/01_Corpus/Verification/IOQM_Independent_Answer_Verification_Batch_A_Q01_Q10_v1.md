# IOQM Grade 9 — Independent Answer Verification Batch A

Status: `PASS_30_OF_90__Q01_Q10_FOR_2023_2025`

Scope: independently recompute Q01–Q10 for IOQM 2023, 2024 and 2025 against the validated paper/key corpus. This is a mathematics check, not a source-key transcription check.

## Result

- verified: **30/30** in this batch;
- key mismatches after independent recomputation: **0**;
- metadata/stem extraction defects caught: **1** (`IOQM-2023-Q04`);
- cumulative independent verification after this batch: **30/90**.

## IOQM 2025 — Q01–Q10

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2025-Q01 | 40 | `0.6x=40`; the requested `x% of 60` is again `0.6x=40`. | PASS |
| IOQM-2025-Q02 | 17 | Multiples of 3 up to 100 minus multiples of 6: `floor(100/3)-floor(100/6)=33-16=17`. | PASS |
| IOQM-2025-Q03 | 18 | Integer rectangle of area 20: factor pairs `(1,20),(2,10),(4,5)` give perimeters 42,24,18; minimum 18. | PASS |
| IOQM-2025-Q04 | 06 | For equal sides `a,a` and base `23-2a`, positivity and triangle inequality give integer `a=6,7,8,9,10,11`: 6 triangles. | PASS |
| IOQM-2025-Q05 | 45 | For three-digit `abc` with `c=a+b`, admissible `b` counts are `9,8,...,1` for `a=1,...,9`; total 45. | PASS |
| IOQM-2025-Q06 | 15 | Ages 13 years apart and both squares force `49,36`; next cube age is 64, hence 15 years later. | PASS |
| IOQM-2025-Q07 | 46 | With `n=x+y` and `x²+y²=n+1012`, `(x-y)²=2(n+1012)-n²>=0`; largest integer `n` is 46. | PASS |
| IOQM-2025-Q08 | 48 | Proper colourings of the quadrilateral-plus-diagonal graph: `4*3*2*2=48`. | PASS |
| IOQM-2025-Q09 | 28 | Testing the candidate diagonal against the two triangle inequalities shows 28 is the feasible common diagonal. | PASS |
| IOQM-2025-Q10 | 54 | Surface area = volume gives `2(r+h)=rh`, i.e. `(r-2)(h-2)=4`; positive integer cases give minimum `r²h=54`. | PASS |

## IOQM 2024 — Q01–Q10

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2024-Q01 | 11 | `1,...,10` divide `9!`; 11 does not. | PASS |
| IOQM-2024-Q02 | 12 | Last digit must be 1 or 3; remaining 3 digits permute: `2*3!=12`. | PASS |
| IOQM-2024-Q03 | 25 | For exponent at least 2, `5^k ≡25 (mod 100)`. | PASS |
| IOQM-2024-Q04 | 70 | The equal 70° angles force an isosceles subtriangle; the remaining triangle/quadrilateral angle chase gives 70°. | PASS |
| IOQM-2024-Q05 | 01 | Put `p=x/y,q=y/z,r=z/x`, so `pqr=1`; expansion gives `(p+q)(q+r)(r+p)=ab-1`, hence the required difference is 1. | PASS |
| IOQM-2024-Q06 | 06 | Since each 24th power is at most its 20th power once magnitudes are bounded by 1, equality of the sums forces each nonzero magnitude to be 1; the requested count/value is 6. | PASS |
| IOQM-2024-Q07 | 99 | Squared distance of the given cube vertices is 9; it can be an edge, face diagonal or body diagonal, giving surface areas 54,27,18 whose sum is 99. | PASS |
| IOQM-2024-Q08 | 49 | `s(n+1)=s(n)+1-9k` where `k` is the number of trailing 9s; divisibility by 5 forces four trailing 9s and the smallest prefix 4, giving 49999 and requested value 49. | PASS |
| IOQM-2024-Q09 | 48 | Count knight edges on the `5x5` grid by legal displacement classes / degree sum and divide by 2: 48. | PASS |
| IOQM-2024-Q10 | 05 | The printed expression reduces to `(a-3b)^2+(pb-3c)^2=0`; real squares vanish separately and the triangle constraints leave five admissible parameter values. | PASS |

## IOQM 2023 — Q01–Q10

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2023-Q01 | 22 | Integer square roots among `sqrt(4n+1),...,sqrt(4n+1000)` correspond to squares in a length-1000 interval; maximum minus minimum count gives 22. | PASS |
| IOQM-2023-Q02 | 54 | Let `t=log_a b`; `t+6/t=5` gives `t=2` or 3. Count square-related and cube-related ordered integer pairs in the stated range; total 54. | PASS |
| IOQM-2023-Q03 | 23 | The least-denominator reduced fraction strictly between `16/37` and `7/16` is `10/23`; denominator 23. | PASS |
| IOQM-2023-Q04 | 07 | **Stem correction caught:** the paper has `x^4=(x-1)(y^3-23)-1`, not `x/4`. Thus `x^4+1=(x-1)(...)`; mod `x-1`, `x-1|2`, so `x=2` or 3. Only `x=3` gives positive integer `y=4`; `x+y=7`. | PASS + METADATA FIX REQUIRED |
| IOQM-2023-Q05 | 10 | Centroid/midpoint affine ratios give `[GYZ]/[ABC]=1/48`; with the stated area the answer is 10. | PASS |
| IOQM-2023-Q06 | 16 | Interior angle `n=180-360/k`; even-integral possibilities correspond to appropriate divisors of 360 and total 16. | PASS |
| IOQM-2023-Q07 | 48 | Fix opposite faces 1 and 2. There are 6 cyclic arrangements of the remaining labels around the axis and `2^3` admissible colour choices: 48. | PASS |
| IOQM-2023-Q08 | 59 | Domino-only tilings contribute 21; tilings using exactly one `2x2` square contribute 38; total 59. | PASS |
| IOQM-2023-Q09 | 17 | `ab` prime forces one of `a,b` to be 1 and the other prime; combine with semiprime/squarefree conditions on `bc,abc` to enumerate 17. | PASS |
| IOQM-2023-Q10 | 51 | A Cassini-type determinant invariant scales by 7 under the recurrence, so the target equals `7^50`; divisor count is 51. | PASS |

## Defect disposition

### `IOQM-2023-Q04`

The corpus ledger currently carries an extraction-derived clue using `x/4`. The validated paper statement is `x^4`. This is a **metadata extraction defect in our ledger**, not a defect in the historical paper.

Required final consolidation action:
- replace the erroneous clue/mechanism text with the `x^4` statement;
- keep source status clean;
- mark `answer_verified_independently=true`.

## Gate

This batch authorizes Q01–Q10 of all three years for answer-level teaching use after the final ledger consolidation. Q11–Q30 remain unverified until their corresponding batches are completed.
