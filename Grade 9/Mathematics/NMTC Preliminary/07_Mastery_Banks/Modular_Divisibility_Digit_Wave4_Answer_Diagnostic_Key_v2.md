# Issue #47 — Wave 4 Answer / Diagnostic Key

Authority for:

`Modular_Divisibility_Digit_Wave4_Mixed_Mastery_Student_v2.md`

This key is teacher/internal material. It must not be placed beside student attempt surfaces.

---

# A. Recognition-only key — 20/20

1. `N=12q+7`, equivalently `N≡7 (mod12)` or `12|(N-7)`.  
   Tag: `DIVISION_TO_CONGRUENCE`.
2. Check `gcd(2,6)` / return to `6|2(x-1)` before cancelling.  
   Tag: `ILLEGAL_MODULAR_CANCELLATION`.
3. Build the last-digit residue cycle of powers of 7.  
   Tag: `POWER_CYCLE_RECOGNITION`.
4. Exponent remainder zero selects the **last** position of the proved four-cycle.  
   Tag: `CYCLE_ZERO_INDEX`.
5. Write `N-5` as a common multiple; use LCM.  
   Tag: `SAME_NUMBER_LCM`.
6. Take pairwise differences; the divisor must divide their GCD.  
   Tag: `SAME_DIVISOR_GCD`.
7. Check shared-GCD compatibility, then intersect progressions / parameterize one congruence.  
   Tag: `CRT_CONSTRUCTIVE`.
8. Compare residues modulo `gcd(4,6)=2`; reject if incompatible.  
   Tag: `CRT_COMPATIBILITY`.
9. Use nested division-algorithm equations for successive quotients; do not flatten to direct congruences.  
   Tag: `SUCCESSIVE_QUOTIENT_REPRESENTATION`.
10. Write `10a+b` and `10b+a`.  
    Tag: `PLACE_VALUE_NOT_GUESSING`.
11. `ABCABC=1000·ABC+ABC=1001·ABC`.  
    Tag: `REPEATED_BLOCK_FACTORIZATION`.
12. Write ordered digit domains and reduce digit sum modulo 9; preserve leading-zero and `0`-versus-`9` identity.  
    Tag: `DIGIT_STATE_DOMAIN`.
13. Use `10≡-1 (mod11)` and alternating powers/signs.  
    Tag: `MOD11_PLACE_VALUE`.
14. Rewrite as `1+6/(n+2)`; require `n+2|6` subject to domain.  
    Tag: `INTEGRALITY_TO_DIVISOR`.
15. `(k-n)(k+n)=120`, then filter factor pairs by parity/sign/order.  
    Tag: `FACTOR_PAIR_ADMISSIBILITY`.
16. Use coprimality to separate prime-exponent blocks; a square product forces each coprime factor to be square.  
    Tag: `COPRIME_PERFECT_POWER`.
17. Introduce prefix sums including `S0`; equal prefix residues correspond to divisible blocks.  
    Tag: `PREFIX_STATE`.
18. Use digit-state update `r'≡10r+d (mod7)`.  
    Tag: `DECIMAL_STATE_UPDATE`.
19. From `3^4≡-1 (modp)`, infer `3^8≡1 (modp)`; after coprimality, order divides 8 and not 4.  
    Tag: `MULTIPLICATIVE_ORDER_CEILING`.
20. Freeze/flag source conflict; return to source authority before constructing a canonical exercise.  
    Tag: `SOURCE_CUSTODY`.

`RECOGNITION_AUDIT: 20/20 PASS`

---

# B. First useful line key — 12/12

1. `N=7q+4` (or `N≡4 (mod7)`).
2. `12 | 4(x-2)` before any cancellation.
3. Last-digit cycle of powers of 7: `7,9,3,1,...`.
4. `N-5` is a multiple of `lcm(12,18)=36`.
5. If the divisor is `d`, then `d|(129-84)=45` and `d|(174-129)=45`.
6. `gcd(4,6)=2` and residues 1,3 agree modulo 2; then e.g. `x=1+4k`.
7. `10b+a-(10a+b)=27`, so `9(b-a)=27`.
8. `ABCABC=1000·ABC+ABC=1001·ABC`.
9. `n^2+5n+10=(n+2)(n+3)+4`, hence quotient `=n+3+4/(n+2)`.
10. `(k-n)(k+n)=120`.
11. Define `S0=0`, `Sj=a1+...+aj`; block sum `=Sj-Si`.
12. Start `r0=0`; for each next digit `d`, use `r_next≡10r+d (mod7)`.

`FIRST_LINE_AUDIT: 12/12 PASS`

---

# C. Mixed solve / transfer key — 18/18

## C1
`9x≡12 (mod15)`. `gcd(9,15)=3`; reduce to `3x≡4 (mod5)`, so `x≡3 (mod5)`. As classes modulo 15:

`x≡3,8,13 (mod15)`.

Tag: `NONUNIT_COEFFICIENT`.

## C2
`5^2≡-1 (mod13)`, hence `5^4≡1`. Since `123≡3 (mod4)`,

`5^123≡5^3=125≡8 (mod13)`.

Tag: `POWER_CYCLE`.

## C3
`lcm(18,24,30)=360`. Thus `N=360k+7`; least `>1000` is

`1087`.

Tag: `SAME_NUMBER_LCM_BOUND`.

## C4
Differences are `72,72,144`; GCD is 72. Therefore greatest divisor is

`72`,

and common remainder is `178 mod72=34`.

Tag: `SAME_DIVISOR_GCD`.

## C5
`x=3+8k`. Require `3+8k≡7 (mod12)`, so `8k≡4 (mod12)` -> `2k≡1 (mod3)` -> `k≡2 (mod3)`.

`x≡19 (mod24)`.

Tag: `NONCOPRIME_COMPATIBLE_CRT`.

## C6
`gcd(6,9)=3`. Residues 2 and 3 are not congruent modulo 3 (`2` vs `0`).

**No solution.**

Tag: `CRT_INCOMPATIBLE`.

## C7
Let tens digit `a`, units digit `b`. Then

`a+b=13`, `b-a=3`.

Hence `a=5`, `b=8`; number

`58`.

Tag: `PLACE_VALUE_REVERSAL`.

## C8
Digits `{0,1,4,5}` without repetition; leading digit nonzero. Divisibility by 3 requires digit sum divisible by 3.

Valid numbers are:

`105,150,405,450,501,504,510,540`.

Count: **8**.

Tag: `ORDERED_DIGIT_DOMAIN`.

## C9

`(n^2+5n+10)/(n+2)=n+3+4/(n+2)`.

For positive `n`, `n+2≥3` and must divide 4. Only `n+2=4` works.

`n=2` only.

Tag: `INTEGRALITY_TO_DIVISOR`.

## C10
Set `u=k-n`, `v=k+n`; `uv=120`, `u<v`, same parity. Valid positive factor pairs are

`(2,60),(4,30),(6,20),(10,12)`.

They give `(k,n)=(31,29),(17,13),(13,7),(11,1)`.

Count: **4**.

Tag: `FACTOR_PAIR_PARITY`.

## C11
`900=2^2·3^2·5^2`. Coprimality forces each complete prime-square block wholly into `a` or `b`. Three independent assignments give

`2^3=8` ordered pairs.

Tag: `COPRIME_BLOCK_ALLOCATION`.

## C12
Prefix sums for `3,1,4,1,5` are

`0,3,4,8,9,14`,

residues modulo 4:

`0,3,0,0,1,2`.

Residue 0 occurs 3 times, contributing `C(3,2)=3`; all others occur once.

Answer: **3** blocks.

Tag: `PREFIX_PAIR_COUNT`.

## C13
Digit-state residues modulo 11 for `271828`:

`2 -> 5 -> 7 -> 1 -> 7 -> 7`.

Final remainder: **7**.

Tag: `DECIMAL_STATE_UPDATE`.

## C14
A total is `6a+10b`, `a,b≥0`. Divide by 2: `3a+5b=23`. One construction is `a=6,b=1`:

`6·6+10=46`.

Therefore **yes**.

Tag: `ATTAINABILITY_CONSTRUCTIVE`.

## C15
`3^4+1=82`. If odd prime `p` divides it, `3^4≡-1 (modp)`, so `3^8≡1` but the order does not divide 4. The odd prime divisor is

`41`.

Indeed `82=2·41`.

Tag: `ORDER_CEILING`.

## C16
Each move advances `17≡5 (mod12)`. After 100 moves:

`4+100·5=504≡0 (mod12)`.

Answer: state **0**.

Tag: `CYCLIC_STATE_TRANSFER`.

## C17

`ABCABC=1001·ABC` and `1001=7·11·13`.

Therefore **all three: 7, 11, and 13** divide every such repeated-block number.

Tag: `PLACE_VALUE_FACTOR_TRANSFER`.

## C18
Required action: **block canonical use; preserve the conflicting versions; return to the exact source/qualification authority; classify as source-sensitive/conflict until resolved.** Do not rewrite the stem to fit the key.

Tag: `SOURCE_CONFLICT_NOT_REPAIRED`.

`MIXED_SOLVE_TRANSFER_AUDIT: 18/18 PASS`

### Transfer classification

Do **not** count all 18 as non-identical transfer.

- routine/near mastery: C1–C7, C9–C11;
- bridge-transfer: C8, C12, C13, C15, C17;
- strongest disguised/context transfer: C14, C16, C18.

The bank therefore satisfies the Issue-47 **18 mixed solve/transfer** requirement without inflating an “18 transfer” claim.

---

# D. WHY-NOT key — 6/6

1. `gcd(6,15)=3`, so 6 is not invertible modulo 15. Correct reduction: `6x≡9 (mod15)` -> `2x≡3 (mod5)` -> `x≡4 (mod5)`; classes modulo 15 are 4,9,14.  
   Tag: `ILLEGAL_MODULAR_CANCELLATION`.
2. The exponent is governed by the proved residue cycle; for powers of 7 modulo 10 the cycle length is 4. Reducing exponent modulo 10 has no structural basis.  
   Tag: `EXPONENT_MOD_WRONG_OBJECT`.
3. “Same remainder” has two grammars. Fixed number + many divisors -> subtract remainder + LCM. Fixed divisor + many numbers -> pairwise differences + GCD.  
   Tag: `LCM_GCD_GRAMMAR`.
4. Congruence class is not object identity. Digits 0 and 9 are distinct choices even though both are residue 0 modulo 9.  
   Tag: `DIGIT_IDENTITY_VS_RESIDUE`.
5. From `u=k-n`, `v=k+n`, integer recovery requires `u,v` to have the same parity, plus sign/order conditions. Factorization creates candidates, not answers.  
   Tag: `FACTOR_PAIR_ADMISSIBILITY`.
6. Q20 is frozen as `SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`; ambiguous wording/key/solution cannot be silently normalized into a preferred CRT interpretation.  
   Tag: `SOURCE_CUSTODY`.

`WHY_NOT_AUDIT: 6/6 PASS`

---

# E. State / digit / high-ceiling key — 4/4

## E1
Digits `{0,3,6,9}`, repetition allowed, leading digit nonzero. Exhaustive residue-aware count gives **16** three-digit multiples of 9.

One explicit list:

`306,333,360,369,396,603,630,639,666,693,900,909,936,963,990,999`.

Tag: `DIGIT_STATE_COUNT`.

## E2
Frequencies in `0,1,3,1,0,3,1`:
- residue 0: 2 -> `C(2,2)=1`;
- residue 1: 3 -> `C(3,2)=3`;
- residue 3: 2 -> `C(2,2)=1`.

Total: **5** equal-residue index pairs.

Tag: `STATE_FREQUENCY_TO_PAIR_COUNT`.

## E3
Digit-state processing of `314159` modulo 7 gives final remainder **6**.

Tag: `DECIMAL_STATE_UPDATE`.

## E4
`3^4+1=82=2·41`; least odd prime divisor **41**. For an odd divisor `p`, `3^4≡-1`, hence `3^8≡1` while the order cannot divide 4. For `p=41`, the order is 8.

Tag: `ORDER_CEILING`.

`STATE_DIGIT_HIGH_CEILING_AUDIT: 4/4 PASS`

---

# F. Source custody

This Wave-4 assessment is author-created. It does not assign fake NMTC IDs to assessment items.

Current Issue-47 custody remains:

- clean scored core mechanism IDs: 16;
- clean scored ceiling/transfer bridge IDs: 4;
- total clean scored mechanism IDs: 20;
- `NMTC-BH-P-2023-Q12`: `SOURCE_SENSITIVE_EVIDENCE — BLOCKED_EXACT_ANCHOR`;
- `NMTC-BH-P-2024-Q20`: `SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`;
- topic-specific bonus evidence: 0.

`SOURCE_CUSTODY: PASS`

---

# G. Diagnostic tags

- `DIVISION_TO_CONGRUENCE`
- `CONGRUENCE_AS_EQUALITY`
- `ILLEGAL_MODULAR_CANCELLATION`
- `NONUNIT_COEFFICIENT`
- `POWER_CYCLE_RECOGNITION`
- `CYCLE_ZERO_INDEX`
- `EXPONENT_MOD_WRONG_OBJECT`
- `SAME_NUMBER_LCM`
- `SAME_DIVISOR_GCD`
- `LCM_GCD_GRAMMAR`
- `CRT_COMPATIBILITY`
- `CRT_INCOMPATIBLE`
- `SUCCESSIVE_QUOTIENT_REPRESENTATION`
- `PLACE_VALUE_NOT_GUESSING`
- `DIGIT_IDENTITY_VS_RESIDUE`
- `LEADING_ZERO_DOMAIN`
- `INTEGRALITY_TO_DIVISOR`
- `FACTOR_PAIR_ADMISSIBILITY`
- `COPRIME_PERFECT_POWER`
- `PREFIX_STATE`
- `STATE_FREQUENCY_TO_PAIR_COUNT`
- `DECIMAL_STATE_UPDATE`
- `ORDER_CEILING`
- `SOURCE_CUSTODY`

`WAVE4_KEY_MATH_REVIEW: PASS`
