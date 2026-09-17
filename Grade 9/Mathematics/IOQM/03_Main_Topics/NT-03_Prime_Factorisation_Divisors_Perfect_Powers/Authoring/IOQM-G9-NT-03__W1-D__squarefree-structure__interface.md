---
main_topic_id: IOQM-G9-NT-03
microstream_id: W1-D
microstream_title: Squarefree structure
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-03
prerequisite_interfaces: [NT01_Prerequisite_Interface.md]
source_cutoff: 2026-09-02
---
# A. Scope boundary
Includes squarefree exponent criterion, squarefree divisors, squarefree kernel and prime-structure forcing. Excludes Mobius/sieve theory.
# B. Learner-state model
`PRIOR_KNOWLEDGE:` prime factors. `LIKELY_HALF_KNOWLEDGE:` interprets squarefree as merely nonsquare. `MISSING_BRIDGES:` exponent <=1. `OWNERSHIP_TARGET:` detect repeated prime factors immediately.
# C. Mathematical invariant / governing structure
Squarefree iff every prime exponent is 0 or 1; equivalently no `p^2` divides the integer.
# D. Representation inventory
| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| exponent vector | repeated primes | test a_i<=1 | integer | test only whether square |
| subset of prime support | squarefree divisors | choose primes | divisor of fixed N | choose exponent sizes |
| squarefree kernel | odd-exponent residue | multiply odd-exponent primes | kernel target | radical approximation |
# E. Decision boundaries
Nonsquare vs squarefree; squarefree number vs squarefree divisor; distinct prime count vs total exponent sum. Ask whether any exponent can reach 2.
# F. Misconception/diagnosis catalogue
`ERROR_CODE: NT03-D-01; WRONG_MOVE: declare every nonsquare squarefree; WHY_TEMPTING: names sound complementary; MISSING_LINK_CLASS: INVARIANT; REPAIR_INVARIANT: no prime square may divide; FALSIFIER_OR_CONTRAST: 12 is nonsquare but not squarefree.`
# G. First-move cues
"not divisible by square of any prime" -> `a_i<=1`; squarefree divisor -> choose subset of prime support.
# H. H3 -> H0 fading plan
H3 inspect factored number; H2 factor then inspect; H1 translate verbal condition; H0 structural triple/large expression.
# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2023-Q09 | 2023 Q09 | CLEAN_VALIDATED | primary | prime/squarefree forcing | no | HBCSE_LINKED_MTAI_EMBEDDED_KEY |
| IOQM-2024-Q28 | 2024 Q28 | CLEAN_OFFICIAL | primary | squarefree expression | no | OFFICIAL_HBCSE_KEY |
# J. Source-independent mathematical trace
2023-Q09 gives 14+3=17 structural cases. 2024-Q28: n=20 expression is squarefree; every 21..29 has a squared prime factor -> 20.
# K. Contrast-pair candidates
Square/squarefree; nonsquare/squarefree; prime/semiprime; support/multiplicity; squarefree divisor/arbitrary divisor.
# L. Transfer candidates
Digit products, product constraints, divisor subsets, expression factorisation.
# M. Candidate mastery items
Recognition, squarefree divisor count, full structural case split, WHY-NOT nonsquare test, verification.
# N. Dependency declarations
Requires FTA/vector. Applies elementary subset counting. Downstream may assume squarefree criterion.
# O. Lead integration notes
Place immediately after perfect powers to exploit the contrast; avoid advanced number-theory notation.
# P. Independent QA status
`DERIVATIONS_CHECKED: PASS; PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS; SOURCE_IDS_VERIFIED: PASS; DEPENDENCY_CONFLICTS: NONE; OPEN_ISSUES: NONE`.
