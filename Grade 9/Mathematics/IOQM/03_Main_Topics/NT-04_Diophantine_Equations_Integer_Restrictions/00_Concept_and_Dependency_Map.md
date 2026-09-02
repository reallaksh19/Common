# NT-04 - Concept and Dependency Map

Status: `WAVE0_ARCHITECTURE_FROZEN`
Main topic: `IOQM-G9-NT-04`
Canonical owner: `IOQM-G9-NT-04`
Production wave: 3

## Governing model

`INTEGER CONDITION -> STRUCTURAL REWRITE -> NECESSARY FILTERS -> FINITE CASE SET -> COMPLETE ENUMERATION -> CHECK ORIGINAL -> REPORT / OPTIMIZE`

The distinguishing habit is not "try small integers." It is to prove that only finitely many
cases can survive before checking them. Integer conditions become useful when factorisation,
divisibility, parity, gcd, bounds, perfect-square conditions or exact rational gaps force a
small admissible set.

## Scope boundary

### Canonically taught here

- converting an integer equation into a finite factor/divisor/parameter case set;
- combining parity, gcd, sign and divisibility filters with that case set;
- using bounds to prove a search interval is complete rather than merely convenient;
- exact rational-approximation gaps of the form `|qa-pb|`, including determinant/Farey-style
  reasoning needed by the validated anchors;
- using a quadratic discriminant only as a bridge to a perfect-square integer condition, then
  returning to finite integer factorisation;
- reconstructing integer solutions from sum/product or related substitutions;
- proving completeness, checking the original condition and applying the requested optimization.

### Retrieved, not retaught

| Mechanism | Disposition | Canonical provider |
|---|---|---|
| factor vs expand; substitution; equivalence discipline | `PREREQUISITE_RETRIEVAL_ONLY` | ALG-01 |
| prime factorisation; divisor/perfect-power structure; coprime factor blocks | `PREREQUISITE_RETRIEVAL_ONLY` | NT-03 |
| divisibility, gcd/lcm, Euclidean facts | `PREREQUISITE_RETRIEVAL_ONLY` | NT-01 |
| discriminant/root behavior | `CROSS_DOMAIN_BRIDGE` | ALG-03 |
| inequality/equality/attainment doctrine | `APPLICATION_ONLY` | ALG-02 |

### Explicit non-ownership

- no second chapter on divisor counting or perfect powers;
- no full derivation of Vieta/discriminant doctrine;
- no general continued-fraction course;
- no generic inequality optimization course;
- no uncontrolled computer/brute-force search as a proof of completeness.

## Grade-9 adaptation tags

| Knowledge | Tag | Treatment |
|---|---|---|
| integer arithmetic, factors, parity, simple equations | `G9_CORE` | retrieve |
| factorisation/substitution with condition checks | `G9_CORE` / `IOQM_BRIDGE` | retrieve ALG-01, bridge only as needed |
| divisor/perfect-square signatures | `IOQM_BRIDGE` | retrieve NT-03 |
| exact determinant gap for nearby fractions | `IOQM_BRIDGE` | teach here at the required level |
| discriminant -> square condition | `JUST_IN_TIME_ADVANCED_LANGUAGE` | retrieve ALG-03, use only the square test |
| continued fractions as a general algorithm | `DEFERRED` | not required |

## Knowledge Dependency Map

1. **Retrieve algebraic rewriting.**
   Learner can factor/rearrange and knows one-way transformations require checking.
2. **Retrieve integer structure.**
   Learner can use divisibility, parity, gcd and prime/factor structure without re-onboarding.
3. **Bridge: equation -> necessary integer condition.**
   Examples: a product equals a fixed integer; a quotient must be integral; a discriminant
   must be a square; a rational gap numerator must be a nonzero integer.
4. **Own: necessary filters -> finite candidate set.**
   The student must know why every solution appears in the list.
5. **Own: reconstruct and check.**
   Recover original variables, restore sign/order/positivity restrictions and test the original equation.
6. **Own: optimize only over the surviving complete set.**
   Maximum/minimum/closest/largest questions are answered after structural reduction, not before.

No downstream step may use "enumerate the finite cases" until the source of finiteness has been proved.

## Method Selection Map

| Visible surface | Structural question | First move | Nearby route to reject |
|---|---|---|---|
| product/area fixed, integer sides | Are candidates exactly factor pairs? | write the factor pairs or divisor parameter | continuous optimum alone |
| polynomial-looking integer equation | Can terms be grouped into a product? | move terms to expose a factorisation | blind two-variable search |
| quotient/integrality condition | What must divide what? | isolate the divisor relation | decimal approximation |
| fraction lies between close rationals | Can cross-products become positive integer gaps? | define determinant gaps | compare decimals |
| quadratic expression must be a square | Does the discriminant become a square? | retrieve discriminant, set it to `k^2` | solve over reals and round |
| sum and product both constrained | Can ones/nonessential terms be separated? | pass to multiplicative partitions / symmetric data | list ordered compositions |
| optimization over integers | Is the feasible set already finite? | build complete candidate set first | optimize a continuous relaxation and stop |
| parity/gcd appears | Does it eliminate whole branches? | apply the filter before enumeration | enumerate then notice parity |

## Transfer Map

| Original mechanism | Changed surface | Transfer type | Preserved invariant |
|---|---|---|---|
| integer rectangle area | integer factor pair with fixed product | context change | complete factor-pair set |
| three-variable system | shifted product equation | representation change | divisor of fixed constant |
| closest fraction | lattice/determinant gap | representation change | nonzero integer cross-product |
| quadratic square condition | difference of squares | representation change | factor pairs of fixed constant |
| product=sum representation | multiplicative partition | representation change | product fixed; ones pad sum |
| geometric integer length | Diophantine factor filter | cross-domain bridge | discrete feasible set |
| real optimum vs integer optimum | nearest factor pair | discrete/continuous change | continuous bound does not certify attainability |

## Internal dependency order

1. structural rewrite and finite-case principle;
2. factor/divisor parameterisation;
3. sign, parity, gcd and divisibility filters;
4. bounding and feasibility;
5. exact rational-gap/determinant method;
6. discriminant/perfect-square bridge;
7. sum/product reconstruction and multiplicative partitions;
8. completeness, original-condition checking and optimization;
9. mixed transfer and source-integrity audit.

## Decision contrasts

1. **Real equation vs integer equation:** a real solution family may collapse to a finite lattice set.
2. **Brute-force search vs structural factorisation:** testing values is evidence only after a proved bound; a factorisation can prove completeness immediately.
3. **Continuous optimum vs discrete factor pairs:** AM-GM may locate the center, but integer factor pairs decide attainability.
4. **Factor pair vs divisor count:** NT-04 enumerates admissible factors; NT-03 owns the divisor-count theorem.
5. **Parity as decoration vs parity as branch killer:** apply parity before expanding the case tree.
6. **Decimal closeness vs exact rational closeness:** compare integer cross-products, not rounded decimals.
7. **Quadratic formula vs square filter:** the discriminant bridge creates an integer square condition; NT-04 owns the resulting finite reconstruction.
8. **Necessary condition vs sufficient solution:** every generated candidate returns to the original condition.
9. **A finite list vs a complete finite list:** the proof must explain why no omitted integer can work.
10. **Sum/product composition vs multiplicative partition:** order and inserted ones must be normalized before counting representations.

## Historical source set

Validated anchors:
`IOQM-2025-Q03`, `IOQM-2025-Q11`, `IOQM-2024-Q13`,
`IOQM-2023-Q03`, `IOQM-2023-Q04`, `IOQM-2023-Q11`, `IOQM-2023-Q29`.

Source correction: `IOQM-2023-Q04` uses `x^4`, not the stale extracted `x/4`.
The historical source is clean; only repository classifier metadata required correction.

No official Grade-9-only syllabus or topic-frequency claim is inferred from this seven-item set.
