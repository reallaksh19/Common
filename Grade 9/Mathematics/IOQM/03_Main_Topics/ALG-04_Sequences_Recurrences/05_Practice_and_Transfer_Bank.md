# ALG-04 — Practice and Transfer Bank

## F0 Foundation

1. Find the 15th term of `4,7,10,...`.
2. Find the 8th term of `3,6,12,...`.
3. If `S_n=n(n+1)`, find `a_n`.

## F1 Direct

4. Determine whether `2,5,10,17,26,...` is AP, GP, or neither; identify a simpler difference pattern.
5. If every 4-term sum is larger than the preceding one, derive a direct inequality involving `a_i` and `a_{i+4}`.
6. Evaluate `sum_{k=1}^{20} 1/[k(k+1)]`.

## F2 Standard

7. If `S_n=2n^2-n`, show the resulting sequence is an AP and find its common difference.
8. Given `a_{n+2}=4a_{n+1}-3a_n`, show first differences form a GP.
9. Evaluate `sum_{k=2}^{n} 1/[k(k-1)]`.

## F3 Disguised

10. Five-term averages of a sequence are increasing. Seven-term averages are decreasing. Translate both statements into index-shift inequalities before doing anything else.
11. Let `a_1=1,a_2=4` and `a_{n+2}=3a_{n+1}-2a_n`. Find a closed form by first studying first differences.
12. Suppose `T_n=a_1+...+a_n` and `T_n=3T_{n-1}+2` for `n>=2`. Rewrite the recurrence directly in terms of `a_n` and `T_{n-1}`.

## F4 Preliminary-style

13. A positive sequence satisfies `a_{n+2}-a_{n+1}=2(a_{n+1}-a_n)` and `a_1=2,a_2=5`. Find `a_{10}` without generating every term one by one.
14. Evaluate `sum_{k=1}^{n} 1/[(2k-1)(2k+1)]` by telescoping.
15. A sequence has all 3-term sums equal. Prove the sequence is periodic with period dividing 3.

## Transfer

16. Explain the common cancellation idea behind `S_n-S_{n-1}` and moving-window subtraction.
17. Give a recurrence problem where first differences are easier than the original terms.
18. Explain why a tiling recurrence should be modelled in COMB-03 even if the final algebra looks identical to a sequence recurrence.
