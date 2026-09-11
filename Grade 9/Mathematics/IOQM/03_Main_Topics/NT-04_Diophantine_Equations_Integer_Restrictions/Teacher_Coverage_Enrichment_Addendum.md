# NT-04 — Teacher Coverage Enrichment Addendum

Status: `STATIC_DIAGNOSTIC_ADDENDUM_V1`
Issue: `#134`

This addendum synchronizes NT-04 with two upstream retrieval bridges introduced by the coverage-enrichment patch. It does not change historical-anchor answers.

## A. Linear Diophantine equations from Bézout

Retrieve from NT-01:

`ax+by=c` has integer solutions iff `gcd(a,b)|c`.

NT-04 then owns the full family. If `g=gcd(a,b)` and `(x0,y0)` is one solution, every integer solution is

`x=x0+(b/g)t`,

`y=y0-(a/g)t`,

for `t in Z`.

### Diagnostic A1

Solve in integers:

`18x+30y=6`.

One solution is `(2,-1)` because `36-30=6`. Since `g=6`, all solutions are

`x=2+5t`, `y=-1-3t`.

### Diagnostic A2 — positivity filter

Find positive integer solutions of

`6x+9y=45`.

Divide by 3:

`2x+3y=15`.

One solution is `(0,5)`; all solutions are `x=3t`, `y=5-2t`. Positivity gives `t=1,2`, hence `(3,3)` and `(6,1)`.

The solvability theorem alone is not the final answer; filtering is the NT-04 step.

## B. Consecutive-sum reconstruction

Retrieve from NT-03:

A positive integer is representable as a sum of at least two consecutive positive integers iff it is not a power of 2.

For reconstruction use

`2n=r(2a+r-1)`

and

`a=((2n/r)-r+1)/2`.

### Diagnostic B1

Represent `45` using three consecutive positive integers.

Set `r=3`:

`a=(90/3-3+1)/2=14`.

So `45=14+15+16`.

### Diagnostic B2 — reject invalid factor pair

For `n=15`, choosing `r=10` is impossible because `r` must divide `2n=30`, but even when a divisor is chosen, the recovered `a` must still be a positive integer. Learners must check reconstruction, not merely list divisors.

### Diagnostic B3 — complete enumeration obligation

If asked for all representations, every admissible factor pair of `2n` must correspond to exactly one checked `(a,r)` case; duplicate/reversed factor interpretations must not be counted twice.

## Diagnostic codes

- `NT04-BEZ-1`: starts parameterization before checking gcd divisibility.
- `NT04-BEZ-2`: retrieves one Bézout solution but cannot generate the full family.
- `NT04-BEZ-3`: forgets positivity/bound filters on the parameter.
- `NT04-CONSEC-1`: ignores NT-03's power-of-two existence obstruction.
- `NT04-CONSEC-2`: lists divisors of `2n` without reconstructing/checking `a`.
- `NT04-CONSEC-3`: does not prove all representations have been covered.

## Evidence truth

The external DOCX was comparison material only. These diagnostics are independently derived curriculum enrichments. Classroom timing/readability, retention, psychometrics, qualification/pass-mark calibration and publication approval remain `NOT_RUN`.