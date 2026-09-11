# COMB-03 — Independent Mathematical Research Audit

Status: `PASS_RESEARCH_ANCHORS__STUDENT_PROMOTION_NOT_STARTED`

Purpose: independently reconstruct the numerical mechanism of the five validated COMB-03 anchors without treating the classifier first-move field as a proof. Exact historical wording/figures remain under validated-paper custody before student reproduction.

## 1. IOQM-2023-Q08 — tilings with at most one `2 x 2` square

Verified key: `59`.

Let `f_n` be the number of domino-only tilings of a `2 x n` board.

Leftmost placement gives

`f_n=f_{n-1}+f_{n-2}`,

with

`f_0=1`, `f_1=1`.

Thus

`f_2=2, f_3=3, f_4=5, f_5=8, f_6=13, f_7=21`.

So domino-only tilings of `2 x 7` contribute `21`.

For tilings using exactly one `2 x 2` square, let that square occupy columns `j,j+1`, where `j=1,...,6`.

The left and right regions are independent domino-only boards of lengths `j-1` and `6-j`, so the count is

`sum_{j=1}^6 f_{j-1} f_{6-j}`

`=1*8 + 1*5 + 2*3 + 3*2 + 5*1 + 8*1`

`=8+5+6+6+5+8`

`=38`.

Total:

`21+38=59`.

Audit verdict: **PASS**.

Pedagogical finding: the recurrence is not justified by the Fibonacci-looking output. It is justified by the exhaustive/disjoint leftmost placement. The one-special-square variant also demonstrates why a resource flag/state may be needed in the general formulation.

---

## 2. IOQM-2024-Q20 — deterministic state graph / reverse search

Verified key: `10`.

Allowed forward moves from a positive integer state are:

- `x -> 2x`;
- `x -> x-3`.

An explicit 10-move path from `11` to `121` is

`11 -> 8 -> 5 -> 10 -> 20 -> 17 -> 34 -> 31 -> 62 -> 124 -> 121`.

That proves the distance is at most 10.

Independent breadth-first search on the exact state graph, retaining positive states and a safe finite envelope beyond the target, reaches `121` for the first time at depth 10. Repeating the search backward gives the same distance using predecessors:

- `y -> y/2` when `y` is even;
- `y -> y+3`.

Therefore no path of length 9 or less exists.

Audit verdict: **PASS — minimum 10**.

Pedagogical finding: this is deterministic shortest-path/state evolution. No opponent chooses moves against the learner, so game-strategy doctrine does not belong here. The reverse direction is a representation choice, not a different problem.

---

## 3. IOQM-2024-Q14 — near-boundary state collapse

Verified key: `80`.

The independently verified corpus route establishes that after 80 evolution steps, the target horizontal displacement `79` is one unit below the maximum possible displacement `80`.

Consequently the entire history must contain:

- exactly 79 right/+1 steps;
- exactly one zero-horizontal step.

There are exactly 80 possible positions for that exceptional step in an 80-step history.

Thus the target particle/state count is

`C(80,1)=80`.

Audit verdict: **PASS**.

Pedagogical finding: apparent global branching collapses when the target lies one unit from an extremal boundary. The first move should be to characterize admissible histories from the target, not to generate the whole evolution tree.

---

## 4. IOQM-2023-Q21 — monotone state / partition representation

Verified key: `15`.

The independent corpus verification reduces the problem to maximizing the baseline triangular contribution

`1+2+...+n = n(n+1)/2`

under the total `2023` constraint. The maximal admissible `n` is `63`, since

`63*64/2 = 2016`

and

`64*65/2 = 2080 > 2023`.

The residual is

`2023-2016=7`.

After subtracting the forced baseline, the remaining monotone nonnegative increments are in bijection with integer partitions of `7`.

The partition number is

`p(7)=15`.

For completeness, the 15 partitions are:

`7`;  
`6+1`;  
`5+2`; `5+1+1`;  
`4+3`; `4+2+1`; `4+1+1+1`;  
`3+3+1`; `3+2+2`; `3+2+1+1`; `3+1+1+1+1`;  
`2+2+2+1`; `2+2+1+1+1`; `2+1+1+1+1+1`;  
`1+1+1+1+1+1+1`.

Audit verdict: **PASS**.

Pedagogical finding: this is a deliberate boundary example. State thinking does not imply “write a recurrence.” A representation/bijection to partitions is cheaper than evolving a recurrence table.

---

## 5. IOQM-2023-Q26 — binary representation with coefficients `0,1,2`

Verified key: `19`.

We count solutions of

`100 = sum d_k 2^k`, where each `d_k in {0,1,2}`.

Binary expansion:

`100 = (1100100)_2`.

Process bits from least significant to most significant. A state needs only:

- current bit position;
- incoming carry `c`.

At a target bit `b`, choose `d in {0,1,2}` satisfying

`d + c = b + 2c'`.

This determines the outgoing carry `c'`.

Starting with carry 0, the counts of paths in carry states after the significant bits evolve as follows (states shown as `{carry 0 count, carry 1 count}`):

- after bit 0 (`b=0`): `{1,1}`;
- after bit 1 (`b=0`): `{1,2}`;
- after bit 2 (`b=1`): `{3,2}`;
- after bit 3 (`b=0`): `{3,5}`;
- after bit 4 (`b=0`): `{3,8}`;
- after bit 5 (`b=1`): `{11,8}`;
- after bit 6 (`b=1`): `{19,8}`.

After processing higher zero bits, valid completed representations are exactly the paths returning to carry 0. The count remains `19`.

A separate direct dynamic program over powers `1,2,4,8,16,32,64`, allowing coefficients `0,1,2` and sums at most 100, independently returns 19 representations of 100.

Audit verdict: **PASS**.

Pedagogical finding: the full earlier choice history is irrelevant. The carry is the minimal sufficient memory. Omitting it makes the state too small; storing all chosen coefficients makes it unnecessarily large.

---

## Cross-anchor mathematical conclusions

The five anchors support one coherent state doctrine rather than five unrelated tricks:

1. define exactly what is counted/reached;
2. retain only information that can affect future legal choices;
3. partition by disjoint structural transitions when deriving a recurrence;
4. include base states and verify small cases;
5. choose the cheaper direction/representation of the state graph;
6. do not force recurrence when a bijection/representation collapses the problem more directly.

## Audit state

```text
IOQM-2023-Q08 = PASS_59
IOQM-2024-Q20 = PASS_10
IOQM-2024-Q14 = PASS_80
IOQM-2023-Q21 = PASS_15
IOQM-2023-Q26 = PASS_19
SOURCE_IDS = PASS
EXACT_STEM_STUDENT_REPRODUCTION = NOT_STARTED
AUTHOR_CREATED_ITEM_AUDIT = NOT_STARTED
COMB01_DEPENDENCY = BLOCKED_NOT_LOCATED
```

This audit closes the numerical research check for the five anchors. It does not authorize integrated student prose before the COMB-01 interface is consumed.
