# Modular Arithmetic, Divisibility & Digit Structure — Concept Book Spec

## Governing idea

Teach number theory as **compression of integer structure**:

`SEE INTEGER FORM -> REALIZE DIVISIBILITY/REMAINDER INVARIANT -> UNDERSTAND WHY THE COMPRESSION WORKS -> ADOPT THE FIRST MOVE IN DISGUISE`

## Chapter architecture

### 1. Division algorithm before congruence notation
Start with `N=dq+r`, `0<=r<d`. Make the student see that numbers with the same remainder differ by a multiple of `d`.

### 2. Congruence as compressed language
Derive `a≡b (mod m)` from `m | (a-b)`. Teach safe addition, subtraction and multiplication. Do not begin with symbolic rules without examples.

### 3. Residue cycles
Show last digits and powers first. Build cycle length experimentally, then explain why repeating residues permit exponent reduction.

### 4. Same-remainder contrast
Teach two non-equivalent triggers:
- one number leaves remainder `r` under several divisors -> `N-r` is a common multiple -> LCM;
- one divisor leaves the same remainder on several numbers -> divisor divides pairwise differences -> GCD.

### 5. Simultaneous congruences
Begin with systematic trial by one modulus, then introduce constructive CRT-style reconstruction. No theorem name is required before the student can build a solution.

### 6. Place-value algebra
Derive:
- two-digit number `10a+b`;
- reversed number `10b+a`;
- three-digit number `100a+10b+c`;
- repeated block `ABCABC=1001·ABC`.

### 7. Divisibility tests from place value
Derive mod-9 and mod-11 tests from powers of 10. Treat the familiar rules as consequences, not magic tricks.

### 8. Integer-valued rational expressions
Use algebraic division or substitution to write an expression as `integer part + constant/divisor`. Then integrality becomes a finite divisor problem.

### 9. Coprimality and factor pairs
Teach `gcd(a,b)=1` as structural information. If coprime positive integers multiply to a square, each is a square. For difference-of-squares, enforce same-parity factor pairs.

### 10. Prefix residues
For a sequence with partial sums `S0,S1,...`, a consecutive block sum is divisible by `m` exactly when two prefix sums have the same residue mod `m`. Use as a ceiling bridge.

### 11. Multiplicative order — ceiling bridge
Teach only after cycles are secure. If `a^k≡1 (mod p)`, the order divides `k`. Use to filter possible prime divisors. Do not make this a prerequisite for ordinary modular questions.

### 12. Canonical representations / balanced ternary — ceiling bridge
Use as an example of choosing the correct representation before counting. Keep separate from core syllabus entry-level work.

### 13. Source integrity
If a transcription damages exponent/parity notation, retain the mechanism as research evidence but block the item as an exact PYQ anchor.

## Mandatory contrast pairs

1. LCM same-remainder vs GCD same-remainder.
2. Reduce the base before the power vs attempt to compute the power.
3. Place-value encoding vs verbal digit guessing.
4. Divisibility test used with proof vs memorized rule used blindly.
5. Integer-valued expression reduced to divisors vs trial of many integers.
6. Cycle reasoning vs multiplicative-order ceiling reasoning.

## Required reconstruction tests

A learner must be able to reconstruct:

- why `a≡b (mod m)` means `m|(a-b)`;
- why congruences may be added/multiplied;
- why digit sum controls divisibility by 9;
- why alternating digit sum controls divisibility by 11;
- why equal remainders imply divisibility of differences;
- why prefix-residue equality corresponds to a divisible block sum.

## Preliminary performance contract

For each mechanism include:

- recognition trigger;
- first useful line;
- minimum expert path;
- wrong-method contrast;
- F0→F4 practice;
- clean PYQ anchor where available;
- non-identical transfer;
- timed recognition and first-line drill.

## Publication constraints

- no fake official questions;
- source-conflicted 2023 Q12 remains blocked;
- high-ceiling 2019 Q26/Q28 must be labelled as ceiling bridges, not basic expectations;
- 2022 remains absent from recurrence claims;
- student copy must not expose family labels during mixed mastery.