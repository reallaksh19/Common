# P2 Mathematical Induction — First-Line Lab v1

Write only the first mathematically useful line after the induction hypothesis is stated.

1. `1+3+...+(2n-1)=n^2`.
2. `2+4+...+2n=n(n+1)`.
3. `5 | (6^n-1)`.
4. `7 | (8^n-1)`.
5. `2^n>=n+1` for `n>=0`.
6. `3^n>n^2` for `n>=2`.
7. `2*4*...*2n=2^n n!`.
8. Verify `a_n=3*2^(n-1)-1` for `a_{n+1}=2a_n+1`.
9. Proof naturally gives `P(k)->P(k+2)`.
10. Next recurrence term depends on two previous terms.
11. Prove `6 | (n^3-n)` but direct factorization is visible.
12. A source labels an item “NMTC induction PYQ” without a stable source locator.

## Review key

1. `S_{k+1}=S_k+(2k+1)`.
2. `S_{k+1}=S_k+2(k+1)`.
3. `6^(k+1)-1=6(6^k-1)+5`.
4. `8^(k+1)-1=8(8^k-1)+7`.
5. `2^(k+1)=2*2^k>=2(k+1)`.
6. `3^(k+1)=3*3^k>3k^2`.
7. `P_{k+1}=P_k*2(k+1)`.
8. `a_{k+1}=2[3*2^(k-1)-1]+1`.
9. Establish enough base cases to cover both parity chains before concluding all n.
10. Plan two base cases and a hypothesis containing both required previous cases, or use strong induction.
11. `n^3-n=n(n-1)(n+1)`; direct proof is cheaper.
12. Stop attribution and mark provenance unresolved; do not invent a PYQ ID.

## Scoring

- 10–12: first-move ready
- 7–9: targeted repair
- <=6: return to concept draft

`CLASSROOM_TIMING_CALIBRATION: NOT_RUN`
