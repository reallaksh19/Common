---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-C
microstream_title: Bounds and feasibility filters
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1]
source_cutoff: 2026-09-02
---

# Bounds and feasibility filters - Research Interface

## A. Scope boundary
Included: proving finite ranges from positivity, order, product/sum constraints and elementary monotonicity; using a bound as a completeness certificate for later enumeration. Excluded: canonical AM-GM/Cauchy teaching and equality/attainment doctrine (ALG-02).

## B. Learner-state model
`PRIOR_KNOWLEDGE:` school inequalities and ordering.

`LIKELY_HALF_KNOWLEDGE:` learner uses a convenient numerical cutoff without proving it.

`MISSING_BRIDGES:` distinguish a heuristic search range from a logically forced range; combine sign/order with factor size; use a continuous bound only to narrow integer candidates.

`OWNERSHIP_TARGET:` make every finite search interval justified and auditable.

## C. Mathematical invariant / governing structure
**Invariant:** `A SEARCH IS A PROOF ONLY AFTER THE RANGE IS FORCED`.

Examples: positive `uv=N` with `u<=v` gives `u<=sqrt(N)`; positive `u+v=S` gives `1<=u<=S-1`; a square-valued expression must be nonnegative; a positive divisor of N lies between 1 and `|N|`. A continuous inequality may supply a bound, but final integer attainability belongs to the discrete set.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| positive fixed product | square-root bound | assume smaller factor first | positivity/order | test all integers |
| fixed sum | finite interval | isolate one variable | positivity | leave an infinite search |
| square/nonnegative target | sign feasibility | impose `E>=0` | real square condition | take square roots prematurely |
| monotone expression | threshold | compare to target | monotonicity proved | numerical pattern only |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| "minimum" | finite integer set | continuous optimizer only | Must variables be integers? | AM-GM is neat |
| trial values | prove cutoff | stop when pattern seems clear | Why can no later value work? | computations look convincing |
| factor pairs | use sqrt symmetry | list both orders | Is order relevant? | duplicates feel safer |
| square equation | nonnegative bound | solve real equation | Is integrality decisive? | real algebra is familiar |

## F. Misconception / diagnosis catalogue
`NT04-BND-01`
- WRONG_MOVE: "checked up to 100, so no solution."
- WHY_TEMPTING: many contest examples have small answers.
- MISSING_LINK_CLASS: DISCRETE_FILTER.
- REPAIR_INVARIANT: derive a forced upper/lower bound.
- FALSIFIER_OR_CONTRAST: a valid solution at 1001 defeats the search.

`NT04-BND-02`
- WRONG_MOVE: use continuous equality at a noninteger point and report it.
- WHY_TEMPTING: the bound is elegant.
- MISSING_LINK_CLASS: DOMAIN_CONDITION.
- REPAIR_INVARIANT: continuous bound locates candidates; integer constraints decide attainability.
- FALSIFIER_OR_CONTRAST: area 20 rectangle has real square side `sqrt(20)`, not integral.

`NT04-BND-03`
- WRONG_MOVE: double-count `(u,v)` and `(v,u)` when order is irrelevant.
- WHY_TEMPTING: ordered algebraic pairs appear naturally.
- MISSING_LINK_CLASS: REPRESENTATION.
- REPAIR_INVARIANT: normalize order before enumeration.
- FALSIFIER_OR_CONTRAST: rectangle side pair 4x5 is one shape, not two.

## G. First-move cues
- positive integers and fixed product -> order them and bound smaller factor by `sqrt(product)`.
- positive integers and fixed sum -> write the forced finite interval.
- square equals expression -> impose nonnegativity, then integrality.
- largest/smallest -> ask whether feasibility is already finite before optimizing.

## H. H3 -> H0 fading plan
- **H3:** bound the smaller factor in `uv=180`.
- **H2:** positive `u+v=41` plus a product condition; derive u's range.
- **H1:** square-valued expression; state only the first feasibility inequality.
- **H0:** integer optimization where a real lower bound narrows to two factor pairs.

## I. Validated IOQM source anchors
Direct primary anchor: `IOQM-2025-Q03`. Supportive use: `IOQM-2023-Q11` and `IOQM-2024-Q13`.

## J. Source-independent mathematical trace
- 2025-Q03: continuous rectangle optimum is not itself an integer-side solution; complete factor pairs give minimum perimeter 18.
- 2023-Q11: factorisation of 231 makes the candidate set finite exactly, so arbitrary n-bounds are unnecessary.
- 2024-Q13: positivity and `a>c` reject divisor branches after c is finite.

## K. Contrast-pair candidates
1. heuristic cutoff vs proved bound;
2. continuous minimum vs integer attainable minimum;
3. ordered pair vs unordered factor pair;
4. nonnegative feasibility vs integer-square feasibility;
5. bound as pre-filter vs bound as final answer.

## L. Transfer candidates
- **T2:** bound a divisor variable by square-root symmetry.
- **T3:** integer rectangle vs real rectangle optimization.
- **T3:** packing context with integer dimensions.
- **T4:** geometry-to-integer bridge where a metric formula yields a finite factor set.

## M. Candidate mastery items
- Recognition: identify which statement actually proves a search finite.
- First-line: for positive `uv=420`, write a bound for the smaller factor.
- Full solve: integer rectangle area 72 with side difference at least 3; minimize perimeter.
- WHY-NOT: reject "the real optimum is `2sqrt(N)`, so that is the integer answer."
- Verification: explain why every tested candidate lies inside the proved interval.

## N. Dependency declarations
`REQUIRES:` elementary order/positivity.

`BRIDGE_REQUIRES:` ALG-02 only if a nontrivial inequality theorem is invoked; avoid it where unnecessary.

`APPLIES:` W3-A factor cases and W3-B filters.

`EXPORTS:` proof-of-range discipline for any later finite enumeration.

## O. Lead integration notes
Teach the epistemic rule "finite search needs a certificate" once, then enforce it throughout. Do not build an inequality mini-course. Prefer structural bounds from products, sums and signs that a Grade-9 learner can reconstruct.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
