---
main_topic_id: IOQM-G9-ALG-05
microstream_id: W1-E
microstream_title: Justified injectivity and surjectivity
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-05
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b]
source_cutoff: 2026-09-02
---

# A. Scope boundary
Own: concrete equation-driven injectivity/surjectivity only when required by an IOQM-style solve. Exclude abstract function theory, inverse-function theory, continuity and monotonicity assumptions.

# B. Learner-state model
`PRIOR_KNOWLEDGE:` informal one-to-one/onto meaning.  
`LIKELY_HALF_KNOWLEDGE:` asserts injective from appearance or surjective from examples.  
`MISSING_BRIDGES:` equal-output proof and arbitrary-target construction.  
`OWNERSHIP_TARGET:` prove only the function property the equation actually supplies and the solution actually needs.

# C. Mathematical invariant / governing structure
Injective: `f(a)=f(b) -> use FE -> a=b`. Surjective: `target t arbitrary -> construct u -> f(u)=t`.

# D. Representation inventory
| Representation | Exposes | First move | Condition | Wrong choice |
|---|---|---|---|---|
| equal outputs | injectivity | assume `f(a)=f(b)` | equation compares them | assume increasing |
| arbitrary target | surjectivity | name `t` | construct legal input | test examples |
| nested `f(y)` input | composition access | choose x=0 or special x | real-domain legality | invoke inverse function |

# E. Decision boundaries
| Surface | A | B | Question | Trap |
|---|---|---|---|---|
| one-to-one | prove injective | assume monotone | does FE turn equal outputs into equal inputs? | graph intuition |
| onto | construct preimage | test outputs | can target t be parameterized? | samples |
| property/solution | prove needed fact | full function theory | does the solution use the property? | terminology invites theory |

# F. Misconception/diagnosis catalogue
```text
ERROR_CODE: INJECTIVE_ASSERTED
WRONG_MOVE: declares f injective without a derivation.
WHY_TEMPTING: candidate formula looks one-to-one.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: start with f(a)=f(b) and force a=b from the FE.
FALSIFIER_OR_CONTRAST: appearance is not a proof before the formula is known.
```
```text
ERROR_CODE: SURJECTIVE_BY_SAMPLES
WRONG_MOVE: checks several outputs and declares onto.
WHY_TEMPTING: target values appear easy to hit.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: choose arbitrary t and build a preimage.
FALSIFIER_OR_CONTRAST: finitely many outputs never cover R.
```

# G. First-move cues
- Need injectivity -> write `f(a)=f(b)`.
- Need surjectivity -> write `t` arbitrary and solve backward for an input.
- Never assume continuity, monotonicity, boundedness or an inverse unless given/proved.

# H. H3 -> H0 fading plan
H3 proof skeleton supplied -> H2 property named -> H1 nested-input clue only -> H0 changed equation requiring learner to decide whether the property is useful.

# I. Validated IOQM source anchors
| ID | Year/Q | Status | Role | Mechanism | Figure | Key |
|---|---|---|---|---|---|---|
| IOQM-2025-Q14 | 2025 Q14 | CLEAN_OFFICIAL | boundary | no injectivity needed | no | FINAL_OFFICIAL |
| IOQM-2024-Q16 | 2024 Q16 | CLEAN_OFFICIAL | boundary | no injectivity needed | no | OFFICIAL_HBCSE_KEY |

# J. Source-independent mathematical trace
Both historical anchors solve without injectivity/surjectivity, which confirms these properties are optional tools rather than required doctrine. For authored `f(x+f(y))=f(x)+y`, equal outputs force equal inputs; setting x=0 gives `f(f(y))=f(0)+y`, so arbitrary targets have explicit preimages.

# K. Contrast-pair candidates
Injective/surjective; proof/assumption; arbitrary target/examples; needed property/full theory; nested-input use/formula guessing.

# L. Transfer candidates
Changed nested-input equation; target construction on integers; equation where injectivity is unnecessary; false monotonicity temptation; compare equal outputs under a shifted input.

# M. Candidate mastery items
Prove injective; construct surjectivity; WHY-NOT monotonicity; decide property relevance; first-line-only equal-output setup.

# N. Dependency declarations
`BRIDGE_REQUIRES` ALG-01 proof/equivalence discipline. `REQUIRES` basic function language only as needed. Downstream may retrieve concrete equal-output/arbitrary-target proof patterns.

# O. Lead integration notes
Place late, after strategic substitutions are secure. Keep terminology operational, not abstract. No production-control labels in learner prose.

# P. Independent QA status
`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_AFFECTING_INTEGRATION`
