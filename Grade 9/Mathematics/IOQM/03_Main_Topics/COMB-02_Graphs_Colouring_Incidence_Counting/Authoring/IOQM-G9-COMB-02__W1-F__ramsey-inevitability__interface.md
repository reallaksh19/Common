---
main_topic_id: IOQM-G9-COMB-02
microstream_id: W1-F
microstream_title: Ramsey-style inevitability and forbidden subgraphs
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-02
prerequisite_interfaces:
  - COMB01_Stable_Counting_Model_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-F — Ramsey-Style Inevitability and Forbidden Subgraphs

## A. Scope boundary
Included: two-colour edge constraints, monochromatic-triangle avoidance, local degree forcing, complement colour structure, and small forbidden-subgraph counting. Excluded: general Ramsey numbers, probabilistic method and advanced extremal graph theory.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: understands red/blue choices and triangles.
LIKELY_HALF_KNOWLEDGE: tries all 2^E colourings or treats edges independently.
MISSING_BRIDGES: local pigeonhole forces structure; avoiding one colour forces the other; complement graph can close the argument.
OWNERSHIP_TARGET: FIX A VERTEX -> FORCE LOCAL COLOUR COUNTS -> PROPAGATE AVOIDANCE -> IDENTIFY GLOBAL STRUCTURE.
```

## C. Mathematical invariant / governing structure
In a red/blue colouring of `K5` with no monochromatic triangle, no vertex can have three incident edges of one colour: three same-colour neighbours would force their mutual edges to the other colour and create a monochromatic triangle. Thus every vertex has red degree 2 and blue degree 2; each colour class is a 5-cycle.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| incident-edge colour multiset | pigeonhole forcing | fix one vertex | complete graph | enumerate all edges |
| colour subgraph | degree structure | inspect red degrees | two-colour complete graph | mix colours in one degree count |
| complement graph | opposite colour automatically | derive complement after one colour fixed | every edge has exactly one colour | recolour independently |
| forbidden triangle family | inclusion of bad events | identify only possible all-blue triangles | small structured surface | generic IE over all triangles |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| K5 no mono triangle | local forcing -> 5-cycle | brute force | does one vertex already force degree pattern? | only 10 edges seems enumerable |
| hexagon with boundary edges fixed red | count forbidden all-blue diagonal triangles | K5 Ramsey route | is graph complete under free edges? | both mention mono triangles |
| existence question | inevitability contradiction | count all valid colourings | is only existence/impossibility asked? | counting is concrete |
| fixed red subgraph | complement/free-edge model | recolour all edges | which edges are actually choices? | visual diagram obscures fixed edges |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMB02-RAM-01
WRONG_MOVE: assume edge colours are independent under triangle avoidance.
WHY_TEMPTING: each edge initially has two options.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: a local same-colour fan forces opposite-colour edges among neighbours.
FALSIFIER_OR_CONTRAST: three red edges from one K5 vertex cannot coexist without consequence.

ERROR_CODE: COMB02-RAM-02
WRONG_MOVE: apply the K5 degree argument to the 2023 hexagon without accounting for fixed red sides.
WHY_TEMPTING: both surfaces ask about monochromatic triangles.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: first identify the graph of free edges and which triangles can be all-blue.
FALSIFIER_OR_CONTRAST: any triangle containing a boundary side is automatically not all-blue.
```

## G. First-move cues
- complete graph + two colours + triangle avoidance -> fix a vertex and apply pigeonhole to incident edges.
- many edges already fixed one colour -> identify which all-free-edge triangles remain possible.
- no monochromatic triangle -> translate to forbidden triangle in each colour subgraph.
- once one colour subgraph is known -> use complement for the other.

## H. H3 -> H0 fading plan
H3: give one vertex with four incident edges and ask why 3-1 split fails. H2: cue “fix one vertex.” H1: show only K5 colouring condition. H0: changed small complete graph/partially fixed graph where learner decides between forcing and bad-subgraph counting.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q19 | 2024/Q19 | CLEAN_OFFICIAL | primary | K5 two-colouring/no mono triangle | no essential figure | 12 independently verified |
| IOQM-2023-Q16 | 2023/Q16 | CLEAN_VALIDATED | primary | fixed red hexagon sides; diagonal triangle avoidance | geometric surface | 94 independently verified |

## J. Source-independent mathematical trace
Q19: every vertex must have exactly two red and two blue incident edges; red graph is a labelled 5-cycle, counted by `(5-1)!/2=12`; complement is valid blue cycle. Q16: only the alternating triples `{1,3,5}` and `{2,4,6}` can have three diagonal edges. Their edge sets are disjoint, so valid diagonal colourings `2^9-2*2^6+2^3=392`; digit-square sum 94.

## K. Contrast-pair candidates
1. brute force vs local forcing;
2. complete graph vs partially fixed graph;
3. vertex colouring vs edge colouring;
4. forbidden-subgraph count vs Ramsey contradiction;
5. one colour graph vs its complement;
6. graph state vs adversarial game (COMB-04 boundary).

## L. Transfer candidates
T2 friendship/enmity K5 story; T2 partially fixed triangle colours; T3 count colourings avoiding one forbidden subgraph; T4 pigeonhole reasoning feeding graph structure.

## M. Candidate mastery items
Recognition: forcing or counting? First-line: fix a vertex and state the 3-edge contradiction. Full solve: K5 no-mono-triangle count. WHY-NOT: explain why 2^10 is not final. Verification: identify all possible all-blue triangles in a partially fixed polygon graph.

## N. Dependency declarations
`REQUIRES`: W1-A modelling; COMB-01 pigeonhole only as an elementary bridge where needed, not COMB-05 canon.  
`BRIDGE_REQUIRES`: W1-B degree language.  
`APPLIES`: Q19/Q16.  
Downstream may assume learner seeks forced local structure before brute-force edge colouring.

## O. Lead integration notes
Teach “inevitability” in plain language before naming Ramsey. Keep general Ramsey numbers out. Contrast Q19 forcing with Q16 forbidden-triangle counting to prevent overgeneralizing one method.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact source page-image custody pending for publication
```
