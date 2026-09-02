# Digits, Place Value & Base Structure

## The central habit
A digit pattern is an **integer written in a representation**. Translate the representation before guessing from examples.

`DIGITS -> PLACE VALUE -> ARITHMETIC RESTRICTION -> CHECK`

If the final question asks for a number of admissible strings, derive the arithmetic restriction here first; then use counting tools.

## 1. Digits are coefficients of powers of the base
The decimal numeral `abc` means

`100a+10b+c`.

The base-`b` numeral `d_k...d_1d_0` means

`d_k b^k+...+d_1 b+d_0`, with `0<=d_i<b` and leading digit nonzero.

This simple translation is the first line for most digit problems.

## 2. Divisibility by 9 comes from place value
Because `10` leaves remainder 1 on division by 9, every power `10^k` does too. Thus a decimal number and its digit sum have the same remainder modulo 9.

For `abcd`,

`1000a+100b+10c+d` has the same remainder as `a+b+c+d` modulo 9.

The rule is not magic; it is place value collapsing.

## 3. Divisibility by 11 alternates
Here `10` leaves remainder `-1` modulo 11. Powers alternate: `10^0,10^1,10^2,...` behave like `1,-1,1,-1,...`.

So `abcd` has the same remainder as

`-a+b-c+d` modulo 11.

A four-digit palindrome `abba` therefore has alternating sum zero, so it is automatically divisible by 11.

## 4. Concatenation is block place value
If block `x` is followed by a `k`-digit block `y`, then

`N=10^k x+y`.

Two two-digit blocks: `100x+y`. A three-digit block repeated twice: `1000x+x=1001x`.

This is usually cheaper than expanding individual digits.

Historical pattern: if a two-digit `p` is followed by a two-digit `q`, then `N=100p+q`. If the divisor is `p+q`, rewrite

`N=99p+(p+q)`.

Now the divisibility condition is visible.

## 5. Carries control digit-sum changes
Let `t` be the number of trailing 9s in decimal `n`. Adding 1 turns those `t` nines into zeros and increases the preceding digit by 1. Therefore

`s(n+1)=s(n)+1-9t`.

If `t=0`, the digit sum rises by 1. If `t>=1`, it may fall sharply.

This replaces blind search with a carry invariant.

## 6. Digit products are prime-compatibility problems
For a nonzero digit product to be squarefree, no prime may appear twice in the combined prime factorisation of all non-one digits.

Consequences:
- digit 4,8,9 is impossible immediately because it already contains a square prime factor;
- repeating digit 6 is impossible because each 6 contributes factors 2 and 3;
- digits 2 and 6 cannot both appear because prime 2 repeats;
- digit 1 may repeat freely because it changes neither product nor prime exponents.

The squarefree theorem itself belongs to prime-exponent structure; here we use it to restrict digits.

## 7. Base representation works the same way
`352_7 = 3*7^2+5*7+2 = 184`.

For an unknown base, the numeral becomes an equation. If `111_b=31`, then

`b^2+b+1=31`,

so `b=5` after the base condition `b>1` is enforced.

Carries also generalize: in base 8, `777_8+1=1000_8`.

## 8. Arithmetic restriction vs counting
Suppose place value proves that a four-digit string must satisfy digit sum 12. The arithmetic work is now done. If the question asks **how many** such strings exist, define the admissible strings and count them using the counting toolkit.

Do not turn place-value derivation into a permutations chapter, and do not ask counting to rediscover divisibility rules.

## 9. Source-anchor recognition
- `abcab` type patterns: write the whole numeral algebraically before testing digits.
- `n` and `n+1` digit sums: count trailing 9s.
- concatenated two-digit blocks: use `100p+q` and reduce against the divisor structure.
- squarefree digit product: classify prime usage before maximizing digit count.

## Closing checks
Leading digit nonzero; every digit in the base range; carry length correct; block length correct in concatenation; divisibility condition applied to the value of the numeral; arithmetic restriction separated from any later counting step.
