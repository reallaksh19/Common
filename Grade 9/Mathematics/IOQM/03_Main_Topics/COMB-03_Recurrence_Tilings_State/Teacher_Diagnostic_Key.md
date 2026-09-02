# Teacher Diagnostic Key - Recurrence, Tilings & State Evolution

## Recognition Lab

1. B - freeze the leftmost unresolved column.
2. B - last bit controls immediate legality; parity controls final acceptance.
3. A - compare forward and reverse branching.
4. B - four E's create five gaps; choose three.
5. B - overlapping branches invalidate naive addition.
6. A - two equal proposed states have different futures, so the state is insufficient.
7. B - the recurrence is supplied; use the recurrence/sequence bridge rather than rederive counting structure.
8. B - branching choices without an optimizing opponent remain a state/reachability problem.

## First-Line Lab

1. `T_n = number of domino tilings of a 2 x n rectangle`.
2. Split valid strings into those beginning with `0` and those beginning with `10`; they leave lengths `n-1` and `n-2`.
3. Record `(remaining sum, whether previous part was 2)` or equivalent two-state notation.
4. From target value `y`, predecessors are `y-1` and, when `y` is even, `y/2`.
5. Use `(binary position, incoming carry)` or an equivalent bounded-part state.
6. Use `(remaining total, largest allowed part)` with include/exclude branching, or an explicit distinct-part representation.
7. After the first symbol has 3 choices, every later position has exactly 2 choices by symmetry, so `w_n=2w_{n-1}`.
8. Ask whether another player chooses moves to optimize an opposing outcome. If not, it is deterministic state evolution/reachability.

## Practice & Transfer Bank

1. First tile has length 1 or 2, so `a_n=a_{n-1}+a_{n-2}`, `a_0=a_1=1`; `a_6=13`.
2. Begin with `0` or `10`, so `b_n=b_{n-1}+b_{n-2}`, `b_0=1,b_1=2`; `b_5=13`.
3. Left edge is one vertical domino or two horizontals, so Fibonacci-type recurrence with `T_0=T_1=1`; `T_5=8`.
4. Final move is 1 or 2 steps; `r_0=1,r_1=1`; `r_7=21`.
5. `u_n=u_{n-1}+u_{n-3}`, with `u_0=u_1=u_2=1`; `u_7=9`.
6. First letter 3 choices, each later letter 2 choices; `3*2^4=48`. A three-last-letter state collapses by symmetry.
7. A width-1 branch uses one vertical domino; a width-2 branch is either two horizontals or one square tile. Hence `v_n=v_{n-1}+2v_{n-2}`, `v_0=v_1=1`; `v_5=21`.
8. Same first-symbol decomposition as item 2; `b_7=34`.
9. State by remaining sum and whether the previous part was 2. Dynamic count gives `19`.
10. Use state `(position,last bit,parity of ones)`. Transition DP gives `11`.
11. Remember the last bit and current run length 1 or 2. The valid counts are `2,4,6,10,16,26`; answer `26`.
12. Remember whether the last symbol is A or non-A together with parity of A-count; splitting B/C symmetrically is enough. Count `52`.
13. A path of length 8 is `1,2,3,6,7,14,15,30,31`. Breadth layers (or reverse layers from 31) contain no 31 earlier; minimum `8`.
14. A path of length 8 is `1,2,3,6,12,24,25,50,100`; reverse breadth search proves no shorter path; minimum `8`.
15. Distinct partitions of 8 are `8`, `7+1`, `6+2`, `5+3`, `5+2+1`, `4+3+1`; answer `6`.
16. Bounded-part DP over `1,2,4,8` with multiplicities `0,1,2` gives `5`.
17. Same recurrence as item 5; values reach `u_10=28`.
18. Four-state DP `(last bit, parity)` gives `27`.
19. A 5-move path is `2,5,10,13,26,29`. Reverse breadth layers from 29 do not contain 2 before depth 5; minimum `5`.
20. Place four E's, creating five gaps. Choose three gaps for the N's: `C(5,3)=10`. The direct gap bijection collapses the whole constraint in one choice, so recurrence is unnecessary overhead.

## Mixed Mastery Test

1. `55` - recurrence `a_n=a_{n-1}+a_{n-2}`, `a_0=a_1=1`; the length-9 value is `a_9=55`.
2. `55` - first-symbol split `0` or `10`.
3. `28` - two-state DP remembering whether the previous part was 2.
4. `43` - `v_n=v_{n-1}+2v_{n-2}`, `v_0=v_1=1`.
5. `17` - state `(last bit, parity)`.
6. `10` - one path is `1,2,3,6,7,14,15,30,31,62,63`; breadth/reverse breadth proves minimality.
7. `10` - independently checkable by distinct-part include/exclude DP.
8. `7` - bounded-part DP over powers `1,2,4,8,16` with multiplicities at most 2.
9. Position alone merges prefixes ending in 0 and 1 and also merges even/odd one-counts, although these have different legal continuations/acceptance. A sufficient state is `(position,last bit,parity of ones)`.
10. An adversarial game requires another player to choose moves with an opposing objective (or alternating strategic control). Multiple legal transitions alone only create branching in a state graph.

## Historical anchor diagnostic notes

- `IOQM-2023-Q08 = 59`: first-step tiling decomposition; independent reconstruction gives 21 domino-only configurations plus 38 with the special square structure.
- `IOQM-2024-Q20 = 10`: deterministic reverse-state shortest path; not game strategy.
- `IOQM-2024-Q14 = 80`: near-boundary history compresses to one exceptional step among 80 positions; recurrence is not the natural endpoint.
- `IOQM-2023-Q21 = 15`: residual 7 converts to a partition count `p(7)=15`.
- `IOQM-2023-Q26 = 19`: local carry-state counting; direct DP and carry DP agree.

## Diagnostic error map

- recurrence before state definition -> require one-sentence counted-state meaning;
- overlapping branches -> ask for one object that belongs to both branches, then redesign;
- omitted branch -> test exhaustive coverage on a small case;
- wrong base state -> draw/list the smallest configurations;
- state too small -> search for two same-state histories with different futures;
- state too large -> remove coordinates one at a time and retest future legality;
- forward explosion -> write inverse moves and compare branching;
- game confusion -> identify the opponent and objective; if absent, return to reachability;
- forced recurrence -> ask whether symmetry, gaps, residual structure, or direct representation is smaller.