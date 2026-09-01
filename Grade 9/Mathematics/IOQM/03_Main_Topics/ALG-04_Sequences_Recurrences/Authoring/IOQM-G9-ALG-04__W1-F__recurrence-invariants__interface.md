---
main_topic_id: IOQM-G9-ALG-04
microstream_id: W1-F
microstream_title: Recurrence invariants and Cassini-type relations
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-04
prerequisite_interfaces: [IOQM-G9-ALG-04__W1-C__recurrence-reading__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: transformed quantities such as `D_n=a_n^2-a_{n-1}a_{n+1}`, neighboring-index scaling and high-index cancellation. Excluded: prime-power divisor-count doctrine, canonically owned by NT-03.
## B. Learner-state model
PRIOR_KNOWLEDGE: second-order recurrence reading and algebra. LIKELY_HALF_KNOWLEDGE: tries to compute huge terms. MISSING_BRIDGES: choose a low-dimensional invariant from the target. OWNERSHIP_TARGET: derive recurrence for the target expression itself.
## C. Mathematical invariant / governing structure
For the recurrence `b_{n+2}=-4b_{n+1}-7b_n`, the Cassini-type quantity `D_n=b_n^2-b_{n-1}b_{n+1}` satisfies `D_{n+1}=7D_n`; with `D_1=1`, `D_n=7^(n-1)`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| high-index determinant-like target | cancellation | define D_n | second-order recurrence | compute b_n |
| recurrence for D_n | geometric scaling | compare D_{n+1}/D_n | derived identity | import unrelated number theory |
| prime-power result | algebraic endpoint | stop at `7^(n-1)` in ALG-04 | authored ALG-04 item | count divisors before NT-03 |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| raw iteration vs invariant | transformed target | term computation | does target combine neighboring terms? | recurrence invites iteration |
| ALG-04 finish vs NT-03 finish | obtain prime power | divisor-count doctrine | what concept owns the requested finish? | source anchor contains both |
| invariant guess vs proof | derive symbolically | test examples | is relation claimed for all n? | numerical checks are easy |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG04-F-01
WRONG_MOVE: teach the prime-power divisor-count rule to finish a new ALG-04 item.
WHY_TEMPTING: the historical anchor asks for a divisor count.
MISSING_LINK_CLASS: PREREQUISITE
REPAIR_INVARIANT: ALG-04 owns the recurrence invariant through `D_n=7^(n-1)`; NT-03 owns divisor-count doctrine.
FALSIFIER_OR_CONTRAST: a student can complete the repaired item without any factor-count theorem.
## G. First-move cues
When the target already combines three neighboring recurrence terms, define that target expression at a general index and compare neighboring values.
## H. H3 -> H0 fading plan
H3: provide D_n. H2: cue neighboring target expressions. H1: ask what quantity appears in the target. H0: changed recurrence/invariant item that stops at the algebraic result.
## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2023-Q10 | 2023 Q10 | HBCSE_LINKED_MTAI | primary invariant anchor; NT-03 bridge at final divisor count | determinant invariant | no | verified answer 51 |
## J. Source-independent mathematical trace
Independent audit derives `D_{n+1}=7D_n`, obtains the required prime power, and confirms the historical official answer. In newly authored ALG-04 Practice #14 and mastery #9, the task now stops at `D_20=7^19`; no divisor-count rule is taught.
## K. Contrast-pair candidates
raw terms vs target invariant; invariant derivation vs numerical testing; algebraic prime power vs divisor-count finish; supplied recurrence vs counting recurrence; local transformation vs brute force.
## L. Transfer candidates
machine-reading Q_n; different second-order coefficients; invariant ratio; high-index target; cross-topic handoff to NT-03.
## M. Candidate mastery items
recognition of invariant target; first-line D_n definition; full derivation; WHY-NOT raw iteration; ownership-boundary explanation.
## N. Dependency declarations
REQUIRES: recurrence reading and algebra. BRIDGE_REQUIRES: none for invariant. APPLIES: high-index cancellation. NT-03 is required only if a downstream task asks for divisor count of the resulting prime power.
## O. Lead integration notes
Preserve the historical anchor but do not make its NT-03 finish a prerequisite for ALG-04 practice/mastery. This repaired boundary is mandatory.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE_AFTER_REPAIR
OPEN_ISSUES: current student PDF must be regenerated after source repair
