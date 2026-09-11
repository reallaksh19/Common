---
main_topic_id: IOQM-G9-NT-03
microstream_id: W1-B
microstream_title: Divisor counting and divisor parity
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-03
prerequisite_interfaces: [NT01_Prerequisite_Interface.md]
source_cutoff: 2026-09-02
---
# A. Scope boundary
Includes divisor exponent choices, `tau`, square-divisor counts, divisor pairing and parity. Excludes generic combinatorics and factorial valuations.
# B. Learner-state model
`PRIOR_KNOWLEDGE:` factors. `LIKELY_HALF_KNOWLEDGE:` can list divisors. `MISSING_BRIDGES:` independent exponent choices and pairing. `OWNERSHIP_TARGET:` count without enumeration.
# C. Mathematical invariant / governing structure
For `n=prod p_i^a_i`, a divisor independently chooses exponent `0..a_i`; hence `tau(n)=prod(a_i+1)`. Pairing `d` with `n/d` leaves a fixed point exactly when n is a square.
# D. Representation inventory
| Representation | Exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| exponent ranges | divisor choices | write 0..a_i | divisor target | list divisors |
| product formula | total count | multiply choice counts | independent ranges | add counts |
| divisor pairs | parity/below-root | pair d,n/d | positive n | enumerate |
# E. Decision boundaries
Divisor count vs factor-pair count; all divisors vs square divisors; odd tau vs explicit enumeration. Discriminating question: what restriction is imposed on divisor exponents or on pairing?
# F. Misconception/diagnosis catalogue
`ERROR_CODE: NT03-B-01; WRONG_MOVE: add exponent counts; WHY_TEMPTING: each prime is considered separately; MISSING_LINK_CLASS: INVARIANT; REPAIR_INVARIANT: choices combine multiplicatively; FALSIFIER_OR_CONTRAST: divisors of 2^2*3.`
# G. First-move cues
"number of divisors" -> `prod(a_i+1)`; "square divisors" -> count even exponents; "odd number of divisors" -> test square.
# H. H3 -> H0 fading plan
H3 supplied formula; H2 exponent ranges; H1 parity cue; H0 divisor-symmetry transfer.
# I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q29 | 2024 Q29 | CLEAN_OFFICIAL | primary | divisor symmetry | no | OFFICIAL_HBCSE_KEY |
| IOQM-2023-Q30 | 2023 Q30 | CLEAN_VALIDATED | primary | divisor parity | no | HBCSE_LINKED_MTAI_EMBEDDED_KEY |
# J. Source-independent mathematical trace
2024-Q29: `tau(n^2)=975`, 487 below n, subtract 259 proper divisors of n -> 228 -> 28. 2023-Q30: `d(i)` odd iff i square; count gives r=990, digit sum 18.
# K. Contrast-pair candidates
Listing/counting; divisor/factor pair; square divisor/arbitrary divisor; tau parity/tau value; below-root/full set.
# L. Transfer candidates
Divisor codes, symmetry around sqrt, cumulative parity, reconstruction from tau.
# M. Candidate mastery items
Count, first-line, pairing proof, WHY-NOT enumeration, changed-surface below-root count.
# N. Dependency declarations
Requires exponent vectors. Applies elementary multiplication principle only. Downstream may assume tau and parity theorem.
# O. Lead integration notes
Teach formula and pairing once, then retrieve in perfect-power/extremal sections.
# P. Independent QA status
`DERIVATIONS_CHECKED: PASS; PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS; SOURCE_IDS_VERIFIED: PASS; DEPENDENCY_CONFLICTS: NONE; OPEN_ISSUES: NONE`.
