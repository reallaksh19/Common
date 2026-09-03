---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-E
microstream_title: Power of a point and radical-axis recognition
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-E — Power of a Point and Radical-Axis Recognition

## A. Scope boundary
Included: point power as a product invariant for secants/tangents, equal powers and radical axis, common chord perpendicular to centre line for two circles, and method selection. Excluded: advanced coaxal systems, inversion and general analytic circle equations.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can multiply segment lengths and use similar triangles.
LIKELY_HALF_KNOWLEDGE: memorizes PA*PB=PC*PD without identifying one external point/circle.
MISSING_BRIDGES: product belongs to one point relative to one circle; equal powers create a locus/radical axis; common chord is structural data.
OWNERSHIP_TARGET: FIX POINT/CIRCLE -> IDENTIFY SECANT/TANGENT PRODUCTS -> EQUAL POWER -> LENGTH/CENTRE CONSEQUENCE.
```

## C. Mathematical invariant / governing structure
For a fixed point `P` and circle, every secant through `P` has signed/appropriate segment product `PA*PB` equal to the same point power; a tangent has power `PT^2`. For two circles, points of equal power lie on their radical axis, which is perpendicular to the line of centres; their common chord lies on this axis.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| secant product | length invariant | pair near/far intersections | same external/interior point | multiply unrelated chords |
| tangent square | equal power | use `PT²` | tangent established | use one tangent length unsquared |
| common chord | radical axis | identify equal-power line | two intersecting circles | treat as arbitrary chord |
| centre coordinates | verification | align radical axis/centres | metric route justified | coordinate before structure |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| two secants from one point | power product | similarity derivation | is product target immediate? | similar triangles familiar |
| tangent+secant | tangent-square power | tangent-radius | target length product or angle? | tangent theorem trigger |
| two circles common chord | radical axis | generic chord geometry | are equal powers/centres relevant? | chord theorem familiarity |
| one circle only | power | radical-axis language | are two circles involved? | advanced term sounds useful |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: GEO04-POW-01
WRONG_MOVE: multiply two visible chord pieces that do not share the same point-power setup.
WHY_TEMPTING: all chord-product formulas look alike.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: name the fixed point and ordered intersections on each line.
FALSIFIER_OR_CONTRAST: unrelated chords with no common intersection point.

ERROR_CODE: GEO04-POW-02
WRONG_MOVE: call any common chord a diameter/radical axis without relating centres.
WHY_TEMPTING: perpendicular picture.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: common-chord points have equal power to both circles; hence chord line is radical axis.
FALSIFIER_OR_CONTRAST: arbitrary chord of one circle.
```

## G. First-move cues
- two secants from same point -> write product equality.
- tangent and secant from same point -> tangent square = secant product.
- two circles intersect at A,B -> AB is their common chord/radical axis; connect centres if useful.
- target is angle at tangent -> W1-D may be cheaper.

## H. H3 -> H0 fading plan
H3: label near/far secant points. H2: cue “same external point.” H1: show two secants/tangent without formula. H0: two-circle common-chord configuration where learner chooses equal power/radical-axis reasoning.

## I. Validated IOQM source anchors
`IOQM-2025-Q30=10` is a bridge anchor using common chord/radical-axis structure between two internally tangent circles. No seed item is a pure textbook secant-product problem.

## J. Source-independent mathematical trace
In Q30, inner circles intersect at `A,B`; their common chord `AB` is perpendicular to the line of centres. Given `OA ⟂ AB`, `O` and the two inner centres align in the perpendicular direction structure. Combining internal tangency distances with point-on-circle equations yields `r1+r2=10`; full coordinate-independent structural role and algebra are independently audited.

## K. Contrast-pair candidates
1. secant product vs chord length formula;
2. tangent square vs equal tangents;
3. one-circle power vs two-circle radical axis;
4. common chord vs arbitrary chord;
5. product invariant vs angle theorem;
6. synthetic power vs coordinate verification.

## L. Transfer candidates
T2 two secants; T2 tangent+secant; T3 intersecting circles with common chord; T4 radical-axis bridge to coordinate/length constraints.

## M. Candidate mastery items
Recognition: identify fixed point/circle. First-line: write correct product. Full solve: tangent-secant length. WHY-NOT: reject unrelated product. Verification: explain why common chord is radical axis.

## N. Dependency declarations
`REQUIRES`: W1-C tangency where tangent used; basic similarity may be retrieved if deriving power.  
`APPLIES`: W1-F chord/secant and Q30.  
Downstream may assume learner recognizes one-point product invariance and common-chord equal power.

## O. Lead integration notes
Derive one representative product from similarity, then compress to a recognition invariant. “Radical axis” may appear after the behavior “equal power to both circles,” not before.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: Q30 exact page-image custody pending
```
