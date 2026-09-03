---
main_topic_id: IOQM-G9-ALG-05
microstream_id: W1-A
microstream_title: Special values
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-05
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b]
source_cutoff: 2026-09-02
---

# A. Scope boundary
Own: zero/one and collapse substitutions. Retrieve generic substitution/equivalence from ALG-01. Exclude generic recurrence teaching and abstract function theory.

# B. Learner-state model
`PRIOR_KNOWLEDGE:` substitution, linear equations.  
`LIKELY_HALF_KNOWLEDGE:` random trials, sample-pattern guessing.  
`MISSING_BRIDGES:` legal-domain choice, structural payoff, global verification.  
`OWNERSHIP_TARGET:` choose and justify a function-equation-specific first move.

# C. Mathematical invariant / governing structure
`DOMAIN -> STRUCTURAL INPUT -> FORCED RELATION -> GLOBAL PROOF -> ORIGINAL CHECK`.  
If a product-like argument appears, test a legal 0 or 1 that makes it constant.

# D. Representation inventory
| Representation | Exposes | First move | Condition | Wrong choice |
|---|---|---|---|---|
| original FE | collapse/pair | inspect argument map | legal input | random value |
| `A=f(x),B=f(c-x)` | 2-value system | write partner | partner legal | guess formula |
| integer step | propagation | use 0/1 | cover negatives | assume real uniqueness |

# E. Decision boundaries
| Surface | A | B | Question | Trap |
|---|---|---|---|---|
| substitution | arbitrary | structural | what collapses most? | small feels useful |
| FE/recurrence | all-input | indexed step | what is original statement? | notation overlaps |
| values/formula | conjecture | proof | all inputs covered? | pattern looks decisive |

# F. Misconception/diagnosis catalogue
```text
ERROR_CODE: RANDOM_INPUT
WRONG_MOVE: convenient input with no structural effect.
WHY_TEMPTING: substitution is familiar.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: choose by what the input removes.
FALSIFIER_OR_CONTRAST: compare 7 with a zero-collapse input.
```
```text
ERROR_CODE: DOMAIN_OR_PROOF_LEAK
WRONG_MOVE: illegal input or finite-value formula claim.
WHY_TEMPTING: algebra/pattern is convenient.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: state domain; derive globally; verify original FE.
FALSIFIER_OR_CONTRAST: integer domain forbids 1/2; finite points do not determine a function.
```

# G. First-move cues
- If a product-like argument appears, test a legal 0 or 1 that makes it constant.
- State the domain before algebra.
- Stop once the target is forced.

# H. H3 -> H0 fading plan
H3 structural input supplied -> H2 structure named -> H1 visible clue only -> H0 changed-surface independent item.

# I. Validated IOQM source anchors
| ID | Year/Q | Status | Role | Mechanism | Figure | Key |
|---|---|---|---|---|---|---|
| IOQM-2025-Q14 | 2025 Q14 | CLEAN_OFFICIAL | primary | zero collapse | no | FINAL_OFFICIAL |
| IOQM-2024-Q16 | 2024 Q16 | CLEAN_OFFICIAL | primary | involution pair | no | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q14: on Z, `m=0 -> f(1)=2`; `n=0 -> f(m)=m+1`; sum `N(N+3)/2`; answer 12.  
Q16: on R, pair `x,3-x`; `7f(x)=x^2-24x+36`; requested difference 8. Keys agree; overlay not applicable.

# K. Contrast-pair candidates
Random/strategic; reflection/periodicity; FE/recurrence; conjecture/proof; integer/real domain.

# L. Transfer candidates
Changed reflection constant; changed product argument; integer step propagation; underdetermined reflection; constructive injectivity/surjectivity.

# M. Candidate mastery items
Recognition; first partner line; full paired solve; WHY-NOT finite data; candidate verification.

# N. Dependency declarations
`BRIDGE_REQUIRES` ALG-01. `REQUIRES` Grade-9 algebra/domain reading. `APPLIES` elementary elimination. Downstream may retrieve strategic FE substitution at this depth.

# O. Lead integration notes
Teach once: domain -> structural input -> pair/combine -> prove -> verify. Never expose microstream/hint/wave/owner/dependency controls in learner prose.

# P. Independent QA status
`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_AFFECTING_INTEGRATION`
