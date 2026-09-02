---
main_topic_id: IOQM-G9-NT-01
microstream_id: W1-E
microstream_title: Divisibility chains and extremal divisors
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-01
prerequisite_interfaces: [IOQM-G9-NT-01__W1-A__divisibility-algebra__interface.md, IOQM-G9-NT-01__W1-C__gcd-lcm-reconstruction__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: transitive divisibility chains, finding all intermediates under `a|x|b`, and extremal common-divisor/common-multiple choices. Excluded: divisor-count formulas and prime-exponent enumeration canon owned by NT-03.
## B. Learner-state model
PRIOR_KNOWLEDGE: basic divisibility. LIKELY_HALF_KNOWLEDGE: can list factors but misses chain implications or extremal direction. MISSING_BRIDGES: normalize intermediate divisors and identify “greatest divisor” versus “least multiple.” OWNERSHIP_TARGET: structural chain reasoning without unnecessary prime-exponent machinery.
## C. Mathematical invariant / governing structure
If `a|x|b`, then write `x=ak` and require `k|(b/a)` when `a|b`. Extremal common-divisor targets route to gcd; extremal common-multiple targets route to lcm.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| `a|x|b` | bounded divisibility chain | write `x=ak` | a|b for simple normalization | enumerate all integers |
| greatest common divisor target | extremal divisor | form gcd | common-divisor context | lcm |
| least common multiple target | extremal multiple | form lcm | common-multiple context | gcd |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| intermediate divisor vs arbitrary factor | chain-normalize | list factors | must x be both multiple and divisor? | factor lists look sufficient |
| greatest divisor vs least multiple | gcd | lcm | divisor or multiple target? | words “greatest/least” dominate |
| enumerate divisors vs NT-03 divisor-count canon | explicit small factor set | exponent formula | is count/exponent structure needed? | prime factorization is familiar |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT01-E-01
WRONG_MOVE: treat `6|x|72` as only “x is a divisor of 72.”
WHY_TEMPTING: second condition is more visually restrictive.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: write `x=6k`, then `k|12`.
FALSIFIER_OR_CONTRAST: divisors such as 8 or 9 fail the multiple-of-6 condition.
## G. First-move cues
For `a|x|b`, factor out a first. For “greatest divisor” use gcd; for “least multiple” use lcm.
## H. H3 -> H0 fading plan
H3: give `x=ak`. H2: cue divisibility chain. H1: ask what x must be a multiple of and divide. H0: changed chain/extremal problem.
## I. Validated IOQM source anchors
`IOQM-2025-Q02` is a simple divisibility-counting bridge, while Q27 supports gcd/lcm structural normalization; exact custody is W1-F.
## J. Source-independent mathematical trace
Chain transformations are verified algebraically; authored intermediate-divisor lists in the teacher key are checked directly.
## K. Contrast-pair candidates
chain vs one-sided divisibility; greatest divisor vs least multiple; enumerate vs normalize; factor list vs structural condition; elementary divisor set vs NT-03 divisor-count theory.
## L. Transfer candidates
intermediate divisor; machine periods; common-step ruler; bounded gcd/lcm reconstruction; downstream divisor-theory handoff.
## M. Candidate mastery items
recognition; first-line normalization; full chain enumeration; WHY-NOT one-sided factor list; extremal-operation choice.
## N. Dependency declarations
REQUIRES: W1-A and W1-C. BRIDGE_REQUIRES: none. APPLIES: practice chains and extremal targets. NT-03 owns general prime-exponent/divisor-count canon.
## O. Lead integration notes
Use small explicit factor sets where needed; do not preteach NT-03 formulas.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after learner-source repair
