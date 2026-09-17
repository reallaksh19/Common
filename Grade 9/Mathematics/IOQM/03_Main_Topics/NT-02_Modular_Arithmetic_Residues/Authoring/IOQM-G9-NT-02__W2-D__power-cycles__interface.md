---
main_topic_id: IOQM-G9-NT-02
microstream_id: W2-D
microstream_title: Power cycles and periodic residue states
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-02
prerequisite_interfaces: [IOQM-G9-NT-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: detecting and using finite power cycles, exponent reduction under justified periodicity, and base/exponent state interactions. Excluded: advanced group-order theorems as required doctrine.
## B. Learner-state model
PRIOR_KNOWLEDGE: exponents and residues. LIKELY_HALF_KNOWLEDGE: tries to compute large powers or reduces exponents by a memorized number. MISSING_BRIDGE: the cycle must be observed/justified for the actual residue state. OWNERSHIP_TARGET: huge power -> finite cycle -> exponent position.
## C. Mathematical invariant / governing structure
For fixed base and modulus the sequence of residues is finite and eventually periodic; promoted problems use verified cycles. When the base state also changes, a universal period must preserve every relevant periodic component.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| power sequence modulo m | repeated state | list residues until repeat | fixed base/modulus | expand huge power |
| exponent modulo cycle length | cycle position | reduce exponent | justified cycle | reduce by m automatically |
| `n^n mod m` | coupled base/exponent states | separate base and exponent periods | handle zero states | use only exponent period |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| brute force vs cycle | compute small exponent | find repeating state | is exponent huge? | arithmetic feels direct |
| one-period vs coupled periods | reduce exponent | preserve base plus exponent state | does base depend on n? | exponent dominates notation |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT02-D-01
WRONG_MOVE: reduce every exponent modulo 6 in a mod-7 problem, including bases divisible by 7.
WHY_TEMPTING: nonzero residues often have periods dividing 6.
MISSING_LINK_CLASS: BOUNDARY
REPAIR_INVARIANT: zero-residue base states need separate handling.
FALSIFIER_OR_CONTRAST: `7^k mod 7` is always 0 and is not governed by a nonzero-residue inverse cycle.
## G. First-move cues
For a huge power, reduce the base, write only enough powers to see the cycle, then locate the exponent within that cycle.
## H. H3 -> H0 fading plan
H3: provide the residue list through the first repeat. H2: cue “find the cycle first.” H1: ask what state repeats. H0: changed base/modulus/exponent with no method label.
## I. Validated IOQM source anchors
`IOQM-2025-Q20` is the primary coupled-period anchor; `IOQM-2024-Q03` supplies a stabilizing power-residue example.
## J. Source-independent mathematical trace
Q20’s minimum universal period 42 is independently reconstructed from the need to preserve mod-7 base state and nonzero exponent period 6; proper divisors are rejected by collision/state checks.
## K. Contrast-pair candidates
cycle vs expansion; period vs modulus; nonzero vs zero base state; fixed base vs changing base.
## L. Transfer candidates
cyclic processes, finite automata intuition, last digits, recurrence-state compression.
## M. Candidate mastery items
find a cycle; compute a huge-power residue; justify exponent reduction; handle a zero base state; explain a coupled period.
## N. Dependency declarations
REQUIRES: W2-A/B. BRIDGE_REQUIRES: none beyond basic divisibility. APPLIES: W2-E last digits and downstream cyclic-state problems.
## O. Lead integration notes
Prefer explicit short cycles over theorem quotation. Use Q20 only after learners understand coupled state preservation.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: regenerate learner PDF after source-label repair
