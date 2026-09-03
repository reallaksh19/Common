# Prime Factorisation, Divisors & Perfect Powers
## First-Step Reference

### One-line router

`FACTOR / INFER EXPONENTS -> TRANSLATE TARGET -> COUNT OR RECONSTRUCT -> CHECK`

| Visible clue | First mathematical line |
|---|---|
| "number of divisors" | write `n=prod p_i^{a_i}` and `tau(n)=prod(a_i+1)` |
| "perfect square" | require every `a_i` even |
| "perfect cube" | require every `a_i` divisible by 3 |
| "greatest perfect-power exponent" | compute `gcd(a_1,...,a_r)` |
| "squarefree" | require every exponent `0` or `1` |
| "divides n!" | compare `v_p(candidate)` with `v_p(n!)` |
| "factor pairs" | pair complementary exponent choices |
| `xy=N`, `gcd(x,y)=1` | assign each complete prime-power block to one side |
| `tau(n)` odd | test whether `n` is a square |
| "smallest n with tau(n)=K" | factor `K` into `(a_i+1)` patterns |
| "divisors of n^2 below n" | pair divisors around `n` first |
| "sum of at least two consecutive positive integers" | ask whether `n` has an odd divisor greater than `1`; equivalently, whether `n` is not a power of `2` |

## Consecutive sums: the divisor structure

Suppose

`n = a+(a+1)+...+(a+r-1)`

with integers `a>=1` and `r>=2`.

Then

`n = r(2a+r-1)/2`,

so

`2n = r(2a+r-1)`.

The two factors on the right have opposite parity because their difference is

`(2a+r-1)-r = 2a-1`,

which is odd.

This exposes the governing structural fact:

> A positive integer can be written as a sum of at least two consecutive positive integers **iff it is not a power of 2**.

Equivalent form:

> Such a representation exists **iff `n` has an odd divisor greater than `1`**.

### Why powers of 2 fail

If `n=2^m`, then `2n` has no odd factor greater than `1`. In the factorization `2n=r(2a+r-1)`, exactly one factor is odd. The only available positive odd factor is `1`, which forces the other structural parameter into the trivial one-term case rather than `r>=2`.

### Why an odd divisor gives a representation

If `n` has an odd divisor `d>1`, then the factorization of `2n` supplies a pair of opposite-parity factors. One can choose the factor order so that the resulting

`a = ((2n/r)-r+1)/2`

is integral; if a direct choice gives nonpositive `a`, swap to the complementary factor where appropriate. NT-04 owns the detailed reconstruction, positivity and length filtering.

### Decision boundary

- If the question asks only **whether a representation exists**, use the odd-divisor / power-of-two characterization here.
- If it asks for the actual number of terms, starting value, all representations, or imposes bounds/positivity restrictions, route to NT-04 reconstruction.

## Close contrasts

- gcd/lcm target -> retrieve gcd/lcm structure; multiplicity target -> exponent vector.
- square -> all exponents even; squarefree -> all exponents at most 1.
- count divisors -> independent exponent choices; count factor pairs -> complementary choices.
- candidate divides factorial -> valuation; last digits of factorial -> modular machinery elsewhere.
- minimize number with fixed `tau` -> exponent pattern + ordered primes; merely compute `tau` -> no minimization.
- consecutive-sum **existence** -> odd-divisor/power-of-two structure; actual sequence reconstruction -> NT-04.

## Checks

1. Did every prime appearing in the number appear in the vector?
2. Did you accidentally use a square criterion for a cube or vice versa?
3. For `gcd(x,y)=1`, did any prime enter both factors?
4. For an extremal construction, did a larger exponent land on a larger prime?
5. For a consecutive-sum claim, did you distinguish `r>=2` and positive starting term from a trivial one-term representation?
6. For historical source work, did you use the validated statement and key status?
