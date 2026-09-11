# IOQM Grade 9 - NT-01 Divisibility, GCD, LCM & Euclidean Structure

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Learner entry model

The learner is assumed to know routine factors, multiples, HCF/LCM calculations and common divisibility tests, but may not yet recognize divisibility as a structural relation that can be transformed.

## Governing router

Before calculating, ask:

1. Is the target a **divisor** or a **multiple**?
2. Are equal remainders hiding a **difference**?
3. Can I shrink numbers without changing their common divisors?
4. Is a prescribed remainder removed by subtracting it first?
5. Is a divisibility chain already telling me the gcd or lcm?
6. If gcd and lcm are both known, should I normalize the pair before casework?

Compressed learner rule:

`TARGET -> DIVISOR/MULTIPLE -> DIFFERENCE/REDUCTION -> GCD/LCM -> CHECK`

## Knowledge dependency map

| Node | Adaptation tag | What is assumed / taught |
|---|---|---|
| integer arithmetic, multiplication, division with remainder | `G9_CORE` | prerequisite retrieval |
| factor and multiple language | `G9_CORE` | prerequisite retrieval |
| implication/equivalence and exact integer reasoning | `IOQM_BRIDGE` | short proof habit bridge |
| `a|b` as `b=ak` for integer `k` | `IOQM_BRIDGE` | NT-01 canonical teaching |
| closure under integer linear combinations | `IOQM_BRIDGE` | NT-01 canonical teaching |
| gcd invariance under `a -> a-qb` | `IOQM_BRIDGE` | NT-01 canonical teaching |
| Euclidean algorithm | `IOQM_BRIDGE` | NT-01 canonical teaching |
| same-remainder -> differences | `IOQM_BRIDGE` | NT-01 canonical teaching |
| prescribed remainder -> common multiple after subtraction | `IOQM_BRIDGE` | NT-01 canonical teaching |
| gcd/lcm structural identities and reconstruction | `IOQM_BRIDGE` | NT-01 canonical teaching |
| divisibility chains | `IOQM_BRIDGE` | NT-01 canonical teaching |
| congruence notation, residue legality, power cycles | `DEFERRED` | canonical owner NT-02 |
| prime-exponent/divisor-count canon | `DEFERRED` | canonical owner NT-03 |

Dependency flow:

```text
G9 integer arithmetic + factor/multiple meaning
        |
        v
     a | b  <->  b = ak
        |
        +--> integer linear combinations
        |       |
        |       +--> gcd invariance under subtraction
        |               |
        |               +--> Euclidean algorithm
        |               +--> gcd of differences
        |                       |
        |                       +--> same-remainder divisor problems
        |
        +--> common multiple language
        |       |
        |       +--> prescribed-remainder reconstruction
        |       +--> lcm / synchronization
        |
        +--> divisibility chains
        |
        +--> gcd-lcm normalization and reconstruction
```

## Canonical ownership and overlap dispositions

| Concept | Disposition in NT-01 |
|---|---|
| divisibility meaning/algebra | `CANONICAL_TEACHING_OWNER` |
| Euclidean algorithm | `CANONICAL_TEACHING_OWNER` |
| gcd/lcm structural use | `CANONICAL_TEACHING_OWNER` |
| same-remainder/difference structure | `CANONICAL_TEACHING_OWNER` |
| divisibility chains | `CANONICAL_TEACHING_OWNER` |
| modular congruence notation and legal cancellation | `ROUTE_TO_NT-02` / retrieval only downstream |
| prime-exponent, divisor-count and perfect-power canon | `ROUTE_TO_NT-03` / no duplicate derivation |
| Diophantine reconstruction beyond basic gcd filters | `APPLICATION_ONLY`; canonical owner NT-04 |

## Method-selection map

| Similar surface | Route A | Route B | Discriminating question | First useful line |
|---|---|---|---|---|
| same remainder appears | gcd of differences | common-multiple reconstruction | Is the unknown the divisor, or the number being constructed? | `d | (a-b)` or `N-r` is a common multiple |
| several divisibility conditions | gcd | lcm | Do I need a common divisor or a common multiple? | write the target relation before factoring |
| large pair for gcd | prime-factor search | Euclidean reduction | Does division with remainder shrink faster? | `a=qb+r -> gcd(a,b)=gcd(b,r)` |
| one-number divisibility | divisibility test | structural divisibility | Is this just a yes/no digit-pattern check, or must I transform a relation involving variables/several expressions? | `b=ak` / take an integer linear combination |
| gcd and lcm both given | product invariant | full pair reconstruction | Is only `ab` required, or are `a,b` themselves required? | `gL=ab`, then if needed `a=gu,b=gv` |
| nested divisibility | independent checking | divisibility chain | Does one relation imply another by transitivity? | `a|b, b|c -> a|c` |

## Transfer map

- representation change (T2): equal-remainder words -> difference divisibility equation;
- representation change (T2): synchronization story -> common-multiple equation;
- context change (T3): alarms/reset cycles -> lcm;
- context change (T3): equally spaced marks / common step size -> gcd of differences;
- cross-domain bridge (T4): later congruence statements in NT-02 retrieve `d|(a-b)` without reteaching NT-01;
- cross-domain bridge (T4): later integer equations in NT-04 use gcd divisibility as a filter.

## Required contrast set

1. gcd target vs lcm target - divisor vs multiple.
2. same remainder with unknown divisor vs prescribed remainder with unknown number - differences vs reconstruction.
3. divisibility test vs structural divisibility reasoning - one-number pattern check vs relation transformation.
4. Euclid vs factor-everything - shrink by remainder vs decompose both numbers.
5. gcd of original numbers vs gcd of differences - common-divisor data vs equal-remainder data.
6. `gcd*lcm=product` vs pair reconstruction - one invariant vs coprime factor split.
7. independent divisibility conditions vs divisibility chain - separate checks vs transitivity.
8. lcm synchronization vs "largest step size" - least common multiple vs greatest common divisor.
9. NT-01 divisibility language vs NT-02 congruence notation - canonical teaching here vs downstream retrieval/application.

Each contrast changes the first move; none is merely a numerical variant.

## Stable downstream interface

The frozen prerequisite contract is exported at `Authoring/NT01_Prerequisite_Interface.md` for NT-02, NT-03, NT-04 and COMB-04. Downstream topics retrieve this interface; they do not rebuild canonical gcd/divisibility teaching.
