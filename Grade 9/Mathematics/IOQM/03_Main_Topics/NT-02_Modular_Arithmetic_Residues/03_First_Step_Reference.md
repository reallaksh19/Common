# Modular Arithmetic, Residues & Power Cycles - First-Step Reference

## Recognition atlas

| Clue | First move |
|---|---|
| same remainder / congruent | write modulus divides the difference |
| huge power modulo m | reduce base; look for a short cycle first |
| huge power with `gcd(base,m)=1` and no short visible cycle | consider Euler's theorem after checking coprimality |
| prime modulus `p`, base not divisible by `p` | Fermat's little theorem may be a compact prime-modulus companion |
| last digit | work mod 10 |
| last two digits | work mod 100 |
| modular equation with a coefficient | test whether the coefficient is invertible |
| two congruences | parametrize one class, then test the other |
| shared-factor moduli | check compatibility modulo their gcd first |

## Legal-operation checklist

From `a congruent b (mod m)` you may safely add, subtract, multiply and take positive integer powers. Division or cancellation needs an invertible factor.

Before cancelling `c` from `ac congruent bc (mod m)`, check `gcd(c,m)=1`.

## Power-cycle checklist

1. Choose the modulus from the target.
2. Reduce the base.
3. List powers only until the residue state repeats.
4. Reduce the exponent by the justified cycle length.
5. Handle zero/non-invertible residue cases separately when needed.
6. If a short cycle is already visible, do not replace it with a heavier theorem just because the exponent is large.

## Euler's theorem - bounded Grade-9 bridge

For a positive integer `n`, let `phi(n)` mean the number of integers among `1,2,...,n` that are coprime to `n`.

If

`gcd(a,n)=1`,

then Euler's theorem gives

`a^phi(n) congruent 1 (mod n)`.

### Why the coprimality condition matters

The theorem is about **invertible residue classes**. If `gcd(a,n)>1`, do not reduce exponents using Euler's theorem.

Example of illegal use: modulo 8, `a=2` is not coprime to 8. Euler gives no permission to replace `2^k` by a period based on `phi(8)`.

### Grade-9 proof idea

Take the residues in `1,...,n` that are coprime to `n`. Multiplying all of them by `a` merely permutes those coprime residue classes because `a` has an inverse modulo `n`. Therefore the product before and after multiplication is congruent. Cancelling the coprime product leaves

`a^phi(n) congruent 1 (mod n)`.

This is a proof idea, not a request to build a full theory of the totient function.

### Decision boundary: cycle or Euler?

- If powers quickly show a short period, use the visible cycle.
- If the modulus/base are coprime and Euler gives a clean exponent reduction, it may be cheaper.
- Always check `gcd(a,n)=1` before invoking Euler.

Example: `3^100 mod 7` has an obvious cycle of length 6 (indeed order 6), so either route works; listing the short cycle is usually more transparent.

## Fermat's little theorem - prime-modulus companion

This is included as a curriculum-design companion to the source-requested Euler bridge.

If `p` is prime and `p` does not divide `a`, then

`a^(p-1) congruent 1 (mod p)`.

It is the prime-modulus special case of the same coprime-power principle because `phi(p)=p-1`.

**Hypothesis check:** if `p|a`, the theorem is not the right statement; the residue is already `0 mod p` for positive powers.

## Simultaneous-congruence checklist

1. Check compatibility if moduli share factors.
2. Write one congruence as a parametrized class.
3. Substitute into the other congruence.
4. State the combined repeating class and its period.

## WHY-NOT reminders

- Congruence is not ordinary equality.
- A common factor does not always cancel.
- A large exponent is not a signal to expand.
- Euler/Fermat are not licenses to ignore coprimality.
- A short visible power cycle can be cheaper and more informative than a named theorem.
- The target determines the modulus; do not default to mod 10.
