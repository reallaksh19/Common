# ALG-01 - Teacher Diagnostic Key

## Assimilation-book checkpoints

- Opening diagnostic `x^4+3x` under `x^2+x=1`: `2`.
- H3 symmetric example: `104`.
- H2 relation example: `x^5=55x-21`.
- H1 cubic symmetric example: `p^3+q^3=351`.
- H0 relation example under `t^2=2t+3`: `t^6-5t^4=82t+78`.

## Recognition and first-line lab

1. `(103-97)(103+97)`.
2. Expand only enough to expose the coefficient: `(2x-3)(x+8)`.
3. `t=x+1/x`, retaining `x!=0`.
4. `a^2+b^2=(a+b)^2-2ab`.
5. Start with `x^2=4x-2` and reduce after each multiplication.
6. Require `x-1>=0` (and hence the radical side is defined); square only after recording the condition, then check.
7. No. Zero-product structure is already visible.
8. `(u+v)^2=(u-v)^2+4uv`.
9. `x!=-2`.
10. Multiply by `t` and use `t^2=-t-1`: `t^3=1`.
11. `p^3+q^3=(p+q)^3-3pq(p+q)`.
12. Retain/check `x=0` before dividing by `x`.
13. `t=x^2`.
14. Expand.
15. Factor.
16. `(m-n)^2=(m+n)^2-4mn` determines magnitude only; the sign depends on which variable is larger.
17. Begin from `y^2=5y-1`; multiply and reduce.
18. Substitute both candidates into the original, pre-squaring equation.

## Practice bank answers/checkpoints

1. `(x-7)(x+7)`.
2. `4x^2-12x+9`.
3. `73`.
4. `(52-48)(52+48)=400`.
5. Identity.
6. `8*2000=16000`.
7. `x^3=22x-15`, `x^4=95x-66`.
8. `t=y+1/y`, giving `t^2-7t+10=0`, with `y!=0`.
9. `8^3-3*12*8=224`.
10. `x=7,-2`.
11. `t^3=10t+3`, `t^4=33t+10`, `t^5=109t+33`, `t^6=360t+109`.
12. Original RHS requires `x>=0`. Squaring gives `x^2-2x-3=0`; candidates `3,-1`; only `3` survives.
13. `(p+q)^2=(p-q)^2+4pq=25+56=81`.
14. Let `S_n=z^n+z^-n`. `S_1=3`, `S_2=7`, `S_3=18`, `S_4=47`.
15. Cancelling can lose `x=1`; preserve that branch before division.
16. `x^2=x+1`; successive reduction gives `x^8=21x+13`.
17. `a^3+b^3+c^3=3abc`.
18. `rs=(25-13)/2=6`; `r^4+s^4=(r^2+s^2)^2-2r^2s^2=169-72=97`.
19. `S_0=2,S_1=4,S_n=4S_(n-1)-S_(n-2)`; `S_5=724`.
20. Require `x>=0`; squaring gives `x=3,-2`; only `3` survives. Squaring is the implication-only step.
21. Under `q^2=2q+1`: `q^3=5q+2`, `q^4=12q+5`, `q^5=29q+12`, `q^6=70q+29`, `q^7=169q+70`; subtract `13q^3=65q+26`, giving `104q+44`.
22. `(a-b)^2=36-20=16`, so `(a-b)^4=256`.
23. `w+1/w=2` gives `(w-1)^2/w=0`, so `w=1`; target `2`. (A recurrence also gives the same.)
24. `t=x^2+3x`; `t^2-7t+10=0`, so repeated block `t` is `2` or `5`.
25. `x^2=1-x`, hence `x^4=2-3x`; target `2`.
26. Any correct linear relation-reduction trace under `x^2=4x-1`; canonical polynomial modulo/remainder language is deferred to ALG-03.
27. With perimeter and area, `u+v` and `uv` are known; symmetric powers such as `u^2+v^2` can be reconstructed.
28. Accept a goal that treats the repeated pair as a structured object and chooses inputs that expose/cancel it; do not require functional-equation theory.
29. `(m+1)(n+1)=36`.
30. Retrieve ALG-01 target/representation selection; ALG-02 then owns the bound/equality/attainment machinery.
31-32. Evaluate whether the chosen representation is demonstrably cheaper for the stated target.

## H0 mastery answers

1. `(1007-993)(1007+993)=14*2000=28000`.
2. `13^3-3*36*13=793`.
3. `x^3=9x+10`, `x^4=28x+45`, `x^5=101x+140`.
4. `p^2+q^2=(p-q)^2+2pq=16+42=58`.
5. Need `3x+4>=0` and `x+2>=0`; the stronger lower bound is `x>=-4/3`. Squaring gives `x(x+1)=0`; `x=0,-1`, and both satisfy the original.
6. `S_3=5^3-3*5=110`.
7. From `u^2+u+1=0`, `u^3=1`; `2026 mod 3=1`, so `u^2026=u`.
8. Example `t=x^2+3x`; it is useful when rewriting in `t` reduces repetition/degree and recoverable restrictions remain visible.
9. Division assumes `x!=0` and therefore discards a valid original solution.
10. Expand strategically; the target is coefficient information. Full expansion is `x^3+6x^2+11x+6`, coefficient `6`.
11. Factor: `(x-3)(x-7)=0`; zeros `3,7`.
12. Only `(m-n)^2=81-56=25` is determined; without an order convention `m-n` can be `5` or `-5`.
13. `t^3=15t-4`, `t^4=56t-15`; target `41t-15`.
14. Exclude `x=3`. Multiply through: `x+1=2x-6`, so `x=7`; original check passes.
15. Cheaper first line: `r^2+s^2=(r+s)^2-2rs`; result `64-30=34`.
16. `(a+1)(b+1)=49`.

## Diagnostic codes

- `ALG01-R1`: manipulates before reading target.
- `ALG01-R2`: factor/expand direction confusion.
- `ALG01-R3`: substitution does not reduce complexity.
- `ALG01-R4`: symmetric target solved through unnecessary individual values.
- `ALG01-R5`: relation not used as a rewriting rule.
- `ALG01-R6`: equivalence/condition check missing.
- `ALG01-R7`: downstream canon imported (Vieta/discriminant/remainder/AM-GM/radical doctrine).

## Remediation routing

- R1/R2 -> First-Step router + contrast items 10/11.
- R3 -> substitution tests in the Assimilation Book.
- R4 -> symmetric reconstruction contrast.
- R5 -> relation-rewrite examples, then H0 #13.
- R6 -> equivalence section, then H0 #5/#14.
- R7 -> route learner to the canonical downstream topic rather than reteaching it here.
