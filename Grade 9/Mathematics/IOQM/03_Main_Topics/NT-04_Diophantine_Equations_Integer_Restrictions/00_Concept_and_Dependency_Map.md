# Concept and Dependency Map - Diophantine Equations & Integer Restrictions

## Governing learner router
`INTEGER TARGET -> TRANSFORM -> CHEAPEST FILTER -> FINITE CANDIDATES -> RECONSTRUCT -> ORIGINAL CHECK`

An equation over integers is not merely a real equation whose answers happen to be integers. Integrality creates extra filters: signs, parity, gcd, divisibility, bounded factor pairs, square feasibility and exact rational gaps.

## Scope boundary
Canonical here: integer factorisation into cases; parity/gcd filters; bounds; exact rational approximation; perfect-square/discriminant feasibility as a narrow bridge; sum/product reconstruction; finite-case completeness.

Retrieval only: prime-exponent/divisor/perfect-power facts from the frozen divisor/perfect-power provider; strategic transformation/equivalence from the frozen algebra provider; discriminant/root facts only as a narrow quadratic bridge. Generic gcd/lcm, prime factorisation and polynomial theory are not retaught.

## Knowledge dependency map
| Need | Learner may already know | Missing bridge | Disposition |
|---|---|---|---|
| factor an expression | school factorisation | factors become integer cases | owned here |
| gcd/parity | routine HCF/even-odd | use them as early eliminators | owned application; retrieve gcd meaning |
| prime exponents | factorisation of numbers | block allocation/perfect-square filters | retrieve frozen divisor/perfect-power interface |
| transform equations | expansion/factorisation | preserve equivalence and original checks | retrieve frozen algebra interface |
| quadratic roots | formula/discriminant | integer root requires square discriminant | narrow bridge only |
| bounds | inequalities | bound before enumeration | owned here |
| rational closeness | decimals | scaled error is an integer | owned here |
| completeness | trial-and-error | prove every case is represented | owned here |

## Method-selection map
| Visible surface | First structural question | Cheapest first move | Nearby wrong route |
|---|---|---|---|
| product equals constant | are factors integral and bounded? | list signed/positive factor pairs | unrestricted search |
| fixed product extremum | are variables integral? | compare divisor pairs near sqrt(N) | continuous optimum only |
| coprime product | what prime-power blocks can split? | allocate whole blocks | count all divisors |
| difference of squares | do factors need same parity? | set (x-y)(x+y)=N | scan squares |
| sum and product | is target symmetric? | reconstruct via S,P | solve two variables first |
| quadratic integer root | must discriminant be a square? | compute discriminant and square filter | use real-root existence only |
| rational near p/q | can scaled error be integral? | minimize |qa-pb| | decimal rounding |
| many variables | can one relation eliminate a variable? | substitute sum/product constraint early | nested loops |
| finite list found | is it exhaustive? | state bijection between cases and solutions | stop after examples |
| one-way manipulation | could extraneous candidates appear? | check original equation | trust transformed relation |

## Transfer map
- integer rectangle optimisation -> factor-pair optimisation;
- coprime factor reconstruction -> prime-power block allocation;
- rational approximation -> determinant/gap arithmetic;
- quadratic integer point -> square discriminant filter;
- geometry/mensuration equation -> integer factor cases;
- equal sum/product representations -> multiplicative partitions plus appended ones.

## Prerequisite interface custody
- NT-03 stable divisor/perfect-power interface: blob `49ed09f2ea0f145fba2051da6d0ab8e08bdb5842`.
- ALG-01 stable transformation/equivalence interface: blob `fc685ff0a2e9bd67fbd6a920e730b7fff633404b`.
- ALG-03 stable polynomial/root interface: blob `03382e63be5a52bade27bf4034a0a23631f5a2bd`; only discriminant/perfect-square feasibility is consumed.

Static architecture state: WAVE0_ARCHITECTURE_FROZEN.
