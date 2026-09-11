# COMB-02 Independent Mathematics and Source Audit

Status: `HISTORICAL_ANSWERS_INDEPENDENTLY_CLOSED_VISUAL_CUSTODY_PENDING`

The six historical answers are re-derived below from the controlled source statements. The repository verification ledger is used only as a final answer check. Exact page/figure custody remains a separate gate for any item with a geometric surface.

## IOQM-2025-Q08 — proper vertex colouring

A quadrilateral `ABCD` has its four sides plus diagonal `AC`. Each vertex is coloured using four colours, and endpoints of every listed edge must have different colours.

The graph is `K4` with edge `BD` removed.

- choose colour of `A`: `4` ways;
- `C` must differ from `A`: `3` ways;
- `B` is adjacent to both `A,C`: `2` ways;
- `D` is also adjacent to both `A,C` but not to `B`: `2` ways.

Total:

`4*3*2*2 = 48`.

Independent result: `48` — PASS.

Contrast preserved: unrestricted `4^4` assignments are not proper colourings.

---

## IOQM-2025-Q29 — colourful regular polygon

Condition: any five consecutive vertices have pairwise distinct colours, using at most six colours.

Graph model: vertices of `C_n`; join two vertices when their cyclic distance is at most `4`. The problem asks whether `C_n^4` is 6-colourable.

A colour class can contain at most

`floor(n/5)`

vertices, because equal-coloured vertices must be separated by at least five steps around the cycle.

For `n=19`, each colour class has size at most `3`. Six colours can cover at most `18` vertices. Hence `n=19` is not colourful.

It remains to show every `n>=20` is colourful.

Base cyclic colourings for lengths `20,21,22,23,24` are:

- `20`: `12345123451234512345`
- `21`: `123451234512345123456`
- `22`: `1234512345123451623456`
- `23`: `12345123451263415623456`
- `24`: `123451236412563145623456`

In each word, equal symbols are separated by at least five positions cyclically, so every block of five consecutive vertices has distinct colours.

Appending a full block `12345` preserves that separation at the join and around the cycle. Therefore every length `20+5q`, `21+5q`, ..., `24+5q` is colourful.

Thus every `n>=20` is colourful, while `19` is not.

Independent result: `19` — PASS.

---

## IOQM-2024-Q09 — knight-move pairs on a 5x5 grid

Each knight-move pair is the diagonal pair of a `3x2` or `2x3` rectangle.

- number of `3x2` placements: `(5-2)(5-1)=12`; each contributes `2` knight edges -> `24`;
- number of `2x3` placements: `(5-1)(5-2)=12`; each contributes `2` knight edges -> `24`.

Total unordered knight-move pairs:

`24+24=48`.

Independent result: `48` — PASS.

Equivalent handshaking interpretation: count directed knight moves, then divide by two.

---

## IOQM-2024-Q19 — red/blue edges on five points, no monochromatic triangle

The complete graph is `K5`.

At any vertex there are four incident edges. Three incident edges cannot have the same colour: if three red edges joined the vertex to three neighbours, then every edge among those neighbours would have to be blue to avoid a red triangle, creating a blue triangle among the three neighbours. The same argument applies with colours reversed.

Therefore every vertex has exactly two red and two blue incident edges.

Hence the red subgraph is 2-regular on five labelled vertices, so it must be a 5-cycle. Its complement is automatically the blue 5-cycle.

The number of labelled undirected 5-cycles is

`(5-1)!/2 = 12`.

Each red 5-cycle determines exactly one valid red/blue colouring.

Independent result: `12` — PASS.

---

## IOQM-2023-Q16 — hexagon diagonals, every triangle has a red side

All six boundary sides are already red. Only the nine diagonals can be red or blue.

A forbidden all-blue triangle must use three diagonals. In a hexagon, the only triples of vertices whose three mutual edges are all diagonals are the alternating triples

`{A1,A3,A5}` and `{A2,A4,A6}`.

Thus among the nine diagonal edges there are exactly two forbidden blue triangles. Their edge sets are disjoint; the remaining three diagonals are the three opposite-vertex diagonals.

Count all diagonal colourings and exclude those containing either all-blue triangle:

`N = 2^9 - 2*2^6 + 2^3`

`= 512 - 128 + 8`

`= 392`.

The question asks for the sum of the squares of the digits of `N`:

`3^2 + 9^2 + 2^2 = 9+81+4 = 94`.

Independent result: `94` — PASS.

---

## IOQM-2023-Q22 — four cevians and exactly nine regions

An equilateral triangle has five admissible interior pegs on each side. Four distinct pegs are chosen, and each is joined to the opposite vertex.

Let `(n_A,n_B,n_C)` be the numbers of chosen cevians from the three vertices, with

`n_A+n_B+n_C=4`.

For `m=4` segments, if an interior intersection point has `r` concurrent segments, the region count is

`R = 1 + m + sum(r-1)`

over distinct interior intersection points.

To obtain `R=9`, the intersection contribution must be `4`.

### Distribution `(2,2,0)`

There are

`n_A n_B + n_B n_C + n_C n_A = 4`

cross-family pairs, and no triple concurrency is possible with only two families. Hence every `(2,2,0)` choice gives nine regions.

Count:

- choose the absent family: `3` ways;
- choose two of five pegs on each active side: `C(5,2)^2=100`.

Contribution:

`3*100=300`.

### Distribution `(2,1,1)`

There are `5` cross-family pairs. To reduce the intersection contribution from `5` to `4`, exactly one triple concurrency is required. A triple point replaces three pairwise intersections by one point with contribution `2`, reducing the total by `1`.

For one cevian from each vertex, let the chosen side positions be `i,j,k` steps from the corresponding cyclic vertices, where each lies in `{1,2,3,4,5}`. By Ceva, concurrency is equivalent to

`[i/(6-i)] [j/(6-j)] [k/(6-k)] = 1`,

or

`ijk = (6-i)(6-j)(6-k)`.

The solutions are:

- permutations of `(1,3,5)`: `6`;
- permutations of `(2,3,4)`: `6`;
- `(3,3,3)`: `1`.

So there are `13` concurrent one-from-each-family triples.

For each concurrent triple:

- choose which of the three families is doubled: `3` ways;
- choose one additional peg on that side, different from the concurrent peg: `4` ways.

Contribution:

`13*3*4 = 156`.

Therefore the number of four-peg selections producing exactly nine regions is

`N = 300+156 = 456`.

The required digit-square sum is

`4^2+5^2+6^2 = 16+25+36 = 77`.

Independent result: `77` — PASS.

---

## Audit disposition

- six historical numerical answers independently re-derived: 6/6 PASS;
- graph modelling precedes terminology/formula use: PASS;
- COMB-01 retrieval boundary respected: PASS;
- no generic P&C / complement / inclusion-exclusion chapter duplicated: PASS;
- exact geometric-surface page/figure custody for publication: `PENDING`;
- classroom timing/readability: `NOT_RUN`.

Next authoring gate: build the seven A-P microstream interfaces and make the modelling decision (`objects -> adjacency/incidence -> graph invariant`) the cross-cutting learner routine.
