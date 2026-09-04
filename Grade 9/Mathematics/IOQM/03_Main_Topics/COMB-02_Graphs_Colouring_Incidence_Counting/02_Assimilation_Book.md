# Graphs, Colouring and Incidence Counting: Model the Relation First

A graph is not mainly a picture of dots and lines. It is a way to keep exactly the relationships that matter and throw away the rest.

The central habit is:

> **Before using graph vocabulary, decide what one vertex means and what one edge means.**

A useful working loop is:

`DEFINE OBJECTS -> MODEL RELATIONS -> CHOOSE DEGREE / COLOUR / INCIDENCE VIEW -> COUNT OR FORCE -> CHECK DOUBLE COUNT`

## 1. When a graph is the right representation

Suppose a problem is about five people and which pairs know each other. Their heights, seating positions, and names may be irrelevant. If only pairwise acquaintance matters, represent:

- one person by one **vertex**;
- one acquaintance relation by one **edge**.

Now the surface story has become a relation structure.

A graph is useful only if the model preserves every condition needed for the question.

## 2. Vertices, edges and adjacency

Two vertices are **adjacent** when an edge joins them.

The **degree** of a vertex is the number of edges incident with it.

If a vertex has degree 4, it is related to four other vertices under the chosen model.

Do not count degree from the visual length or direction of an edge. Only incidence matters.

## 3. The handshaking identity

Every edge has two endpoints. Therefore, when we add all vertex degrees, each edge is counted twice:

`sum of all degrees = 2 x number of edges`.

This is the handshaking identity.

### Example

A graph has degrees

`3,3,2,2,2,2`.

Their sum is 14, so the graph has

`14/2=7`

edges.

The factor 2 is not a formula to memorize blindly. It comes from counting each edge once at each endpoint.

## 4. Direct edge count or degree sum?

Use direct enumeration when edges fall naturally into a few disjoint types.

Use degree sum when local degrees are easier to compute than the global edge set.

Ask:

> **Is it easier to count relations themselves, or count how many relations touch each object?**

## 5. Proper colouring is not unrestricted colouring

In a vertex-colouring problem, colours are assigned to vertices.

A **proper colouring** requires adjacent vertices to have different colours.

If a graph has 4 vertices and 4 available colours, there are `4^4` unrestricted assignments. A proper colouring is a smaller set because adjacency forbids some assignments.

The first step is not “use a colouring formula.” It is:

1. identify the graph;
2. identify adjacency;
3. count colour choices under those restrictions.

## 6. Sequential colouring: restrictions change after each choice

Consider a triangle with 4 colours.

- first vertex: 4 choices;
- second adjacent vertex: 3 choices;
- third vertex adjacent to both: 2 choices.

So there are

`4*3*2=24`

proper colourings.

This uses the ordinary multiplication principle already learned in counting. The new content is the graph restriction that determines the number of legal choices at each stage.

## 7. A missing edge changes the colouring count

Suppose four vertices form a quadrilateral and one diagonal is present. This is `K4` with one edge missing.

The two non-adjacent vertices are allowed to share a colour. That single missing relation matters.

In `IOQM-2025-Q08`, modelling the picture this way turns the problem into a short proper-colouring count. The answer is `48`.

The lesson is:

> **Colour the graph you actually have, not the complete graph your eye imagines.**

## 8. Cyclic colouring: the end must meet the beginning

A line of positions and a cycle of positions can have the same local-looking rule but different global constraints.

For a cyclic arrangement, positions near the end may also be close to positions near the beginning.

If every set of five consecutive vertices must have different colours, then vertices within cyclic distance 4 must receive different colours. This is naturally a graph-colouring condition.

The wrap-around condition is part of the problem, not a final correction.

## 9. Grid and knight graphs

A board problem can become a graph:

- each square is a vertex;
- two squares are adjacent if a legal knight move connects them.

Then “how many pairs of squares are connected by a knight move?” becomes “how many edges are in the knight graph?”

You may count directed moves from each starting square and divide by 2, but only because every unordered legal pair is counted once from each endpoint.

In `IOQM-2024-Q09`, this degree/incidence viewpoint gives `48` unordered knight-move pairs on the `5 x 5` board.

## 10. Ordered moves vs unordered pairs

If you count

`A -> B`

and

`B -> A`

as two directed moves, then an undirected edge `{A,B}` has been counted twice.

But you must not divide by 2 automatically. Ask:

> **Does every final object appear exactly twice in my count?**

This is the same counting discipline as before, now expressed through graph incidence.

## 11. Incidence double counting

An **incidence** is a relation such as:

- vertex lies on an edge;
- point lies on a line;
- chosen cevian passes through an intersection;
- region boundary contains an edge.

Double counting means counting the same set of incidences in two different ways.

The most important first step is to name the incidence object clearly.

### Example

If a graph has `E` edges, then the set

`{(vertex, edge): vertex is an endpoint of edge}`

has size `2E` when counted by edges, and `sum degrees` when counted by vertices. This is exactly the handshaking identity.

## 12. Geometry can hide an incidence problem

A problem may mention points on triangle sides, cevians and regions. The geometry may be only the surface.

If the question depends on which cevians cross, concur, or create new regions, an incidence representation may be cheaper than coordinates.

In `IOQM-2023-Q22`, the requirement of exactly nine regions can be translated into the required intersection pattern. Once that pattern is understood, the remaining task is a count of valid peg selections. The answer is `77`.

The lesson is:

> **When the exact lengths and angles do not matter, ask whether only the intersection pattern matters.**

## 13. Edge colouring and monochromatic triangles

Sometimes colours belong to edges rather than vertices.

A triangle is **monochromatic** when all three of its edges have the same colour.

A raw search over all edge colourings is usually expensive. Instead, fix one vertex and look at the colours of the edges incident with it.

If many incident edges share one colour, the edges among their other endpoints are forced to avoid that colour if monochromatic triangles are forbidden.

This is a local-to-global forcing argument.

## 14. A Ramsey-style inevitability habit

Ramsey-style reasoning does not mean memorizing large Ramsey numbers. At this level, it means:

1. fix a small local structure;
2. use pigeonhole or degree information to force a repeated type;
3. examine the relations among the forced neighbours;
4. derive either the required configuration or a contradiction.

In `IOQM-2024-Q19`, forbidding monochromatic triangles in a red/blue colouring of the edges of `K5` forces a very rigid cycle-like pattern. The answer is `12`.

The lesson is:

> **Do not enumerate every colouring when local avoidance rules force the rest.**

## 15. Forbidden subgraphs

A colouring condition can often be restated as “a certain small graph must not appear in one colour.”

For example, “every triangle has at least one red edge” means the blue-edge graph contains no triangle.

In `IOQM-2023-Q16`, the sides of the hexagon are already red, and the diagonal colours must avoid creating an all-blue triangle. The graph language makes the forbidden configuration explicit. The answer is `94`.

## 16. Cyclic local restrictions as graph powers

Suppose vertices of a regular polygon are coloured and any five consecutive vertices must all have different colours.

Two vertices are forbidden to share a colour whenever their cyclic distance is at most 4.

Instead of repeatedly speaking about overlapping blocks of five, build a graph in which those forbidden pairs are adjacent. Then the problem is an ordinary proper-colouring question on that graph.

This is the key representation in `IOQM-2025-Q29`, whose answer is `19`.

The lesson is:

> **A repeated local restriction can become one static adjacency rule.**

## 17. Graph state vs game state

A graph can represent legal moves in a game, but a static graph-colouring/counting question is not automatically a game-strategy problem.

If players make choices adversarially and future options depend on the history, the central object is a game state and winning/losing strategy. That belongs to a different route.

If the task only asks which assignments or relations are valid in a fixed graph, stay in graph counting/colouring.

## 18. Historical pattern: knight moves

`IOQM-2024-Q09` rewards a degree/incidence count rather than listing every pair individually.

The lesson is:

> **When local move counts are easy, sum local degrees and correct the double count.**

## 19. Historical pattern: proper colouring

`IOQM-2025-Q08` looks like a small colouring exercise, but the important step is identifying the exact adjacency graph before multiplying choices.

The lesson is:

> **Restrictions come from edges, not from the number of colours alone.**

## 20. A compact router

When a relation/counting problem appears, ask:

1. What should one vertex represent?
2. What exactly should an edge represent?
3. Does the graph preserve every relevant condition?
4. Is the target an edge count, degree count, colouring, or incidence count?
5. If colouring, is it proper and is the arrangement cyclic?
6. If counting moves, am I counting directed moves or unordered pairs?
7. Can the same incidence set be counted in two ways?
8. Is a forbidden local configuration forcing a global pattern?
9. Is this actually an adversarial game rather than a static graph problem?

Build the right representation first. The counting becomes shorter afterward.
