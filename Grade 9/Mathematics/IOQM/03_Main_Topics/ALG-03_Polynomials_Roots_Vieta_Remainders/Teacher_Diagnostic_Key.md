# ALG-03 - Teacher Diagnostic Key

## Recognition lab

1. `alpha+beta=7`, `alpha beta=10`; reconstruct target.
2. Factor `(x-5)(x-2)`.
3. `Delta=16-20<0`.
4. Route to ALG-02; complete square `(x-2)^2+1`.
5. `x-3`.
6. Evaluate `P(2)`.
7. `P(x-4)`.
8. Each root moves down by 4.
9. Use `x^2≡1`; remainder `1`.
10. `x^3≡1`; 2026 mod 3 =1, remainder `x`.
11. Subtract/combine to eliminate leading terms.
12. `1/r+1/s=(r+s)/(rs)`; need sum/product.
13. Evaluate at `x=-1`; result 0, so yes.
14. `Delta=0`.
15. For roots doubled, test a scalar-normalized version of `P(x/2)`.
16. No; a divisor/relation is needed to define reduction.

## Practice answers

1. `(x-2)(x-3)`, roots 2,3.
2. sum 7, product 10.
3. `29`.
4. `Delta=0`; repeated root 3.
5. `P(1)=8`.
6. sum `5/2`, product `-3/2`.
7. `8^3-3*12*8=224`.
8. `Delta=-4`; no real roots.
9. `Delta=1`; two distinct real roots.
10. `P(-1)=0`; yes.
11. `P(x-4)=(x-6)(x-7)=x^2-13x+42`.
12. roots `-2,-1`.
13. `1`.
14. `x`.
15. `x^5≡55x-21 (mod x^2-3x+1)`.
16. subtract -> `-x+3=0`; common root 3.
17. `(alpha+beta)/(alpha beta)=(-2/3)/(-5/3)=2/5`.
18. `p^3+q^3=s^3-3st`.
19. `Delta=k^2-36=0`; `k=+-6`, repeated roots `+-3` respectively.
20. `P(1)=0`; remainder 0, factor yes.
21. `41=81-2alpha beta`, so product 20; polynomial `x^2-9x+20`.
22. `x^3≡1`; exponents 1000,999,998 reduce to 1,0,2 mod3, so `x+1+x^2≡0`.
23. First at -1: `1-a+6=0` -> `a=7`; second `1-b+3=0` -> `b=4`. Polynomials roots `-1,-6` and `-1,-3`.
24. `20 mod3=2`; reduce `x^2 ≡ -x-1`, so the canonical remainder is `-x-1`.
25. roots `(9-1)/2=4`, `(9+1)/2=5`; polynomial `x^2-9x+20`.
26. Vieta avoids computing roots and preserves only requested symmetric information.
27. root count -> ALG-03 discriminant, no real roots; minimum -> ALG-02 square completion, min 1.
28. Desired roots `alpha-3,beta-3` come from `P(x+3)`.
29. A characteristic relation identifies powers modulo a low-degree polynomial; reduce rather than iterate huge powers.
30. Subtraction/remainder elimination toward a common factor is the elementary form of gcd reasoning.

## H0 answers

1. sum `9/2`, product `2`; square sum `81/4-4=65/4`.
2. `Delta=4-60=-56`; no real roots.
3. `Delta=0`; root `12/(8)=3/2`.
4. Original roots 2,4; shifted roots 5,7; polynomial `x^2-12x+35` = `P(x-3)`.
5. Roots move up by 2: if `P(alpha)=0`, `Q(alpha+2)=P(alpha)=0`.
6. `3^4+6+7=94`.
7. `P(2)=8-12+4=0`; yes.
8. `99 mod3=0`; remainder `1`.
9. Relation `x^2=2x+1`; reductions give `x^6=70x+29`.
10. subtract -> `-x+2=0`; common root `2`.
11. sum 10, product 21; `1000-630=370`.
12. ALG-02; `(x-5)^2-4`, minimum `-4`.
13. `Delta=k^2-16>0`, so `|k|>4`.
14. A low-degree relation already identifies the remainder class; direct high-power expansion computes irrelevant information.
15. If old root is `alpha`, `P((alpha+5)+5)=P(alpha+10)` need not be zero; `P(x-5)` is correct for root shift +5.
16. Difference gives a necessary candidate for any common root; original checks establish sufficiency.

## Diagnostic tags

- `ALG03-R1` solves roots unnecessarily instead of using invariants.
- `ALG03-R2` discriminant used for an optimization request or vice versa.
- `ALG03-R3` root/input shift sign reversed.
- `ALG03-R4` high powers calculated rather than reduced.
- `ALG03-R5` factor/remainder theorem not connected through evaluation.
- `ALG03-R6` common-root candidate not checked in both originals.
