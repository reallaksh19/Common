---
main_topic_id: IOQM-G9-NT-03
microstream_id: W1-A
microstream_title: FTA and prime exponent vectors
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-03
prerequisite_interfaces: [NT01_Prerequisite_Interface.md]
source_cutoff: 2026-09-02
---
# A. Scope boundary
Includes unique prime factorisation, exponent vectors, componentwise divisibility and valuation notation. Excludes Euclidean/gcd teaching (NT-01), modular arithmetic (NT-02) and Diophantine reconstruction (NT-04).
# B. Learner-state model
`PRIOR_KNOWLEDGE:` primes and factor trees. `LIKELY_HALF_KNOWLEDGE:` can factor small numbers but does not use multiplicity strategically. `MISSING_BRIDGES:` target -> exponent representation. `OWNERSHIP_TARGET:` automatic exponent-vector first move.
# C. Mathematical invariant / governing structure
Unique prime factorisation makes a positive integer uniquely determined by all prime exponents; equality/divisibility can therefore be checked prime-by-prime.
# D. Representation inventory
| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| factor tree | prime support | factor | moderate integer | stop before collecting powers |
| exponent vector | multiplicity | collect equal primes | positive integer | raw factor list |
| `v_p` | one-prime capacity | isolate p | prime p | treat valuation as additive on sums |
# E. Decision boundaries
| Similar surface | Route A | Route B | Question | Temptation |
|---|---|---|---|---|
| gcd target | Euclid/NT-01 | exponent vector | is multiplicity itself needed? | factorisation is familiar |
| equality vs divisibility | equal exponents | componentwise <= | must numbers equal or one fit in another? | same prime support |
| number vs representation | compute value | retain vector | what does target use? | premature multiplication |
# F. Misconception/diagnosis catalogue
`ERROR_CODE: NT03-A-01; WRONG_MOVE: ignore multiplicity; WHY_TEMPTING: prime set looks sufficient; MISSING_LINK_CLASS: REPRESENTATION; REPAIR_INVARIANT: exponents determine the integer; FALSIFIER_OR_CONTRAST: 2 and 2^5.`
# G. First-move cues
Prime-power product -> write exponent vector. Divisibility -> compare required exponents. One-prime capacity -> write `v_p`.
# H. H3 -> H0 fading plan
H3 collect powers; H2 choose vector; H1 state one exponent comparison; H0 changed-surface divisibility problem. Candidates independently checked.
# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q01 | 2024 Q01 | CLEAN_OFFICIAL | primary | prime-exponent capacity | no | OFFICIAL_HBCSE_KEY |
# J. Source-independent mathematical trace
All 1..10 divide 9!; prime 11 does not. Official answer 11 agrees.
# K. Contrast-pair candidates
Factor list/vector; gcd/valuation; same support/different multiplicity; equality/divisibility; computed integer/symbolic vector.
# L. Transfer candidates
Verbal divisibility -> vector; factorial capacity; factor-pair allocation; cross-domain product constraints.
# M. Candidate mastery items
Recognition, first-line vector, full divisibility solve, WHY-NOT prime-set-only, verification.
# N. Dependency declarations
`REQUIRES:` G9_CORE and NT-01 divisibility meaning. `APPLIES:` elementary counting later. Downstream may assume vector/divisibility equivalence.
# O. Lead integration notes
Teach FTA/vector once at chapter start; later streams retrieve it. Do not expose control-plane labels.
# P. Independent QA status
`DERIVATIONS_CHECKED: PASS; PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS; SOURCE_IDS_VERIFIED: PASS; DEPENDENCY_CONFLICTS: NONE; OPEN_ISSUES: NONE`.
