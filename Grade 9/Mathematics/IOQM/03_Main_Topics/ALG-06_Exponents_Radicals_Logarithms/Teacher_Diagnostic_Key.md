# Teacher Diagnostic Key — Exponents, Radicals and Logarithms

## Recognition and First-Line Lab

1. B. `8` and `4` are powers of 2, so common-base normalization is cheaper than logarithms.
2. C. Principal square root gives `sqrt(x^2)=|x|`.
3. C. `sqrt(U)` requires `U>=0`; to make squaring `sqrt(U)=V` reversible, also require `V>=0`.
4. B. The conjugate converts the denominator to `7-5`.
5. B. The inner radical remains part of the outer radicand.
6. B. Without the sign condition, squaring may create candidates; check the original equation.
7. B. Base `x-2>0`, base `x-2!=1`, argument `x+1>0`.
8. B. Set `t=log_a b`; then `log_b a=1/t`.

9. `3^(3x)=3^(2x+2)`.
10. `5-2x>=0`, so `x<=5/2`.
11. `2x+3>=0` and `x+1>=0`; together the reversible-square domain is `x>=-1`.
12. Multiply by `(sqrt11-sqrt3)/(sqrt11-sqrt3)`.
13. `m+n=13` and `mn=40`.
14. `x+6>=0` and `x-sqrt(x+6)>=0`.
15. `x>0`, `x!=1`, and exponent form `(x)^4=16`.
16. Set `t=log_a b>0`; then `t+6/t=5`.

## Practice and Transfer Bank

1. `27^(2/3)=(3^3)^(2/3)=3^2=9`.
2. `3^(2x)=3^3`, so `x=3/2`.
3. `sqrt200=sqrt(100*2)=10sqrt2`.
4. `5-2x>=0`, so `x<=5/2`.
5. `(sqrt7+sqrt5)/(7-5)=(sqrt7+sqrt5)/2`.
6. Domain requires `x>=0`. Squaring gives `x+6=x^2`, hence `x=3,-2`; only `3` is valid.
7. `|x-4|=3`, so `x=1,7`.
8. `(2+sqrt3)^2=7+4sqrt3`, so the expression is `2+sqrt3`.
9. Domain gives `x+1>=0`. Squaring gives `2x+3=(x+1)^2`, hence `x^2=2`. Only `x=sqrt2` satisfies `x+1>=0`.
10. Let `A=sqrt(x+1)`, `B=sqrt(x-3)`. Then `A-B=1` and `(A-B)(A+B)=4`, so `A+B=4`. Hence `A=5/2`, `B=3/2`, giving `x=21/4`.
11. `13-4sqrt10=(sqrt8-sqrt5)^2`; since `sqrt8>sqrt5`, the value is `sqrt8-sqrt5=2sqrt2-sqrt5`.
12. Squaring once gives `sqrt(x+6)=x-4`, so `x>=4`. Squaring again gives `x^2-9x+10=0`; only `x=(9+sqrt41)/2` satisfies the sign condition.
13. `x-1=8`, so `x=9`.
14. Set `t=log_a b>0`. Then `t+1/t=5/2`, so `t=2` or `1/2`. Thus `b=a^2` or `a=b^2`. Squares within 20 come from bases `2,3,4`, giving 3 pairs each direction, total `6`.
15. `x=log_2 7`.
16. Base conditions: `x>0`, `x!=1`. Exponent form gives `x^4=16`; the legal real base is `x=2`.
17. `54`. Set `t=log_a b`; then `t+6/t=5`, so `t=2,3`. Count `b=a^2` for `a=2..44` (43 pairs) and `b=a^3` for `a=2..12` (11 pairs).
18. `91`. Domain/sign analysis forces `y=0`; then `sqrt(x+a)=x-a`. Set `t=x-a>=0`; this gives `a=t(t-1)/2`. The largest admissible nonsquare below 100 is `t=14 -> a=91`.
19. Squaring gives `x=x^2-4x+4`, so candidates are `1,4`. The original equation requires `x-2>=0`; therefore only `x=4` is valid.
20. `log_2 x` must be defined and non-negative. Squaring gives `log_2 x=4`, hence `x=16`, which satisfies all domain conditions.

## Mixed Mastery Test

1. `2^(4x-4)=2^(6x+3)`, so `x=-7/2`.
2. Domain requires `x>=0`. Squaring gives `x^2-3x+2=0`, so `x=1,2`; both satisfy the original equation.
3. Since `2-sqrt3>0`, `sqrt((2-sqrt3)^2)=2-sqrt3`.
4. `3(sqrt5-1)/(5-1)=3(sqrt5-1)/4`.
5. Let `A=sqrt(x+5)`, `B=sqrt(x+1)`. Then `A-B=1`, `A+B=4`; hence `A=5/2`, giving `x=5/4`.
6. `(2+sqrt5)^2=9+4sqrt5`, so the value is `2+sqrt5`.
7. First square: `sqrt(x+2)=x-1`, so `x>=1`. Second square gives `x^2-3x-1=0`; valid solution `x=(3+sqrt13)/2`.
8. Candidates after squaring are `1,4`; original sign condition `x-2>=0` leaves `4`.
9. `x-1=9`, so `x=10`.
10. Base `x>0`, `x!=1`; exponent form `x^3=27` gives `x=3`.
11. Set `t=log_a b>0`. Then `t+2/t=3`, so `t=1` or `2`. `t=1` gives `a=b`: 99 pairs. `t=2` gives `b=a^2` for `a=2..10`: 9 more. Total `108`.
12. Squaring is reversible because both sides are non-negative. The same reduction gives `a=t(t-1)/2`. Under `a<50`, `t=10` gives `45` and `t=11` gives `55`; `45` is nonsquare. Answer `45`.

## Historical anchor audit

`IOQM-2023-Q02 = 54`.
- logarithm bases/arguments are legal because `a,b>=2`;
- `t=log_a b>0` and reciprocal log is `1/t`;
- quadratic roots are `2,3`;
- integer bounds give `43+11=54` ordered pairs.

`IOQM-2025-Q28 = 91`.
- exact controlled source contains the nested radical `sqrt(x-sqrt(x+a))`;
- principal-root signs are recorded before squaring;
- irrationality/integer structure forces `y=0`;
- all squaring steps used in the final route are reversible under recorded signs;
- `a=t(t-1)/2`, and `t=14` gives the maximal admissible nonsquare `91`.

## Diagnostic map

- `sqrt(x^2)` replaced by `x` -> restore principal-root rule `|x|`;
- radical squared with no sign record -> classify the move as candidate-generating and check the original;
- denominator rationalized mechanically -> ask what difference-of-squares structure the conjugate exposes;
- nested radical flattened -> preserve inner radical as one object;
- logarithm manipulated before base/argument domain -> return to domain conditions;
- logarithm introduced despite an obvious common base -> normalize first;
- quadratic roots all accepted after squaring -> test sign conditions and original equation;
- integer search started before algebraic structure -> solve the real/domain problem first, then filter integers.
