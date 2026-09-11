---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-G
microstream_title: Integer Geometry Filters
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: applying integrality after geometric structure is established; integer side/perimeter/hypotenuse restrictions; factor-pair searches created by metric identities; discrete optimization after continuous geometry.

Excluded: generic Diophantine theory, divisor-count canon, modular arithmetic, or NT-04 teaching. Those are BRIDGE/ROUTE-BACK only.

# B. Learner-state model
PRIOR_KNOWLEDGE: integer arithmetic, factors, simple enumeration.
LIKELY_HALF_KNOWLEDGE: begins by listing integers and may miss the geometric equation that collapses the search.
MISSING_BRIDGES: geometry defines the admissible real set first; integrality then selects lattice points or factor pairs.
OWNERSHIP_TARGET: `GEOMETRY -> EQUATION/INTERVAL -> INTEGER FILTER -> CHECK`.

# C. Mathematical invariant / governing structure
Discrete geometry problems are two-stage: first derive a continuous geometric constraint; only then use integrality. If a metric relation factors into integers, search factor pairs of the geometric invariant rather than raw side tuples.

Example: a right triangle with altitude `h` to the hypotenuse and integer hypotenuse/perimeter can produce a difference-of-squares factorization; the factor pairs encode the integer filter.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| feasibility interval | admissible real lengths | derive strict bounds | triangle side problem | list integers first |
| perimeter parameterization | one-variable integer family | express remaining side from total | fixed integer perimeter | enumerate triples |
| factorized metric identity | finite factor pairs | factor the constant/invariant | both factors integer | brute-force side lengths |
| projection variables | product/sum structure | use right-triangle metric relation | altitude/projections available | continuous AM-GM only |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| integer sides + perimeter | geometric interval then integers | partition counting first | what inequalities make a triangle? | counting is finite |
| integer hypotenuse/perimeter | factorized metric relation | continuous optimization | does integrality turn a difference of squares into factor pairs? | minimum language suggests calculus/AM-GM |
| side ratios from algebra | test triangle + integrality | accept algebraic values | are sides required integer/positive/feasible? | algebra seems complete |
| divisor search appears | bridge to elementary factors | teach NT-04 | is factorization merely a terminal filter? | number-theory surface emerges late |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-INT-01
WRONG_MOVE: enumerate integer triples before deriving geometry.
WHY_TEMPTING: small numerical ranges.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: continuous admissibility first.
FALSIFIER_OR_CONTRAST: increase perimeter so enumeration becomes impractical.

ERROR_CODE: G01-INT-02
WRONG_MOVE: optimize over reals and ignore that the optimum may be nonintegral.
WHY_TEMPTING: standard inequality methods give a clean lower bound.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: distinguish real lower bound from attainable integer minimum.
FALSIFIER_OR_CONTRAST: nearest real optimum fails factor/integrality conditions.

ERROR_CODE: G01-INT-03
WRONG_MOVE: turn a final factor-pair step into a hidden number-theory chapter.
WHY_TEMPTING: factorization becomes the visible last step.
MISSING_LINK_CLASS: PREREQUISITE
REPAIR_INVARIANT: geometry owns the equation; arithmetic only filters it.
FALSIFIER_OR_CONTRAST: remove integrality and observe the same geometric derivation still works.

# G. First-move cues
- integer perimeter + isosceles -> parameterize one side, derive strict triangle bounds, then count integers.
- integer hypotenuse/perimeter + altitude -> derive the metric identity first, then factor.
- algebra gives parameterized side ratio -> impose positivity, triangle feasibility, then integrality if stated.
- “minimum integer” -> separate continuous bound from discrete attainability.

# H. H3 -> H0 fading plan
- H3: list integers inside a supplied admissible interval.
- H2: derive the interval/equation, then filter.
- H1: identify whether factor pairs or interval integers are the right discrete representation.
- H0: changed-surface metric problem where the real optimum is not automatically admissible.

# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q04 | 2025 Q04 | CLEAN_OFFICIAL | primary | integer isosceles sides + feasibility | no essential figure | FINAL_OFFICIAL |
| IOQM-2024-Q10 | 2024 Q10 | CLEAN_OFFICIAL | bridge | integer parameter after side-ratio feasibility | no essential figure | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q15 | 2024 Q15 | CLEAN_OFFICIAL | bridge | least integer above acute-triangle threshold | no essential figure | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q30 | 2024 Q30 | CLEAN_OFFICIAL | primary | integer hypotenuse/perimeter + altitude | custody pending | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
- Q04: geometric bounds force `a=6..11`, so six integer triangles.
- Q10: square decomposition gives side ratio; triangle inequalities force integer `p=7..11`, answer `05`.
- Q15: continuous threshold `n>38(1+sqrt2)≈91.74`; least integer `92`.
- Q30: with altitude 12, `ac=12b` and integer `l=a+c`; `(b+12-l)(b+12+l)=144`; factor pair `(2,72)` yields minimum `b=25`, realized by `15-20-25`.

# K. Contrast-pair candidates
1. real feasibility vs integer admissibility;
2. continuous lower bound vs attainable integer minimum;
3. interval filtering vs factor-pair filtering;
4. geometry equation vs number-theory ownership;
5. brute-force triples vs one-parameter structure;
6. candidate integer vs final original-condition check.

# L. Transfer candidates
- T2: integer stick-length triangle count.
- T2: right triangle with rational altitude and integer perimeter.
- T3: compare continuous optimum with nearest admissible integer geometry.
- T4: factor-pair filter after a geometric difference-of-squares identity.

# M. Candidate mastery items
- recognition-only: identify whether integrality is structural or merely a final filter.
- first-line-only: write the geometric interval/equation before enumeration.
- full solve: minimum integer hypotenuse under a metric constraint.
- WHY-NOT: explain why a real AM-GM minimizer does not finish an integer problem.
- verification: reconstruct a triangle from the winning factor pair and check all original conditions.

# N. Dependency declarations
REQUIRES: GEO-01 feasibility/metric identities.
BRIDGE_REQUIRES: elementary factor pairs and integer ordering; NT-04 only if deeper integer structure is genuinely needed.
APPLIES: arithmetic filtering after geometry.
DOWNSTREAM MAY ASSUME: geometry-first discrete-filter workflow.

# O. Lead integration notes
Distribute this doctrine across examples rather than creating a long standalone integer-geometry chapter. Make the two-stage workflow visible in First-Step Reference and diagnostic feedback. Route deeper number theory away from GEO-01.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NT-04 is not assumed frozen; only elementary arithmetic filtering is consumed here.
