# Benchmark Assimilation Lab — Graphs, Colouring and Incidence Counting

Use this after the Assimilation Book and before the final mastery test. The aim is to test whether you can build the correct model, not whether you remember graph vocabulary.

Learning loop:

`RECONNECT -> DIAGNOSE -> ADOPT -> TRANSFER`

## A. RECONNECT — no notes

Write only the first useful line unless a short answer is requested.

1. In a friendship problem, what must be defined before writing a graph?
2. Why is the sum of all vertex degrees even?
3. What is the difference between unrestricted vertex colourings and proper colourings?
4. Why can a linear colouring count fail on a cycle?
5. Before dividing a directed-move count by 2, what must be proved?
6. If a geometry problem depends only on crossings and concurrencies, what representation should be tested before coordinates?
7. In a red/blue edge-colouring problem forbidding monochromatic triangles, what local structure should you inspect first?
8. What extra information does a game state need beyond the underlying move graph?

Diagnostic interpretation:

- misses 1 -> graph-modelling bridge is weak;
- misses 2 or 5 -> incidence/double-count bridge is weak;
- misses 3-4 -> colouring restriction/closure bridge is weak;
- misses 6 -> representation-selection bridge is weak;
- misses 7 -> Ramsey local-forcing bridge is weak;
- misses 8 -> static-graph vs game-state boundary is weak.

## B. Error laboratory

For each proposed solution, identify the first invalid or inefficient move and repair it.

### Error 1 — drawing before defining

Claim: “The story has six people, so draw six dots in a hexagon and connect the obvious pairs.”

Repair target: define exactly what one vertex and one edge mean before drawing.

### Error 2 — unrestricted colouring reflex

Claim: “Four vertices, three colours, so there are `3^4` colourings.”

Repair target: determine whether adjacency restrictions make the colouring proper.

### Error 3 — divide by two automatically

Claim: “I counted 40 moves, so there are 20 edges.”

Repair target: prove every desired unordered edge was counted exactly twice and no exceptional object behaves differently.

### Error 4 — linearize a cycle

Claim: “Colour the first vertex, then continue left to right; the last position has no extra condition.”

Repair target: include wrap-around adjacency from the beginning.

### Error 5 — count the wrong incidence set

Claim: “I counted point-line incidences by lines and counted crossing points by points, so the two totals are equal.”

Repair target: explicitly define one identical incidence set before double counting.

### Error 6 — brute-force Ramsey search

Claim: “There are only `2^10` colourings of the edges of `K5`, so enumerate all of them.”

Repair target: fix one vertex and force the local colour pattern first.

## C. ADOPT — first move only

Do not solve fully. Write the first two useful lines.

1. Six students exchange messages; only who communicates with whom matters.
2. A graph has degree sequence `4,4,3,3,2,2`.
3. Colour the vertices of a path of length 5 properly with 4 colours.
4. Colour the vertices of a 7-cycle properly with 3 colours.
5. Count unordered knight-move pairs on a `6 x 5` board.
6. Ten lines each contain 4 selected points; each selected point lies on exactly 2 lines.
7. Two colours are used on the edges of `K6`; prove a monochromatic triangle must occur.
8. A polygon rule says any four consecutive vertices must have distinct colours. What static conflict graph should be built?

## D. TRANSFER — changed surface

1. A tournament schedule says each team plays certain pairs of opponents exactly once. The question asks whether a claimed list of numbers of games played is possible. Translate the claim into degree language before checking it.
2. A seating rule forbids guests within cyclic distance 2 from sharing a badge colour. Replace the repeated local rule by one graph-colouring statement.
3. A board has several legal jump types. Explain two different valid edge-count routes and the exact condition under which their totals must agree.
4. A family of sets is described by which elements belong to which sets. Define an incidence set that can be counted by sets and by elements.
5. A geometric diagram contains many cevians, but all lengths and angles are irrelevant to the target region count. Explain which information the graph/incidence model must preserve and which it may discard.
6. Construct a static graph-counting problem that looks game-like but does **not** require game-state analysis, then explain the boundary.

## E. Six-question assimilation test

Choose one problem from Section D and answer all six questions before completing the count/proof.

1. **What did you notice?** State the relation pattern that matters.
2. **Why does the representation work?** Explain what information it preserves.
3. **What clue would make you think of it again?** Give a future recognition cue.
4. **What similar-looking situation needs a different method?** State one contrast pair.
5. **Can you write the first two useful lines without help?** Write them.
6. **Can you solve a disguised version?** Change the surface while preserving the same graph/incidence invariant and outline the route.

## Readiness rule

You are not ready merely because you know the words vertex, degree, colouring or Ramsey. You are ready when you can define the relation model from an unfamiliar story, choose the smallest graph/incidence view, justify every overcount correction, handle cyclic closure, reject a tempting wrong representation, and start a disguised problem without a chapter label.
