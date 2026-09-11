---
main_topic_id: IOQM-G9-COMB-02
microstream_id: W1-D
microstream_title: Incidence and intersection double counting
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-02
prerequisite_interfaces:
  - COMB01_Stable_Counting_Model_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-D — Incidence and Intersection Double Counting

## A. Scope boundary
Included: count incidences two ways, region increment from segment intersections, concurrence corrections, and translating geometry surfaces into combinatorial intersection data. Excluded: full planar graph Euler theory, projective geometry, and generic inclusion-exclusion teaching.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can count crossings in a picture.
LIKELY_HALF_KNOWLEDGE: assumes every pair intersects separately and confuses pair intersections with distinct intersection points.
MISSING_BRIDGES: incidence multiplicity; concurrency changes region increment; geometry supplies legal intersection structure.
OWNERSHIP_TARGET: DEFINE INCIDENCE -> COUNT PAIRS -> CORRECT CONCURRENCY -> GLOBAL REGION/OBJECT COUNT.
```

## C. Mathematical invariant / governing structure
When a new segment crosses `k` distinct prior segments at distinct points, it is cut into `k+1` pieces and adds `k+1` regions. More generally, for an arrangement of `m` cevians with interior concurrence points where `r_p` segments meet, `R=1+m+Σ_p(r_p-1)`, provided source incidence/endpoint conditions match the model.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| cross-family pair count | potential intersections | count pairs of segment families | same-family cevians meet only at vertex | count all C(m,2) |
| concurrence point data | multiplicity correction | replace pair crossings by `r-1` contribution | exact concurrency proved | count r choose 2 as regions |
| Ceva ratio model | triple concurrence | encode side positions as ratios | triangle/cevians | use coordinates unnecessarily |
| region increment | global region count | add segments one at a time | no overlap segments | assume every new line adds same number |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| many crossings | incidence multiplicity | coordinate intersections | are exact coordinates needed or only concurrence? | coordinates seem rigorous |
| pairwise intersections | pair count | distinct-point count | can 3+ segments concur? | pairs are easy to count |
| triangle cevians | Ceva for concurrence | generic graph | does ratio position control triple meeting? | graph abstraction may erase geometry constraint |
| regions | incremental formula | Euler formula | is elementary segment insertion sufficient? | Euler is famous but overkill |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMB02-INC-01
WRONG_MOVE: count three concurrent segments as three distinct interior intersections.
WHY_TEMPTING: three segment pairs exist.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: region contribution depends on distinct point with multiplicity r via r-1.
FALSIFIER_OR_CONTRAST: three lines through one point create 6 regions, not the generic 7.

ERROR_CODE: COMB02-INC-02
WRONG_MOVE: assume two cevians from the same vertex make an interior crossing.
WHY_TEMPTING: every segment pair is treated uniformly.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: source endpoints matter; same-family cevians meet at the common vertex only.
FALSIFIER_OR_CONTRAST: draw two rays from one triangle vertex to opposite side.
```

## G. First-move cues
- “regions formed by segments” -> ask how many distinct new intersections each segment creates.
- three cevian families -> count cross-family pairs, then inspect concurrence.
- exact nine-region target -> translate target into required intersection contribution.
- side pegs in equal subdivisions -> encode ratios; test Ceva for triple concurrency.

## H. H3 -> H0 fading plan
H3: supply segment-family counts and ask for cross pairs. H2: cue “pair intersections vs concurrent point.” H1: show only region target. H0: different polygon/line arrangement where learner builds the incidence model independently.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2023-Q22 | 2023/Q22 | CLEAN_VALIDATED | primary | cevians, concurrency, regions | geometric surface | 77 independently verified |

## J. Source-independent mathematical trace
For four cevians, nine regions requires intersection contribution 4. Distribution `(2,2,0)` always contributes 4: `3*C(5,2)^2=300` choices. Distribution `(2,1,1)` has five cross pairs and needs exactly one triple concurrency. Ceva on positions `i,j,k in {1..5}` yields 13 concurrent triples: permutations of `(1,3,5)`, `(2,3,4)`, plus `(3,3,3)`. Choose doubled family 3 ways and extra peg 4 ways: `13*12=156`. Total selections `456`; digit-square sum `4^2+5^2+6^2=77`.

## K. Contrast-pair candidates
1. pair intersections vs distinct points;
2. generic crossing vs triple concurrency;
3. incidence count vs coordinate computation;
4. region increment vs raw crossing count;
5. same-family vs cross-family cevians;
6. handshaking W1-B vs geometric incidence W1-D.

## L. Transfer candidates
T2 lines through marked polygon points; T2 student-club membership bipartite incidence; T3 concurrency changes a maximum-region count; T4 Ceva geometry feeding a combinatorial count.

## M. Candidate mastery items
Recognition: where can concurrency occur? First-line: write cross-family pair count. Full solve: four-segment region target. WHY-NOT: show why C(4,2) intersections can overcount. Verification: compare region count before/after merging three crossings into one concurrency.

## N. Dependency declarations
`REQUIRES`: W1-A model; COMB-01 object/multiplicity discipline.  
`BRIDGE_REQUIRES`: minimal Ceva condition from geometry when source requires it; no geometry chapter.  
`APPLIES`: Q22.  
Downstream may assume learner distinguishes pair incidences from distinct intersection points.

## O. Lead integration notes
Place after handshaking as “count relations twice” in a different surface. Keep Ceva as a source-specific bridge, not canonical geometry teaching. Student item must include enough exact source geometry to justify incidence claims.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact source page/figure custody pending for publication
```
