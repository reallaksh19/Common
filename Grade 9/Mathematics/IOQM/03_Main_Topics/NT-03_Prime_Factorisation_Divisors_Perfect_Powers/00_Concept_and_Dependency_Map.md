# NT-03 - Concept and Dependency Map

Status: `WAVE0_ARCHITECTURE_FROZEN`
Canonical owner: `IOQM-G9-NT-03`

## Governing model

`INTEGER -> PRIME EXPONENT VECTOR -> CONSTRAINT ON EXPONENTS -> COUNT / RECONSTRUCT -> CHECK`

The chapter treats prime factorisation as a coordinate system for positive integers. Once
`n = p1^a1 ... pr^ar` is fixed, divisibility, divisor counts, perfect powers, squarefree
structure, valuations and many factor-pair restrictions become statements about the
exponents `a_i`.

## Prerequisites and ownership

| Concept | Disposition | Provider |
|---|---|---|
| factors/multiples; gcd/lcm meaning | PREREQUISITE_RETRIEVAL_ONLY | NT-01 stable interface |
| Euclidean algorithm / same-remainder gcd | PREREQUISITE_RETRIEVAL_ONLY | NT-01 |
| Fundamental Theorem of Arithmetic | CANONICAL_TEACHING_OWNER | NT-03 |
| prime exponent vectors and valuations | CANONICAL_TEACHING_OWNER | NT-03 |
| divisor counting and divisor parity | CANONICAL_TEACHING_OWNER | NT-03 |
| perfect squares/cubes/k-th powers | CANONICAL_TEACHING_OWNER | NT-03 |
| squarefree structure | CANONICAL_TEACHING_OWNER | NT-03 |
| factor-pair restrictions from exponent allocation | CANONICAL_TEACHING_OWNER | NT-03 |
| general integer-equation reconstruction | DOWNSTREAM_APPLICATION_ONLY | NT-04 |

## Internal dependency order

1. unique prime factorisation;
2. exponent-vector divisibility;
3. divisor counting;
4. perfect powers and squarefree structure;
5. valuations, including factorial valuations;
6. factor-pair restrictions and extremal reconstruction;
7. source-integrity audit and mixed transfer.

## Decision contrasts

1. **Need gcd/lcm only?** Retrieve NT-01. **Need prime multiplicities?** Use the exponent vector here.
2. **Need all divisors?** Exponents range independently. **Need factor pairs?** Pair complementary exponent choices.
3. **Perfect square?** Every exponent is even. **Squarefree?** Every exponent is 0 or 1.
4. **Number of divisors odd?** Test whether the number is a square; do not enumerate.
5. **Divides a factorial?** Compare valuations prime by prime; do not multiply the factorial.
6. **Smallest number with a given divisor count?** Allocate larger exponents to smaller primes.
7. **Product `xy=N` with `gcd(x,y)=1`?** Whole prime-power blocks must go to one side.
8. **Perfect k-th power?** `k` divides every prime exponent; the greatest possible `k` is their gcd.

## Source set

Historical anchors: `IOQM-2025-Q06`; `IOQM-2024-Q01,Q25,Q28,Q29`;
`IOQM-2023-Q01,Q09,Q30`.

No official topic frequency or Grade-9-only syllabus claim is inferred from this set.
