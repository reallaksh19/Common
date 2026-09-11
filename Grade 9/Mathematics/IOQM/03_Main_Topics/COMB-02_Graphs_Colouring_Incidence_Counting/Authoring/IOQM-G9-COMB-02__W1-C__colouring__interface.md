---
main_topic_id: IOQM-G9-COMB-02
microstream_id: W1-C
microstream_title: Proper colouring and local cyclic constraints
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-02
prerequisite_interfaces:
  - COMB01_Stable_Counting_Model_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-C — Proper Colouring and Local Cyclic Constraints

## A. Scope boundary
Included: proper vertex colouring, sequential colouring under adjacency, cyclic distance constraints, cycle-power modelling, and colour-class capacity arguments. Excluded: chromatic-polynomial theory, general graph-colouring algorithms and unrestricted assignment counting as a separate chapter.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can assign colours to objects.
LIKELY_HALF_KNOWLEDGE: multiplies available colours independently and misses adjacency/wraparound constraints.
MISSING_BRIDGES: proper colouring is a relational restriction; choose an order that exposes conditional choices; cyclic closure matters.
OWNERSHIP_TARGET: GRAPH -> ADJACENCY -> COLOUR ORDER/PATTERN -> CLOSURE CHECK.
```

## C. Mathematical invariant / governing structure
A proper colouring assigns different colours to adjacent vertices. For a cyclic “any five consecutive distinct” rule, equal colours must be cyclically separated by at least five positions, so each colour class has size at most `floor(n/5)`.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| adjacency graph | forbidden equalities | choose a high-constraint order | graph fixed | multiply `k^n` |
| cycle word | periodic/local rule | track cyclic gaps | wraparound enforced | solve linear word only |
| colour-class capacity | impossibility | bound class size | separation known | construct before checking capacity |
| explicit periodic pattern | existence | give base pattern then extend | join remains legal | assume periodicity without closure check |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| small fixed graph | sequential colouring | global inclusion-exclusion | can vertices be ordered with simple remaining choices? | IE seems general |
| large cyclic local rule | gap/capacity + pattern | sequential casework | is there translation symmetry? | local choices seem manageable |
| polygon drawing | graph route | geometry | do angles/lengths affect colouring? | visual surface |
| path rule | linear pattern | cyclic pattern | must first/last vertices also interact? | same local wording |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMB02-COL-01
WRONG_MOVE: count all colour assignments as proper.
WHY_TEMPTING: colour choices look independent.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: every edge imposes an inequality constraint.
FALSIFIER_OR_CONTRAST: one edge with two colours has 2, not 4, proper assignments.

ERROR_CODE: COMB02-COL-02
WRONG_MOVE: build a valid linear pattern that fails at cyclic wraparound.
WHY_TEMPTING: learner checks only consecutive positions as written on a line.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: cycle has no endpoint; check gaps across the join.
FALSIFIER_OR_CONTRAST: compare C_n with P_n.
```

## G. First-move cues
- “joined vertices different” -> proper-colouring graph.
- “any five consecutive” -> equal colours need cyclic gap at least 5.
- “at most six colours” -> test colour-class capacity before constructing.
- small graph with one missing edge -> colour highly constrained vertices first.

## H. H3 -> H0 fading plan
H3: give vertex order and available-colour counts. H2: cue “colour A,C before B,D.” H1: show graph only. H0: cyclic local-colour rule where learner must choose capacity proof or construction.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q08 | 2025/Q08 | CLEAN_OFFICIAL | primary | proper colouring K4 minus edge | geometric surface | 48 independently verified |
| IOQM-2025-Q29 | 2025/Q29 | CLEAN_OFFICIAL | primary | cycle-power/local colouring | no essential figure | 19 independently verified |

## J. Source-independent mathematical trace
Q08: `4*3*2*2=48`. Q29: for `n=19`, six colour classes each have size at most 3, so cover at most 18; impossible. Explicit valid cyclic patterns exist for 20–24 and appending a five-colour block preserves legality, so every `n>=20` works; answer 19.

## K. Contrast-pair candidates
1. unrestricted assignment vs proper colouring;
2. path vs cycle;
3. construction vs impossibility bound;
4. sequential colouring vs symmetry pattern;
5. colour count vs colour-class capacity;
6. vertex colouring vs edge colouring/Ramsey W1-F.

## L. Transfer candidates
T2 timetable conflicts; T2 necklace local-separation rule; T3 minimum-colour/capacity question; T4 coding/string constraint represented as a graph.

## M. Candidate mastery items
Recognition: proper or unrestricted? First-line: choose colouring order. Full solve: small graph colouring. WHY-NOT: identify wraparound failure. Verification: test an explicit cyclic word for all forbidden distances.

## N. Dependency declarations
`REQUIRES`: W1-A modelling; COMB-01 conditional multiplication.  
`BRIDGE_REQUIRES`: W1-B degree only where useful.  
`APPLIES`: Q08/Q29.  
Downstream may assume proper colouring means adjacency-driven conditional choices and cyclic closure is checked explicitly.

## O. Lead integration notes
Introduce colouring through constraints, not terminology. Q08 is an early supported anchor; Q29 belongs late/transfer because it combines impossibility and construction.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact HBCSE page-image custody pending
```
