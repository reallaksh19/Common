# Teacher Diagnostic Key — Functional Equations

## Recognition and First-Line Lab

1. B. Setting one integer variable to 0 changes `mn+1` to 1.
2. B. `x -> 8-x -> x`.
3. B. Substitute `5-x`.
4. C. `-1` is certainly an integer.
5. B. The rule must be proved for every allowed input.
6. B. Start from `f(a)=f(b)` and derive `a=b`.
7. A. Let the target be arbitrary and construct a preimage.
8. B. It is indexed by `n` and relates neighboring sequence terms.

9. Replacing `x` by `4-x` gives `3f(x)+2f(4-x)=11-x`.
10. Set `m=0`: `f(n)=f(0)+n=n+5`.
11. Set `m=n=0`, giving `f(0)=2f(0)` and hence `f(0)=0`.
12. Assume `f(a)=f(b)`.
13. Add the two equations first (or subtract, provided the elimination is correct).
14. Substitute: `(x+y)^2+1 = (x^2+1)+(y^2+1)+2xy-1`.
15. Verify the derived candidate in the original two-variable functional equation on the full integer domain.
16. Try `x=0` or `y=0` to make `xy=0`; also `x=1` or `y=1` may preserve the other variable.

## Practice and Transfer Bank

1. Put `x=0`: `2f(0)=2`, so `f(0)=1`; hence `f(x)=x+1` and `f(7)=8`.
2. Add the two displayed equations: `2f(x)=2x+4`; `f(x)=x+2`; answer `5`.
3. Pair `x` with `4-x`. Let `a=f(x), b=f(4-x)`. Then `a+2b=x+4` and `2a+b=8-x`; solve `a=4-x`. Thus `f(1)=3`.
4. Additivity on integers gives `f(0)=0`, `f(-n)=-f(n)`, and `f(n)=3n`; answer `-12`.
5. The relation only connects values whose inputs differ by an integer. Values on different fractional parts can be chosen independently, subject to the shift rule. So real-domain values are not fully determined.
6. Put `x=1`: `f(y)=f(y)+y f(1)`. Since `y>0`, `f(1)=0`.
7. Put one variable equal to 0 to get `f(0)=0`, then `n=1`: `f(m+1)=f(m)+1+2m`. This yields `f(m)=m^2` on integers. Answer `36`.
8. The equation only fixes the sum of two companion values. For example, changing `f(5)` can be offset by changing `f(-3)` so their sum remains 10.
9. Add/subtract: `f(x)=x+4`; answer `9`.
10. Pair with `5-x`: `2f(x)+3f(5-x)=x+10`, `3f(x)+2f(5-x)=15-x`. Solving gives `f(x)=5-x`; answer `7`.
11. Pair with `1-x`: solve to obtain `f(x)=1-x`; answer `-6`.
12. `f(0)=0`; setting `n=1` gives `f(m+1)=f(m)+1+m`. Hence `f(n)=n(n+1)/2` on integers. Answer `36`.
13. If `f(a)=f(b)`, then `x+f(a)=x+f(b)`. Applying the equation gives `f(x)+a=f(x)+b`, so `a=b`.
14. Put `x=0`: `f(f(y))=f(0)+y`. For target `t`, choose `y=t-f(0)`; then `f(f(y))=t`.
15. Put `m=0`: `f(-n)=f(0)-n=3-n`. Take `n=11`; `f(-11)=-8`.
16. Pair with `3-x`: equations give `f(x)=x+2`; `f(20)=22`.
17. From `f(0)=0` and `n=1`, `f(m+1)-f(m)=m+1`. Thus for nonnegative integers `f(n)=n(n+1)/2`. The same difference rule extends consistently to negative integers. Verification:
`[(m+n)(m+n+1)-m(m+1)-n(n+1)]/2 = mn`.
18. Finite values only support a conjecture. Complete the argument by deriving the formula for all integers from the equation, or by proving the proposed formula satisfies the equation and required initial data.
19. Pair with `4-x`: `3f(x)+f(4-x)=4x+4`, `3f(4-x)+f(x)=20-4x`. Solving gives `f(x)=2x-1`; answer `13`.
20. Direct substitution gives both sides `x^2+2xy+y^2+1`; therefore it satisfies the equation for every real pair.

## Mixed Mastery Test

1. Pair with `3-x`; `f(x)=x+2`; answer `12`.
2. Integer propagation gives `f(n)=n(n+1)/2`; answer `45`.
3. No. Only the sum of `f(5)` and `f(-3)` is fixed at 6; neither value is individually forced.
4. Same injectivity argument as Practice 13: from `f(a)=f(b)`, compare the equations and obtain `a=b`.
5. Set `m=0`: `f(-n)=4-n`. To obtain `f(13)`, choose `n=-13`; answer `17`.
6. Paired equations give `f(x)=2x-1`; answer `13`.
7. A recurrence-like step controls the integer values of one indexed progression. A two-variable functional equation is an all-pairs statement; a candidate obtained from the step must still be checked in that original relation.
8. Yes. Both sides simplify to `x^2+2xy+y^2+1`.
9. Add the equations: `f(x)=x+2`; answer `-2`.
10. Substitute the conjectured rule into the original equation and prove it for every allowed input, including any stated initial/domain conditions.

## Historical anchor audit

`IOQM-2025-Q14 = 12`.
- integer domain makes `m=0,n=0` legal;
- `m=0` gives `f(1)=2`;
- `n=0` gives `f(m)=m+1` for every integer;
- cumulative sum is `N(N+3)/2`;
- 12 gives 90 and 13 gives 104.

`IOQM-2024-Q16 = 08`.
- real domain makes `3-x` legal for all real `x`;
- paired equations are a nonsingular 2x2 system;
- `7f(x)=x^2-24x+36`;
- difference `f(27)-f(25)=8`.

## Diagnostic map

- random small-number trials -> ask which substitution collapses the argument;
- formula guessed from a value table -> require all-domain verification;
- reflection present but no partner equation -> apply the reflection twice;
- injectivity asserted -> demand the `f(a)=f(b) => a=b` derivation;
- surjectivity asserted -> demand a construction for arbitrary target;
- real-domain shift treated like integer recurrence -> point out independent fractional-part classes;
- illegal input -> return to the stated domain before algebra.
