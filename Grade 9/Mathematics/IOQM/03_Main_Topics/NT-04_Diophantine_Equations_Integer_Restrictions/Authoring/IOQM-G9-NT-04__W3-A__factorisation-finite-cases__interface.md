---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-A
microstream_title: Factorisation into finite integer cases
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1, NT03_Stable_Divisor_PerfectPower_Interface_v1]
source_cutoff: 2026-09-02
---

# Factorisation into finite integer cases - Research Interface

## A. Scope boundary

Included: rearranging integer equations to products, shifted products and divisor relations; parameterising all factor pairs; restoring sign/order/positivity restrictions. Excluded: general factorisation instruction (ALG-01), divisor-count theorem (NT-03), and polynomial root canon (ALG-03). The stream owns the step from a structural rewrite to a **proved complete finite candidate set**.

## B. Learner-state model

`PRIOR_KNOWLEDGE:` learner can factor routine expressions and list factors of a fixed integer.

`LIKELY_HALF_KNOWLEDGE:` learner recognizes a factorisation after seeing it but may still test values first.

`MISSING_BRIDGES:` shifted-variable products; sign-aware factor pairs; proof that every integer solution corresponds to one listed pair.

`OWNERSHIP_TARGET:` convert an integer equation into exhaustive factor/divisor cases and reconstruct.

## C. Mathematical invariant / governing structure

**Invariant:** `PRODUCT = FIXED INTEGER` converts an unbounded-looking integer search into the divisors of one fixed number.

If `(u-r)(v-s)=N`, every integer solution corresponds to an ordered factor pair `(d,N/d)` of `N`, with `u=r+d` and `v=s+N/d`. Conversely every divisor `d|N` gives a candidate pair, subject to the original restrictions. This two-way correspondence is the completeness proof. For negative `N`, factor signs differ; for positive `N`, signs match. Additional positivity, order, parity or gcd conditions are filters on this complete list.

## D. Representation inventory

| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| expanded bilinear equation | hidden product | collect to `(u-r)(v-s)=N` | preserve equivalence | scan integer pairs |
| fixed product `uv=N` | finite divisors | list/parameterise divisors | include sign cases | use only positive pairs automatically |
| factor pair plus sum/order | reconstruction | combine sum or inequality | check all constraints | stop after product fits |
| quotient integral | divisor relation | rewrite as `d|N` | denominator nonzero | approximate quotient |

## E. Decision boundaries

| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| `uv=N` | enumerate factor pairs | continuous optimization | Are u,v integers? | AM-GM is familiar |
| bilinear equation | shift/factor | substitute many values | Can adding a constant complete a product? | variables look independent |
| `d|N` | finite divisor cases | divisor-count formula | Need actual admissible values or only count? | NT-03 formula is nearby |
| positive variables | positive factors only | signed factors | Does the transformed variable preserve positivity? | shift can change sign |

## F. Misconception / diagnosis catalogue

`NT04-FAC-01`
- WRONG_MOVE: test u=1,2,3,... without a bound.
- WHY_TEMPTING: integer problems invite search.
- MISSING_LINK_CLASS: REPRESENTATION.
- REPAIR_INVARIANT: expose a fixed product.
- FALSIFIER_OR_CONTRAST: `(u-100)(v+7)=12` has remote solutions found instantly by factors.

`NT04-FAC-02`
- WRONG_MOVE: list only positive divisors because original variables are positive.
- WHY_TEMPTING: sign restriction is copied through a shift incorrectly.
- MISSING_LINK_CLASS: DOMAIN_CONDITION.
- REPAIR_INVARIANT: apply sign restrictions to transformed variables, then reconstruct.
- FALSIFIER_OR_CONTRAST: `u>0` does not imply `u-5>0`.

`NT04-FAC-03`
- WRONG_MOVE: claim the listed cases are all without a correspondence proof.
- WHY_TEMPTING: the list looks finite.
- MISSING_LINK_CLASS: INVARIANT.
- REPAIR_INVARIANT: every solution determines a divisor, and every divisor reconstructs a candidate.
- FALSIFIER_OR_CONTRAST: a hand-picked subset of factors may miss a valid branch.

## G. First-move cues

- "integer product is fixed" -> write `uv=N` and a divisor parameter.
- "terms look like `uv-u-v`" -> try adding 1 to form `(u-1)(v-1)`.
- "positive integers plus bilinear relation" -> isolate a product before checking values.
- "find all / largest / smallest" -> build the complete factor-pair set before optimizing.

## H. H3 -> H0 fading plan

- **H3:** `(x-2)(y+1)=18`; table all signed factor pairs and reconstruct.
- **H2:** `xy-3x+2y=12`; cue: complete a shifted product.
- **H1:** positive integers satisfy a bilinear relation; ask only for the first useful rewrite.
- **H0:** changed-surface integer-dimension item; derive the fixed product independently before optimizing.

## I. Validated IOQM source anchors

| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| `IOQM-2025-Q03` | 2025/03 | CLEAN_OFFICIAL | primary | factor pairs; discrete optimum | no | FINAL_OFFICIAL |
| `IOQM-2024-Q13` | 2024/13 | CLEAN_OFFICIAL | primary | shifted factorisation; finite cases | no | OFFICIAL_HBCSE_KEY |
| `IOQM-2023-Q04` | 2023/04 | CLEAN_VALIDATED + metadata overlay | primary | divisibility/factorisation | no | EMBEDDED_KEY |

## J. Source-independent mathematical trace

- **2025-Q03:** factor pairs of 20 give perimeters 42,24,18; minimum 18.
- **2024-Q13:** `(a-b)(c-1)=66-c`, hence `a-b=65/(c-1)-1`, so `c-1|65`; only `(19,7,6)` survives positivity, sum and `a>c`.
- **2023-Q04:** exact source has `x^4`; `x-1|2`, yielding only `(x,y)=(3,4)`.
All promoted answers agree with their governing keys under the explicit correction overlay.

## K. Contrast-pair candidates

1. fixed product vs continuous optimization;
2. actual factor values vs divisor count;
3. original positivity vs shifted-factor sign;
4. factorisation proof vs numerical search;
5. necessary product relation vs full original-system sufficiency.

## L. Transfer candidates

- **T2 representation:** `xy+x+y=35` -> `(x+1)(y+1)=36`.
- **T2 sign:** integer solutions of `(x-3)(y+4)=-20`.
- **T3 geometry:** integer rectangle/perimeter after a fixed area.
- **T4 algebra bridge:** a discriminant-square condition becomes a difference-of-squares product.

## M. Candidate mastery items

- Recognition-only: Which of four equations should first be rewritten as a fixed product?
- First-line-only: Rewrite `xy-4x-3y=1` into shifted-product form.
- Full solve: Find all positive integer solutions of `(x-2)(y-1)=24` with `x<y`.
- WHY-NOT: Explain why testing `x<=10` is not a proof unless a bound was established.
- Verification: Given a candidate pair from a divisor case, check it in the original unshifted equation.

## N. Dependency declarations

`REQUIRES:` ALG-01 factorisation/equivalence; NT-03 factor structure.

`BRIDGE_REQUIRES:` NT-01 divisibility language when a quotient is isolated.

`APPLIES:` factor lists, sign/order filters.

`EXPORTS:` product-to-divisor correspondence; completeness language for finite factor cases.

## O. Lead integration notes

Teach the solution <-> factor-pair correspondence once near the start of the integrated book. Later streams should retrieve it in one sentence. Do not rederive divisor-count formulas. Place this before parity/bounds so later filters operate on a logically complete candidate generator.

## P. Independent QA status

DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
