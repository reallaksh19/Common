---
main_topic_id: IOQM-G9-COMB-02
microstream_id: W1-B
microstream_title: Degree counting and handshaking
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-02
prerequisite_interfaces:
  - COMB01_Stable_Counting_Model_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-B — Degree Counting and Handshaking

## A. Scope boundary
Included: degree as local incidence count, `sum degrees = 2|E|`, directed-to-undirected halving, local degree classes and grid/knight applications. Excluded: general double-counting canon beyond graph/incidence use and advanced degree-sequence theorems.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can count neighbours one object at a time.
LIKELY_HALF_KNOWLEDGE: double-counts pairs or divides by two without naming what was counted twice.
MISSING_BRIDGES: each edge contributes one incidence at each endpoint; local degree sum is a global edge count.
OWNERSHIP_TARGET: LOCAL INCIDENCES -> SUM -> IDENTIFY MULTIPLICITY -> GLOBAL COUNT.
```

## C. Mathematical invariant / governing structure
Every undirected edge has exactly two endpoints, so summing vertex degrees counts every edge exactly twice: `Σ_v deg(v)=2|E|`. This is a specialized incidence double count and must be tied to the defined graph model.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| degree table | local variation | group symmetric vertex types | graph model fixed | enumerate edges individually |
| directed moves | easy local count | count outgoing legal moves | reversal corresponds to same unordered edge | forget to halve |
| rectangle placements | structural edge families | count placements × diagonals/moves | each edge unique to family | sum overlapping families |
| incidence pairs `(v,e)` | proof of handshaking | count by vertices and edges | undirected simple incidence | treat loops identically without note |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| board-move pairs | degree sum | list unordered pairs | are local moves easier? | pair list seems direct |
| regular graph | `n*d/2` | vertex-by-vertex | is degree constant? | formula memorization |
| directed transition | do not automatically halve | handshaking | is reverse move the same object? | “edges divide by two” reflex |
| incidence with two object classes | bipartite double count | degree sum on one class only | what does each incidence join? | graph vocabulary hides two classes |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMB02-DEG-01
WRONG_MOVE: divide by two after counting objects that were not double-counted.
WHY_TEMPTING: handshaking rule is memorized as a final operation.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: name the counted incidence and prove its multiplicity.
FALSIFIER_OR_CONTRAST: directed arcs need not pair.

ERROR_CODE: COMB02-DEG-02
WRONG_MOVE: assume all grid vertices have same degree.
WHY_TEMPTING: board symmetry is overgeneralized to boundary points.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: partition corners/edges/interior or use displacement placements.
FALSIFIER_OR_CONTRAST: knight degree at corner vs centre.
```

## G. First-move cues
- “pairs connected by a legal move” -> count incidences or displacement placements.
- local neighbour counts repeated by symmetry -> make a degree class table.
- every edge has two endpoints -> write `Σdeg=2E` only after model is stated.
- ordered moves asked -> do not halve unless the requested object is unordered.

## H. H3 -> H0 fading plan
H3: fill a degree table then sum. H2: cue “count directed moves first.” H1: only present a board and move rule. H0: changed-surface network with boundary/interior degree classes.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q09 | 2024/Q09 | CLEAN_OFFICIAL | primary | knight graph / unordered edge count | board surface | answer 48 independently verified |

## J. Source-independent mathematical trace
On a 5x5 board, each knight edge is a diagonal of a 3x2 or 2x3 rectangle. There are `3*4=12` placements of each orientation and 2 knight diagonals per placement, so `24+24=48` unordered pairs. Equivalent directed-degree sum gives the same result.

## K. Contrast-pair candidates
1. local degree vs global edges;
2. directed moves vs unordered pairs;
3. regular interior vs boundary degree;
4. handshaking proof vs divide-by-two ritual;
5. edge enumeration vs displacement classes;
6. degree sum vs general incidence count W1-D.

## L. Transfer candidates
T2 friendship network handshake count; T2 rook/king move graph; T3 graph with two degree classes; T4 divisibility/parity conclusion from degree sum.

## M. Candidate mastery items
Recognition: when should a local count be halved? First-line: define degree for a move graph. Full solve: count edges on a small grid graph. WHY-NOT: diagnose a mistaken uniform-degree assumption. Verification: check a degree table against an independently counted edge list.

## N. Dependency declarations
`REQUIRES`: W1-A graph model; COMB-01 multiplicity/count-object discipline.  
`BRIDGE_REQUIRES`: elementary arithmetic.  
`APPLIES`: W1-E grid/knight graphs and Ramsey degree arguments.  
Downstream may assume handshaking is understood as a double count, not a formula only.

## O. Lead integration notes
Introduce degree immediately after graph modelling with tiny examples. Delay notation-heavy degree sequences. Use Q09 to bridge local move counting to global edge count.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: source page-image custody pending
```
