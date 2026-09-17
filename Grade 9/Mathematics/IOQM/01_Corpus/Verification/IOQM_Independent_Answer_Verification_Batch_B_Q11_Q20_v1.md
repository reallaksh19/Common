# IOQM Grade 9 — Independent Answer Verification Batch B

Status: `PASS_30_OF_30__CUMULATIVE_60_OF_90`

Scope: independently recompute Q11–Q20 for IOQM 2023, 2024 and 2025 against the validated paper/key corpus. This is a mathematics check, not a source-key transcription check.

## Result

- verified in this batch: **30/30**;
- answer-key mismatches after independent recomputation: **0**;
- cumulative independently verified: **60/90**;
- key-custody event retained: `IOQM-2025-Q11` is `KEY_CORRECTED` because the final official key corrected the provisional 61 to 26.

## IOQM 2025 — Q11–Q20

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2025-Q11 | 26 | For reduced `a/b != 3/4`, distance is `|4a-3b|/(4b)`. With `b<=15`, the best nonzero determinant is 1 and the largest admissible denominator giving it is `b=15`, `a=11`; `a+b=26`. | PASS |
| IOQM-2025-Q12 | 33 | Exhaust the digit constraints algebraically/finite-state: the maximum digit sum occurs at `75975`, divisible by 75 but not 13; sum `7+5+9+7+5=33`. | PASS |
| IOQM-2025-Q13 | 60 | Put the common side of length 9 on an axis. The two adjacent side vectors from the 30°/90° data give diagonal vectors with dot-product cosine `1/2`; acute angle is 60°. | PASS |
| IOQM-2025-Q14 | 12 | Set `m=0` then `n=0`: `f(1)=2` and `f(k)=k+1`. Hence `sum_{k=1}^N f(k)=N(N+3)/2<100`; largest `N=12`. | PASS |
| IOQM-2025-Q15 | 40 | The three coupon-pairs have allowed envelope sets `{3,4,5,6}`, `{1,2,5,6}`, `{1,2,3,4}` and must use distinct envelopes. Direct restricted-injection count is 40. | PASS |
| IOQM-2025-Q16 | 22 | `h=f-4g` is quadratic and has roots `-2,3`, so `h=k(x+2)(x-3)`. Data at 7 gives `k=1`; at 5, `f(5)=4g(5)+14=22`. | PASS |
| IOQM-2025-Q17 | 23 | Let adjacent sides be `t,1/t`. Area fixes `sin theta=40/41`, so choose `cos theta=-9/41` for the shorter target diagonal. `d²=t²+t^-2-18/41` is minimized at `t=1`, giving `64/41`; `|64-41|=23`. | PASS |
| IOQM-2025-Q18 | 40 | Choose positions of the two 2s in `C(9,2)=36` ways. Among the remaining 3 threes/4 fours, the required event means the final symbol of the 3/4 subsequence is 3: `C(6,2)=15`; `N=540`, remainder 40. | PASS |
| IOQM-2025-Q19 | 29 | Coordinates `B=(0,0), C=(2,0), A=(0,1)` and square side `s` give `d+3s=2` and circle condition `d²+(s-1)²=1`. Nondegenerate solution `s=2/5`; area `4/25`, so `m+n=29`. | PASS |
| IOQM-2025-Q20 | 42 | For `n` coprime to 7, base is periodic mod 7 and exponent mod 6; a universal period must also preserve multiples of 7. Thus the minimal common period is `lcm(7,6)=42`. | PASS |

## IOQM 2024 — Q11–Q20

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2024-Q11 | 12 | Set `x=1/(a+1), y=1/(2b+1), z=1/(3c+1)`. The two supplied equalities force the equality case `x=y=z=2/3`, hence `a=1/2,b=1/4,c=1/6` and `1/a+1/b+1/c=12`. | PASS |
| IOQM-2024-Q12 | 96 | Coordinate square of side 16: the trisection points on `CD` and intersection of `BF` with `AE` give `M=(8,12)`. Thus `[MAB]=16*12/2=96`. | PASS |
| IOQM-2024-Q13 | 19 | First equation rearranges to `(a-b)(c-1)=66`; together with `a+b+c=32` and positive integers with `a>c`, the unique solution is `(19,7,6)`. | PASS |
| IOQM-2024-Q14 | 80 | The initial count is `3^80`; after 80 moves, displacement 79 requires exactly 79 `+1` moves and one zero move. The zero can occur in any of 80 positions, leaving 80 particles at `(79,80)`. | PASS |
| IOQM-2024-Q15 | 92 | Worst acute-triangle test uses sides `n,n,n+38`. Require `(n+38)²<2n²`; the smallest positive integer satisfying it is 92. | PASS |
| IOQM-2024-Q16 | 08 | Solve the equations at `x` and `3-x`: `f(x)=(x²-24x+36)/7`; direct subtraction gives `f(27)-f(25)=8`. | PASS |
| IOQM-2024-Q17 | 25 | Isosceles triangle altitude is `5sqrt(7)`, circumradius `40/sqrt(7)`. The horizontal chord through the midpoint of the altitude has half-length `25/2`; chord length 25. | PASS |
| IOQM-2024-Q18 | 13 | Finite enumeration of two-digit `p,q` with last digit nonzero, `gcd(p,q)=1`, and `p+q | 100p+q` gives maximal printed number `8613`; requested last two digits are 13. | PASS |
| IOQM-2024-Q19 | 12 | Exhaust all `2^10` red/blue colourings of edges of `K5` and reject those with a monochromatic triangle; exactly 12 remain. | PASS |
| IOQM-2024-Q20 | 10 | Breadth-first search on the exact allowed moves `x->2x` and `x->x-3` gives minimum path length 10 from 11 to 121; reverse-state reasoning gives the same lower bound. | PASS |

## IOQM 2023 — Q11–Q20

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2023-Q11 | 14 | Rewrite as `(4m)^2-(8n-5)^2=231`. Factor pairs of 231 give the finite integer solutions; maximum `|m-n|=14`, attained e.g. `(n,m)=(-4,10)` and `(15,29)`. | PASS |
| IOQM-2023-Q12 | 18 | Cube identity gives either `p1+p2+p3=0` or `p1=p2=p3`. The first branch forces even `c`, contradicting odd `c`; equal values force `a=-6,b=11`, and the target is 18. | PASS |
| IOQM-2023-Q13 | 58 | With exradii `21/2,12,14`, Heron/exradius relations give area 84 and `s-a,s-b,s-c = 8,7,6`; sides are `13,14,15`. Then `p=42,q=587,r=2730`; nearest integer to `sqrt(3359)` is 58. | PASS |
| IOQM-2023-Q14 | 40 | Vector setup with `B=0`: `D=2C`, `E=3A-2C`, `F=-3A`, so centroid `K=0`. Since `G=(32,24)`, `GK=40`. | PASS |
| IOQM-2023-Q15 | 03 | Coordinate the unit square. The perimeter condition and circumcentre equations simplify to `(OP/OA)^2=1/2`; hence `m+n=3`. | PASS |
| IOQM-2023-Q16 | 94 | There are 9 diagonals whose colours are free. Exhaust `2^9` choices and reject any all-blue triangle; `N=392`, so digit-square sum `3²+9²+2²=94`. | PASS |
| IOQM-2023-Q17 | 66 | For a uniformly chosen 5-subset of `{1,...,99}`, expected 4th order statistic is `4(100)/6=200/3`; floor is 66. | PASS |
| IOQM-2023-Q18 | 71 | The selected diagonals form an outer-1-planar graph. The sharp outer-1-planar edge bound is `floor(5n/2-4)` including the `n` polygon sides; for `n=50`, selected diagonals are at most `125-4-50=71`, and the standard extremal construction attains it. | PASS |
| IOQM-2023-Q19 | 92 | Squarefree digit product permits nontrivial prime factors 2,3,5,7 at most once. Product 210 and proper divisor digit-sum 105 allow digits `2,3,5,7` plus 88 ones: 92 digits; no larger proper divisor below product allows more. | PASS |
| IOQM-2023-Q20 | 43 | Put `a=|A|, b=|B|`. Then `a|11`, `b|12`, `max A=12/b`, `max B=11/a`. Counting subsets containing their maxima gives `N=439=100*4+39`; requested `4+39=43`. | PASS |

## Gate

Batch B closes Q11–Q20 for all three years. Together with Batch A, **60/90** historical items are independently answer-verified. Q21–Q30 remain gated to Batch C.