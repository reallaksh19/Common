# ALG-02 - Teacher Diagnostic Key

## Recognition lab

1. `(x-4)^2+4`.
2. `12-(x+1)^2<=12`.
3. AM-GM on positive `x,25/x`; equality `x=5`.
4. `(a-b)^2>=0` or AM-GM -> `ab<=81`, equality `a=b=9`.
5. No; `0` is excluded and values approach it.
6. Real equality point is `1/2`; integer filter checks `0,1`.
7. Engel: `1/x+1/y >= 4/(x+y)=1/3`.
8. Equality is excluded, so `7` is only a lower bound unless another point attains it; no minimum `7`.
9. No. Root-count/feasibility by discriminant belongs to ALG-03.
10. Complete the square.
11. AM-GM: `a+b>=6`, equality `a=b=3`.
12. No positive minimum; product approaches `0` as one variable approaches `0+`.
13. Equality condition and attainment in the original domain.
14. Check adjacent admissible integers (normally floor/ceiling candidates, plus any boundary constraints).
15. Upper bound `1` is approached as `x->infinity` but never attained; no maximum.
16. No extremum claim is needed; only proof and equality characterization if requested/useful.

## Practice answers

1. `(x-3)^2+4`, min `4` at `x=3`.
2. max `9` at `x=4`.
3. `x+4/x>=4`, equality `x=2`.
4. `ab<=25`, equality `a=b=5`.
5. On `x>0`, lower bound `0` is not attained; no minimum.
6. min `6` at `x=3`.
7. max `36` at `a=b=6`.
8. min `2/5` at `x=y=5`.
9. `(x+5)^2+4`, min `4`.
10. `9/4`, attained at `n=0,1`.
11. min `8` at `x=y=4`.
12. max `100` at `x=y=10`.
13. no minimum; infimum `0`.
14. no maximum; supremum `1`.
15. `n^2-5n+9=(n-5/2)^2+11/4`; integers `2,3` give `3`.
16. perimeter 40 -> `x+y=20`; max area `100` at `10,10`.
17. Let `u=2p`, `v=8q`; `uv=16pq=576`, so `u+v>=48`; min `48` when `2p=8q`, giving `p=12,q=3`.
18. Engel -> `1/x+1/y>=4`, equality `x=y=1/2`.
19. exact: `t^2+t^-2=(t+t^-1)^2-2=23`; generic AM-GM lower bound is `2` and is not the requested exact consequence.
20. balance integers `7,8`; max `56`.
21. Put `s=x+y`. `(x-y)^2=2(s+1012)-s^2>=0`; positive root bound is `<47`, so largest integer `46`.
22. AM-GM `a+b+c>=3(abc)^(1/3)=3`; equality `a=b=c=1`.
23. `x^2/y+y^2/x = (x^3+y^3)/(xy)`; with `x+y=8`, symmetric reduction or Engel gives minimum `8` at `x=y=4`. Direct Engel: `x^2/y+y^2/x >= (x+y)^2/(x+y)=8`.
24. real form `(n-7/2)^2+11/4`; integer min `3` at `n=3,4`; real min `11/4`.
25. `x+1/x>2` for `x>1`, and approaches `2` as `x->1+`; no minimum, infimum `2`.
26. Square completion answers value/location of vertex; discriminant canon answers root behavior/feasibility.
27. real: min 0 at 0; positive real: no minimum, infimum 0; nonzero integer: min 1 at `+-1`.
28. Inequality created a finite feasible interval; discrete/divisibility filters still decide admissible integers.
29. area `xy` under fixed `x+y` is maximized at equality; geometry supplies the context.
30. Any correct example, e.g. `x^2` on `x>0`.

## H0 answers

1. `(x-6)^2+4`; min `4`.
2. max `17` at `x=5`.
3. min `12` at `x=6`.
4. max `64` at `a=b=8`.
5. min `2/7` at `x=y=7`.
6. no minimum; infimum 0.
7. minimum `5/4` at `n=1,2`.
8. `(n-9/2)^2+11/4`; integer min `3` at `n=4,5`.
9. `10` is a lower bound but not attained under the stated equality mechanism; cannot claim minimum 10.
10. max `81` at `p=q=9`.
11. no minimum; infimum 0.
12. ALG-03; repeated-root/discriminant behavior is polynomial-root canon.
13. Evaluate the objective at admissible integers nearest 2.4 (and relevant boundaries), compare, then verify constraints.
14. `x+y=14`; max area `49` at `7,7`.
15. The inequality is a lower bound on the sum, not an upper bound. With fixed product, the sum is unbounded above.
16. Example `f(x)=1-1/x` on `x>0`: supremum 1, no maximum.

## Diagnostic tags

- `ALG02-R1` bound called extremum without equality.
- `ALG02-R2` equality condition identified but not checked against domain.
- `ALG02-R3` inequality direction does not match request.
- `ALG02-R4` continuous optimum accepted in discrete domain.
- `ALG02-R5` named theorem selected without matching structure/hypotheses.
- `ALG02-R6` discriminant/root doctrine imported from ALG-03.
