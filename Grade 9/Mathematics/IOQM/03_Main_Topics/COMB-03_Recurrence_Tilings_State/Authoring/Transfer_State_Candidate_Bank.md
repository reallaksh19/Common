# COMB-03 Transfer / State Candidate Bank

Status: `AUTHORING_ONLY_RESEARCH_CANDIDATES`

These are source-independent candidates for later pedagogy. They are **not** promoted student items yet. Promotion waits for COMB-01 interface acceptance and full item-level metadata/QA.

Every candidate is selected to test a changed surface while preserving the state-first doctrine.

## Candidate set

| ID | Surface | State decision | Structural relation / method | Checked target |
|---|---|---|---|---:|
| C03-T01 | `2 x n` domino tilings | remaining board length `n` is sufficient | `t_n=t_{n-1}+t_{n-2}`, `t_0=t_1=1` | `t_8=34` |
| C03-T02 | `1 x n` strip with tiles of lengths 1 and 3 | remaining length is sufficient | `u_n=u_{n-1}+u_{n-3}`, `u_0=u_1=u_2=1` | `u_7=9` |
| C03-T03 | binary strings with no consecutive 1s | length alone works after first-symbol decomposition | `a_n=a_{n-1}+a_{n-2}`, `a_0=1,a_1=2` | `a_8=55` |
| C03-T04 | compositions with parts 1 or 2, but no consecutive 2s | must remember whether previous part was 2 | two-state recurrence / DP | total for sum `8` is `19` |
| C03-T05 | machine `x -> x+1` or `x -> 2x` | current integer is state; target suggests search | BFS / reverse-search contrast | min moves `1 -> 31` is `8` |
| C03-T06 | same machine, larger target | current integer; reverse direction has small predecessors | reverse BFS | min moves `1 -> 100` is `8` |
| C03-T07 | `2 x n` tiling by dominoes plus one `2 x 2` square-tile type allowed any number of times | remaining length sufficient; width-2 placements create two length-2 branches | `v_n=v_{n-1}+2v_{n-2}`, `v_0=v_1=1` | `v_6=43` |
| C03-T08 | words over `{A,B,C}` with adjacent letters different | last letter class is symmetric | `w_n=2w_{n-1}`, `w_1=3` | `w_6=96` |
| C03-T09 | lattice words with 4 E and 3 N, no consecutive N | previous symbol / gap state | state DP or gap representation | count `10` |
| C03-T10 | partitions of 8 into distinct positive parts | remaining total + next allowable part | include/exclude state recurrence | count `6` |
| C03-T11 | representations of 10 as sum of powers of 2, each power usable 0,1,2 times | digit position + carry / remaining sum | carry-state or bounded-part DP | count `5` |
| C03-T12 | length-6 binary strings, no consecutive 1s, even number of 1s | last bit + parity are both required | four-state transition DP | count `11` |

## Independent checks

### C03-T01
`1,1,2,3,5,8,13,21,34`; target `34`.

### C03-T02
`1,1,1,2,3,4,6,9`; target `9`.

### C03-T03
`1,2,3,5,8,13,21,34,55`; target `55`.

### C03-T04
Direct state DP gives totals by target sum
`1,1,2,3,4,6,9,13,19,...`; target `19` for sum 8.

This candidate is useful specifically because a naive one-state "last part ignored" recurrence is unsafe; the previous-part flag is real state information.

### C03-T05
One 8-move path:
`1 -> 2 -> 3 -> 6 -> 7 -> 14 -> 15 -> 30 -> 31`.
Independent breadth-first search finds no path with fewer than 8 moves.

### C03-T06
One 8-move path:
`1 -> 2 -> 3 -> 6 -> 12 -> 24 -> 25 -> 50 -> 100`.
Independent breadth-first search confirms minimum 8.

The pedagogical purpose is not BFS syntax; it is the representation decision "forward or reverse?".

### C03-T07
`v_0=1,v_1=1`; then
`v_2=3,v_3=5,v_4=11,v_5=21,v_6=43`.
The two width-2 branches are (i) two horizontal dominoes and (ii) one square tile; they are distinct construction types.

### C03-T08
First symbol has 3 choices; each later symbol has 2 choices. Recurrence form `w_n=2w_{n-1}` gives `w_6=3*2^5=96`.
This is a useful close contrast against a genuine two-state recurrence: apparent state can collapse by symmetry.

### C03-T09
Choosing 3 nonadjacent N positions among a word with 4 E is equivalent to choosing 3 of the 5 gaps around the E symbols, giving `C(5,3)=10`. A state-DP route must agree.
This is a representation-choice transfer: recurrence is available but not automatically best.

### C03-T10
Independent include/exclude partition recursion gives 6 distinct-part partitions of 8. This checks transfer from path-like states to representation states.

### C03-T11
Independent bounded-part DP over powers `1,2,4,8` with multiplicities 0,1,2 gives 5 representations of 10. A binary carry-state derivation is the intended alternate representation.

### C03-T12
A direct exhaustive check and a four-state DP indexed by `(last_bit, parity)` both give 11. Dropping either memory component merges states with different futures/acceptance conditions.

## Promotion filters after COMB-01 arrives

Each candidate must then receive:
1. a counted-object statement using COMB-01 canonical vocabulary;
2. explicit disjoint/exhaustive branch proof where recurrence is used;
3. initialization check;
4. small-case verification;
5. H3/H2/H1/H0 support plan;
6. misconception target;
7. metadata row;
8. independent answer audit after final wording;
9. owner-boundary check against COMB-01, ALG-04, COMB-04 and NT-05.

## Intended contrast pairs

- T01 vs T09: recurrence is natural vs direct representation is cleaner.
- T03 vs T04: one-state recurrence sufficient vs hidden-memory state required.
- T05/T06: forward search vs reverse-search choice.
- T07 vs T08: multiple structural branches vs symmetry-collapsed transition.
- T10 vs T11: representation recursion vs carry-state recursion.
- T04 vs T12: one memory bit vs two independent state coordinates.

No candidate is yet counted toward student practice, H0 mastery or psychometric coverage.