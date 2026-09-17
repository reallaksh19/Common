---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-C
microstream_title: Tangency, radius and equal tangents
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-C — Tangency, Radius and Equal Tangents

## A. Scope boundary
Included: radius perpendicular to tangent, equal tangents from one external point, centres aligned for internal/external circle tangency, and tangent recognition chains. Excluded: full power-of-point canon (W1-E), alternate segment theorem (W1-D), and general coordinate-circle methods.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: may recall “radius is perpendicular to tangent.”
LIKELY_HALF_KNOWLEDGE: labels any touching-looking line as tangent or any close circles as tangent.
MISSING_BRIDGES: tangency is a proved/incidence condition; centre-radius relation creates the first right angle or centre-line equation.
OWNERSHIP_TARGET: TANGENCY GIVEN/PROVED -> CENTRE/RADIUS OBJECT -> PERPENDICULAR OR CENTRE-LINE RELATION -> SHORT CHAIN.
```

## C. Mathematical invariant / governing structure
At a tangent point `T`, radius `OT` is perpendicular to the tangent. From an external point `P`, tangent lengths to one circle are equal. If two circles are internally tangent, their centres and tangency point are collinear and centre distance equals the difference of radii; for external tangency it equals the sum.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| radius-tangent right angle | local angle/length structure | join centre to tangent point | tangent established | infer tangent from appearance |
| centre-line tangency | radius sum/difference | connect centres | two circles tangent | use chord relation instead |
| equal tangent segments | length equality | identify common external point | two tangents to same circle | assume equal chords |
| coordinate centre-distance | metric fallback | place centres simply | synthetic chain not shorter | coordinate every circle item |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| line meets circle once in drawing | tangency only if stated/proved | secant/chord | is tangent condition given? | visual contact |
| two tangent circles | centre distance | generic circle intersection | one or two common points? | both have two circles |
| external point with two contact points | equal tangents | Pythagorean computation | are both segments tangents from same point? | lengths look unrelated |
| tangent + chord angle | W1-D alternate segment | radius right angle | which target relation is shorter? | tangent-radius theorem is first remembered |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: GEO04-TAN-01
WRONG_MOVE: draw radius perpendicular to an unstated tangent.
WHY_TEMPTING: line touches the sketch.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: tangent must be stated or proved.
FALSIFIER_OR_CONTRAST: a secant drawn nearly tangent.

ERROR_CODE: GEO04-TAN-02
WRONG_MOVE: centre distance = r1+r2 for internal tangency.
WHY_TEMPTING: sum formula is memorized without type.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: external -> sum; internal -> absolute difference.
FALSIFIER_OR_CONTRAST: one circle inside another.
```

## G. First-move cues
- tangent point named -> join centre to it.
- two tangent circles -> draw line of centres and decide internal/external.
- two tangents from same point -> mark equal lengths.
- tangent/chord angle target -> consider W1-D before a long radius chase.

## H. H3 -> H0 fading plan
H3: radius already drawn. H2: cue “join centre to point of contact.” H1: show tangency marks only. H0: changed two-circle configuration where learner chooses centre-line or equal-tangent route.

## I. Validated IOQM source anchors
`IOQM-2025-Q30=10` is the main tangency anchor: outer circle radius 10 with two internally tangent circles; full answer trace independently closed. Other tangency mechanisms are author-created/transfer candidates.

## J. Source-independent mathematical trace
For Q30, place the two inner centres on a common horizontal line determined by the common chord geometry. Internal tangency gives `OC_i=10-r_i`; combining with a common point `A` and `OA ⟂ AB` yields a quadratic for centre coordinates whose two roots sum to the coordinate of `A`, causing `r1+r2=10`. Independent result agrees with official answer.

## K. Contrast-pair candidates
1. tangent vs secant;
2. internal vs external circle tangency;
3. equal tangents vs equal chords;
4. radius-tangent route vs alternate segment;
5. tangent given vs tangent inferred visually;
6. synthetic centre-line vs coordinate metric fallback.

## L. Transfer candidates
T2 two tangents from external point; T2 internal/external tangent-circle comparison; T3 integer radii under fixed outer radius; T4 radical-axis relation from two intersecting/tangent-linked circles.

## M. Candidate mastery items
Recognition: internal or external? First-line: draw/mark the one radius relation. Full solve: tangent length/radius chain. WHY-NOT: reject sum-of-radii for internal tangency. Verification: identify missing tangency proof in a diagram-based solution.

## N. Dependency declarations
`REQUIRES`: GEO-02 perpendicular/local angle basics.  
`APPLIES`: W1-D/E and Q30.  
Downstream may assume tangent point -> radius perpendicular and circle tangency -> centre-line distance relation.

## O. Lead integration notes
Teach tangency through a two-question router: “what is tangent to what?” and “what does that make perpendicular/equal/collinear?” Avoid a detached theorem list.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: HBCSE page-image custody pending for Q30
```
