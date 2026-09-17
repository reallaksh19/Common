# 7. Graphs, matchings and colourings

A graph is just a convenient picture for pairwise relations. Use it only when it simplifies the restriction.

## 7.1 Handshakes and unordered pairs

An unordered handshake is an unordered pair. If every pair of \(n\) people is considered once, there are

\[
\binom n2
\]

pairs.

If two types of pair cover all possibilities, count the easier class and subtract from the total.

### Teacher example

If 12 people form unordered pairs of people, there are \(\binom{12}{2}\) possible pairs in total. If a particular subgroup of 5 all produce one kind of interaction and every other pair produces another kind, the second kind is

\[
\binom{12}{2}-\binom52.
\]

## 7.2 Handshake lemma

If vertex \(v\) has degree \(d(v)\), then

\[
\sum_v d(v)=2|E|.
\]

Every edge contributes 1 to the degree of each endpoint.

Before dividing by 2, check that every desired relation is counted from both ends exactly once.

## 7.3 Perfect matchings

Splitting people into unordered pairs is a perfect matching problem.

On a highly symmetric allowed-edge graph, do not list all pairings. Classify matchings by a useful feature such as the number of opposite edges or special edge types.

The key question is:

> After I choose one pair, what structure remains?

A recursive or case-based matching count often becomes very small once the graph symmetry is used.

## 7.4 Degree 2 means cycles

A finite simple graph in which every vertex has degree 2 is a disjoint union of cycles.

So a handshake problem where every person shakes hands with exactly two others becomes a problem of decomposing the labeled vertex set into possible cycle sizes.

For 9 labeled vertices, for example, cycle-size partitions must use parts at least 3:

- \(9\);
- \(6+3\);
- \(5+4\);
- \(3+3+3\).

Each structure is then counted separately, taking care not to overcount the order of cycles.

## 7.5 Proper colourings

If adjacent objects must receive different colors, model the forbidden pairs as graph edges.

For a cycle \(C_n\) with \(q\) colors,

\[
P(C_n,q)=(q-1)^n+(-1)^n(q-1).
\]

For small graphs, a direct case split may be clearer than invoking the formula.

## 7.6 Small-grid colouring by opposite cells

In a \(2\times2\) grid, opposite cells are not adjacent. Conditioning on the relationship between opposite cells can make the remaining two cells independent.

A useful split is:

- opposite cells same;
- opposite cells are a forbidden pair;
- opposite cells are different but compatible.

This is often cleaner than choosing colors cell by cell.

## 7.7 Cyclic coloring closure

A line and a cycle are different.

On a line, the last object is unrelated to the first unless stated. On a cycle, the last-first adjacency is active from the start. Do not finish a linear count and then casually “fix the ends” unless you have proved that correction.

## What should I notice?

- handshakes → unordered pairs or edges;
- every vertex same degree → use degree sum, then inspect structure;
- degree 2 everywhere → cycles;
- pair everyone → matching;
- adjacent colors must differ → graph coloring;
- cycle → remember the last-first edge from the beginning;
- tiny grid → consider conditioning on nonadjacent/opposite cells.

## Common mistakes

- treating directed neighbour counts as unordered edges without checking double counting;
- forgetting the wrap-around edge of a cycle;
- using graph vocabulary without simplifying the count;
- counting all matchings when the allowed graph has symmetry that should be exploited;
- forgetting that cycles themselves are unordered components in a cycle-decomposition count;
- using the cycle-coloring formula with the wrong value of \(q\) or \(n\).

## Appendix A practice

Questions **Q2, Q8, Q33, Q34, Q49**.
