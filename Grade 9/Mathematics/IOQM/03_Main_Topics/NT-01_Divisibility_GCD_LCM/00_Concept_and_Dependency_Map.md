# IOQM Grade 9 — NT-01 Divisibility, GCD, LCM & Euclidean Structure

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Learner entry model

Assume the learner can compute HCF/LCM and knows routine divisibility tests, but may not yet see gcd/lcm as **structural tools** for reducing a problem.

## Governing idea

> When several integers share a divisibility condition, look for a quantity that is unchanged by subtraction, common multiples, or Euclidean reduction.

## Knowledge dependency map

```text
G9 integer arithmetic + factorisation
        |
        v
meaning of a | b
        |
        +--> common divisor language
        |       |
        |       +--> gcd invariance under subtraction
        |       |       |
        |       |       +--> Euclidean algorithm
        |       |       +--> gcd of differences
        |       |
        |       +--> same-remainder problems
        |
        +--> common multiple language
                |
                +--> lcm reconstruction
                +--> simultaneous divisibility

stable NT-01 interface
        |
        +--> NT-02 modular arithmetic
        +--> NT-03 prime/divisor structure
        +--> NT-04 Diophantine filters
        +--> COMB-04 parity/residue invariants
```

## Method-selection router

1. **Asked whether one number divides another?** Translate to `b = ak`.
2. **Same unknown divisor leaves equal remainders?** Subtract the numbers; the divisor divides their differences.
3. **Need greatest possible common divisor?** Reduce with gcd / Euclidean algorithm.
4. **Need least number satisfying several divisibility requirements?** Think lcm / common multiple construction.
5. **Both gcd and lcm are given for two positive integers?** Consider `gcd(a,b) * lcm(a,b) = ab`.
6. **Problem is really about prime exponents/divisor count?** Route to NT-03; do not duplicate that canon here.

## Canonical concept ownership

NT-01 owns:
- divisibility meaning;
- gcd/lcm as structural relations;
- Euclidean algorithm;
- gcd invariance under integer linear combinations;
- same-remainder -> difference reduction;
- lcm reconstruction.

NT-03 owns prime-exponent/divisor-count theory. NT-02 owns congruence notation and modular cycles.

## Transfer map

```text
same remainder
    -> subtract
    -> gcd of differences
    -> Euclidean reduction
    -> Diophantine filtering

multiple conditions
    -> common multiple
    -> lcm
    -> synchronization/cycle problems
```

## Mandatory contrasts

- gcd vs lcm;
- divisor of each number vs divisor of their difference;
- same-remainder divisor problem vs construct-a-number multiple problem;
- divisibility structure vs prime-exponent structure.

## Exit belief

A successful learner should say:

> “I do not start by factoring everything. I first ask whether subtraction, gcd, lcm, or Euclidean reduction exposes the invariant.”
