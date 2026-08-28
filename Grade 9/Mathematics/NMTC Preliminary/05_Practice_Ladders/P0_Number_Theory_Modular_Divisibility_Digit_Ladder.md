# P0 Number Theory — F0→F4→PYQ→XF Ladders

All non-PYQ prompts below are author-created.

## Family 1 — Modular power cycles
- F0: find `17 mod 5`.
- F1: list `2^n mod 5` for `n=1..6`.
- F2: find `2^100 mod 5`.
- F3: find the last digit of `7^173`.
- F4: combine two power cycles under one modulus.
- PYQ: `NMTC-BH-P-2018-Q29`; direct residue `2025-Q13`.
- XF: modulus/base changed so the cycle begins after reducing a negative residue.

## Family 2 — Same remainder -> LCM
- F0: find `lcm(6,8)`.
- F1: if `N` leaves remainder 2 on division by 6 and 8, show `N-2` is divisible by 24.
- F2: find the least such positive `N` above 2.
- F3: largest such `N` below a bound.
- F4: three divisors with non-coprime overlaps.
- PYQ: `NMTC-BH-P-2025-Q01`.
- XF: add a lower/upper interval constraint.

## Family 3 — Same remainder -> GCD differences
- F0: if 37 and 22 leave same remainder mod `d`, show `d|15`.
- F1: greatest divisor leaving equal remainders on 37,22.
- F2: three numbers; compute pairwise-difference GCD.
- F3: recover the common remainder after finding divisor.
- F4: combine with a maximum-divisor condition.
- PYQ: `NMTC-BH-P-2024-Q21`.
- XF: one number replaced by an algebraic expression.

## Family 4 — Simultaneous congruences
- F0: list numbers `≡2 mod5` below 30.
- F1: among them find one `≡1 mod3`.
- F2: solve two small congruences.
- F3: three congruences by progressive substitution.
- F4: reconstruct least residue modulo lcm/product where justified.
- PYQ: `NMTC-BH-P-2024-Q20`.
- XF: ask for a residue modulo a new composite modulus after reconstruction.

## Family 5 — Place value and digit equations
- F0: write a two-digit number as `10a+b`.
- F1: reversal difference simplifies to `9(b-a)`.
- F2: impose digit-sum and reversal conditions.
- F3: three-digit quotient/remainder relation.
- F4: repeated block factorization such as `ABCABC`.
- PYQ: 2018 Q28; 2019 Q01/Q16/Q17; 2025 Q14.
- XF: base-10 verbal problem with hidden place-value invariant.

## Family 6 — Divisibility tests from congruence
- F0: derive `10≡1 mod9`.
- F1: prove digit-sum rule mod9 for three digits.
- F2: derive `10≡-1 mod11`.
- F3: count digits satisfying a mod9 condition.
- F4: simultaneous digit and divisibility restrictions.
- PYQ: `NMTC-BH-P-2025-Q21`, plus 2019 Q01.
- XF: a digit may be 0 or 9 and shares residue 0; avoid undercounting.

## Family 7 — Integer-valued rational expressions
- F0: if `12/n` integer, list positive `n`.
- F1: rewrite `(n+5)/(n+1)=1+4/(n+1)`.
- F2: count positive `n` making expression integral.
- F3: substitution turns denominator into a divisor of a fixed constant.
- F4: parity/domain restrictions on the divisor variable.
- PYQ: `NMTC-BH-P-2025-Q26`; 2018 Q10/Q19.
- XF: denominator can be negative as well as positive; count all integer solutions if requested.

## Family 8 — Coprime/factor-pair structure
- F0: factor `k²-n²`.
- F1: impose same parity on `(k-n),(k+n)`.
- F2: enumerate factor pairs under positivity.
- F3: use `gcd(a,b)=1` and square product.
- F4: combine perfect-power/coprime condition with consecutive integers.
- PYQ: 2018 Q18; 2023 Q18; 2019 Q27.
- XF: cube/perfect-fourth-power analogue.

## Family 9 — Prefix residues ceiling bridge
- F0: write prefix sums of a short sequence.
- F1: show block sum `i+1..j` is `Sj-Si`.
- F2: translate divisibility by `m` to `Sj≡Si modm`.
- F3: count equal-residue prefix pairs.
- F4: avoid double-counting and include `S0`.
- PYQ ceiling: `NMTC-BH-P-2019-Q06`.
- XF: change modulus and sequence length.

## Family 10 — Multiplicative order ceiling bridge
- F0: cycle powers of 2 mod7.
- F1: identify smallest exponent giving 1.
- F2: infer order divides an exponent if a power is 1.
- F3: distinguish `a^8≡-1` from `a^8≡1`.
- F4: filter candidate prime divisors by order constraints.
- PYQ ceiling: `NMTC-BH-P-2019-Q26`.
- XF: new exponent with the same order logic.

## Adoption rule

A mechanism is adopted only when the student can:

1. state the first move before calculation;
2. explain why that move is valid;
3. solve at least one disguised F4/XF item;
4. reject the nearest wrong first move;
5. preserve digit/domain/parity restrictions.