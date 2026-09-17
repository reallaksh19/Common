# Modular, Divisibility & Digit Structures — Assimilation Book v2
## NMTC Bhaskara Preliminary / Grade IX–X competitive foundation

### Who this book is for

You probably already know how to divide with a remainder, calculate an HCF/LCM, use some divisibility rules, and find the last digit of a small power. The difficult part is usually **not the arithmetic**. It is deciding:

- what information the target can actually see;
- which smaller representation preserves exactly that information;
- which operations are legal in that representation;
- which near-looking problem actually needs a different method.

The central question of this book is therefore:

> **What information can the target see, and what smaller representation preserves exactly that information?**

Learning loop:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Performance loop:

`RECOGNIZE -> COMPRESS -> FIRST MOVE -> SOLVE -> CHECK -> TRANSFER`

---

# 0. RECONNECT — diagnostic before teaching

Do these without notes. Do not look for a chapter label. Write the first useful mathematical line even if you cannot finish.

1. What is the remainder when 47 is divided by 6?
2. Write three equivalent mathematical forms for: “`N` leaves remainder 4 when divided by 7.”
3. Is `35 ≡ 3 (mod 8)` true? Explain from divisibility of a difference.
4. Solve `2x ≡ 2 (mod 6)` as residue classes modulo 6.
5. Find the last digit of `7^20` without calculating the power.
6. A number leaves remainder 5 when divided by both 12 and 18. What quantity is divisible by both 12 and 18?
7. What first quantity would you calculate if one divisor leaves the same remainder on 84, 129 and 174?
8. Write a two-digit number with tens digit `a` and units digit `b` algebraically.
9. Why should digit sum have anything to do with divisibility by 9?
10. Rewrite `(n+8)/(n+2)` so that its integrality becomes a divisor condition.
11. Factor `k^2-n^2` in the form that is useful for integer factor pairs.
12. If `S_i` and `S_j` are prefix sums, what does `S_i ≡ S_j (mod m)` tell you about the block between them?

### How to interpret the diagnostic

- Miss 1–3: the remainder-to-congruence bridge is unstable.
- Miss 4: modular cancellation/division needs repair.
- Miss 5: cycle recognition or cycle indexing needs repair.
- Miss 6–7: the two “same remainder” grammars are being mixed.
- Miss 8–9: place-value representation is not yet automatic.
- Miss 10–11: finite divisor/factor-pair reduction is weak.
- Miss 12: state/prefix representation is unfamiliar.

This is not a score. It identifies the bridge to rebuild.

---

# 1. One idea first: keep only what the target can see

A question asking for a remainder does not care which exact integer you started with. It only cares which **remainder class** the integer belongs to.

A question asking whether a decimal number is divisible by 9 does not need the whole number once powers of 10 have been compressed modulo 9.

A question asking for a huge power modulo 10 does not need the huge power. It needs the repeating residue state.

A question asking whether a rational expression is an integer may not need a search through many integers. It may need only the divisors of one fixed constant.

That is the recurring number-theory move:

```text
VISIBLE FORM
    -> identify what information matters
    -> choose a smaller representation
    -> preserve legality / admissibility
    -> solve in the smaller representation
    -> check the original conditions
```

## CONTRAST 1 — exact value versus remainder value

- “Find `7^20`.” Exact integer information matters.
- “Find the last digit of `7^20`.” Only modulo 10 matters.

Same expression. Different target. Different representation.

## TRY — first move only

For each, write the smaller representation you would use before calculating.

1. Last digit of `3^2026`.
2. Greatest divisor leaving equal remainders on three given numbers.
3. A two-digit number and its reversal.
4. Positive integer `n` for which `(n+8)/(n+2)` is integral.
5. Number of consecutive blocks whose sums are divisible by 7.

---

# 2. Remainder language: division algorithm -> congruence -> divisibility

## RECONNECT

You already know that

`47 = 7·6 + 5`.

The remainder is 5.

## DISCOVER

The important part for remainder questions is not the quotient 6. It is the statement

`47 - 5` is divisible by 7.

So the following three forms carry the same information:

`47 = 7q + 5`

`47 ≡ 5 (mod 7)`

`7 | (47-5)`.

For a general integer `N`:

`N = mq+r`, with `0 <= r < m`

is equivalent to

`N ≡ r (mod m)`

and to

`m | (N-r)`.

## MAKE SENSE — congruence is not equality

`17 ≡ 2 (mod 5)` is true because `17-2=15` is divisible by 5.

But `17=2` is false.

Congruence says that two integers occupy the same **remainder state** modulo the chosen modulus.

## Why addition and multiplication work

Suppose

`a ≡ b (mod m)` and `c ≡ d (mod m)`.

Then `m|(a-b)` and `m|(c-d)`.

For addition,

`(a+c)-(b+d)=(a-b)+(c-d)`,

which is divisible by `m`.

For multiplication,

`ac-bd = a(c-d)+d(a-b)`,

and both terms are divisible by `m`.

So replacing numbers by simpler congruent representatives before adding or multiplying is legitimate.

## Worked compression

Find `47·58+19 (mod 9)`.

Instead of multiplying:

`47 ≡ 2`, `58 ≡ 4`, `19 ≡ 1 (mod 9)`.

Therefore

`47·58+19 ≡ 2·4+1 = 9 ≡ 0 (mod 9)`.

The arithmetic became smaller without changing the target information.

### Source mechanism grounding

`NMTC-BH-P-2025-Q13` is clean scored evidence for direct residue manipulation. The mechanism is used here without reproducing the historical question statement.

---

# 3. The operation that is not automatic: modular cancellation

A partly prepared learner often transfers ordinary algebra too aggressively into modular arithmetic.

## DISCOVER A FALSIFIER

Consider

`2x ≡ 2 (mod 6)`.

Ordinary-equation reflex says “divide by 2” and write

`x ≡ 1 (mod 6)`.

But test `x=4`:

`2x=8 ≡ 2 (mod 6)`.

So `x=4` satisfies the original congruence, yet `4` is not congruent to 1 modulo 6.

The cancellation lost valid solutions.

## MAKE SENSE FROM DIVISIBILITY

`2x ≡ 2 (mod 6)` means

`6 | 2(x-1)`.

Divide the divisibility statement by `gcd(2,6)=2`:

`3 | (x-1)`.

So the correct compressed statement is

`x ≡ 1 (mod 3)`,

which corresponds to two residue classes modulo 6: `1` and `4`.

## When cancellation is safe

If `ca ≡ cb (mod m)` and `gcd(c,m)=1`, then `c` has an inverse modulo `m`, so cancellation modulo the same modulus is valid.

Example:

`5x ≡ 10 (mod 12)`.

Since `gcd(5,12)=1`, cancellation/inversion is safe and gives a unique class modulo 12.

## CONTRAST 2 — reduction versus cancellation

- `14·19 ≡ 2·1 (mod 6)` is safe reduction of representatives.
- `2x ≡ 2 (mod 6) -> x ≡ 1 (mod 6)` is unsafe cancellation.

**Decision boundary:** replacing an integer by an equivalent residue is always legitimate; dividing a congruence requires an invertibility/GCD check.

## TRY — H0 attempt

1. Solve `4x ≡ 8 (mod 12)` as residue classes modulo 12.
2. Solve `7x ≡ 14 (mod 15)`.
3. A learner cancels 6 from `6x ≡ 9 (mod 15)`. Identify the first question that must be asked before accepting the step.

Do not look for hints yet. The Hint Bank is later.

---

# 4. Huge powers become finite-state problems

## RECONNECT

For last digits of powers of 7:

`7^1 -> 7`

`7^2 -> 9`

`7^3 -> 3`

`7^4 -> 1`

`7^5 -> 7` again.

The residue state repeats with period 4.

## REALIZE

The huge exponent is not the real difficulty. The finite residue cycle is the structure.

For `7^173`,

`173 ≡ 1 (mod 4)`,

so the residue is the first cycle entry.

## The zero-position trap

For `7^20`,

`20 ≡ 0 (mod 4)`.

Zero does **not** mean “use the first entry.” It means the exponent lands at the end of the four-position cycle:

`7, 9, 3, 1`.

So a multiple of the cycle length selects the fourth entry.

## CONTRAST 3 — modulus for the base versus modulus for the exponent

To find `7^173 mod 10`:

- reduce the **base** modulo 10;
- reduce the **exponent** modulo the proved cycle length 4.

Do not reduce the exponent modulo 10 merely because the final modulus is 10.

## A second residue cycle

Powers of 3 modulo 7 are

`3,2,6,4,5,1`,

with period 6.

So `3^100 mod 7` is controlled by `100 mod 6`, not by the size of `3^100`.

### Source mechanism grounding

- `NMTC-BH-P-2018-Q29` is a clean core power-cycle anchor.
- `NMTC-BH-P-2019-Q26` is clean high-ceiling evidence for multiplicative-order filtering; it belongs later, after ordinary cycles are secure.

## TRY — H0 attempt

1. Find the last digit of `7^222`.
2. Find `3^100 mod 7`.
3. Find `(2^50+3^50) mod 5`.
4. Explain the error in: “The cycle length is 4 and `20 mod4=0`, so use the first cycle entry.”

---

# 5. The flagship decision boundary: two different “same remainder” grammars

The words *same remainder* are dangerous because two structurally different problems can use them.

## Case A — one number, several divisors

Suppose `N` leaves remainder 3 when divided by 8 and 12.

Then

`N-3` is divisible by 8 and by 12.

Therefore `N-3` is a common multiple of 8 and 12:

`N = lcm(8,12)·k + 3 = 24k+3`.

This is an **LCM structure**.

## Case B — one divisor, several numbers

Suppose the same divisor `d` leaves the same remainder on 30, 53 and 99.

Then

`30 ≡ 53 ≡ 99 (mod d)`.

Therefore `d` divides the pairwise differences:

`53-30`, `99-53`, `99-30`.

The greatest possible such divisor is the GCD of those differences.

This is a **GCD-of-differences structure**.

## CONTRAST 4 — change one grammatical role, change the method

Ask before touching HCF/LCM:

> Is the **number fixed and divisors changing**, or is the **divisor fixed and numbers changing**?

| Visible grammar | First move | Structure |
|---|---|---|
| same `N`, many divisors, same remainder `r` | subtract `r` | LCM |
| same divisor on many numbers | subtract the numbers | GCD of differences |

### Clean paired source anchors

- `NMTC-BH-P-2025-Q01` grounds the first structure.
- `NMTC-BH-P-2024-Q21` grounds the second.

These are deliberately taught as a contrast pair.

## TRY — H0 attempt

1. Find the least positive integer greater than 100 that leaves remainder 5 on division by 12 and 18.
2. Find the greatest divisor that leaves the same remainder on 84, 129 and 174.
3. Find the largest integer below 5000 that leaves remainder 7 when divided by 12, 18 and 30.
4. A divisor `d` leaves remainder 8 on both 50 and 92. What extra condition must every candidate divisor satisfy besides dividing the difference?

---

# 6. Several congruences: intersect progressions, but check compatibility first

Generic simultaneous congruence reasoning is required for this unit even though the current qualified corpus does not provide a clean exact historical anchor for it.

## DISCOVER — each congruence is a progression

`N ≡ 2 (mod 5)` means

`N=2+5k`.

Now impose

`N ≡ 1 (mod 3)`.

Substitute:

`2+5k ≡ 1 (mod 3)`.

This turns the second condition into a smaller congruence in `k`.

The common solutions form the intersection of two arithmetic progressions.

## Compatible non-coprime moduli

Consider

`N ≡ 1 (mod 4)`

and

`N ≡ 3 (mod 6)`.

Because `gcd(4,6)=2`, the residues must agree modulo 2. They do: both are odd.

So a solution is possible.

## Incompatible system

Now compare

`N ≡ 1 (mod 4)`

and

`N ≡ 2 (mod 6)`.

Modulo `gcd(4,6)=2`, the first residue is odd and the second is even. No integer can satisfy both.

This is a recognition problem before it is a calculation problem.

## CONTRAST 5 — compatible versus impossible

The Chinese-Remainder-style first move is not “start listing numbers.” It is:

1. confirm all conditions apply to the same original unknown;
2. check shared-GCD compatibility when necessary;
3. parameterize one progression;
4. impose the next;
5. state the full repeating solution class if requested.

## CONTRAST 6 — simultaneous remainders versus successive quotient remainders

These are not the same representation:

- “`N` leaves specified remainders when directly divided by several moduli” -> simultaneous congruences;
- “divide `N`, then divide the quotient, then divide that quotient” -> nested division-algorithm reconstruction.

A remainder of a quotient must not be flattened into a congruence for the original number.

### Source-QC boundary: `NMTC-BH-P-2024-Q20`

An older repository summary classified this item as a clean simultaneous-congruence anchor. Wave-1 source review found that this classification is not defensible: the reproduced wording, keyed `43*`, and published solution do not support that clean interpretation without additional assumptions.

Current disposition:

`SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`.

The lesson is mathematical as well as editorial: **do not repair an ambiguous remainder chain into the problem you expected to see.**

## TRY — H0 attempt

1. Solve `N ≡ 2 (mod5)`, `N ≡ 1 (mod3)` and state the complete class.
2. Decide without search whether `N ≡ 1 (mod4)`, `N ≡ 2 (mod6)` is possible.
3. Solve `N ≡ 1 (mod4)`, `N ≡ 3 (mod6)`.
4. Solve `N ≡ 2 (mod3)`, `N ≡ 3 (mod5)`, `N ≡ 2 (mod7)`.

---

# 7. Digits are place-value algebra before they are counting

## RECONNECT

A two-digit number with tens digit `a` and units digit `b` is

`10a+b`.

Its reversal is

`10b+a`.

The difference is

`9(b-a)`.

So reversal problems naturally produce multiples of 9 because of place value, not because of a memorized trick.

## Three-digit and repeated-block structure

A three-digit number is

`100a+10b+c`.

If `ABC` denotes the three-digit integer with digits `A,B,C`, then

`ABCABC = 1000·ABC + ABC = 1001·ABC`.

Since

`1001=7·11·13`,

that repeated block carries built-in factors.

### Source mechanism grounding

Clean place-value evidence includes `NMTC-BH-P-2018-Q28`, `NMTC-BH-P-2019-Q01`, `NMTC-BH-P-2019-Q16`, `NMTC-BH-P-2019-Q17` and `NMTC-BH-P-2025-Q14`.

## Why divisibility by 9 uses digit sum

For

`N=100a+10b+c`,

we have `10 ≡ 1 (mod9)`, so `100 ≡ 1 (mod9)`.

Therefore

`N ≡ a+b+c (mod9)`.

The familiar digit-sum rule is a consequence of place value modulo 9.

## Why divisibility by 11 uses alternating sum

Modulo 11,

`10 ≡ -1`.

Therefore powers of 10 alternate:

`1,-1,1,-1,...`.

For a four-digit number `abcd`,

`1000a+100b+10c+d ≡ -a+b-c+d (mod11)`.

Again, the rule comes from place value.

## CONTRAST 7 — digit identity versus residue identity

Modulo 9, digits 0 and 9 have the same residue.

But they are not the same digit.

A counting problem may therefore have two different digit choices representing one residue state.

This is exactly the kind of partial-knowledge trap that a memorized “digit sum” rule does not expose.

## CONTRAST 8 — ordered versus unordered choices

Digits 2 and 5 can form `25` and `52`.

If the object is a numeral, position usually matters. Counting `{2,5}` as one unordered choice loses a number.

## CONTRAST 9 — legal digit versus legal leading digit

Units digit may be 0. A leading digit of a two- or three-digit number may not be 0.

This domain restriction belongs in the representation from the beginning.

### Clean counting anchor

`NMTC-BH-P-2025-Q21` is clean scored evidence for digit counting under a mod-9 condition, including the need to distinguish digit identity from residue identity.

## TRY — H0 attempt

1. A two-digit number has digit sum 11 and its reversal exceeds it by 27. Write the two first equations.
2. Explain why divisibility by 11 of `abcd` is controlled by `-a+b-c+d`.
3. How many two-digit positive integers have digit sum divisible by 9?
4. Digits are chosen from `{0,3,6,9}`, repetition allowed. What restrictions must be written before counting three-digit numbers divisible by 9?

---

# 8. Integer-valued expressions: make a denominator divide a constant

A problem may appear to ask you to test infinitely many integers. Often the right algebra converts it into a finite divisor list.

## DISCOVER

For integer `n` with `n≠-2`,

`(n+8)/(n+2) = 1 + 6/(n+2)`.

So integrality requires

`n+2 | 6`.

The infinite search over `n` has become a finite search over divisors of 6.

## Another algebraic division

`(n^2+3n+5)/(n+1)`

can be rewritten as

`n+2 + 3/(n+1)`.

Again, integrality is a divisor condition.

## MAKE SENSE

The denominator may divide a constant only after a useful division or substitution. The expert first move is therefore not “try values.” It is:

> Can I rewrite this as an integer expression plus `C / g(n)`?

### Clean mechanism grounding

- `NMTC-BH-P-2018-Q10` and `Q19` support divisor/integrality restrictions.
- `NMTC-BH-P-2025-Q26` is a clean transform-first anchor where a substitution converts the condition to divisibility by a fixed constant.

## Conditions survive the reduction

After obtaining a divisor condition, still check:

- denominator is nonzero;
- positive/natural/integer domain;
- negative divisors if all integers are allowed;
- bounds or parity inherited from a substitution.

## CONTRAST 10 — divisor reduction versus integer trial

- Trial method: test `n=1,2,3,...` until tired.
- Structural method: reduce to finitely many divisors, then filter admissibility.

The second is not merely faster. It proves completeness.

## TRY — H0 attempt

1. Find all positive integers `n` for which `(n+8)/(n+2)` is an integer.
2. Find all positive integers `n` for which `(n^2+3n+5)/(n+1)` is an integer.
3. Explain why a denominator-zero check must remain even after a divisor list has been formed.

---

# 9. Factor pairs are candidates, not answers

## Difference of squares

If

`k^2-n^2=96`,

then

`(k-n)(k+n)=96`.

Set

`u=k-n`, `v=k+n`.

Then

`k=(u+v)/2`, `n=(v-u)/2`.

For `k,n` to be integers, `u` and `v` must have the same parity.

So not every factor pair of 96 is admissible.

## CONTRAST 11 — factor pair versus admissible factor pair

A factor pair must still survive:

- parity;
- sign;
- order;
- positivity;
- stated bounds;
- coprimality or perfect-power conditions.

Factorization creates candidates. It does not finish the problem.

### Clean anchors

- `NMTC-BH-P-2018-Q18` is a clean same-parity difference-of-squares anchor.
- `NMTC-BH-P-2019-Q27` extends factorization with divisibility and bounds.

## Coprime product is a perfect power

Suppose positive integers `a,b` satisfy

`gcd(a,b)=1`

and `ab` is a perfect square.

Because `a` and `b` share no prime factor, prime exponents cannot be split between them. Since every exponent in `ab` is even, every exponent in `a` and in `b` must already be even.

Therefore each factor is itself a square.

## CONTRAST 12 — coprime product versus arbitrary product

`2·8=16` is a square, but neither 2 nor 8 is a square. The conclusion “each factor is square” fails because the factors are not coprime.

Coprimality is the structural condition that makes the prime-exponent argument work.

### Clean anchor

`NMTC-BH-P-2023-Q18` grounds the coprime-perfect-square mechanism.

## TRY — H0 attempt

1. How many positive integer pairs `k>n` satisfy `k^2-n^2=96`?
2. If positive coprime integers `a,b` satisfy `ab=144`, how many ordered pairs are possible?
3. Explain why the pair `(2,8)` is a falsifier for the statement “if `ab` is square, then `a` and `b` are square.”

---

# 10. Prefix residues: stop enumerating every consecutive block

Suppose a sequence is

`a1,a2,...,an`.

Define prefix sums

`S0=0`,

`S1=a1`,

`S2=a1+a2`, and so on.

Then the sum from `a_{i+1}` through `a_j` is

`S_j-S_i`.

Therefore that block sum is divisible by `m` exactly when

`S_j ≡ S_i (mod m)`.

This converts a problem about many blocks into a problem about repeated remainder states.

## Worked state table

For the sequence

`2,5,4,7`

modulo 3, the prefix sums are

`0,2,7,11,18`,

with residues

`0,2,1,2,0`.

Equal residue pairs correspond to divisible consecutive blocks.

The key object is not the block itself. It is the pair of equal prefix states.

## Why `S0` matters

If a divisible block begins with the first term, it is represented by

`S_j-S_0`.

Omitting `S0=0` loses every qualifying block that starts at the beginning.

## CONTRAST 13 — residue frequency versus block count

If one residue appears `f` times among the prefix states, it contributes

`C(f,2)`

pairs, not `f` blocks.

The states are vertices; the qualifying blocks are pairs of vertices.

### Clean ceiling anchor

`NMTC-BH-P-2019-Q06` is clean scored evidence for prefix-residue reasoning. It is a ceiling bridge, not the first lesson in modular arithmetic.

## Decimal state update

Prefix-state thinking also explains digit-by-digit remainder tracking.

If a decimal prefix has remainder `r` modulo `m` and the next digit is `d`, the new remainder is

`r' ≡ 10r+d (mod m)`.

So a long numeral can be processed as a sequence of small remainder states without reconstructing every large prefix.

## TRY — H0 attempt

1. For `2,5,4,7`, count consecutive blocks whose sums are divisible by 3.
2. Prefix residues modulo 5 are `0,2,0,3,2,0`. How many qualifying index pairs exist?
3. Explain why a sequence of 8 integers must contain a nonempty consecutive block whose sum is divisible by 8.
4. Track the remainder of the decimal number 31415 modulo 7 by the state update `r'≡10r+d`.

---

# 11. Ceiling tools come after core residue competence

This section is deliberately later. It should not be used to make ordinary remainder questions look more advanced than they are.

## 11.1 Multiplicative order as a refined cycle question

If `gcd(a,p)=1`, the multiplicative order of `a` modulo `p` is the least positive `r` such that

`a^r ≡ 1 (mod p)`.

Suppose an odd prime `p` divides `2^4+1`.

Then

`2^4 ≡ -1 (mod p)`,

so

`2^8 ≡ 1 (mod p)`,

but the order cannot divide 4.

That sharply restricts possible primes.

**Decision rule:** ordinary last-digit/remainder question -> build a cycle. Prime-divisor question with a strong `a^k≡±1` condition -> order may become useful after coprimality is checked.

### Clean ceiling anchor

`NMTC-BH-P-2019-Q26` supports this ceiling.

## 11.2 Attainability as a residue filter

When a total is built from allowed integer contributions, a congruence can sometimes rule out whole classes of totals before any enumeration.

`NMTC-BH-P-2019-Q14` is clean transfer evidence for this kind of attainability filtering.

## 11.3 Canonical representation as “choose representation before count”

`NMTC-BH-P-2019-Q28` supplies high-ceiling evidence that a difficult counting problem can become simple only after the correct number representation is chosen.

The pedagogical lesson is not “memorize balanced ternary.” It is:

> representation choice can convert a global counting problem into independent local state choices.

---

# 12. DIAGNOSE — error laboratory

For each proposed solution, identify the **first invalid or inferior move**, not merely the final wrong answer.

### Error 1 — congruence treated as equality

A learner writes `17≡2 (mod5)`, therefore `17=2`.

**Gap type:** meaning/representation.

### Error 2 — illegal cancellation

From `2x≡2 (mod6)`, a learner writes `x≡1 (mod6)`.

**Gap type:** legality/admissibility.

### Error 3 — exponent reduced modulo the wrong object

To compute `7^173 mod10`, a learner reduces 173 modulo 10.

**Gap type:** cycle representation.

### Error 4 — cycle remainder zero mapped to first entry

A learner says `7^20` uses the first entry because `20 mod4=0`.

**Gap type:** indexing.

### Error 5 — LCM reflex

“Same remainder” appears, so the learner takes an LCM before deciding what is fixed.

**Gap type:** decision boundary.

### Error 6 — GCD of original numbers

For an equal-remainder divisor problem, the learner takes `gcd(A,B,C)` instead of differences.

**Gap type:** invariant selection.

### Error 7 — incompatible congruences searched by brute force

The learner lists numbers for `x≡1 (mod4)`, `x≡2 (mod6)` forever.

**Gap type:** compatibility recognition.

### Error 8 — successive quotient data flattened into congruences

A remainder of a quotient is treated as though it were a remainder of the original number.

**Gap type:** representation/source reading.

### Error 9 — digit guessing before place value

The learner tests many two-digit numbers instead of writing `10a+b`.

**Gap type:** representation.

### Error 10 — unordered digit counting

The digits 2 and 5 are treated as producing only one two-digit number.

**Gap type:** object definition/order.

### Error 11 — leading zero accepted

`037` is counted as a three-digit number.

**Gap type:** domain/admissibility.

### Error 12 — residue identity confused with digit identity

Modulo 9, the learner replaces residue 0 by digit 0 only and forgets digit 9.

**Gap type:** residue-class interpretation.

### Error 13 — integer trial instead of divisor proof

A learner tests the first ten `n` values for an integrality problem and declares the list complete.

**Gap type:** completeness/representation.

### Error 14 — every factor pair accepted

After `(k-n)(k+n)=96`, every positive factor pair is counted.

**Gap type:** parity/admissibility.

### Error 15 — `S0` omitted

Prefix sums begin at `S1`, so blocks starting from the first term disappear.

**Gap type:** state representation.

### Error 16 — source conflict silently repaired

A damaged/ambiguous historical item is rewritten to match a published answer.

**Gap type:** source integrity.

---

# 13. FADE — four support ladders

**Rule:** attempt every item first at H0. Only then consult the Hint Bank in Section 16. Across each track, the maximum available help fades from H3 to H0.

## Track A — legal modular operations

- `A1 — H3 available after attempt:` solve `4x≡8 (mod12)` as classes modulo 12.
- `A2 — H2 maximum:` solve `6x≡9 (mod15)` as classes modulo 15.
- `A3 — H1 maximum:` solve `7x≡14 (mod15)`.
- `A4 — H0:` solve `8x≡12 (mod20)` completely.

## Track B — same-remainder method selection

- `B1 — H3 available:` least integer greater than 100 leaving remainder 5 modulo 12 and 18.
- `B2 — H2 maximum:` greatest divisor leaving the same remainder on 84,129,174.
- `B3 — H1 maximum:` largest integer below 3000 leaving remainder 3 when divided by 8,15,20.
- `B4 — H0:` greatest divisor leaving remainder 8 on 71,116,161.

## Track C — place-value/divisibility counting

- `C1 — H3 available:` reconstruct why digit sum controls divisibility by 9.
- `C2 — H2 maximum:` derive the divisibility-by-11 condition for `abcd`.
- `C3 — H1 maximum:` count two-digit positive integers whose digit sum is divisible by 9.
- `C4 — H0:` digits from `{0,3,6,9}`, repetition allowed: count three-digit numbers divisible by 9.

## Track D — cycles and state reasoning

- `D1 — H3 available:` last digit of `7^222`.
- `D2 — H2 maximum:` `3^100 mod7`.
- `D3 — H1 maximum:` for `2,5,4,7`, count consecutive blocks with sum divisible by 3.
- `D4 — H0:` process the digits of `31415` left-to-right and determine the final remainder modulo 7 using only remainder states.

A student who still needs H2/H3 on the fourth item has not yet reached ADOPT for that track.

---

# 14. ADOPT — mixed unlabelled first-move independence

No method labels are supplied. For each item, first write:

1. what structure you notice;
2. the first useful mathematical line;
3. then solve if needed.

1. Is `45≡3 (mod7)` true? Give the shortest justification.
2. Solve `6x≡9 (mod15)` as classes modulo 15.
3. Find the last digit of `3^2026`.
4. Find the least integer greater than 500 leaving remainder 7 on division by 12 and 18.
5. Find the greatest divisor leaving equal remainders on 100,136,172.
6. Solve `x≡2 (mod5)`, `x≡4 (mod6)`.
7. Decide whether `x≡2 (mod4)`, `x≡3 (mod6)` is possible.
8. A two-digit number is four times the sum of its digits. Find all possible numbers.
9. How many two-digit positive integers have digit sum divisible by 9?
10. Explain structurally why `527527` is divisible by 13.
11. Find all positive integers `n` for which `(n+8)/(n+2)` is an integer.
12. How many positive pairs `k>n` satisfy `k^2-n^2=96`?
13. Positive coprime integers `a,b` satisfy `ab=144`. How many ordered pairs are possible?
14. For the sequence `2,5,4,7`, count consecutive blocks whose sums are divisible by 3.
15. Find the least odd prime divisor of `2^4+1` using a cycle/order observation before direct testing.
16. A historical source paraphrase and its answer key cannot both be true under the same remainder interpretation. What is the mathematically responsible first action?

---

# 15. TRANSFER — same invariants, changed surfaces

These are not number swaps of the worked examples. The surface representation changes.

### T1 — circular machine state

A machine has 12 states numbered `0` to `11`. Each move advances 17 states cyclically. Starting at state 4, determine the state after 100 moves without simulating all moves.

### T2 — invertibility as information loss

A code stores only `4x mod12`. Can two different residue classes of `x mod12` produce the same stored code? Use this to explain why division by 4 is not reversible modulo 12.

### T3 — repeating light pattern

A light pattern has 4 phases corresponding to the successive last digits of powers of 3. Which phase is active at exponent 2026, and why is the exponent reduced modulo 4 rather than modulo 10?

### T4 — synchronized remainder condition

A ticket number leaves remainder 3 when divided by 8, 15 and 20. Find the largest such ticket number below 3000.

### T5 — unknown box capacity

Three piles contain 71,116 and 161 objects. The same box capacity leaves remainder 8 from each pile. Find the greatest possible box capacity.

### T6 — two repeating schedules

A marker occurs at positions congruent to 1 modulo 4 and 3 modulo 6. Describe all positions where both conditions occur. Then explain why changing the second residue from 3 to 2 destroys compatibility.

### T7 — reversal as place-value algebra

A two-digit number has digit sum 11. Its reversal is 27 greater than the original. Find the original number without guessing candidates.

### T8 — state-aware digit count

Digits are chosen from `{0,3,6,9}`, repetition allowed. Count the three-digit numbers divisible by 9, enforcing the leading-digit restriction.

### T9 — quotient becomes finite divisors

For positive integer `n`, determine when

`(n^2+3n+5)/(n+1)`

is an integer. Prove your list is complete.

### T10 — changed difference-of-squares load

How many positive integer pairs `k>n` satisfy

`k^2-n^2=180`?

Do not accept a factor pair before checking parity.

### T11 — existence without listing blocks

Prove that among any 8 integers there is a nonempty consecutive block whose sum is divisible by 8.

### T12 — process a long numeral as a state machine

Without long division, process the decimal digits of `314159` one at a time using

`r'≡10r+d (mod7)`

and determine the final remainder.

---

# 16. Hint Bank — use only after an attempt

This section contains **no final answers**. It supplies only the maximum hint allowed by the fading plan.

## Track A

**A1 — H3 execution:** Rewrite `4x≡8 (mod12)` as `12 | 4(x-2)`. Divide the divisibility relation by the GCD before describing classes modulo 12.

**A2 — H2 structure:** First compute `gcd(6,15)`. Check solvability, then reduce the coefficient/modulus relationship rather than cancelling 6 modulo 15.

**A3 — H1 recognition:** Is 7 invertible modulo 15?

**A4 — H0:** no hint.

## Track B

**B1 — H3 execution:** Write `N-5` as a multiple of `lcm(12,18)` before applying the lower bound.

**B2 — H2 structure:** Equal remainders under one fixed divisor imply divisibility of pairwise differences.

**B3 — H1 recognition:** Which object is fixed: the number or the divisor?

**B4 — H0:** no hint.

## Track C

**C1 — H3 execution:** Start with `N=a0+10a1+10^2a2+...` and replace each power of 10 by its residue modulo 9.

**C2 — H2 structure:** Powers of 10 alternate between `1` and `-1` modulo 11.

**C3 — H1 recognition:** For a two-digit positive integer, the tens digit is `1..9`, the units digit is `0..9`; possible digit sums divisible by 9 are limited.

**C4 — H0:** no hint.

## Track D

**D1 — H3 execution:** Write the mod-10 cycle of powers of 7 and reduce 222 modulo its length.

**D2 — H2 structure:** Build the residue cycle of 3 modulo 7; reduce the exponent by the cycle length, not by 7.

**D3 — H1 recognition:** Include `S0=0`; equal prefix residues correspond to divisible blocks.

**D4 — H0:** no hint.

---

# 17. ADOPT rules — what should become automatic

1. **Remainder language:** when I see a remainder, I can move among `N=mq+r`, congruence, and divisibility of a difference.
2. **Legality:** before dividing a congruence, I check whether the factor is invertible modulo the modulus.
3. **Huge powers:** I reduce the base, build the residue cycle, then reduce the exponent by the cycle length.
4. **Same remainder:** I first decide whether the number or the divisor is fixed.
5. **Several congruences:** I check compatibility, then intersect arithmetic progressions.
6. **Digits:** I encode place value before guessing or counting.
7. **Divisibility tests:** I can rebuild them from powers of 10.
8. **Integrality:** I try to make a denominator divide a fixed constant.
9. **Factor pairs:** I filter parity, sign, order, bounds and coprimality before accepting candidates.
10. **Consecutive blocks:** I compare prefix remainder states instead of enumerating blocks.
11. **Ceiling tools:** I use multiplicative order/canonical representation only when ordinary residue/state methods are not enough.
12. **Source integrity:** a plausible answer never authorizes silent repair of a damaged historical question.

---

# 18. Source custody — mechanism grounding, not copied question text

## Clean scored core mechanism IDs

- `NMTC-BH-P-2018-Q10`
- `NMTC-BH-P-2018-Q18`
- `NMTC-BH-P-2018-Q19`
- `NMTC-BH-P-2018-Q28`
- `NMTC-BH-P-2018-Q29`
- `NMTC-BH-P-2019-Q01`
- `NMTC-BH-P-2019-Q16`
- `NMTC-BH-P-2019-Q17`
- `NMTC-BH-P-2019-Q27`
- `NMTC-BH-P-2023-Q18`
- `NMTC-BH-P-2024-Q21`
- `NMTC-BH-P-2025-Q01`
- `NMTC-BH-P-2025-Q13`
- `NMTC-BH-P-2025-Q14`
- `NMTC-BH-P-2025-Q21`
- `NMTC-BH-P-2025-Q26`

## Clean scored ceiling / transfer bridges

- `NMTC-BH-P-2019-Q06` — prefix residues;
- `NMTC-BH-P-2019-Q14` — attainability/congruence transfer;
- `NMTC-BH-P-2019-Q26` — multiplicative-order ceiling;
- `NMTC-BH-P-2019-Q28` — canonical representation ceiling.

## Blocked evidence

- `NMTC-BH-P-2023-Q12` — source-sensitive, corrupted searchable statement; mechanism may inform research but exact anchor is blocked.
- `NMTC-BH-P-2024-Q20` — source-conflict/interpretation ambiguity; exact anchor blocked and not used as clean simultaneous-congruence evidence.

## Author-created teaching material

All diagnostics, contrast examples, fading items, ADOPT problems and transfer items in this book are author-created unless a stable source ID is explicitly named as mechanism grounding. They must not be assigned fake NMTC year/question labels.

---

# 19. Final self-test — six questions for every major idea

Before calling a mechanism learned, ask yourself:

1. **What did I notice?**
2. **Why does this representation preserve the information I need?**
3. **What clue would make me choose it?**
4. **What near-looking situation requires a different method?**
5. **Can I write the first two useful lines without help?**
6. **Can I solve a disguised version?**

If you can repeat a worked solution but cannot answer 3, 4 or 6, the method is not yet assimilated.

`END OF STUDENT ASSIMILATION BOOK v2`
