# P0 Number Theory — First-Step Cards

Use: `SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`.

## Card 1 — Huge power, small modulus
**See:** `a^N mod m`, last digit, remainder of a huge power.
**Write:** reduce `a mod m`; list residues until they repeat.
**Choose:** reduce the exponent by the cycle length.
**Check:** exponent-zero position and sign.
**PYQ:** 2018 Q29; 2025 Q13; ceiling: 2019 Q26.

## Card 2 — One number, same remainder under several divisors
**See:** `N leaves remainder r when divided by d1,d2,...`.
**Write:** `N-r` is divisible by every divisor.
**Choose:** LCM.
**Check:** final number reproduces remainder `r`.
**PYQ:** 2025 Q01.

## Card 3 — One divisor, same remainder on several numbers
**See:** greatest divisor leaving the same remainder on `A,B,C`.
**Write:** divisor divides `A-B`, `B-C`, `A-C`.
**Choose:** GCD of differences.
**Check:** remainders are equal.
**PYQ:** 2024 Q21.

## Card 4 — Several remainder conditions
**See:** `N≡a (mod m)`, `N≡b (mod n)`, ...
**Write:** start from the simplest progression, e.g. `N=a+mk`.
**Choose:** impose the next congruence on `k`.
**Check:** substitute into all original congruences.
**PYQ:** 2024 Q20.

## Card 5 — Digits mentioned
**See:** tens/units/reversal/digit sum.
**Write:** `10a+b`, `10b+a`, or `100a+10b+c`.
**Choose:** solve algebraically before enumerating.
**Check:** each symbol remains a legal digit.
**PYQ:** 2018 Q28; 2019 Q16/Q17; 2025 Q14.

## Card 6 — Divisibility by 9
**See:** digit sum and multiple of 9.
**Write:** `10≡1 (mod9)`.
**Choose:** replace number by digit sum modulo 9.
**Check:** leading-digit and zero restrictions.
**PYQ:** 2025 Q21.

## Card 7 — Divisibility by 11 / repeating block
**See:** alternating digit structure or repeated block.
**Write:** `10≡-1 (mod11)` or factor the block by place value.
**Choose:** alternating sum / algebraic factorization.
**Check:** do not use a digit rule without verifying position signs.
**PYQ:** 2019 Q01; prefix-residue bridge Q06.

## Card 8 — Integer-valued rational expression
**See:** expression in integer `n` must be an integer.
**Write:** transform to `integer expression + C/g(n)`.
**Choose:** require `g(n)|C`.
**Check:** denominator nonzero and domain restrictions.
**PYQ:** 2025 Q26; 2018 Q10/Q19.

## Card 9 — Difference of squares
**See:** `a²-b²` plus divisibility/bounds.
**Write:** `(a-b)(a+b)`.
**Choose:** factor-pair restrictions.
**Check:** factors have same parity; positivity/order/bounds.
**PYQ:** 2018 Q18; 2019 Q27.

## Card 10 — Coprime product is a perfect square/power
**See:** `gcd(a,b)=1` and `ab` square.
**Write:** prime factors of `a` and `b` do not overlap.
**Choose:** each factor must itself carry even exponents.
**Check:** positivity and exceptional zero cases.
**PYQ:** 2023 Q18.

## Card 11 — Consecutive block sum divisible by m
**See:** many consecutive subsequences or block sums.
**Write:** prefix sums `S0=0,S1,...` modulo `m`.
**Choose:** equal prefix residues.
**Check:** count distinct index pairs, not just residue classes.
**PYQ ceiling bridge:** 2019 Q06.

## Card 12 — Prime divides `a^k±1`
**See:** least prime divisor / strong power congruence.
**Write:** infer a power congruent to 1.
**Choose:** multiplicative-order restriction only after ordinary cycles are understood.
**Check:** base not divisible by candidate prime; special prime 2 separately.
**PYQ ceiling bridge:** 2019 Q26.

## Card 13 — Attainable score / integer combination
**See:** can a total be formed from allowed scoring values?
**Write:** linear integer combination; reduce modulo a useful gcd/modulus.
**Choose:** eliminate impossible residue classes before enumeration.
**Check:** non-negative count restrictions.
**PYQ:** 2019 Q14.

## Card 14 — Source notation damaged
**See:** exponent/parity symbol is corrupted or key cannot be reconciled.
**Write:** `SOURCE_CONFLICT` / `TRANSCRIPTION_SUSPECT`.
**Choose:** preserve mechanism as research evidence only.
**Check:** never invent the missing notation.
**PYQ contrast:** 2023 Q12.