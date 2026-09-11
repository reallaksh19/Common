---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-C
microstream_title: Negative inputs
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: [IOQM-G9-ALG-07__W1-A__definition-order__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: floor/ceiling on negative inputs, truncation contrast, consecutive-integer localization. Excluded: decimal representation theory and general signed inequality canon.

## B. Learner-state model
PRIOR_KNOWLEDGE: ordering negative numbers.
LIKELY_HALF_KNOWLEDGE: assumes floor means delete decimals.
MISSING_BRIDGES: greatest integer not exceeding vs truncation toward zero.
OWNERSHIP_TARGET: definition-led handling of negative inputs.

## C. Mathematical invariant / governing structure
If `m<=x<m+1`, then `floor(x)=m` even for negative x. Therefore `floor(-2.3)=-3`, while `ceil(-2.3)=-2`.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| number line | consecutive integers | locate x | real x | truncate digits |
| order inequality | greatest/least qualifying integer | bracket x | negative x | compare absolute values |
| reflection | ceiling/floor duality | use `ceil(x)=-floor(-x)` | any real x | change sign without swapping function |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| truncation vs floor | toward zero | toward `-infinity` as needed | which definition is requested? | same result for positive decimals |
| floor vs ceiling | greatest <=x | least >=x | lower or upper integer? | both produce nearby integers |
| decimal digits vs fractional part | textual digits | `x-floor(x)` | is x negative? | positive-number intuition |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-C-01
WRONG_MOVE: `floor(-2.3)=-2`.
WHY_TEMPTING: truncation habit.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: choose the greatest integer `<=x`.
FALSIFIER_OR_CONTRAST: `-2` is greater than `-2.3`, so it cannot be the floor.

## G. First-move cues
For a negative decimal, place it between consecutive integers before evaluating floor or ceiling.

## H. H3 -> H0 fading plan
H3: give the bracketing inequality. H2: cue “greatest integer <=x.” H1: cue “do not truncate.” H0: changed negative input and fractional-part item.

## I. Validated IOQM source anchors
No historical anchor is promoted solely by this microstream; the topic anchors remain verified in W1-G and the source map.

## J. Source-independent mathematical trace
All claims follow directly from the definitions and are checked by bracketing negative examples. No official source dependence is required.

## K. Contrast-pair candidates
positive vs negative decimal; truncation vs floor; floor vs ceiling; negative fractional part vs visible decimal digits; direct definition vs reflection identity.

## L. Transfer candidates
T2 number-line representation; T2 reflection identity; T3 signed measurement context; T3 fractional part; T4 negative endpoint filter in discrete problems.

## M. Candidate mastery items
Recognition of truncation error; first-line bracketing; full evaluation; WHY-NOT explaining `-2`; verification using definition.

## N. Dependency declarations
REQUIRES: real-number order and W1-A. BRIDGE_REQUIRES: none. APPLIES: reflection identity later. Downstream may assume negative-input correctness.

## O. Lead integration notes
Teach before fractional part and mixed equations. Keep “truncation” only as a contrast, never as a method.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
