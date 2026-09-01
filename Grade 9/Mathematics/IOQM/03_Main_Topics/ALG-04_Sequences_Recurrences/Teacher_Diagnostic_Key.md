# ALG-04 — Teacher Diagnostic Key

## Recognition and First-Line Lab

1. `a_n=S_n-S_{n-1}`.
2. AP; `a_{n+1}-a_n=4`.
3. GP; `a_{n+1}/a_n=4`.
4. Neither; first differences `3,5,7,9,...`.
5. Explicit form; substitute `n=100`.
6. Recursive form; record the recurrence range and initial value `a_1=1`.
7. Subtract adjacent 5-term windows: `a_{i+5}>a_i`.
8. Multiply by 7 and subtract adjacent windows: `a_{i+7}<a_i`.
9. `a_{n+2}-a_{n+1}=4(a_{n+1}-a_n)`.
10. `1/[k(k+1)]=1/k-1/(k+1)`.
11. No immediate neighboring-factor telescope; do not force one.
12. Define/compare `D_n=b_n^2-b_{n-1}b_{n+1}`; derive `D_{n+1}=7D_n`.
13. A is AP, constant difference 4; B is GP, constant ratio 3.
14. A explicit; B recursive.
15. A: subtract neighboring 4-term windows. B: `a_n=S_n-S_{n-1}`.
16. A telescopes immediately; B does not from this surface.
17. For the counting recurrence, the state and disjoint/exhaustive first-step decomposition must be proved.
18. Deterministic process -> COMB-03; adversarial game -> COMB-04.
19. Must verify all initial values and prove the formula satisfies the recurrence for every allowed index.
20. Enough starting values plus the recurrence's valid starting index/range.

## Practice and Transfer Bank

1. `46`.
2. `384`.
3. `a_n=2n`.
4. First is explicit. Second is recursive and needs the initial value `a_1=1` plus its valid index range.
5. Neither AP nor GP; first differences are `3,5,7,9,...`.
6. `a_{i+4}>a_i`.
7. `20/21`.
8. Initials: formula gives `1,4`. Substitution gives `3*2^(n+1)-2 = 3(3*2^n-2)-2(3*2^(n-1)-2)`, so the recurrence holds.
9. `a_n=4n-3`; common difference `4`.
10. Let `d_n=a_{n+1}-a_n`; then `d_{n+1}=3d_n`, `d_1=3`, so `a_n=2+sum_{j=1}^{n-1}3^j=(3^n+1)/2`; `a_8=3281`.
11. `1-1/n=(n-1)/n`.
12. Adjacent 3-term windows give `a_{i+3}=a_i`.
13. `a_{i+5}>a_i` and `a_{i+7}<a_i`.
14. `D_{n+1}=7D_n`, `D_1=1`; hence `D_20=7^19`. Stop there: converting this prime power to a divisor count is owned by NT-03 and is not required by the repaired ALG-04 item.
15. `a_n=T_n-T_{n-1}=2T_{n-1}+2`.
16. `1/[(2k-1)(2k+1)]=(1/2)[1/(2k-1)-1/(2k+1)]`; sum `n/(2n+1)`.
17. First differences double: `d_1=3`, `d_n=3*2^(n-1)`; `a_10=1535`.
18. Equal 4-term windows imply `a_{i+4}=a_i`; `99≡3 (mod 4)`, so `a_99=a_3=4`.
19. `a_n=n^3-(n-1)^3=3n^2-3n+1`. Differentiation is a continuous operation and is not the identity that isolates a discrete term; finite difference is.
20. Equal ratios in a finite prefix do not determine all future terms unless a rule is given.
21. `a_n=10n-4`.
22. `d_{n+1}=5d_n` for `d_n=a_{n+1}-a_n`.
23. `sum_{k=3}^{n}[1/(k-1)-1/k]=1/2-1/n`.
24. `a_{i+5}=a_i`; period divides 5.
25. If `R_i=r_i+...+r_{i+5}`, then `R_{i+1}-R_i=r_{i+6}-r_i>0`.
26. Layer `n` cost is `C_n-C_{n-1}=n`.
27. General invariant gives `Q_{n+1}=-3Q_n`; ratio `-3`.
28. Since `1/[k(k+1)]=1/k-1/(k+1)`, they are identical term-by-term representations.
29. In A, direct substitution is cheapest. In B, high index suggests a transform/invariant because the representation is recursive. High index alone is not a method label.
30. Sequence algebra: read notation, initialization, verify/manipulate a supplied recurrence. Counting-model ownership: define the state, prove a disjoint/exhaustive first-step decomposition, establish base states, and only then justify the recurrence.

## H0 control map for the learner-facing Independent Mixed Mastery Check

The H0 designation is retained here only as teacher/control metadata; it is not displayed in the learner-facing mastery title.

1. `a_n=S_n-S_{n-1}`.
2. If `W_i=a_i+...+a_{i+5}`, then `W_{i+1}-W_i=a_{i+6}-a_i>0`.
3. Explicit formula; substitute `n=50`.
4. `a_{n+2}-a_{n+1}=4(a_{n+1}-a_n)`.
5. `a_n=8n-3`.
6. First differences satisfy `d_{n+1}=4d_n`, `d_1=3`; this gives `a_n=4^(n-1)`, so `a_8=16384`.
7. `50/51`.
8. `a_{i+4}=a_i`; `99≡3 (mod 4)`, so `a_99=4`.
9. `D_{n+1}=7D_n`, `D_1=1`; hence `D_20=7^19`. No divisor-count theorem is required in ALG-04.
10. A: AP, difference 4. B: GP, ratio 3.
11. A explicit; B recursive. Without `a_1=4`, infinitely many sequences can satisfy `a_{n+1}=a_n+3`.
12. The first decomposes exactly as `1/k-1/(k+1)`; the second has no such immediate consecutive-factor identity and needs a different analysis.
13. `r_{i+5}>r_i`.
14. `Q_{n+1}=-3Q_n`.
15. Matching finitely many terms is not proof. Check all initial values and prove the formula satisfies the recurrence for every allowed `n`.
16. “Fibonacci-looking” notation does not prove a count. Define the tiling state, partition by the first step into disjoint/exhaustive cases, show the cases reduce to the claimed smaller states, and verify base states.

## Diagnostic codes

- `ALG04-D01 TERM_SUM_CONFUSION`
- `ALG04-D02 AP_GP_SURFACE_MATCHING`
- `ALG04-D03 EXPLICIT_RECURSIVE_CONFUSION`
- `ALG04-D04 INITIALIZATION_OMITTED`
- `ALG04-D05 RECURRENCE_VERIFICATION_BY_EXAMPLES`
- `ALG04-D06 WINDOW_CANCELLATION_NOT_RECOGNIZED`
- `ALG04-D07 HIGH_INDEX_BRUTE_FORCE`
- `ALG04-D08 TELESCOPE_FALSE_POSITIVE`
- `ALG04-D09 INDEX_SHIFT_OFF_BY_ONE`
- `ALG04-D10 ALGEBRAIC_VS_COUNTING_RECURRENCE_OWNER`
- `ALG04-D11 COUNTING_STATE_VS_ADVERSARIAL_GAME`
- `ALG04-D12 TRANSFER_REPRESENTATION_FAILURE`

## Remediation routing

- D01/D03/D04 -> revisit the Recurrence Interface card.
- D02 -> use AP/GP close contrasts with “neither” examples.
- D05 -> require initials + symbolic recurrence check.
- D06/D09 -> draw two aligned windows and cross out shared terms.
- D07 -> ask for one transformed quantity before any raw iteration.
- D08 -> require exact partial-fraction identity before summing.
- D10/D11 -> route state modelling to COMB-03 and adversarial strategy to COMB-04.
- D12 -> use rolling-total and machine-reading transfers without method labels.

## Historical anchor custody

- `IOQM-2025-Q26`: verified answer `10`; window-difference anchor.
- `IOQM-2023-Q10`: verified answer `51`; neighboring-term invariant anchor. The historical question's divisor-count finish remains source custody; new ALG-04 practice/mastery items no longer teach the NT-03 divisor-count doctrine.

Historical source wording remains controlled by the validated papers.
