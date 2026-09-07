---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-D
microstream_title: Reversible and one-way transformations
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-D — Reversible and One-Way Transformations

## A. Scope boundary
Included: equivalence vs implication for squaring, taking roots, multiplying/dividing by expressions, exponent/log conversion, sign conditions, and candidate checking. Excluded: generic equation-solving doctrine already exported by ALG-01; this stream specializes the doctrine for roots/exponents/logs.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: can perform algebraic operations on equations.
LIKELY_HALF_KNOWLEDGE: believes doing the same operation to both sides always preserves equivalence.
MISSING_BRIDGES: an operation can enlarge or shrink the solution set; domain/sign conditions decide reversibility.
OWNERSHIP_TARGET: DOMAIN -> OPERATION -> CONDITIONS -> ⇔ OR ⇒ -> CANDIDATES -> ORIGINAL CHECK.
```

## C. Mathematical invariant / governing structure
A transformation is safe as `⇔` only when the operation is one-to-one on the current admissible values or when its inverse conditions are explicitly imposed. For real `A,B`, `A=B ⇒ A^2=B^2`, but `A^2=B^2 ⇒ A=B` only with a compatible sign condition such as `A,B>=0`.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| implication chain | candidate generation | mark `⇒` | reverse not proved | write `=`/`⇔` automatically |
| equivalence chain | preserved solution set | state sign/domain before move | inverse valid | check redundantly but harmlessly |
| domain ledger | admissible set | write restrictions in margin | before manipulation | postpone domain to end |
| candidate table | extraneous roots | substitute into original | after one-way move | check transformed equation only |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| square two nonnegative sides | `⇔` | `⇒` + check | are both sides known nonnegative? | all squaring looks risky |
| square unrestricted sides | `⇒` + check | `⇔` | is sign equality encoded? | symmetric operation myth |
| divide by expression | split zero/nonzero branch | divide directly | can divisor be zero? | algebraic cancellation habit |
| apply log | equivalence | illegal step | are arguments positive and base valid? | log seen as a button |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-REV-01
WRONG_MOVE: mark every squaring step as equivalent.
WHY_TEMPTING: same operation is applied to both sides.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: square is not one-to-one on all reals; carry sign data.
FALSIFIER_OR_CONTRAST: 1^2=(-1)^2.

ERROR_CODE: ALG06-REV-02
WRONG_MOVE: discard a zero-divisor branch while cancelling.
WHY_TEMPTING: simplified equation looks cleaner.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: before division, branch on divisor=0 or prove nonzero.
FALSIFIER_OR_CONTRAST: x(x-1)=0 divided by x.
```

## G. First-move cues
- “square both sides” -> first write the signs of both sides.
- denominator contains variable -> protect the zero branch before cancelling.
- logarithm appears or is introduced -> write base/argument domain immediately.
- any `⇒` step -> create an explicit “check in original” obligation.

## H. H3 -> H0 fading plan
- H3: label each supplied step `⇔` or `⇒` and state why.
- H2: give only the equation and ask for the domain ledger.
- H1: provide a tempting radical equation with no warning.
- H0: mixed root/log equation where the learner chooses operations and maintains the ledger independently.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q28 | 2025/Q28 | CLEAN_OFFICIAL; overlay correction required | primary bridge | sign-controlled squaring | no | FINAL_OFFICIAL; answer 91 independently verified |
| IOQM-2023-Q02 | 2023/Q02 | CLEAN_VALIDATED | bridge | positive-log substitution and reversible multiplication by `t` | no | embedded key; answer 54 independently verified |

## J. Source-independent mathematical trace
Q28 audit explicitly proves both sides nonnegative before the first and second squaring, so those steps are reversible. Q02 has `a,b>=2`, hence `t=log_a b>0`; multiplying `t+6/t=5` by `t` is reversible. Both traces are fully recorded in the independent audit.

## K. Contrast-pair candidates
1. `A=B` vs `A^2=B^2`;
2. principal root vs ± solutions of a squared equation;
3. divide by known nonzero constant vs variable expression;
4. apply log on positive arguments vs unknown-sign expression;
5. transformed-solution check vs original-equation check;
6. cross-stream: common-base exact equivalence vs log-domain conversion.

## L. Transfer candidates
- T2: rational equation with removable zero branch.
- T2: geometry length equation where nonnegativity makes squaring reversible.
- T3: integer candidates generated by a square, then original check.
- T4: functional-equation substitution with domain restrictions compared to radical domain restrictions.

## M. Candidate mastery items
- recognition: classify five equation transformations as `⇔`, `⇒`, or invalid.
- first-line: state conditions before squaring `sqrt(f(x))=g(x)`.
- full solve: radical equation with one extraneous root.
- WHY-NOT: show why dividing by `x-2` can lose a solution.
- verification: repair a worked solution whose answer happens to be correct but logic is not.

## N. Dependency declarations
`REQUIRES`: ALG-01 equivalence/implication distinction.  
`BRIDGE_REQUIRES`: principal-root sign from W1-B; log domain from W1-E.  
`APPLIES`: all ALG-06 equation streams.  
Downstream may assume learners keep a domain/reversibility ledger and check candidates after one-way moves.

## O. Lead integration notes
This should be a topic-wide visual routine, not an isolated lesson: margin symbols `DOMAIN`, `⇔`, `⇒`, `CHECK`. Teach once, then require it silently in every root/log solution. Avoid formal logic terminology beyond what supports action.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
```
