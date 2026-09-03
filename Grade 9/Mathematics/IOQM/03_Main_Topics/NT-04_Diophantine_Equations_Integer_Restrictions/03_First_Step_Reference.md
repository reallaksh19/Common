# First-Step Reference - Diophantine Equations & Integer Restrictions

## Recognition atlas
| Visible clue | Structural question | First useful line |
|---|---|---|
| linear integer equation `ax+by=c` | does `gcd(a,b)` divide `c`? | retrieve NT-01 Bézout/extended-Euclid solvability before parameterizing |
| product/shifted product equals constant | are factors integral? | set factors equal to divisor pair |
| difference of squares | what parity must factor pair have? | `(x-y)(x+y)=N` |
| fixed product + gcd 1 | can prime-power blocks split? | allocate whole blocks |
| consecutive positive-integer sum | does NT-03's odd-divisor criterion allow a representation? | write `2n=r(2a+r-1)` and reconstruct admissible factor pairs |
| integer maximum/minimum | can I bound before listing? | locate feasible factor pair near real optimum |
| fraction near p/q | is scaled error an integer? | write the exact cross-product gap and retrieve Bézout when a minimal linear combination is relevant |
| sum and product | is target symmetric? | use `S,P` invariants or `t^2-St+P` |
| quadratic must have integer root | is discriminant a square? | `D=b^2-4ac=k^2` |
| many variables + fixed sum | can one variable be eliminated? | substitute side condition immediately |
| finite candidates | have I proved completeness? | state case-to-solution correspondence |

## Linear Diophantine bridge: retrieve, then reconstruct

NT-01 owns the theorem/algorithmic bridge:

`ax+by=c` has integer solutions iff `gcd(a,b)|c`.

If this test fails, stop. If it passes, retrieve one Bézout solution and then NT-04 owns the reconstruction step.

Let `g=gcd(a,b)` and suppose `(x0,y0)` is one solution of `ax+by=c`. Then every integer solution is

`x = x0 + (b/g)t`,

`y = y0 - (a/g)t`,

for integer `t`.

Now impose the actual problem's positivity, bounds, ordering, coprimality or optimization constraints on `t`.

### Decision boundary

- Need only existence / one Bézout certificate -> retrieve NT-01.
- Need all integer solutions or bounded/positive solutions -> stay in NT-04 and parameterize/filter.

## Consecutive-sum reconstruction

NT-03 exports the structural existence criterion:

> A positive integer is a sum of at least two consecutive positive integers iff it is not a power of `2`.

For actual reconstruction, write

`n = a+(a+1)+...+(a+r-1) = r(2a+r-1)/2`,

so

`2n = r(2a+r-1)`.

The factors `r` and `2a+r-1` have opposite parity. For each admissible factor choice `r | 2n`, recover

`a = ((2n/r)-r+1)/2`.

Keep the case only if:

- `a` is an integer;
- `a>=1`;
- `r>=2`;
- all extra problem restrictions hold.

This gives a complete factor-pair-to-sequence correspondence rather than a brute-force scan of starting values.

## Rational approximation and Bézout boundary

For fractions `a/b` near `p/q`,

`|p/q-a/b| = |pb-qa|/(qb)`.

The numerator is an integer linear combination. If `gcd(p,q)=1`, Bézout explains why the smallest possible nonzero determinant is `1` **in principle**. But a denominator bound may prevent the best determinant-1 candidate from using the largest denominator, so NT-04 still checks all admissible extremal candidates exactly.

## Contrast strip
- Real optimum vs integer attainment: a bound suggests where to look; divisors decide what exists.
- Bézout solvability vs Diophantine reconstruction: gcd divisibility says whether solutions exist; NT-04 parameterizes and filters them.
- Factorisation vs brute force: factorisation is complete only when sign/parity branches are accounted for.
- Consecutive-sum existence vs reconstruction: NT-03 gives the power-of-two obstruction; NT-04 recovers actual `(a,r)` pairs.
- Decimal closeness vs exact rational gap: decimals estimate; the cross-product determinant certifies.
- Quadratic real root vs integer root: `D>=0` is not enough; integer feasibility is stricter.
- Sum/product reconstruction vs solving variables: symmetric targets often stop before roots.
- Prime-exponent retrieval vs local teaching: use block allocation, do not rebuild divisor theory.

## Final checks
Original equation; positivity/sign; parity; gcd/coprimality; denominator nonzero; integer reconstruction; duplicate removal; boundary endpoints; all one-way candidates rechecked.
