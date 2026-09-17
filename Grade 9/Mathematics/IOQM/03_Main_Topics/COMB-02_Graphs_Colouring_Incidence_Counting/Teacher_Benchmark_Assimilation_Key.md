# Teacher Key — COMB-02 Benchmark Assimilation Lab

This key supports `07_Benchmark_Assimilation_Lab.md`. It is separate from the main Teacher Diagnostic Key so the benchmark-specific diagnostic can be checked independently.

## A. RECONNECT

1. Define the model: what one vertex represents and exactly when two vertices are joined by an edge.
2. Every edge contributes 1 to the degree of each of its two endpoints, so `sum degrees = 2|E|`, which is even.
3. Unrestricted colouring permits any colour at any vertex. Proper colouring requires every adjacent pair to receive different colours.
4. A cycle has wrap-around adjacency: the final positions can be adjacent to the initial positions, so a linear count can violate the closure condition.
5. Prove that every desired unordered pair occurs exactly twice in the directed count, once from each endpoint, and that no loops/exceptional objects have a different multiplicity.
6. Test an incidence/intersection graph: retain which cevians cross or concur and discard irrelevant metric data.
7. Fix one vertex and inspect the colours of its incident edges; pigeonhole/local forcing often determines the next structure.
8. At minimum record whose turn it is and the current legal configuration/resources. Add history when it changes future legal moves or terminal conditions.

## B. Error laboratory

### Error 1
A geometric drawing is not the model. First write, for example, `vertex = one person` and `edge = one communicating pair`; only then choose a drawing convenient for reasoning.

### Error 2
`3^4` counts unrestricted assignments. If adjacency matters, list the graph restrictions first and count only legal colour choices.

### Error 3
A total of 40 directed moves implies 20 edges only if each desired unordered edge is counted exactly twice. Verify that condition before halving.

### Error 4
For a cycle, include the edge/conflict between the last and first positions from the start. A path count cannot simply ignore closure.

### Error 5
Double counting requires one identical set. Define, for example, `I={(line,point): selected point lies on selected line}` and count `I` by lines and then by points.

### Error 6
For a two-colouring of `K5` or `K6`, raw enumeration hides the invariant. Fix one vertex; pigeonhole forces several incident edges of one colour, and the edges among their other endpoints force a monochromatic triangle or the complementary structure.

## C. ADOPT

1. First lines: `vertex = one student`; `edge = one unordered communicating pair`.
2. `sum degrees = 4+4+3+3+2+2 = 18`; therefore `2|E|=18`, so `|E|=9`.
3. A path of length 5 has 6 vertices. First vertex: 4 choices; each subsequent vertex: 3 choices, so the count begins `4*3^5`.
4. Model `C7`. A standard cycle-colouring route with `q=3` gives `(q-1)^7-(q-1)=2^7-2=126`; alternatively carry a path colouring with an explicit closure check.
5. Count knight edges by rectangle placements or degrees. For an `m x n` board, `2(m-1)(n-2)+2(m-2)(n-1)`. With `m=6,n=5`: `2*5*3+2*4*4=62` unordered knight edges.
6. Count incidences. By lines: `10*4=40`. Each selected point lies on two lines, so `2P=40`, giving `P=20`.
7. Fix a vertex of `K6`. Of its five incident edges, at least three have one colour, say red, to `A,B,C`. If any of `AB,BC,CA` is red, it forms a red triangle with the fixed vertex; if none is red, all three are blue and `ABC` is a blue triangle.
8. Build the cycle conflict graph in which two polygon vertices are adjacent exactly when their cyclic distance is at most 3. The colouring rule becomes ordinary proper colouring of this graph.

## D. TRANSFER

1. Translate “number of games played by each team” into vertex degrees. Before constructing a schedule, check handshaking parity and degree bounds such as `0<=d(v)<=n-1` in a simple schedule graph.
2. Create a graph on the cyclic seats and connect two seats when cyclic distance is at most 2. Then badge assignments are proper colourings of that conflict graph.
3. Route A: count legal jumps by displacement/rectangle classes. Route B: sum local degrees and divide by 2. They must agree only when both count the same unordered legal-jump edge set and the degree sum counts each edge exactly twice.
4. Define `I={(S,x): element x belongs to selected set S}`. Count `|I|` by summing set sizes and again by summing, over elements, the number of sets containing each element.
5. Preserve which cevians meet, the multiplicity of each concurrence, endpoint/family information needed to determine allowable crossings, and boundary incidence. Discard exact lengths/angles when they cannot change that incidence pattern.
6. Example: “How many legal moves are available from each square of a fixed board?” can be a static move-graph degree-count problem even though the word *move* appears. It becomes a game-state problem only when players make adversarial sequential choices and future legality/winning depends on the evolving state.

## E. Six-question assimilation test — diagnostic rubric

A strong response should contain all six components:

1. a specific relation clue rather than the chapter name;
2. an explanation of what the proposed graph/incidence representation preserves;
3. a reusable future recognition cue;
4. a genuine near-neighbour requiring a different route;
5. two mathematically productive opening lines;
6. a changed-surface example with the same invariant and a valid route.

Diagnostic tags:

- `recognition`: relation pattern not identified;
- `modelling`: vertex/edge/incidence meanings are ambiguous or wrong;
- `representation`: a more complex or lossy representation chosen;
- `counting`: multiplication/addition/complement applied to the wrong object set;
- `double_count`: halving/equating counts without multiplicity proof;
- `cyclic_closure`: wrap-around restriction omitted;
- `forcing`: Ramsey/local inevitability replaced by unstructured enumeration;
- `boundary`: static graph confused with adversarial game state;
- `transfer`: surface and mathematical invariant both changed.

## Independent QA disposition

All deterministic counts and route claims above were recomputed after the learner lab was authored. No answer was copied from the learner-facing text.

`BENCHMARK_LAB_KEY_STATIC_CHECK = PASS`.
