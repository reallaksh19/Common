---
main_topic_id: IOQM-G9-NT-03
microstream_id: W1-C
microstream_title: Perfect squares, cubes and k-th powers
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-03
prerequisite_interfaces: [NT01_Prerequisite_Interface.md]
source_cutoff: 2026-09-02
---
# A. Scope boundary
Includes exponent criteria for squares/cubes/k-th powers, greatest power exponent and minimal multiplier/divisor. Excludes radical-equation and general exponential-equation canon.
# B. Learner-state model
`PRIOR_KNOWLEDGE:` familiar squares/cubes. `LIKELY_HALF_KNOWLEDGE:` numerical recognition only. `MISSING_BRIDGES:` exponent divisibility. `OWNERSHIP_TARGET:` translate perfect power to exponent congruence/divisibility.
# C. Mathematical invariant / governing structure
`prod p_i^a_i` is a perfect k-th power iff k divides every a_i; greatest k is gcd of the exponents.
# D. Representation inventory
| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| exponent vector | power divisibility | inspect a_i | positive integer | approximate roots |
| exponent deficits | minimal multiplier | raise to next multiple | multiplication allowed | rebuild number |
| difference of squares | two-square gap | factor difference | square difference | enumerate squares |
# E. Decision boundaries
Square vs cube; perfect-power membership vs least multiplier; difference of squares vs generic Diophantine. Ask which exponent modulus or factorisation the target imposes.
# F. Misconception/diagnosis catalogue
`ERROR_CODE: NT03-C-01; WRONG_MOVE: use even exponents for every perfect power; WHY_TEMPTING: squares dominate prior examples; MISSING_LINK_CLASS: RECOGNITION; REPAIR_INVARIANT: k must divide every exponent; FALSIFIER_OR_CONTRAST: 2^6*3^3 is cube but not square.`
# G. First-move cues
Square -> all a_i even; cube -> 3|a_i; greatest k -> gcd exponents; fixed square difference -> factor `A^2-B^2`.
# H. H3 -> H0 fading plan
H3 test supplied vector; H2 choose exponent criterion; H1 recognize deficit; H0 changed-surface square/cube constraint.
# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q06 | 2025 Q06 | CLEAN_OFFICIAL | primary | square gap + next cube | no | FINAL_OFFICIAL |
# J. Source-independent mathematical trace
`u^2-v^2=13` -> `(u,v)=(7,6)` -> age 49 -> next cube 64 -> answer 15.
# K. Contrast-pair candidates
Square/cube; square/squarefree; membership/minimal multiplier; exponent gcd/numerical root; perfect power/nearby integer.
# L. Transfer candidates
Age gap, area/product, code exponents, minimal repair, cross-domain factorisation.
# M. Candidate mastery items
Recognition, first-line exponent condition, minimal multiplier full solve, WHY-NOT numerical guessing, verification.
# N. Dependency declarations
Requires exponent vectors; applies difference of squares from G9 algebra; downstream may assume perfect-power criteria.
# O. Lead integration notes
Teach after divisor counting; keep difference-of-squares use narrow and do not absorb NT-04.
# P. Independent QA status
`DERIVATIONS_CHECKED: PASS; PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS; SOURCE_IDS_VERIFIED: PASS; DEPENDENCY_CONFLICTS: NONE; OPEN_ISSUES: NONE`.
