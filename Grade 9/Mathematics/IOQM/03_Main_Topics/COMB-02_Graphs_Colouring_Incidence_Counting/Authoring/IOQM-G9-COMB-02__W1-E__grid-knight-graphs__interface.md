---
main_topic_id: IOQM-G9-COMB-02
microstream_id: W1-E
microstream_title: Grid and knight graphs
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-02
prerequisite_interfaces:
  - COMB01_Stable_Counting_Model_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-E — Grid and Knight Graphs

## A. Scope boundary
Included: board positions as vertices, legal displacement edges, boundary effects, rectangle-placement counting, symmetry/degree classes. Excluded: chess strategy, pathfinding algorithms and general lattice-geometry canon.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: knows knight move and rectangular grids.
LIKELY_HALF_KNOWLEDGE: counts from a central square and assumes uniformity.
MISSING_BRIDGES: move graph representation; boundary degree changes; displacement rectangles count edges efficiently.
OWNERSHIP_TARGET: LEGAL DISPLACEMENT -> PLACEMENT CLASSES -> ORDERED/UNORDERED CHECK.
```

## C. Mathematical invariant / governing structure
A knight edge corresponds uniquely to one diagonal of a `2x3` or `3x2` rectangle. Counting rectangle placements removes boundary-case clutter and counts every unordered knight pair exactly once.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| move graph | adjacency | squares as vertices | fixed board | count paths instead of edges |
| displacement vector | move types | list `(±1,±2)` | oriented count | forget duplicates/reversals |
| 2x3 rectangle | unordered edges | count placements ×2 | rectangular board | degree case explosion |
| degree classes | boundary effects | classify square types | symmetry manageable | assume regular graph |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| fixed rectangular board | rectangle placements | degree table | do moves correspond to fixed bounding boxes? | degree table is familiar |
| irregular board | degree sum | rectangle formula | are all placements present? | formula reuse |
| ordered moves | displacement count | unordered-edge count | is start/end order relevant? | knight pairs usually unordered |
| reachability | path/state search | edge count | is question about sequences rather than legal pairs? | same graph surface |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMB02-GRID-01
WRONG_MOVE: multiply centre-square degree by number of squares.
WHY_TEMPTING: board seems symmetric.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: boundary squares have smaller degree; use placement or degree classes.
FALSIFIER_OR_CONTRAST: corner vs centre on 5x5.

ERROR_CODE: COMB02-GRID-02
WRONG_MOVE: count each knight pair twice as two directions.
WHY_TEMPTING: displacement vectors are oriented.
MISSING_LINK_CLASS: EXECUTION
REPAIR_INVARIANT: requested object is unordered pair; pair opposite directions or count rectangle diagonals once.
FALSIFIER_OR_CONTRAST: one legal move A->B represents same pair as B->A.
```

## G. First-move cues
- knight pairs on rectangle -> count 2x3 and 3x2 placements.
- irregular board -> switch to degree classes.
- “ways to move from” -> ordered local degree, no automatic halving.
- “pairs of squares” -> unordered edges.

## H. H3 -> H0 fading plan
H3: mark a 2x3 rectangle and its two knight edges. H2: cue “bounding rectangle.” H1: only board size + knight pair request. H0: changed leaper move `(1,3)` or rectangular board where learner derives the bounding-box count.

## I. Validated IOQM source anchors
`IOQM-2024-Q09`, CLEAN_OFFICIAL, grid/knight graph, independently verified answer 48.

## J. Source-independent mathematical trace
On 5x5: `(5-2)(5-1)=12` placements of 3x2 and 12 of 2x3; each has two knight diagonals. Total `12*2+12*2=48`.

## K. Contrast-pair candidates
1. centre vs boundary degree;
2. displacement directions vs unordered pairs;
3. rectangle placement vs square-by-square enumeration;
4. rectangular vs irregular board;
5. legal pair vs multi-move path;
6. grid graph vs abstract graph with same degrees.

## L. Transfer candidates
T2 `(1,3)` leaper; T2 rook adjacency on a small board; T3 remove corner cells and use degree sum; T4 lattice-distance condition converted to a move graph.

## M. Candidate mastery items
Recognition: edge-count or path problem? First-line: identify bounding rectangle. Full solve: count leaper pairs on m×n. WHY-NOT: refute uniform degree. Verification: independently match placement count to degree-sum count on a 4×4 board.

## N. Dependency declarations
`REQUIRES`: W1-A modelling, W1-B handshaking.  
`BRIDGE_REQUIRES`: elementary grid arithmetic.  
`APPLIES`: Q09.  
Downstream may assume learners can choose placement vs degree representation.

## O. Lead integration notes
Use as a concrete visual bridge after handshaking. Avoid chess terminology beyond the move rule. Make ordered/unordered object definition explicit via COMB-01 retrieval.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: HBCSE page-image custody pending
```
