---
main_topic_id: IOQM-G9-COMB-01
microstream_id: W1-A
microstream_title: Addition and multiplication principles
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-01
prerequisite_interfaces: []
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: disjoint alternatives and sequential stages. Excluded: generic recurrence/state evolution, graph-coloring canon and arithmetic digit-rule derivation.
## B. Learner-state model
PRIOR_KNOWLEDGE: basic factorial notation and informal counting. LIKELY_HALF_KNOWLEDGE: can apply formulas but may not define identity/cases. MISSING_BRIDGES: object definition, exact-one cases, restriction-first modeling. OWNERSHIP_TARGET: structure before formula.
## C. Mathematical invariant / governing structure
addition requires disjoint cases; multiplication requires valid stage counts after previous choices. The topic router is `DEFINE OBJECT -> IDENTITY/ORDER -> RESTRICTIONS -> CASES/STAGES -> DIRECT/COMPLEMENT/IE -> COUNT -> CHECK`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| object + identity rule | what is distinct | state equivalence | before counting | formula-first |
| case split | alternatives | test disjoint/exhaustive | exact-one branches | naive addition |
| stages | sequential choices | count choices per stage | later counts respect earlier choices | independent multiplication |
| complement/property sets | forbidden/overlap structure | define universe | same object universe | subtract unrelated counts |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| ordered vs unordered | arrangements/roles | subsets | does swapping selected elements change the object? | same chosen elements |
| direct vs complement | count desired | universe minus forbidden | which description is simpler? | direct wording feels mandatory |
| disjoint cases vs IE | add | repair overlap | can one object enter two cases? | both use addition signs |
| digit counting vs arithmetic | count known-valid strings | NT-05 | is the digit property being derived? | same decimal surface |
## F. Misconception/diagnosis catalogue
ERROR_CODE: COMB01-W1-A-01
WRONG_MOVE: write a factorial/binomial expression before defining the counted object and restrictions.
WHY_TEMPTING: familiar surface keywords.
MISSING_LINK_CLASS: MODEL_SELECTION
REPAIR_INVARIANT: define identity, then verify stages/cases before calculating.
FALSIFIER_OR_CONTRAST: two solutions with the same formula surface can differ because one is ordered and the other unordered.
## G. First-move cues
Name one object, decide identity/order, list active restrictions, then choose disjoint cases or sequential stages.
## H. H3 -> H0 fading plan
H3: object and case/stage model supplied. H2: object supplied, split withheld. H1: only the decisive identity/restriction cue. H0: changed surface with no method label.
## I. Validated IOQM source anchors
IOQM-2024-Q02. Exact source/key custody and independent routes are recorded in the source map and audit.
## J. Source-independent mathematical trace
Promoted counts are recomputed with a second route or small-case check where practical; IE signs and repeated-object multiplicities are explicitly audited.
## K. Contrast-pair candidates
ordered/unordered; disjoint/overlapping; direct/complement; distinct/repeated; counting/arithmetic digit structure.
## L. Transfer candidates
restricted assignments; subset statistics; finite-set counts; recurrence branch validation; graph/coloring restrictions.
## M. Candidate mastery items
recognition; first-line model; full count; WHY-NOT formula; overlap repair; changed-surface transfer.
## N. Dependency declarations
REQUIRES: elementary arithmetic/set language. BRIDGE_REQUIRES: arithmetic digit rules only when a problem requires deriving them. EXPORTS: stable counting/model semantics to COMB-02/03.
## O. Lead integration notes
Keep formulas subordinate to object identity, restrictions and exact-one reasoning. Retrieve the stable provider interface downstream rather than duplicating this chapter.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: exact current-source PDF render QA pending
