---
main_topic_id: IOQM-G9-ALG-04
microstream_id: W1-A
microstream_title: AP and GP recognition
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-04
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: AP/GP recognition by invariant, finite-prefix caution, and “neither” cases. Excluded: general polynomial theory and counting-state recurrence derivation.
## B. Learner-state model
PRIOR_KNOWLEDGE: arithmetic operations. LIKELY_HALF_KNOWLEDGE: pattern matching from first terms. MISSING_BRIDGES: invariant vs visual pattern. OWNERSHIP_TARGET: classify by constant difference/ratio only when justified.
## C. Mathematical invariant / governing structure
AP: `a_{n+1}-a_n` is constant. GP: `a_{n+1}/a_n` is constant where defined. A finite matching prefix does not determine the infinite rule without a definition.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| term list | candidate invariant | differences/ratios | enough terms/rule | visual pattern only |
| explicit formula | global structure | simplify difference/ratio | all n | infer from first terms |
| recurrence | generation rule | compare with AP/GP recurrence | initialization known | ignore initial data |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| AP vs GP | difference | ratio | which invariant is constant? | both may start smoothly |
| GP vs finite ratio coincidence | global rule | finite evidence | is continuation defined? | first ratios match |
| AP/GP vs neither | invariant | first-difference pattern | is the invariant actually constant? | named categories dominate |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG04-A-01
WRONG_MOVE: declare GP from three equal observed ratios.
WHY_TEMPTING: finite evidence resembles definition.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: classification requires a rule valid for all allowed indices.
FALSIFIER_OR_CONTRAST: change the next term while preserving the prefix.
## G. First-move cues
Term list: compute differences and ratios before naming the family.
## H. H3 -> H0 fading plan
H3: specify invariant to test. H2: cue difference/ratio. H1: ask what must stay constant. H0: changed-surface classification including “neither.”
## I. Validated IOQM source anchors
No anchor is promoted solely by this stream; topic anchors are verified in W1-G.
## J. Source-independent mathematical trace
Claims are definition-derived; no external numerical key is needed.
## K. Contrast-pair candidates
AP vs GP; GP vs finite-prefix coincidence; AP vs nonlinear first-difference pattern; explicit vs listed terms; invariant vs visual pattern.
## L. Transfer candidates
representation change; context-labelled sequence; hidden AP in finite differences; recurrence-to-classification; false-positive diagnosis.
## M. Candidate mastery items
recognition; first-line invariant; full classification; WHY-NOT finite-prefix proof; verification from explicit formula.
## N. Dependency declarations
REQUIRES: elementary algebra. BRIDGE_REQUIRES: none. APPLIES: later recurrence/transfer work. Downstream may assume difference/ratio classification discipline.
## O. Lead integration notes
Teach invariants once; keep internal H/T control labels out of student prose.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
