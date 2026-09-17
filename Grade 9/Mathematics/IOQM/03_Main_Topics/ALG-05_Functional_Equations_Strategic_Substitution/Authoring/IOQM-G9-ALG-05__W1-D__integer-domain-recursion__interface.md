---
main_topic_id: IOQM-G9-ALG-05
microstream_id: W1-D
microstream_title: Integer-domain propagation
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-05
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b]
source_cutoff: 2026-09-02
---

# A. Scope boundary
Own: integer-domain step rules produced by functional equations and their proof-completeness boundary. ALG-04 owns generic sequence/recurrence doctrine; ALG-01 owns generic equivalence.

# B. Learner-state model
`PRIOR_KNOWLEDGE:` integer substitution and simple recurrence reading.  
`LIKELY_HALF_KNOWLEDGE:` derives `f(n+1)` and treats it as the original problem.  
`MISSING_BRIDGES:` cover negative integers and verify the candidate in the all-pairs equation.  
`OWNERSHIP_TARGET:` use recurrence-like consequences without changing the canonical problem type.

# C. Mathematical invariant / governing structure
`INTEGER FE -> BASE VALUE -> UNIT STEP -> ALL INTEGER VALUES -> VERIFY ORIGINAL FE`.

# D. Representation inventory
| Representation | Exposes | First move | Condition | Wrong choice |
|---|---|---|---|---|
| all-pairs FE | global constraint | set 0/1/-1 | integer domain | import real theorem |
| step relation | propagation | establish base | cover negative direction | stop too early |
| candidate closed form | global check | substitute back | all integer pairs | trust table |

# E. Decision boundaries
| Surface | A | B | Question | Trap |
|---|---|---|---|---|
| FE/recurrence | all-pairs relation | derived step | which is original statement? | both use n |
| Z/R | integer propagation | real shift | can fractional classes vary? | extrapolate Z logic |
| formula/table | proof | conjecture | verified for all pairs? | several values match |

# F. Misconception/diagnosis catalogue
```text
ERROR_CODE: STEP_EQUALS_PROOF
WRONG_MOVE: stops after deriving f(n+1)-f(n).
WHY_TEMPTING: the step computes values.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: verify the candidate in the original two-variable FE.
FALSIFIER_OR_CONTRAST: an unrelated recurrence can share the same first terms.
```
```text
ERROR_CODE: NEGATIVE_GAP
WRONG_MOVE: proves only nonnegative integers.
WHY_TEMPTING: forward stepping is easy.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: derive a backward step or substitute negative integers directly.
FALSIFIER_OR_CONTRAST: the stated domain is all Z.
```

# G. First-move cues
- On Z, test 0 for the base value and 1/-1 for a step.
- State how negative integers are covered.
- Substitute the final candidate into the original FE.

# H. H3 -> H0 fading plan
H3 base+step supplied -> H2 one special input supplied -> H1 integer-domain cue -> H0 changed two-variable FE requiring full propagation and verification.

# I. Validated IOQM source anchors
| ID | Year/Q | Status | Role | Mechanism | Figure | Key |
|---|---|---|---|---|---|---|
| IOQM-2025-Q14 | 2025 Q14 | CLEAN_OFFICIAL | primary | integer special inputs | no | FINAL_OFFICIAL |
| IOQM-2024-Q16 | 2024 Q16 | CLEAN_OFFICIAL | contrast | real paired equations | no | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q14 uses legal integer zero substitutions to derive `f(m)=m+1` directly; threshold answer 12. Authored integer equations independently yield `n^2` or `n(n+1)/2` and verify on all integer pairs. Q16 answer 8 provides the real-domain contrast.

# K. Contrast-pair candidates
FE/recurrence; integer/real shift; forward/backward propagation; candidate/verification; direct special input/long recursion.

# L. Transfer candidates
Quadratic additive corrections; difference equation `m-n`; changed initial value; real shift underdetermination; recurrence consequence as WHY-NOT.

# M. Candidate mastery items
Derive base; derive unit step; cover negatives; full formula+substitution; explain why recurrence consequence alone is incomplete.

# N. Dependency declarations
`BRIDGE_REQUIRES` ALG-01. `APPLIES` minimal recurrence notation from school knowledge; no ALG-04 reteaching. Downstream may retrieve integer FE propagation and proof boundary.

# O. Lead integration notes
Place after special-value and pairing mechanisms. Make the FE-vs-recurrence contrast explicit. Never expose production control labels in learner prose.

# P. Independent QA status
`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_AFFECTING_INTEGRATION`
