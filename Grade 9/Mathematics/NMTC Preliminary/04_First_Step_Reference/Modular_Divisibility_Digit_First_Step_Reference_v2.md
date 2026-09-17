# Modular, Divisibility & Digit Structures — First-Step Reference v2
## Use after the Assimilation Book

This is a **compression/revision layer**, not a substitute for the teaching book.

Core loop:

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

Central question:

> **What information can the target see, and what smaller representation preserves it?**

---

# 1. Ten-second decision tree

```text
REMAINDER / MODULO LANGUAGE?
    -> write division algorithm / congruence / divisibility-of-difference

DIVIDING OR CANCELLING A CONGRUENCE?
    -> check gcd(coefficient, modulus) before cancelling

HUGE POWER, SMALL REMAINDER / LAST DIGIT?
    -> reduce base -> build residue cycle -> reduce exponent by cycle length

“SAME REMAINDER”?
    -> fixed number, many divisors?  subtract r -> LCM
    -> fixed divisor, many numbers?  differences -> GCD

SEVERAL DIRECT REMAINDER CONDITIONS ON SAME NUMBER?
    -> check compatibility -> parameterize one progression -> impose next

DIGITS / REVERSAL / DIVISIBILITY RULE?
    -> write place value first

INTEGER-VALUED FRACTION?
    -> rewrite as integer part + C/divisor-expression

DIFFERENCE OF SQUARES / FACTOR PRODUCT?
    -> factor -> then filter parity/sign/order/bounds/coprimality

CONSECUTIVE BLOCK SUM / STREAM OF DIGITS?
    -> use prefix/residue states

PRIME DIVISOR OF a^k±1 / DAMAGED SOURCE?
    -> ceiling order test only after core; source-QC if evidence conflicts
```

---

# 2. Recognition atlas

| If you see... | Test this first |
|---|---|
| “remainder `r` on division by `m`” | `N=mq+r` / `N≡r (modm)` / `m|(N-r)` |
| common factor being cancelled in a congruence | `gcd(factor, modulus)` |
| huge exponent, last digit/remainder | residue cycle |
| same `N`, several divisors, same remainder | subtract remainder -> LCM |
| same divisor, several numbers, same remainder | pairwise differences -> GCD |
| several congruences on one unknown | compatibility + progression intersection |
| quotient is divided again | nested division algorithm, not CRT by reflex |
| digits / reversal / digit sum | place value |
| divisibility by 9 or 11 | derive from `10≡1 mod9`, `10≡-1 mod11` |
| rational expression must be integer | denominator divides a fixed constant after reduction |
| `u^2-v^2` with integer conditions | factor pairs + parity/admissibility |
| coprime product is a perfect power | prime-exponent separation |
| many consecutive block sums | prefix residues |
| digit-by-digit remainder processing | state update `r'≡10r+d` |
| prime divides `a^k±1` | multiplicative-order ceiling, after coprimality check |
| statement/key cannot both be right | source-integrity check; do not repair silently |

---

# 3. Phrase decoder

- “leaves remainder `r`” -> subtract `r` from the number before divisibility reasoning.
- “greatest divisor leaving the same remainder” -> subtract the **numbers**, then take a GCD.
- “least/largest number leaving the same remainder under several divisors” -> subtract the **remainder**, then use an LCM and the bound.
- “last digit” -> modulo 10.
- “last two digits” -> modulo 100.
- “reversal of a two-digit number” -> `10a+b` and `10b+a`.
- “digit sum divisible by 9” -> place value modulo 9; remember 0 and 9 are different digits with the same residue.
- “integer for all/which `n`” in a fraction -> look for `integer + C/g(n)`.
- “consecutive block divisible by `m`” -> equal prefix residues modulo `m`.
- “same number satisfies several congruences” -> intersection of arithmetic progressions.

---

# 4. First-Step Cards

## Card A — Remainder compression

**Clue:** remainder/modulo wording.

**Write:** one of

`N=mq+r`, `N≡r (modm)`, `m|(N-r)`.

**Check:** `0 <= r < m`.

---

## Card B — Cancellation legality

**Clue:** a coefficient/factor is being divided away in a congruence.

**Write:** `d=gcd(c,m)`.

**Choose:**

- `d=1` -> cancellation/inversion modulo `m` is safe;
- `d>1` -> return to divisibility / reduce modulus carefully.

**Do not:** cancel as though a congruence were an ordinary equation.

---

## Card C — Power cycle

**Clue:** huge exponent, small modulus, last digit.

**Write:** successive residues of the reduced base.

**Choose:** reduce exponent by the **cycle length**.

**Check:** exponent remainder zero means the final position in the displayed cycle.

---

## Card D — Same remainder: choose LCM or GCD

**Clue:** words “same remainder.”

**Ask:** what is fixed?

- same number, divisors change -> `N-r` common multiple -> LCM;
- same divisor, numbers change -> divisor divides differences -> GCD.

**Check:** if a remainder is prescribed, divisor must exceed it.

---

## Card E — Several congruences

**Clue:** one unknown has several direct remainder conditions.

**Write:** `N=a+mk` for one condition.

**Before solving:** if moduli share a GCD, check residue compatibility.

**Then:** impose the next condition on `k`.

**Check:** substitute final class into every original congruence.

---

## Card F — Place value / digit divisibility

**Clue:** digits, reversal, digit sum, repeated block.

**Write:** `10a+b`, `100a+10b+c`, or the appropriate powers-of-10 expression.

**Then:** ordinary algebra or justified modular reduction.

**Check:** leading digit nonzero; positions are ordered unless stated otherwise.

---

## Card G — Integer-valued fraction

**Clue:** expression must be integral for integer/natural `n`.

**Write:** algebraic division/substitution until

`integer expression + C/g(n)`.

**Choose:** require `g(n)|C`.

**Check:** denominator nonzero; sign/domain/bounds.

---

## Card H — Factor-pair admissibility

**Clue:** difference of squares / product of two integer expressions.

**Write:** factor first.

**Then filter:** parity, sign, order, positivity, bounds, coprimality.

**Remember:** factor pairs are candidates, not answers.

---

## Card I — Prefix/state reasoning

**Clue:** many consecutive blocks or a long digit stream.

**Write:** `S0=0,S1,...` or state update `r'≡10r+d`.

**Choose:** equal prefix residues for divisible blocks.

**Check:** count pairs `C(f,2)`, not merely residue frequencies.

---

## Card J — Ceiling / source boundary

**Clue A:** prime divides `a^k±1` and ordinary cycles are already secure.

**Write:** power congruence; consider multiplicative order only after checking the base is invertible.

**Clue B:** source wording/key/solution conflict.

**Write:** `SOURCE_CONFLICT` / `SOURCE_SENSITIVE`.

**Do not:** invent the missing condition or notation.

---

# 5. Critical contrast pairs

## Pair 1 — reduction vs cancellation

- replace `14` by `2 mod6` -> safe;
- cancel 2 from `2x≡2 mod6` -> not safe modulo6.

## Pair 2 — base modulus vs exponent cycle

- reduce base modulo the requested modulus;
- reduce exponent modulo the proved cycle length.

## Pair 3 — cycle zero position

For cycle `7,9,3,1`:

- exponent `21≡1 mod4` -> first entry;
- exponent `20≡0 mod4` -> fourth entry.

## Pair 4 — same remainder: LCM vs GCD

- same `N`, many divisors -> LCM;
- same divisor, many numbers -> GCD of differences.

## Pair 5 — compatible vs impossible congruences

- `x≡1 mod4`, `x≡3 mod6` -> compatible;
- `x≡1 mod4`, `x≡2 mod6` -> impossible.

## Pair 6 — simultaneous vs successive quotient remainders

- every condition applies directly to the same `N` -> simultaneous congruences;
- later conditions apply to quotients -> nested division algorithm.

## Pair 7 — digit identity vs residue identity

Modulo9, digits `0` and `9` share a residue but remain two distinct digit choices.

## Pair 8 — factor pair vs admissible factor pair

After `(k-n)(k+n)=C`, same parity is required before `k,n` can both be integers.

## Pair 9 — core cycle vs order ceiling

- routine remainder/last digit -> cycle;
- prime-divisor restriction from `a^k≡±1` -> order may help later.

---

# 6. Recognition laboratory — DO NOT SOLVE

Write only the **first move / representation**.

1. `N` leaves remainder 7 when divided by 12.
2. Solve `2x≡2 (mod6)`.
3. Find the last digit of `7^222`.
4. Find `3^100 mod7`.
5. A number leaves remainder 5 on division by 12,18 and 30.
6. Find the greatest divisor leaving equal remainders on 84,129,174.
7. Solve `x≡1 (mod4)`, `x≡3 (mod6)`.
8. Decide whether `x≡1 (mod4)`, `x≡2 (mod6)` is possible.
9. A number is divided by 5; then its quotient is divided by 6.
10. A two-digit number has digits `a,b`; its reversal is mentioned.
11. A four-digit number `abcd` is tested for divisibility by 11.
12. Count two-digit numbers whose digit sum is divisible by 9.
13. Find positive `n` making `(n+8)/(n+2)` integral.
14. Solve an integer condition containing `k^2-n^2=96`.
15. Positive coprime integers multiply to a perfect square.
16. Count consecutive blocks whose sum is divisible by 7.
17. Process a long decimal numeral modulo 13 digit by digit.
18. An odd prime `p` divides `2^8+1`.
19. A source key disagrees with the mathematics forced by the printed stem.
20. A huge integer is given, but the target asks only its remainder modulo 5.

---

# 7. Recognition key — check only after all 20

1. Division algorithm / congruence: `N=12q+7`, equivalently `N≡7 mod12`.
2. Check `gcd(2,6)`; return to divisibility before cancellation.
3. Build the last-digit cycle of powers of 7.
4. Build the residue cycle of 3 modulo7; reduce exponent by cycle length.
5. Subtract 5; use LCM of 12,18,30.
6. Take pairwise differences; use their GCD.
7. Check compatibility, then parameterize one progression.
8. Compare residues modulo `gcd(4,6)=2`; reject if incompatible.
9. Use nested division-algorithm equations for successive quotients; do not flatten to direct congruences.
10. Write `10a+b` and `10b+a`.
11. Use `10≡-1 mod11`; form alternating digit sum.
12. Use ordered digit domains and digit-sum residue; remember leading digit nonzero and 0/9 residue distinction.
13. Rewrite as `1+6/(n+2)`; require divisor condition.
14. Factor `(k-n)(k+n)`; filter same parity and other restrictions.
15. Separate prime-exponent blocks using coprimality.
16. Use prefix sums including `S0`; equal prefix residues.
17. Use state update `r'≡10r+d (mod13)`.
18. Convert to `2^8≡-1 modp`, hence a power returning to 1; consider multiplicative order after coprimality check.
19. Stop canonical use; preserve source conflict and independently verify the printed mathematics.
20. Reduce the integer modulo5 immediately; preserve only target-visible information.

`RECOGNITION_LAB: 20 ITEMS`

---

# 8. Thirty-second checks

Before committing to a method, ask:

1. What is actually fixed: the number, divisor, digits, factor product, or state?
2. What information does the target need: exact value or only a remainder/divisibility property?
3. Have I chosen the smallest representation that preserves that information?
4. Am I about to divide/cancel something that may not be invertible?
5. Is my remainder smaller than the divisor?
6. Did I preserve leading-zero, order, parity, sign, bounds and denominator restrictions?
7. If I used a cycle, did I handle exponent residue zero correctly?
8. If I used prefix residues, did I include `S0` and count pairs rather than frequencies?
9. Did I accidentally use a ceiling tool when a core method is shorter?
10. Does the final answer satisfy the original statement rather than only the transformed one?

---

# 9. Source-to-first-step map

| Source ID | Disposition | First-step mechanism |
|---|---|---|
| `NMTC-BH-P-2018-Q29` | clean scored | last-digit cycle |
| `NMTC-BH-P-2025-Q13` | clean scored | direct residue operation |
| `NMTC-BH-P-2025-Q01` | clean scored | same number / several divisors -> LCM |
| `NMTC-BH-P-2024-Q21` | clean scored | same divisor / several numbers -> GCD differences |
| `NMTC-BH-P-2018-Q28` | clean scored | place-value / reversal |
| `NMTC-BH-P-2019-Q01` | clean scored | repeated-block place-value factorization |
| `NMTC-BH-P-2025-Q21` | clean scored | digit residue/counting |
| `NMTC-BH-P-2025-Q26` | clean scored | integrality -> divisor condition |
| `NMTC-BH-P-2018-Q18` | clean scored | difference of squares + parity |
| `NMTC-BH-P-2023-Q18` | clean scored | coprime perfect-power structure |
| `NMTC-BH-P-2019-Q06` | clean ceiling bridge | prefix residues |
| `NMTC-BH-P-2019-Q26` | clean ceiling bridge | multiplicative order |
| `NMTC-BH-P-2023-Q12` | source-sensitive blocked | source-QC only |
| `NMTC-BH-P-2024-Q20` | source-conflict blocked | simultaneous-vs-successive/source-QC boundary only |

---

# 10. Can I start without help?

For an unfamiliar number-theory problem, can you answer all five before seeing a solution?

1. What visible clue matters?
2. What smaller representation preserves the target information?
3. What is my first useful line?
4. Which tempting near-method am I deliberately not using?
5. What admissibility/source condition must survive to the end?

If yes, the concept is becoming operational rather than memorized.
