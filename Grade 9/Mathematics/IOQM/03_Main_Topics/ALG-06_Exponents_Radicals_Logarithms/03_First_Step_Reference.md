# First-Step Reference: Exponents, Radicals and Logarithms

Use the smallest valid first move. Do not start by expanding or squaring unless the structure requires it.

| You see | First question | First mathematical line |
|---|---|---|
| several powers such as `8^x`, `4^(x+1)` | can they share one base? | rewrite them as powers of the same positive base |
| negative exponent | can the base be zero? | record `base != 0`, then use `a^(-n)=1/a^n` |
| `sqrt(U)` | is the radical defined? | write `U>=0` |
| `sqrt(U)=V` | is the right side non-negative? | write `U>=0` and `V>=0` before squaring |
| `sqrt(x^2)` | what sign can x have? | write `sqrt(x^2)=|x|` |
| `sqrt(p)-sqrt(q)` in a denominator | will the conjugate collapse it? | multiply by `sqrt(p)+sqrt(q)` |
| `sqrt(A+2sqrt(B))` | can it be `sqrt(m)+sqrt(n)`? | compare `m+n=A` and `mn=B` |
| nested radical such as `sqrt(x-sqrt(x+a))` | what inner quantity should be named or isolated? | preserve the nesting; record both radicand conditions |
| equation after a square | did the square preserve equivalence? | mark the move `⇔` if both sides had known same sign; otherwise mark `⇒` and plan a final check |
| `log_a b` | is the logarithm legal? | write `a>0`, `a!=1`, `b>0` |
| reciprocal logs `log_a b`, `log_b a` | can one variable represent both? | set `t=log_a b`, then `log_b a=1/t` |
| variable exponent, no common base | would log form reduce the exponent cleanly? | take logs only after positivity/domain is secure |
| integer restrictions after radicals/logs | has the continuous algebraic structure already been solved? | finish the equation first, then apply the integer filter |

## Fast route choices

### Common base vs logarithm
Prefer **common base** when both sides already factor into powers of one small positive base.

Prefer **logarithm** when no useful common base exists and taking logs genuinely makes the variable exponent linear or simpler.

### Conjugate vs squaring
Prefer a **conjugate** when a sum/difference of radicals is multiplying or dividing and a difference of squares will remove the radicals.

Prefer **squaring** when an equation has an isolated radical and all needed sign conditions have been recorded.

### Simple radical vs nested radical
For a simple radical, isolate it and protect the sign.

For a nested radical, first preserve the inside as one object. Repeated squaring without a representation plan usually creates more structure than it removes.

## The three checks before squaring

Before replacing `sqrt(U)=V` by `U=V^2`, confirm:

1. `U>=0`;
2. `V>=0`;
3. whether these conditions make the square reversible.

If you cannot prove the sign of `V`, squaring may create candidates. Check them in the original equation.

## The three checks before using a logarithm

For every variable logarithm, confirm:

1. base `>0`;
2. base `!=1`;
3. argument `>0`.

Then decide whether exponent form or log form is cheaper.

## Stop rule

Stop transforming once the requested value is determined and every candidate satisfies the original domain and equation. More algebra is not more proof.
