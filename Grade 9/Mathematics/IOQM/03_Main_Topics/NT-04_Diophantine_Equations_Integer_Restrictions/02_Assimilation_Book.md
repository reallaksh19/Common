# Diophantine Equations & Integer Restrictions

## The central habit
When variables are integers, **use integrality early**. Do not solve a large real problem and hope integer answers fall out.

Use this route:

`TRANSFORM -> FILTER -> FINITE CANDIDATES -> RECONSTRUCT -> CHECK`

### Reconnect
You already know factoring, parity, gcd, and quadratic equations. Here they become filters. A good filter removes whole families of candidates before arithmetic grows.

## 1. A product equation is a case generator
Suppose positive integers satisfy

`(x-2)(y+3)=20`.

The first useful line is not expansion. Set `x-2=d` and `y+3=20/d`. Since the factors are integers, `d` must be a divisor of 20. Positivity removes some signed divisors. The factor list is not a heuristic: it is a complete parametrisation of the solutions.

**Try first:** Before reading further, write the signed factor-pair list for `(u)(v)=12` and mark which pairs survive if `u>0` and `v>3`.

A common failure is to list only positive divisors when the shifted factors may be negative. The sign conditions belong to the original variables, not automatically to the factors.

## 2. Difference of squares adds a parity filter
From `x^2-y^2=N`, write

`(x-y)(x+y)=N`.

The two factors have the same parity. For odd `N`, both are odd. For `N` divisible by 2 but not 4, there is no integer solution with both factors even. This parity check can eliminate factor pairs before reconstruction.

For `x^2-y^2=45`, factor pairs `(1,45),(3,15),(5,9)` all have matching parity, yielding three positive solutions.

## 3. Coprimality changes the factor-pair problem
If `xy=N` and `gcd(x,y)=1`, a prime-power block of `N` cannot be split between both factors. Retrieve that fact from prime-exponent structure, then return here to the case problem.

Example: `N=2^2*3*7`. The blocks `4,3,7` must each go wholly to one side. That makes only `2^3` ordered allocations, instead of all divisors of 84.

This is an application of prime-exponent structure, not a second prime-factorisation lesson.

## 4. Bound before you enumerate
A bound turns an infinite integer problem into a finite one.

If `n(n+1)<90` and `n` is positive, monotonicity gives a cheap endpoint test: `8*9=72<90` but `9*10=90`. So `n<=8`.

For a fixed product `xy=N` with positive integers, the smallest sum occurs at the factor pair closest to `sqrt(N)`. A real inequality can suggest the square, but the answer is determined by actual divisor pairs. For area 96, `8*12` beats `6*16`; the least perimeter is 40.

## 5. Exact rational approximation is an integer-gap problem
For a reduced fraction `a/b` near `p/q`,

`|a/b-p/q| = |qa-pb|/(qb)`.

The numerator `|qa-pb|` is an integer. Unless the fractions are equal, it is at least 1. This converts a vague decimal-closeness question into an exact Diophantine one.

Near `3/4` with `b<=15`, the best possible determinant is 1. Solving `4a-3b=+/-1`, the largest useful denominator is `b=15`, giving `a=11`; the sum is 26.

**Contrast:** Decimal testing estimates distance. The determinant certifies optimality.

## 6. Sum/product data reconstruct integers
If integers `x,y` have sum `S` and product `P`, then they are roots of

`t^2-St+P=0`.

Use this only as a representation bridge. If the target is symmetric, stop earlier. For example,

`x^2+y^2=S^2-2P`.

Do not solve individual roots when the requested quantity is already determined.

## 7. A quadratic integer root needs more than real feasibility
For `ax^2+bx+c=0` with integer coefficients, an integer root forces the discriminant `D=b^2-4ac` to be a nonnegative perfect square, together with the divisibility condition from the quadratic formula. This is a narrow feasibility bridge: the general discriminant theory lives elsewhere.

A useful square filter often becomes a difference of squares after completing the square. If

`n^2+6n+5=k^2`, then `(n+3)^2-k^2=4`, so `(n+3-k)(n+3+k)=4`. The fixed product creates finitely many cases.

## 8. One equation plus a side condition: eliminate first
With several integer variables, use the side condition early. A fixed sum may remove one variable; a gcd condition may normalize two variables; a positivity condition may bound a factor.

Historical anchor pattern: an equation in `a,b,c` together with `a+b+c=32` can be rearranged to `(a-b)(c-1)=66`. The product structure and the sum cooperate; a three-dimensional brute-force search is unnecessary.

## 9. Completeness is part of the solution
A finite case solution is not complete until you answer:

1. Why must every solution enter one of these cases?
2. Are the cases disjoint, or have duplicates been removed?
3. Did sign, parity, gcd, and domain conditions survive reconstruction?
4. Did a one-way step create candidates that need checking?
5. Have all surviving candidates been substituted into the original condition?

For multiplicative partitions, sort factors or impose a canonical order before counting; otherwise permutations of the same factorisation masquerade as new cases.

## 10. Source anchors as recognition training
- A fixed-area rectangle asks for **discrete factor pairs**, not just a continuous square optimum.
- A closest fraction with bounded denominator asks for the **integer determinant** `qa-pb`.
- A quartic-looking positive-integer relation may collapse immediately modulo a shifted factor; always preserve the printed exponent.
- A quadratic Diophantine equation may become a **fixed difference of squares** after scaling.
- An equal-sum/equal-product representation becomes a **multiplicative partition plus forced ones** problem.

## Closing router
Before calculating, ask:

`What integer restriction collapses the search first?`

Then transform only far enough to expose that restriction, enumerate a provably complete finite set, reconstruct, and check the original statement.
