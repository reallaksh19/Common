# Divisibility, GCD and LCM — Assimilation Book

For a Grade-9 learner who can calculate HCF/LCM but does not yet reliably know **when** those ideas are the shortest route.

## 1. RECONNECT — what you probably already know

You may already be able to answer:
- `12` divides `60`;
- `gcd(84,126)=42`;
- `lcm(12,18)=36`.

The IOQM difficulty is usually not the calculation. It is recognizing the hidden structure.

### Diagnostic

Without solving fully, decide the first useful idea:

1. Find the greatest integer that divides 173 and 239 leaving the same remainder.
2. Find the least positive integer divisible by 12, 15 and 18.
3. Simplify the task of finding `gcd(987,610)`.
4. If `gcd(a,b)=6` and `lcm(a,b)=180`, what relation must `ab` satisfy?

Expected recognition: **difference, lcm, Euclidean algorithm, gcd*lcm product**.

---

## 2. DISCOVER — why subtraction is so powerful

Suppose a positive integer `d` divides both `a` and `b`.

Then

`a = dm`, `b = dn`

for integers `m,n`. Therefore

`a-b = d(m-n)`.

So every common divisor of `a` and `b` also divides `a-b`.

The reverse direction is just as useful: if `d|b` and `d|(a-b)`, then `d|a`.

Hence

`gcd(a,b) = gcd(b,a-b)`.

More generally,

`gcd(a,b) = gcd(b,a-qb)`

for any integer `q`.

This is the engine of the Euclidean algorithm.

### Why this matters

The pair `(987,610)` looks large. But

`987-610=377`,
`610-377=233`,
`377-233=144`, ...

The numbers shrink while the gcd stays unchanged.

> **Adopt:** when the same divisor is hidden in several numbers, subtraction can reveal it without changing the common-divisor structure.

---

## 3. MAKE SENSE — same remainder means difference

If `a` and `b` leave the same remainder `r` when divided by `d`, then

`a = dq+r`, `b = dp+r`.

Subtract:

`a-b = d(q-p)`.

Therefore

`d | (a-b)`.

### Example

What is the greatest integer that divides 173 and 239 leaving the same remainder?

Do not search remainders.

The divisor must divide

`239-173 = 66`.

The greatest possible such divisor is therefore `66`.

Check: `173 mod 66 = 41`, `239 mod 66 = 41`.

### Contrast

- **same remainder, greatest divisor** -> subtract, then gcd;
- **least number divisible by several integers** -> lcm.

These are opposite directions: divisor structure vs multiple structure.

---

## 4. DISCOVER — what LCM is really doing

A common multiple of `a` and `b` is a number that both divide.

The lcm is the **smallest positive synchronization point**.

Example: a light flashes every 12 seconds and another every 18 seconds. Starting together, when do they next flash together?

The answer is `lcm(12,18)=36` seconds.

This same structure appears even when there are no lights in the problem.

### Recognition cue

Phrases like:
- “least positive integer divisible by...”
- “first time together...”
- “smallest number satisfying all divisibility conditions...”

suggest **LCM construction**.

---

## 5. MAKE SENSE — linking gcd and lcm

For positive integers `a,b`,

`gcd(a,b) * lcm(a,b) = ab`.

A useful normalization is

`a = gu`, `b = gv`, where `g=gcd(a,b)` and `gcd(u,v)=1`.

Then

`lcm(a,b)=guv`,

so

`g * guv = g^2uv = ab`.

### Example

If `gcd(a,b)=6` and `lcm(a,b)=180`, then

`ab = 6*180 = 1080`.

This does not identify `a,b` uniquely, but it gives a strong invariant before casework.

---

## 6. TRY — attempt before hints

### Problem A

Find the greatest integer that divides 221, 323 and 425 leaving the same remainder.

Try first.

**H1 — recognition:** equal remainder means what happens after subtraction?

**H2 — structure:** the divisor divides `323-221` and `425-323`.

**H3 — execution:** compute `gcd(102,102)`.

Answer: `102`.

### Problem B

Find the least positive integer divisible by 18, 24 and 30.

Try first.

**H1:** are you seeking a divisor or a common multiple?

**H2:** build the least common multiple.

**H3:** `lcm(18,24)=72`, then `lcm(72,30)=360`.

Answer: `360`.

---

## 7. DIAGNOSE — common wrong starts

### Wrong start 1: factor everything immediately

Factoring is sometimes fine, but if the numbers are large and subtraction rapidly reduces them, Euclid is cheaper.

### Wrong start 2: use lcm for a same-remainder divisor problem

Equal remainders create **differences**, and the unknown is a divisor of those differences.

### Wrong start 3: divide by a gcd without normalizing

When setting `a=gu, b=gv`, explicitly state `gcd(u,v)=1`. That coprimality is often the whole point.

### Wrong start 4: use decimal intuition

Divisibility is exact integer structure. Keep the work integral.

---

## 8. FADE — H3 -> H0

### Faded set 1

Find `gcd(2026,748)`.

- H3: repeatedly replace the larger number by the remainder after division.
- H2: use `gcd(a,b)=gcd(b,a mod b)`.
- H1: preserve gcd while shrinking the pair.
- H0: solve independently.

### Faded set 2

A number leaves remainder 7 when divided by each of 12, 18 and 30 after subtracting 7 from it. Find the least such number greater than 7.

- H3: solve `N-7 = lcm(12,18,30)`.
- H2: translate same prescribed remainder into a common-multiple condition.
- H1: remove the remainder first.
- H0: solve independently.

---

## 9. ADOPT — five mental rules

1. `a|b` means `b=ak` for some integer `k`.
2. Common divisors survive subtraction of integer multiples.
3. Same remainder -> subtract -> gcd of differences.
4. Least simultaneous divisibility -> lcm.
5. Given gcd and lcm of two positive integers -> use `g*l=ab` before casework.

---

## 10. PYQ ANCHORS

- `IOQM-2025-Q02`: direct divisibility-counting anchor; year/Q provenance must remain attached.
- `IOQM-2025-Q27`: higher-ceiling lcm/gcd normalization anchor; independently verified.

Use the validated paper for exact historical wording.

---

## 11. TRANSFER

The same subtraction invariant appears later in:
- modular arithmetic (`a congruent b mod d` means `d|(a-b)`);
- Diophantine equations where a gcd must divide a linear combination;
- game invariants where parity or residue survives allowed moves.

The surface changes. The structural question does not:

> **What quantity remains divisible after I combine or subtract the conditions?**
