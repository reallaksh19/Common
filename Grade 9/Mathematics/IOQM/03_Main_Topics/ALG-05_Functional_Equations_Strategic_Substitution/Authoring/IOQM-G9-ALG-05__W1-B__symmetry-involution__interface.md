---
main_topic_id: IOQM-G9-ALG-05
microstream_id: W1-B
microstream_title: Symmetry and involution
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-05
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b]
source_cutoff: 2026-09-02
---

# A. Scope boundary
Own: reflection/involution partner substitutions. Retrieve generic substitution/equivalence from ALG-01. Exclude periodicity theory, generic recurrence teaching and abstract function theory.

# B. Learner-state model
`PRIOR_KNOWLEDGE:` substitution, linear equations.  
`LIKELY_HALF_KNOWLEDGE:` notices `c-x` but does not reapply it.  
`MISSING_BRIDGES:` recognize self-returning partner map and manufacture the second equation.  
`OWNERSHIP_TARGET:` pair a function value with its involutive companion.

# C. Mathematical invariant / governing structure
`DOMAIN -> PARTNER MAP -> SECOND EQUATION -> ELIMINATION -> CHECK`.  
If `f(c-x)` appears, write the equation at `c-x` and verify that applying the map twice returns to `x`.

# D. Representation inventory
| Representation | Exposes | First move | Condition | Wrong choice |
|---|---|---|---|---|
| `x <-> c-x` | involution | apply partner | domain closed | call it periodic |
| `A=f(x),B=f(c-x)` | 2-value system | write both equations | determinant nonzero when solving | guess formula |
| target difference | direct elimination | combine target-first | equivalent algebra | derive unnecessary full theory |

# E. Decision boundaries
| Surface | A | B | Question | Trap |
|---|---|---|---|---|
| `f(c-x)` | reflection | periodicity | does two applications return x? | repeated form looks periodic |
| one equation | underdetermined | paired system | does partner create second equation? | sample values feel easier |
| full formula/target | solve all | eliminate target | what is actually requested? | over-solving |

# F. Misconception/diagnosis catalogue
```text
ERROR_CODE: PARTNER_NOT_WRITTEN
WRONG_MOVE: keeps one equation in two companion values.
WHY_TEMPTING: equation looks complete.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: apply the involution once more.
FALSIFIER_OR_CONTRAST: x -> c-x -> x closes the pair.
```
```text
ERROR_CODE: REFLECTION_AS_PERIOD
WRONG_MOVE: assumes f(x)=f(c-x) or periodicity.
WHY_TEMPTING: same two arguments recur.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: the map relates inputs; it does not assert equal outputs.
FALSIFIER_OR_CONTRAST: the source anchor has unequal companion values in general.
```

# G. First-move cues
- `f(c-x)` beside `f(x)` -> replace `x` by `c-x`.
- Confirm the partner is legal in the stated domain.
- Name the two function values only if it simplifies elimination.

# H. H3 -> H0 fading plan
H3 partner map supplied -> H2 reflection constant highlighted -> H1 only `f(c-x)` clue -> H0 changed coefficients/constant with no cue.

# I. Validated IOQM source anchors
| ID | Year/Q | Status | Role | Mechanism | Figure | Key |
|---|---|---|---|---|---|---|
| IOQM-2025-Q14 | 2025 Q14 | CLEAN_OFFICIAL | bridge | special input | no | FINAL_OFFICIAL |
| IOQM-2024-Q16 | 2024 Q16 | CLEAN_OFFICIAL | primary | `x <-> 3-x` | no | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q16: on R, pair the equations at `x` and `3-x`; solve `3A+4B=x^2`, `4A+3B=(3-x)^2`; obtain `7f(x)=x^2-24x+36`; requested difference is 8. Q14 independently gives 12. Keys agree; overlay not applicable.

# K. Contrast-pair candidates
Reflection/periodicity; partner equation/sample table; paired solve/formula guess; target elimination/full solve; real-domain partner/integer legality.

# L. Transfer candidates
`4-x`, `5-x`, and `1-x` partners; unequal coefficients; underdetermined single reflection identity; target-only elimination.

# M. Candidate mastery items
Recognize involution; write partner line; solve 2x2 companion system; WHY-NOT periodicity; evaluate target without guessing.

# N. Dependency declarations
`BRIDGE_REQUIRES` ALG-01. `REQUIRES` elementary elimination. `APPLIES` domain closure under affine reflection. Downstream may retrieve involution pairing.

# O. Lead integration notes
Teach the partner-map idea once before repeated paired examples. Do not expose owner/microstream/hint/wave controls or abstract symmetry theory in learner prose.

# P. Independent QA status
`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_AFFECTING_INTEGRATION`
