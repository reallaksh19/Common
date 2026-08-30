# ALG-04 — Teacher Diagnostic Key

## Recognition lab

1. `a_n=S_n-S_{n-1}`.
2. AP, difference 4.
3. GP, ratio 4.
4. subtract adjacent 5-term sums -> `a_{i+5}>a_i`.
5. `a_{n+2}-a_{n+1}=4(a_{n+1}-a_n)`.
6. `1/[k(k+1)]=1/k-1/(k+1)`.
7. `1/[(k-1)k]=1/(k-1)-1/k`.
8. model belongs to COMB-03; recurrence notation may use ALG-04.
9. search invariant/transformed recurrence before iteration.
10. use adjacent differences of `S_n` and then compare `a_{n+1}-a_n`.

## Practice answers

1. `46`.
2. `384`.
3. `a_n=2n`.
4. Neither AP nor GP; first differences are `3,5,7,9,...`.
5. `a_{i+4}>a_i`.
6. `20/21`.
7. `a_n=4n-3`, common difference 4.
8. Let `d_n=a_{n+1}-a_n`; then `d_{n+1}=3d_n`.
9. `1-1/n=(n-1)/n`.
10. `a_{i+5}>a_i` and `a_{i+7}<a_i`.
11. First differences double: `d_1=3`, `d_n=3*2^{n-1}`; hence `a_n=1+3(2^{n-1}-1)=3*2^{n-1}-2`.
12. `a_n=T_n-T_{n-1}=2T_{n-1}+2`.
13. `d_1=3`, `d_n=3*2^{n-1}`; `a_{10}=2+3(2^9-1)=1535`.
14. `1/[(2k-1)(2k+1)]=(1/2)[1/(2k-1)-1/(2k+1)]`; sum `= n/(2n+1)`.
15. Equality of adjacent 3-term sums gives `a_{i+3}=a_i`.

## H0 mastery answers

1. `a_n=S_n-S_{n-1}=8n-3`.
2. First differences multiply by 4. `d_1=3`; `a_n=2+3(4^{n-1}-1)/3=4^{n-1}+1`; `a_8=16385`.
3. `50/51`.
4. Adjacent-window subtraction gives `a_{i+6}>a_i`.
5. Adjacent-window equality gives `a_{i+4}=a_i`.
6. Neither; first differences `3,5,7,9,...` form an AP.
7. First differences double: `d_1=4`; `a_n=3+4(2^{n-1}-1)=2^{n+1}-1`; `a_{20}=2^{21}-1=2097151`.
8. `n/(2n+1)`.
9. COMB-03 owns state definition/counting decomposition; ALG-04 owns algebraic recurrence manipulation after the recurrence exists.
10. Evaluate explanation and correctness of transformed sequence/invariant.

## Diagnostic tags

- `ALG04-R1` term-vs-sum confusion.
- `ALG04-R2` AP/GP formula matching without invariant check.
- `ALG04-R3` moving-window cancellation not recognized.
- `ALG04-R4` recurrence brute-force dependence.
- `ALG04-R5` telescoping decomposition not recognized.
- `ALG04-R6` counting-state ownership confused with algebraic recurrence.

## Gate

A learner who can compute AP/GP formulas but cannot explain window cancellation or transform a recurrence has not assimilated the topic.
