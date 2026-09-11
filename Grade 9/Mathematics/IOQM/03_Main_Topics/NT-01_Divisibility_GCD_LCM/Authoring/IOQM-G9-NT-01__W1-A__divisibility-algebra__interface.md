---
main_topic_id: IOQM-G9-NT-01
microstream_id: W1-A
microstream_title: Divisibility meaning and algebra
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-01
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: `d|n` as integer-quotient structure, closure under integer linear combinations and divisibility chains. Excluded: congruence notation/cycles (NT-02) and prime-exponent divisor canon (NT-03).
## B. Learner-state model
PRIOR_KNOWLEDGE: integer arithmetic and divisibility tests. LIKELY_HALF_KNOWLEDGE: can test small numbers but does not use divisibility algebra. MISSING_BRIDGES: integer linear combinations and transitivity as problem-solving tools. OWNERSHIP_TARGET: structural divisibility before digit tests or enumeration.
## C. Mathematical invariant / governing structure
`d|a` and `d|b` imply `d|(ra+sb)` for all integers r,s. Also `a|b` and `b|c` imply `a|c`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| `d|n` | integer quotient | write `n=dq` if proof needed | integers | decimal divisibility intuition |
| two divisible expressions | eliminable variables | take integer linear combination | common divisor d | digit test |
| divisibility chain | transitivity | compose quotients | integers | recompute gcd/lcm |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| one-number test vs structural relation | divisibility test | linear combination | is d unknown across expressions? | digit tests are familiar |
| divisor vs multiple target | gcd-style restriction | lcm-style construction | is the unknown dividing or being divided? | same words recur |
| direct divisibility vs prime-exponent reasoning | algebraic quotient | NT-03 structure | are exponents actually needed? | factorization feels universal |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT01-A-01
WRONG_MOVE: apply a digit divisibility test to `d|(4n+7)` and `d|(7n+13)`.
WHY_TEMPTING: divisibility keyword.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: eliminate n by an integer linear combination.
FALSIFIER_OR_CONTRAST: `7(4n+7)-4(7n+13)=-3` immediately forces `d|3`.
## G. First-move cues
If the same unknown divisor divides two algebraic expressions, search for a small integer linear combination eliminating variables.
## H. H3 -> H0 fading plan
H3: provide the eliminating combination. H2: cue “eliminate n.” H1: ask what any common divisor must divide. H0: changed coefficients with no method label.
## I. Validated IOQM source anchors
`IOQM-2025-Q02` is a direct divisibility-counting bridge; `IOQM-2025-Q27` uses gcd/lcm normalization. Exact custody is W1-F.
## J. Source-independent mathematical trace
All promoted authored linear-combination restrictions are independently checked by expansion; Q02=17 and Q27=40 remain independently verified in the source map.
## K. Contrast-pair candidates
divisor vs multiple; digit test vs structural divisibility; direct quotient vs linear combination; transitivity vs recomputation; divisibility algebra vs congruence notation.
## L. Transfer candidates
same-remainder differences; coefficient elimination; chain extremals; integer factor bridge; later modular statement retrieval.
## M. Candidate mastery items
recognition; first-line combination; full structural-divisibility solve; WHY-NOT digit test; chain verification.
## N. Dependency declarations
REQUIRES: integer arithmetic. BRIDGE_REQUIRES: none. APPLIES: Euclid, gcd/lcm and same-remainder streams. Downstream may assume linear-combination closure and transitivity.
## O. Lead integration notes
Teach as the algebraic foundation. Do not introduce NT-02 notation or NT-03 exponent canon here.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after learner-source repair
