# ALG-01 — Teacher Diagnostic Key

## Recognition lab

1. `(103-97)(103+97)`.
2. `t=x+1/x`.
3. `(a+b)^2-2ab`.
4. start from `x^2=4x-2` and reduce powers successively.
5. require `x-1>=0` and `x+3>=0`; then square and check.
6. no; zero-product structure is already visible.
7. `(u+v)^2=(u-v)^2+4uv`.
8. `x != -2`.
9. multiply `t^2+t+1=0` by `t` and use it to obtain `t^3=1` for a root of that quadratic.
10. `(p+q)^3-3pq(p+q)`.

## Practice answers

1. `(x-7)(x+7)`.
2. `4x^2-12x+9`.
3. 73.
4. `(8)(2000)=16000`.
5. `x^3=22x-15`; `x^4=95x-66`.
6. `t=y+1/y`, giving `t^2-7t+10=0`.
7. `8^3-3(12)(8)=224`.
8. `t^3=10t+3`, `t^4=33t+10`, `t^5=109t+33`, `t^6=360t+109`.
9. Domain requires `x>=0`. Squaring gives `x^2-2x-3=0`, so candidates are `3,-1`; only `3` satisfies the original equation.
10. Let `S_n=z^n+z^-n`; `S_1=3`, `S_2=7`, `S_3=18`, `S_4=47`.
11. With `x^2=x+1`, powers follow the Fibonacci-type reduction: `x^8=21x+13`.
12. Since `a+b+c=0`, `a^3+b^3+c^3=3abc`.
13. `rs=(25-13)/2=6`; `r^4+s^4=13^2-2*36=97`.
14. `S_0=2,S_1=4,S_n=4S_{n-1}-S_{n-2}`; `S_5=724`.
15. Domain `x>=0`; squaring gives `x^2=x+6`, candidates `3,-2`; only `3` satisfies the original equation.

## H0 mastery answers

1. `14*2000=28000`.
2. `13^3-3(36)(13)=793`.
3. `x^3=9x+10`; `x^4=28x+45`; `x^5=101x+140`.
4. `p^2+q^2=(p-q)^2+2pq=58`.
5. Domain requires `x>=-4/3`. Squaring gives `x^2+x=0`, candidates `0,-1`; both satisfy the original equation.
6. `S_3=5^3-3*5=110`.
7. `u^3=1`; `2026 mod 3 = 1`, so `u^2026=u`.
8. Example `t=x^2+3x`; useful if the equation/target depends on that block repeatedly and constraints can be recovered.
9. Dividing by `x` discards the valid branch `x=0`.
10. Evaluate reasoning rather than one fixed answer.

## Diagnostic tags

- `ALG01-R1` manipulates before reading target.
- `ALG01-R2` factor/expand direction confusion.
- `ALG01-R3` substitution does not reduce complexity.
- `ALG01-R4` symmetric target solved via unnecessary individual values.
- `ALG01-R5` relation not used as rewriting rule.
- `ALG01-R6` equivalence/domain check missing.

## Gate

Reject a candidate solution produced by a non-reversible transformation unless it has been checked in the original condition.