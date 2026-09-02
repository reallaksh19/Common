---
main_topic_id: IOQM-G9-NT-03
microstream_id: W1-E
microstream_title: Prime valuations and factorial capacity
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-03
prerequisite_interfaces: [NT01_Prerequisite_Interface.md]
source_cutoff: 2026-09-02
---
# A. Scope boundary
Includes `v_p`, product valuations, Legendre factorial valuation and prime-by-prime capacity. Excludes p-adic theory and generic modular arithmetic.
# B. Learner-state model
`PRIOR_KNOWLEDGE:` factorial/divisibility. `LIKELY_HALF_KNOWLEDGE:` expands or factors whole factorial. `MISSING_BRIDGES:` focus on one prime. `OWNERSHIP_TARGET:` automatic valuation comparison.
# C. Mathematical invariant / governing structure
Divisibility localizes prime-by-prime; in products valuations add. In `n!`, multiples of `p,p^2,...` contribute successive layers.
# D. Representation inventory
| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| `v_p(N)` | p multiplicity | isolate p | prime p | whole factorisation |
| Legendre sum | factorial capacity | floors n/p^j | factorial | compute n! |
| valuation comparison | divisibility | compare exponents | positive integers | decimal size |
# E. Decision boundaries
Factorial value vs valuation; valuation of product vs valuation of sum; divisibility capacity vs last-digit/cycle question. Ask whether only one prime's multiplicity matters.
# F. Misconception/diagnosis catalogue
`ERROR_CODE: NT03-E-01; WRONG_MOVE: use v_p(A+B)=v_p(A)+v_p(B); WHY_TEMPTING: product rule overgeneralized; MISSING_LINK_CLASS: DOMAIN_CONDITION; REPAIR_INVARIANT: additivity is for products; FALSIFIER_OR_CONTRAST: v_2(2+2)=2 but 1+1=2 only accidentally, use 2+6.`
# G. First-move cues
"divides n!" -> required prime valuations; "exponent of p in n!" -> Legendre floors.
# H. H3 -> H0 fading plan
H3 evaluate supplied floors; H2 choose p; H1 infer factorial capacity; H0 smallest nondivisor/constraint.
# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q01 | 2024 Q01 | CLEAN_OFFICIAL | primary | factorial capacity | no | OFFICIAL_HBCSE_KEY |
# J. Source-independent mathematical trace
1..10 divide 9!, while 11 does not; answer 11.
# K. Contrast-pair candidates
Factorial value/valuation; product/sum; Euclid/factorisation; divisibility/last digits; one-prime/all-prime checks.
# L. Transfer candidates
Trailing factors, factorial divisibility, multinomial products, prime-capacity bounds.
# M. Candidate mastery items
Compute valuation, first-line capacity, full divisor check, WHY-NOT factorial expansion, verification.
# N. Dependency declarations
Requires exponent vectors and NT-01 divisibility meaning. Downstream may assume valuation rules.
# O. Lead integration notes
Teach after squarefree/perfect powers so `v_p` notation has a clear purpose; keep formulas finite and Grade-9 appropriate.
# P. Independent QA status
`DERIVATIONS_CHECKED: PASS; PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS; SOURCE_IDS_VERIFIED: PASS; DEPENDENCY_CONFLICTS: NONE; OPEN_ISSUES: NONE`.
