---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-D
microstream_title: Translation, reflection and fractional part
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: [IOQM-G9-ALG-07__W1-A__definition-order__interface.md, IOQM-G9-ALG-07__W1-C__negative-inputs__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: integer shifts, floor/ceiling reflection, fractional-part definition and negative-input behavior. Excluded: noninteger-shift pseudo-identities and unrelated modular arithmetic canon.

## B. Learner-state model
PRIOR_KNOWLEDGE: floor/ceiling definitions.
LIKELY_HALF_KNOWLEDGE: recognizes patterns from examples but overgeneralizes shifts.
MISSING_BRIDGES: proof from interval definitions; fractional part for negative values.
OWNERSHIP_TARGET: safe use of structural identities.

## C. Mathematical invariant / governing structure
For integer k, `floor(x+k)=floor(x)+k` and `ceil(x+k)=ceil(x)+k`; also `ceil(x)=-floor(-x)` and `{x}=x-floor(x)` with `0<={x}<1`. Each follows by translating/reflection of the defining half-open interval.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| integer translation | same unit interval shifted | isolate integer shift | k integer | extend identity to noninteger shift |
| reflection | floor/ceiling duality | negate input/output | any real x | forget to swap floor/ceiling |
| fractional part | residual in `[0,1)` | subtract floor | any real x | use visible decimal digits |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| integer vs noninteger shift | identity | decode directly | is the shift an integer? | notation looks similar |
| floor vs reflected ceiling | direct decode | reflection identity | which is cheaper? | both are valid |
| decimal tail vs fractional part | typography | structural residual | can x be negative/nonterminating? | positive examples coincide |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-D-01
WRONG_MOVE: assume `floor(x+0.4)=floor(x)+0.4`.
WHY_TEMPTING: linearity intuition.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: only integer translations preserve the staircase exactly.
FALSIFIER_OR_CONTRAST: take x=0.8.

## G. First-move cues
If an integer shift is visible, pull it outside. If a ceiling of a negated expression appears, test reflection. For fractional part, write `x-floor(x)`.

## H. H3 -> H0 fading plan
H3: state the exact identity. H2: cue integer shift/reflection. H1: ask whether the shift is integral. H0: mixed shifted/reflected/fractional-part item.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q21 | 2024 Q21 | HBCSE_OFFICIAL | bridge | floor constraints | no | verified |
| IOQM-2024-Q26 | 2024 Q26 | HBCSE_OFFICIAL | bridge | floor-value case structure | no | verified |

## J. Source-independent mathematical trace
The identities are definition-derived and do not depend on historical wording. Topic anchors Q21=91 and Q26=33 remain independently verified in the source map.

## K. Contrast-pair candidates
integer vs noninteger shift; direct decode vs reflection; positive vs negative fractional part; floor translation vs naive linearity; fractional part vs decimal digits.

## L. Transfer candidates
T2 symbolic identity; T2 interval translation; T3 clock/level shifts; T3 negative fractional part; T4 bridge to discrete residue-style reasoning without importing NT canon.

## M. Candidate mastery items
Recognition of applicable shift; first-line identity; full solve after translation; WHY-NOT noninteger shift; verification by interval definition.

## N. Dependency declarations
REQUIRES: W1-A and W1-C. BRIDGE_REQUIRES: elementary algebra. APPLIES: later equations/counting. Downstream may assume these exact identities and their conditions.

## O. Lead integration notes
Teach after negative inputs. Emphasize conditions on identities and avoid presenting them as generic linearity.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
