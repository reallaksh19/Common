---
main_topic_id: IOQM-G9-COMB-02
microstream_id: W1-A
microstream_title: Graph modelling as a representation choice
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-02
prerequisite_interfaces:
  - COMB01_Stable_Counting_Model_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-A — Graph Modelling as a Representation Choice

## A. Scope boundary
Included: deciding vertices/edges, preserving adjacency/incidence, translating geometric or scheduling surfaces to graphs, and defining counted objects before graph terminology. Excluded: generic counting formulas from COMB-01, graph algorithms, advanced graph theory and game-state graphs owned by COMB-04.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can draw dots/lines and count arrangements.
LIKELY_HALF_KNOWLEDGE: starts naming graph terms before deciding what the dots mean.
MISSING_BRIDGES: model identity; which relations become edges; what information geometry contributes and what may be discarded.
OWNERSHIP_TARGET: OBJECTS -> RELATION -> GRAPH -> INVARIANT/COUNT -> CHECK AGAINST ORIGINAL.
```

## C. Mathematical invariant / governing structure
A graph is useful only if its vertices and edges preserve exactly the relation that controls legality/counting. Two different surface drawings may induce the same graph and therefore the same combinatorial problem.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| vertex-edge graph | adjacency constraints | define one vertex and one edge | pairwise relation drives problem | import distances/angles unnecessarily |
| incidence bipartite graph | object-feature incidences | choose two object classes | two-type incidence | force all objects into one vertex type |
| cycle/cycle-power graph | local cyclic constraints | translate forbidden distances | cyclic order fixed | treat as a line and forget wraparound |
| geometric drawing | source incidence | copy exact connections first | source custody intact | infer an edge from visual crossing |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| coloured polygon | vertex colouring | geometric angle chase | is only adjacency/consecutive-position legality relevant? | picture looks geometric |
| line crossings | incidence graph/count | coordinates | do metric locations matter or only crossings/concurrencies? | coordinates feel concrete |
| move grid | graph edges | path enumeration | are legal moves pairwise relations? | board invites casework |
| adversarial moves | game-state graph | static graph | does an opponent choose transitions? | both use vertices/edges |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMB02-MOD-01
WRONG_MOVE: make every visually close pair adjacent.
WHY_TEMPTING: drawing proximity is confused with stated relation.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: edge means exactly one declared relation.
FALSIFIER_OR_CONTRAST: redraw same graph with different geometry.

ERROR_CODE: COMB02-MOD-02
WRONG_MOVE: preserve metric data after it becomes irrelevant.
WHY_TEMPTING: discarding source information feels unsafe.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: verify incidence first, then retain only data affecting legal configurations.
FALSIFIER_OR_CONTRAST: K4-minus-edge colouring is independent of quadrilateral shape.
```

## G. First-move cues
- “different colours when joined” -> vertices are objects, joins are edges.
- “any five consecutive” -> cycle-power adjacency.
- “knight move” -> grid squares as vertices, legal moves as edges.
- “regions from cevians” -> model intersection/incidence before coordinates.

## H. H3 -> H0 fading plan
- H3: graph already drawn; label what vertices/edges mean.
- H2: provide objects and ask for edge rule.
- H1: give only surface statement with a repeated pairwise restriction.
- H0: changed context (students/conflicts, tasks/incompatibility) that induces a known graph structure.

## I. Validated IOQM source anchors
All six COMB-02 anchors exercise modelling. Primary examples: `IOQM-2025-Q08` (K4 minus one edge), `IOQM-2025-Q29` (cycle power), `IOQM-2024-Q09` (knight graph), `IOQM-2023-Q22` (incidence intersections). Answers are independently closed in the audit.

## J. Source-independent mathematical trace
Q08 model gives proper-colouring count 48; Q29 model converts the local five-consecutive rule to distance-at-most-4 conflict edges; Q09 makes knight-move pairs graph edges; Q22 turns geometric cevians into intersection contributions. Full source traces are in the independent audit.

## K. Contrast-pair candidates
1. graph model vs decorative diagram;
2. adjacency vs proximity;
3. cycle vs path (wraparound);
4. incidence graph vs coordinate placement;
5. static graph vs game-state graph;
6. COMB-01 counted object vs COMB-02 relational model.

## L. Transfer candidates
- T2: exam scheduling conflicts -> proper colouring.
- T2: social handshakes -> degree sum.
- T3: cyclic seating restrictions -> cycle power.
- T4: geometric intersections -> incidence graph.

## M. Candidate mastery items
Recognition: state vertices/edges for four surfaces. First-line: write the graph model, not the count. Full solve: model then count a small conflict graph. WHY-NOT: explain why a crossing in a drawing is not automatically a graph vertex. Verification: compare two surface drawings for graph isomorphism at an informal Grade-9 level.

## N. Dependency declarations
`REQUIRES`: COMB-01 counted-object definition and disjoint/exhaustive discipline.  
`BRIDGE_REQUIRES`: none.  
`APPLIES`: all COMB-02 streams.  
Downstream may assume learner defines objects and relation before graph terminology.

## O. Lead integration notes
Teach this first. Use plain language “objects and links” before formal vertex/edge names. Never reteach generic multiplication/complement here. Keep graph isomorphism terminology out of learner prose; use “same connection pattern.”

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact page-image custody pending for geometric-surface anchors
```
