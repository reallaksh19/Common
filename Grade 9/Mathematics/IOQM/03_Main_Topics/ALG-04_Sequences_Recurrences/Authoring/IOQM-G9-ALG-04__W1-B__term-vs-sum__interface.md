---
main_topic_id: IOQM-G9-ALG-04
microstream_id: W1-B
microstream_title: Term versus sum
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-04
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: partial sums, finite differences and conversion `a_n=S_n-S_{n-1}`. Excluded: continuous differentiation as a substitute and general series theory.
## B. Learner-state model
PRIOR_KNOWLEDGE: sums and algebra. LIKELY_HALF_KNOWLEDGE: confuses term and accumulated total. MISSING_BRIDGES: finite-difference extraction. OWNERSHIP_TARGET: automatically separate contribution from accumulation.
## C. Mathematical invariant / governing structure
If `S_n=a_1+...+a_n`, then `a_n=S_n-S_{n-1}` for n>=2, with `a_1=S_1`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| partial-sum formula | accumulation | subtract neighbors | n>=2 | treat S_n as a_n |
| cumulative context | total-to-date | current minus previous | ordered stages | divide by n |
| polynomial S_n | degree drop by finite difference | expand `S_n-S_{n-1}` | discrete n | differentiate |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| term vs sum | finite difference | direct substitution | does symbol denote cumulative total? | same index n |
| finite difference vs derivative | discrete identity | continuous operation | is n a sequence index? | both reduce degree |
| a_1 vs later terms | use S_1 | subtract S_0 if defined | is S_0 defined? | formula overgeneralization |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG04-B-01
WRONG_MOVE: set `a_n=S_n`.
WHY_TEMPTING: shared index.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: contribution equals change in accumulation.
FALSIFIER_OR_CONTRAST: compare `S_2=a_1+a_2` with `a_2`.
## G. First-move cues
Whenever cumulative/partial sums are given and a term is asked for, write `S_n-S_{n-1}`.
## H. H3 -> H0 fading plan
H3: provide subtraction identity. H2: cue neighboring totals. H1: ask “contribution or accumulation?” H0: changed cumulative context.
## I. Validated IOQM source anchors
No anchor is primary solely here; topic source custody remains W1-G.
## J. Source-independent mathematical trace
Identity follows by cancellation of `S_n-(a_1+...+a_{n-1})`.
## K. Contrast-pair candidates
term vs sum; contribution vs accumulation; finite difference vs derivative; formula vs recurrence for totals; S_1 vs S_n.
## L. Transfer candidates
layer cost from cumulative cost; daily contribution from running total; polynomial partial sums; recurrence for totals; representation switch.
## M. Candidate mastery items
recognition; first-line subtraction; full polynomial extraction; WHY-NOT differentiation; cumulative-context transfer.
## N. Dependency declarations
REQUIRES: algebra. BRIDGE_REQUIRES: none. APPLIES: AP recognition and recurrence transforms. Downstream may assume term/sum distinction.
## O. Lead integration notes
Teach early and retrieve throughout; do not label student work with internal control codes.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
