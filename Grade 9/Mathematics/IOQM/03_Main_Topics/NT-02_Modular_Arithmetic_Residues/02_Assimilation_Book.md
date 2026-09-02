# Modular Arithmetic, Residues & Power Cycles - Assimilation Book

## 1. RECONNECT - from divisibility to congruence

From prior divisibility work, `m|(a-b)` means `a` and `b` differ by a multiple of `m`. Modular arithmetic compresses that into

`a congruent b (mod m)`.

It means **same remainder modulo m**, not ordinary equality.

Example: `17 congruent 5 (mod 12)` because `12|(17-5)`.

### Contrast: equality vs congruence

`17` is not equal to `5`, but they are congruent modulo 12. Equality is exact; congruence depends on a chosen modulus.

## 2. DISCOVER - residues are states

Modulo 7 every integer belongs to one of seven states: `0,1,2,3,4,5,6`. You may replace a number by any congruent representative when using legal operations.

If `a congruent b (mod m)` and `c congruent d (mod m)`, then:

- `a+c congruent b+d`;
- `a-c congruent b-d`;
- `ac congruent bd`;
- positive integer powers preserve congruence.

So reduce early: `1234567 mod 9` may be replaced by its residue before further modular arithmetic.

## 3. MAKE SENSE - cancellation is conditional

From `ac congruent bc (mod m)`, cancellation of c is safe modulo m when `gcd(c,m)=1`, because c then has a modular inverse.

Counterexample: `2*1 congruent 2*4 (mod 6)` since `2 congruent 8 (mod 6)`, but `1` is not congruent to `4 (mod 6)`. The cancelled factor 2 is not invertible mod 6.

If `3x congruent 6 (mod 7)`, inverse of 3 mod 7 is 5, so `x congruent 30 congruent 2 (mod 7)`.

> Never write modular division before asking: **is the divisor invertible modulo m?**

## 4. Power cycles

Compute only enough powers to see repetition.

Modulo 7:

`2^1,2^2,2^3,...` gives residues `2,4,1,2,4,1,...`.

So `2^100 mod 7` uses `100 mod 3 = 1`, hence residue 2.

For last digits, choose the modulus from the target:

- last digit -> mod 10;
- last two digits -> mod 100.

The 2024 anchor `5^2024` stabilizes at 25 modulo 100 after exponent 2.

## 5. Base cycle and exponent cycle can both matter

For `n^n mod 7`, the base depends on `n mod 7`; for nonzero residues, the exponent can be reduced through a period dividing 6. A universal period must preserve **both** pieces of information. That produces the 2025 anchor period `lcm(7,6)=42`.

Do not blindly reduce the exponent modulo 6 when the base is divisible by 7; handle zero-residue cases explicitly.

## 6. Simultaneous congruences

Solve

`x congruent 2 (mod 3)` and `x congruent 3 (mod 5)`.

Numbers in the first class are `2,5,8,11,...`; 8 is the first also congruent to 3 mod 5. Solutions repeat every 15:

`x congruent 8 (mod 15)`.

With non-coprime moduli, consistency matters. Example:

`x congruent 1 (mod 4)`, `x congruent 3 (mod 6)` has solution `x congruent 9 (mod 12)`.

But `x congruent 1 (mod 4)`, `x congruent 2 (mod 6)` is impossible because the requested residues disagree modulo `gcd(4,6)=2`.

At Grade-9 depth, listing or parametrizing one congruence and checking the other is often cheaper than quoting a general theorem.

## 7. TRY - attempt before help

### Track A - meaning
Show `83 congruent 11 (mod 12)`.
- Full support: subtract and show divisibility by 12.
- Medium support: same remainder means difference divisible by modulus.
- Light support: compare remainders.
- Independent: decide whether `137 congruent 5 (mod 11)`.

### Track B - cycle
Find `3^100 mod 7`.
- Full support: list residues of `3,3^2,...` until 1 returns; use exponent modulo cycle length.
- Medium support: find the cycle before touching exponent 100.
- Light support: huge power -> small repeated residue state.
- Independent: find the last digit of `7^2026`.

### Track C - cancellation
Solve `4x congruent 3 (mod 7)`.
- Full support: inverse of 4 mod 7 is 2; multiply both sides.
- Medium support: test gcd(4,7)=1, then invert.
- Light support: cancellation/division requires invertibility.
- Independent: analyze `6x congruent 9 (mod 15)` without illegal cancellation.

### Track D - simultaneous congruences
Solve `x congruent 1 (mod 4)`, `x congruent 4 (mod 5)`.
- Full support: write x=1+4k and test modulo 5.
- Medium support: parametrize one residue class.
- Light support: combine two repeating lists.
- Independent: solve `x congruent 2 (mod 6)`, `x congruent 5 (mod 9)` or prove impossible.

## 8. DIAGNOSE

- **Equality reflex:** congruent numbers need not be equal.
- **Divisibility reflex:** `a congruent b` is a statement about `a-b`, not only about either number separately.
- **Expansion reflex:** large powers usually call for a cycle.
- **Cancellation reflex:** common factor does not automatically cancel modulo m.
- **Wrong modulus:** last two digits are mod 100, not mod 10.
- **CRT reflex:** simultaneous congruences may be incompatible when moduli share factors.

## 9. ADOPT - six mental rules

1. `a congruent b (mod m)` means `m|(a-b)`.
2. Reduce residues early under legal operations.
3. Addition, subtraction and multiplication are safe; division is conditional.
4. A factor is invertible mod m exactly when its gcd with m is 1.
5. Huge powers -> search for a cycle before expanding.
6. Multiple congruences -> check compatibility, then find the repeating combined class.

## 10. TRANSFER

Residues later become:
- last-digit and place-value filters in later number-theory work;
- parity/residue invariants in later combinatorial work;
- finite states in cyclic processes;
- collision detectors: two values share a residue iff their difference is divisible by the modulus.
