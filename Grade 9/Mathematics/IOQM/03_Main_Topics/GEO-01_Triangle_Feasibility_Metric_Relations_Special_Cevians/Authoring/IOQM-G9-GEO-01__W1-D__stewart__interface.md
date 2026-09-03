---
main_topic_id: IOQM-G9-GEO-01
microstream_id: W1-D
microstream_title: Stewart's Theorem and General Cevian Metric Structure
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-GEO-01
prerequisite_interfaces:
  - GEO03_Stable_Similarity_Ratio_Area_Interface_v1.md
source_cutoff: 2026-09-03
---
# A. Scope boundary
Included: general cevian metric identity, choosing Stewart only when a cevian is neither reducible by similarity nor a simpler special case, derivation, and hypothesis discipline.

Excluded: median special case as primary teaching; angle-bisector theorem; full coordinate geometry canon; memorization without classification.

# B. Learner-state model
PRIOR_KNOWLEDGE: Pythagoras and algebraic expansion.
LIKELY_HALF_KNOWLEDGE: may have seen Stewart as a mnemonic and applies it to every cevian.
MISSING_BRIDGES: Stewart is the general fallback after cheaper structure is ruled out; segment names/lengths must be mapped consistently.
OWNERSHIP_TARGET: use one verified general identity without turning the chapter into formula hunting.

# C. Mathematical invariant / governing structure
For triangle `ABC`, point `D` on `BC`, let `BD=m`, `DC=n`, `BC=a=m+n`, `AB=c`, `AC=b`, `AD=d`. Then

`b^2 m + c^2 n = a(d^2 + mn)`.

Derivation by coordinates: put `D=(0,0)`, `B=(-m,0)`, `C=(n,0)`, `A=(u,v)`. Then
`c^2=(u+m)^2+v^2`, `b^2=(u-n)^2+v^2`, `d^2=u^2+v^2`. Expanding `b^2m+c^2n` cancels the linear `u` term and yields `(m+n)(d^2+mn)`.

# D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| labelled cevian | exact segment map | assign `m,n,a,b,c,d` once | D lies on BC | swap `m,n` against wrong adjacent side |
| coordinate derivation | cancellation structure | place D at origin | derivation/check only | use coordinates when formula is already cheapest |
| special-case router | simpler theorem availability | ask midpoint / angle bisector / altitude / similarity? | classification complete | Stewart immediately |
| algebraic identity | target metric | solve only for requested quantity | sufficient data | expand beyond target |

# E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| midpoint cevian | Apollonius | Stewart | is `m=n`? | Stewart always works |
| angle bisector | angle-bisector theorem + metric if needed | Stewart | is equal-angle information given/proved? | side split data resembles Stewart variables |
| parallel/similarity configuration | GEO-03 retrieval | Stewart | can ratio transfer close the target without lengths? | topic is “metric relations” |
| arbitrary cevian with side split | Stewart | coordinate brute force | are all six metric quantities naturally linked? | coordinates feel systematic |

# F. Misconception/diagnosis catalogue
ERROR_CODE: G01-STEW-01
WRONG_MOVE: memorize a mnemonic and mismatch sides.
WHY_TEMPTING: many symbols.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: each base segment multiplies the square of the opposite full side adjacent to the other base endpoint: derive/check with coordinates.
FALSIFIER_OR_CONTRAST: test the identity when `m=n` and verify Apollonius emerges.

ERROR_CODE: G01-STEW-02
WRONG_MOVE: use Stewart when similarity already closes the problem.
WHY_TEMPTING: formula availability.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: cheapest-valid-relation router.
FALSIFIER_OR_CONTRAST: parallel-line cevian with no metric lengths needed.

ERROR_CODE: G01-STEW-03
WRONG_MOVE: assume a cevian is special from appearance.
WHY_TEMPTING: symmetric drawing.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: classify only from stated/proved properties.
FALSIFIER_OR_CONTRAST: same diagram with unequal marked base segments.

# G. First-move cues
- arbitrary cevian with `BD,DC` and side lengths -> write a clean variable map before the identity.
- midpoint -> route back to Apollonius.
- equal vertex angles -> test angle-bisector route first.
- parallel/ratio clues -> retrieve GEO-03 before metric machinery.

# H. H3 -> H0 fading plan
- H3: substitute into a labelled Stewart template.
- H2: build the six-variable map, then write Stewart.
- H1: choose Stewart only after rejecting cheaper special cases.
- H0: changed-surface cevian problem with no method label.

# I. Validated IOQM source anchors
`IOQM-2024-Q22` is a useful boundary anchor: despite a `2:1` split, its right-triangle relation gives a cheaper direct metric equation than invoking full Stewart.

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q22 | 2024 Q22 | CLEAN_OFFICIAL | contrast | divided hypotenuse + right-triangle metric | custody pending | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q22: set `BD=2t`, `DC=t`, `AB=x`, `AC=y`; source relation gives `y=x+t`; Pythagoras gives `x^2+y^2=9t^2`; direct algebra yields `(AC/AB)=(9+sqrt17)/8`, answer `34`. This demonstrates that Stewart is not mandatory merely because a cevian divides a side.

# K. Contrast-pair candidates
1. arbitrary cevian vs median;
2. arbitrary cevian vs angle bisector;
3. Stewart vs GEO-03 similarity retrieval;
4. Stewart vs direct Pythagorean equation;
5. correctly mapped sides vs mnemonic mismatch;
6. general formula vs special-case simplification.

# L. Transfer candidates
- T2: general cevian in a scalene triangle with one unknown length.
- T2: recover Apollonius by setting `m=n`.
- T3: derive Stewart by coordinates, then use it synthetically.
- T4: integer cevian-length feasibility after Stewart yields a square condition.

# M. Candidate mastery items
- recognition-only: choose Stewart vs median/angle-bisector/similarity route.
- first-line-only: write a correct variable map.
- full solve: solve one unknown cevian length.
- WHY-NOT: explain why Stewart is overkill in a direct right-triangle case.
- verification: substitute a simple coordinate triangle and check both sides numerically.

# N. Dependency declarations
REQUIRES: algebraic expansion; segment addition; triangle feasibility.
BRIDGE_REQUIRES: GEO-03 similarity retrieval for route comparison.
APPLIES: coordinate derivation as verification.
DOWNSTREAM MAY ASSUME: correct Stewart identity and special-case routing discipline.

# O. Lead integration notes
Place after median/Apollonius so the general theorem grows out of a special case. Emphasize route selection more than mnemonic. Keep the coordinate derivation concise and optional for learners; retain it teacher-side for verification.

# P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: authored Stewart numerical items still require independent key checks before integration.
