# P2 Greatest / Least Integer Functions — Recognition Lab v1

**Rule:** classify the first move only. Do not fully solve.

1. `floor(4x-1)=7` → `FL`
2. `ceil(2x+5)=-3` → `CE`
3. evaluate `floor(-4.02)` → `NEG`
4. evaluate `{-9/4}` → `FR`
5. rewrite `ceil(t)` using floor → `RF`
6. simplify `floor(x+8)` → `SH`
7. `floor(3x)>=5` → `FI`
8. `ceil(3x)<=5` → `CI`
9. `x+floor(x)=c` → `NX`
10. `floor(ceil(x))` → `NE`
11. compare `floor(x)+floor(y)` with `floor(x+y)` → `SUM`
12. count integers in `[a,b]` → `CNT`
13. `floor(sqrt(n))=k` → `SQ`
14. a GP problem ends by taking `floor(answer)` → `QC`
15. `floor(x)=floor(2x)` → `NX`
16. prove a floor identity with shifts `1/3,2/3` → `FR`
17. `ceil(x)=-floor(-x)` appears → `RF`
18. claim `floor(-2.8)=-2` → `NEG`
19. count complete groups of size `d` from `N` objects → `FL`
20. minimum groups of capacity `d` for `N` objects → `CE`

## Target

- 18/20 correct under 3 minutes;
- zero confusion between `FL` and `CE` endpoint directions;
- zero truncation errors for negative inputs.
