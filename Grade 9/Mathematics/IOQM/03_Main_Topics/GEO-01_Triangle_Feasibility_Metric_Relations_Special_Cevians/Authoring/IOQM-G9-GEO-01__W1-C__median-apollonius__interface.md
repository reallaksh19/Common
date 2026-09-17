---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-C
microstream_title: Median and Apollonius Structure
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: recognizing a median from midpoint data, deriving/using Apollonius for the median, centroid retrieval from GEO-03 when the median is intersected by medians, and distinguishing median from altitude/angle bisector.

Excluded: Stewart in full generality; centroid canon beyond GEO-03 retrieval; angle-bisector theorem; coordinate/vector canon.

# B. Learner-state model
PRIOR_KNOWLEDGE: median joins a vertex to the midpoint of the opposite side.
LIKELY_HALF_KNOWLEDGE: treats median as perpendicular or angle-bisecting; memorizes a median-length formula without seeing it as a special Stewart/Pythagorean balance.
MISSING_BRIDGES: classify the segment before choosing a theorem; midpoint means two equal base segments, not perpendicularity.
OWNERSHIP_TARGET: median recognition and the cheapest metric relation.

# C. Mathematical invariant / governing structure
If `AM` is a median of triangle `ABC` and `BM=CM=a/2`, with `AB=c`, `AC=b`, `BC=a`, then

`AB^2+AC^2 = 2(AM^2+BM^2)`

or equivalently

`m_a^2=(2b^2+2c^2-a^2)/4`.

One derivation: place `M` at the origin on the x-axis with `B=(-a/2,0)`, `C=(a/2,0)`, `A=(u,v)`; adding `AB^2` and `AC^2` cancels the linear `u` terms and yields the identity.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| midpoint marking | median identity | state `BM=CM` | midpoint explicitly given/proved | assume right angle |
| side-square balance | Apollonius | write `b^2+c^2=2(m_a^2+a^2/4)` | median established | use Stewart with unnecessary variables |
| centroid on median | fixed `2:1` ratio | retrieve GEO-03 centroid interface | centroid established | reteach centroid chapter |
| coordinates centered at midpoint | derivation/check | place `B,C` symmetrically | alternate route useful | default to coordinate brute force |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| cevian hits midpoint | median/Apollonius | Stewart | does midpoint symmetry collapse the general formula? | Stewart seems universal |
| cevian looks perpendicular | median only | altitude/Pythagoras | is a right angle stated/proved? | common textbook diagrams |
| cevian splits vertex angle | angle-bisector route | median | is equal angle stated/proved? | symmetry appearance |
| centroid appears | retrieve 2:1 | derive from coordinates | is centroid property already exported by GEO-03? | coordinates are easy to set up |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-MED-01
WRONG_MOVE: assume a median is an altitude.
WHY_TEMPTING: isosceles examples dominate memory.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: midpoint information gives equal base segments only.
FALSIFIER_OR_CONTRAST: scalene triangle with a visibly slanted median.

ERROR_CODE: G01-MED-02
WRONG_MOVE: apply median formula to any cevian.
WHY_TEMPTING: formula is remembered without hypothesis.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: verify midpoint before Apollonius.
FALSIFIER_OR_CONTRAST: same triangle with division ratio `2:1` instead of `1:1`.

ERROR_CODE: G01-MED-03
WRONG_MOVE: reteach centroid ratios inside GEO-01.
WHY_TEMPTING: centroid lies on medians.
MISSING_LINK_CLASS: PREREQUISITE
REPAIR_INVARIANT: retrieve GEO-03 `2:1` and area facts; add only new metric structure.
FALSIFIER_OR_CONTRAST: ask whether target closes from centroid ratio alone before invoking lengths.

# G. First-move cues
- “M is midpoint of BC” and `AM` appears -> write `BM=CM=BC/2`.
- target involves median length + side lengths -> write Apollonius in side-square form.
- centroid divides the median -> retrieve `AG:GM=2:1` from GEO-03 before adding metric information.
- no midpoint -> do not call the cevian a median.

# H. H3 -> H0 fading plan
- H3: substitute into a supplied Apollonius identity.
- H2: learner identifies midpoint and writes the identity.
- H1: decide median route vs Stewart/angle-bisector route.
- H0: changed-surface problem with a midpoint hidden in equal segment data.

# I. Validated IOQM source anchors
No listed historical anchor is a pure Apollonius item. `IOQM-2024-Q22` is a deliberate contrast: `BD:DC=2:1`, so `AD` must not be misclassified as a median.

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q22 | 2024 Q22 | CLEAN_OFFICIAL | contrast | non-midpoint cevian in right triangle | custody pending | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q22 has `BD:DC=2:1`, not `1:1`; therefore median/Apollonius is invalid. Treating `BD=2t,DC=t` and using the actual right-triangle relation yields answer `34`, confirming that correct classification precedes theorem choice.

# K. Contrast-pair candidates
1. midpoint cevian vs `2:1` cevian;
2. median vs altitude;
3. median vs angle bisector;
4. Apollonius vs general Stewart;
5. centroid ratio retrieval vs new metric teaching;
6. symmetric coordinate derivation vs formula memorization.

# L. Transfer candidates
- T2: median in a triangle described only by equal base segments.
- T2: parallelogram diagonal problem that reduces to midpoint coordinates.
- T3: derive median identity with vectors/coordinates, then solve synthetically.
- T4: integer side problem where Apollonius produces a square/integrality filter.

# M. Candidate mastery items
- recognition-only: decide whether a named cevian is a median from the givens.
- first-line-only: write the Apollonius relation.
- full solve: recover a missing median/side length.
- WHY-NOT: explain why a `2:1` division cannot use the median formula.
- verification: check a candidate formula on a `3-4-5` triangle with a chosen median.

# N. Dependency declarations
REQUIRES: midpoint definition; Pythagorean algebra.
BRIDGE_REQUIRES: GEO-03 centroid ratio only when centroid appears.
APPLIES: coordinate symmetry as a derivation/check.
DOWNSTREAM MAY ASSUME: median recognition and Apollonius relation.

# O. Lead integration notes
Place after feasibility/angle classification but before general Stewart. Use this stream to establish the chapter-wide router: classify the cevian first. Teach centroid facts by retrieval only. Keep coordinate derivation teacher-side or discovery-side if it improves sense-making.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: no pure historical Apollonius anchor in the named set; authored examples require independent item-key verification before promotion.
