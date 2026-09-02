---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-E
microstream_title: Quadratic and perfect-square filters
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [ALG03_Stable_Prerequisite_Interface_v1, NT03_Stable_Divisor_PerfectPower_Interface_v1]
source_cutoff: 2026-09-02
---

# Quadratic and perfect-square filters - Research Interface

## A. Scope boundary
Included: retrieving the discriminant as a bridge when an integer variable must solve a quadratic; requiring the discriminant to be a perfect square; converting the resulting square equation to difference-of-squares factor cases. Excluded: full discriminant/root theory (ALG-03) and full perfect-power canon (NT-03).

## B. Learner-state model
`PRIOR_KNOWLEDGE:` quadratic formula may be familiar; perfect squares are familiar.

`LIKELY_HALF_KNOWLEDGE:` learner checks discriminant >=0 but forgets integer roots require a square and numerator divisibility.

`MISSING_BRIDGES:` integer root -> square discriminant -> factorisation -> finite cases -> reconstruction.

`OWNERSHIP_TARGET:` use borrowed discriminant machinery to generate a complete integer candidate set.

## C. Mathematical invariant / governing structure
**Invariant:** `INTEGER QUADRATIC ROOT -> PERFECT-SQUARE DISCRIMINANT -> DIFFERENCE OF SQUARES -> FINITE FACTOR PAIRS`.

For `An^2+Bn+C=0` with integer coefficients and integer n, the discriminant `Delta=B^2-4AC` must be a nonnegative perfect square `k^2`; additionally `-B +/- k` must be divisible by `2A`. NT-04 uses this only as a candidate generator.

If the square condition rearranges to `X^2-Y^2=N`, factor `(X-Y)(X+Y)=N`. The factors must have the same parity to reconstruct integer X,Y. Enumerate factor pairs, reconstruct variables, then check the original equation.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| quadratic in integer n | discriminant square | write `Delta=k^2` | `Delta>=0`; numerator divisibility | solve decimals |
| `X^2-Y^2=N` | factor pairs | `(X-Y)(X+Y)=N` | factor parity/order | search squares |
| square-valued expression | perfect-square filter | retrieve NT-03 signature if useful | nonnegative integer | only test nonnegativity |
| reconstructed root | original equation | substitute back | all signs/domains | trust discriminant alone |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| quadratic real root | ALG-03 behavior | integer square filter | Is root required integral? | discriminant >=0 seems sufficient |
| square condition | factor difference of squares | scan k values | Can fixed N be factored? | square search is concrete |
| perfect square | retrieve NT-03 | derive square theory again | Is squarehood only a filter? | topic adjacency |
| candidate root | divisibility check | stop after square Delta | Does denominator divide numerator? | quadratic formula looks complete |

## F. Misconception / diagnosis catalogue
`NT04-SQ-01`
- WRONG_MOVE: use `Delta>=0` as the integer-root criterion.
- WHY_TEMPTING: that is the real-root criterion.
- MISSING_LINK_CLASS: DISCRETE_FILTER.
- REPAIR_INVARIANT: Delta must be a square and the root numerator integral.
- FALSIFIER_OR_CONTRAST: `x^2-x-1=0` has positive discriminant 5 but no integer roots.

`NT04-SQ-02`
- WRONG_MOVE: test k=0,1,2,... without a bound.
- WHY_TEMPTING: perfect square suggests square enumeration.
- MISSING_LINK_CLASS: REPRESENTATION.
- REPAIR_INVARIANT: factor a difference of squares with fixed product.
- FALSIFIER_OR_CONTRAST: `(X-k)(X+k)=N` gives all k from divisors at once.

`NT04-SQ-03`
- WRONG_MOVE: reconstruct from a factor pair but ignore parity.
- WHY_TEMPTING: factors satisfy the product.
- MISSING_LINK_CLASS: DOMAIN_CONDITION.
- REPAIR_INVARIANT: `X=(r+s)/2`, `Y=(s-r)/2` must be integers.
- FALSIFIER_OR_CONTRAST: opposite-parity factors do not reconstruct integer X,Y.

## G. First-move cues
- integer n solves a quadratic -> retrieve discriminant and write `Delta=k^2`.
- square differs from square by fixed N -> factor the difference.
- factor pair reconstructs X,Y -> check same parity.
- quadratic candidate found -> verify numerator divisibility and original equation.

## H. H3 -> H0 fading plan
- **H3:** solve a guided integer square condition by difference of squares.
- **H2:** quadratic in n; cue only "integer root -> square discriminant."
- **H1:** discriminant square already written; ask for the next structural factorisation.
- **H0:** changed-surface integer lattice equation whose discriminant becomes `X^2-Y^2=N`.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| `IOQM-2023-Q11` | 2023/11 | CLEAN_VALIDATED | primary | discriminant square; factorisation; bounds | no | EMBEDDED_KEY |

## J. Source-independent mathematical trace
For `m^2=4n^2-5n+16`, view as quadratic in n:
`4n^2-5n+(16-m^2)=0`. Integer n implies
`k^2=25-16(16-m^2)=16m^2-231`, hence `(4m-k)(4m+k)=231`.
Positive factor pairs `(1,231),(3,77),(7,33),(11,21)` reconstruct
`(m,n)=(29,15),(10,-4),(5,-1),(4,0)`.
The corresponding `|m-n|` values are **14,14,6,4**, so the maximum is 14.

## K. Contrast-pair candidates
1. real root vs integer root;
2. nonnegative discriminant vs square discriminant;
3. perfect-square filter vs full NT-03 theory;
4. scanning squares vs factoring a difference of squares;
5. square discriminant vs integral quadratic-root numerator.

## L. Transfer candidates
- **T2:** Pythagorean-looking equation reduced to difference of squares.
- **T2:** parameter values making a quadratic have integer roots.
- **T3:** integer geometry where a length equation produces a quadratic square filter.
- **T4:** algebraic root condition feeding NT-04 finite reconstruction.

## M. Candidate mastery items
- Recognition: determine when `Delta=k^2` is the right first bridge.
- First-line: write the square-discriminant condition for a quadratic in n.
- Full solve: find integer parameters making a bounded quadratic have integer roots.
- WHY-NOT: exhibit a quadratic with positive nonsquare discriminant.
- Verification: after factor reconstruction, check numerator divisibility by `2A`.

## N. Dependency declarations
`REQUIRES:` ALG-03 discriminant; NT-03 square condition.

`BRIDGE_REQUIRES:` W3-A difference-of-squares factor enumeration.

`APPLIES:` W3-B parity and W3-C bounds.

`EXPORTS:` integer-quadratic square-filter pipeline, not discriminant canon.

## O. Lead integration notes
Introduce this after factor/bound tools, so the borrowed discriminant immediately feeds the familiar finite-case router. Keep the ALG-03 bridge short. The error-sensitive checkpoint is `(m,n)=(5,-1)`, where `|m-n|=6`.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
