# W1-B — Power Cycles & Multiplicative Order Interface

`ISSUE_AUTHORITY: #47`

`WAVE: 1B`

`STATUS: INTERFACE_COMPLETE`

## 1. CONCEPTS

- reduce base before exponentiation;
- residue tables and eventual periodicity;
- cycle length and exponent-position mapping;
- zero-remainder cycle-index trap;
- last-digit / last-two-digit / general modulus variants;
- multiplicative order only after ordinary cycles are secure;
- prime-divisor filtering from `a^k ≡ ±1` conditions.

## 2. PREREQUISITES

- W1-A congruence meaning and safe operations;
- small powers;
- gcd/coprimality;
- factors/divisors of an exponent for ceiling work.

## 3. LIKELY_HALF_KNOWLEDGE

- can spot a last-digit pattern after several powers are listed but does not treat it as a finite-state cycle;
- reduces the exponent modulo the original modulus instead of the cycle length;
- maps exponent remainder 0 to the first cycle position;
- invokes Fermat/order language on routine questions before ordinary cycling is understood;
- forgets coprimality when using multiplicative order.

## 4. RECOGNITION_CUES

- huge exponent but tiny requested remainder;
- last digit / last two digits;
- repeated powers modulo a fixed integer;
- prime `p` divides `a^n±1`;
- statement such as `a^8≡-1 (modp)`.

## 5. FIRST_MOVES

1. Reduce the base modulo the target modulus.
2. List successive residues until a state repeats.
3. Record the cycle in order and its length.
4. Map the exponent to the correct cycle position; if exponent remainder is zero, use the final cycle position.
5. For prime-divisor ceiling questions, only then ask for the least positive exponent returning to 1.

## 6. INVARIANTS

- once the same residue state reappears under repeated multiplication by the same base, future residues repeat;
- when `gcd(a,m)=1`, powers lie among the units modulo `m` and a return to 1 exists;
- the multiplicative order divides any exponent `k` for which `a^k≡1`.

## 7. REPRESENTATION_SWITCHES

- `a^N mod m` -> short residue list/table;
- exponent `N` -> `N = qL+r` relative to cycle length `L`;
- `p | a^k-1` -> `a^k≡1 (modp)` -> order divides `k`;
- `p | a^k+1` -> `a^k≡-1`, hence `a^(2k)≡1` but `a^k≠1` for odd relevant `p`.

## 8. LEGALITY / ADMISSIBILITY CONDITIONS

- do not reduce an exponent modulo `m` merely because the modulus is `m`;
- order is defined only when the base is invertible modulo the modulus, e.g. `gcd(a,m)=1`;
- treat exceptional candidate primes dividing the base separately;
- cycle behavior can have a preperiod when the base is not coprime to the modulus; do not assume a pure cycle beginning at exponent 1 in every case.

## 9. DECISION_BOUNDARIES

**DB-B1 compute vs cycle**  
`7^173 mod10`: cycle is the intended representation; direct exponentiation is pointless.

**DB-B2 base modulus vs cycle modulus**  
Base is reduced modulo 10, exponent is reduced modulo the cycle length 4—not modulo 10.

**DB-B3 cycle remainder zero**  
For cycle `7,9,3,1`, exponent `20≡0 (mod4)` selects residue `1`, the fourth entry.

**DB-B4 ordinary cycle vs multiplicative order**  
Last digit of a power: ordinary cycle.  
Least prime divisor of `a^8+1`: order-style filtering may be efficient after base/nonzero checks.

## 10. MISCONCEPTION_TRAPS

- computing several huge powers before reducing;
- reducing exponent modulo the original modulus;
- mapping exponent remainder zero to the first cycle entry;
- assuming every sequence of powers starts with a pure cycle;
- invoking Fermat/order language without checking coprimality;
- using high-ceiling order arguments on a routine last-digit question.

## 11. CONTRAST_PAIRS

1. `7^173 mod10`: cycle length 4; `173 mod4`.  
   `7^173 mod4`: base is `3`; a different residue system/cycle applies.
2. `3^20 mod10`: exponent remainder zero means fourth cycle position.  
   `3^21 mod10`: first cycle position.
3. routine last digit vs prime divisor of `2019^8+1`: same finite-state idea, different ceiling.

## 12. TRANSFER_MECHANISMS

- last two digits where the learner must build a modulus-100 state table;
- a base whose powers enter zero/fixed-point behavior rather than a unit cycle;
- reverse question: infer possible exponent residues from a stated final residue;
- prime-divisor filtering where order must divide `2k` but not `k`.

## 13. SOURCE_IDS_AND_DISPOSITIONS

Clean scored anchors:
- `NMTC-BH-P-2018-Q29` — last-digit cycle;
- `NMTC-BH-P-2025-Q13` — direct residue squaring;
- `NMTC-BH-P-2019-Q26` — high-ceiling multiplicative-order filtering.

Classification:
- 2018 Q29 / 2025 Q13 = core;
- 2019 Q26 = `CLEAN_SCORED_CEILING_BRIDGE`, not entry prerequisite.

## 14. CANDIDATE_MASTERY_ITEMS

`B-M1` Find the last digit of `7^222`.

`B-M2` Find `3^100 mod7` by a residue cycle.

`B-M3` Find `(2^50+3^50) mod5`.

`B-M4` A learner says `7^20` has the first entry of the mod-10 cycle because `20 mod4=0`. Diagnose and correct.

`B-M5` If odd prime `p` divides `2^4+1`, explain what the order of 2 modulo `p` must divide and what it cannot divide before testing candidates.

Independent check:
- B-M1: cycle `7,9,3,1`; `222 mod4=2` -> 9;
- B-M2: powers mod7 cycle length 6; `100 mod6=4`; `3^4=81≡4`;
- B-M3: `2^50 mod5=4`, `3^50 mod5=4`, total `3 mod5`;
- B-M4: zero maps to final cycle entry, answer last digit 1;
- B-M5: `2^4≡-1`, so order divides 8 and does not divide 4.

## 15. DIAGNOSTIC_TAGS

- `BRUTE_FORCE_POWER`
- `EXPONENT_MOD_WRONG_OBJECT`
- `CYCLE_ZERO_INDEX_ERROR`
- `PREPERIOD_UNSEEN`
- `ORDER_TOO_EARLY`
- `ORDER_COPRIMALITY_MISSING`

## 16. H3_TO_H0_FADE_PLAN

- `B-F1 H3`: provide the first four residues and ask for cycle/index mapping.
- `B-F2 H2`: say only “build a residue cycle; do not expand.”
- `B-F3 H1`: highlight that only a remainder/last digit is requested.
- `B-F4 H0`: disguised power or prime-divisor item requiring independent choice between direct reduction, cycle, or order.

`W1-B_GATE: PASS`