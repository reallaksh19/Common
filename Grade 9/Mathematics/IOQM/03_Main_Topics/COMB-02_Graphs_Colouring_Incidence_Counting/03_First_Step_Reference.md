# First-Step Reference: Graphs, Colouring and Incidence Counting

Use the smallest representation that preserves the restriction. Do not introduce graph terminology unless it simplifies the problem.

| You see | First question | First mathematical line |
|---|---|---|
| objects with pairwise relations | what should a vertex and edge mean? | write `vertices = ...`, `edges = ...` |
| graph degrees | are local degrees easier than listing edges? | write `sum degrees = 2|E|` |
| coloured vertices | are adjacent vertices required to differ? | write the adjacency restriction before counting choices |
| a nearly complete small graph | which edges are missing? | identify the exact non-adjacent pairs |
| positions around a polygon/cycle | does the restriction wrap around? | translate cyclic distance into adjacency |
| legal moves on a board | am I counting directed moves or unordered pairs? | define the move graph and what one edge means |
| directed move total used for unordered pairs | is every edge counted from both ends exactly once? | divide by 2 only after verifying the two-count |
| regions/intersections/cevians | do exact lengths matter, or only who meets whom? | define one incidence/intersection object |
| same incidence set can be counted locally and globally | what are the two viewpoints? | write both counts for the same set before equating |
| red/blue edge colouring with forbidden monochromatic triangle | what happens at one fixed vertex? | group incident edges by colour |
| every small local block must use distinct colours | can forbidden pairs be made edges of one graph? | build the static conflict graph |
| players choose moves adversarially | is this really a fixed colouring/count? | route to game-state analysis instead of static graph counting |

## Fast route choices

### Direct enumeration vs degree sum
Use **direct enumeration** when edges split naturally into a few disjoint types.

Use **degree sum** when the number of legal neighbours of each vertex or vertex class is easy to compute.

### Unrestricted assignments vs proper colouring
Start with unrestricted assignments only as a comparison. The actual count must respect every adjacency restriction.

### Linear vs cyclic colouring
On a line, the last position may be unrelated to the first.

On a cycle, wrap-around constraints are active from the start. Do not “fix the ends” after finishing a linear count unless you have proved that correction is valid.

### Static graph vs game state
A fixed graph records allowed/forbidden relations.

A game state records whose turn it is, what moves remain, and how choices affect the future. If adversarial strategy matters, a static graph count is not enough.

## The three checks before dividing by 2

Before halving a count, confirm:

1. every desired unordered object appears in the directed/incidence count;
2. every desired object appears exactly twice;
3. no loop or exceptional object is counted a different number of times.

## The three checks before a colouring product

Before multiplying available colour choices, confirm:

1. the graph and adjacency are correct;
2. each stage count reflects all colours already forbidden by coloured neighbours;
3. cyclic closure or other global restrictions have not been postponed incorrectly.

## Stop rule

Stop once the requested count or forced structure is determined and the counted object has been checked for overcount/undercount. More graph vocabulary is not more proof.
