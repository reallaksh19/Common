---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-B
microstream_title: Cyclic quadrilaterals and cyclicity recognition
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-B — Cyclic Quadrilaterals and Cyclicity Recognition

## A. Scope boundary
Included: opposite-angle supplementary relation, equal-angle cyclicity criteria, right-angle/diameter cyclicity, and distinguishing cyclic from generic quadrilaterals. Excluded: generic `360°` quadrilateral closure (retrieve GEO-02), power of point (W1-E) and coordinate determinant methods as canonical teaching.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: quadrilateral angle sum; may know opposite angles of cyclic quadrilateral sum 180°.
LIKELY_HALF_KNOWLEDGE: assumes a quadrilateral is cyclic from appearance or uses cyclic relations before proving cyclicity.
MISSING_BRIDGES: cyclicity is a structure to establish; generic and cyclic angle relations are different.
OWNERSHIP_TARGET: PROVE/READ CYCLICITY -> SELECT CYCLIC RELATION -> LOCAL CLOSURE -> CHECK NONDEGENERACY.
```

## C. Mathematical invariant / governing structure
Four points are concyclic when a valid cyclicity criterion holds; then opposite angles are supplementary and equal angles may subtend the same chord. Conversely, a supplementary pair of opposite interior angles in a nondegenerate quadrilateral certifies cyclicity.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| opposite-angle relation | cyclic closure | test sum 180° | nondegenerate quadrilateral | use generic 360° only |
| equal-angle criterion | common chord | identify matching endpoints | oriented/geometry context valid | infer from drawing |
| right-angle pair | circle with diameter | find common endpoints | two right angles subtend same segment | assume any two right angles suffice |
| coordinate cyclic check | verification route | normalize simple coordinates | synthetic route not shorter | make coordinates default |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| generic quadrilateral | GEO-02 360° | cyclic relation | is cyclicity given/proved? | one relation is stronger |
| rectangle + four points | cyclic criterion | metric algebra | does one supplementary/right-angle condition certify circle? | rectangle suggests coordinates |
| equal angles | cyclicity | parallel-line converse | what endpoints do angles subtend? | both use equal angles |
| degenerate placement | fail closed | cyclic formula | are four points distinct/nondegenerate as required? | algebra may still simplify |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: GEO04-CYC-01
WRONG_MOVE: opposite angles supplementary because the quadrilateral looks cyclic.
WHY_TEMPTING: circle is suggested visually.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: cyclicity must be given or proved.
FALSIFIER_OR_CONTRAST: arbitrary quadrilateral.

ERROR_CODE: GEO04-CYC-02
WRONG_MOVE: use only 360° closure when cyclicity gives a two-angle relation.
WHY_TEMPTING: generic rule is familiar and always legal.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: once cyclic, use the strongest local invariant first.
FALSIFIER_OR_CONTRAST: compare generic vs cyclic quadrilateral with same three known angles.
```

## G. First-move cues
- “concyclic” stated -> write the relevant opposite-angle or same-chord relation.
- two right angles sharing endpoints -> test common-diameter cyclicity.
- equal angle pair with four points -> test cyclicity before chasing.
- rectangle surface plus circle condition -> separate generic rectangle facts from the one circle-specific constraint.

## H. H3 -> H0 fading plan
H3: mark opposite cyclic angles. H2: cue “what proves cyclic?” H1: show only angle data. H0: changed quadrilateral where learner chooses generic closure or cyclicity criterion.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q23 | 2025/Q23 | CLEAN_OFFICIAL | primary | rectangle + concyclicity + metric equalities | source figure likely; custody pending | 03 independently verified |

## J. Source-independent mathematical trace
Normalize rectangle `AB=1`, let `M=(u,0)`, `N=(1,v)`, height `h`. `MC=CD` gives `h²=2u-u²`; cyclicity gives, under canonical nondegenerate `N!=C`, `hv=u(1-u)`; `MD=MN` gives `v²=4u-u²-1`. Elimination yields `h²=1/2`, so `(AB/BC)²=2=2/1` and answer 03. Degenerate alternate reading remains excluded per source custody note.

## K. Contrast-pair candidates
1. cyclic vs generic quadrilateral;
2. prove cyclicity vs assume from drawing;
3. supplementary criterion vs 360° closure;
4. right-angle cyclicity vs ordinary right triangle;
5. nondegenerate vs degenerate branch;
6. synthetic cyclic relation vs coordinate verification.

## L. Transfer candidates
T2 quadrilateral with equal subtended angles; T2 two right-angle feet; T3 cyclicity hidden in a rectangle/trapezium; T4 coordinate determinant used only to check synthetic cyclicity.

## M. Candidate mastery items
Recognition: cyclic or generic? First-line: state the cyclic relation. Full solve: prove cyclic then find angle/ratio. WHY-NOT: reject appearance-based cyclicity. Verification: identify a degenerate branch that invalidates a criterion.

## N. Dependency declarations
`REQUIRES`: GEO-02 generic quadrilateral and angle closure; W1-A same-chord recognition.  
`APPLIES`: W1-D/E/F.  
Downstream may assume learner proves/reads cyclicity before using cyclic formulas.

## O. Lead integration notes
Make the contrast “generic quadrilateral vs cyclic quadrilateral” explicit. Q23 belongs after basic recognition because its metric surface is harder than its cyclic trigger.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact HBCSE page-image/figure custody pending
```
