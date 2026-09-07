---
main_topic_id: IOQM-G9-ALG-06
microstream_id: W1-B
microstream_title: Principal radicals and conjugates
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-06
prerequisite_interfaces:
  - ALG01_Stable_Prerequisite_Interface_v1.md
source_cutoff: 2026-09-03
---
# W1-B — Principal Radicals and Conjugates

## A. Scope boundary
Included: principal square root, radicand domain, `sqrt(u^2)=|u|`, simplification, conjugate products, rationalisation only when it reveals structure. Excluded: nested-radical source pattern (W1-C), general squaring/reversibility protocol (W1-D), and abstract field theory.

## B. Learner-state model
```text
PRIOR_KNOWLEDGE: simplify sqrt(12), multiply simple surds.
LIKELY_HALF_KNOWLEDGE: writes sqrt(u^2)=u automatically and rationalises by habit.
MISSING_BRIDGES: principal-root sign; domain before algebra; conjugate as difference-of-squares tool.
OWNERSHIP_TARGET: RADICAND -> SIGN -> SIMPLEST STRUCTURE -> CONJUGATE IF USEFUL -> CHECK.
```

## C. Mathematical invariant / governing structure
For real `u`, `sqrt(u^2)=|u|`, because the principal square root is non-negative. For `A>=0,B>=0`, the conjugate identity `(sqrt(A)-sqrt(B))(sqrt(A)+sqrt(B))=A-B` converts a radical difference into algebra without changing the value.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| factor-square radicand | removable square factor | extract perfect squares | radicand nonnegative | split sums under a root |
| conjugate pair | difference of squares | multiply numerator/denominator or equation strategically | conjugate factor nonzero if dividing | rationalise everything |
| absolute-value form | principal sign | replace `sqrt(u^2)` by `|u|` | real `u` | write `u` |
| geometric length | positivity | state length/root nonnegative | geometry valid | introduce ± for a principal root |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| `sqrt(50)` | factor square | decimal | is exact form expected? | calculator reflex |
| `1/(sqrt5-2)` | conjugate | square denominator | does conjugate collapse denominator? | squaring feels direct |
| `sqrt((x-3)^2)` | absolute value | `x-3` | is sign of `x-3` known? | cancellation pattern |
| `sqrt(a+b)` | leave/transform whole radicand | split roots | is radicand a product? | false distributivity |

## F. Misconception/diagnosis catalogue
```text
ERROR_CODE: ALG06-RAD-01
WRONG_MOVE: sqrt(x^2)=x for unrestricted real x.
WHY_TEMPTING: square/root are treated as inverse symbols without principal-value convention.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: sqrt(x^2)=|x|.
FALSIFIER_OR_CONTRAST: x=-3.

ERROR_CODE: ALG06-RAD-02
WRONG_MOVE: sqrt(a+b)=sqrt(a)+sqrt(b).
WHY_TEMPTING: product rule is overextended to addition.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: root multiplication applies to admissible products, not sums.
FALSIFIER_OR_CONTRAST: sqrt(1+1)!=2.
```

## G. First-move cues
- square hidden inside radicand -> factor it before expanding anything.
- radical difference in denominator or product -> test the conjugate.
- `sqrt(expression^2)` -> ask for sign before removing the root.
- equation with a single radical -> isolate it, then hand off to W1-D sign/reversibility protocol.

## H. H3 -> H0 fading plan
- H3: explicitly mark the perfect-square factor or conjugate.
- H2: cue “principal root/sign?”
- H1: show only a radical expression whose wrong shortcut is tempting.
- H0: mixed expression where learner decides between factoring, conjugating, or leaving the radical untouched.

## I. Validated IOQM source anchors
`IOQM-2025-Q28` is a bridge anchor because its nested radical and principal-root signs depend on this stream; the full source trace is in W1-C/W1-G. Verified answer `91`; source correction overlay mandatory.

## J. Source-independent mathematical trace
For Q28, this stream contributes only the sign facts: both principal roots are nonnegative and `sqrt(a)-y` must be nonnegative. Full derivation independently closes to `91` in `Independent_Math_and_Source_Audit.md`.

## K. Contrast-pair candidates
1. `sqrt(x^2)` vs `x` when `x>=0`;
2. product under root vs sum under root;
3. conjugate as structure vs decorative rationalisation;
4. principal root vs equation `z^2=a` with two possible signs;
5. exact surd vs decimal approximation;
6. simple radical difference vs nested radical (W1-C).

## L. Transfer candidates
- T2: geometric distance expression with hidden square factor.
- T2: rational denominator changed to a numerator radical difference.
- T3: integer condition after rationalisation.
- T4: number-theory irrationality check using nonsquare `a`.

## M. Candidate mastery items
- recognition: identify invalid `sqrt(x^2)=x` step.
- first-line: simplify `sqrt(72y^2)` under `y<0`.
- full solve: exact conjugate simplification with a condition preventing zero denominator.
- WHY-NOT: explain why a split-root move fails.
- verification: state the missing sign assumption in a worked solution.

## N. Dependency declarations
`REQUIRES`: ALG-01 equivalence discipline.  
`BRIDGE_REQUIRES`: absolute value meaning.  
`APPLIES`: difference-of-squares identity.  
Downstream may assume principal roots are nonnegative and `sqrt(u^2)=|u|`.

## O. Lead integration notes
Teach principal-root meaning before any radical equation. Conjugates should appear as a structural move, not a compulsory formatting rule. Keep abstract irrationality proofs teacher-side except the simple nonsquare argument needed by Q28.

## P. Independent QA status
```text
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
```
