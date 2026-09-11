# Teacher Diagnostic Key — Graphs, Colouring and Incidence Counting

## Recognition and First-Line Lab

1. B. Vertices are people; edges are the communicating pairs.
2. B. `sum degrees=2|E|`.
3. B. These are proper vertex colourings because adjacency forbids equal colours.
4. A. The endpoints of the missing edge are non-adjacent and may share a colour.
5. B. Cyclic wrap-around can create extra conflicts between the final and initial positions.
6. A. Halving is valid only if every unordered pair was counted exactly twice.
7. A. If only crossings/concurrencies matter, incidence structure is the cheaper representation.
8. B. Turn, history and remaining options can matter in a game state.

9. Example: “Each student is a vertex; two vertices are joined exactly when those students are friends.”
10. `2|E|=4+3+3+2+2+2=16`, so `|E|=8`.
11. `5*4*3`.
12. Join two cycle vertices exactly when their cyclic distance is 1 or 2.
13. Vertex = one board square; edge = one unordered pair of squares connected by a legal knight move.
14. Count `{(line,point): the selected point lies on the line}`.
15. Fix one vertex and inspect the colours of its four incident edges.
16. At minimum record the player to move and the current remaining/legal configuration; resource counts/history may also matter if they change future moves.

## Practice and Transfer Bank

1. Degree sum `10`, so `5` edges.
2. No. The degree sum would be `11`, but every graph has even degree sum.
3. First vertex `3` choices, then `2` choices at each of the next three vertices: `3*2^3=24`.
4. `4*3*2=24`.
5. Let the missing edge be `CD`. Colour `A`: 3; `B`: 2; `C`: 1; `D`: 1 because it may equal C but must differ from A and B. Total `6`.
6. `K_(3,3)` has `3*3=9` edges. Degree sum is six vertices of degree 3, total 18, hence 9 edges.
7. Knight edges on an `m x n` board: `2(m-1)(n-2)+2(m-2)(n-1)`. For `4 x 4`: `12+12=24`.
8. `3*4=12` edges; degree sum `3*4+4*3=24`, hence 12.
9. For a 5-cycle and 3 colours: `(3-1)^5-(3-1)=32-2=30`.
10. Degree sum `12`, so `6` edges.
11. Count line-point incidences: `8*3=24`. Each selected point is counted twice, so there are `12` points.
12. A `3 x 2` knight rectangle has two knight edges. There are 12 placements of each orientation on a `5 x 5` board, so `24+24=48`.
13. The number of odd-degree vertices must be even because the total degree sum is even. Hence exactly one odd-degree vertex is impossible.
14. Once the first two colours are distinct, the third is forced to be the remaining colour, and the pattern repeats with period 3. Since `12` is divisible by 3, any ordered choice of distinct first two colours works: `3*2=6`.
15. Fix a vertex of `K6`. Among its 5 incident edges, at least 3 have one colour, say red, to vertices A,B,C. If any of AB,BC,CA is red, there is a red triangle with the fixed vertex; if none is red, all three are blue, giving a blue triangle ABC.
16. Total membership incidences `10*6=60`. Each student contributes 3 incidences, so there are `60/3=20` students.
17. `48`. The graph is `K4` minus one edge: `4*3*2*2`.
18. `48`, by the `3 x 2` / `2 x 3` rectangle count or directed-degree count divided by 2.
19. `12`. Every vertex must have exactly two red and two blue incident edges, so the red graph is a labelled 5-cycle; there are `(5-1)!/2=12` such cycles.
20. `19`. Equal-coloured vertices must be separated by at least five cyclic steps. For `n=19`, six colour classes cover at most `6*floor(19/5)=18` vertices, impossible. Explicit valid cyclic patterns exist for 20 through 24 and appending a full five-colour block extends them to every larger `n`; hence 19 is largest non-colourful.
21. `392`. Only the two alternating vertex triples can have all three sides among the nine diagonals. Inclusion-exclusion on those two disjoint all-blue triangles gives `2^9-2*2^6+2^3=392`.
22. `9` regions. There are four segments and four cross-family intersections, with no triple concurrency. Region count is `1+4+4=9`.

## Mixed Mastery Test

1. Degree sum `14`, so `7` edges.
2. No. The degree sum is `19`, which is odd.
3. `4*3^4=324`.
4. Proper colourings of `C4` with 3 colours: `(3-1)^4+(3-1)=16+2=18`.
5. `4*3*2*2=48`.
6. `24` unordered knight-move pairs.
7. `10*6/3=20` students.
8. No. Three named colours and “every three consecutive positions distinct” force a period-3 pattern. A cycle closes only when its length is divisible by 3; `8` is not.
9. Same `K6` proof as Practice 15: among five incident edges, three share a colour; their other endpoints force either a triangle in that colour or a triangle in the other colour.
10. Line-point incidences: `12*4=48`; each point contributes 3 incidences, so `16` points.
11. Outdegree only lists immediate options. Winning strategy can depend on whose turn it is, which position/resources remain, terminal conditions and any history-dependent restrictions.
12. Proper colourings of `C7` with 3 colours: `(3-1)^7-(3-1)=128-2=126`.

## Historical anchor audit

`IOQM-2025-Q08 = 48`.
- exact model is `K4` with edge `BD` removed;
- sequential legal choices are `4,3,2,2`.

`IOQM-2025-Q29 = 19`.
- conflict graph is the fourth power of the cycle;
- equal colours require cyclic separation at least 5;
- six colours cannot cover 19 vertices because each class has size at most 3;
- explicit base colourings establish all `n>=20`.

`IOQM-2024-Q09 = 48`.
- each knight edge is one diagonal pair of a `3 x 2` or `2 x 3` rectangle;
- 12 placements of each orientation, 2 edges each.

`IOQM-2024-Q19 = 12`.
- triangle avoidance forces degree 2 in each colour at every vertex;
- the red subgraph is a labelled 5-cycle; its complement is the blue 5-cycle.

`IOQM-2023-Q16 = 94`.
- nine diagonals have `392` valid red/blue colourings after excluding the two possible all-blue alternating triangles;
- requested digit-square sum is `3^2+9^2+2^2=94`.

`IOQM-2023-Q22 = 77`.
- region count 9 requires intersection contribution 4;
- `(2,2,0)` family distribution contributes 300 selections;
- `(2,1,1)` requires exactly one triple concurrency; discrete Ceva gives 13 concurrent triples, contributing `13*3*4=156`;
- total 456, digit-square sum `16+25+36=77`.

## Diagnostic map

- graph terminology used before defining the model -> ask what one vertex and one edge mean;
- unrestricted colour count used -> list adjacency restrictions before multiplying;
- divide-by-two done automatically -> demand proof that every desired object was counted exactly twice;
- cyclic problem treated as linear -> inspect wrap-around conflicts;
- degree sum odd but accepted -> use handshaking parity;
- incidence double count has two different object sets -> explicitly define the incidence pair before equating counts;
- Ramsey problem attacked by raw enumeration -> fix one vertex and force local colour degrees;
- geometric surface attacked with coordinates although only crossings matter -> move to incidence structure;
- static graph count used for an adversarial game -> add player-to-move and future-state information.
