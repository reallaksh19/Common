---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-B
microstream_title: Right / Acute / Obtuse Metric Tests
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: converse-Pythagoras metric classification, largest-side discipline, extremal reduction when many candidate side triples must all be acute, and feasibility-before-angle classification.

Excluded: generic inequalities, trigonometric canon, coordinate/vector canon, and optimization beyond the minimum needed to identify a worst-case triple.

# B. Learner-state model
PRIOR_KNOWLEDGE: Pythagoras theorem.
LIKELY_HALF_KNOWLEDGE: knows `a^2+b^2=c^2` for right triangles but not the acute/obtuse comparison or why `c` must be the largest side.
MISSING_BRIDGES: feasibility first; then compare the square of the largest side with the sum of squares of the other two; for families, monotonicity can identify the hardest triple.
OWNERSHIP_TARGET: reliable metric angle classification without diagram guessing.

# C. Mathematical invariant / governing structure
For a feasible triangle with `a<=b<=c`:
- acute iff `c^2<a^2+b^2`;
- right iff `c^2=a^2+b^2`;
- obtuse iff `c^2>a^2+b^2`.

This is the law-of-cosines sign test for the angle opposite `c`, compressed to the only angle that can be right/obtuse when `c` is largest.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| ordered side triple | critical angle type | sort and compare squares | triangle feasible | test an arbitrary side as `c` |
| parameterized side set | worst case | maximize `c`, minimize `a,b` subject to source rules | monotonic family | check every triple |
| repeated-choice family | true extremal case | honor whether choices may repeat | source permits repetition | silently force distinct choices |
| coordinate placement | angle through dot product | only as alternate/check | route demonstrably cheaper | replace simple square comparison with coordinates |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| three side lengths | square comparison | angle chase | are only lengths given? | angle methods feel geometric |
| many triples from ordered set | extremal monotonic test | enumerate all triples | which choice makes `c^2-a^2-b^2` largest? | finite set suggests brute force |
| repeated allowed vs distinct | use repeated minimums if allowed | use two smallest distinct | does source say “not necessarily distinct”? | habit assumes selection without replacement |
| candidate not feasible | reject before classifying | apply square test anyway | do the lengths form a triangle? | square test still produces a sign |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-ANGLE-01
WRONG_MOVE: use the square test without sorting.
WHY_TEMPTING: memorized formula has generic letters.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: `c` must be the largest side.
FALSIFIER_OR_CONTRAST: compare the same triangle under a relabeling.

ERROR_CODE: G01-ANGLE-02
WRONG_MOVE: classify an infeasible triple as obtuse.
WHY_TEMPTING: `c^2>a^2+b^2` numerically holds.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: triangle feasibility is a prior gate.
FALSIFIER_OR_CONTRAST: `2,3,8` is not an obtuse triangle; it is no triangle.

ERROR_CODE: G01-ANGLE-03
WRONG_MOVE: in Q15-style families, use `n,n+2,n+38` when repetition is allowed.
WHY_TEMPTING: students assume three selected set elements are distinct.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: preserve selection semantics before optimization.
FALSIFIER_OR_CONTRAST: repeated `n,n,n+38` is strictly harder to keep acute.

# G. First-move cues
- three side lengths -> sort; check feasibility; compare `c^2` with `a^2+b^2`.
- “every three choices are acute” -> identify the triple maximizing `c^2-a^2-b^2`.
- repeated choices allowed -> test repeated smallest values.
- right triangle already stated -> use exact equality as a metric relation, not a classification question.

# H. H3 -> H0 fading plan
- H3: classify supplied feasible triples with the comparison written.
- H2: learner chooses the largest side and writes one comparison.
- H1: identify the extremal triple in a family.
- H0: changed-surface threshold problem where choices may repeat.

# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q15 | 2024 Q15 | CLEAN_OFFICIAL with mechanism correction | primary | every selected triple acute; repeated choices allowed | no essential figure | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q22 | 2024 Q22 | CLEAN_OFFICIAL | bridge | stated right triangle supplies metric equality | figure custody pending | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
- Q15: hardest permitted triple is `(n,n,n+38)`; require `(n+38)^2<2n^2`; threshold `n>38(1+sqrt(2))`, least integer `92`. This corrects the stale distinct-choice mechanism.
- Q22: right angle at `A` gives `AB^2+AC^2=BC^2`; with `BD:DC=2:1` and side relation, independent algebra closes to answer `34`.

# K. Contrast-pair candidates
1. feasible obtuse triangle vs infeasible triple;
2. largest-side square test vs arbitrary-side comparison;
3. repeated-choice extremum vs distinct-choice extremum;
4. one triple vs all-triples threshold;
5. metric route vs diagram-based angle guess;
6. exact right equality vs approximate numerical appearance.

# L. Transfer candidates
- T2: classify triangle from squared lengths directly.
- T2: threshold for all triples from an arithmetic progression to be acute.
- T3: integer-valued parameter after a continuous inequality threshold.
- T4: compare a coordinate dot-product check with the side-square test.

# M. Candidate mastery items
- recognition-only: identify which side must be `c`.
- first-line-only: write the correct comparison for an ordered triple.
- full solve: find least parameter ensuring every permitted triple is acute.
- WHY-NOT: explain why `2,3,8` is not “obtuse.”
- source-integrity: decide how the extremal triple changes when repetition is allowed.

# N. Dependency declarations
REQUIRES: triangle feasibility; Pythagoras theorem.
BRIDGE_REQUIRES: elementary monotonicity/inequality manipulation.
APPLIES: coordinate check only as alternate representation.
DOWNSTREAM MAY ASSUME: sorted-side acute/right/obtuse criterion and feasibility-first rule.

# O. Lead integration notes
Place immediately after feasibility. Explicitly surface the source-language distinction between distinct and not-necessarily-distinct choices. Avoid introducing law-of-cosines formalism if the square comparison suffices. Reuse as a check in later metric problems.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact HBCSE page-image custody pending where the historical figure is promoted.
