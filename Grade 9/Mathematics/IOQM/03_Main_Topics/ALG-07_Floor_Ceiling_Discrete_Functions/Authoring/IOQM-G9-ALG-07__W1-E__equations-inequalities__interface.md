---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-E
microstream_title: Floor and ceiling equations and inequalities
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: [IOQM-G9-ALG-07__W1-A__definition-order__interface.md, IOQM-G9-ALG-07__W1-B__endpoint-control__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: decoding floor/ceiling equations and threshold inequalities into continuous conditions, then solving with endpoint control. Excluded: optimization, equality cases and general inequality canon owned by ALG-02.

## B. Learner-state model
PRIOR_KNOWLEDGE: linear equations/inequalities and interval notation.
LIKELY_HALF_KNOWLEDGE: treats discrete-function equations as ordinary equations.
MISSING_BRIDGES: decode-first workflow and integer-threshold interpretation.
OWNERSHIP_TARGET: `DECODE -> SOLVE -> CHECK ENDPOINTS`.

## C. Mathematical invariant / governing structure
A floor/ceiling equation specifies a half-open interval for its argument. Solve that continuous condition first; for inequalities, reduce to the relevant integer threshold without importing unrelated optimization methods.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| `floor(f(x))=n` | interval family | `n<=f(x)<n+1` | n integer | set `f(x)=n` |
| `ceil(f(x))=n` | opposite half-open interval | `n-1<f(x)<=n` | n integer | use floor endpoints |
| discrete inequality | threshold | identify integer comparison | order-known | manipulate floor symbol like a variable |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| floor equation vs algebraic equation | decode interval | solve equality | is floor/ceiling present? | equation notation |
| discrete vs continuous target | solve interval | integer filter later | what is the final domain? | early case mixing |
| local inequality vs ALG-02 canon | minimal decode | optimization machinery | is optimization/equality doctrine actually needed? | same inequality symbols |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-E-01
WRONG_MOVE: `floor(2x)=3 -> 2x=3`.
WHY_TEMPTING: direct equation-solving reflex.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: `3<=2x<4`.
FALSIFIER_OR_CONTRAST: x=1.8 satisfies the floor equation but not `2x=3`.

## G. First-move cues
Whenever the discrete function equals an integer, write its defining double inequality before algebra.

## H. H3 -> H0 fading plan
H3: full decoded inequality. H2: cue “decode the discrete value.” H1: cue endpoint strictness. H0: mixed floor/ceiling equation on a changed expression.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q21 | 2024 Q21 | HBCSE_OFFICIAL | primary | invert floor constraints and intersect | no | verified |
| IOQM-2024-Q26 | 2024 Q26 | HBCSE_OFFICIAL | primary | set floor value n and solve feasibility | no | verified |

## J. Source-independent mathematical trace
Q21 independently narrows the repeated-digit interval and permutation interval to n=8991, answer 91. Q26 independently finds only floor values 16 and 17, answer 33. Both agree with the official key.

## K. Contrast-pair candidates
floor equation vs ordinary equation; floor vs ceiling equation; real solution interval vs integer solution set; endpoint included vs excluded; local decoding vs general inequality optimization.

## L. Transfer candidates
T2 symbol-to-interval; T2 interval-to-symbol; T3 integer parameter; T3 digit constraint after floor inversion; T4 bridge to NT/COMB final filtering.

## M. Candidate mastery items
Recognition of correct decode; first-line inequality only; full linear solve; WHY-NOT ordinary equality; source-style multi-constraint intersection.

## N. Dependency declarations
REQUIRES: W1-A/W1-B and routine algebra. BRIDGE_REQUIRES: narrow factor-sign reasoning where declared. APPLIES: integer filtering W1-F. Downstream may assume decode-first equation handling.

## O. Lead integration notes
Keep general inequality methods out. Teach one governing router and reuse it across all equations/inequalities.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
