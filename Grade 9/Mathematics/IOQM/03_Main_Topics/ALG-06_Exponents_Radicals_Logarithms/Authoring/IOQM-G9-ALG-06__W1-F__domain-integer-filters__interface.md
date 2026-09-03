---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-F
microstream_title: Domain and integer filters
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-F — Domain and Integer Filters

## A. Scope boundary
Included: convert radical/log conditions into admissible sets, perfect-square/nonsquare tests, nonnegative-integer constraints, bounds, and filtering candidates after algebra. Excluded: general number-theory factorisation canon, modular arithmetic chapters, and inequality optimization beyond minimal filtering.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: knows integers, squares and inequalities.
LIKELY_HALF_KNOWLEDGE: solves over reals and only later notices the problem asked for integers.
MISSING_BRIDGES: domain is part of the equation; discrete restrictions can be used early; candidate count is often much smaller than real-solution set.
OWNERSHIP_TARGET: DOMAIN SET -> ALGEBRAIC STRUCTURE -> DISCRETE FILTER -> ORIGINAL CHECK.
```

## C. Mathematical invariant / governing structure
A valid solution lies in the intersection of every constraint: algebraic relation, root/log domain, sign conditions, and stated discrete set. Filtering is not an afterthought: if a relation proves `a=t(t-1)/2` with integer `t`, the integer/bound structure is now the primary representation.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| interval/domain set | legal real inputs | intersect restrictions | all conditions collected | solve first, filter vaguely |
| perfect-square condition | integer root | write radicand=`k^2` | root proved integer | assume integer from integer radicand |
| parameter sequence | finite search | use monotonicity/bound | parameter integral | enumerate original variables |
| exponent-power pairs | integer count | bound base by power | exponent exact | count reals |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| root result is integer | perfect-square filter | leave radical | is integrality proved/stated? | integer radicand confusion |
| parameter `<100` | monotone bound | list 1..99 | is there a one-parameter formula? | small range |
| log equation with integer bases | count power pairs | solve continuously | did exponent become integer? | logarithms suggest real analysis |
| radical domain | interval intersection | candidate checking only | can domain eliminate branches now? | checking feels sufficient |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-FLT-01
WRONG_MOVE: treat every nonnegative integer radicand as having an integer square root.
WHY_TEMPTING: closure of integers under basic operations is overgeneralized.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: integer square root iff radicand is a perfect square.
FALSIFIER_OR_CONTRAST: sqrt(2).

ERROR_CODE: ALG06-FLT-02
WRONG_MOVE: keep a real solution that violates a stated natural-number bound.
WHY_TEMPTING: algebraic solving is mistaken for problem completion.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: final set is intersection of algebra, domain, and discrete constraints.
FALSIFIER_OR_CONTRAST: real x=3/2 when x must be integer.
```

## G. First-move cues
- “nonnegative integers” -> write the discrete set immediately.
- principal root equals integer -> ask whether the equation proves a perfect square.
- bounded parameter after structural substitution -> use monotonicity, not brute force.
- exact exponent `2` or `3` with bounded integer bases -> count power pairs.

## H. H3 -> H0 fading plan
- H3: provide candidate list and ask which survive all restrictions.
- H2: give domain + one discrete condition to intersect.
- H1: show only “positive nonsquare integer <100”.
- H0: derive a parameter relation and independently decide the cheapest discrete filter.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q28 | 2025/Q28 | CLEAN_OFFICIAL; correction overlay | primary | nonsquare/bound/integer filter | no | independently verified 91 |
| IOQM-2023-Q02 | 2023/Q02 | CLEAN_VALIDATED | primary | bounded integer power pairs | no | independently verified 54 |

## J. Source-independent mathematical trace
Q28 reduces to `a=t(t-1)/2`; monotonicity gives `t=14 ->91`, `t=15 ->105`, and nonsquare check retains 91. Q02 reduces to `b=a^2` or `b=a^3`; bounds give 43+11=54 pairs. Both agree with verification authority.

## K. Contrast-pair candidates
1. real solution vs admissible integer solution;
2. integer radicand vs perfect-square radicand;
3. brute-force bound vs monotone parameter bound;
4. domain exclusion vs extraneous-root exclusion;
5. square parameter vs nonsquare condition;
6. cross-domain: algebraic relation vs number-theory filter.

## L. Transfer candidates
- T2: nested radical leading to a pentagonal/triangular-number sequence.
- T2: log equation leading to fourth powers under a different bound.
- T3: radical equation with parity constraint.
- T4: geometry length that must be integer after a root relation.

## M. Candidate mastery items
- recognition: identify which constraints should be applied before solving.
- first-line: write the admissible set for a root/log expression.
- full solve: parameter relation plus `<N` and nonsquare filter.
- WHY-NOT: explain why checking only the transformed equation is insufficient.
- verification: audit a candidate list for completeness and legality.

## N. Dependency declarations
`REQUIRES`: W1-B principal roots, W1-D reversibility, W1-E log domain.  
`BRIDGE_REQUIRES`: elementary perfect-square and integer-bound reasoning.  
`APPLIES`: all historical ALG-06 anchors.  
Downstream may assume learners intersect algebraic and discrete conditions explicitly.

## O. Lead integration notes
Do not make this a separate number-theory lesson. Recur as a final column in the topic router: `conditions/check`. Use source anchors to show discrete filters can simplify early, not merely validate late.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
```
