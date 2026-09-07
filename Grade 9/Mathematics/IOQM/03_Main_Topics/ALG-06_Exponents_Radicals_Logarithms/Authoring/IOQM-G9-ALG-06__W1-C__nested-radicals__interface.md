---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-C
microstream_title: Nested radicals and structural reduction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-C — Nested Radicals and Structural Reduction

## A. Scope boundary
Included: nested square roots, sign/domain routing, naming an inner root, detecting integer/irrational separation, and structural substitutions that reduce nesting. Excluded: arbitrary denesting formula catalogues, olympiad surd tricks without Grade-9 transfer value, and general implication/equivalence doctrine beyond W1-D.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can square a simple radical equation.
LIKELY_HALF_KNOWLEDGE: squares immediately and expands before reading the inner root.
MISSING_BRIDGES: nested structure has an inner object; sign conditions arrive before squaring; nonsquare irrationality can force coefficients to vanish.
OWNERSHIP_TARGET: NAME INNER ROOT -> DOMAIN/SIGN -> ISOLATE STRUCTURE -> REVERSIBLE MOVE -> DISCRETE FILTER.
```

## C. Mathematical invariant / governing structure
In `sqrt(U - sqrt(V))`, the inner value is a constrained nonnegative object. Naming `t=sqrt(V)` can expose both an algebraic relation and a sign condition. When `sqrt(a)` is irrational for nonsquare integer `a`, an equality `r+s sqrt(a)=integer` with rational/integer `r,s` forces `s=0`.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| named inner root `t` | two-layer dependency | set `t=sqrt(V)` | `V>=0,t>=0` | square outer and inner simultaneously |
| integer + irrational part | coefficient forcing | collect `sqrt(a)` term | `a` nonsquare | compare coefficients without proving irrationality |
| triangular-number form | discrete candidates | reduce to `a=t(t-1)/2` | integer `t` established | brute-force `a` |
| conjugate/rationalised form | product invariant | multiply conjugate only if it shortens nesting | nonzero factor if dividing | denest by guessing |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| simple `sqrt(x+a)` | isolate and square | name inner root | is there another outer root depending on it? | same notation |
| nested root with integer target | irrationality separation | repeated expansion | does one side become integer plus `sqrt(a)`? | expansion feels systematic |
| `sqrt(m+2sqrt n)` | square-pattern recognition | Q28-style inner-root route | is the radicand itself a quadratic surd? | all nested roots look alike |
| bounded integer parameter | structural formula then filter | enumerate | can nesting yield a one-parameter integer form? | small bound invites brute force |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-NEST-01
WRONG_MOVE: square both layers in one step and lose the sign constraints.
WHY_TEMPTING: nesting is seen as merely extra parentheses.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: name the inner principal root and carry its nonnegativity.
FALSIFIER_OR_CONTRAST: compare with a simple one-root equation.

ERROR_CODE: ALG06-NEST-02
WRONG_MOVE: assume sqrt(x+a) is an integer because x,a are integers.
WHY_TEMPTING: integer radicand is confused with square radicand.
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: integer root requires perfect-square radicand or an equation that proves integrality.
FALSIFIER_OR_CONTRAST: sqrt(2).
```

## G. First-move cues
- root inside root -> name the inner root before expanding.
- nonsquare parameter with an integer equality -> collect rational and irrational parts.
- upper bound on integer parameter -> derive a monotone/discrete formula before testing values.
- any squaring -> invoke W1-D and record sign/equivalence.

## H. H3 -> H0 fading plan
- H3: give `t=sqrt(x+a)` explicitly and ask for the two resulting relations.
- H2: say “name the inner root.”
- H1: show a nested radical plus a nonsquare-integer condition only.
- H0: changed-surface nested radical where a discrete parameter emerges only after the learner chooses the inner object.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q28 | 2025/Q28 | CLEAN_OFFICIAL; metadata overlay required | primary | nested radical; irrationality; integer filter | no | FINAL_OFFICIAL; independently verified 91 |

## J. Source-independent mathematical trace
Exact source: `sqrt(x-sqrt(x+a))=sqrt(a)-y`, with `a` positive nonsquare `<100`, `x,y` nonnegative integers. Domain gives RHS nonnegative. If `y>0`, after a reversible first square write `sqrt(x+a)=k+2y sqrt(a)` with integer `k`; a second equality to an integer forces `k=0`, which yields `a=y^2/(4y^2-2)<1`, contradiction. Thus `y=0`. Then `sqrt(x+a)=x-a=t>=0`, so `t^2=2a+t` and `a=t(t-1)/2`; `t=14` gives 91, `t=15` gives 105. Official answer agrees.

## K. Contrast-pair candidates
1. simple radical vs nested radical;
2. name inner object vs expand everything;
3. nonsquare irrationality vs perfect-square inner root;
4. structural parameter formula vs bounded brute force;
5. reversible square vs candidate-generating square;
6. cross-stream: conjugate simplification vs inner-root substitution.

## L. Transfer candidates
- T2: nested radical with different outer constant but same inner-root invariant.
- T2: integer equality containing `p+q sqrt(a)`.
- T3: triangular-number parameter with parity/bound filter.
- T4: geometry length nested in a distance expression, then integer constraint.

## M. Candidate mastery items
- recognition: which object should be named first in a two-level root?
- first-line: state domain/sign facts before squaring.
- full solve: derive a discrete parameter formula from a nested radical.
- WHY-NOT: explain why integer radicand does not imply integer root.
- source-integrity: distinguish the correct Q28 nested stem from the stale flattened classifier.

## N. Dependency declarations
`REQUIRES`: W1-B principal-root meaning; ALG-01 equivalence discipline.  
`BRIDGE_REQUIRES`: elementary irrationality of `sqrt(n)` for nonsquare integer `n`.  
`APPLIES`: integer/discrete filters from W1-F.  
Downstream may assume learners identify and name the inner root before manipulating a nested radical.

## O. Lead integration notes
Use Q28 as the flagship source anchor only after principal-root and reversibility routines are established. Do not teach a catalogue of denesting identities. Keep the stale Q28 classifier visible only in teacher/source-custody notes, never learner prose.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
```
