---
main_topic_id: IOQM-G9-GEO-04
microstream_id: W1-D
microstream_title: Alternate segment theorem as a recognition route
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-04
prerequisite_interfaces:
  - GEO02_Stable_Angle_Polygon_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-D — Alternate Segment Theorem

## A. Scope boundary
Included: angle between tangent and chord equals angle in the alternate segment subtended by that chord, theorem/converse recognition where justified, and method selection against radius-tangent chasing. Excluded: tangent proof from appearance, generic parallel-angle canon and advanced directed-angle notation.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: tangent-radius perpendicular; inscribed-angle facts.
LIKELY_HALF_KNOWLEDGE: quotes “alternate segment” without naming the tangent, chord and target chord endpoints.
MISSING_BRIDGES: recognize exact tangent-chord pair; route directly to the matching inscribed angle.
OWNERSHIP_TARGET: TANGENT + CHORD -> NAME CHORD -> FIND INSCRIBED ANGLE SUBTENDING IT -> LOCAL CLOSURE.
```

## C. Mathematical invariant / governing structure
If a tangent at `A` meets chord `AB`, the angle between the tangent and `AB` equals an inscribed angle subtending chord `AB` in the opposite segment. This can be derived from radius-tangent perpendicularity plus the inscribed/central-angle relation, so it is not an isolated magic rule.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| tangent-chord angle | direct target match | name chord endpoints | tangent established | match an angle subtending different chord |
| radius proof | derivation/check | join centre to tangent point | centre available | use for every problem |
| same-chord inscribed angle | destination angle | locate circumference point | point on same circle | choose visually similar angle |
| local angle chase | remaining closure | retrieve GEO-02 | circle relation already used | replace theorem by long chase |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| tangent+chord target | alternate segment | radius chase | is there an inscribed angle subtending same chord? | radius theorem is familiar |
| tangent+radius length | radius/perpendicular | alternate segment | is target metric rather than angular? | theorem name triggered by tangent |
| secant line | chord/inscribed angle | alternate segment | is the line actually tangent? | near-tangent drawing |
| unknown circle membership | first prove cyclicity | alternate segment | is target point on circle? | geometry appears circular |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: GEO04-ALT-01
WRONG_MOVE: match tangent-chord angle to any angle on the circle.
WHY_TEMPTING: “angle in alternate segment” is remembered vaguely.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: both angles must subtend the same chord.
FALSIFIER_OR_CONTRAST: compare two different chords from tangent point.

ERROR_CODE: GEO04-ALT-02
WRONG_MOVE: apply theorem to a secant.
WHY_TEMPTING: line crosses near point of contact.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: prove/stipulate tangency first.
FALSIFIER_OR_CONTRAST: secant makes two circle intersections.
```

## G. First-move cues
- tangent and chord share contact point -> write the matching same-chord inscribed angle.
- target is angle only -> try alternate segment before adding centre.
- target is length/power -> route to W1-C/E instead.

## H. H3 -> H0 fading plan
H3: highlight tangent, chord and destination angle. H2: highlight only chord. H1: give clean figure with tangent mark. H0: changed orientation/labels where learner identifies same chord unaided.

## I. Validated IOQM source anchors
No historical anchor is promoted solely by this theorem in the five-item seed. It is required canonical scope and must be validated with independently checked author-created items.

## J. Source-independent mathematical trace
Derivation route: radius at contact is perpendicular to tangent; in the isosceles centre-chord triangle, express the tangent-chord angle in terms of the central angle; an inscribed angle on the same chord is half that central angle. Conditions are explicit and no source answer is promoted.

## K. Contrast-pair candidates
1. tangent-chord vs radius-tangent angle;
2. same chord vs different chord;
3. tangent vs secant;
4. alternate-segment shortcut vs long centre chase;
5. theorem vs converse;
6. target angle vs target power/length.

## L. Transfer candidates
T2 rotate tangent figure; T2 chord endpoint reversed; T3 prove tangency from an angle equality then use theorem; T4 combine with cyclic quadrilateral.

## M. Candidate mastery items
Recognition: identify matching angle. First-line: state relation only. Full solve: one theorem + local chase. WHY-NOT: reject a different-chord angle. Verification: state tangency/circle membership obligations.

## N. Dependency declarations
`REQUIRES`: W1-A circle angles, W1-C tangency, GEO-02 local angle closure.  
Downstream may assume learner names the common chord before using alternate segment.

## O. Lead integration notes
Teach as a derived shortcut after radius-tangent and same-chord facts, not as a memorized standalone theorem. Include at least one “do not use” secant contrast.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: NOT_RUN
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: author-created candidate items still require lead selection
```
