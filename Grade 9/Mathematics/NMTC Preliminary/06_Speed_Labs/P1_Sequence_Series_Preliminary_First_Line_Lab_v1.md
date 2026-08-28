# P1 Sequence & Series — First-Line Lab v1

## Rule

Write exactly one mathematically useful first line. Do not finish the problem.

1. AP: `a_6=19`, `a_14=43`; find `d`.
2. GP: `a_4=24`, `a_9=768`; target `a_30/a_25`.
3. `Σ_{k=1}^{30} k(2k-1)`.
4. `a_{n+1}=a_n/(1+3a_n)`.
5. `a_{n+1}=4a_n+6`.
6. `a_{m+n}=a_m+a_n+3mn`, target `a_8`.
7. Infinite GP has sum 15 and sum of squares 45.
8. `S_n=2n²+5n`; find `a_n`.
9. `Σ 1/[k(k+2)]`.
10. `Σ 1/(sqrt(k+2)+sqrt(k))` over a same-parity range.
11. `4,10,18,28,40,...`.
12. Reproduced historical GP text disagrees with provisional key.

## Model first lines

1. `43-19=(14-6)d`.
2. `a_30/a_25=r^5`.
3. `Σ k(2k-1)=2Σk²-Σk`.
4. `b_n=1/a_n`.
5. Choose fixed-point shift: `b_n=a_n+2`, since `4(-2)+6=-2`.
6. Use strategic doubling, starting `(m,n)=(1,1)`.
7. `|r|<1`, `a/(1-r)=15`, `a²/(1-r²)=45`.
8. `a_n=S_n-S_{n-1}`.
9. `1/[k(k+2)]=(1/2)(1/k-1/(k+2))`.
10. Rationalize each term by multiplying by `sqrt(k+2)-sqrt(k)`.
11. First differences: `6,8,10,12,...`.
12. `Solve the printed relation independently; record SOURCE_KEY_CONFLICT if the key still disagrees.`

## Target

10/12 first lines correct before full solving.