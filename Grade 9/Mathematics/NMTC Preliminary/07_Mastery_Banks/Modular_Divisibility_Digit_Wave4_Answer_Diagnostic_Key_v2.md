# Issue #47 — Wave 4 Answer / Diagnostic Key

Authority for `Modular_Divisibility_Digit_Wave4_Mixed_Mastery_Student_v2.md`.

Teacher/internal material only. Do not place this beside student attempt surfaces.

---

# A. Recognition-only key — 20/20

1. `N=12q+7` / `N≡7 (mod12)` / `12|(N-7)` — `DIVISION_TO_CONGRUENCE`.
2. Check `gcd(2,6)` and return to `6|2(x-1)` before cancelling — `ILLEGAL_MODULAR_CANCELLATION`.
3. Build the last-digit cycle of powers of 7 — `POWER_CYCLE_RECOGNITION`.
4. Exponent remainder 0 selects the last position of the proved cycle — `CYCLE_ZERO_INDEX`.
5. `N-5` is a common multiple -> LCM — `SAME_NUMBER_LCM`.
6. Pairwise differences -> GCD — `SAME_DIVISOR_GCD`.
7. Shared-GCD compatibility, then intersect progressions — `CRT_CONSTRUCTIVE`.
8. Compare residues modulo `gcd(4,6)=2`; reject if incompatible — `CRT_COMPATIBILITY`.
9. Nested division-algorithm equations for successive quotients — `SUCCESSIVE_QUOTIENT_REPRESENTATION`.
10. `10a+b`, reversal `10b+a` — `PLACE_VALUE_NOT_GUESSING`.
11. `ABCABC=1001·ABC` — `REPEATED_BLOCK_FACTORIZATION`.
12. Ordered digit domains + digit sum modulo 9; preserve leading zero and `0` vs `9` — `DIGIT_STATE_DOMAIN`.
13. `10≡-1 (mod11)` -> alternating signs — `MOD11_PLACE_VALUE`.
14. `(n+8)/(n+2)=1+6/(n+2)` -> divisor condition — `INTEGRALITY_TO_DIVISOR`.
15. `(k-n)(k+n)=120`, then parity/sign/order filtering — `FACTOR_PAIR_ADMISSIBILITY`.
16. Coprimality separates prime-exponent blocks — `COPRIME_PERFECT_POWER`.
17. Prefix sums including `S0`; equal residues -> divisible blocks — `PREFIX_STATE`.
18. `r'≡10r+d (mod7)` — `DECIMAL_STATE_UPDATE`.
19. `3^4≡-1 (modp)` -> `3^8≡1`; after coprimality, order divides 8 but not 4 — `ORDER_CEILING`.
20. Freeze/flag source conflict; return to source authority before canonical use — `SOURCE_CUSTODY`.

`RECOGNITION_AUDIT: 20/20 PASS`

---

# B. First useful line key — 12/12

1. `N=7q+4`.
2. `12|4(x-2)`.
3. Last-digit cycle `7,9,3,1,...`.
4. `N-5` multiple of `lcm(12,18)=36`.
5. `d|(129-84)=45` and `d|(174-129)=45`.
6. `gcd(4,6)=2`; residues 1 and 3 agree modulo 2; e.g. start `x=1+4k`.
7. `10b+a-(10a+b)=27`, hence `9(b-a)=27`.
8. `ABCABC=1000·ABC+ABC=1001·ABC`.
9. `n^2+5n+10=(n+2)(n+3)+4`.
10. `(k-n)(k+n)=120`.
11. `S0=0`, `Sj=a1+...+aj`; block sum `Sj-Si`.
12. `r0=0`, then `r_next≡10r+d (mod7)` digit by digit.

`FIRST_LINE_AUDIT: 12/12 PASS`

---

# C. Mixed solve / transfer key — 18/18

| Item | Independently checked result | Diagnostic focus |
|---:|---|---|
| C1 | `x≡3 (mod5)` -> classes `3,8,13 (mod15)` | non-unit coefficient |
| C2 | `5^123≡8 (mod13)` because `5^2≡-1`, period 4 | cycle |
| C3 | `lcm(18,24,30)=360`; least `>1000` is `1087` | LCM + bound |
| C4 | greatest divisor `72`; common remainder `34` | GCD of differences |
| C5 | `x≡19 (mod24)` | compatible non-coprime system |
| C6 | no solution; residues disagree modulo `gcd(6,9)=3` | compatibility rejection |
| C7 | `58` | place value / reversal |
| C8 | `8` numbers: `105,150,405,450,501,504,510,540` | ordered digit domain |
| C9 | `n=2` only; quotient `=n+3+4/(n+2)` | divisor reduction |
| C10 | `4` pairs: `(31,29),(17,13),(13,7),(11,1)` | same-parity factor pairs |
| C11 | `8` ordered coprime pairs | prime-square block allocation |
| C12 | `3` divisible blocks; prefix residues `0,3,0,0,1,2` | prefix pair count |
| C13 | remainder `7`; state trace `2,5,7,1,1,7` | decimal state update |
| C14 | yes; e.g. `46=6·6+10·1` | attainability/construction |
| C15 | least odd prime divisor `41`; order divides 8, not 4 | order ceiling |
| C16 | state `0`; `4+100·(17 mod12)=504≡0` | cyclic-state transfer |
| C17 | all `7,11,13`; `ABCABC=1001·ABC` | repeated-block factorization |
| C18 | block canonical use; preserve conflict; return to exact source/qualification authority | source custody |

`MIXED_SOLVE_TRANSFER_AUDIT: 18/18 PASS`

### Transfer classification — deliberately conservative

Do **not** describe all 18 as non-identical transfer.

- routine/near mastery: C1–C7, C9–C11;
- bridge-transfer: C8, C12, C13, C15, C17;
- strongest disguised/context transfer: C14, C16, C18.

This satisfies the Issue-47 **18 mixed solve/transfer** count without inflating the transfer claim.

---

# D. WHY-NOT key — 6/6

1. `gcd(6,15)=3`; 6 is not invertible modulo 15. Correctly reduce to `2x≡3 (mod5)` -> `x≡4 (mod5)`; modulo-15 classes `4,9,14`.
2. The exponent is reduced by the proved power-cycle length (4 here), not automatically by target modulus 10.
3. “Same remainder” must be parsed: fixed number/many divisors -> LCM; fixed divisor/many numbers -> GCD of differences.
4. Residue equality is not digit identity: 0 and 9 are distinct digit choices.
5. `u=k-n`, `v=k+n` must have the same parity (plus sign/order conditions); factor pairs are candidates only.
6. `NMTC-BH-P-2024-Q20` remains `SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`; do not rewrite it into a preferred CRT problem.

`WHY_NOT_AUDIT: 6/6 PASS`

---

# E. State / digit / high-ceiling key — 4/4

1. **16** three-digit multiples of 9 from `{0,3,6,9}` with repetition and nonzero leading digit: `306,333,360,369,396,603,630,639,666,693,900,909,936,963,990,999`.
2. Frequencies `0:2, 1:3, 3:2` -> `C(2,2)+C(3,2)+C(2,2)=1+3+1=5` equal-residue pairs.
3. `314159 mod7=6`; state trace `3,3,6,5,6,6`.
4. `3^4+1=82=2·41`; least odd prime divisor `41`; `3^4≡-1 (mod41)`, so order is 8.

`STATE_DIGIT_HIGH_CEILING_AUDIT: 4/4 PASS`

---

# F. Source custody

Wave-4 assessment prompts are author-created and receive no fake NMTC IDs.

Current Issue-47 custody:

- clean scored core mechanism IDs: **16**;
- clean scored ceiling/transfer bridges: **4**;
- total clean scored mechanism IDs: **20**;
- `NMTC-BH-P-2023-Q12`: `SOURCE_SENSITIVE_EVIDENCE — BLOCKED_EXACT_ANCHOR`;
- `NMTC-BH-P-2024-Q20`: `SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`;
- topic-specific bonus evidence: **0**.

`SOURCE_CUSTODY: PASS`

---

# G. Principal diagnostic tags

`DIVISION_TO_CONGRUENCE` · `ILLEGAL_MODULAR_CANCELLATION` · `NONUNIT_COEFFICIENT` · `POWER_CYCLE_RECOGNITION` · `CYCLE_ZERO_INDEX` · `EXPONENT_MOD_WRONG_OBJECT` · `SAME_NUMBER_LCM` · `SAME_DIVISOR_GCD` · `CRT_COMPATIBILITY` · `CRT_INCOMPATIBLE` · `SUCCESSIVE_QUOTIENT_REPRESENTATION` · `PLACE_VALUE_NOT_GUESSING` · `DIGIT_IDENTITY_VS_RESIDUE` · `LEADING_ZERO_DOMAIN` · `INTEGRALITY_TO_DIVISOR` · `FACTOR_PAIR_ADMISSIBILITY` · `COPRIME_PERFECT_POWER` · `PREFIX_STATE` · `STATE_FREQUENCY_TO_PAIR_COUNT` · `DECIMAL_STATE_UPDATE` · `ORDER_CEILING` · `SOURCE_CUSTODY`

`WAVE4_KEY_MATH_REVIEW: PASS`
