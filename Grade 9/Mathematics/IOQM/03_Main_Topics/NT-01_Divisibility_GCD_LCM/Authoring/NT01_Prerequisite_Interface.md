# NT-01 Stable Prerequisite Interface

main_topic_id: `IOQM-G9-NT-01`  
status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`  
canonical_teaching_owner: `IOQM-G9-NT-01`

This interface is authoring/control material and is not part of the student export.

## Prerequisites

- `G9_CORE`: integer arithmetic; factors/multiples; division with remainder; elementary algebraic manipulation.
- `IOQM_BRIDGE`: implication/equivalence; exact integer reasoning; short proof by rewriting divisibility as an integer equation.
- No dependency on NT-02 congruence notation.
- No dependency on NT-03 prime-exponent/divisor-count canon.

## Concepts owned

1. `a|b` means `b=ak` for an integer `k`.
2. Common divisors are closed under integer linear combinations.
3. **Euclid's Lemma:** if prime `p|ab`, then `p|a` or `p|b`; primality is a mandatory hypothesis.
4. `gcd(a,b)=gcd(b,a-qb)` for integer `q`.
5. Euclidean algorithm as repeated invariant-preserving reduction.
6. Equal-remainder divisor problems reduce to gcd of differences.
7. Prescribed-remainder number construction reduces to a common multiple after subtracting the remainder.
8. LCM as least positive common multiple / synchronization point.
9. For positive integers, `gcd(a,b)*lcm(a,b)=ab`.
10. Reconstruction by `a=gu`, `b=gv`, `gcd(u,v)=1`, `uv=L/g`.
11. Divisibility transitivity and chains.

## Retrieval cues

- prime `p` divides a product -> check primality, then split by Euclid's Lemma;
- "same remainder" -> first ask what is unknown;
- "greatest divisor" -> common-divisor/difference structure;
- "least divisible by" / "first together" -> common multiple/lcm;
- large gcd pair -> Euclidean reduction;
- gcd+lcm both given -> product invariant, then normalize if pair required;
- nested `a|b|c` -> chain/transitivity;
- common divisor of algebraic expressions -> integer linear combination.

## First-move rules

1. Prime divisor of product: if `p` is prime and `p|ab`, invoke Euclid's Lemma only after checking primality.
2. Unknown divisor + equal remainders: `d|(x_i-x_j)`.
3. Unknown number + prescribed remainder `r`: write `N-r` as a common multiple.
4. Large gcd: write one division-with-remainder equation.
5. Common divisor of expressions: choose integer coefficients that cancel a variable/term.
6. gcd/lcm pair reconstruction: `a=gu`, `b=gv`, `gcd(u,v)=1`, `uv=L/g`.
7. Divisibility chain: compress by transitivity before enumeration.

## Decision boundaries

- prime divisor of product vs arbitrary composite divisor of product;
- divisor target vs common-multiple target;
- unknown divisor same-remainder vs unknown number prescribed-remainder;
- one-number divisibility test vs structural divisibility reasoning;
- Euclid vs full factorization;
- product-only use of `gL=ab` vs actual pair reconstruction;
- independent divisibility checks vs chain/transitivity;
- NT-01 difference language vs NT-02 congruence notation.

## Misconception traps

- applying Euclid's Lemma to a composite divisor (e.g. `6|2*3` does not imply `6|2` or `6|3`);
- using lcm whenever the phrase "same remainder" appears;
- taking gcd of the original numbers instead of their differences in equal-remainder divisor problems;
- defaulting to prime factorization for every gcd;
- using digit divisibility tests on variable-expression problems;
- assuming `gL=ab` uniquely determines the pair;
- forgetting `gcd(u,v)=1` after normalization;
- reteaching congruence/cancellation rules inside downstream topics instead of routing to NT-02;
- importing prime-exponent/divisor-count doctrine from NT-03 into NT-01.

## Reusable identities and lemmas

- `d|A`, `d|B` -> `d|(rA+sB)` for all integers `r,s`.
- **Euclid's Lemma:** prime `p|ab` -> `p|a` or `p|b`.
- `gcd(a,b)=gcd(b,a-qb)`.
- equal remainder modulo divisor `d` -> `d|(a-b)`.
- prescribed remainder `r` under divisors `m_i` -> each `m_i | (N-r)`.
- `gcd(a,b)*lcm(a,b)=ab` for positive integers.
- `a=gu`, `b=gv`, `gcd(u,v)=1`, `lcm(a,b)=guv`.
- `a|b` and `b|c` -> `a|c`.
- if `a|b`, then `gcd(a,b)=a`, `lcm(a,b)=b`.

## Downstream assumptions

### NT-02 may assume
- divisibility meaning;
- `d|(a-b)` as the underlying equal-remainder fact;
- gcd meaning and Euclidean computation;
- but must teach congruence notation, legal modular operations, inverses/cancellation, power cycles and its own bounded Euler bridge itself.

### NT-03 may assume
- factors/multiples and gcd/lcm structural meaning;
- **Euclid's Lemma as an exported NT-01 result** when prime divisibility must split across a product;
- but owns prime factorisation, exponent/valuation structure, divisor counts and perfect powers.

### NT-04 may assume
- common-divisor linear-combination filters and gcd divisibility restrictions;
- but owns full Diophantine reconstruction/filtering doctrine.

### COMB-04 may retrieve
- divisibility/parity-style invariant language as a bridge;
- but adversarial game/invariant strategy remains COMB-04 canon.

## Interface QA

- source anchors checked: PASS (`IOQM-2025-Q02`, `IOQM-2025-Q27`);
- promoted anchor answers independently recomputed: PASS (17, 40);
- Euclid's Lemma bridge statement/proof boundary: PASS_STATIC;
- dependency inversion: NONE;
- NT-02 canon duplicated: NO;
- NT-03 canon duplicated: NO;
- downstream status: `READY_FOR_RETRIEVAL`.
