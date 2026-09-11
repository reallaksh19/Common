---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-F
microstream_title: Integer filtering and counting
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: [IOQM-G9-ALG-07__W1-A__definition-order__interface.md, IOQM-G9-ALG-07__W1-B__endpoint-control__interface.md, IOQM-G9-ALG-07__W1-E__equations-inequalities__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: solve a real interval, intersect with integers, count admissible integers, audit endpoints. Excluded: general combinatorial counting and congruence canon.

## B. Learner-state model
PRIOR_KNOWLEDGE: integers, interval notation.
LIKELY_HALF_KNOWLEDGE: mixes integer filtering into inequality solving and rounds endpoints inconsistently.
MISSING_BRIDGES: two-stage real-solve then discrete-filter workflow.
OWNERSHIP_TARGET: reliable conversion from continuous interval to integer solution set/count.

## C. Mathematical invariant / governing structure
First determine the real interval. Only then intersect with `Z`. For `[a,b)`, the first admissible integer is `ceil(a)` and the last is `ceil(b)-1`; count by verified first/last candidates rather than ad hoc rounding.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| real interval | continuous feasibility | solve fully | real target stage | enumerate early |
| integer set | discrete candidates | intersect with `Z` | integer target | round both endpoints same way |
| first/last integer | count | compute endpoints explicitly | nonempty interval | use length of real interval |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| real vs integer solutions | keep continuum | filter to integers | what domain is requested? | same variable symbol |
| open vs closed endpoint | exclude boundary integer | include it | is boundary admissible? | visual closeness |
| counting vs solving | first/last candidate | full enumeration | is only count requested? | small examples invite listing |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-F-01
WRONG_MOVE: count integers in `[12.4,20]` as `20-12.4` rounded.
WHY_TEMPTING: interval-length intuition.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: identify first and last admissible integers.
FALSIFIER_OR_CONTRAST: explicit list 13 through 20.

## G. First-move cues
If the final variable is integral, write the solved real interval first, then append `intersect Z` and identify the boundary integers.

## H. H3 -> H0 fading plan
H3: provide real interval and first candidate. H2: cue “intersect with integers.” H1: cue endpoint audit. H0: changed interval/counting item without method label.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q21 | 2024 Q21 | HBCSE_OFFICIAL | primary | integer intersection of floor-generated ranges | no | verified |
| IOQM-2024-Q26 | 2024 Q26 | HBCSE_OFFICIAL | bridge | discrete floor-value case filtering | no | verified |

## J. Source-independent mathematical trace
Q21 independently intersects integer ranges to the unique n=8991, yielding 91. Q26 filters possible integer floor values to 16 and 17, yielding 33.

## K. Contrast-pair candidates
real interval vs integer set; `[a,b)` vs `[a,b]`; length vs integer count; enumerate vs first/last; floor decode vs final integer filter.

## L. Transfer candidates
T2 number-line to integer list; T2 first/last formula; T3 labels/timestamps; T3 digit filters; T4 downstream NT/COMB final discrete selection.

## M. Candidate mastery items
Recognition of need for integer filter; first-line first/last candidates; full count; WHY-NOT interval-length method; verification by listing boundary cases.

## N. Dependency declarations
REQUIRES: W1-A/B/E and integer order. BRIDGE_REQUIRES: none. APPLIES: source-style digit/integer problems. Downstream may assume solve-then-filter discipline.

## O. Lead integration notes
Teach after equations. Keep the method distinct from general combinatorial counting and do not introduce NT/COMB taxonomy to learners.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
