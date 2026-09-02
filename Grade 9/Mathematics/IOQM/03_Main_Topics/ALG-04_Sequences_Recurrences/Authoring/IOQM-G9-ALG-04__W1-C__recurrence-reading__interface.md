---
main_topic_id: IOQM-G9-ALG-04
microstream_id: W1-C
microstream_title: Recurrence reading and verification
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-04
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: recurrence notation, initialization, valid index range, symbolic verification and explicit-vs-recursive distinction. Excluded: combinatorial derivation of counting recurrences (COMB-03).
## B. Learner-state model
PRIOR_KNOWLEDGE: substitution. LIKELY_HALF_KNOWLEDGE: can iterate but omits initial data or proves formulas by examples. MISSING_BRIDGES: recurrence as rule plus sufficient starting state. OWNERSHIP_TARGET: read and verify supplied recurrences correctly.
## C. Mathematical invariant / governing structure
A recurrence does not determine a sequence without enough initial values and a valid index range. A proposed explicit form is verified by checking all required initials and the recurrence symbolically for every allowed index.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| recurrence + initials | generation rule | record order and initials | valid range given | ignore initialization |
| explicit formula | direct access | substitute target n | formula established | iterate unnecessarily |
| proposed closed form | verification target | initials + symbolic recurrence | same range | check first few terms only |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| explicit vs recursive | direct evaluate | generate/transform | is a_n directly in n? | both use subscripts |
| examples vs proof | finite check | symbolic identity | claim for all n? | examples are persuasive |
| supplied vs derived recurrence | algebraic use | modelling proof | was recurrence justified by the context? | familiar Fibonacci form |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG04-C-01
WRONG_MOVE: prove recurrence solution by matching five terms.
WHY_TEMPTING: local agreement.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: initials plus symbolic recurrence verification.
FALSIFIER_OR_CONTRAST: another sequence can share a finite prefix then diverge.
## G. First-move cues
Write the recurrence order, required initials and valid starting index before computation.
## H. H3 -> H0 fading plan
H3: state full verification checklist. H2: cue initials and symbolic check. H1: ask whether finite examples prove all n. H0: changed recurrence/formula verification.
## I. Validated IOQM source anchors
`IOQM-2023-Q10` is a verified recurrence/invariant anchor; exact custody is in W1-G.
## J. Source-independent mathematical trace
The recurrence-verification principle is definition-level. Q10's promoted arithmetic is independently checked in the source map.
## K. Contrast-pair candidates
explicit vs recursive; enough vs insufficient initials; examples vs proof; supplied recurrence vs counting-model derivation; raw iteration vs transform.
## L. Transfer candidates
machine readings; cumulative recurrence; tiling claim boundary; explicit candidate verification; initialization diagnosis.
## M. Candidate mastery items
recognition of missing initial value; first-line range statement; full verification; WHY-NOT finite testing; ownership-boundary item.
## N. Dependency declarations
REQUIRES: algebra and sequence notation. BRIDGE_REQUIRES: none. APPLIES: all recurrence streams. Downstream COMB-03 may rely on notation/verification, not modelling ownership.
## O. Lead integration notes
Export recurrence notation semantics through `ALG04_Recurrence_Interface_v1.md`; keep counting-state derivation outside ALG-04.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
