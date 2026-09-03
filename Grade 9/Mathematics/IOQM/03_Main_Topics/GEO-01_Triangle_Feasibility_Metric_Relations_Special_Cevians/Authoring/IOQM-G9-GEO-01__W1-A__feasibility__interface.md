---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-A
microstream_title: Triangle Feasibility
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: strict triangle inequality, interval form for an unknown side, feasibility before construction/calculation, shared-diagonal feasibility, integer-side filtering when it is only a final restriction.

Excluded: generic integer/Diophantine canon; quadrilateral classification; full counting methods; right/acute/obtuse metric classification.

# B. Learner-state model
PRIOR_KNOWLEDGE: `a+b>c` is familiar.
LIKELY_HALF_KNOWLEDGE: checks only one inequality, or checks after long algebra.
MISSING_BRIDGES: for sides `p,q,d`, feasibility is the interval `|p-q|<d<p+q`; feasibility should be tested before optimizing/counting.
OWNERSHIP_TARGET: make geometric admissibility an automatic gate.

# C. Mathematical invariant / governing structure
Three positive lengths form a nondegenerate triangle iff the largest is less than the sum of the other two. Equivalently, for fixed `p,q`, the third side satisfies `|p-q|<d<p+q`.

Proof: the upper bound is triangle inequality; the lower bound is the two rearranged inequalities `p<q+d` and `q<p+d`.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| sorted sides | single critical upper inequality | order `a<=b<=c`, test `a+b>c` | positive lengths | test all three mechanically |
| interval for unknown side | complete feasibility window | write `|p-q|<d<p+q` | two fixed sides | use only `d<p+q` |
| two triangles sharing a diagonal | intersection of two windows | form one interval per side-pair | quadrilateral diagonal splits the four sides into two pairs | use a quadrilateral rule from appearance |
| integer filter | admissible lattice points | intersect interval with integers | integrality stated | teach number theory instead of geometry |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| three lengths | feasibility | compute area/angles | do they form a triangle at all? | formulas are familiar |
| four sides + proposed diagonal | intersect two triangle windows | quadrilateral theorem | is the diagonal simply the shared third side of two triangles? | surface says quadrilateral |
| real interval + integer side | geometry first, integer filter second | enumerate integers first | what is the geometric admissible interval? | finite search feels easy |
| similarity-looking cevian | retrieve GEO-03 | new metric theorem | can ratio/area transfer already close it? | topic label suggests cevian formula |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-FEAS-01
WRONG_MOVE: check only `a+b>c` without identifying the largest side.
WHY_TEMPTING: memorized slogan.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: sort first or use interval form.
FALSIFIER_OR_CONTRAST: sides `2,8,9` vs `2,3,8`.

ERROR_CODE: G01-FEAS-02
WRONG_MOVE: allow equality in triangle inequality.
WHY_TEMPTING: inequality endpoints feel harmless.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: equality is degenerate, not a triangle.
FALSIFIER_OR_CONTRAST: `3,4,7` lies on a line.

ERROR_CODE: G01-FEAS-03
WRONG_MOVE: count integer candidates before deriving the geometric interval.
WHY_TEMPTING: small numbers invite enumeration.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: continuous feasibility first, discrete filter second.
FALSIFIER_OR_CONTRAST: change perimeter so brute-force list becomes large.

# G. First-move cues
- fixed sides `p,q`, unknown third side -> `|p-q|<d<p+q`.
- perimeter + isosceles -> express base from perimeter, then enforce positivity and `<2a`.
- proposed quadrilateral diagonal -> build two third-side intervals and intersect.
- algebra gives side ratios -> test positivity and triangle inequality before accepting.

# H. H3 -> H0 fading plan
- H3: write all three inequalities for a supplied triple.
- H2: sort sides and reduce to one critical inequality.
- H1: derive an interval for an unknown third side.
- H0: changed-surface shared-diagonal item with integer candidate choices.

# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q04 | 2025 Q04 | CLEAN_OFFICIAL | primary | isosceles integer feasibility | no essential figure | FINAL_OFFICIAL |
| IOQM-2025-Q09 | 2025 Q09 | CLEAN_OFFICIAL | primary | shared-diagonal feasibility | no essential figure | FINAL_OFFICIAL |
| IOQM-2024-Q10 | 2024 Q10 | CLEAN_OFFICIAL | bridge | algebraic side ratio then feasibility | no essential figure | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
- Q04: equal side `a`, base `23-2a`; positivity and `23-2a<2a` give `a=6..11`, answer `06`.
- Q09: pairings produce diagonal intervals `(25,30)`, `(55,60)`, `(65,70)`; only source candidate `28` is feasible, answer `28`.
- Q10: source quadratic becomes `(a-3b)^2+(pb-3c)^2=0`; side ratio `3:1:p/3`, triangle inequalities give integer `p=7..11`, answer `05`.

# K. Contrast-pair candidates
1. positive lengths vs feasible triangle;
2. strict inequality vs degenerate equality;
3. one triangle interval vs intersection of two intervals;
4. real feasibility vs integer filtering;
5. algebraic solution vs geometrically admissible solution;
6. quadrilateral surface vs two-triangle structure.

# L. Transfer candidates
- T2: stick lengths instead of triangle side labels.
- T2: unknown diagonal in a four-bar linkage.
- T3: continuous interval then count admissible integer lengths.
- T4: algebraic parameter produces candidate side ratios; reject infeasible values.

# M. Candidate mastery items
- recognition-only: identify which proposed triples cannot form a triangle.
- first-line-only: write the admissible interval for a third side.
- full solve: isosceles integer perimeter count.
- WHY-NOT: explain why `d<p+q` alone is insufficient.
- verification: decide whether an algebra-derived side triple is geometrically valid.

# N. Dependency declarations
REQUIRES: positivity/order of real numbers.
BRIDGE_REQUIRES: elementary integer filtering when stated.
APPLIES: GEO-03 only when a ratio transfer already solves the surface.
DOWNSTREAM MAY ASSUME: triangle feasibility interval and strict-degeneracy rule.

# O. Lead integration notes
Teach feasibility early, before any cevian formula. Reuse the interval form throughout the chapter as a fail-closed check. Compress integer enumeration to a filter, not a separate lesson. No internal source codes in student prose.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: HBCSE page-image custody remains pending for publication where exact source presentation is needed.
