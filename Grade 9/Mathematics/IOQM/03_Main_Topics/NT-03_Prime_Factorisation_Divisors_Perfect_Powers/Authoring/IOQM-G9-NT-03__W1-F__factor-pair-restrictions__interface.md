---
main_topic_id: IOQM-G9-NT-03
microstream_id: W1-F
microstream_title: Factor-pair restrictions and extremal reconstruction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-03
prerequisite_interfaces: [NT01_Prerequisite_Interface.md]
source_cutoff: 2026-09-02
---
# A. Scope boundary
Includes complementary exponent allocation, coprime block allocation, factor-pair symmetry and smallest integer from divisor-count patterns. Excludes general Diophantine completeness, owned by NT-04.
# B. Learner-state model
`PRIOR_KNOWLEDGE:` factor pairs. `LIKELY_HALF_KNOWLEDGE:` enumerates pairs. `MISSING_BRIDGES:` exponent allocation and extremal order. `OWNERSHIP_TARGET:` structural finite allocation.
# C. Mathematical invariant / governing structure
For `xy=N`, exponent contributions add to those of N; with `gcd(x,y)=1`, every prime-power block goes wholly to one factor. Fixed exponent patterns are minimized by putting larger exponents on smaller primes.
# D. Representation inventory
| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| complementary exponents | all factor pairs | split a_i | xy=N | independent factors |
| block assignment | coprime pairs | assign p^a wholly | gcd=1 | split p across both |
| multiplicative partition of tau | exponent patterns | factor tau | fixed divisor count | search n sequentially |
| divisor pairing | below/above sqrt | pair d,N/d | positive N | enumerate |
# E. Decision boundaries
Ordered/unordered pairs; coprime/unrestricted pairs; compute tau/reconstruct least n; discrete factor minimum/continuous optimum. Ask which allocations are genuinely independent and whether order matters.
# F. Misconception/diagnosis catalogue
`ERROR_CODE: NT03-F-01; WRONG_MOVE: split p^a between coprime factors; WHY_TEMPTING: valid without gcd restriction; MISSING_LINK_CLASS: DISCRETE_FILTER; REPAIR_INVARIANT: shared p would make gcd>1; FALSIFIER_OR_CONTRAST: xy=2^6 with gcd=1.`
# G. First-move cues
`xy=N,gcd=1` -> whole blocks; "least n with tau(n)=K" -> factor K into `(a_i+1)`; "below sqrt" -> pair divisors.
# H. H3 -> H0 fading plan
H3 allocate one block; H2 identify ordered/unordered; H1 factor K; H0 changed-surface extremal reconstruction.
# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q25 | 2024 Q25 | CLEAN_OFFICIAL | primary | extremal square reserve | no | OFFICIAL_HBCSE_KEY |
| IOQM-2024-Q29 | 2024 Q29 | CLEAN_OFFICIAL | primary | divisor pairing | no | OFFICIAL_HBCSE_KEY |
| IOQM-2023-Q01 | 2023 Q01 | CLEAN_VALIDATED | bridge | square interval endpoints | no | HBCSE_LINKED_MTAI_EMBEDDED_KEY |
# J. Source-independent mathematical trace
Q25: seven squares sum 588; roots 24,23 impossible by reserve; 22 works. Q29: 487-259=228. Q01: endpoint square count max 29, min 7 ->22.
# K. Contrast-pair candidates
Ordered/unordered; coprime/unrestricted; tau compute/reconstruct; factor pairs/exponent patterns; continuous/discrete minima.
# L. Transfer candidates
Box side allocations, integer rectangles, divisor codes, extremal distinct powers.
# M. Candidate mastery items
Coprime pair count, least-n reconstruction, below-root count, WHY-NOT continuous optimization, verification.
# N. Dependency declarations
Requires FTA/divisor count; applies NT-01 gcd meaning. NT-04 consumes the frozen export for broader integer-case reconstruction.
# O. Lead integration notes
Teach structural allocation here, but route general finite-case Diophantine doctrine to NT-04.
# P. Independent QA status
`DERIVATIONS_CHECKED: PASS; PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS; SOURCE_IDS_VERIFIED: PASS; DEPENDENCY_CONFLICTS: NONE; OPEN_ISSUES: NONE`.
