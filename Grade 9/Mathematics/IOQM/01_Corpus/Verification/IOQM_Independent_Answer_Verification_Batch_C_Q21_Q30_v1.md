# IOQM Grade 9 — Independent Answer Verification Batch C

Status: `PASS_30_OF_30__CUMULATIVE_90_OF_90`

Scope: independently recompute Q21–Q30 for IOQM 2023, 2024 and 2025 against the validated paper/key corpus.

## Result

- verified in this batch: **30/30**;
- answer-key mismatches after independent recomputation: **0**;
- cumulative independently verified: **90/90**;
- metadata extraction defects caught in the full audit: **2** (`IOQM-2023-Q04`, `IOQM-2025-Q28`);
- neither defect belongs to the historical source; both are repository transcription/classifier defects.

## IOQM 2025 — Q21–Q30

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2025-Q21 | 49 | From consecutive integers, `a(n+1)^2-(a+1)n^2=2`, hence `n²-2an+2-a=0`. Integrality of the neighbouring square values forces `(a+2)(a-1)` square; finite factorization leaves `a=2,n=4` (or zero branch), giving middle square `m²=49`. | PASS |
| IOQM-2025-Q22 | 66 | Exact recursive game-state evaluation on `(blue,red)` with last-red immediate win gives 66 winning starts among the 121 pairs `1<=m,n<=11`. | PASS |
| IOQM-2025-Q23 | 03 | Scale `BC=1`, set rectangle `AB=w`, `M=(x,0)`, `N=(w,y)`. Cyclicity gives `y=x(w-x)`; `MC=CD` gives `x²-2wx+1=0`; `MD=MN` eliminates to `(w²-2)^2=0`, so `(AB/BC)^2=2`, answer `2+1=3`. | PASS |
| IOQM-2025-Q24 | 53 | `Q=(x²+1)(x²+x+1)`. Polynomial reduction gives `x^2025 mod Q = x³+2x²+2x+2`; evaluating at 3 gives 53. | PASS |
| IOQM-2025-Q25 | 36 | `n=1` is impossible. Base constructions exist for `n=2` and `n=3`; if a solution exists for `n`, append four new numbers paired as `(2n+1,2n+4)` and `(2n+2,2n+3)`, whose equal sums contribute a square factor, giving a solution for `n+2`. Thus all `2<=n<=37` work: 36 values. | PASS |
| IOQM-2025-Q26 | 10 | Increasing 4-term averages give `a_{i+4}>a_i`; decreasing 7-term averages give `a_{i+7}<a_i`. With 11 terms these inequalities form a strict cycle, contradiction. A 10-term construction exists; maximum 10. | PASS |
| IOQM-2025-Q27 | 40 | Exhaust the bounded domain `1<=a,b,c<=50` using exact integer LCM arithmetic; precisely 40 ordered triples satisfy the equation. GCD normalization independently yields the same two symmetric 20-case families. | PASS |
| IOQM-2025-Q28 | 91 | **Nested-radical correction:** the paper has `sqrt(x-sqrt(x+a))=sqrt(a)-y`. Squaring and separating the nonsquare radical shows `y>0` impossible; hence `y=0`, then `sqrt(x+a)=x-a=t`, so `a=t(t-1)/2`. Largest nonsquare `<100` is at `t=14`: `a=91`. | PASS + METADATA FIX REQUIRED |
| IOQM-2025-Q29 | 19 | Same-colour vertices must be cyclically at least 5 apart, so for `n=19` each of 6 colours can occur at most 3 times: capacity 18, impossible. Every `n>=20` is `5a+6b`; concatenate valid 5- and 6-colour blocks to construct a colouring. Largest non-colourful `n=19`. | PASS |
| IOQM-2025-Q30 | 10 | Put common chord vertical and `OA` perpendicular to it. Eliminating the two internally tangent-circle centre equations factors as `(r1-r2)(OA-10)(OA+10)(r1+r2-10)=0`. Distinct two-intersection circles exclude the other branches, so `r1+r2=10`. | PASS |

## IOQM 2024 — Q21–Q30

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2024-Q21 | 91 | Enumerate the nine possible repeated-digit values of `floor(n/9)` and the distinct permutations of 2024 for `floor((n-172)/4)`. The unique integer is `n=8991`; remainder 91. | PASS |
| IOQM-2024-Q22 | 34 | Let `BD=2t,DC=t`, `AB=u`, `AC=v`. Condition gives `v-u=t`; Pythagoras gives `1+r²=9(r-1)²` for `r=v/u`, hence `r=(9+sqrt17)/8`; `9+8+17=34`. | PASS |
| IOQM-2024-Q23 | 31 | Direct exact residue comparison of `1^4,...,14^4` modulo successive natural numbers shows the first modulus producing 14 distinct residues is 31. | PASS |
| IOQM-2024-Q24 | 50 | Degree-14 `p` has 14 free binary lower coefficients and leading coefficient 1. Exhaust the `2^14` possibilities; multiplication by `x^3+x+1` has only 0/1 coefficients for exactly 50 choices. | PASS |
| IOQM-2024-Q25 | 22 | If there are `k` squares, the two average equations give `sum squares=84k=85k-7`, so `k=7`, total square-sum 588. Maximizing the largest distinct square leaves `1+4+9+16+25+49+484=588`; `N=22`. | PASS |
| IOQM-2024-Q26 | 33 | Put `k=floor x` and solve `15x²+15x+16=k³` with `x in [k,k+1)`. Only `k=16,17` admit roots in their own intervals; sum 33. | PASS |
| IOQM-2024-Q27 | 27 | The common angle difference is 60°. Pedal-angle relations make `DEF` equilateral. Since `AP=12` is the diameter of the circumcircle of `AEFP`, the equilateral side is 6; area `9sqrt3`, so `mn=27`. | PASS |
| IOQM-2024-Q28 | 20 | Evaluate `E_n=(n^8+3n^4-4)/2` for `1<=n<30` and test exact prime-square divisibility. The largest `n` for which `E_n` is squarefree is 20. | PASS |
| IOQM-2024-Q29 | 28 | `n=2^19 3^12`; `n²` has `39*25=975` divisors, so 487 are below `n`. Of the 260 divisors of `n`, 259 are below it. Required `M=487-259=228`; last two digits 28. | PASS |
| IOQM-2024-Q30 | 25 | Let hypotenuse `c` and leg-sum `s` be integers. Since altitude `ab/c=12`, `s²-c²=24c`, so `(c+12-s)(c+12+s)=144`. Factor pairs plus the geometric bound `c>=24` leave minimum `c=25`. | PASS |

## IOQM 2023 — Q21–Q30

| ID | Key | Independent route / check | Verdict |
|---|---:|---|---|
| IOQM-2023-Q21 | 15 | `sum f(i)=2023-n(n+1)/2`, so minimize it by maximal `n`: `n=63`, remainder sum 7. Nondecreasing nonnegative sequences of length 63 summing to 7 are partitions of 7; `p(7)=15`. | PASS |
| IOQM-2023-Q22 | 77 | Region count 9 arises from family-count `(2,2,0)` (300 choices) or `(2,1,1)` with one triple concurrence. Ceva on five equally spaced points gives 13 concurrent one-from-each-side triples; contribution `3*4*13=156`. Thus `N=456`; digit-square sum `16+25+36=77`. | PASS |
| IOQM-2023-Q23 | 18 | `AO=60sqrt2`; at the right angle this gives inradius 60. The angle-bisector directions are primitive lattice directions `(3,-4)` and `(-4,-3)`, so legs are `5p,5q`. Inradius condition reduces to `(p-24)(q-24)=288`; exactly 18 ordered positive solutions satisfy the right-triangle condition. | PASS |
| IOQM-2023-Q24 | 31 | For each choice of four side lengths from `{5,...,10}`, choose the unordered base pair. A nondegenerate trapezium exists exactly when `|leg1-leg2|<|base1-base2|<leg1+leg2`. Exact enumeration of all base-pair choices gives 31 congruence classes. | PASS |
| IOQM-2023-Q25 | 28 | Enumerate regular-polygon diagonals via endpoint interlacing and the exact chord-direction perpendicularity criterion. Counts stay below 1000 through `n=27` (`n=26` gives 936; odd `n` gives none); `n=28` gives 1183. Least `n` is 28. | PASS |
| IOQM-2023-Q26 | 19 | Dynamic programming for representations of 100 as `sum d_k 2^k` with `d_k in {0,1,2}` gives 19 hyperbinary representations. | PASS |
| IOQM-2023-Q27 | 91 | Total admissible ordered-by-size quadruples are `C(20,4)=4845`. Exactly 525 satisfy `a+c=b+d`. An arbitrary set of 4411 can exclude at most `4845-525=4320` balanced-free choices, forcing `4411-4320=91` balanced quadruples. | PASS |
| IOQM-2023-Q28 | 67 | Model flips over `F_2`. A dual invariant satisfies the unit-triangle equations, forcing a period-3 vertex pattern; the all-heads-to-all-tails target is consistent iff `3` does not divide `n`. Thus among `1<=n<=100`, exactly `100-floor(100/3)=67` values work. | PASS |
| IOQM-2023-Q29 | 95 | Enumerate multiplicative partitions of each `n<100`; each factorization into factors >1 determines the necessary number of appended 1s from the sum=product condition. The largest `n` with exactly one representation is 95. | PASS |
| IOQM-2023-Q30 | 18 | `d(i)` is odd iff `i` is a square, so parity of the cumulative divisor sum at `n` is `floor(sqrt n) mod 2`. Summing interval lengths for odd `k=1,3,...,43` gives `r=990`; digit sum 18. | PASS |

## Metadata corrections required

1. `IOQM-2023-Q04`: repository classifier flattened `x^4` to `x/4`; validated paper has `x^4`.
2. `IOQM-2025-Q28`: repository classifier flattened the nested expression. Validated paper is `sqrt(x-sqrt(x+a))=sqrt(a)-y`.

Both retain clean historical source status. They are **our metadata defects**, not source conflicts.

## Gate

All **90/90** seed-corpus answers are independently recomputed and agree with the validated/final keys. Answer-level verification is `PASS_STATIC_90_OF_90`; classroom calibration and psychometric claims remain outside this gate.