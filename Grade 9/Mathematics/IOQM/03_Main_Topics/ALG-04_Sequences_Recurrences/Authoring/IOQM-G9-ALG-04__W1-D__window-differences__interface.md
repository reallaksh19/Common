---
main_topic_id: IOQM-G9-ALG-04
microstream_id: W1-D
microstream_title: Window differences
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-04
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: adjacent equal-length window subtraction, periodicity and shifted inequalities. Excluded: general inequality optimization and unrelated averaging theory.
## B. Learner-state model
PRIOR_KNOWLEDGE: sums and inequalities. LIKELY_HALF_KNOWLEDGE: expands many windows instead of cancelling. MISSING_BRIDGES: neighboring-window subtraction. OWNERSHIP_TARGET: automatic local cancellation.
## C. Mathematical invariant / governing structure
For `W_i=a_i+...+a_{i+k-1}`, `W_{i+1}-W_i=a_{i+k}-a_i`. Equality or order of adjacent windows becomes a direct relation between terms k apart.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| rolling sum | shared terms | subtract neighbors | equal length | compute all sums |
| rolling average | same after multiplying by k | clear denominator then subtract | fixed k | compare averages termwise |
| equal windows | periodicity | cancel common terms | same length | assume constant sequence |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| adjacent vs nonadjacent windows | one cancellation | repeated relation | do windows overlap by k-1 terms? | all window sums look global |
| equal vs increasing windows | equality | inequality | what is the window comparison? | same algebraic surface |
| average vs sum | multiply by fixed k | direct sum | same window length? | averaging language hides cancellation |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG04-D-01
WRONG_MOVE: expand every rolling sum separately.
WHY_TEMPTING: problem is stated globally.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: subtract adjacent windows; common terms vanish.
FALSIFIER_OR_CONTRAST: aligned windows show only entering/leaving terms survive.
## G. First-move cues
Write two neighboring windows aligned and subtract before computing any term values.
## H. H3 -> H0 fading plan
H3: display both aligned windows. H2: cue “subtract neighbors.” H1: ask which terms enter/leave. H0: changed rolling-average context.
## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q26 | 2025 Q26 | HBCSE_OFFICIAL | primary | adjacent 4- and 7-term window inequalities | no | verified answer 10 |
## J. Source-independent mathematical trace
Independent reconstruction obtains `a_{i+4}>a_i` and `a_{i+7}<a_i` by adjacent subtraction and yields the verified maximum length 10.
## K. Contrast-pair candidates
window sum vs term relation; equal vs increasing windows; 4-window vs 7-window shifts; average vs sum; local cancellation vs brute force.
## L. Transfer candidates
sensor totals; moving averages; periodic equal windows; dual window inequalities; context change.
## M. Candidate mastery items
recognition; first-line subtraction; full periodicity proof; WHY-NOT brute expansion; source-style dual-window problem.
## N. Dependency declarations
REQUIRES: algebra and order. BRIDGE_REQUIRES: none. APPLIES: periodicity and source Q26. Downstream may assume adjacent-window cancellation.
## O. Lead integration notes
Use as the canonical high-index cancellation pattern; avoid importing general inequality doctrine.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
