# Teacher Key — ALG-06 Benchmark Assimilation Lab

This key supports `07_Benchmark_Assimilation_Lab.md`. It is separate from the main Teacher Diagnostic Key so the benchmark-specific learner diagnostic can be audited independently.

## A. RECONNECT

1. `sqrt(x^2)=|x|` over the reals.
2. `2x-1>=0` for the radicand and `x-2>=0` because the left side is non-negative. Together `x>=2`; on this restricted domain squaring is reversible.
3. Common base. Write `8=2^3`, `4=2^2` before considering logarithms.
4. Conjugate `sqrt7+sqrt3`; the product is `7-3=4`, a rational denominator.
5. For `log_(x-1)(x+2)`: `x-1>0`, `x-1!=1`, `x+2>0`. Thus `x>1` and `x!=2`; the argument condition is then automatic.
6. Square root is not linear over subtraction. The entire expression `x-sqrt(x+a)` is the radicand of the outer root and must remain one object.
7. `log_b a=1/t`, provided both logarithms are defined and `t!=0`.
8. Check every candidate against the original domain/sign restrictions and the original unsquared equation.

## B. Error laboratory

### Error 1
Correct identity: `sqrt((x-5)^2)=|x-5|`. It equals `x-5` only when `x>=5`.

### Error 2
Before squaring `sqrt(x+3)=1-x`, require `x+3>=0` and `1-x>=0`. Thus `-3<=x<=1`. Squaring is reversible only on that restricted domain; any algebraic candidate outside it is invalid.

### Error 3
`sqrt(x-sqrt(x+a))` cannot be distributed over subtraction. Preserve the outer radicand; first require `x+a>=0` and `x-sqrt(x+a)>=0`.

### Error 4
For `log_(x-2)(x+1)`, first require `x-2>0`, `x-2!=1`, `x+1>0`. Only then convert to exponent form.

### Error 5
`9^x=27` is already `3^(2x)=3^3`, so compare exponents: `2x=3`. Logs are valid but inefficient.

### Error 6
First solve/reduce the radical/logarithmic structure under its real-domain conditions. Apply integrality only after the admissible algebraic family is known.

## C. ADOPT

1. Write `3x+4>=0` and, because `sqrt(3x+4)=x`, also `x>=0`; then square on `x>=0`.
2. Multiply numerator and denominator by `sqrt13+sqrt5`.
3. Test `sqrt m+sqrt n`: `m+n=17`, `mn=60` (hence `{m,n}={12,5}`).
4. Domain: `x-1>0`, `x-1!=1`; then `(x-1)^3=27`.
5. Set `t=log_a b>0`, so `log_b a=1/t`; obtain `t+2/t=3`.
6. Rewrite in base 2: `2^(4x-4)=2^(3x+6)`.
7. Record `x+6>=0` and `x-sqrt(x+6)>=0`; after the first justified square, write `x-sqrt(x+6)=4`.
8. Require `x-4>=0` before the second square; this is the missing sign condition that makes the next square reversible.

## D. TRANSFER

1. Yes. Compare `11-6sqrt2` with `(sqrt m-sqrt n)^2=m+n-2sqrt(mn)`. Need `m+n=11`, `mn=18`; `{m,n}={9,2}`, so `u=3-sqrt2` because `u>=0`.
2. Set `t=log_a b>0`; then `t+1/t=5/2`, so `2t^2-5t+2=0`, giving `t=2` or `1/2`. Thus `b=a^2` or `a=b^2`; the bounds reduce the problem to counting integer square pairs.
3. `sqrt(P(x))` is non-negative, so any solution also needs `Q(x)>=0`. Squaring may solve `P(x)=Q(x)^2`, but candidates with `Q(x)<0` or invalid radicand must be rejected in the original equation.
4. Separate rational and irrational parts. Since `sqrt a` is irrational for nonsquare `a`, an equality between an integer/rational quantity and `k+m sqrt a` forces the irrational coefficient to satisfy the necessary cancellation condition (often `m=0` or another exact coefficient equation).
5. Normalize both sides to powers of 6 and compare exponents. Logs would preserve correctness but introduce an unnecessary operation and extra notation without reducing the structure further.
6. Example: `sqrt(x+4)=x+1` together with the recorded condition `x>=-1` and `x+4>=0`. On that domain both sides are non-negative, so squaring is an equivalence.

## E. Six-question assimilation test — diagnostic rubric

A strong response should contain all six elements:

1. a specific visible clue, not a chapter name;
2. the invariant/domain reason the proposed method is valid;
3. a reusable recognition cue;
4. a genuine near-neighbour requiring a different route;
5. two mathematically useful opening lines;
6. a changed-surface example preserving the invariant, with a plausible route.

Diagnostic tags:

- `recognition`: clue not identified;
- `representation`: wrong route chosen despite a cheaper one;
- `domain_condition`: sign/base/argument condition omitted;
- `equivalence`: implication-only transformation treated as reversible;
- `execution`: correct route but algebra error;
- `checking`: candidates not returned to original equation;
- `transfer`: disguised version changes the mathematics rather than only the surface.

## Independent QA disposition

All deterministic answers and route claims above were recomputed after the learner lab was authored. No answer is inherited from the learner-facing document.

`BENCHMARK_LAB_KEY_STATIC_CHECK = PASS`.
