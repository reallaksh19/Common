# Modular Arithmetic, Divisibility & Digit Structure
## NMTC Bhaskara Preliminary — Student Concept Book Draft v0.1

> **Goal:** make large integer questions small by preserving only the information that matters.

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and during a Preliminary problem:

`RECOGNIZE -> COMPRESS -> FIRST MOVE -> RECONSTRUCT -> CHECK`.

---

# 0. Diagnostic

1. What is the remainder when 47 is divided by 6?
2. If two integers leave the same remainder on division by 7, what can you say about their difference?
3. Find the last digit of `3^4`.
4. Write the two-digit number with tens digit `a` and units digit `b`.
5. Why does divisibility by 9 depend on digit sum?
6. If `N` leaves remainder 4 when divided by 6 and 8, what is divisible by both 6 and 8?

Answers:
1. 5.
2. Their difference is divisible by 7.
3. 1.
4. `10a+b`.
5. Because `10≡1 (mod9)`.
6. `N-4`.

---

# 1. Remainder first, notation second

For any integer `N` divided by positive `d`:

`N=dq+r`, where `0<=r<d`.

Example:

`47=7·6+5`.

So 47 leaves remainder 5 modulo 7.

We compress this as:

`47≡5 (mod7)`.

## REALIZE

`a≡b (mod m)` means exactly:

`m | (a-b)`.

The notation does not create a new rule. It abbreviates divisibility of a difference.

---

# 2. Why congruences may be added and multiplied

If

`a≡b (mod m)`

and

`c≡d (mod m)`,

then `m|(a-b)` and `m|(c-d)`.

Adding:

`m | [(a+c)-(b+d)]`,

so:

`a+c≡b+d (mod m)`.

For multiplication:

`ac-bd=a(c-d)+d(a-b)`,

and both terms on the right are divisible by `m`.

Therefore:

`ac≡bd (mod m)`.

This is why we can reduce numbers before multiplying them.

---

# 3. Huge powers: never compute what you do not need

Find the last digit of `7^173`.

Last digit means modulo 10.

Powers of 7:

`7,9,3,1,7,...`

Cycle length 4.

`173≡1 (mod4)`.

So the last digit is the first cycle entry: 7.

## PYQ CONNECTION

- 2018 Q29 uses this power-cycle behavior.
- 2025 Q13 is even shorter: if `n≡4 (mod11)`, then `n²≡16≡5`.
- 2019 Q26 is a higher-ceiling extension where cycle/order restrictions filter prime divisors.

## ADOPT

Before calculating `a^N mod m`, ask:

1. Can I reduce `a` first?
2. What is the residue cycle?
3. Is there a special exponent-zero position in the cycle?

---

# 4. The most important “same remainder” contrast

## Case A — one number, several divisors

Suppose `N` leaves remainder 3 when divided by 8 and 12.

Then:

`N-3` is divisible by 8 and 12.

So:

`N-3` is a multiple of `lcm(8,12)=24`.

Thus:

`N=24k+3`.

This is an **LCM problem**.

### PYQ

2025 Q01 uses this exact structural first move.

## Case B — one divisor, several numbers

Suppose a divisor `d` leaves the same remainder when dividing 53 and 30.

Then:

`53≡30 (mod d)`.

Therefore:

`d | 23`.

If the question asks for the greatest such divisor across several numbers, take the GCD of pairwise differences.

### PYQ

2024 Q21 gives the clean model:

`gcd(53-30,99-53,99-30)=23`.

## CONTRAST

Do not see the words “same remainder” and automatically write LCM.

Ask:

- same **number** under several divisors? -> subtract remainder, LCM;
- same **divisor** on several numbers? -> subtract numbers, GCD.

---

# 5. Several congruences: reconstruct systematically

Suppose:

`N≡2 (mod5)`

and

`N≡1 (mod3)`.

Start with:

`N=2+5k`.

Now impose mod 3:

`2+5k≡1 (mod3)`.

Since `5≡2`:

`2+2k≡1`

`2k≡2`

`k≡1 (mod3)`.

So `k=1+3t` and:

`N=7+15t`.

The least positive solution is 7.

## PYQ CONNECTION

2024 Q20 combines three congruences and reconstructs the least suitable residue.

## CHECK

Always test the final answer against every original remainder condition.

---

# 6. Digits are algebra, not guesswork

A two-digit number with tens digit `a` and units digit `b` is:

`10a+b`.

Its reversal is:

`10b+a`.

Their difference:

`(10b+a)-(10a+b)=9(b-a)`.

So reversal questions naturally create multiples of 9.

A three-digit number is:

`100a+10b+c`.

## PYQ CONNECTION

- 2018 Q28 uses two-digit number and reversal structure.
- 2019 Q16/Q17 convert digit conditions into equations.
- 2025 Q14 uses direct place-value encoding.

---

# 7. Repeated digit blocks reveal factors

Let `ABC` denote the three-digit number `100A+10B+C`.

Then:

`ABCABC = 1000·ABC + ABC`

`=1001·ABC`

`=7·11·13·ABC`.

So divisibility by 7, 11 and 13 is automatically built into the repeated block.

## PYQ CONNECTION

2019 Q01 uses exactly this place-value factorization behavior.

The first move is not to test divisibility digit by digit. It is to factor the repeated block structurally.

---

# 8. Why the digit-sum test for 9 works

For a number:

`N=100a+10b+c`.

Modulo 9:

`10≡1`, so `100≡1`.

Therefore:

`N≡a+b+c (mod9)`.

That is the entire reason the digit-sum rule works.

## PYQ CONNECTION

2025 Q21 counts digit choices under a mod-9 condition and includes the subtle point that digit 0 and digit 9 have the same residue modulo 9.

## TRAP

Residues may be equal even when digits are different. Do not replace “residue 0” by “digit 0 only.”

---

# 9. Why alternating digit sum appears for 11

Modulo 11:

`10≡-1`.

Therefore:

`10^2≡1`, `10^3≡-1`, etc.

For a four-digit number `abcd`:

`1000a+100b+10c+d`

is congruent to:

`-a+b-c+d (mod11)`.

So divisibility by 11 is controlled by an alternating digit sum.

This rule should be reconstructed from powers of 10, not memorized without explanation.

---

# 10. Integer-valued rational expressions: make the denominator divide a constant

Suppose positive integer `n` must make:

`(n+5)/(n+1)`

an integer.

Rewrite:

`(n+5)/(n+1)=1+4/(n+1)`.

For the expression to be an integer:

`n+1 | 4`.

Now the infinite search over `n` becomes a finite divisor list.

## Higher-level substitution

Sometimes the right denominator is hidden. The 2025 Preliminary qualification contains an elegant example where `t=2n-1` transforms integrality into:

`t | 25`.

That is the desired move: turn integrality into finite divisor structure.

## CHECK

- denominator cannot be zero;
- if all integers are allowed, include negative divisors when appropriate;
- if natural numbers are required, filter afterward.

---

# 11. Factor pairs and parity matter

If:

`k²-n²=96`,

then:

`(k-n)(k+n)=96`.

But not every factor pair of 96 works.

`k-n` and `k+n` have the same parity.

So valid factor pairs must have matching parity before recovering `k,n`.

## PYQ CONNECTION

2018 Q18 uses this difference-of-squares factor-pair structure.

2019 Q27 combines factorization, divisibility and bounds at a higher ceiling.

---

# 12. Coprime products that are squares

Suppose positive integers `a,b` satisfy:

`gcd(a,b)=1`

and

`ab` is a perfect square.

Because `a,b` share no prime factor, every prime exponent belonging to `a` remains entirely inside `a`, and similarly for `b`.

Since all exponents in `ab` are even, all exponents in `a` and `b` are even.

Therefore both `a` and `b` are perfect squares.

## PYQ CONNECTION

2023 Q18 uses this with consecutive integers. Consecutive integers are coprime, and two positive consecutive perfect squares cannot occur.

---

# 13. Prefix residues — a powerful ceiling bridge

Let a sequence have prefix sums:

`S0=0`, `S1=a1`, `S2=a1+a2`, ...

The sum from term `i+1` to term `j` is:

`Sj-Si`.

This block sum is divisible by `m` exactly when:

`Sj≡Si (modm)`.

So counting divisible consecutive blocks becomes counting pairs of equal prefix residues.

## PYQ CONNECTION

2019 Q06 is a clean high-ceiling Preliminary example.

## TRAP

Do not forget `S0=0`; blocks beginning at the first term depend on it.

---

# 14. Multiplicative order — after cycles, not before

If `gcd(a,p)=1`, the multiplicative order of `a mod p` is the smallest positive `r` such that:

`a^r≡1 (modp)`.

If you know:

`a^16≡1 (modp)`

but

`a^8≡-1 (modp)`,

then the order divides 16 but does not divide 8. That strongly restricts the order, and therefore candidate primes.

## PYQ CONNECTION

2019 Q26 uses this kind of filtering.

This is a **ceiling bridge**, not the first lesson in modular arithmetic.

---

# 15. Source integrity is mathematical discipline

A reproduced 2023 item has damaged notation in its searchable statement. Its recovered solution indicates modulo-4 parity reasoning, but the exact mathematical question cannot be reconstructed safely from the damaged text alone.

Correct action:

`TRANSCRIPTION_SUSPECT -> retain mechanism evidence -> block exact PYQ anchor`.

Never invent missing exponents or symbols just because a likely solution is visible.

---

# 16. First-move lab — do not solve

Choose the first move only.

1. Largest `N<5000` leaving remainder 7 when divided by 12,18,30.
2. Greatest divisor leaving equal remainders on 84,129,174.
3. Last digit of `3^2026`.
4. Two-digit number plus reversal condition.
5. Three digits form a multiple of 9.
6. `(n+8)/(n+2)` must be integer.
7. `x²-y²` divisible by a large number.
8. Several remainder equations for one unknown.
9. Count consecutive blocks divisible by 7.
10. Prime divisor of `a^8+1`.

Expected first moves:

1. subtract 7, LCM;
2. pairwise differences, GCD;
3. residue cycle;
4. `10a+b`, `10b+a`;
5. digit sum mod9;
6. rewrite as integer plus constant/(n+2);
7. difference of squares;
8. progressive congruence reconstruction;
9. prefix residues;
10. order/cycle filter after checking the base is nonzero modulo the prime.

---

# 17. Adoption test

You have adopted the unit only if you can explain, without notes:

1. why congruence means divisibility of a difference;
2. why the two same-remainder problems use different operations;
3. why digit sum works modulo 9;
4. why alternating digit sum works modulo 11;
5. why a rational integrality problem can become a divisor problem;
6. why coprime factors of a square must each be squares;
7. why equal prefix residues create divisible block sums;
8. why multiplicative order is a ceiling tool rather than a memorized shortcut.

## Draft status

`STUDENT_DRAFT_v0.1`

All examples in this draft are author-created unless explicitly identified by stable PYQ ID. Full paper wording is not reproduced.