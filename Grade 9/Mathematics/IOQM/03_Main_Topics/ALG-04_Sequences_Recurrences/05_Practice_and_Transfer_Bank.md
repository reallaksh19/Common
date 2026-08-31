# ALG-04 — Practice and Transfer Bank

First attempt every item at H0. The first section repairs foundations; later sections increase decision complexity.

## F0 — Foundation

1. Find the 15th term of `4,7,10,...`.
2. Find the 8th term of `3,6,12,...`.
3. If `S_n=n(n+1)`, find `a_n`.
4. Classify each representation:
   - `a_n=2n^2-1`;
   - `a_{n+1}=a_n+2n+1`, `a_1=1`.
   State what initialization the recursive form needs.

## F1 — Direct structure

5. Determine whether `2,5,10,17,26,...` is AP, GP, or neither. Identify a simpler pattern in its first differences.
6. If every 4-term sum is larger than the preceding 4-term sum, derive a direct inequality involving `a_i` and `a_{i+4}`.
7. Evaluate `sum_{k=1}^{20} 1/[k(k+1)]`.
8. Verify, not merely test, that
   `a_n=3*2^(n-1)-2`
   satisfies
   `a_{n+2}=3a_{n+1}-2a_n`,
   `a_1=1,a_2=4`.

## F2 — Standard

9. If `S_n=2n^2-n`, show that the resulting sequence is an AP and find its common difference.
10. Given `a_{n+2}=4a_{n+1}-3a_n`, `a_1=2,a_2=5`, transform to first differences and find `a_8`.
11. Evaluate `sum_{k=2}^{n} 1/[k(k-1)]`.
12. All 3-term sums of a sequence are equal. Prove the sequence is periodic with period dividing 3.

## F3 — Disguised

13. Five-term averages are increasing and seven-term averages are decreasing. Translate both statements into term inequalities before doing anything else.
14. Let `b_0=0,b_1=1` and
    `b_{n+2}=-4b_{n+1}-7b_n`.
    Define `D_n=b_n^2-b_{n-1}b_{n+1}`.
    Find `D_20` and the number of its positive divisors without computing `b_20`.
15. Let `T_n=a_1+...+a_n` and
    `T_n=3T_{n-1}+2` for `n>=2`.
    Rewrite `a_n` directly in terms of `T_{n-1}`.
16. Evaluate
    `sum_{k=1}^{n} 1/[(2k-1)(2k+1)]`
    by telescoping.

## F4 — Preliminary-style

17. A sequence satisfies
    `a_{n+2}-a_{n+1}=2(a_{n+1}-a_n)`,
    with `a_1=2,a_2=5`.
    Find `a_10` efficiently.
18. All 4-term sums are equal. If
    `a_1=1,a_2=2,a_3=4,a_4=8`,
    find `a_99`.
19. If `S_n=n^3`, find `a_n`. Explain why “differentiate n^3” is not a valid discrete argument even though the resulting expression is also quadratic.
20. A student says: “The first three ratios are equal, so the infinite sequence is definitely a GP.” Give the smallest logical objection.

## Support-fading tracks

These four tasks deliberately reduce the **maximum available** hint support.

### H3-available
21. `S_n=5n^2+n`. Find `a_n`.
- H1 if needed: compare neighboring accumulated totals.
- H2 if needed: use `S_n-S_{n-1}`.
- H3 if needed: start with `a_n=(5n^2+n)-[5(n-1)^2+(n-1)]`.

### H2-maximum
22. `a_{n+2}=6a_{n+1}-5a_n`. Find a simpler recurrence.
- H1 if needed: compare neighboring terms.
- H2 if needed: study first differences.

### H1-maximum
23. Evaluate `sum_{k=3}^{n} 1/[(k-1)k]`.
- H1 if needed: consecutive factors suggest local cancellation.

### H0
24. Every 5-term sum equals the preceding 5-term sum. Prove the strongest simple periodicity statement you can.

## Transfer bank

25. **T3 context change — rolling totals.**  
    A sensor's consecutive 6-day totals are strictly increasing. Without computing any total explicitly, prove a direct inequality between two readings six days apart.

26. **T2 representation change — accumulation to contribution.**  
    A layered design has cumulative cost `C_n=n(n+1)/2` after `n` layers. Find the cost of layer `n` using no summation formula.

27. **T3 context change — invariant audit.**  
    Machine readings satisfy
    `x_{n+2}=2x_{n+1}+3x_n`.
    For `Q_n=x_n^2-x_{n-1}x_{n+1}`, determine `Q_{n+1}/Q_n` whenever `Q_n!=0`.

28. **T2 representation change — telescope recognition.**  
    Compare
    `sum (1/k-1/(k+1))`
    with
    `sum 1/[k(k+1)]`.
    Explain why they are the same cancellation written in different representations.

29. **T3 close boundary — local versus global.**  
    Problem A gives an explicit `a_n=f(n)` and asks for `a_500`.  
    Problem B gives a second-order recurrence and asks for `a_500`.  
    Explain why “high index” alone does not determine the method.

30. **T4 ownership bridge — counting state.**  
    A tiling count is asserted to satisfy `t_n=t_{n-1}+t_{n-2}`.
    List what ALG-04 can verify once this recurrence is supplied, and what COMB-03 must prove before the recurrence is legitimate.
