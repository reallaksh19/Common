---
main_topic_id: IOQM-G9-ALG-05
microstream_id: W1-C
microstream_title: Equation combinations
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-05
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b]
source_cutoff: 2026-09-02
---

# A. Scope boundary
Own: add/subtract/eliminate companion function values after strategic equations are created. Generic algebraic equivalence remains ALG-01; generic linear algebra is not expanded here.

# B. Learner-state model
`PRIOR_KNOWLEDGE:` solve two linear equations.  
`LIKELY_HALF_KNOWLEDGE:` solves for everything even when target is smaller.  
`MISSING_BRIDGES:` target-led equation combination.  
`OWNERSHIP_TARGET:` eliminate the unwanted function value with the cheapest legal combination.

# C. Mathematical invariant / governing structure
`CREATE THE RIGHT EQUATIONS -> COMBINE TARGET-FIRST -> STOP WHEN TARGET IS FORCED`.

# D. Representation inventory
| Representation | Exposes | First move | Condition | Wrong choice |
|---|---|---|---|---|
| two displayed relations | sum/difference | inspect coefficients | same inputs | substitute random values |
| partner pair | 2x2 system | name A,B | partner legal | guess formula |
| requested difference/value | direct linear combination | eliminate nuisance term | equivalent combination | solve unnecessary unknowns |

# E. Decision boundaries
| Surface | A | B | Question | Trap |
|---|---|---|---|---|
| add/subtract | add | subtract | which cancels the nuisance value? | mechanical choice |
| target/full formula | direct target | solve function | does target need full formula? | over-solving |
| equivalent/one-way | linear combination | unsafe division | is any divisor zero? | familiar algebra hides condition |

# F. Misconception/diagnosis catalogue
```text
ERROR_CODE: COMBINE_WITHOUT_TARGET
WRONG_MOVE: performs arbitrary row operations.
WHY_TEMPTING: two equations invite elimination.
MISSING_LINK_CLASS: EXECUTION
REPAIR_INVARIANT: choose the combination that removes the target's nuisance value.
FALSIFIER_OR_CONTRAST: compare a direct difference with solving A and B separately.
```
```text
ERROR_CODE: UNSAFE_DIVISION
WRONG_MOVE: divides by an expression without a nonzero check.
WHY_TEMPTING: algebra is routine.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: preserve zero branches or use addition/subtraction instead.
FALSIFIER_OR_CONTRAST: denominator may vanish at an allowed input.
```

# G. First-move cues
- Two equations in the same two function values -> name them and inspect coefficients.
- Target is a sum/difference -> try to manufacture it directly.
- Do not solve more than the question asks.

# H. H3 -> H0 fading plan
H3 combination supplied -> H2 nuisance value named -> H1 coefficients only -> H0 changed paired system requiring independent choice.

# I. Validated IOQM source anchors
| ID | Year/Q | Status | Role | Mechanism | Figure | Key |
|---|---|---|---|---|---|---|
| IOQM-2025-Q14 | 2025 Q14 | CLEAN_OFFICIAL | bridge | collapse then algebra | no | FINAL_OFFICIAL |
| IOQM-2024-Q16 | 2024 Q16 | CLEAN_OFFICIAL | primary | paired elimination | no | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Q16 companion equations form a nonsingular system and give `7f(x)=x^2-24x+36`, hence difference 8. Q14 gives `f(n)=n+1`, sum threshold 12. Official keys agree.

# K. Contrast-pair candidates
Add/subtract; target/full formula; paired solve/sample values; equivalent/unsafe division; equation combination/recurrence manipulation.

# L. Transfer candidates
Changed coefficient pairs; target sum instead of individual value; direct difference; reflection constant changes; underdetermined one-equation case.

# M. Candidate mastery items
Choose combination; write first elimination line; full paired solve; WHY-NOT over-solving; verify algebra/domain conditions.

# N. Dependency declarations
`BRIDGE_REQUIRES` ALG-01 equivalence. `REQUIRES` elementary simultaneous equations. Downstream may retrieve target-led companion-value elimination.

# O. Lead integration notes
Teach after partner-equation creation. Keep general algebra retrieval short. No microstream/hint/wave/owner codes in learner prose.

# P. Independent QA status
`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_AFFECTING_INTEGRATION`
