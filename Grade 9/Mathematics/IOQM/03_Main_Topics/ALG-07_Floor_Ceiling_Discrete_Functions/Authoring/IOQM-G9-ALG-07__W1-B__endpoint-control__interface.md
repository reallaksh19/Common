---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-B
microstream_title: Endpoint control
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: [IOQM-G9-ALG-07__W1-A__definition-order__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: open/closed endpoint discipline for floor/ceiling intervals and endpoint checking. Excluded: general inequality optimization (ALG-02) and integer-count formulas (W1-F).

## B. Learner-state model
PRIOR_KNOWLEDGE: interval notation.
LIKELY_HALF_KNOWLEDGE: can solve inequalities but ignores strictness.
MISSING_BRIDGES: preserving endpoint status through algebra.
OWNERSHIP_TARGET: reliable half-open endpoint control.

## C. Mathematical invariant / governing structure
Floor intervals are left-closed/right-open; ceiling intervals are left-open/right-closed. Algebraic transformations must preserve the encoded inclusion/exclusion.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| brackets | endpoint inclusion | mark before solving | ordered interval | make both closed |
| inequalities | strict/non-strict side | copy signs exactly | valid transformation | normalize signs by habit |
| number line | admissibility | test boundary values | final interval | skip endpoint audit |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| floor lower/upper endpoint | include lower | exclude upper | which bound comes from `<=`? | visual symmetry |
| ceiling lower/upper endpoint | exclude lower | include upper | which bound comes from `<`? | visual symmetry |
| transformed inequality | preserve status | flip on negative multiplier | did inequality direction change? | routine manipulation |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-B-01
WRONG_MOVE: convert `[a,b)` to `[a,b]` after solving.
WHY_TEMPTING: endpoints look secondary.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: endpoint status is part of the floor/ceiling definition.
FALSIFIER_OR_CONTRAST: test the excluded endpoint directly.

## G. First-move cues
Before algebra, annotate which endpoint is strict. After algebra, test any transformed boundary that could be ambiguous.

## H. H3 -> H0 fading plan
H3: brackets supplied. H2: cue “one endpoint is strict.” H1: ask which endpoint belongs. H0: mixed floor/ceiling endpoint problem.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q21 | 2024 Q21 | HBCSE_OFFICIAL | bridge | intersect floor-generated integer intervals | no | verified |
| IOQM-2024-Q26 | 2024 Q26 | HBCSE_OFFICIAL | primary | interval feasibility with closed/open endpoints | no | verified |

## J. Source-independent mathematical trace
The topic source audit independently verifies Q21=91 and Q26=33; endpoint feasibility is explicitly checked in both reconstructions.

## K. Contrast-pair candidates
floor vs ceiling endpoints; `[a,b)` vs `(a,b]`; boundary test passes vs fails; real interval vs integer endpoint; sign-preserving vs sign-flipping transformation.

## L. Transfer candidates
T2 interval notation; T2 number-line verification; T3 counting labels at a boundary; T3 shifted interval; T4 endpoint audit after NT/COMB filtering.

## M. Candidate mastery items
Recognition of correct brackets; first-line endpoint annotation; full solve with transformed endpoints; WHY-NOT for including excluded endpoint; verification by substitution.

## N. Dependency declarations
REQUIRES: W1-A definition interface. BRIDGE_REQUIRES: elementary inequalities. APPLIES: interval notation. Downstream may assume exact endpoint discipline.

## O. Lead integration notes
Teach immediately after definitions; retrieve during equations and integer counting. Do not expose control codes in student prose.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
