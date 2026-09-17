# Issue #47 — Wave 2 Integrated Assimilation Book QA

`STATUS: WAVE2_INTEGRATED_ASSIMILATION_BOOK_PASS_INTERNAL`

Student source:

`03_Concept_Books/Number_Theory/Modular_Divisibility_Digit_Structure/Modular_Divisibility_Digit_Assimilation_Book_v2.md`

This is teacher/internal QA authority. It is deliberately separate from the student attempt surface.

---

# 1. Architecture audit

| Requirement | Result |
|---|---|
| one integrated book, not seven pasted interfaces | PASS |
| recurring compression question | PASS |
| reconnect diagnostic | 12 prompts — PASS |
| division algorithm before congruence abstraction | PASS |
| illegal modular cancellation falsifier | PASS |
| cycle-zero indexing diagnosis | PASS |
| flagship same-remainder LCM-vs-GCD contrast | PASS_STRONG |
| compatible + incompatible non-coprime congruences | PASS |
| simultaneous-vs-successive remainder boundary | PASS |
| place-value derivation of mod 9 / mod 11 | PASS |
| ordered/unordered digit boundary | PASS |
| leading-zero boundary | PASS |
| digit identity vs residue identity | PASS |
| integrality -> finite divisor reduction | PASS |
| factor-pair admissibility | PASS |
| prefix-state representation | PASS |
| ceiling material after core | PASS |
| source conflict not silently repaired | PASS |

Explicit close contrast mechanisms: **13**.

Issue #47 minimum: 7.

`CONTRAST_GATE: 13 >= 7 — PASS_STRONG`

Error laboratory: **16** diagnosis cases.

`DIAGNOSE_GATE: PASS_STRONG`

---

# 2. Attempt-before-hint / fading audit

Student diagnostic, TRY, FADE, ADOPT and TRANSFER prompts do not place final answers immediately below the attempt.

A separate Hint Bank appears later and contains no final answers.

Four genuine fading tracks:

1. legal modular operations;
2. same-remainder method selection;
3. place-value/divisibility counting;
4. cycles/state reasoning.

Each track uses:

`H3 available after attempt -> H2 maximum -> H1 maximum -> H0`

Total fading items: **16**.

`ATTEMPT_BEFORE_HINT: PASS`

`H3_TO_H0_FADING: 4 TRACKS / 16 ITEMS — PASS`

---

# 3. Independent mathematics audit

All conclusions were recomputed independently after authoring. Modular equations and finite digit/factor cases were also exhaustively enumerated where useful.

## 3.1 Reconnect — 12/12

1. `47 mod6 = 5`.
2. `N=7q+4`; `N≡4 (mod7)`; `7|(N-4)`.
3. true: `35-3=32` divisible by 8.
4. `2x≡2 (mod6)` -> `x≡1 (mod3)` -> classes `1,4 (mod6)`.
5. last digit `7^20 = 1`.
6. `N-5` divisible by both 12 and 18.
7. GCD of pairwise differences.
8. `10a+b`.
9. `10^k≡1 (mod9)`.
10. `(n+8)/(n+2)=1+6/(n+2)`.
11. `(k-n)(k+n)`.
12. `S_j-S_i` divisible by `m` -> intervening block sum divisible by `m`.

`RECONNECT_AUDIT: 12/12 PASS`

## 3.2 Congruence / cancellation

- `4x≡8 (mod12)` -> classes `2,5,8,11`.
- `7x≡14 (mod15)` -> `x≡2 (mod15)`.
- `6x≡9 (mod15)` -> `x≡4 (mod5)` -> classes `4,9,14`.
- `8x≡12 (mod20)` -> `x≡4 (mod5)` -> classes `4,9,14,19`.

`CANCELLATION_AUDIT: PASS`

## 3.3 Power cycles

- last digit `7^222` -> 9.
- `3^100 mod7` -> 4.
- `(2^50+3^50) mod5` -> 3.
- cycle-zero diagnosis is correct: exponent residue zero selects the last position of a 1-indexed displayed cycle.

`POWER_CYCLE_AUDIT: PASS`

## 3.4 Same remainder

- least `N>100`, remainder 5 modulo12,18 -> `113`.
- greatest equal-remainder divisor of 84,129,174 -> `45`.
- largest `N<5000`, remainder 7 modulo12,18,30 -> `4867`.
- if divisor `d` leaves remainder 8 on 50 and 92, then `d|42` and also `d>8`.

`SAME_REMAINDER_AUDIT: PASS`

## 3.5 Simultaneous congruences

- `N≡2 (mod5)`, `N≡1 (mod3)` -> `N≡7 (mod15)`.
- `N≡1 (mod4)`, `N≡2 (mod6)` -> incompatible.
- `N≡1 (mod4)`, `N≡3 (mod6)` -> `N≡9 (mod12)`.
- `N≡2 (mod3)`, `N≡3 (mod5)`, `N≡2 (mod7)` -> `N≡23 (mod105)`.

Historical 2024 Q20 is not used to generate these examples or answers.

`SIMULTANEOUS_CONGRUENCE_AUDIT: PASS`

## 3.6 Place value / digits

- digit sum 11 + reversal increase 27 -> `a+b=11`, `b-a=3`.
- four-digit mod11 reduction -> `-a+b-c+d`.
- two-digit positive integers with digit sum divisible by 9 -> **10**.
- digits `{0,3,6,9}`, repetition allowed, three-digit, divisible by 9 -> **16** after ordered/leading-zero filtering.

`PLACE_VALUE_AUDIT: PASS`

## 3.7 Integrality

`(n+8)/(n+2)=1+6/(n+2)`.

For positive `n`, `n+2` must be a positive divisor of 6 and at least 3 -> `n∈{1,4}`.

`(n^2+3n+5)/(n+1)=n+2+3/(n+1)`.

For positive `n`, `n+1` must be a positive divisor of 3 and at least 2 -> `n=2`.

`INTEGRALITY_AUDIT: PASS`

## 3.8 Factor pairs / coprime square product

`k^2-n^2=96` has four positive `k>n` pairs after same-parity filtering:

`(10,2),(11,5),(14,10),(25,23)`.

Positive coprime `ab=144=2^4·3^2` gives four ordered pairs:

`(1,144),(9,16),(16,9),(144,1)`.

`FACTOR_PAIR_AUDIT: PASS`

## 3.9 Prefix/state reasoning

For `2,5,4,7` modulo 3:

prefix residues `0,2,1,2,0` -> **2** equal-residue pairs.

For prefix residues `0,2,0,3,2,0`:

`C(3,2)+C(2,2)=3+1=4`.

For any 8 integers, 9 prefix sums occupy 8 residue classes modulo8 -> a repeated residue yields a nonempty divisible block.

Digit-state processing modulo7:

- `31415`: states `3,3,6,5,6` -> remainder **6**;
- `314159`: states `3,3,6,5,6,6` -> remainder **6**.

`PREFIX_STATE_AUDIT: PASS`

---

# 4. Fading-track audit — 16/16

| Item | Independent result |
|---|---|
| A1 | `2,5,8,11 (mod12)` |
| A2 | `4,9,14 (mod15)` |
| A3 | `2 (mod15)` |
| A4 | `4,9,14,19 (mod20)` |
| B1 | `113` |
| B2 | `45` |
| B3 | remainder **3** under 8,15,20 -> largest `<3000` is `2883` |
| B4 | greatest divisor leaving prescribed remainder 8 on 71,116,161 -> `gcd(63,108,153)=9` |
| C1 | digit-sum derivation from `10≡1 (mod9)` |
| C2 | alternating-sum derivation from `10≡-1 (mod11)` |
| C3 | `10` |
| C4 | `16` |
| D1 | `9` |
| D2 | `4` |
| D3 | `2` |
| D4 | `6` |

`FADING_MATH_AUDIT: 16/16 PASS`

---

# 5. ADOPT mixed unlabelled audit — 16/16

1. true; `42` divisible by 7.
2. classes `4,9,14 (mod15)`.
3. last digit `9`.
4. `511`.
5. `36`.
6. `x≡22 (mod30)`.
7. impossible by parity compatibility.
8. `12,24,36,48`.
9. `10`.
10. `527527=1001·527`, and `13|1001`.
11. `{1,4}`.
12. `4` positive pairs.
13. `4` ordered coprime pairs.
14. `2` divisible blocks.
15. `17`.
16. return to source custody; recheck exact statement/key/solution and block canonical use while unresolved.

`ADOPT_AUDIT: 16/16 PASS`

---

# 6. Transfer audit — 12/12

## T1 circular machine

`4+100·17 ≡ 0 (mod12)` -> state **0**.

## T2 invertibility as information loss

Yes. For example `x≡0` and `x≡3 (mod12)` both map to `4x≡0`. Multiplication by 4 is not injective modulo12 because `gcd(4,12)>1`.

## T3 repeating light

Power-of-3 last-digit cycle `3,9,7,1`; `2026≡2 (mod4)` -> phase 2 / last digit **9**.

## T4 synchronized remainder

Corrected prompt uses remainder **3**, admissible for all divisors 8,15,20.

`lcm=120`; largest `120k+3<3000` -> **2883**.

## T5 unknown box capacity

Prescribed remainder 8 means divide `63,108,153`; GCD -> **9**.

## T6 two schedules

`x≡1 (mod4), x≡3 (mod6)` -> `x≡9 (mod12)`.

Replacing 3 by 2 makes the system incompatible modulo2.

## T7 reversal

`a+b=11`, `b-a=3` -> `a=4,b=7` -> **47**.

## T8 state-aware digit count

Three-digit numbers from `{0,3,6,9}`, repetition allowed, leading digit nonzero, digit sum divisible by9 -> **16**.

## T9 finite divisors

`n+2+3/(n+1)` integral for positive `n` -> **n=2** only.

## T10 changed difference of squares

`k^2-n^2=180` -> same-parity positive factor pairs give:

`(14,4),(18,12),(46,44)`.

Count **3**.

## T11 existence via prefix residues

Nine prefix sums modulo8 occupy eight residue classes -> two coincide -> nonempty consecutive block sum divisible by8.

## T12 decimal state machine

`314159` modulo7 states:

`3,3,6,5,6,6` -> final remainder **6**.

`TRANSFER_AUDIT: 12/12 PASS`

---

# 7. Defect caught during independent audit

First authored Wave-2 draft contained:

- fading B3 with remainder `11` under divisors including 8;
- transfer T4 with the same invalid remainder condition.

This violates the division-algorithm condition `0 <= r < d`.

The prompts were corrected before Wave-2 promotion to use remainder **3**.

No downstream key promoted the invalid version.

`AUDIT_CAUGHT_DEFECT: CORRECTED_BEFORE_GATE`

---

# 8. Source custody audit

Current Issue-47 source custody remains:

- clean scored core mechanism IDs: **16**;
- clean scored ceiling/transfer bridges: **4**;
- total clean scored mechanism IDs: **20**;
- `NMTC-BH-P-2023-Q12`: source-sensitive / blocked exact anchor;
- `NMTC-BH-P-2024-Q20`: source-conflict / blocked exact anchor;
- topic-specific bonus evidence: **0**.

No blocked source is reproduced as a canonical historical exercise.

`SOURCE_CUSTODY: PASS`

---

# 9. Benchmark-parity gate

| Benchmark question | Wave-2 result |
|---|---|
| Can a partially prepared learner understand why the method works? | PASS |
| Are close decision boundaries explicit? | PASS_STRONG |
| Does the learner attempt before scaffolding? | PASS |
| Does support genuinely fade H3->H0? | PASS |
| Can the learner practice first-move selection unlabelled? | PASS |
| Is transfer structurally related but surface-changed? | PASS |
| Are source conflicts preserved? | PASS |
| Were answers independently recomputed? | PASS |
| PDF/render QA | NOT_RUN — Wave 5 |
| classroom timing/readability | NOT_RUN |

`WAVE2_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE3_FIRST_STEP_REFERENCE`
