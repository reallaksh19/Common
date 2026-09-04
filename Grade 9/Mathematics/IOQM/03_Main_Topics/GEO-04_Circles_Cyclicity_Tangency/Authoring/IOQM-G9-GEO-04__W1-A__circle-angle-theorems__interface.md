---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-A
microstream_title: Centre, inscribed and chord-angle recognition
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-A — Circle Angle Theorems

## A. Scope boundary
Included: centre/inscribed angle relation, same-chord/same-segment angle recognition, diameter/right-angle converse in circle context, and short angle chains. Excluded: generic line/triangle angle teaching (retrieve GEO-02), cyclic-quadrilateral integration (W1-B), tangent alternate-segment use (W1-D), and coordinate circle equations as canonical teaching.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: school angle rules; may know “angle at centre is double.”
LIKELY_HALF_KNOWLEDGE: quotes a circle theorem without identifying the same arc/chord.
MISSING_BRIDGES: theorem selection comes after proving which points/chord/arc control the angle.
OWNERSHIP_TARGET: CIRCLE STRUCTURE -> CHORD/ARC -> ANGLE PAIR -> LOCAL GEO-02 CLOSURE -> CHECK.
```

## C. Mathematical invariant / governing structure
For a fixed chord `AB`, inscribed angles subtending the same chord in the same segment are equal, and the central angle subtending the same minor arc is twice an inscribed angle. A diameter subtends a right angle at any point on the circle; conversely a right angle can certify a diameter/cyclicity relation when hypotheses are exact.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| chord/arc view | same-segment equality | name common chord | points proven concyclic | compare visually similar angles |
| centre-radius triangles | isosceles structure | join centre to endpoints | centre known | use centre theorem without centre |
| diameter view | right angle | identify endpoints of diameter | line through centre or converse proof | assume longest chord is shown |
| local angle network | closure | retrieve GEO-02 G02-1 | circle-specific relation already obtained | reteach generic chase |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| two equal-looking angles | same-chord theorem | generic chase | do both subtend same chord? | picture symmetry |
| 90° at circumference | diameter/cyclicity route | triangle-only route | is there a candidate circle/diameter? | right triangle is familiar |
| centre given | radius/central-angle route | coordinate route | do equal radii create a short chain? | coordinates feel universal |
| no circle structure proved | generic geometry | circle theorem | are points actually concyclic? | circular-looking diagram |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: GEO04-ANG-01
WRONG_MOVE: equal inscribed angles because they “look on the same circle.”
WHY_TEMPTING: theorem recalled without chord/arc condition.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: explicitly name the common chord/arc.
FALSIFIER_OR_CONTRAST: choose two angles subtending different chords.

ERROR_CODE: GEO04-ANG-02
WRONG_MOVE: import GEO-02 angle chase as the main strategy before checking circle structure.
WHY_TEMPTING: angle arithmetic is familiar.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: first ask what circle relation compresses the chase.
FALSIFIER_OR_CONTRAST: same-chord equality replaces several local steps.
```

## G. First-move cues
- two angles with same endpoints on a circle -> name the common chord.
- centre plus chord endpoints -> draw/notice radii.
- right angle with endpoints on a circle -> test diameter relation.
- circle relation established -> retrieve only the minimum GEO-02 local closure.

## H. H3 -> H0 fading plan
H3: mark the common chord. H2: cue “which chord does each angle subtend?” H1: give an uncluttered circle figure. H0: changed figure with auxiliary lines where learner recognizes the same-chord invariant independently.

## I. Validated IOQM source anchors
`IOQM-2024-Q17=25` is a bridge anchor through circumcircle/chord geometry; `IOQM-2025-Q19=29` also uses a circle membership constraint. Full numerical traces are independently closed.

## J. Source-independent mathematical trace
Q17 can be solved via symmetric coordinates after identifying the circumcircle/chord structure, yielding chord `PQ=25`. This stream does not claim coordinate teaching; it supplies the circle recognition boundary and leaves alternate representation to GEO-05 bridge.

## K. Contrast-pair candidates
1. same chord vs merely same circle;
2. central vs inscribed angle;
3. diameter right angle vs generic right triangle;
4. circle recognition vs local angle chase;
5. proved concyclicity vs circular appearance;
6. circle theorem vs coordinate fallback.

## L. Transfer candidates
T2 rotate/relabel same-chord configuration; T2 right-angle converse; T3 hidden diameter in polygon surface; T4 coordinate solution used only as verification of a synthetic relation.

## M. Candidate mastery items
Recognition: identify common chord. First-line: state one circle angle relation. Full solve: short angle chain after one circle theorem. WHY-NOT: reject a same-segment claim with different endpoints. Verification: state what must be proven before using the theorem.

## N. Dependency declarations
`REQUIRES`: GEO-02 local angle closure and theorem/converse discipline.  
`BRIDGE_REQUIRES`: none.  
`APPLIES`: later cyclic/tangent streams.  
Downstream may assume learner identifies the controlling chord/arc before theorem use.

## O. Lead integration notes
Teach recognition chains, not a theorem list. Put one compact circle-angle map early, then use retrieval. Avoid formal arc-measure machinery beyond what is needed for Grade 9 IOQM.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact HBCSE page-image custody pending for publication
```
